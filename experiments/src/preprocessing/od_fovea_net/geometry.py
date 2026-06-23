"""FOV crop + isotropic resize with an exact forward/inverse affine.

This is a self-contained reimplementation of the monorepo's
``src/preprocessing/crop_resize.py`` concept. The detector must operate on a
FOV-cropped, isotropically-resized square frame (so the dark vignette that
broke the classical fovea search is gone), and it must be able to map
coordinates *both* ways:

* forward  — original-image pixels -> FOV frame pixels (to place GT targets);
* inverse  — FOV frame pixels -> original-image pixels (to return API coords).

The transform is a similarity transform (crop offset + single isotropic scale
+ centering pad), so the inverse is closed-form and exact. The forward then
inverse round-trip recovers the input point to floating-point precision (this
is asserted by ``tests/test_geometry.py``).

All images are RGB ``uint8`` NumPy arrays ``(H, W, 3)``. No torch dependency.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image, ImageFilter


@dataclass
class FovTransform:
    """Forward/inverse mapping between source pixels and the FOV frame.

    The mapping for a source point ``(x, y)`` into the padded ``target_size``
    canvas is::

        x_frame = (x - left) * scale + x_off
        y_frame = (y - upper) * scale + y_off

    Attributes:
        bbox: ``(left, upper, right, lower)`` crop box in source pixels.
        scale: Isotropic scale factor applied after cropping.
        x_off: Horizontal padding offset on the output canvas.
        y_off: Vertical padding offset on the output canvas.
        new_w: Width of the resized (pre-pad) region.
        new_h: Height of the resized (pre-pad) region.
        target_size: Output canvas side length (square).
    """

    bbox: tuple[int, int, int, int]
    scale: float
    x_off: int
    y_off: int
    new_w: int
    new_h: int
    target_size: int

    def apply(self, x: float, y: float) -> tuple[float, float]:
        """Map a source-image point into FOV-frame (canvas) pixels.

        Args:
            x: Source-image x coordinate (pixels).
            y: Source-image y coordinate (pixels).

        Returns:
            ``(x_frame, y_frame)`` in the padded ``target_size`` canvas.
        """
        left, upper = self.bbox[0], self.bbox[1]
        return (
            (x - left) * self.scale + self.x_off,
            (y - upper) * self.scale + self.y_off,
        )

    def invert(self, x_frame: float, y_frame: float) -> tuple[float, float]:
        """Map a FOV-frame point back to source-image pixels.

        Args:
            x_frame: FOV-frame x coordinate (pixels).
            y_frame: FOV-frame y coordinate (pixels).

        Returns:
            ``(x, y)`` in original source-image pixels.
        """
        left, upper = self.bbox[0], self.bbox[1]
        return (
            (x_frame - self.x_off) / self.scale + left,
            (y_frame - self.y_off) / self.scale + upper,
        )


def detect_fov_bbox(image: np.ndarray) -> tuple[int, int, int, int]:
    """Detect the fundus FOV bounding box, robust to vignette/border.

    Strategy: grayscale + low threshold to drop the dark border, then take the
    bounding box of the largest connected foreground region. Falls back to the
    full image if nothing credible is found. Unlike the monorepo helper this
    does not restrict to landscape images — IDRiD/EyePACS frames vary.

    Args:
        image: RGB uint8 array ``(H, W, 3)``.

    Returns:
        ``(left, upper, right, lower)`` crop box in source pixels.
    """
    h, w = image.shape[:2]
    # Mild blur to suppress speckle, then threshold the luminance.
    pil = Image.fromarray(image).convert("L").filter(ImageFilter.BLUR)
    gray = np.asarray(pil)
    # Background estimate from the image corners (robust to bright fundus).
    corner = np.concatenate([
        gray[:h // 16 + 1, :w // 16 + 1].ravel(),
        gray[:h // 16 + 1, -w // 16 - 1:].ravel(),
        gray[-h // 16 - 1:, :w // 16 + 1].ravel(),
        gray[-h // 16 - 1:, -w // 16 - 1:].ravel(),
    ])
    bg = float(np.median(corner))
    thresh = max(bg + 10.0, 15.0)
    fg = (gray > thresh).astype(np.uint8)

    num, labels, stats, _ = cv2.connectedComponentsWithStats(fg, connectivity=8)
    if num <= 1:
        return (0, 0, w, h)
    # Largest component excluding the background label 0.
    areas = stats[1:, cv2.CC_STAT_AREA]
    idx = int(np.argmax(areas)) + 1
    x = int(stats[idx, cv2.CC_STAT_LEFT])
    y = int(stats[idx, cv2.CC_STAT_TOP])
    bw = int(stats[idx, cv2.CC_STAT_WIDTH])
    bh = int(stats[idx, cv2.CC_STAT_HEIGHT])
    left, upper, right, lower = x, y, x + bw, y + bh

    # Sanity: a credible FOV is at least 40% of the frame in both dims.
    if (right - left) < 0.4 * w or (lower - upper) < 0.4 * h:
        return (0, 0, w, h)
    return (left, upper, right, lower)


def crop_and_resize(
    image: np.ndarray,
    target_size: int = 512,
) -> tuple[np.ndarray, np.ndarray, FovTransform]:
    """FOV-crop + isotropic-resize an image to ``target_size`` square.

    Mirrors the monorepo's ``crop_and_resize`` (isotropic scale + centered
    zero-pad) but always returns the geometric transform so coordinates can be
    mapped in both directions.

    Args:
        image: RGB uint8 array ``(H, W, 3)``.
        target_size: Output side length in pixels (square canvas).

    Returns:
        Tuple of:
          * canvas: RGB uint8 array ``(target_size, target_size, 3)``.
          * mask: float32 array ``(target_size, target_size)``; 1.0 = real
            data, 0.0 = padding.
          * transform: the :class:`FovTransform` used (forward + inverse).
    """
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(f"expected RGB (H, W, 3), got shape {image.shape}")

    bbox = detect_fov_bbox(image)
    left, upper, right, lower = bbox
    crop = image[upper:lower, left:right]
    crop_h, crop_w = crop.shape[:2]
    if crop_h == 0 or crop_w == 0:
        raise ValueError("empty crop region from FOV detection")

    scale = target_size / max(crop_h, crop_w)
    new_w = max(int(round(crop_w * scale)), 1)
    new_h = max(int(round(crop_h * scale)), 1)
    resized = cv2.resize(crop, (new_w, new_h), interpolation=cv2.INTER_AREA)

    canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    mask = np.zeros((target_size, target_size), dtype=np.float32)
    y_off = (target_size - new_h) // 2
    x_off = (target_size - new_w) // 2
    canvas[y_off:y_off + new_h, x_off:x_off + new_w] = resized
    mask[y_off:y_off + new_h, x_off:x_off + new_w] = 1.0

    transform = FovTransform(
        bbox=(left, upper, right, lower),
        scale=scale,
        x_off=x_off,
        y_off=y_off,
        new_w=new_w,
        new_h=new_h,
        target_size=target_size,
    )
    return canvas, mask, transform


def render_gaussian_heatmap(
    cx: float,
    cy: float,
    size: int,
    sigma: float,
) -> np.ndarray:
    """Render a normalized 2D-Gaussian target heatmap.

    The peak is centered on ``(cx, cy)`` in heatmap-grid pixels. The map is
    L1-normalized to sum to 1 (a probability map), matching the DSNT
    convention used by the decoder and loss.

    Args:
        cx: Gaussian center x in heatmap-grid pixels.
        cy: Gaussian center y in heatmap-grid pixels.
        size: Heatmap side length (square grid).
        sigma: Gaussian standard deviation in heatmap-grid pixels.

    Returns:
        float32 array ``(size, size)`` summing to 1 (0 if center is far
        off-grid and no mass lands in range).
    """
    ys, xs = np.mgrid[0:size, 0:size].astype(np.float32)
    d2 = (xs - cx) ** 2 + (ys - cy) ** 2
    g = np.exp(-d2 / (2.0 * sigma * sigma)).astype(np.float32)
    total = float(g.sum())
    if total > 0:
        g /= total
    return g
