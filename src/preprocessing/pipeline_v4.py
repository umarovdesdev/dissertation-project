"""
V4 Pipeline Orchestrator.

:class:`PreprocessingPipelineV4` chains all six V4 stages in the correct order.
It is the main public interface for the V4 preprocessing stack.

Stage execution order
---------------------
Preprocessing (train + inference):
  0. Canonical flip      — left→right eye orientation
  1. FOV crop + resize   — always
  2. Flat-field          — toggleable (``use_flat_field``)
  3. Upgraded CLAHE      — toggleable, stochastic at train time
  4. ImageNet normalize  — always last, outputs ``torch.Tensor``

Augmentation (train only, inserted before Stage 4):
  5. Unified affine + brightness/contrast + PCA colour jitter

The V3 :class:`~src.preprocessing.pipeline.PreprocessingPipeline` is left
intact for backward compatibility with exp2–exp6.
"""

from __future__ import annotations

import numpy as np
import torch

from .canonical_orientation import canonical_flip, canonical_orientation
from .od_fovea_detect import ODFoveaResult
from .config import PreprocessingV4Config
from .crop_resize import crop_and_resize
from .flat_field import apply_flat_field
from .imagenet_normalize import imagenet_normalize
from .upgraded_clahe import ClaheParams, maybe_apply_clahe
# NOTE: FundusAugmentationV4 is imported lazily inside __init__ to avoid
# circular imports (src.data imports from src.preprocessing and vice-versa).


class PreprocessingPipelineV4:
    """
    V4 6-stage preprocessing + augmentation pipeline.

    Preprocessing stages 0–4 are applied identically at train and inference
    (except Stage 3 CLAHE, which is stochastic at train time).  Stage 5
    augmentation is applied only during training, inserted *before* Stage 4
    normalisation so that it operates on uint8 images.

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
        config: :class:`PreprocessingV4Config` controlling all parameters
            and toggle flags.
        is_training: ``True`` enables stochastic CLAHE and augmentation.
        pca_eigvecs: PCA eigenvectors of shape ``(3, 3)`` for colour
            augmentation.  ``None`` disables PCA colour jitter.
        pca_eigvals: PCA eigenvalues of shape ``(3,)``.  ``None`` disables
            PCA colour jitter.
        input_color_space: ``"bgr"`` or ``"rgb"``.  Controls BGR→RGB
            conversion at the pipeline entry point.  Default ``"bgr"``
            matches :func:`cv2.imread` output.
    """

    def __init__(
        self,
        config: PreprocessingV4Config,
        is_training: bool = False,
        pca_eigvecs: np.ndarray | None = None,
        pca_eigvals: np.ndarray | None = None,
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
        # Lazy import to break the circular dependency with src.data
        from src.data.augmentation_v4 import FundusAugmentationV4  # noqa: PLC0415
        self._augmentation = FundusAugmentationV4(
            config=config,
            pca_eigvecs=pca_eigvecs,
            pca_eigvals=pca_eigvals,
        )

    # ------------------------------------------------------------------
    # Core callable
    # ------------------------------------------------------------------

    def __call__(
        self,
        image: np.ndarray,
        eye_side: str = "unknown",
    ) -> torch.Tensor:
        """
        Apply the full V4 pipeline to one image.

        Args:
            image: Raw image as a uint8 NumPy array of shape ``(H, W, 3)``.
                Must match ``input_color_space`` set at construction:
                ``"bgr"`` for :func:`cv2.imread` output,
                ``"rgb"`` for PIL/already-converted arrays.
            eye_side: ``"left"``, ``"right"``, or ``"unknown"``.

        Returns:
            ImageNet-normalised float32 tensor of shape
            ``(4, target_size, target_size)``.
            Channel 3 is a binary FOV mask (1.0 = real data, 0.0 = padding).
        """
        # Convert to RGB if input is BGR (e.g. from cv2.imread).
        # If caller already provides RGB, pass input_color_space="rgb" at construction.
        if self._input_color_space == "bgr":
            import cv2
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Stage 0: canonical orientation (flip + OD–fovea rotation)
        od_fovea_result: ODFoveaResult | None = None
        if self.config.use_canonical_flip or self.config.use_od_fovea_rotation:
            image, od_fovea_result = canonical_orientation(
                image,
                eye_side=eye_side if self.config.use_canonical_flip else "unknown",
                enable_rotation=self.config.use_od_fovea_rotation,
            )

        # Stage 1: FOV crop + isotropic resize (always) — returns (image, mask)
        image, fov_mask = crop_and_resize(image, self.config.target_size)

        # Stage 2: flat-field correction
        if self.config.use_flat_field:
            image = apply_flat_field(image, self.config.flat_field_sigma)

        # Stage 3: upgraded CLAHE (stochastic at train time)
        if self.config.use_clahe:
            image = maybe_apply_clahe(
                image,
                params=self._clahe_params,
                is_training=self.is_training,
                train_prob=self.config.clahe_train_prob,
            )

        # Stage 5: augmentation (train only, uint8, before normalize)
        if self.is_training:
            image = self._augmentation(image, od_fovea_result=od_fovea_result)

        # Stage 4: ImageNet normalize → tensor (always last)
        rgb_tensor = imagenet_normalize(
            image,
            mean=self.config.normalize_mean,
            std=self.config.normalize_std,
        )

        # Append FOV mask as 4th channel
        mask_tensor = torch.from_numpy(fov_mask).unsqueeze(0)  # (1, H, W)
        return torch.cat([rgb_tensor, mask_tensor], dim=0)      # (4, H, W)

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def is_active(self) -> bool:
        """Return ``True`` if main preprocessing components are enabled."""
        return self.config.use_flat_field and self.config.use_clahe

    def is_absent(self) -> bool:
        """Return ``True`` if only crop + resize + normalize are active (baseline)."""
        return not self.config.use_flat_field and not self.config.use_clahe

    # ------------------------------------------------------------------
    # Factory class-methods
    # ------------------------------------------------------------------

    @classmethod
    def create_for_training(
        cls,
        config: PreprocessingV4Config,
        pca_eigvecs: np.ndarray | None = None,
        pca_eigvals: np.ndarray | None = None,
        input_color_space: str = "bgr",
    ) -> "PreprocessingPipelineV4":
        """
        Create a pipeline in training mode (stochastic CLAHE + augmentation).

        Args:
            config: :class:`PreprocessingV4Config` instance.
            pca_eigvecs: Optional PCA eigenvectors for colour jitter.
            pca_eigvals: Optional PCA eigenvalues for colour jitter.
            input_color_space: ``"bgr"`` (default) or ``"rgb"``.

        Returns:
            :class:`PreprocessingPipelineV4` with ``is_training=True``.
        """
        return cls(
            config,
            is_training=True,
            pca_eigvecs=pca_eigvecs,
            pca_eigvals=pca_eigvals,
            input_color_space=input_color_space,
        )

    @classmethod
    def create_for_inference(
        cls,
        config: PreprocessingV4Config,
        input_color_space: str = "bgr",
    ) -> "PreprocessingPipelineV4":
        """
        Create a pipeline in inference mode (deterministic, no augmentation).

        Args:
            config: :class:`PreprocessingV4Config` instance.
            input_color_space: ``"bgr"`` (default) or ``"rgb"``.

        Returns:
            :class:`PreprocessingPipelineV4` with ``is_training=False``.
        """
        return cls(config, is_training=False, input_color_space=input_color_space)

    @classmethod
    def create_baseline(
        cls,
        target_size: int = 512,
        is_training: bool = False,
        input_color_space: str = "bgr",
    ) -> "PreprocessingPipelineV4":
        """
        Create a minimal baseline pipeline (crop + resize + normalize only).

        All optional preprocessing components (canonical flip, flat-field,
        CLAHE) and all augmentation sub-stages are disabled.

        Args:
            target_size: Output spatial resolution in pixels.
            is_training: Whether to enable augmentation (no-op here since
                all augmentation toggles are off).
            input_color_space: ``"bgr"`` (default) or ``"rgb"``.

        Returns:
            :class:`PreprocessingPipelineV4` configured as a resize-only baseline.
        """
        config = PreprocessingV4Config(
            use_canonical_flip=False,
            use_flat_field=False,
            use_clahe=False,
            use_pca_color=False,
            use_brightness_contrast=False,
            use_shear=False,
            use_stretch=False,
            target_size=target_size,
        )
        return cls(config, is_training=is_training, input_color_space=input_color_space)
