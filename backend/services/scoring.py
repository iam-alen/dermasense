from typing import List
from pydantic import BaseModel
from data.ingredients import INGREDIENTS

class Profile(BaseModel):
    skin_type: str = "Combination"
    concerns: List[str] = []
    allergies: List[str] = []
    avoid: List[str] = []

class ProductIn(BaseModel):
    ingredients: str
    profile: Profile

def found(text: str):
    t = text.lower()
    return [k for k in INGREDIENTS if k in t]

def score_product(text: str, p: Profile):
    score, good, bad = 60, [], []
    for ing in found(text):
        helps, risky, note = INGREDIENTS[ing]
        hit = [c for c in p.concerns if c in helps]
        if hit: score += 10 * len(hit); good.append(f"{ing.title()} helps with {', '.join(hit).lower()}. {note}")
        if p.skin_type in risky: score -= 14; bad.append(f"{ing.title()}: {note}")
        elif ing in ("fragrance", "parfum"): score -= 6; bad.append(f"{ing.title()}: {note}")
    for word in p.allergies + p.avoid:
        if word.strip() and word.strip().lower() in text.lower():
            score -= 40; bad.append(f"Contains {word.strip()}, which you listed to avoid.")
    score = max(0, min(100, score))
    verdict = "Great match" if score >= 75 else "Okay, with care" if score >= 50 else "Skip this one"
    return {"score": score, "verdict": verdict, "why_good": good, "why_not": bad}

