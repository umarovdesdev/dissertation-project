"""FastAPI app: endpoints + startup model load.

Run locally:
    uvicorn server.app.main:app --reload --port 8000
"""

from __future__ import annotations

import asyncio

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from . import corrections as corrections_mod
from . import gradcam as gradcam_mod
from . import imaging
from . import visualize as visualize_mod
from .config import settings
from .inference import engine
from .schemas import (
    AuthResponse,
    GradcamResponse,
    HealthResponse,
    ODFoveaCorrectionResponse,
    PatientPredictionResponse,
    SelftestResponse,
    VisualizeResponse,
)
from .security import check_password, password_required

app = FastAPI(title="DR-Classifier Demo API", version=settings.resolve_version())

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single CUDA stream → serialize predictions to avoid races on one GPU.
_predict_lock = asyncio.Lock()

# Map imaging-layer exceptions to HTTP status codes (TASK-Demo §C.4).
_IMAGING_STATUS = {
    imaging.PayloadTooLarge: 413,
    imaging.UnsupportedMedia: 415,
    imaging.BadImage: 400,
}


def _http_from_imaging(exc: Exception) -> HTTPException:
    """Translate an imaging exception into an HTTPException."""
    for cls, status in _IMAGING_STATUS.items():
        if isinstance(exc, cls):
            return HTTPException(status_code=status, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))


def _require_password(password: str | None) -> None:
    """Enforce the shared-password gate (TASK-Demo §C.2)."""
    if not check_password(password):
        raise HTTPException(status_code=401, detail="Access denied — invalid password.")


async def _read_validated(upload: UploadFile) -> bytes:
    """Read an upload and validate MIME + size before decoding.

    Args:
        upload: The incoming file.

    Returns:
        The raw bytes.

    Raises:
        HTTPException: 413/415 on limit violations.
    """
    data = await upload.read()
    try:
        imaging.check_upload(upload.content_type, len(data))
    except (imaging.PayloadTooLarge, imaging.UnsupportedMedia) as exc:
        raise _http_from_imaging(exc) from exc
    return data


@app.on_event("startup")
async def _startup() -> None:
    """Load the model once when the server boots."""
    engine.load()
    if not engine.checkpoint_loaded:
        print(f"[WARN] checkpoint not found at {settings.checkpoint_path} — "
              "predictions use random-init weights until one is provided.")
    if not engine.using_dataset_stats:
        print(f"[WARN] norm stats not found at {settings.norm_stats_path} — "
              "Stage 7 falls back to ImageNet (preprocessing drift vs Config D).")


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness + provenance for the frontend badge/footer."""
    return HealthResponse(
        status="ok",
        model="config-D",
        checkpoint=settings.checkpoint_id,
        checkpoint_loaded=engine.checkpoint_loaded,
        device=str(engine.device),
        version=settings.resolve_version(),
        git_sha=settings.resolve_git_sha(),
        requires_password=password_required(),
    )


@app.post("/api/auth", response_model=AuthResponse)
async def auth(password: str | None = Form(default=None)) -> AuthResponse:
    """Validate the shared password for the frontend access screen (§C.2).

    Returns ``{ "ok": true }`` when the gate is open or the password matches;
    raises 401 otherwise. Stateless — the frontend re-sends the password on
    every protected request regardless.
    """
    _require_password(password)
    return AuthResponse(ok=True)


@app.post("/api/predict", response_model=PatientPredictionResponse)
async def predict(
    left: UploadFile | None = File(default=None),
    right: UploadFile | None = File(default=None),
    password: str | None = Form(default=None),
) -> PatientPredictionResponse:
    """Predict DR grade for one or both eyes (worst-eye patient grade)."""
    _require_password(password)
    if left is None and right is None:
        raise HTTPException(status_code=400, detail="Provide at least one of left/right.")

    left_bytes = await _read_validated(left) if left is not None else None
    right_bytes = await _read_validated(right) if right is not None else None

    try:
        async with _predict_lock:
            return engine.predict_patient(left_bytes, right_bytes)
    except (imaging.BadImage, imaging.PayloadTooLarge, imaging.UnsupportedMedia) as exc:
        raise _http_from_imaging(exc) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/gradcam", response_model=GradcamResponse)
async def gradcam(
    image: UploadFile = File(...),
    eye: str = Form(default="left"),
    password: str | None = Form(default=None),
    target_class: int | None = Form(default=None),
) -> GradcamResponse:
    """Grad-CAM overlay for one eye, computed on the live checkpoint."""
    _require_password(password)
    data = await _read_validated(image)
    try:
        async with _predict_lock:
            return GradcamResponse(**gradcam_mod.compute_gradcam(engine, data, eye, target_class))
    except (imaging.BadImage, imaging.PayloadTooLarge) as exc:
        raise _http_from_imaging(exc) from exc


@app.post("/api/visualize", response_model=VisualizeResponse)
async def visualize(
    image: UploadFile = File(...),
    eye: str = Form(default="left"),
    password: str | None = Form(default=None),
) -> VisualizeResponse:
    """preview strip + FOV mask + OD/fovea payload for one image."""
    _require_password(password)
    data = await _read_validated(image)
    try:
        return VisualizeResponse(**visualize_mod.compute_visualization(engine, data, eye))
    except (imaging.BadImage, imaging.PayloadTooLarge) as exc:
        raise _http_from_imaging(exc) from exc


_MIME_EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}


@app.post("/api/od_fovea/correct", response_model=ODFoveaCorrectionResponse)
async def od_fovea_correct(
    image: UploadFile = File(...),
    eye: str = Form(default="left"),
    od_x: float = Form(...),
    od_y: float = Form(...),
    fovea_x: float = Form(...),
    fovea_y: float = Form(...),
    od_confidence: float = Form(default=0.0),
    fovea_confidence: float = Form(default=0.0),
    notes: str | None = Form(default=None),
    reviewer: str | None = Form(default=None),
    password: str | None = Form(default=None),
) -> ODFoveaCorrectionResponse:
    """Persist a clinician OD/fovea correction and echo the updated overlay.

    Corrected centres arrive in the analysis frame (where the frontend edits).
    The overlay geometry is recomputed from them, and they are mapped back to
    original-image pixels for the Phase-4 feedback store (the original image is
    saved once, content-addressed by SHA-256).
    """
    _require_password(password)
    data = await _read_validated(image)
    try:
        async with _predict_lock:
            result = visualize_mod.compute_correction(
                engine, data, eye, (od_x, od_y), (fovea_x, fovea_y)
            )
    except (imaging.BadImage, imaging.PayloadTooLarge) as exc:
        raise _http_from_imaging(exc) from exc

    image_hash = imaging.sha256_hex(data)
    ext = _MIME_EXT.get((image.content_type or "").split(";")[0].strip().lower(), "png")
    record = {
        "eye": eye,
        "od_center_analysis": [od_x, od_y],
        "fovea_center_analysis": [fovea_x, fovea_y],
        "space_w": result["od_fovea"]["space_w"],
        "space_h": result["od_fovea"]["space_h"],
        "od_center_original": result["original"]["od_center"],
        "fovea_center_original": result["original"]["fovea_center"],
        "original_w": result["original"]["space_w"],
        "original_h": result["original"]["space_h"],
        "od_confidence_at_capture": od_confidence,
        "fovea_confidence_at_capture": fovea_confidence,
        "reviewer": reviewer,
        "notes": notes,
    }
    try:
        record_id = corrections_mod.save_correction(
            settings.corrections_dir, record, data, image_hash, image_ext=ext
        )
        stored = True
    except OSError as exc:  # store is best-effort: never fail the correction
        print(f"[WARN] could not persist OD/fovea correction: {exc}")
        record_id, stored = image_hash, False

    return ODFoveaCorrectionResponse(
        od_fovea=result["od_fovea"], stored=stored, record_id=record_id
    )


@app.get("/api/selftest", response_model=SelftestResponse)
async def selftest(password: str | None = Query(default=None)) -> SelftestResponse:
    """Run predict + gradcam + visualize on synthetic fundus images (§C.7)."""
    _require_password(password)
    from .selftest import run_selftest
    return SelftestResponse(**run_selftest(engine))
