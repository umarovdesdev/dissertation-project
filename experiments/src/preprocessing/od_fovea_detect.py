"""
Anatomical landmark detection for fundus images.

Detects Optic Disc (OD) and fovea centers. The production ``detect_od_fovea``
(Phase 2) delegates to a pre-trained, **frozen** heatmap-regression detector
(``src/preprocessing/od_fovea_net``); it FOV-crops internally, returns genuine
per-landmark confidence, and drives (a) Stage 1 rotation normalization,
(b) Stage 5 uncertainty-aware adaptive rotation augmentation, (c) the Stage 5
polar-CLAHE fovea pivot, and (d) the demo OD/fovea overlay.

``detect_od_fovea_classical`` and the ``_detect_*`` helpers retain the original
classical-CV implementation (brightest region = OD, darkest with distance prior
= fovea) for reference and tests; it is no longer on the live path.

All functions expect RGB uint8 NumPy arrays as input.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class ODFoveaResult:
    """
    Result of OD and fovea detection on a single fundus image.

    The first block is the original contract (unchanged). The fields after
    ``confident`` are **additive** (Phase 2): they carry the learned detector's
    genuine per-landmark confidence and optional probability heatmaps. They have
    defaults so the classical detector and cache-path ``SimpleNamespace`` stand-
    ins remain valid without setting them.

    Attributes:
        od_center: (x, y) pixel coordinates of optic disc center.
        od_radius: Estimated radius of optic disc in pixels.
        fovea_center: (x, y) pixel coordinates of fovea center.
        fovea_radius: Estimated radius of fovea in pixels.
        distance: Euclidean distance between OD and fovea centers in pixels.
        angle_rad: Angle of OD→fovea vector in radians (from arctan2).
        angle_deg: Same angle in degrees.
        rotation_sigma_deg: Per-image adaptive rotation σ in degrees,
            derived from localization uncertainty.
        confident: True if detection passed all sanity checks (classical) or
            both landmark confidences exceed the threshold (learned).
            When False, caller should skip rotation normalization, use default
            rotation_sigma, and pivot polar CLAHE on the FOV centroid.
        od_confidence: OD confidence in ``[0, 1]`` (learned detector; 1.0 from
            the classical detector, which has no genuine confidence).
        fovea_confidence: Fovea confidence in ``[0, 1]`` (learned; 1.0 classical).
        od_heatmap: float32 OD probability map resized to the input frame, or
            ``None`` (classical, or when heatmaps were not requested).
        fovea_heatmap: float32 fovea probability map, or ``None``.
    """

    od_center: tuple[int, int]
    od_radius: float
    fovea_center: tuple[int, int]
    fovea_radius: float
    distance: float
    angle_rad: float
    angle_deg: float
    rotation_sigma_deg: float
    confident: bool
    od_confidence: float = 1.0
    fovea_confidence: float = 1.0
    od_heatmap: np.ndarray | None = None
    fovea_heatmap: np.ndarray | None = None


def _detect_od_center(
    green: np.ndarray,
    blur_sigma: float = 15.0,
    percentile: float = 97.0,
) -> tuple[tuple[int, int], float]:
    """
    Detect optic disc center as the centroid of the brightest region.

    Uses heavy Gaussian blur to suppress specular reflections and vessel
    highlights, then thresholds at the given percentile to isolate the
    OD region.

    Args:
        green: Single-channel (green) uint8 array.
        blur_sigma: Gaussian σ for blur (suppresses noise/vessels).
        percentile: Intensity percentile for OD mask threshold.

    Returns:
        ((cx, cy), radius) — center coordinates and equivalent radius.
    """
    blurred = cv2.GaussianBlur(green, (0, 0), blur_sigma)
    threshold = np.percentile(blurred, percentile)
    od_mask = (blurred >= threshold).astype(np.uint8)

    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    od_mask = cv2.morphologyEx(od_mask, cv2.MORPH_CLOSE, kernel)
    od_mask = cv2.morphologyEx(od_mask, cv2.MORPH_OPEN, kernel)

    # Centroid via moments
    M = cv2.moments(od_mask)
    if M["m00"] == 0:
        # Fallback: just use argmax location
        _, _, _, max_loc = cv2.minMaxLoc(blurred)
        return max_loc, 30.0  # default radius estimate

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # Equivalent radius from mask area
    area = M["m00"]
    radius = math.sqrt(area / math.pi)

    return (cx, cy), radius


def _detect_fovea_center(
    green: np.ndarray,
    od_center: tuple[int, int],
    od_radius: float,
    blur_sigma: float = 25.0,
    inner_factor: float = 1.5,
    outer_factor: float = 3.5,
) -> tuple[tuple[int, int], float]:
    """
    Detect fovea center as the darkest region on the opposite side of OD.

    Search is constrained to an annular region around the OD center at
    a distance of inner_factor to outer_factor OD diameters.  Heavy blur
    suppresses dark vessels that could otherwise be mistaken for the fovea.

    Args:
        green: Single-channel (green) uint8 array.
        od_center: (x, y) of detected OD center.
        od_radius: Detected OD radius in pixels.
        blur_sigma: Gaussian σ for vessel suppression.
        inner_factor: Inner annulus boundary as multiple of OD diameter.
        outer_factor: Outer annulus boundary as multiple of OD diameter.

    Returns:
        ((cx, cy), radius) — fovea center coordinates and estimated radius.
    """
    h, w = green.shape
    od_diameter = od_radius * 2.0
    inner_r = inner_factor * od_diameter
    outer_r = outer_factor * od_diameter

    # Create annular search mask
    Y, X = np.ogrid[:h, :w]
    dist_from_od = np.sqrt((X - od_center[0]) ** 2 + (Y - od_center[1]) ** 2)
    annular_mask = ((dist_from_od >= inner_r) & (dist_from_od <= outer_r)).astype(np.uint8)

    # Exclude pixels outside the fundus FOV (black border)
    # Pixels with green channel < 15 are likely background
    fov_mask = (green > 15).astype(np.uint8)
    search_mask = annular_mask & fov_mask

    if search_mask.sum() == 0:
        # Fallback: use image center as fovea estimate
        return (w // 2, h // 2), max(od_radius * 0.5, 10.0)

    # Heavy blur to suppress vessels (dark and thin → blur eliminates them)
    heavily_blurred = cv2.GaussianBlur(green, (0, 0), blur_sigma)

    # Find darkest point in search region
    # Set non-search pixels to 255 so they are never the minimum
    search_image = heavily_blurred.copy()
    search_image[search_mask == 0] = 255

    _, _, min_loc, _ = cv2.minMaxLoc(search_image)
    fovea_center = min_loc  # (x, y) from minMaxLoc

    # Fovea radius is approximately 0.5× OD radius (anatomical prior)
    fovea_radius = max(od_radius * 0.5, 10.0)

    return fovea_center, fovea_radius


# Sanity-check constants
_MIN_DISTANCE_FACTOR = 1.0    # OD–fovea distance must be >= 1.0× OD diameter
_MAX_DISTANCE_FACTOR = 5.0    # OD–fovea distance must be <= 5.0× OD diameter
_MAX_ROTATION_SIGMA = 15.0    # Hard cap on adaptive σ (degrees)
_MIN_OD_RADIUS = 10.0         # Minimum credible OD radius (pixels)
_MAX_OD_RADIUS_FRACTION = 0.15  # OD radius must be < 15% of image width


def detect_od_fovea_classical(image_rgb: np.ndarray) -> ODFoveaResult:
    """
    Detect optic disc and fovea centers in a fundus image (classical CV).

    Uses classical CV: brightest region for OD, darkest region (with
    anatomical distance prior) for fovea.  Returns detection result
    including per-image rotation angle and adaptive augmentation σ.

    Detection confidence is set to False if any sanity check fails:
    - OD radius too small or too large
    - OD–fovea distance outside anatomical range
    - OD or fovea center outside image bounds

    When confidence is False, the caller should:
    - Skip deterministic rotation normalization (Stage 0b)
    - Use default rotation_sigma instead of adaptive σ (Stage 5)

    Args:
        image_rgb: RGB uint8 NumPy array of shape (H, W, 3).

    Returns:
        ODFoveaResult with all detection outputs and confidence flag.
    """
    h, w = image_rgb.shape[:2]
    green = image_rgb[:, :, 1]  # Green channel — best contrast

    # Step 1: Detect OD
    od_center, od_radius = _detect_od_center(green)

    # Step 2: Detect fovea
    fovea_center, fovea_radius = _detect_fovea_center(
        green, od_center, od_radius
    )

    # Step 3: Compute geometry
    dx = fovea_center[0] - od_center[0]
    dy = fovea_center[1] - od_center[1]
    distance = math.sqrt(dx * dx + dy * dy)
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    # Step 4: Compute adaptive rotation σ
    #   σ_pos = sqrt(r_od² + r_fovea²)    (independent localization errors)
    #   σ_θ   = arctan(σ_pos / d)          (angular uncertainty)
    sigma_pos = math.sqrt(od_radius ** 2 + fovea_radius ** 2)
    if distance > 0:
        rotation_sigma_deg = math.degrees(math.atan(sigma_pos / distance))
    else:
        rotation_sigma_deg = _MAX_ROTATION_SIGMA

    # Cap σ at maximum
    rotation_sigma_deg = min(rotation_sigma_deg, _MAX_ROTATION_SIGMA)

    # Step 5: Sanity checks
    confident = True
    od_diameter = od_radius * 2.0

    # Check OD radius bounds
    if od_radius < _MIN_OD_RADIUS:
        confident = False
    if od_radius > _MAX_OD_RADIUS_FRACTION * w:
        confident = False

    # Check distance bounds (anatomical: fovea is 2–4 OD diameters from OD)
    if od_diameter > 0:
        distance_ratio = distance / od_diameter
        if distance_ratio < _MIN_DISTANCE_FACTOR:
            confident = False
        if distance_ratio > _MAX_DISTANCE_FACTOR:
            confident = False
    else:
        confident = False

    # Check centers are within image
    margin = 10
    if not (margin <= od_center[0] < w - margin and margin <= od_center[1] < h - margin):
        confident = False
    if not (margin <= fovea_center[0] < w - margin and margin <= fovea_center[1] < h - margin):
        confident = False

    return ODFoveaResult(
        od_center=od_center,
        od_radius=od_radius,
        fovea_center=fovea_center,
        fovea_radius=fovea_radius,
        distance=distance,
        angle_rad=angle_rad,
        angle_deg=angle_deg,
        rotation_sigma_deg=rotation_sigma_deg,
        confident=confident,
    )


def detect_od_fovea(
    image_rgb: np.ndarray,
    return_heatmaps: bool = False,
) -> ODFoveaResult:
    """
    Detect optic disc and fovea centers in a fundus image (learned detector).

    This is the production facade (Phase 2). It delegates to the pre-trained,
    **frozen** heatmap-regression detector (``src/preprocessing/od_fovea_net``),
    which internally FOV-crops the image to a 512² frame before inference — so
    detection runs on the FOV-cropped frame (eliminating the dark-vignette
    failure of the classical detector) — then maps coordinates back to
    input-image pixels. The signature is unchanged from the classical detector
    (``return_heatmaps`` is an additive keyword with a default), so callers
    (``canonical_orientation``, the demo server, ``validate_od_fovea_idrid.py``)
    need no changes.

    Unlike the classical detector, ``confident`` is a **genuine** gate: it is
    True only when both landmark confidences (derived from heatmap peak
    sharpness and spatial spread) exceed the configured threshold. When False,
    the caller should skip rotation normalization and pivot polar CLAHE on the
    FOV centroid.

    The detector is pre-trained and frozen relative to the DR classifier; this
    call performs inference only.

    Args:
        image_rgb: RGB uint8 NumPy array of shape (H, W, 3), arbitrary
            resolution. FOV-cropping is performed internally.
        return_heatmaps: If True, attach OD/fovea probability heatmaps resized
            to the input frame (for the demo overlay). Default False for the
            pipeline path (skips two full-resolution resizes).

    Returns:
        ODFoveaResult with coordinates in **input-image pixels** plus the
        additive confidence/heatmap fields.
    """
    # Lazy import: the learned detector pulls in torch/timm, which the classical
    # path (and torch-free callers) must not require at module import time.
    from .od_fovea_net import detect_od_fovea as _net_detect

    res = _net_detect(image_rgb, return_heatmaps=return_heatmaps)
    return ODFoveaResult(
        od_center=res.od_center,
        od_radius=res.od_radius,
        fovea_center=res.fovea_center,
        fovea_radius=res.fovea_radius,
        distance=res.distance,
        angle_rad=res.angle_rad,
        angle_deg=res.angle_deg,
        rotation_sigma_deg=res.rotation_sigma_deg,
        confident=res.confident,
        od_confidence=res.od_confidence,
        fovea_confidence=res.fovea_confidence,
        od_heatmap=res.od_heatmap,
        fovea_heatmap=res.fovea_heatmap,
    )


def rotate_to_horizontal(
    image: np.ndarray,
    angle_deg: float,
    center: tuple[int, int] | None = None,
) -> np.ndarray:
    """
    Rotate image so that the OD–fovea axis becomes horizontal.

    Rotation center defaults to the image center.  Uses BORDER_REFLECT
    to avoid introducing black pixels at the edges.

    Args:
        image: RGB uint8 NumPy array of shape (H, W, 3).
        angle_deg: Angle to correct (from ODFoveaResult.angle_deg).
            Image is rotated by -angle_deg to bring axis to 0°.
        center: Optional rotation center.  Defaults to image center.

    Returns:
        Rotated RGB uint8 NumPy array of same shape.
    """
    h, w = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT,
    )
    return rotated
