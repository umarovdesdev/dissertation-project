"""Image quality metrics for preprocessing pipeline analysis (§3.3).

Metrics:
  CNR   — Contrast-to-Noise Ratio (vessel vs background)
  Entropy — Shannon entropy (information content)
  SSIM  — Structural Similarity (preservation vs original)
"""

from __future__ import annotations

import cv2
import numpy as np
from skimage.metrics import structural_similarity


def compute_cnr(image: np.ndarray) -> float:
    """Compute Contrast-to-Noise Ratio between vessel and background regions.

    Uses the green channel (best vessel contrast in retinal images) and
    Otsu thresholding to separate vessel from background pixels.

    CNR = |mean_vessel - mean_background| / std_background

    Args:
        image: BGR or single-channel uint8 or float32 image.

    Returns:
        CNR scalar. Higher is better.
    """
    # Extract green channel (index 1 in BGR)
    if image.ndim == 3:
        green = image[:, :, 1]
    else:
        green = image

    # Normalise to uint8 for Otsu
    if green.dtype != np.uint8:
        g8 = (np.clip(green, 0, 1) * 255).astype(np.uint8)
    else:
        g8 = green

    _, mask = cv2.threshold(g8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    vessel_pixels = g8[mask > 0].astype(np.float64)
    bg_pixels     = g8[mask == 0].astype(np.float64)

    if len(vessel_pixels) == 0 or len(bg_pixels) == 0:
        return 0.0

    std_bg = float(np.std(bg_pixels))
    if std_bg < 1e-8:
        return 0.0

    return float(abs(np.mean(vessel_pixels) - np.mean(bg_pixels)) / std_bg)


def compute_entropy(image: np.ndarray) -> float:
    """Compute Shannon entropy of the image intensity histogram.

    H = -sum(p * log2(p)) over histogram bins (zero-probability bins skipped).

    Args:
        image: Any-channel image (uint8 or float32). Converted to grayscale
               if multichannel.

    Returns:
        Entropy in bits. Higher means more information content.
    """
    if image.ndim == 3:
        gray = cv2.cvtColor(
            (image * 255).astype(np.uint8) if image.dtype != np.uint8 else image,
            cv2.COLOR_BGR2GRAY,
        )
    else:
        gray = image

    if gray.dtype != np.uint8:
        gray = (np.clip(gray, 0, 1) * 255).astype(np.uint8)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).ravel()
    prob = hist / (hist.sum() + 1e-12)
    prob = prob[prob > 0]
    return float(-np.sum(prob * np.log2(prob)))


def compute_ssim(original: np.ndarray, processed: np.ndarray) -> float:
    """Compute Structural Similarity Index between original and processed images.

    Measures how much structural information is preserved after preprocessing.
    Both images are converted to grayscale uint8 and resized to the same
    resolution if they differ.

    Args:
        original: Reference image (BGR uint8 or float32).
        processed: Processed image (BGR uint8 or float32).

    Returns:
        SSIM in [-1, 1]. Values near 1 indicate high structural preservation.
    """
    def _to_gray_u8(img: np.ndarray) -> np.ndarray:
        if img.dtype != np.uint8:
            img = (np.clip(img, 0, 1) * 255).astype(np.uint8)
        if img.ndim == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    g_orig = _to_gray_u8(original)
    g_proc = _to_gray_u8(processed)

    # Resize processed to match original if sizes differ
    if g_orig.shape != g_proc.shape:
        g_proc = cv2.resize(g_proc, (g_orig.shape[1], g_orig.shape[0]),
                            interpolation=cv2.INTER_LINEAR)

    score, _ = structural_similarity(g_orig, g_proc, full=True)
    return float(score)


def compute_all_quality_metrics(
    image: np.ndarray,
    original: np.ndarray | None = None,
) -> dict[str, float | None]:
    """Compute all image quality metrics for one image.

    Args:
        image: Processed image (BGR uint8 or float32).
        original: Optional reference image for SSIM computation.
                  If None, ssim is returned as None.

    Returns:
        Dict with keys: cnr, entropy, ssim (float or None).
    """
    return {
        "cnr":     compute_cnr(image),
        "entropy": compute_entropy(image),
        "ssim":    compute_ssim(original, image) if original is not None else None,
    }
