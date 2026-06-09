"""Grad-CAM on the live checkpoint (TASK-Demo §C.5).

Self-contained hook-based Grad-CAM (torch only — no pytorch_grad_cam dependency
for the live server). Target layer is EfficientNet's ``conv_head`` (the last
conv before global pooling), reusing the authoritative choice from
``experiments/src/models/efficientnet.get_gradcam_target_layer``. The JET
overlay is blended over the **original** uploaded RGB (clearer for a
non-technical audience than the preprocessed image), reusing
``experiments/src/explainability/visualization.overlay_gradcam``.

NC-14 (INVARIANTS): Grad-CAM is interpretability evidence, not clinical
localization of pathology.
"""

from __future__ import annotations

import cv2
import numpy as np
import torch
import torch.nn as nn

# experiments/ is on sys.path via app/__init__.py.
# NOTE: import the layer-selection helper from the module directly; we do NOT
# import src.explainability (its package __init__ pulls in pytorch_grad_cam,
# which the live server intentionally does not depend on). The JET overlay is a
# few lines, inlined below.
from src.models.efficientnet import get_gradcam_target_layer

from . import imaging


class _GradCAM:
    """Hook-based Grad-CAM for a single target layer."""

    def __init__(self, model: nn.Module, target_layer: nn.Module) -> None:
        self.model = model
        self._activations: torch.Tensor | None = None
        self._gradients: torch.Tensor | None = None
        target_layer.register_forward_hook(self._fwd_hook)
        target_layer.register_full_backward_hook(self._bwd_hook)

    def _fwd_hook(self, _module, _inp, output: torch.Tensor) -> None:
        self._activations = output.detach()

    def _bwd_hook(self, _module, _grad_in, grad_out) -> None:
        self._gradients = grad_out[0].detach()

    def __call__(
        self,
        input_tensor: torch.Tensor,
        target_class: int | None = None,
    ) -> tuple[np.ndarray, int]:
        """Compute a Grad-CAM heatmap.

        Args:
            input_tensor: Model input of shape ``(1, C, H, W)`` on the model's
                device.
            target_class: Class to explain; defaults to the predicted class.

        Returns:
            Tuple ``(heatmap, target_class)`` where ``heatmap`` is a float32
            array of shape ``(h, w)`` in ``[0, 1]`` at the target layer's
            spatial resolution.
        """
        self.model.zero_grad(set_to_none=True)
        logits = self.model(input_tensor)               # (1, num_classes)
        if target_class is None:
            target_class = int(logits.argmax(dim=1).item())
        score = logits[0, target_class]
        score.backward()

        acts = self._activations[0]                     # (C, h, w)
        grads = self._gradients[0]                       # (C, h, w)
        weights = grads.mean(dim=(1, 2))                 # (C,)
        cam = torch.relu((weights[:, None, None] * acts).sum(dim=0))  # (h, w)

        cam = cam.cpu().numpy().astype(np.float32)
        cam -= cam.min()
        peak = cam.max()
        if peak > 1e-8:
            cam /= peak
        return cam, target_class


def _build_rationale(heatmap_full: np.ndarray, target_class: int) -> dict:
    """Compose a one-line predicted-class rationale from CAM geometry (§D.3).

    Derives the sentence purely from the Grad-CAM heatmap — pixel count above a
    salience threshold and the centroid of that region — with no LLM. The region
    is described in neutral image-space terms (e.g. "upper-left"), not anatomical
    arcade names, per INVARIANTS NC-14: Grad-CAM is interpretability evidence,
    not clinical localization of pathology.

    Args:
        heatmap_full: Grad-CAM heatmap in ``[0, 1]`` at the original image size,
            shape ``(H, W)``.
        target_class: The DR grade (0–4) the CAM explains.

    Returns:
        Dict with ``rationale`` (str), ``cam_pixel_count`` (int),
        ``cam_area_frac`` (float in ``[0, 1]``), ``cam_region`` (str).
    """
    h, w = heatmap_full.shape
    total = float(h * w) or 1.0
    salient = heatmap_full >= 0.5
    n_pix = int(salient.sum())
    area_frac = n_pix / total

    if n_pix == 0:
        region = "diffuse"
        sentence = (
            "Grad-CAM shows no concentrated activation above threshold; attention "
            f"is diffuse across the field, consistent with the features the model "
            f"associates with DR grade {target_class}."
        )
        return {
            "rationale": sentence,
            "cam_pixel_count": 0,
            "cam_area_frac": 0.0,
            "cam_region": region,
        }

    ys, xs = np.nonzero(salient)
    cy = float(ys.mean()) / h          # normalized centroid (0=top, 1=bottom)
    cx = float(xs.mean()) / w          # normalized centroid (0=left, 1=right)
    vert = "upper" if cy < 0.40 else "lower" if cy > 0.60 else "mid"
    horiz = "left" if cx < 0.40 else "right" if cx > 0.60 else "central"
    if vert == "mid" and horiz == "central":
        region = "central"
    elif vert == "mid":
        region = horiz
    elif horiz == "central":
        region = vert
    else:
        region = f"{vert}-{horiz}"

    sentence = (
        f"Model attention concentrates on ~{n_pix:,} pixels "
        f"({area_frac * 100:.1f}% of the field) in the {region} region of the "
        f"image, consistent with the features the model associates with DR grade "
        f"{target_class}."
    )
    return {
        "rationale": sentence,
        "cam_pixel_count": n_pix,
        "cam_area_frac": round(area_frac, 4),
        "cam_region": region,
    }


def compute_gradcam(engine, image_bytes: bytes, eye: str,
                    target_class: int | None = None) -> dict:
    """Run Grad-CAM for one eye and return base64 PNG overlays.

    Args:
        engine: The loaded :class:`InferenceEngine` (model + pipeline).
        image_bytes: Raw image bytes.
        eye: ``"left"`` or ``"right"`` (drives canonical flip).
        target_class: Optional class to explain (defaults to prediction).

    Returns:
        Dict with ``gradcam_png_b64``, ``attention_overlay_png_b64``,
        ``target_class``, and the predicted-class rationale fields
        (``rationale``, ``cam_pixel_count``, ``cam_area_frac``, ``cam_region``).

    Raises:
        RuntimeError: If the model is not loaded.
        imaging.BadImage / imaging.PayloadTooLarge: On bad/oversized input.
    """
    if engine.model is None:
        raise RuntimeError("Model not loaded.")

    rgb = imaging.decode_rgb(image_bytes)                # (H0, W0, 3) original
    tensor = engine.pipeline(rgb, eye_side=eye).unsqueeze(0).to(engine.device)

    cam_engine = _GradCAM(engine.model, get_gradcam_target_layer(engine.model))
    heatmap, target = cam_engine(tensor, target_class)   # (h, w) in [0,1]

    h0, w0 = rgb.shape[:2]
    heatmap_full = cv2.resize(heatmap, (w0, h0), interpolation=cv2.INTER_LINEAR)

    # Heatmap-only PNG (JET) and alpha-blended overlay over the ORIGINAL image.
    heatmap_u8 = (np.clip(heatmap_full, 0, 1) * 255).astype(np.uint8)
    heatmap_bgr = cv2.applyColorMap(heatmap_u8, cv2.COLORMAP_JET)
    original_bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    overlay_bgr = cv2.addWeighted(heatmap_bgr, 0.5, original_bgr, 0.5, 0)

    return {
        "gradcam_png_b64": imaging.png_b64_from_bgr(heatmap_bgr),
        "attention_overlay_png_b64": imaging.png_b64_from_bgr(overlay_bgr),
        "target_class": int(target),
        **_build_rationale(heatmap_full, int(target)),
    }
