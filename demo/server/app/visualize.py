"""preview strip + FOV mask + OD/fovea payload (TASK-Demo §C.6/§D.2).

Reuses ``PreprocessingPipeline.stage_breakdown`` (experiments) so the panels
are the exact intermediates the model sees — the most direct visual argument
for the P2 paradigm.
"""

from __future__ import annotations

import math

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


def _fit_max(image_rgb: np.ndarray, max_side: int = 512) -> np.ndarray:
    """Downscale ``image_rgb`` so its longest side is ``max_side`` (keeps aspect).

    Used to bound the per-stage slide payloads — the pre-crop stages (original /
    canonical flip) can be at full upload resolution. Already-small images are
    returned unchanged.
    """
    h, w = image_rgb.shape[:2]
    scale = max_side / float(max(h, w))
    if scale < 1.0:
        image_rgb = cv2.resize(
            image_rgb, (int(round(w * scale)), int(round(h * scale))),
            interpolation=cv2.INTER_AREA,
        )
    return image_rgb


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
            "od_confidence": float(getattr(od, "od_confidence", 0.0)) if od else 0.0,
            "fovea_confidence": float(getattr(od, "fovea_confidence", 0.0)) if od else 0.0,
            "od_heatmap_png_b64": "", "fovea_heatmap_png_b64": "",
        }
    od_hm = analysis.get("od_heatmap")
    fovea_hm = analysis.get("fovea_heatmap")
    return {
        "od_center": [float(analysis["od_center"][0]), float(analysis["od_center"][1])],
        "od_radius": float(analysis["od_radius"]),
        "fovea_center": [float(analysis["fovea_center"][0]), float(analysis["fovea_center"][1])],
        "fovea_radius": float(analysis["fovea_radius"]),
        "angle_deg": float(od.angle_deg),
        "rotation_sigma_deg": float(od.rotation_sigma_deg),
        "confident": bool(od.confident),
        "space_w": space, "space_h": space, "flipped": False,
        "od_confidence": float(getattr(od, "od_confidence", 0.0)),
        "fovea_confidence": float(getattr(od, "fovea_confidence", 0.0)),
        "od_heatmap_png_b64": imaging.heatmap_png_b64(od_hm) if od_hm is not None else "",
        "fovea_heatmap_png_b64": imaging.heatmap_png_b64(fovea_hm) if fovea_hm is not None else "",
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

    bd = engine.pipeline.stage_breakdown(rgb, eye_side=eye, with_heatmaps=True)
    strip_rgb = _compose_strip(bd["stages"])

    # Analysis-space base: the cropped/oriented RGB that the FOV mask and the
    # projected OD/fovea markers share a coordinate frame with.
    stage_map = dict(bd["stages"])
    fov_base_rgb = stage_map["fov_crop_resize"]
    space = int(fov_base_rgb.shape[0])

    mask_u8 = (np.clip(bd["fov_mask"], 0, 1) * 255).astype(np.uint8)

    # Per-stage slides for the step-by-step detailed view: each preprocessing
    # stage as its own image (bounded resolution), plus the FOV mask (Stage 3,
    # the 4th input channel) as a final slide.
    stage_slides = [
        {
            "key": label,
            "caption": _PANEL_LABELS.get(label, label),
            "png_b64": imaging.png_b64_from_rgb(_fit_max(img)),
        }
        for label, img in bd["stages"]
    ]
    stage_slides.append({
        "key": "fov_mask",
        "caption": "3. FOV mask (4th channel)",
        "png_b64": imaging.png_b64_from_bgr(mask_u8),
    })

    return {
        "fov_mask_png_b64": imaging.png_b64_from_bgr(mask_u8),  # single-channel → PNG
        "fov_base_png_b64": imaging.png_b64_from_rgb(fov_base_rgb),
        "preview_png_b64": imaging.png_b64_from_rgb(strip_rgb),
        "od_fovea": _od_payload(bd["od_fovea"], bd["od_fovea_analysis"], space),
        "stages": stage_slides,
    }


def _analysis_to_original(
    point: tuple[float, float], transform: dict, eye: str
) -> tuple[float, float]:
    """Invert the Stage 0/1/2 geometry: analysis-frame point → original pixels.

    Reverses the chain :func:`stage_breakdown` applies — canonical flip, Stage-1
    rotation, then FOV crop+resize — so a clinician-corrected centre placed in
    the analysis frame maps back to the raw uploaded image's pixels (the frame
    the Phase-4 fine-tune loop trains on).

    Args:
        point: ``(x, y)`` in the ``target_size`` analysis canvas.
        transform: The ``transform`` dict from ``stage_breakdown`` (``crop_tf``,
            ``angle_deg``, ``flipped``, ``src_w``, ``src_h``).
        eye: ``"left"``/``"right"`` (only used as a sanity tag; the flip is
            taken from ``transform['flipped']``).

    Returns:
        ``(x, y)`` in original (uploaded) image pixels.
    """
    crop_tf = transform["crop_tf"]
    ax, ay = float(point[0]), float(point[1])
    # 1. Invert FOV crop+resize → oriented (rotated) image pixels.
    rx, ry = crop_tf.invert(ax, ay) if hasattr(crop_tf, "invert") else (
        (ax - crop_tf.x_off) / crop_tf.scale + crop_tf.bbox[0],
        (ay - crop_tf.y_off) / crop_tf.scale + crop_tf.bbox[1],
    )
    # 2. Invert the Stage-1 rotation (about the flipped-image centre).
    src_w, src_h = int(transform["src_w"]), int(transform["src_h"])
    inv_rot = cv2.getRotationMatrix2D(
        (src_w // 2, src_h // 2), -float(transform["angle_deg"]), 1.0
    )
    fx = inv_rot[0, 0] * rx + inv_rot[0, 1] * ry + inv_rot[0, 2]
    fy = inv_rot[1, 0] * rx + inv_rot[1, 1] * ry + inv_rot[1, 2]
    # 3. Invert the canonical flip (left eye was mirrored horizontally).
    if transform.get("flipped"):
        fx = (src_w - 1) - fx
    return (fx, fy)


def compute_correction(
    engine,
    image_bytes: bytes,
    eye: str,
    od_corrected: tuple[float, float],
    fovea_corrected: tuple[float, float],
) -> dict:
    """Recompute the OD/fovea overlay from clinician-corrected centres.

    Re-runs ``stage_breakdown`` on the submitted image (deterministic — frozen
    detector weights) to recover the Stage 0/1/2 geometry, then:
      * recomputes the analysis-space overlay (angle/distance/radii) from the
        corrected centres so the frontend can re-render immediately;
      * maps the corrected centres back to **original-image pixels** for the
        Phase-4 feedback store.

    Args:
        engine: The loaded inference engine (holds the pipeline).
        image_bytes: Raw original image bytes.
        eye: ``"left"`` or ``"right"``.
        od_corrected: Corrected OD centre ``(x, y)`` in the analysis frame.
        fovea_corrected: Corrected fovea centre ``(x, y)`` in the analysis frame.

    Returns:
        Dict with ``od_fovea`` (an :class:`ODFoveaPayload` dict) and
        ``original`` (``{od_center, fovea_center, space_w, space_h}`` in original
        pixels) for persistence.

    Raises:
        imaging.BadImage / imaging.PayloadTooLarge: On bad/oversized input.
    """
    rgb = imaging.decode_rgb(image_bytes)
    bd = engine.pipeline.stage_breakdown(rgb, eye_side=eye, with_heatmaps=False)
    transform = bd["transform"]
    space = int(transform["space"])

    odx, ody = float(od_corrected[0]), float(od_corrected[1])
    fvx, fvy = float(fovea_corrected[0]), float(fovea_corrected[1])

    # Geometry recomputed from the corrected centres (analysis frame).
    dx, dy = fvx - odx, fvy - ody
    distance = math.hypot(dx, dy)
    angle_deg = math.degrees(math.atan2(dy, dx))
    od_radius = max(distance / 4.0, 10.0)        # same anatomical prior as infer
    fovea_radius = max(od_radius * 0.5, 5.0)

    payload = {
        "od_center": [odx, ody], "od_radius": od_radius,
        "fovea_center": [fvx, fvy], "fovea_radius": fovea_radius,
        "angle_deg": angle_deg,
        "rotation_sigma_deg": 0.0,               # manual correction → exact
        "confident": True,
        "space_w": space, "space_h": space, "flipped": False,
        "od_confidence": 1.0, "fovea_confidence": 1.0,
        "od_heatmap_png_b64": "", "fovea_heatmap_png_b64": "",
    }

    od_orig = _analysis_to_original((odx, ody), transform, eye)
    fv_orig = _analysis_to_original((fvx, fvy), transform, eye)
    original = {
        "od_center": [od_orig[0], od_orig[1]],
        "fovea_center": [fv_orig[0], fv_orig[1]],
        "space_w": int(transform["src_w"]), "space_h": int(transform["src_h"]),
    }
    return {"od_fovea": payload, "original": original}
