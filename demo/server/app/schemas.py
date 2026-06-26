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


class StageSlide(BaseModel):
    """One preprocessing-stage result, rendered as its own slide in the demo.

    ``key`` is the raw stage label from ``stage_breakdown`` (e.g.
    ``fov_crop_resize``); ``caption`` is the human-readable title; ``png_b64``
    is the base64 PNG of that stage's output image. ``channels`` is that stage's
    R/G/B/FOV decomposition (also ``StageSlide`` items) — empty for slides that
    are themselves a single channel (e.g. the standalone FOV-mask slide).
    """

    key: str
    caption: str
    png_b64: str
    channels: list["StageSlide"] = []


class ODFoveaPayload(BaseModel):
    """Learned OD/fovea detection result (TASK-Demo §C.1; Phase 3).

    Coordinates are in the **flipped (pre-rotation) frame** described by
    ``space_w``/``space_h``/``flipped`` — i.e. the canonical-flip image
    (``flipped`` False because the base image, ``detect_base_png_b64``, is
    already flipped). The OD–fovea axis is shown at its true tilt here; the
    Stage-1 rotation slide is what levels it.

    The ``od_confidence``/``fovea_confidence`` fields and the base64 heatmap
    PNGs are additive (Phase 3): the genuine per-landmark confidence from the
    learned detector, and translucent RGBA probability-map overlays aligned to
    the same flipped frame. Heatmap strings are empty when no detection /
    heatmaps are available.
    """

    od_center: list[float]
    od_radius: float
    fovea_center: list[float]
    fovea_radius: float
    angle_deg: float
    rotation_sigma_deg: float
    confident: bool
    space_w: int
    space_h: int
    flipped: bool
    od_confidence: float = 0.0
    fovea_confidence: float = 0.0
    od_heatmap_png_b64: str = ""
    fovea_heatmap_png_b64: str = ""


class ODFoveaCorrectionResponse(BaseModel):
    """POST /api/od_fovea/correct payload (Phase 3).

    Echoes the corrected OD/fovea overlay back in the same flipped frame the
    frontend edits in, *plus* the full re-run of the pipeline driven by the
    correction: the recomputed rotation and every downstream stage. The frontend
    swaps these in so the whole step-by-step view updates. ``stored`` is ``True``
    when the correction was persisted to the feedback store (Phase 4), with
    ``record_id`` its content-hash key.
    """

    od_fovea: ODFoveaPayload
    stored: bool
    record_id: str
    # Full re-run of the pipeline from the corrected centres (mirrors
    # VisualizeResponse), so the detailed view refreshes after a Save correction.
    fov_mask_png_b64: str = ""
    fov_base_png_b64: str = ""
    detect_base_png_b64: str = ""
    stages: list[StageSlide] = []


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
    fov_base_png_b64: str
    # Un-rotated canonical-flip RGB the OD/fovea detection overlay aligns to.
    detect_base_png_b64: str = ""
    preview_png_b64: str
    od_fovea: ODFoveaPayload
    # Per-stage slides (original → flip → rotation → crop → flat-field → CLAHE
    # → FOV mask) for the step-by-step detailed view; each carries its R/G/B/FOV
    # channel decomposition in ``channels``.
    stages: list[StageSlide] = []


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
