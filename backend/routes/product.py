import re
import numpy as np
from typing import List
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from data.ingredients import CONFLICTS
from services.scoring import Profile, ProductIn, found, score_product

router = APIRouter()

@router.post("/api/product/analyze")
def product_analyze(body: ProductIn):
    return score_product(body.ingredients, body.profile)

@router.post("/api/product/ocr")
async def product_ocr(file: UploadFile = File(...)):
    import cv2, easyocr  # pip install easyocr
    img = cv2.imdecode(np.frombuffer(await file.read(), np.uint8), cv2.IMREAD_COLOR)
    text = " ".join(easyocr.Reader(["en"], gpu=False).readtext(img, detail=0))
    m = re.search(r"ingredients?[:\s]+(.*)", text, re.I | re.S)
    return {"ingredients": (m.group(1) if m else text)[:1500]}

class ConflictIn(BaseModel):
    products: List[str]

@router.post("/api/conflicts")
def conflicts(body: ConflictIn):
    sets = [set(found(p)) for p in body.products]
    out = []
    for i, a in enumerate(sets):
        for j, b in enumerate(sets):
            if i < j:
                for x, y, msg in CONFLICTS:
                    if (a & x and b & y) or (b & x and a & y): out.append(msg)
    return {"conflicts": sorted(set(out))}

@router.post("/api/routine")
def routine(p: Profile):
    am = ["Gentle cleanser", "Hydrating serum" if "Dryness" in p.concerns else "Niacinamide serum",
          "Lightweight moisturiser" if p.skin_type == "Oily" else "Barrier cream", "SPF 30+"]
    pm = ["Gentle cleanser", "Retinol 2-3 nights a week" if "Acne" in p.concerns or "Dark spots" in p.concerns
          else "Ceramide serum", "Moisturiser"]
    return {"morning": am, "night": pm}

