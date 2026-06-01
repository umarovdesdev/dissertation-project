"""Model loading + prediction.

Loads the Config D EfficientNet-B3 checkpoint once and runs the full V5
inference pipeline on raw upload bytes. Worst-eye aggregation gives the
patient-level grade.
"""

from __future__ import annotations

import io
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

# experiments/ is on sys.path via app/__init__.py
from src.models.factory import create_model

from .config import settings
from .preprocessing import build_inference_pipeline, load_norm_stats
from .schemas import EyePrediction, PatientPredictionResponse


class InferenceEngine:
    """Holds the loaded model + preprocessing pipeline for the server lifetime."""

    def __init__(self) -> None:
        self.device = torch.device(settings.resolve_device())
        self.model: torch.nn.Module | None = None
        self.checkpoint_loaded: bool = False
        self.using_dataset_stats: bool = load_norm_stats(settings.norm_stats_path) is not None

        self.pipeline = build_inference_pipeline(
            preset=settings.preset,
            norm_stats_path=settings.norm_stats_path,
            input_color_space="rgb",
        )

    def load(self) -> None:
        """Instantiate the model and load checkpoint weights (if present).

        Missing checkpoint is non-fatal: the server still boots and reports
        ``checkpoint_loaded=False`` via /api/health.
        """
        model = create_model(
            settings.model_name,
            {
                "pretrained": False,
                "num_classes": settings.num_classes,
                "dropout": 0.4,
                "in_channels": settings.in_channels,
            },
        )

        ckpt_path: Path = settings.checkpoint_path
        if ckpt_path.exists():
            ckpt = torch.load(str(ckpt_path), map_location="cpu", weights_only=False)
            state = ckpt.get("model_state_dict", ckpt)
            model.load_state_dict(state)
            self.checkpoint_loaded = True

        model.eval().to(self.device)
        self.model = model

    # ------------------------------------------------------------------

    def _decode_rgb(self, image_bytes: bytes) -> np.ndarray:
        """Decode raw bytes to an RGB uint8 array.

        Args:
            image_bytes: Raw uploaded file bytes.

        Returns:
            ``(H, W, 3)`` uint8 RGB array.

        Raises:
            ValueError: If the bytes are not a decodable image.
        """
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as exc:  # noqa: BLE001
            raise ValueError("Uploaded file is not a decodable image.") from exc
        return np.asarray(img, dtype=np.uint8)

    @torch.no_grad()
    def predict_eye(self, image_bytes: bytes, eye: str) -> EyePrediction:
        """Run the full pipeline + model on one eye.

        Args:
            image_bytes: Raw image bytes.
            eye: ``"left"`` or ``"right"`` (drives canonical flip).

        Returns:
            An :class:`EyePrediction`.

        Raises:
            RuntimeError: If the model has not been loaded.
            ValueError: If the image cannot be decoded.
        """
        if self.model is None:
            raise RuntimeError("Model not loaded — call load() at startup.")

        t0 = time.perf_counter()
        rgb = self._decode_rgb(image_bytes)
        tensor = self.pipeline(rgb, eye_side=eye)            # (4, 512, 512)
        batch = tensor.unsqueeze(0).to(self.device)          # (1, 4, 512, 512)

        logits = self.model(batch)                           # (1, 5)
        probs = F.softmax(logits, dim=1)[0].cpu().numpy()
        pred = int(np.argmax(probs))
        latency_ms = int((time.perf_counter() - t0) * 1000)

        return EyePrediction(
            eye=eye,
            pred=pred,
            probs=[float(p) for p in probs],
            confidence=float(probs[pred]),
            latency_ms=latency_ms,
        )

    def predict_patient(
        self,
        left_bytes: bytes | None,
        right_bytes: bytes | None,
    ) -> PatientPredictionResponse:
        """Predict per-eye and aggregate to a worst-eye patient grade.

        Args:
            left_bytes: Left-eye image bytes, or ``None``.
            right_bytes: Right-eye image bytes, or ``None``.

        Returns:
            A :class:`PatientPredictionResponse`.

        Raises:
            ValueError: If neither eye is provided.
        """
        t0 = time.perf_counter()
        per_eye: list[EyePrediction] = []
        if left_bytes is not None:
            per_eye.append(self.predict_eye(left_bytes, "left"))
        if right_bytes is not None:
            per_eye.append(self.predict_eye(right_bytes, "right"))
        if not per_eye:
            raise ValueError("At least one of left/right images is required.")

        worst = max(per_eye, key=lambda e: e.pred)
        return PatientPredictionResponse(
            pred=worst.pred,
            probs=worst.probs,
            confidence=worst.confidence,
            latency_ms=int((time.perf_counter() - t0) * 1000),
            per_eye=per_eye,
        )


engine = InferenceEngine()
