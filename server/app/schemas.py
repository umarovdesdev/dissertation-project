"""Pydantic request/response models.

Response shapes intentionally mirror what ``Demo.js`` already renders
(``per_eye`` snake_case, probs as a 5-vector) so the frontend changes stay
minimal — see TASK-Config-D.md §B.3.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class EyePrediction(BaseModel):
    """Single-eye prediction."""

    eye: str = Field(..., description='"left" or "right"')
    pred: int = Field(..., ge=0, le=4, description="Predicted DR grade 0–4.")
    probs: list[float] = Field(..., min_length=5, max_length=5,
                               description="Softmax over the 5 DR grades.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="probs[pred].")
    latency_ms: int = Field(..., ge=0)


class PatientPredictionResponse(BaseModel):
    """Patient-level (worst-eye) prediction plus per-eye breakdown."""

    pred: int = Field(..., ge=0, le=4, description="Worst-eye DR grade.")
    probs: list[float] = Field(..., min_length=5, max_length=5,
                               description="Softmax of the worst eye.")
    confidence: float = Field(..., ge=0.0, le=1.0)
    latency_ms: int = Field(..., ge=0)
    per_eye: list[EyePrediction] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """GET /api/health payload (+ provenance for the demo footer, §D.7)."""

    status: str
    model: str
    checkpoint: str
    checkpoint_loaded: bool
    device: str
    version: str
    git_sha: str
    requires_password: bool


class ODFoveaPayload(BaseModel):
    """Classical-CV OD/fovea detection result (TASK-Demo §C.1).

    Coordinates are in the analysis-image pixel space described by
    ``space_w``/``space_h``/``flipped``.
    """

    od_center: list[int]
    od_radius: float
    fovea_center: list[int]
    fovea_radius: float
    angle_deg: float
    rotation_sigma_deg: float
    confident: bool
    space_w: int
    space_h: int
    flipped: bool


class GradcamResponse(BaseModel):
    """POST /api/gradcam payload."""

    gradcam_png_b64: str
    attention_overlay_png_b64: str
    target_class: int
    # Predicted-class rationale (TASK-Demo §D.3): a one-line sentence and the
    # CAM region statistics it is derived from. No LLM — pure CAM geometry.
    rationale: str
    cam_pixel_count: int
    cam_area_frac: float
    cam_region: str


class VisualizeResponse(BaseModel):
    """POST /api/visualize payload."""

    fov_mask_png_b64: str
    preview_png_b64: str
    od_fovea: ODFoveaPayload


class SelftestResponse(BaseModel):
    """GET /api/selftest payload — per-op pass/fail report (§C.7)."""

    predict: str
    gradcam: str
    visualize: str
    details: list[str] = []


class AuthResponse(BaseModel):
    """POST /api/auth payload — password-gate validation (§C.2).

    Used by the frontend access screen to validate the shared password before
    unlocking the demo body. A wrong password returns HTTP 401, not this shape.
    """

    ok: bool
