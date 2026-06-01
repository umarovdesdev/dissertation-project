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
    """GET /api/health payload."""

    status: str
    model: str
    checkpoint: str
    checkpoint_loaded: bool
    device: str
