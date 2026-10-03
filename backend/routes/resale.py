import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scoring import Profile, score_product

router = APIRouter()

BANNED = ["mascara", "eyeliner", "lip gloss", "lipstick", "kajal", "eye pencil"]
LISTINGS: list = []

class ListingIn(BaseModel):
    name: str
    category: str
    packaging: str  # pump | tube | sealed | jar
    uses: int = 0
    original_price: float
    months_left: int = 12
    ingredients: str = ""

def evaluate(l: ListingIn):
    c = l.category.lower() + " " + l.name.lower()
    if any(b in c for b in BANNED):
        return False, "Eye and lip products can't be resold for hygiene reasons."
    if l.packaging == "jar" and l.uses > 0:
        return False, "Used jars can't be resold. Only pump, tube or sealed packs."
    if l.packaging != "sealed" and l.uses > 3:
        return False, "Products used more than 3 times can't be listed."
    if l.months_left < 3:
        return False, "Less than 3 months of shelf life left."
    return True, "Eligible"

def price(l: ListingIn):
    f = 0.7 if l.packaging == "sealed" else max(0.35, 0.6 - 0.07 * l.uses)
    return round(l.original_price * f * min(1, 0.5 + l.months_left / 24), 2)

@router.post("/api/listings")
def add_listing(l: ListingIn):
    ok, reason = evaluate(l)
    if not ok: raise HTTPException(422, reason)
    item = {"id": uuid.uuid4().hex[:8], **l.dict(), "price": price(l)}
    LISTINGS.append(item)
    return item

@router.post("/api/price-estimate")
def estimate(l: ListingIn):
    ok, reason = evaluate(l)
    return {"eligible": ok, "reason": reason, "price": price(l) if ok else None}

@router.post("/api/listings/match")
def match(p: Profile):
    return [{**i, "match": score_product(i["ingredients"], p)} for i in LISTINGS]
