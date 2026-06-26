"""preview strip + FOV mask + OD/fovea payload (TASK-Demo §C.6/§D.2).

Reuses ``PreprocessingPipeline.stage_breakdown`` (experiments) so the panels
are the exact intermediates the model sees — the most direct visual argument
for the P2 paradigm.
"""

from __future__ import annotations

import math

import cv2
import numpy as np
from src.preprocessing.od_fovea_detect import ODFoveaResult

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


def _od_payload(od, src_w: int, src_h: int) -> dict:
    """Build an ODFoveaPayload dict in the **flipped (pre-rotation) frame**.

    The detection overlay is shown on the un-rotated canonical-flip image, so the
    OD–fovea axis appears at its true tilt — the Stage-1 rotation slide is what
    levels it. Coordinates are therefore the detector's native flipped-frame
    pixels (``space_w == src_w``, ``space_h == src_h``, ``flipped`` False: the
    base image is already flipped, so the frontend overlays directly). Heatmaps
    are the detector's native flipped-frame probability maps — no warp needed.

    Args:
        od: The :class:`ODFoveaResult` (centres in the flipped frame), or
            ``None`` when no detection ran.
        src_w: Width of the flipped frame (== original width; flip preserves size).
        src_h: Height of the flipped frame.
    """
    if od is None:
        return {
            "od_center": [0, 0], "od_radius": 0.0,
            "fovea_center": [0, 0], "fovea_radius": 0.0,
            "angle_deg": 0.0, "rotation_sigma_deg": 0.0, "confident": False,
            "space_w": int(src_w), "space_h": int(src_h), "flipped": False,
            "od_confidence": 0.0, "fovea_confidence": 0.0,
            "od_heatmap_png_b64": "", "fovea_heatmap_png_b64": "",
        }
    od_hm = od.od_heatmap
    fovea_hm = od.fovea_heatmap
    return {
        "od_center": [float(od.od_center[0]), float(od.od_center[1])],
        "od_radius": float(od.od_radius),
        "fovea_center": [float(od.fovea_center[0]), float(od.fovea_center[1])],
        "fovea_radius": float(od.fovea_radius),
        "angle_deg": float(od.angle_deg),
        "rotation_sigma_deg": float(od.rotation_sigma_deg),
        "confident": bool(od.confident),
        "space_w": int(src_w), "space_h": int(src_h), "flipped": False,
        "od_confidence": float(getattr(od, "od_confidence", 0.0)),
        "fovea_confidence": float(getattr(od, "fovea_confidence", 0.0)),
        "od_heatmap_png_b64": imaging.heatmap_png_b64(_fit_max(od_hm)) if od_hm is not None else "",
        "fovea_heatmap_png_b64": (
            imaging.heatmap_png_b64(_fit_max(fovea_hm)) if fovea_hm is not None else ""
        ),
    }


# Analysis-frame stages share the 512² FOV mask (Stage 3's 4th channel). Earlier
# (pre-crop) stages predate that mask, so their FOV channel is the stage's own
# foreground (a luma threshold), keeping every stage a consistent 4-channel view.
_ANALYSIS_STAGES: frozenset[str] = frozenset({"fov_crop_resize", "flat_field", "clahe"})


def _stage_channels(disp_rgb: np.ndarray, label: str, mask_u8: np.ndarray) -> list[dict]:
    """Split a stage's display RGB into its R/G/B/FOV channel PNGs.

    R/G/B are the stage image's three channels (the literal per-channel
    intensities the CNN would see); the FOV channel is the analysis FOV mask for
    analysis-frame stages, or the stage's own foreground for earlier stages.

    Args:
        disp_rgb: The (bounded) RGB image shown for this stage.
        label: The stage label (e.g. ``"clahe"``).
        mask_u8: The 512² analysis FOV mask (Stage 3's 4th channel).

    Returns:
        Four channel dicts (``key``/``caption``/``png_b64``): R, G, B, FOV.
    """
    if label in _ANALYSIS_STAGES:
        fov = mask_u8
        if fov.shape[:2] != disp_rgb.shape[:2]:
            fov = cv2.resize(
                fov, (disp_rgb.shape[1], disp_rgb.shape[0]),
                interpolation=cv2.INTER_NEAREST,
            )
    else:
        gray = cv2.cvtColor(disp_rgb, cv2.COLOR_RGB2GRAY)
        fov = (gray > 15).astype(np.uint8) * 255
    return [
        {"key": "ch_r", "caption": "Ch 0 · R",
         "png_b64": imaging.png_b64_from_bgr(np.ascontiguousarray(disp_rgb[:, :, 0]))},
        {"key": "ch_g", "caption": "Ch 1 · G",
         "png_b64": imaging.png_b64_from_bgr(np.ascontiguousarray(disp_rgb[:, :, 1]))},
        {"key": "ch_b", "caption": "Ch 2 · B",
         "png_b64": imaging.png_b64_from_bgr(np.ascontiguousarray(disp_rgb[:, :, 2]))},
        {"key": "ch_fov", "caption": "Ch 3 · FOV",
         "png_b64": imaging.png_b64_from_bgr(fov)},
    ]


def _build_payload(
    engine,
    image_bytes: bytes,
    eye: str,
    *,
    od_override: ODFoveaResult | None = None,
    with_heatmaps: bool = True,
) -> dict:
    """Run ``stage_breakdown`` and assemble the demo's visualize payload.

    Shared by :func:`compute_visualization` (live detector) and
    :func:`compute_correction` (clinician override re-run), so a Save correction
    rebuilds the SAME payload — the recomputed rotation and every downstream
    stage — from the corrected OD/fovea centres.

    Args:
        engine: The loaded inference engine (holds the pipeline).
        image_bytes: Raw image bytes.
        eye: ``"left"`` or ``"right"``.
        od_override: Clinician-corrected detection (flipped frame) to drive the
            rotation, or ``None`` to use the learned detector.
        with_heatmaps: Request detector probability heatmaps (live path only).

    Returns:
        Dict with ``fov_mask_png_b64``, ``fov_base_png_b64``,
        ``detect_base_png_b64`` (the un-rotated overlay base), ``preview_png_b64``,
        ``od_fovea`` (flipped frame), and ``stages`` — each image stage carrying a
        ``channels`` list (its R/G/B/FOV decomposition).

    Raises:
        imaging.BadImage / imaging.PayloadTooLarge: On bad/oversized input.
    """
    rgb = imaging.decode_rgb(image_bytes)
    src_h, src_w = rgb.shape[:2]

    bd = engine.pipeline.stage_breakdown(
        rgb, eye_side=eye, with_heatmaps=with_heatmaps, od_override=od_override
    )
    strip_rgb = _compose_strip(bd["stages"])

    stage_map = dict(bd["stages"])
    # Analysis-space crop (the Grad-CAM frame) and the pre-rotation overlay base
    # (the canonical-flip image the detection markers are aligned to).
    fov_base_rgb = stage_map["fov_crop_resize"]
    detect_base_rgb = stage_map["canonical_flip"]

    mask_u8 = (np.clip(bd["fov_mask"], 0, 1) * 255).astype(np.uint8)

    # Per-stage slides for the step-by-step detailed view: each preprocessing
    # stage as its own image (bounded resolution), plus the FOV mask (Stage 3,
    # the 4th input channel) as a final slide. Each image stage also carries its
    # R/G/B/FOV channel decomposition (``channels``) so the demo can show how a
    # method reshapes the individual channels — the "how preprocessing helps"
    # panel. The final CLAHE stage's channels are the CNN input tensor itself.
    stage_slides = []
    for label, img in bd["stages"]:
        disp = _fit_max(img)
        stage_slides.append({
            "key": label,
            "caption": _PANEL_LABELS.get(label, label),
            "png_b64": imaging.png_b64_from_rgb(disp),
            "channels": _stage_channels(disp, label, mask_u8),
        })
    stage_slides.append({
        "key": "fov_mask",
        "caption": "3. FOV mask (4th channel)",
        "png_b64": imaging.png_b64_from_bgr(mask_u8),
        "channels": [],
    })

    return {
        "fov_mask_png_b64": imaging.png_b64_from_bgr(mask_u8),  # single-channel → PNG
        "fov_base_png_b64": imaging.png_b64_from_rgb(fov_base_rgb),
        "detect_base_png_b64": imaging.png_b64_from_rgb(_fit_max(detect_base_rgb)),
        "preview_png_b64": imaging.png_b64_from_rgb(strip_rgb),
        "od_fovea": _od_payload(bd["od_fovea"], src_w, src_h),
        "stages": stage_slides,
    }


def compute_visualization(engine, image_bytes: bytes, eye: str) -> dict:
    """Produce the preview strip, FOV mask PNG, stage slides, and OD/fovea payload.

    Args:
        engine: The loaded :class:`InferenceEngine` (holds the pipeline).
        image_bytes: Raw image bytes.
        eye: ``"left"`` or ``"right"``.

    Returns:
        The visualize payload (see :func:`_build_payload`). The OD/fovea overlay
        is in the flipped (pre-rotation) frame and aligns to ``detect_base_png_b64``.

    Raises:
        imaging.BadImage / imaging.PayloadTooLarge: On bad/oversized input.
    """
    return _build_payload(engine, image_bytes, eye, od_override=None, with_heatmaps=True)


def _flip_to_original(
    point: tuple[float, float], src_w: int, flipped: bool
) -> tuple[float, float]:
    """Map a flipped-frame point back to original (uploaded) image pixels.

    The detection overlay now lives in the canonical-flip frame, which is the
    full original image after (at most) a horizontal flip — no rotation or crop
    to undo. So the inverse is the flip alone, giving the raw-pixel coordinate
    the Phase-4 fine-tune loop trains on.

    Args:
        point: ``(x, y)`` in the flipped frame.
        src_w: Original/flipped image width.
        flipped: Whether the canonical flip was applied (left eye).

    Returns:
        ``(x, y)`` in original (uploaded) image pixels.
    """
    fx, fy = float(point[0]), float(point[1])
    if flipped:
        fx = (src_w - 1) - fx
    return (fx, fy)


def compute_correction(
    engine,
    image_bytes: bytes,
    eye: str,
    od_corrected: tuple[float, float],
    fovea_corrected: tuple[float, float],
) -> dict:
    """Re-run the pipeline from clinician-corrected OD/fovea centres.

    The corrected centres arrive in the flipped (pre-rotation) frame — where the
    detection slide is edited. They are packaged as an :class:`ODFoveaResult`
    override whose ``angle_deg`` (the fovea→OD tilt) redefines the Stage-1
    rotation; ``stage_breakdown`` is re-run with that override so the rotation
    and **every downstream stage** (crop, flat-field, CLAHE, FOV mask) are
    recomputed. The corrected centres are also mapped back to original-image
    pixels for the Phase-4 feedback store.

    Args:
        engine: The loaded inference engine (holds the pipeline).
        image_bytes: Raw original image bytes.
        eye: ``"left"`` or ``"right"``.
        od_corrected: Corrected OD centre ``(x, y)`` in the flipped frame.
        fovea_corrected: Corrected fovea centre ``(x, y)`` in the flipped frame.

    Returns:
        The full visualize payload (see :func:`_build_payload`) for the corrected
        geometry, plus ``original`` (``{od_center, fovea_center, space_w,
        space_h}`` in original pixels) for persistence.

    Raises:
        imaging.BadImage / imaging.PayloadTooLarge: On bad/oversized input.
    """
    odx, ody = float(od_corrected[0]), float(od_corrected[1])
    fvx, fvy = float(fovea_corrected[0]), float(fovea_corrected[1])

    # Geometry from the corrected centres (flipped frame). The Stage-1 rotation
    # levels the fovea→OD axis (note the negated deltas), keeping the optic disc
    # on the canonical right side — matching the detector's own convention.
    dx, dy = fvx - odx, fvy - ody
    distance = math.hypot(dx, dy)
    angle_rad = math.atan2(-dy, -dx)
    angle_deg = math.degrees(angle_rad)
    od_radius = max(distance / 4.0, 10.0)        # same anatomical prior as infer
    fovea_radius = max(od_radius * 0.5, 5.0)

    override = ODFoveaResult(
        od_center=(odx, ody), od_radius=od_radius,
        fovea_center=(fvx, fvy), fovea_radius=fovea_radius,
        distance=distance, angle_rad=angle_rad, angle_deg=angle_deg,
        rotation_sigma_deg=0.0,                  # manual correction → exact
        confident=True, od_confidence=1.0, fovea_confidence=1.0,
    )

    payload = _build_payload(
        engine, image_bytes, eye, od_override=override, with_heatmaps=False
    )

    # Map the corrected flipped-frame centres back to ORIGINAL pixels (invert the
    # canonical flip only; ``space_w`` of the payload is the flipped == original
    # width).
    src_w = int(payload["od_fovea"]["space_w"])
    src_h = int(payload["od_fovea"]["space_h"])
    flipped = bool(eye == "left" and engine.pipeline.config.use_canonical_flip)
    od_orig = _flip_to_original((odx, ody), src_w, flipped)
    fv_orig = _flip_to_original((fvx, fvy), src_w, flipped)
    payload["original"] = {
        "od_center": [od_orig[0], od_orig[1]],
        "fovea_center": [fv_orig[0], fv_orig[1]],
        "space_w": src_w, "space_h": src_h,
    }
    return payload
