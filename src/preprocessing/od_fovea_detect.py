"""
Anatomical landmark detection for fundus images.

Detects Optic Disc (OD) and fovea centers using classical computer vision
(no learned models).  Used by Stage 0b for deterministic rotation normalization
and by Stage 5 for uncertainty-aware adaptive rotation augmentation.

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
        confident: True if detection passed all sanity checks.
            When False, caller should skip rotation normalization
            and use default rotation_sigma.
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


def detect_od_fovea(image_rgb: np.ndarray) -> ODFoveaResult:
    """
    Detect optic disc and fovea centers in a fundus image.

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
