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


def _od_payload(od, analysis: dict | None, space: int) -> dict:
    """Build an ODFoveaPayload dict in **analysis space** (the cropped frame).

    Coordinates are expressed in the ``space`` × ``space`` ``fov_crop_resize``
    frame so the frontend overlays them directly on the analysis-space base
    image (no flip/rotation to undo). ``space_w == space_h == space`` and
    ``flipped`` is always ``False`` for this reason.

    Args:
        od: The :class:`ODFoveaResult` (for scalar fields), or ``None``.
        analysis: ``od_fovea_analysis`` from ``stage_breakdown`` (coords already
            projected into analysis space), or ``None`` when not confident.
        space: Analysis-frame side length (``target_size``).
    """
    if od is None or analysis is None:
        return {
            "od_center": [0, 0], "od_radius": 0.0,
            "fovea_center": [0, 0], "fovea_radius": 0.0,
            "angle_deg": 0.0, "rotation_sigma_deg": 0.0, "confident": False,
            "space_w": space, "space_h": space, "flipped": False,
        }
    return {
        "od_center": [float(analysis["od_center"][0]), float(analysis["od_center"][1])],
        "od_radius": float(analysis["od_radius"]),
        "fovea_center": [float(analysis["fovea_center"][0]), float(analysis["fovea_center"][1])],
        "fovea_radius": float(analysis["fovea_radius"]),
        "angle_deg": float(od.angle_deg),
        "rotation_sigma_deg": float(od.rotation_sigma_deg),
        "confident": bool(od.confident),
        "space_w": space, "space_h": space, "flipped": False,
    }


def compute_visualization(engine, image_bytes: bytes, eye: str) -> dict:
    """Produce the preview strip, FOV mask PNG, and OD/fovea payload.

    Args:
        engine: The loaded :class:`InferenceEngine` (holds the pipeline).
        image_bytes: Raw image bytes.
        eye: ``"left"`` or ``"right"``.

    Returns:
        Dict with ``fov_mask_png_b64``, ``fov_base_png_b64``,
        ``preview_png_b64``, ``od_fovea``. ``fov_base_png_b64`` is the
        analysis-space (cropped/oriented 512²) RGB the mask and OD/fovea
        markers are aligned to.

    Raises:
        imaging.BadImage / imaging.PayloadTooLarge: On bad/oversized input.
    """
    rgb = imaging.decode_rgb(image_bytes)

    bd = engine.pipeline.stage_breakdown(rgb, eye_side=eye)
    strip_rgb = _compose_strip(bd["stages"])

    # Analysis-space base: the cropped/oriented RGB that the FOV mask and the
    # projected OD/fovea markers share a coordinate frame with.
    stage_map = dict(bd["stages"])
    fov_base_rgb = stage_map["fov_crop_resize"]
    space = int(fov_base_rgb.shape[0])

    mask_u8 = (np.clip(bd["fov_mask"], 0, 1) * 255).astype(np.uint8)

    return {
        "fov_mask_png_b64": imaging.png_b64_from_bgr(mask_u8),  # single-channel → PNG
        "fov_base_png_b64": imaging.png_b64_from_rgb(fov_base_rgb),
        "preview_png_b64": imaging.png_b64_from_rgb(strip_rgb),
        "od_fovea": _od_payload(bd["od_fovea"], bd["od_fovea_analysis"], space),
    }
