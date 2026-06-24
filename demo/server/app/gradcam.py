"""Grad-CAM on the live checkpoint (TASK-Demo §C.5).

Self-contained hook-based Grad-CAM (torch only — no pytorch_grad_cam dependency
for the live server). Target layer is EfficientNet's ``conv_head`` (the last
conv before global pooling), reusing the authoritative choice from
``experiments/src/models/efficientnet.get_gradcam_target_layer``.

The CAM is computed in the **analysis frame** (the canonically-flipped,
OD-fovea-rotated, FOV-cropped, isotropically-resized 512² canvas the CNN
processes) and then **warped back into the original upload frame** before
display, so the attention overlay is shown in exactly the same orientation as
the uploaded snapshot — no horizontal/vertical flip or rotation relative to it.
The inverse of the Stage 0/1/2 geometry (canonical flip → OD-fovea rotation →
FOV crop/resize/pad) is reconstructed from the ``transform`` payload
``stage_breakdown`` returns; this is the same forward geometry that already
aligns the OD/fovea markers, run in reverse. The JET overlay is then blended
over the original RGB and clipped to the (warped) FOV so no tint appears outside
the fundus disc.

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
from src.preprocessing.od_fovea_detect import rotation_affine_expand

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


def _build_rationale(
    heatmap_full: np.ndarray, target_class: int, fov: np.ndarray | None = None
) -> dict:
    """Compose a one-line predicted-class rationale from CAM geometry (§D.3).

    Derives the sentence purely from the Grad-CAM heatmap — pixel count above a
    salience threshold and the centroid of that region — with no LLM. The region
    is described in neutral image-space terms (e.g. "upper-left"), not anatomical
    arcade names, per INVARIANTS NC-14: Grad-CAM is interpretability evidence,
    not clinical localization of pathology. Positions are in the analysis frame
    (the model's own canonically-oriented view).

    Args:
        heatmap_full: Grad-CAM heatmap in ``[0, 1]`` in the analysis frame
            (already clipped to the FOV), shape ``(H, W)``.
        target_class: The DR grade (0–4) the CAM explains.
        fov: Optional binary FOV mask ``(H, W)``. When given, the area fraction
            is expressed relative to the field of view (not the padded canvas).

    Returns:
        Dict with ``rationale`` (str), ``cam_pixel_count`` (int),
        ``cam_area_frac`` (float in ``[0, 1]``), ``cam_region`` (str).
    """
    h, w = heatmap_full.shape
    total = float((fov > 0).sum()) if fov is not None else float(h * w)
    total = total or 1.0
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


def _fit_max_bgr(image: np.ndarray, max_side: int = 768) -> np.ndarray:
    """Downscale a BGR image so its longest side is ``max_side`` (keeps aspect).

    The overlay is rendered in the original upload frame, which can be up to
    4096². The demo displays it at ~260px, so bounding the rendered PNG keeps the
    base64 response small with no visible loss. Already-small images pass through.
    """
    h, w = image.shape[:2]
    scale = max_side / float(max(h, w))
    if scale < 1.0:
        image = cv2.resize(
            image, (int(round(w * scale)), int(round(h * scale))),
            interpolation=cv2.INTER_AREA,
        )
    return image


def _warp_analysis_to_original(field: np.ndarray, transform: dict) -> np.ndarray:
    """Map an analysis-frame field (``S×S``) back to the original image frame.

    Inverts the Stage 0/1/2 geometry — canonical flip → OD-fovea rotation → FOV
    crop/resize/pad — so a heatmap computed in the model's analysis frame can be
    displayed over the original upload in its own orientation. The forward chain
    ``original → analysis`` is ``crop ∘ rotate ∘ flip``; ``cv2.warpAffine`` with
    ``WARP_INVERSE_MAP`` samples, for each original pixel, its analysis location.

    Args:
        field: Analysis-frame array of shape ``(S, S)`` (float heatmap or mask).
        transform: The ``transform`` dict from ``stage_breakdown`` — ``crop_tf``,
            ``angle_deg``, ``flipped``, ``src_w``, ``src_h``.

    Returns:
        ``(src_h, src_w)`` float32 array in the original upload frame, zero
        outside the mapped analysis region.
    """
    crop_tf = transform["crop_tf"]
    src_w, src_h = int(transform["src_w"]), int(transform["src_h"])
    angle = float(transform["angle_deg"])
    left, upper = float(crop_tf.bbox[0]), float(crop_tf.bbox[1])

    # F: canonical horizontal flip (original → post-flip frame), only for left.
    flip = np.eye(3, dtype=np.float64)
    if transform["flipped"]:
        flip[0, 0] = -1.0
        flip[0, 2] = src_w - 1.0
    # R: Stage-1 rotation into the expanded canvas (matches the pipeline's
    # lossless rotation; identity when angle is 0).
    rot_m, _, _ = rotation_affine_expand(src_w, src_h, angle)
    rot = np.vstack([rot_m, [0.0, 0.0, 1.0]])
    # C: FOV crop + isotropic scale + centred pad.
    crop = np.array([
        [crop_tf.scale, 0.0, crop_tf.x_off - left * crop_tf.scale],
        [0.0, crop_tf.scale, crop_tf.y_off - upper * crop_tf.scale],
        [0.0, 0.0, 1.0],
    ], dtype=np.float64)

    m_fwd = (crop @ rot @ flip)[:2, :]  # original → analysis
    return cv2.warpAffine(
        field.astype(np.float32), m_fwd, (src_w, src_h),
        flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
        borderMode=cv2.BORDER_CONSTANT, borderValue=0,
    )


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

    # The CAM is computed in the analysis frame (the 512² canvas the CNN sees),
    # then warped back to the original upload frame for display so the overlay
    # keeps the snapshot's own orientation. ``transform`` carries the Stage 0/1/2
    # geometry needed to invert it.
    bd = engine.pipeline.stage_breakdown(rgb, eye_side=eye, with_heatmaps=False)
    base_rgb = dict(bd["stages"])["fov_crop_resize"]     # (S, S, 3) analysis RGB
    fov_mask = bd["fov_mask"]                            # (S, S) float in {0,1}
    transform = bd["transform"]
    space = int(base_rgb.shape[0])

    tensor = engine.pipeline(rgb, eye_side=eye).unsqueeze(0).to(engine.device)

    cam_engine = _GradCAM(engine.model, get_gradcam_target_layer(engine.model))
    heatmap, target = cam_engine(tensor, target_class)   # (h, w) in [0,1]

    # Upsample the CAM to the analysis canvas and clip it to the FOV so no
    # activation is ever shown outside the fundus disc.
    heatmap_full = cv2.resize(heatmap, (space, space), interpolation=cv2.INTER_LINEAR)
    fov = (fov_mask > 0).astype(np.float32)
    # The FOV mask is degenerate for some inputs (it can come back all-ones,
    # failing to exclude the dark border / zero-padding of the analysis canvas).
    # Intersect it with the non-black region of the base image so the heatmap
    # never appears over black padding regardless of the mask's quality — this
    # is what keeps the overlay inside the visible fundus.
    in_image = (base_rgb.mean(axis=2) > 10).astype(np.float32)
    fov = fov * in_image
    heatmap_full = heatmap_full * fov

    # Warp the FOV-clipped CAM and the FOV itself back to the original upload
    # frame, then blend in that frame so the overlay matches the snapshot's
    # orientation exactly (no flip / rotation relative to the upload).
    cam_orig = _warp_analysis_to_original(heatmap_full, transform)
    fov_orig = _warp_analysis_to_original(fov, transform) > 0.5

    heatmap_u8 = (np.clip(cam_orig, 0, 1) * 255).astype(np.uint8)
    heatmap_bgr = cv2.applyColorMap(heatmap_u8, cv2.COLORMAP_JET)
    # JET maps 0 → dark blue (not black), so blank everything outside the fundus
    # for a clean background and an honest "nothing outside the fundus" overlay.
    heatmap_bgr[~fov_orig] = 0
    orig_bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    # Alpha-blend the heatmap over the fundus only; leave the surround untinted
    # so the snapshot reads naturally.
    overlay_bgr = orig_bgr.copy()
    blended = cv2.addWeighted(heatmap_bgr, 0.5, orig_bgr, 0.5, 0)
    overlay_bgr[fov_orig] = blended[fov_orig]

    # Bound payload size: the original frame can be large; the display is ~260px.
    overlay_bgr = _fit_max_bgr(overlay_bgr)
    heatmap_bgr = _fit_max_bgr(heatmap_bgr)

    return {
        "gradcam_png_b64": imaging.png_b64_from_bgr(heatmap_bgr),
        "attention_overlay_png_b64": imaging.png_b64_from_bgr(overlay_bgr),
        "target_class": int(target),
        **_build_rationale(cam_orig, int(target), fov_orig.astype(np.float32)),
    }
