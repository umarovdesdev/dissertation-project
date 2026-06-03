"""preview strip + FOV mask + OD/fovea payload (TASK-Demo §C.6/§D.2).

Reuses ``PreprocessingPipeline.stage_breakdown`` (experiments) so the panels
are the exact intermediates the model sees — the most direct visual argument
for the P2 paradigm.
"""

from __future__ import annotations

import cv2
import numpy as np

from . import imaging

# Human-readable panel captions keyed by the stage labels stage_breakdown emits.
_PANEL_LABELS: dict[str, str] = {
    "original": "0. Original",
    "canonical_flip": "0. Canonical flip",
    "od_fovea_rotation": "1. OD-fovea rotation",
    "fov_crop_resize": "2/3. FOV crop + resize",
    "flat_field": "4. Flat-field",
    "clahe": "5. CLAHE",
}
_PANEL_PX = 256
_LABEL_H = 22


def _label_panel(image_rgb: np.ndarray, caption: str) -> np.ndarray:
    """Resize a panel to ``_PANEL_PX`` and add a caption bar on top.

    Args:
        image_rgb: RGB uint8 panel image.
        caption: Caption text.

    Returns:
        RGB uint8 panel of size ``(_PANEL_PX + _LABEL_H, _PANEL_PX, 3)``.
    """
    panel = cv2.resize(image_rgb, (_PANEL_PX, _PANEL_PX), interpolation=cv2.INTER_AREA)
    bar = np.full((_LABEL_H, _PANEL_PX, 3), 30, dtype=np.uint8)
    cv2.putText(bar, caption, (4, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.38,
                (235, 235, 235), 1, cv2.LINE_AA)
    return np.vstack([bar, panel])


def _compose_strip(stages: list[tuple[str, np.ndarray]]) -> np.ndarray:
    """Compose labelled stage panels left-to-right into one RGB image."""
    panels = [_label_panel(img, _PANEL_LABELS.get(label, label)) for label, img in stages]
    return np.hstack(panels)


def _od_payload(od, space_w: int, space_h: int, flipped: bool) -> dict:
    """Build an ODFoveaPayload dict from an ODFoveaResult (or a not-confident stub)."""
    if od is None:
        return {
            "od_center": [0, 0], "od_radius": 0.0,
            "fovea_center": [0, 0], "fovea_radius": 0.0,
            "angle_deg": 0.0, "rotation_sigma_deg": 0.0, "confident": False,
            "space_w": space_w, "space_h": space_h, "flipped": flipped,
        }
    return {
        "od_center": [int(od.od_center[0]), int(od.od_center[1])],
        "od_radius": float(od.od_radius),
        "fovea_center": [int(od.fovea_center[0]), int(od.fovea_center[1])],
        "fovea_radius": float(od.fovea_radius),
        "angle_deg": float(od.angle_deg),
        "rotation_sigma_deg": float(od.rotation_sigma_deg),
        "confident": bool(od.confident),
        "space_w": space_w, "space_h": space_h, "flipped": flipped,
    }


def compute_visualization(engine, image_bytes: bytes, eye: str) -> dict:
    """Produce the preview strip, FOV mask PNG, and OD/fovea payload.

    Args:
        engine: The loaded :class:`InferenceEngine` (holds the pipeline).
        image_bytes: Raw image bytes.
        eye: ``"left"`` or ``"right"``.

    Returns:
        Dict with ``fov_mask_png_b64``, ``preview_png_b64``, ``od_fovea``.

    Raises:
        imaging.BadImage / imaging.PayloadTooLarge: On bad/oversized input.
    """
    rgb = imaging.decode_rgb(image_bytes)
    h0, w0 = rgb.shape[:2]

    bd = engine.pipeline.stage_breakdown(rgb, eye_side=eye)
    strip_rgb = _compose_strip(bd["stages"])

    mask_u8 = (np.clip(bd["fov_mask"], 0, 1) * 255).astype(np.uint8)

    flipped = bool(engine.pipeline.config.use_canonical_flip and eye == "left")
    return {
        "fov_mask_png_b64": imaging.png_b64_from_bgr(mask_u8),  # single-channel → PNG
        "preview_png_b64": imaging.png_b64_from_rgb(strip_rgb),
        "od_fovea": _od_payload(bd["od_fovea"], w0, h0, flipped),
    }
