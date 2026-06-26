"""
Stage 6: Augmentation — Unified Affine + ColorJitter + Gaussian Noise + JPEG.

Replaces :class:`FundusAugmentation` with an augmentation pipeline that applies,
in order:

1. a single unified affine transform (rotation + zoom + stretch + shear) with
   stochastic interpolation;
2. ColorJitter (brightness, contrast, saturation, hue) — each component sampled
   and applied independently;
3. Gaussian noise (acquisition-variability simulation);
4. JPEG compression (acquisition-variability simulation).

Applied to **RGB uint8** images *before* the Stage-7 normalisation.  All
sub-transforms are individually toggleable via :class:`PreprocessingConfig`.

References
----------
Work 2: kaggle_diabetic, team o_O, 2nd place Kaggle DR 2015.
Wang et al., "Rotation Has Two Sides", ICLR 2024 (rotation distribution).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.preprocessing.od_fovea_detect import ODFoveaResult

import cv2
import numpy as np

from src.preprocessing.config import PreprocessingConfig


class UnifiedFundusAugmentation:
    """
    Augmentation: unified affine + ColorJitter + Gaussian noise + JPEG.

    Applied to uint8 RGB images before the Stage-7 normalisation.  All
    sub-transforms are controlled by the boolean toggles in *config*.

    Args:
        config: :class:`PreprocessingConfig` controlling all augmentation
            parameters and toggle flags.
    """

    def __init__(self, config: PreprocessingConfig) -> None:
        self.config = config

    # ------------------------------------------------------------------
    # Public callable
    # ------------------------------------------------------------------

    def __call__(
        self,
        image: np.ndarray,
        od_fovea_result: ODFoveaResult | None = None,
    ) -> np.ndarray:
        """
        Apply the full augmentation pipeline to one image.

        Application order:
        1. Unified affine (rotation + zoom + stretch + shear)
        2. ColorJitter (brightness, contrast, saturation, hue)
        3. Gaussian noise
        4. JPEG compression

        Args:
            image: RGB uint8 NumPy array of shape ``(H, W, 3)``.
            od_fovea_result: Optional detection result from Stage 0b.
                When provided and confident, the rotation σ is derived
                from OD/fovea localization uncertainty instead of the
                fixed ``config.rotation_sigma``.

        Returns:
            Augmented RGB uint8 NumPy array of the same shape.
        """
        h, w = image.shape[:2]
        center = (w / 2.0, h / 2.0)

        # 1. Unified affine
        params = self._sample_affine_params(od_fovea_result=od_fovea_result)
        M = self._build_affine_matrix(
            theta=params["theta"],
            sx=params["sx"],
            sy=params["sy"],
            shear_rad=params["shear_rad"],
            center=center,
        )
        interp = self._sample_interpolation()
        image = self._apply_affine(image, M, interp)

        # 2. ColorJitter (brightness / contrast / saturation / hue)
        if self.config.use_color_jitter:
            image = self._apply_color_jitter(image)

        # 3. Gaussian noise
        if self.config.use_gaussian_noise:
            image = self._apply_gaussian_noise(image)

        # 4. JPEG compression
        if self.config.use_jpeg_compression:
            image = self._apply_jpeg_compression(image)

        return image

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _sample_affine_params(
        self,
        od_fovea_result: ODFoveaResult | None = None,
    ) -> dict[str, float]:
        """
        Sample affine transform parameters.

        Args:
            od_fovea_result: Optional OD/fovea detection result.
                When provided, confident, and ``config.adaptive_rotation_sigma``
                is enabled, the rotation σ is derived from localization
                uncertainty.  Otherwise ``config.fallback_rotation_sigma``
                (or ``config.rotation_sigma`` if adaptive is disabled) is used.

        Returns:
            Dict with keys ``theta`` (°), ``sx``, ``sy``, ``shear_rad`` (rad).
        """
        cfg = self.config

        # Rotation σ: adaptive (per-image) or fixed (fallback)
        if (
            cfg.adaptive_rotation_sigma
            and od_fovea_result is not None
            and od_fovea_result.confident
        ):
            rotation_sigma = od_fovea_result.rotation_sigma_deg
        elif cfg.adaptive_rotation_sigma:
            # Adaptive enabled but detection failed → use fallback
            rotation_sigma = cfg.fallback_rotation_sigma
        else:
            # Adaptive disabled → use original fixed σ
            rotation_sigma = cfg.rotation_sigma

        # Rotation: truncated Gaussian, clipped at ±rotation_clip
        theta = float(np.random.normal(0.0, rotation_sigma))
        theta = float(np.clip(theta, -cfg.rotation_clip, cfg.rotation_clip))

        # Zoom: isotropic, log-uniform in zoom_range
        log_zoom = np.random.uniform(
            np.log(cfg.zoom_range[0]),
            np.log(cfg.zoom_range[1]),
        )
        zoom = float(np.exp(log_zoom))

        # Stretch: anisotropic, log-uniform in stretch_range
        if cfg.use_stretch:
            log_stretch = np.random.uniform(
                np.log(cfg.stretch_range[0]),
                np.log(cfg.stretch_range[1]),
            )
            stretch = float(np.exp(log_stretch))
        else:
            stretch = 1.0

        sx = zoom * stretch
        sy = zoom / stretch

        # Shear: conditional
        if cfg.use_shear and np.random.rand() < cfg.shear_prob:
            shear_deg = float(np.random.uniform(cfg.shear_range[0], cfg.shear_range[1]))
        else:
            shear_deg = 0.0
        shear_rad = float(np.deg2rad(shear_deg))

        return {"theta": theta, "sx": sx, "sy": sy, "shear_rad": shear_rad}

    def _build_affine_matrix(
        self,
        theta: float,
        sx: float,
        sy: float,
        shear_rad: float,
        center: tuple[float, float],
    ) -> np.ndarray:
        """
        Build a unified 2×3 affine matrix combining rotation, scale, and shear.

        Args:
            theta: Rotation angle in degrees.
            sx: Horizontal scale factor (zoom × stretch).
            sy: Vertical scale factor (zoom / stretch).
            shear_rad: Shear angle in radians.
            center: Image centre ``(cx, cy)`` in pixels.

        Returns:
            2×3 float64 affine matrix for :func:`cv2.warpAffine`.
        """
        M = cv2.getRotationMatrix2D(center, theta, 1.0)   # (2, 3)
        M_full = np.array([
            [M[0, 0] * sx,  M[0, 1] + np.tan(shear_rad),  M[0, 2]],
            [M[1, 0],        M[1, 1] * sy,                  M[1, 2]],
        ], dtype=np.float64)
        return M_full

    def _sample_interpolation(self) -> int:
        """
        Sample a cv2 interpolation flag stochastically.

        Probabilities: 60 % LINEAR, 30 % CUBIC, 10 % NEAREST (from
        ``config.interp_weights``).

        Returns:
            One of ``cv2.INTER_LINEAR``, ``cv2.INTER_CUBIC``,
            ``cv2.INTER_NEAREST``.
        """
        flags = [cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_NEAREST]
        weights = list(self.config.interp_weights)
        # numpy choice requires integer indices; use cumulative sum
        r = np.random.rand()
        cumulative = 0.0
        for flag, w in zip(flags, weights):
            cumulative += w
            if r < cumulative:
                return flag
        return cv2.INTER_LINEAR  # fallback

    def _apply_affine(
        self,
        image: np.ndarray,
        M: np.ndarray,
        interp: int,
    ) -> np.ndarray:
        """
        Warp *image* with affine matrix *M*.

        Args:
            image: RGB uint8 array of shape ``(H, W, 3)``.
            M: 2×3 affine matrix.
            interp: cv2 interpolation flag.

        Returns:
            Warped RGB uint8 array of the same shape.
        """
        h, w = image.shape[:2]
        return cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=interp,
            borderMode=self.config.border_mode,
        )

    def _apply_color_jitter(self, image: np.ndarray) -> np.ndarray:
        """
        Apply ColorJitter (brightness, contrast, saturation, hue).

        Each component is sampled from its configured range and applied
        independently with probability ``config.color_jitter_prob``.  Brightness
        and contrast operate in RGB; saturation and hue operate in HSV.

        Args:
            image: RGB uint8 array of shape ``(H, W, 3)``.

        Returns:
            Jittered RGB uint8 array of the same shape.
        """
        cfg = self.config
        img = image.astype(np.float32)

        # Brightness: scale RGB intensities.
        if np.random.rand() < cfg.color_jitter_prob:
            factor = float(np.random.uniform(*cfg.color_jitter_brightness_range))
            img = img * factor

        # Contrast: blend toward the per-image grayscale mean.
        if np.random.rand() < cfg.color_jitter_prob:
            factor = float(np.random.uniform(*cfg.color_jitter_contrast_range))
            gray_mean = float(
                np.mean(img @ np.array([0.299, 0.587, 0.114], dtype=np.float32))
            )
            img = (img - gray_mean) * factor + gray_mean

        img = np.clip(img, 0, 255)

        # Saturation: blend toward the per-pixel grayscale image.
        if np.random.rand() < cfg.color_jitter_prob:
            factor = float(np.random.uniform(*cfg.color_jitter_saturation_range))
            gray = img @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
            img = gray[..., None] + factor * (img - gray[..., None])
            img = np.clip(img, 0, 255)

        # Hue: rotate the H channel in HSV space.
        if np.random.rand() < cfg.color_jitter_prob:
            # hue range is a fraction of the colour circle ([-0.5, 0.5]); OpenCV
            # encodes hue in [0, 180), so scale the shift by 180.
            shift = float(np.random.uniform(*cfg.color_jitter_hue_range)) * 180.0
            hsv = cv2.cvtColor(
                np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV
            ).astype(np.float32)
            hsv[..., 0] = (hsv[..., 0] + shift) % 180.0
            img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)

        return np.clip(img, 0, 255).astype(np.uint8)

    def _apply_gaussian_noise(self, image: np.ndarray) -> np.ndarray:
        """
        Add zero-mean Gaussian noise with probability ``config.gaussian_noise_prob``.

        The standard deviation is sampled uniformly from
        ``config.gaussian_noise_sigma_range`` on the 8-bit RGB scale.

        Args:
            image: RGB uint8 array.

        Returns:
            Noisy RGB uint8 array (or original if skipped).
        """
        if np.random.rand() >= self.config.gaussian_noise_prob:
            return image

        sigma = float(np.random.uniform(*self.config.gaussian_noise_sigma_range))
        noise = np.random.normal(0.0, sigma, size=image.shape).astype(np.float32)
        img_float = image.astype(np.float32) + noise
        return np.clip(img_float, 0, 255).astype(np.uint8)

    def _apply_jpeg_compression(self, image: np.ndarray) -> np.ndarray:
        """
        Apply lossy JPEG re-compression with probability ``config.jpeg_prob``.

        The quality factor is sampled uniformly from
        ``config.jpeg_quality_range``.  The image is round-tripped through the
        JPEG codec (RGB→BGR for encoding so the codec's YCbCr transform matches
        real-world acquisition, then BGR→RGB back).

        Args:
            image: RGB uint8 array.

        Returns:
            Re-compressed RGB uint8 array (or original if skipped).
        """
        if np.random.rand() >= self.config.jpeg_prob:
            return image

        lo, hi = self.config.jpeg_quality_range
        quality = int(np.random.randint(int(lo), int(hi) + 1))
        bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        ok, buf = cv2.imencode(".jpg", bgr, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        if not ok:
            return image
        decoded = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        return cv2.cvtColor(decoded, cv2.COLOR_BGR2RGB)
