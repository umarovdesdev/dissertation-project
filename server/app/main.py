"""FastAPI app: endpoints + startup model load.

Run locally:
    uvicorn server.app.main:app --reload --port 8000
"""

from __future__ import annotations

import asyncio

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .gradcam import compute_gradcam
from .inference import engine
from .schemas import HealthResponse, PatientPredictionResponse

app = FastAPI(title="DR-Classifier Demo API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single CUDA stream → serialize predictions to avoid races on one GPU.
_predict_lock = asyncio.Lock()


@app.on_event("startup")
async def _startup() -> None:
    """Load the model once when the server boots."""
    engine.load()
    if not engine.checkpoint_loaded:
        print(f"[WARN] checkpoint not found at {settings.checkpoint_path} — "
              "predictions will use random-init weights until one is provided.")
    if not engine.using_dataset_stats:
        print(f"[WARN] norm stats not found at {settings.norm_stats_path} — "
              "Stage 7 falls back to ImageNet (preprocessing drift vs Config D).")


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness + provenance for the frontend badge."""
    return HealthResponse(
        status="ok",
        model="config-D",
        checkpoint=settings.checkpoint_id,
        checkpoint_loaded=engine.checkpoint_loaded,
        device=str(engine.device),
    )


@app.post("/api/predict", response_model=PatientPredictionResponse)
async def predict(
    left: UploadFile | None = File(default=None),
    right: UploadFile | None = File(default=None),
) -> PatientPredictionResponse:
    """Predict DR grade for one or both eyes (worst-eye patient grade).

    Args:
        left: Optional left-eye image upload.
        right: Optional right-eye image upload.

    Returns:
        Patient-level prediction with per-eye breakdown.
    """
    if left is None and right is None:
        raise HTTPException(status_code=400, detail="Provide at least one of left/right.")

    left_bytes = await left.read() if left is not None else None
    right_bytes = await right.read() if right is not None else None

    try:
        async with _predict_lock:
            return engine.predict_patient(left_bytes, right_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/gradcam")
async def gradcam(
    eye: str = "left",
    image: UploadFile = File(...),
) -> dict:
    """Grad-CAM overlay for one eye (scaffold → 501)."""
    image_bytes = await image.read()
    try:
        return compute_gradcam(image_bytes, eye)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
