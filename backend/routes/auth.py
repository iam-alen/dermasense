import sqlite3, hashlib, secrets, os
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth")
DB = os.path.join(os.path.dirname(__file__), "..", "dermasense.db")

def db():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    c.execute("create table if not exists users(id integer primary key, name text, email text unique, pw text, salt text)")
    c.execute("create table if not exists sessions(token text primary key, user_id integer)")
    return c

def hash_pw(pw, salt):
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 100_000).hex()

def new_session(c, uid):
    t = secrets.token_hex(24); c.execute("insert into sessions values(?,?)", (t, uid)); c.commit(); return t

class Signup(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(b: Signup):
    if "@" not in b.email or len(b.password) < 8 or not b.name.strip():
        raise HTTPException(422, "Enter your name, a valid email and a password of at least 8 characters.")
    c, salt = db(), secrets.token_hex(8)
    try:
        cur = c.execute("insert into users(name,email,pw,salt) values(?,?,?,?)",
                        (b.name.strip(), b.email.lower(), hash_pw(b.password, salt), salt))
    except sqlite3.IntegrityError:
        raise HTTPException(409, "That email already has an account. Try logging in.")
    return {"token": new_session(c, cur.lastrowid), "name": b.name.strip()}

@router.post("/login")
def login(b: Login):
    c = db(); u = c.execute("select * from users where email=?", (b.email.lower(),)).fetchone()
    if not u or hash_pw(b.password, u["salt"]) != u["pw"]:
        raise HTTPException(401, "Email or password doesn't match.")
    return {"token": new_session(c, u["id"]), "name": u["name"]}

@router.get("/me")
def me(authorization: str = Header("")):
    c = db()
    u = c.execute("select name,email from users where id=(select user_id from sessions where token=?)",
                  (authorization.replace("Bearer ", ""),)).fetchone()
    if not u: raise HTTPException(401, "Please log in again.")
    return dict(u)
