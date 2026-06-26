"""Two-view 4-channel SSL augmentation (brief §4 — binding channel contract).

The single most important correctness rule (§4.3):

- GEOMETRIC ops apply to ALL 4 channels together (RGB + FOV mask), so the mask
  stays spatially consistent with the image. After interpolation the mask is
  re-thresholded back to {0, 1}.
- PHOTOMETRIC ops apply to the RGB channels ONLY, NEVER the mask channel — the
  mask is a geometry indicator, not an image.

Input to :class:`TwoViewTransform` is a 4-channel float tensor ``[R, G, B, M]``
with RGB in ``[0, 1]`` and ``M`` in ``{0, 1}`` (the deterministic Stage 0–5 base
produced by :class:`~src.ssl.dataset.EyePACSSSLDataset`). Each view returns a
normalized 4-channel tensor: RGB normalized with the configured mean/std, mask
left binary and un-normalized.
"""

from __future__ import annotations

import random
from typing import Any, Sequence

import torch
import torchvision.transforms as T
import torchvision.transforms.functional as F


class _SingleView:
    """One stochastic 4-channel view (geometric-on-all, photometric-on-RGB).

    Args:
        out_size: Output spatial size (square), e.g. 256.
        crop_scale: ``(min, max)`` area scale for RandomResizedCrop.
        color_jitter: ``(brightness, contrast, saturation, hue)`` strengths.
        color_jitter_prob: Probability of applying ColorJitter (RGB only).
        grayscale_prob: Probability of RandomGrayscale (RGB only).
        blur_prob: Probability of Gaussian blur for this view (RGB only).
        solarize_prob: Probability of solarize for this view (RGB only).
        hflip_prob: Probability of horizontal flip (all 4 channels).
        mean: Per-channel RGB normalization mean (3,).
        std: Per-channel RGB normalization std (3,).
    """

    def __init__(
        self,
        out_size: int,
        crop_scale: tuple[float, float],
        color_jitter: tuple[float, float, float, float],
        color_jitter_prob: float,
        grayscale_prob: float,
        blur_prob: float,
        solarize_prob: float,
        hflip_prob: float,
        mean: Sequence[float],
        std: Sequence[float],
    ) -> None:
        self.out_size = int(out_size)
        self.crop_scale = (float(crop_scale[0]), float(crop_scale[1]))
        self.color_jitter_prob = float(color_jitter_prob)
        self.grayscale_prob = float(grayscale_prob)
        self.blur_prob = float(blur_prob)
        self.solarize_prob = float(solarize_prob)
        self.hflip_prob = float(hflip_prob)
        self.mean = list(mean)
        self.std = list(std)

        b, c, s, h = color_jitter
        self._color_jitter = T.ColorJitter(brightness=b, contrast=c, saturation=s, hue=h)
        # Kernel ~ 10% of size (odd), matching SimCLR/BYOL blur convention.
        k = max(3, int(0.1 * self.out_size) | 1)
        self._blur = T.GaussianBlur(kernel_size=k, sigma=(0.1, 2.0))

    def __call__(self, base: torch.Tensor) -> torch.Tensor:
        """Produce one augmented, normalized 4-channel view.

        Args:
            base: 4-channel float tensor ``(4, H, W)`` — RGB in ``[0, 1]``,
                mask in ``{0, 1}``.

        Returns:
            4-channel float tensor ``(4, out_size, out_size)``: normalized RGB +
            binary mask.
        """
        # --- GEOMETRIC (all 4 channels, shared sampled params) ---
        i, j, h, w = T.RandomResizedCrop.get_params(
            base, scale=self.crop_scale, ratio=(3.0 / 4.0, 4.0 / 3.0)
        )
        x = F.resized_crop(
            base, i, j, h, w, [self.out_size, self.out_size],
            interpolation=F.InterpolationMode.BILINEAR, antialias=True,
        )
        if random.random() < self.hflip_prob:
            x = F.hflip(x)

        # --- split: RGB vs mask ---
        rgb = x[:3].clamp(0.0, 1.0)
        mask = x[3:4]

        # --- PHOTOMETRIC (RGB only) ---
        if random.random() < self.color_jitter_prob:
            rgb = self._color_jitter(rgb)
        if random.random() < self.grayscale_prob:
            rgb = F.rgb_to_grayscale(rgb, num_output_channels=3)
        if random.random() < self.blur_prob:
            rgb = self._blur(rgb)
        if random.random() < self.solarize_prob:
            rgb = F.solarize(rgb.clamp(0.0, 1.0), threshold=0.5)

        # --- Stage 7: normalize RGB only ---
        rgb = F.normalize(rgb.clamp(0.0, 1.0), mean=self.mean, std=self.std)

        # --- re-binarize mask (interpolation may have produced fractional values) ---
        mask = (mask > 0.5).float()

        return torch.cat([rgb, mask], dim=0)


class TwoViewTransform:
    """Generate two independently-augmented 4-channel views of one base tensor.

    The two views use asymmetric blur/solarize probabilities (BYOL/MoCo/SimSiam
    convention): view 1 always blurs and never solarizes; view 2 rarely blurs
    and may solarize.

    Args:
        out_size: Output spatial size (square), e.g. 256.
        crop_scale: ``(min, max)`` area scale for RandomResizedCrop.
        color_jitter: ``(brightness, contrast, saturation, hue)`` strengths.
        color_jitter_prob: Probability of ColorJitter (RGB only).
        grayscale_prob: Probability of RandomGrayscale (RGB only).
        blur_prob_view1: Gaussian-blur probability for view 1.
        blur_prob_view2: Gaussian-blur probability for view 2.
        solarize_prob_view2: Solarize probability for view 2 (view 1 = 0).
        hflip_prob: Horizontal-flip probability (all 4 channels). Default 0.5.
        mean: Per-channel RGB normalization mean (3,).
        std: Per-channel RGB normalization std (3,).
    """

    def __init__(
        self,
        out_size: int,
        crop_scale: tuple[float, float] = (0.2, 1.0),
        color_jitter: tuple[float, float, float, float] = (0.4, 0.4, 0.2, 0.1),
        color_jitter_prob: float = 0.8,
        grayscale_prob: float = 0.2,
        blur_prob_view1: float = 1.0,
        blur_prob_view2: float = 0.1,
        solarize_prob_view2: float = 0.2,
        hflip_prob: float = 0.5,
        mean: Sequence[float] = (0.485, 0.456, 0.406),
        std: Sequence[float] = (0.229, 0.224, 0.225),
    ) -> None:
        self.view1 = _SingleView(
            out_size, crop_scale, color_jitter, color_jitter_prob, grayscale_prob,
            blur_prob=blur_prob_view1, solarize_prob=0.0, hflip_prob=hflip_prob,
            mean=mean, std=std,
        )
        self.view2 = _SingleView(
            out_size, crop_scale, color_jitter, color_jitter_prob, grayscale_prob,
            blur_prob=blur_prob_view2, solarize_prob=solarize_prob_view2,
            hflip_prob=hflip_prob, mean=mean, std=std,
        )

    def __call__(self, base: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Return the positive pair ``(view1, view2)`` for a base tensor.

        Args:
            base: 4-channel float tensor ``(4, H, W)`` — RGB in ``[0, 1]``,
                mask in ``{0, 1}``.

        Returns:
            Tuple ``(v1, v2)`` of normalized 4-channel tensors.
        """
        return self.view1(base), self.view2(base)


def resolve_normalize_stats(
    config: dict[str, Any],
) -> tuple[tuple[float, float, float], tuple[float, float, float], str]:
    """Resolve the Stage-7 RGB normalize mean/std for the SSL base tensor (§4.1).

    Prefers EyePACS dataset-specific stats from ``config.preprocessing`` when
    present; otherwise falls back to ImageNet (an acceptable stopgap — the
    choice is recorded in the manifest).

    Args:
        config: Full config dict.

    Returns:
        Tuple ``(mean, std, source)`` where ``source`` is ``"dataset_specific"``
        or ``"imagenet"``.
    """
    pre = config.get("preprocessing", {}) or {}
    mean = pre.get("dataset_mean")
    std = pre.get("dataset_std")
    if mean and std:
        return tuple(mean), tuple(std), "dataset_specific"
    imnet_mean = pre.get("imagenet_mean", (0.485, 0.456, 0.406))
    imnet_std = pre.get("imagenet_std", (0.229, 0.224, 0.225))
    return tuple(imnet_mean), tuple(imnet_std), "imagenet"


def build_two_view_transform(config: dict[str, Any]) -> TwoViewTransform:
    """Build a :class:`TwoViewTransform` from the ``ssl`` config block.

    Args:
        config: Full config dict (reads ``ssl.image_size`` and ``ssl.augment``,
            plus normalize stats via :func:`resolve_normalize_stats`).

    Returns:
        A configured :class:`TwoViewTransform`.
    """
    ssl_cfg = config["ssl"]
    aug = ssl_cfg.get("augment", {})
    mean, std, _src = resolve_normalize_stats(config)
    return TwoViewTransform(
        out_size=int(ssl_cfg.get("image_size", 256)),
        crop_scale=tuple(aug.get("global_crop_scale", (0.2, 1.0))),
        color_jitter=tuple(aug.get("color_jitter", (0.4, 0.4, 0.2, 0.1))),
        color_jitter_prob=float(aug.get("color_jitter_prob", 0.8)),
        grayscale_prob=float(aug.get("grayscale_prob", 0.2)),
        blur_prob_view1=float(aug.get("blur_prob_view1", 1.0)),
        blur_prob_view2=float(aug.get("blur_prob_view2", 0.1)),
        solarize_prob_view2=float(aug.get("solarize_prob_view2", 0.2)),
        hflip_prob=float(aug.get("hflip_prob", 0.5)),
        mean=mean,
        std=std,
    )
