"""Run from this folder:  uvicorn main:app --reload   then open http://localhost:8000"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import auth, skin, product, remedies, resale

app = FastAPI(title="DermaSense")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
for module in (auth, skin, product, remedies, resale):
    app.include_router(module.router)
FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="site")
