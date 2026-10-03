from typing import Optional
from fastapi import APIRouter
from data.remedies import REMEDIES, AVOID, RED_FLAGS

router = APIRouter()

@router.get("/api/remedies")
def remedies(q: str, product: Optional[str] = ""):
    q = q.lower()
    hits = [{"concern": c, **d} for c, d in REMEDIES.items() if any(k in q for k in d["keys"])]
    return {"stop_product": f"Stop using {product or 'the product'} until your skin settles.",
            "matches": hits, "avoid": AVOID, "see_doctor_if": RED_FLAGS,
            "disclaimer": "General guidance, not a diagnosis. Patch-test any remedy on your inner arm first."}

