import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/api/skin/analyze")
async def skin_analyze(file: UploadFile = File(...)):
    import cv2
    img = cv2.imdecode(np.frombuffer(await file.read(), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(400, "That file isn't a readable image. Try a JPG or PNG.")
    h, w = img.shape[:2]
    face, ratio = img[h // 6: 5 * h // 6, w // 4: 3 * w // 4], 1.3
    try:
        import mediapipe as mp
        with mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as fm:
            res = fm.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not res.multi_face_landmarks:
            raise HTTPException(422, "No face found. Use a front-facing photo in daylight.")
        pts = np.array([[p.x * w, p.y * h] for p in res.multi_face_landmarks[0].landmark])
        x0, y0 = pts.min(0).astype(int).clip(0)
        x1, y1 = pts.max(0).astype(int)
        face, ratio = img[y0:y1, x0:x1], (y1 - y0) / max(x1 - x0, 1)
    except ImportError:
        pass  # falls back to centre crop
    lab = cv2.cvtColor(face, cv2.COLOR_BGR2LAB).astype(float)
    hsv = cv2.cvtColor(face, cv2.COLOR_BGR2HSV)
    L, A = lab[..., 0] * 100 / 255, lab[..., 1] - 128
    tone = "Fair" if L.mean() > 68 else "Medium" if L.mean() > 52 else "Deep"
    shine = float(((hsv[..., 2] > 240) & (hsv[..., 1] < 60)).mean())
    skin_type = "Oily" if shine > 0.06 else "Combination" if shine > 0.02 else "Dry/Normal"
    acne = float((A > A.mean() + 2.2 * A.std()).mean())
    spots = float((L < L.mean() - 2 * L.std()).mean())
    concerns = []
    if acne > 0.025: concerns.append("Acne")
    if spots > 0.03: concerns.append("Dark spots")
    if A.mean() > 12: concerns.append("Redness")
    shape = "Oblong" if ratio > 1.45 else "Oval" if ratio > 1.3 else "Round/Square"
    return {"skin_tone": tone, "skin_type": skin_type, "face_shape": shape, "concerns": concerns,
            "note": "Heuristic estimate. Swap in a trained CNN for clinical-grade accuracy."}

