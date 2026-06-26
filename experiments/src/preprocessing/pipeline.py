"""
Pipeline Orchestrator.

:class:`PreprocessingPipeline` chains all eight stages in the correct order.
It is the main public interface for the preprocessing stack.

Stage execution order
---------------------
Preprocessing (train + inference):
  0. Canonical flip      — left→right eye orientation
  1. OD-Fovea rotation   — always (classical CV, fallback on low confidence)
  2. FOV crop + resize   — always (512×512, centered zero-padding)
  3. FOV mask            — implicit, returned from Stage 2 as 4th channel
  4. Flat-field          — always (adaptive σ=0.07·D, inside mask only)
  5. Upgraded CLAHE      — always (stochastic p=0.8 at train time)
  7. Dataset-specific normalize — always last, outputs ``torch.Tensor``

Augmentation (train only, inserted before Stage 7):
  6. Unified affine + brightness/contrast + PCA colour jitter
     (rotation σ adaptive from Stage 1)

Baseline mode (``create_baseline``):
  Simple stretch-resize to 512×512 + ImageNet normalize. 3 channels (no mask).
  Replicates what most competitors do in the literature.
"""

from __future__ import annotations

from types import SimpleNamespace

import cv2
import numpy as np
import torch

from .canonical_orientation import canonical_flip, canonical_orientation
from .od_fovea_detect import ODFoveaResult, rotation_affine_expand
from .config import PreprocessingConfig
from .crop_resize import crop_and_resize, CropResizeTransform, _fov_foreground_mask
from .flat_field import apply_flat_field
from .imagenet_normalize import imagenet_normalize
from .polar_clahe import (
    PolarClaheParams,
    apply_polar_clahe,
    maybe_apply_polar_clahe,
)
from .upgraded_clahe import ClaheParams, maybe_apply_clahe
# NOTE: UnifiedFundusAugmentation is imported lazily inside __init__ to avoid
# circular imports (src.data imports from src.preprocessing and vice-versa).


def _project_to_analysis(
    point: tuple[float, float],
    angle_deg: float,
    src_w: int,
    src_h: int,
    crop_tf: "CropResizeTransform",
) -> tuple[float, float]:
    """Project a pre-crop (post-flip) point into the cropped analysis frame.

    Mirrors the rotation applied inside :func:`canonical_orientation` (about the
    flipped-image centre) followed by the FOV crop+resize transform, so a point
    detected in pre-rotation/pre-crop space lands exactly on the
    ``target_size`` analysis canvas. Used for the Stage-5 polar-CLAHE fovea pivot
    and the demo overlay so both agree with what the CNN sees.

    Args:
        point: ``(x, y)`` in pre-crop (post-flip) image pixels.
        angle_deg: Rotation angle applied by Stage 1 (``ODFoveaResult.angle_deg``).
        src_w: Width of the (rotation-preserved) pre-crop image.
        src_h: Height of the pre-crop image.
        crop_tf: The :class:`CropResizeTransform` from Stage 2's crop+resize.

    Returns:
        ``(x, y)`` in the padded ``target_size`` analysis canvas.
    """
    rot_m, _, _ = rotation_affine_expand(src_w, src_h, angle_deg)
    px, py = float(point[0]), float(point[1])
    rx = rot_m[0, 0] * px + rot_m[0, 1] * py + rot_m[0, 2]
    ry = rot_m[1, 0] * px + rot_m[1, 1] * py + rot_m[1, 2]
    return crop_tf.apply(rx, ry)


def _warp_heatmap_to_analysis(
    heatmap: np.ndarray,
    angle_deg: float,
    src_w: int,
    src_h: int,
    crop_tf: "CropResizeTransform",
) -> np.ndarray:
    """Warp a flipped-frame probability heatmap into the analysis canvas.

    Applies the *same* geometric chain :func:`_project_to_analysis` applies to a
    point — rotation about the flipped-image centre followed by the FOV
    crop+resize — but to a full heatmap image, so the demo can overlay the
    detector's probability map on the ``fov_crop_resize`` panel exactly where
    the markers land.

    Args:
        heatmap: float32 ``(src_h, src_w)`` probability map in the flipped
            (pre-rotation, pre-crop) input frame.
        angle_deg: Rotation angle applied by Stage 1 (``angle_deg``).
        src_w: Width of the flipped/pre-crop image.
        src_h: Height of the flipped/pre-crop image.
        crop_tf: The :class:`CropResizeTransform` from Stage 2's crop+resize.

    Returns:
        float32 ``(target_size, target_size)`` heatmap on the analysis canvas.
    """
    rot_m, _, _ = rotation_affine_expand(src_w, src_h, angle_deg)
    left, upper = crop_tf.bbox[0], crop_tf.bbox[1]
    # Affine for crop_tf.apply: (x - left) * scale + x_off, (y - upper) * scale + y_off.
    crop_m = np.array(
        [
            [crop_tf.scale, 0.0, crop_tf.x_off - left * crop_tf.scale],
            [0.0, crop_tf.scale, crop_tf.y_off - upper * crop_tf.scale],
        ],
        dtype=np.float64,
    )
    # Compose crop_m ∘ rot_m (apply rotation first, then crop) in homogeneous form.
    rot_h = np.vstack([rot_m, [0.0, 0.0, 1.0]])
    combined = (np.vstack([crop_m, [0.0, 0.0, 1.0]]) @ rot_h)[:2, :]
    size = int(crop_tf.target_size)
    return cv2.warpAffine(
        heatmap.astype(np.float32), combined, (size, size),
        flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0.0,
    )


class PreprocessingPipeline:
    """
    8-stage preprocessing + augmentation pipeline.

    Preprocessing stages 0–5 and 7 are applied identically at train and
    inference (except Stage 5 CLAHE, which is stochastic at train time).
    Stage 6 augmentation is applied only during training, inserted *before*
    Stage 7 normalisation so that it operates on uint8 images.

    All internal processing is done in **RGB**.  The ``input_color_space``
    parameter controls whether the input image is converted before any stage
    runs:

    - ``"bgr"`` (default) — converts BGR→RGB on entry.  Use this when images
      are loaded with :func:`cv2.imread`, which returns BGR.
    - ``"rgb"`` — no conversion.  Use this when the caller already provides
      an RGB array (e.g. loaded via PIL or a dataset that returns RGB).

    Passing an already-RGB image to a ``"bgr"`` pipeline silently swaps R and
    B channels, corrupting the image.  Always match this parameter to how the
    caller loads images.

    Args:
        config: :class:`PreprocessingConfig` controlling all parameters
            and toggle flags.
        is_training: ``True`` enables stochastic CLAHE and augmentation.
        input_color_space: ``"bgr"`` or ``"rgb"``.  Controls BGR→RGB
            conversion at the pipeline entry point.  Default ``"bgr"``
            matches :func:`cv2.imread` output.
    """

    def __init__(
        self,
        config: PreprocessingConfig,
        is_training: bool = False,
        input_color_space: str = "bgr",
    ) -> None:
        if input_color_space not in ("bgr", "rgb"):
            raise ValueError(
                f"input_color_space must be 'bgr' or 'rgb', got {input_color_space!r}"
            )
        self.config = config
        self.is_training = is_training
        self._input_color_space = input_color_space

        self._clahe_params = ClaheParams(
            tile_grid_size=config.clahe_tile_grid_size,
            clip_factor=config.clahe_clip_factor,
            global_threshold=config.clahe_global_threshold,
        )
        # Stage 5 polar-CLAHE params (used when config.clahe_mode == "polar").
        self._polar_clahe_params = PolarClaheParams(
            clip_factor=config.clahe_clip_factor,
            global_threshold=config.clahe_global_threshold,
            radial_rings=config.clahe_radial_rings,
            radial_exponent=config.clahe_radial_exponent,
            fine_bins=config.clahe_fine_bins,
            min_sector_area_frac=config.clahe_min_sector_area_frac,
        )
        # Lazy import to break the circular dependency with src.data
        from src.data.augmentation_unified import UnifiedFundusAugmentation  # noqa: PLC0415
        self._augmentation = UnifiedFundusAugmentation(config=config)

    # ------------------------------------------------------------------
    # Core callable
    # ------------------------------------------------------------------

    def __call__(
        self,
        image: np.ndarray,
        eye_side: str = "unknown",
    ) -> torch.Tensor:
        """
        Apply the full pipeline to one image.

        Args:
            image: Raw image as a uint8 NumPy array of shape ``(H, W, 3)``.
                Must match ``input_color_space`` set at construction:
                ``"bgr"`` for :func:`cv2.imread` output,
                ``"rgb"`` for PIL/already-converted arrays.
            eye_side: ``"left"``, ``"right"``, or ``"unknown"``.

        Returns:
            Normalised float32 tensor of shape
            ``(4, target_size, target_size)`` for full mode, or
            ``(3, target_size, target_size)`` for baseline mode.
            In full mode, channel 3 is a binary FOV mask
            (1.0 = real data, 0.0 = padding).
        """
        # Convert to RGB if input is BGR (e.g. from cv2.imread).
        if self._input_color_space == "bgr":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Baseline mode: simple stretch-resize + ImageNet normalize (3 channels)
        if self.config.mode == "baseline":
            image = cv2.resize(
                image,
                (self.config.target_size, self.config.target_size),
                interpolation=cv2.INTER_LINEAR,
            )
            return imagenet_normalize(
                image,
                mean=self.config.normalize_mean,
                std=self.config.normalize_std,
            )

        # Full pipeline: deterministic Stages 0–4, then stochastic Stages 5–7.
        # Split into two helpers so the precompute-and-cache path
        # (precompute_deterministic + finish_from_cache) is provably identical
        # to the live path — both finish through the same self._finish.
        flat_rgb, fov_mask, od_fovea_result, fovea_pivot = self._precompute_rgb(
            image, eye_side
        )
        return self._finish(flat_rgb, fov_mask, od_fovea_result, fovea_pivot)

    # ------------------------------------------------------------------
    # Stage split: deterministic 0–4  vs  stochastic 5–7
    # ------------------------------------------------------------------

    def _precompute_rgb(
        self,
        image: np.ndarray,
        eye_side: str,
    ) -> tuple[np.ndarray, np.ndarray, "ODFoveaResult | None", "tuple[float, float] | None"]:
        """Run the **deterministic** Stages 0–4 on an already-RGB image.

        These stages carry no train-time randomness, so their output is safe to
        cache once and reuse every epoch (the throughput fix). Stage 5 CLAHE
        is the first stochastic stage and is intentionally excluded here.

        Args:
            image: RGB uint8 array of shape ``(H, W, 3)`` (already colour-
                converted — callers handle ``input_color_space``).
            eye_side: ``"left"``, ``"right"``, or ``"unknown"``.

        Returns:
            Tuple of:
              - ``flat_rgb``: RGB uint8 ``(target_size, target_size, 3)`` after
                Stage 4 flat-field (padding zeroed).
              - ``fov_mask``: float32 ``(target_size, target_size)`` binary mask
                (1.0 inside FOV, 0.0 padding).
              - ``od_fovea_result``: :class:`ODFoveaResult` from Stage 0/1, or
                ``None`` if orientation is disabled.
              - ``fovea_pivot``: detected fovea centre projected into the
                ``target_size`` analysis frame for the Stage-5 polar-CLAHE pivot,
                or ``None`` when detection is absent / not confident (→ centroid
                pivot).
        """
        # Pre-rotation dims (canonical flip preserves size), needed to project
        # the detected fovea through the SAME expand-rotation into analysis space.
        # Captured before the reassignment below — Stage-1 rotation now grows the
        # canvas, so the post-rotation size is not the rotation pivot frame.
        src_h, src_w = image.shape[:2]

        # Stage 0: canonical orientation (flip + OD–fovea rotation). Build the
        # FOV mask from the CLEAN pre-rotation frame and carry it through the
        # identical flip+rotation (BORDER_CONSTANT) so the reflected "ears" the
        # RGB's BORDER_REFLECT rotation introduces are excluded from the FOV.
        od_fovea_result: ODFoveaResult | None = None
        mask_oriented: np.ndarray | None = None
        if self.config.use_canonical_flip or self.config.use_od_fovea_rotation:
            raw_mask = _fov_foreground_mask(image)
            image, od_fovea_result, mask_oriented = canonical_orientation(
                image,
                eye_side=eye_side if self.config.use_canonical_flip else "unknown",
                enable_rotation=self.config.use_od_fovea_rotation,
                fov_mask=raw_mask,
            )

        # Stage 2/3: FOV crop + isotropic resize (always) — keep the transform so
        # the fovea pivot can be mapped into the cropped analysis frame. Pass the
        # oriented mask so it is cropped with the identical bbox (None → segment
        # from the crop, used only when no orientation ran).
        image, fov_mask, crop_tf = crop_and_resize(
            image, self.config.target_size, return_transform=True,
            fov_mask=mask_oriented,
        )

        # Stage-5 polar-CLAHE pivot: the detected fovea, projected to analysis
        # space, only when the learned detector is confident (TASK-fix #4).
        fovea_pivot: tuple[float, float] | None = None
        if (
            self.config.use_od_fovea_rotation
            and od_fovea_result is not None
            and od_fovea_result.confident
        ):
            fovea_pivot = _project_to_analysis(
                od_fovea_result.fovea_center,
                od_fovea_result.angle_deg,
                src_w, src_h, crop_tf,
            )

        # Compute FOV diameter from mask for adaptive flat-field
        fov_rows = np.any(fov_mask > 0, axis=1)
        fov_diameter = float(np.sum(fov_rows))  # height of FOV region in pixels
        adaptive_sigma = self.config.flat_field_sigma_factor * fov_diameter

        # Stage 4: flat-field correction (adaptive σ)
        if self.config.use_flat_field:
            if self.config.flat_field_mode == "adaptive":
                sigma = adaptive_sigma
            else:
                sigma = self.config.flat_field_sigma
            image = apply_flat_field(
                image,
                sigma=sigma,
                mask=fov_mask if self.config.flat_field_mask_only else None,
            )

        return image, fov_mask, od_fovea_result, fovea_pivot

    def _finish(
        self,
        image: np.ndarray,
        fov_mask: np.ndarray,
        od_fovea_result: "ODFoveaResult | SimpleNamespace | None",
        fovea_pivot: "tuple[float, float] | None" = None,
    ) -> torch.Tensor:
        """Run the **stochastic** Stages 5–7 on a Stage-4 (flat-field) image.

        Shared by both the live :meth:`__call__` path and the cached
        :meth:`finish_from_cache` path, guaranteeing identical train/inference
        behaviour regardless of whether Stages 0–4 came from disk.

        Args:
            image: RGB uint8 array (Stage-4 flat-field output).
            fov_mask: float32 binary FOV mask (Stage 2 output).
            od_fovea_result: object exposing ``confident`` and
                ``rotation_sigma_deg`` (only fields Stage 6 reads), or ``None``.
            fovea_pivot: detected fovea centre in analysis-frame pixels for the
                Stage-5 polar-CLAHE pivot, or ``None`` → FOV-centroid pivot. Must
                be supplied identically on the live and cached paths so the two
                stay bit-identical.

        Returns:
            Normalised float32 tensor ``(4, target_size, target_size)``;
            channel 3 is the (un-augmented) FOV mask.
        """
        # Stage 5: CLAHE (stochastic at train time). When the learned detector
        # is confident, polar CLAHE pivots on the detected fovea (TASK-fix #4);
        # otherwise it falls back to the robust FOV-mask centroid
        # (``resolve_pivot`` also re-checks the pivot lands inside the FOV).
        if self.config.use_clahe:
            if self.config.clahe_mode == "polar":
                image = maybe_apply_polar_clahe(
                    image,
                    fov_mask,
                    params=self._polar_clahe_params,
                    is_training=self.is_training,
                    train_prob=self.config.clahe_train_prob,
                    fovea_xy=fovea_pivot,
                )
            else:
                image = maybe_apply_clahe(
                    image,
                    params=self._clahe_params,
                    is_training=self.is_training,
                    train_prob=self.config.clahe_train_prob,
                )

        # Stage 6: augmentation (train only, uint8, before normalize)
        if self.is_training:
            image = self._augmentation(image, od_fovea_result=od_fovea_result)

        # Stage 7: dataset-specific or ImageNet normalize → tensor (always last)
        if self.config.normalize_mode == "dataset_specific" and \
                self.config.dataset_mean is not None and \
                self.config.dataset_std is not None:
            mean = self.config.dataset_mean
            std = self.config.dataset_std
        else:
            mean = self.config.normalize_mean
            std = self.config.normalize_std

        rgb_tensor = imagenet_normalize(image, mean=mean, std=std)

        # Append FOV mask as 4th channel (un-augmented, mirrors live behaviour)
        mask_tensor = torch.from_numpy(fov_mask).unsqueeze(0)  # (1, H, W)
        return torch.cat([rgb_tensor, mask_tensor], dim=0)      # (4, H, W)

    # ------------------------------------------------------------------
    # Precompute-and-cache public API (throughput fix)
    # ------------------------------------------------------------------

    def precompute_deterministic(
        self,
        image: np.ndarray,
        eye_side: str = "unknown",
    ) -> tuple[np.ndarray, np.ndarray, bool, float, "tuple[float, float] | None"]:
        """Stages 0–4 for offline caching, from a raw (decoded) image.

        Handles ``input_color_space`` then runs :meth:`_precompute_rgb`,
        returning the cacheable scalars from the OD/fovea result rather than the
        full object: ``confident`` and ``rotation_sigma_deg`` (Stage 6) plus the
        analysis-frame ``fovea_pivot`` (Stage 5 polar pivot). Caching the pivot
        keeps the cached training path bit-identical to live inference.

        Args:
            image: Raw uint8 array matching ``input_color_space`` (``"bgr"`` for
                :func:`cv2.imread` output).
            eye_side: ``"left"``, ``"right"``, or ``"unknown"``.

        Returns:
            ``(flat_rgb_uint8, fov_mask_float32, confident, rotation_sigma_deg,
            fovea_pivot)`` where ``fovea_pivot`` is ``(x, y)`` in analysis-frame
            pixels or ``None``.
        """
        if self._input_color_space == "bgr":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        flat_rgb, fov_mask, od, fovea_pivot = self._precompute_rgb(image, eye_side)
        confident = bool(od.confident) if od is not None else False
        rotation_sigma_deg = float(od.rotation_sigma_deg) if od is not None else 0.0
        return flat_rgb, fov_mask, confident, rotation_sigma_deg, fovea_pivot

    def finish_from_cache(
        self,
        flat_rgb: np.ndarray,
        fov_mask: np.ndarray,
        confident: bool,
        rotation_sigma_deg: float,
        fovea_pivot: "tuple[float, float] | None" = None,
    ) -> torch.Tensor:
        """Stages 5–7 from cached Stage-4 output — the per-epoch train path.

        Equivalent to :meth:`__call__` for the full pipeline, but skips the
        expensive deterministic Stages 0–4 by consuming a cached flat-field
        image + FOV mask + the cached OD/fovea scalars.

        Args:
            flat_rgb: cached RGB uint8 Stage-4 image.
            fov_mask: cached float32 binary FOV mask.
            confident: cached ``ODFoveaResult.confident``.
            rotation_sigma_deg: cached ``ODFoveaResult.rotation_sigma_deg``.
            fovea_pivot: cached analysis-frame fovea pivot ``(x, y)`` or ``None``
                (older caches without the column read as ``None`` → centroid
                pivot, matching pre-Phase-2 behaviour).

        Returns:
            Normalised float32 tensor ``(4, target_size, target_size)``.
        """
        od = SimpleNamespace(
            confident=bool(confident),
            rotation_sigma_deg=float(rotation_sigma_deg),
        )
        return self._finish(flat_rgb, fov_mask, od, fovea_pivot)

    # ------------------------------------------------------------------
    # Stage breakdown (for the demo "what preprocessing does" panel)
    # ------------------------------------------------------------------

    def stage_breakdown(
        self,
        image: np.ndarray,
        eye_side: str = "unknown",
        with_heatmaps: bool = False,
        od_override: "ODFoveaResult | None" = None,
    ) -> dict:
        """Run preprocessing Stages 0–5 capturing each intermediate.

        Mirrors :meth:`__call__` up to (but excluding) augmentation and Stage 7
        normalize, returning the labelled intermediate images for the demo's
        preview strip (TASK-Demo §C.6) plus the FOV mask and OD/fovea result.
        Deterministic (inference mode): CLAHE is applied with no stochasticity.

        Args:
            image: Raw uint8 array matching ``input_color_space``.
            eye_side: ``"left"``, ``"right"``, or ``"unknown"``.
            with_heatmaps: If ``True``, request the learned detector's OD/fovea
                probability heatmaps and warp them into analysis space (added to
                ``od_fovea_analysis`` as ``od_heatmap``/``fovea_heatmap``). Used
                by the demo overlay (Phase 3).
            od_override: Optional clinician-corrected :class:`ODFoveaResult`
                (centres in the flipped frame) that replaces the learned
                detector. When given, the override's ``angle_deg`` drives the
                Stage-1 rotation and therefore every downstream stage — the
                demo's "Save correction" re-run.

        Returns:
            Dict with:
              - ``stages``: list of ``(label, rgb_uint8)`` from original →
                flip → rotation → FOV crop+resize → flat-field → CLAHE.
              - ``fov_mask``: float32 ``(H, W)`` mask (1.0 inside FOV).
              - ``od_fovea``: :class:`ODFoveaResult` or ``None``.
              - ``od_fovea_analysis``: OD/fovea centres and radii projected
                into the ``target_size`` analysis frame (the
                ``fov_crop_resize`` panel) so markers overlay it exactly, or
                ``None`` when no confident detection is available. When
                ``with_heatmaps`` and confident, also carries float32
                ``od_heatmap``/``fovea_heatmap`` on the analysis canvas.
              - ``transform``: dict with ``angle_deg``, ``crop_tf``, ``flipped``,
                ``src_w``, ``src_h``, ``space`` — the Stage 0/1/2 geometry needed
                to invert analysis-space coordinates back to input-image pixels
                (used by the demo correction endpoint), or ``None``.
        """
        if self._input_color_space == "bgr":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        stages: list[tuple[str, np.ndarray]] = [("original", image.copy())]

        # Stage 0: canonical flip only (for a dedicated panel).
        flipped = (
            canonical_flip(image, eye_side)
            if self.config.use_canonical_flip else image
        )
        stages.append(("canonical_flip", flipped.copy()))

        # Stage 0+1: flip + OD-fovea rotation (the real path), with OD result.
        # The FOV mask is segmented from the CLEAN pre-rotation frame and carried
        # through the same flip+rotation (BORDER_CONSTANT) so reflected "ears"
        # from the RGB's BORDER_REFLECT rotation are kept out of the FOV.
        od_fovea_result: ODFoveaResult | None = None
        mask_oriented: np.ndarray | None = None
        if (
            self.config.use_canonical_flip
            or self.config.use_od_fovea_rotation
            or od_override is not None
        ):
            raw_mask = _fov_foreground_mask(image)
            oriented, od_fovea_result, mask_oriented = canonical_orientation(
                image,
                eye_side=eye_side if self.config.use_canonical_flip else "unknown",
                enable_rotation=self.config.use_od_fovea_rotation,
                return_heatmaps=with_heatmaps,
                fov_mask=raw_mask,
                od_override=od_override,
            )
        else:
            oriented = image
        stages.append(("od_fovea_rotation", oriented.copy()))

        # Stage 2/3: FOV crop + isotropic resize → (image, mask, transform). Pass
        # the oriented mask so it is cropped with the identical bbox.
        cropped, fov_mask, crop_tf = crop_and_resize(
            oriented, self.config.target_size, return_transform=True,
            fov_mask=mask_oriented,
        )
        stages.append(("fov_crop_resize", cropped.copy()))

        # Project OD/fovea (detected in pre-rotation, pre-crop space) into the
        # cropped analysis frame so the demo can overlay markers on the
        # ``fov_crop_resize`` panel. Mirror the rotation applied inside
        # ``canonical_orientation`` (about the flipped image centre), then the
        # crop+resize transform. The projection is produced for ANY detection
        # (confident or not) so the demo can show a best-guess marker the
        # clinician can drag-correct even at low confidence. Because
        # ``canonical_orientation`` rotates the image only for confident
        # detections, project with the angle actually applied: ``angle_deg``
        # when confident, ``0`` otherwise (the analysis base is unrotated).
        od_fovea_analysis: dict | None = None
        fovea_pivot: tuple[float, float] | None = None
        if od_fovea_result is not None:
            src_h, src_w = image.shape[:2]
            applied_angle = (
                od_fovea_result.angle_deg if od_fovea_result.confident else 0.0
            )

            def _to_analysis(point: tuple[int, int]) -> list[float]:
                ax, ay = _project_to_analysis(
                    point, applied_angle, src_w, src_h, crop_tf
                )
                return [ax, ay]

            fovea_center_analysis = _to_analysis(od_fovea_result.fovea_center)
            # Polar-CLAHE pivots on the detected fovea ONLY for confident
            # detections — matching the model path, where low confidence falls
            # back to the FOV centroid (TASK-fix #4). The overlay projection
            # above must not change this gate, or the demo's stage strip would
            # diverge from what the CNN actually sees.
            if od_fovea_result.confident:
                fovea_pivot = (fovea_center_analysis[0], fovea_center_analysis[1])
            od_fovea_analysis = {
                "od_center": _to_analysis(od_fovea_result.od_center),
                "fovea_center": fovea_center_analysis,
                "od_radius": float(od_fovea_result.od_radius) * crop_tf.scale,
                "fovea_radius": float(od_fovea_result.fovea_radius) * crop_tf.scale,
                "space": int(self.config.target_size),
            }

            # Warp the detector's probability heatmaps (flipped pre-crop frame)
            # into the analysis canvas so the demo overlays them on the markers.
            if (
                with_heatmaps
                and od_fovea_result.od_heatmap is not None
                and od_fovea_result.fovea_heatmap is not None
            ):
                od_fovea_analysis["od_heatmap"] = _warp_heatmap_to_analysis(
                    od_fovea_result.od_heatmap,
                    applied_angle, src_w, src_h, crop_tf,
                )
                od_fovea_analysis["fovea_heatmap"] = _warp_heatmap_to_analysis(
                    od_fovea_result.fovea_heatmap,
                    applied_angle, src_w, src_h, crop_tf,
                )

        # Stage 4: flat-field correction (adaptive σ).
        flat = cropped
        if self.config.use_flat_field:
            if self.config.flat_field_mode == "adaptive":
                fov_rows = np.any(fov_mask > 0, axis=1)
                sigma = self.config.flat_field_sigma_factor * float(np.sum(fov_rows))
            else:
                sigma = self.config.flat_field_sigma
            flat = apply_flat_field(
                cropped, sigma=sigma,
                mask=fov_mask if self.config.flat_field_mask_only else None,
            )
        stages.append(("flat_field", flat.copy()))

        # Stage 5: CLAHE (deterministic at inference). Same dispatch as the
        # model path so the demo panel shows exactly what the CNN sees.
        clahed = flat
        if self.config.use_clahe:
            if self.config.clahe_mode == "polar":
                clahed = apply_polar_clahe(
                    flat, fov_mask, params=self._polar_clahe_params,
                    fovea_xy=fovea_pivot,
                )
            else:
                clahed = maybe_apply_clahe(
                    flat, params=self._clahe_params,
                    is_training=False, train_prob=self.config.clahe_train_prob,
                )
        stages.append(("clahe", clahed.copy()))

        # Geometry needed to invert analysis-space coordinates back to
        # input-image pixels (demo correction endpoint). ``angle_deg`` is the
        # Stage-1 rotation (0 when no confident detection drove a rotation).
        src_h, src_w = image.shape[:2]
        transform = {
            "angle_deg": (
                float(od_fovea_result.angle_deg)
                if (od_fovea_result is not None and od_fovea_result.confident)
                else 0.0
            ),
            "crop_tf": crop_tf,
            "flipped": bool(self.config.use_canonical_flip and eye_side == "left"),
            "src_w": int(src_w),
            "src_h": int(src_h),
            "space": int(self.config.target_size),
        }

        return {
            "stages": stages,
            "fov_mask": fov_mask,
            "od_fovea": od_fovea_result,
            "od_fovea_analysis": od_fovea_analysis,
            "transform": transform,
        }

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def is_active(self) -> bool:
        """Return ``True`` if main preprocessing components are enabled."""
        return self.config.use_flat_field and self.config.use_clahe

    def is_absent(self) -> bool:
        """Return ``True`` if pipeline is in baseline mode."""
        return self.config.mode == "baseline"

    # ------------------------------------------------------------------
    # Factory class-methods
    # ------------------------------------------------------------------

    @classmethod
    def create_for_training(
        cls,
        config: PreprocessingConfig,
        input_color_space: str = "bgr",
    ) -> "PreprocessingPipeline":
        """
        Create a pipeline in training mode (stochastic CLAHE + augmentation).

        Args:
            config: :class:`PreprocessingConfig` instance.
            input_color_space: ``"bgr"`` (default) or ``"rgb"``.

        Returns:
            :class:`PreprocessingPipeline` with ``is_training=True``.
        """
        return cls(
            config,
            is_training=True,
            input_color_space=input_color_space,
        )

    @classmethod
    def create_for_inference(
        cls,
        config: PreprocessingConfig,
        input_color_space: str = "bgr",
    ) -> "PreprocessingPipeline":
        """
        Create a pipeline in inference mode (deterministic, no augmentation).

        Args:
            config: :class:`PreprocessingConfig` instance.
            input_color_space: ``"bgr"`` (default) or ``"rgb"``.

        Returns:
            :class:`PreprocessingPipeline` with ``is_training=False``.
        """
        return cls(config, is_training=False, input_color_space=input_color_space)

    @classmethod
    def create_baseline(
        cls,
        target_size: int = 512,
        is_training: bool = False,
        input_color_space: str = "bgr",
    ) -> "PreprocessingPipeline":
        """Baseline: stretch-resize + ImageNet normalize (3 channels, no mask).

        This replicates what most competitors do in the literature.

        Args:
            target_size: Output spatial resolution in pixels.
            is_training: Unused (baseline has no stochastic components).
            input_color_space: ``"bgr"`` (default) or ``"rgb"``.

        Returns:
            :class:`PreprocessingPipeline` in baseline mode.
        """
        config = PreprocessingConfig(
            mode="baseline",
            use_canonical_flip=False,
            use_od_fovea_rotation=False,
            use_flat_field=False,
            use_clahe=False,
            use_color_jitter=False,
            use_gaussian_noise=False,
            use_jpeg_compression=False,
            use_shear=False,
            use_stretch=False,
            target_size=target_size,
            normalize_mode="imagenet",
        )
        return cls(config, is_training=is_training, input_color_space=input_color_space)
