# Implementation Plan: OD–Fovea Geometric Normalization + Uncertainty-Aware Rotation

**Project:** dr-classifier  
**Author:** Yesmukhamedov N.S. (plan by Claude Opus, execution by Claude Code)  
**Date:** 2026-03-25  
**Scope:** Two features integrated into V4 preprocessing pipeline  
**Branch:** `feature/od-fovea-alignment`

---

## Overview

Two related features that extend Stage 0 (Canonical Orientation) and Stage 5 (Augmentation):

1. **Stage 0b — Deterministic OD–Fovea Rotation Normalization (preprocessing)**  
   Detect optic disc and fovea centers, compute the angle of the OD→fovea axis, rotate the image to make this axis horizontal. Applied identically at train and inference time.

2. **Stage 5 upgrade — Uncertainty-Aware Adaptive Rotation σ (augmentation)**  
   Replace the fixed `rotation_sigma=13.0` with a per-image adaptive σ derived from localization uncertainty of OD/fovea detection radii. Applied only at train time.

Both features preserve the existing 6-stage pipeline structure (no new stages added).

---

## Prerequisites

Before starting, ensure you have:
- The `dr-classifier` repo checked out on the `main` branch
- Read `~/CLAUDE.md` for project context
- The conda `dr-classifier` environment activated
- Access to EyePACS images at `/mnt/d/datasets/EyePACS/` for testing

**Files you will modify:**
- `src/preprocessing/canonical_flip.py` → rename to `src/preprocessing/canonical_orientation.py`
- `src/preprocessing/pipeline_v4.py`
- `src/preprocessing/config.py`
- `src/preprocessing/__init__.py`
- `src/data/augmentation_v4.py`
- `configs/default.yaml`
- `configs/smoke_test_1pct.yaml`

**Files you will create:**
- `src/preprocessing/od_fovea_detect.py` (NEW)
- `tests/test_od_fovea_detect.py` (NEW)
- `scripts/visualize_od_fovea.py` (NEW — diagnostic visualization)

---

## STAGE 1: Create OD/Fovea Detection Module

**File:** `src/preprocessing/od_fovea_detect.py`

Create this file with ALL of the following content as a single module.

### 1.1 Module docstring, imports, and dataclass

```python
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
```

### 1.2 OD detection (private)

```python
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
```

### 1.3 Fovea detection (private)

```python
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
```

### 1.4 Sanity-check constants and main detection function

```python
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
```

### 1.5 Rotation utility

```python
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
```

---

## STAGE 2: Rename and Extend Canonical Orientation Module

### 2.1 Rename file

```bash
git mv src/preprocessing/canonical_flip.py src/preprocessing/canonical_orientation.py
```

### 2.2 Create backward-compatibility shim

Create a NEW file `src/preprocessing/canonical_flip.py` containing only:

```python
"""Backward-compatibility shim.  Real code lives in canonical_orientation.py."""
from .canonical_orientation import detect_eye_side, canonical_flip  # noqa: F401
```

### 2.3 Add `canonical_orientation()` to `canonical_orientation.py`

Keep ALL existing code (`detect_eye_side`, `canonical_flip`, the `_FILENAME_ENCODED` constant, all imports) unchanged.

**Add** the following imports at the top (after existing imports):

```python
from .od_fovea_detect import ODFoveaResult, detect_od_fovea, rotate_to_horizontal
```

**Append** the following function at the end of the file:

```python
def canonical_orientation(
    image: np.ndarray,
    eye_side: str = "unknown",
    enable_rotation: bool = True,
) -> tuple[np.ndarray, ODFoveaResult | None]:
    """
    Apply full canonical orientation: flip + OD–fovea rotation.

    Sub-step 0a: Canonical flip (left→right eye, existing logic).
    Sub-step 0b: OD–fovea rotation normalization (new).

    When *enable_rotation* is ``False`` or detection confidence is low,
    only the flip is applied and ``ODFoveaResult`` is returned with
    ``confident=False`` (or ``None``).

    Args:
        image: RGB uint8 NumPy array of shape ``(H, W, 3)``.
        eye_side: ``"left"``, ``"right"``, or ``"unknown"``.
        enable_rotation: If ``False``, skip OD–fovea rotation entirely.

    Returns:
        Tuple of ``(processed_image, od_fovea_result)``.
        *od_fovea_result* is ``None`` when *enable_rotation* is ``False``.
        ``od_fovea_result.confident`` may be ``False`` if detection failed.
    """
    # Sub-step 0a: canonical flip (existing)
    image = canonical_flip(image, eye_side)

    # Sub-step 0b: OD–fovea rotation normalization (new)
    if not enable_rotation:
        return image, None

    result = detect_od_fovea(image)

    if result.confident:
        image = rotate_to_horizontal(image, result.angle_deg)

    return image, result
```

---

## STAGE 3: Update PreprocessingV4Config

**File:** `src/preprocessing/config.py`

### 3.1 Add new toggle field

In the `# --- Toggles ---` section, add ONE new line immediately after `use_canonical_flip`:

```python
    use_canonical_flip: bool = True
    use_od_fovea_rotation: bool = True      # NEW: Stage 0b rotation normalization
```

### 3.2 Add new parameter fields

Add a new section AFTER the `# --- Stage 4: Normalise ---` block and BEFORE the `from_dict` method:

```python
    # --- Stage 0b: OD-Fovea Rotation Detection ---
    od_blur_sigma: float = 15.0
    od_percentile: float = 97.0
    fovea_blur_sigma: float = 25.0
    fovea_inner_factor: float = 1.5
    fovea_outer_factor: float = 3.5
    adaptive_rotation_sigma: bool = True
    fallback_rotation_sigma: float = 13.0
```

### 3.3 Update presets

Add to BOTH presets in `PIPELINE_PRESETS`:

```python
    "resnet": {
        # ... existing fields unchanged ...
        "use_od_fovea_rotation": True,
        "adaptive_rotation_sigma": True,
    },
    "efficientnet": {
        # ... existing fields unchanged ...
        "use_od_fovea_rotation": True,
        "adaptive_rotation_sigma": True,
    },
```

### 3.4 Update docstring

Add to the `PreprocessingV4Config` class docstring, in the Args section:

```
        use_od_fovea_rotation: Enable Stage 0b OD–fovea axis rotation normalization.
        od_blur_sigma: Gaussian σ for OD detection blur.
        od_percentile: Intensity percentile for OD mask threshold.
        fovea_blur_sigma: Gaussian σ for fovea detection blur.
        fovea_inner_factor: Inner annulus boundary as multiple of OD diameter.
        fovea_outer_factor: Outer annulus boundary as multiple of OD diameter.
        adaptive_rotation_sigma: Use per-image adaptive σ (from OD/fovea uncertainty)
            instead of fixed rotation_sigma for augmentation.
        fallback_rotation_sigma: Rotation σ used when adaptive detection fails
            or adaptive_rotation_sigma is False.
```

---

## STAGE 4: Update Pipeline V4 Orchestrator

**File:** `src/preprocessing/pipeline_v4.py`

### 4.1 Update imports

Replace the current import:

```python
from .canonical_flip import canonical_flip
```

With:

```python
from .canonical_orientation import canonical_flip, canonical_orientation
from .od_fovea_detect import ODFoveaResult
```

### 4.2 Modify `__call__` method — Stage 0

Find this block in `__call__`:

```python
        # Stage 0: canonical flip
        if self.config.use_canonical_flip:
            image = canonical_flip(image, eye_side)
```

Replace with:

```python
        # Stage 0: canonical orientation (flip + OD–fovea rotation)
        od_fovea_result: ODFoveaResult | None = None
        if self.config.use_canonical_flip or self.config.use_od_fovea_rotation:
            image, od_fovea_result = canonical_orientation(
                image,
                eye_side=eye_side if self.config.use_canonical_flip else "unknown",
                enable_rotation=self.config.use_od_fovea_rotation,
            )
```

### 4.3 Modify `__call__` method — Stage 5

Find this block in `__call__`:

```python
        # Stage 5: augmentation (train only, uint8, before normalize)
        if self.is_training:
            image = self._augmentation(image)
```

Replace with:

```python
        # Stage 5: augmentation (train only, uint8, before normalize)
        if self.is_training:
            image = self._augmentation(image, od_fovea_result=od_fovea_result)
```

### 4.4 No other changes to pipeline_v4.py

Do NOT modify `__init__`, factory methods, `is_active`, `is_absent`, or any other method.

---

## STAGE 5: Update Augmentation V4

**File:** `src/data/augmentation_v4.py`

This is the most surgery-sensitive edit.  Three precise changes only.

### 5.1 Add import (top of file)

Add after the existing imports:

```python
from __future__ import annotations   # MOVE TO VERY TOP if not already there

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.preprocessing.od_fovea_detect import ODFoveaResult
```

NOTE: `from __future__ import annotations` MUST be the very first import in the file (before `import cv2`).  If it is already present, do not duplicate it.  The file already has it — confirmed.  So only add the `TYPE_CHECKING` block.

### 5.2 Modify `__call__` signature and body

Current code (lines ~63–92):

```python
    def __call__(self, image: np.ndarray) -> np.ndarray:
        """
        Apply the full V4 augmentation pipeline to one image.

        Application order:
        1. Unified affine (rotation + zoom + stretch + shear)
        2. Brightness / contrast
        3. PCA colour jitter

        Args:
            image: RGB uint8 NumPy array of shape ``(H, W, 3)``.

        Returns:
            Augmented RGB uint8 NumPy array of the same shape.
        """
        h, w = image.shape[:2]
        center = (w / 2.0, h / 2.0)

        # 1. Unified affine
        params = self._sample_affine_params()
```

Replace with:

```python
    def __call__(
        self,
        image: np.ndarray,
        od_fovea_result: ODFoveaResult | None = None,
    ) -> np.ndarray:
        """
        Apply the full V4 augmentation pipeline to one image.

        Application order:
        1. Unified affine (rotation + zoom + stretch + shear)
        2. Brightness / contrast
        3. PCA colour jitter

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
```

Everything else in `__call__` after this line remains UNCHANGED.

### 5.3 Modify `_sample_affine_params` — signature and rotation σ

Current code (lines ~96–132):

```python
    def _sample_affine_params(self) -> dict[str, float]:
        """
        Sample affine transform parameters.

        Returns:
            Dict with keys ``theta`` (°), ``sx``, ``sy``, ``shear_rad`` (rad).
        """
        cfg = self.config

        # Rotation: truncated Gaussian σ=rotation_sigma, clipped at ±rotation_clip
        theta = float(np.random.normal(0.0, cfg.rotation_sigma))
        theta = float(np.clip(theta, -cfg.rotation_clip, cfg.rotation_clip))
```

Replace with:

```python
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
```

Everything after `theta = float(np.clip(...))` in this method remains UNCHANGED (zoom, stretch, shear logic is untouched).

### 5.4 Summary of changes to augmentation_v4.py

Only THREE locations are modified:
1. Add `TYPE_CHECKING` import block (after existing imports)
2. `__call__` — add `od_fovea_result` parameter, pass it to `_sample_affine_params`
3. `_sample_affine_params` — add `od_fovea_result` parameter, replace first 2 lines of rotation sampling with adaptive/fallback logic

**NOTHING ELSE changes.** Do not touch: `_build_affine_matrix`, `_sample_interpolation`, `_apply_affine`, `_apply_pca_color`, `_apply_brightness_contrast`, or the `__init__` method.

---

## STAGE 6: Update `__init__.py` Exports

**File:** `src/preprocessing/__init__.py`

### 6.1 Replace canonical_flip import

Find:

```python
from .canonical_flip import detect_eye_side, canonical_flip
```

Replace with:

```python
from .canonical_orientation import detect_eye_side, canonical_flip, canonical_orientation
```

### 6.2 Add new imports

Add after the V4 import block:

```python
from .od_fovea_detect import ODFoveaResult, detect_od_fovea, rotate_to_horizontal
```

### 6.3 Update `__all__`

Add to the V4 section of `__all__`:

```python
    "canonical_orientation",
    "ODFoveaResult",
    "detect_od_fovea",
    "rotate_to_horizontal",
```

---

## STAGE 7: Update Config Files

### 7.1 `configs/default.yaml`

In the `preprocessing_v4:` section, add after `use_canonical_flip: true`:

```yaml
  use_od_fovea_rotation: true
```

Add a new sub-section (anywhere in `preprocessing_v4:`, recommend after the Stage 3 CLAHE block):

```yaml
  # Stage 0b — OD-Fovea Rotation Detection
  od_blur_sigma: 15.0
  od_percentile: 97.0
  fovea_blur_sigma: 25.0
  fovea_inner_factor: 1.5
  fovea_outer_factor: 3.5
  adaptive_rotation_sigma: true
  fallback_rotation_sigma: 13.0
```

### 7.2 `configs/smoke_test_1pct.yaml`

Add the identical block as in default.yaml.  Place after `use_canonical_flip: true`:

```yaml
  use_od_fovea_rotation: true
```

And the parameter block:

```yaml
  od_blur_sigma: 15.0
  od_percentile: 97.0
  fovea_blur_sigma: 25.0
  fovea_inner_factor: 1.5
  fovea_outer_factor: 3.5
  adaptive_rotation_sigma: true
  fallback_rotation_sigma: 13.0
```

---

## STAGE 8: Create Diagnostic Visualization Script

**File:** `scripts/visualize_od_fovea.py`

```python
"""
Visualize OD/fovea detection on sample fundus images.

Usage:
    python scripts/visualize_od_fovea.py --input /path/to/image.jpeg --output viz_output.png
    python scripts/visualize_od_fovea.py --input /mnt/d/datasets/EyePACS/train/ --output viz_dir/ --n 20
"""

import argparse
import pathlib
import random
import sys

import cv2
import numpy as np

# Allow imports from project root
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from src.preprocessing.od_fovea_detect import detect_od_fovea, rotate_to_horizontal


def visualize_single(image_path: pathlib.Path, output_path: pathlib.Path) -> None:
    """Draw detection result on a single image and save."""
    bgr = cv2.imread(str(image_path))
    if bgr is None:
        print(f"Cannot read: {image_path}")
        return
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    result = detect_od_fovea(rgb)

    # Draw on BGR copy for cv2.imwrite
    viz = bgr.copy()

    # OD: green circle + center dot
    cv2.circle(viz, result.od_center, int(result.od_radius), (0, 255, 0), 2)
    cv2.circle(viz, result.od_center, 3, (0, 255, 0), -1)

    # Fovea: red circle + center dot
    cv2.circle(viz, result.fovea_center, int(result.fovea_radius), (0, 0, 255), 2)
    cv2.circle(viz, result.fovea_center, 3, (0, 0, 255), -1)

    # OD→fovea line (blue)
    cv2.line(viz, result.od_center, result.fovea_center, (255, 0, 0), 2)

    # Text info
    info = (
        f"angle={result.angle_deg:.1f} "
        f"sigma={result.rotation_sigma_deg:.1f} "
        f"conf={'Y' if result.confident else 'N'}"
    )
    cv2.putText(viz, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Side-by-side: original with annotations + rotated
    if result.confident:
        rotated_rgb = rotate_to_horizontal(rgb, result.angle_deg)
        rotated_bgr = cv2.cvtColor(rotated_rgb, cv2.COLOR_RGB2BGR)
    else:
        rotated_bgr = bgr.copy()
        cv2.putText(
            rotated_bgr, "SKIP (low confidence)", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
        )

    # Resize both to same height for concatenation
    target_h = 512
    scale = target_h / viz.shape[0]
    viz_resized = cv2.resize(viz, None, fx=scale, fy=scale)
    rot_resized = cv2.resize(rotated_bgr, None, fx=scale, fy=scale)
    combined = np.hstack([viz_resized, rot_resized])

    cv2.imwrite(str(output_path), combined)
    print(
        f"Saved: {output_path}  "
        f"(confident={result.confident}, "
        f"angle={result.angle_deg:.1f}deg, "
        f"sigma={result.rotation_sigma_deg:.1f}deg)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize OD/fovea detection")
    parser.add_argument("--input", required=True, help="Image file or directory")
    parser.add_argument("--output", required=True, help="Output file or directory")
    parser.add_argument(
        "--n", type=int, default=20,
        help="Number of images to sample (if input is directory)",
    )
    args = parser.parse_args()

    inp = pathlib.Path(args.input)
    out = pathlib.Path(args.output)

    if inp.is_file():
        visualize_single(inp, out)
    elif inp.is_dir():
        out.mkdir(parents=True, exist_ok=True)
        images = (
            list(inp.glob("*.jpeg"))
            + list(inp.glob("*.jpg"))
            + list(inp.glob("*.png"))
        )
        sample = random.sample(images, min(args.n, len(images)))
        for img_path in sample:
            visualize_single(img_path, out / f"viz_{img_path.stem}.png")
    else:
        print(f"Input not found: {inp}")


if __name__ == "__main__":
    main()
```

---

## STAGE 9: Create Unit Tests

**File:** `tests/test_od_fovea_detect.py`

```python
"""Unit tests for OD/fovea detection module."""

import math

import cv2
import numpy as np
import pytest

from src.preprocessing.od_fovea_detect import (
    ODFoveaResult,
    detect_od_fovea,
    rotate_to_horizontal,
    _detect_od_center,
    _detect_fovea_center,
)


def _make_synthetic_fundus(
    size: int = 512,
    od_pos: tuple[int, int] = (350, 256),
    fovea_pos: tuple[int, int] = (180, 256),
    od_brightness: int = 220,
    fovea_darkness: int = 80,
    bg_level: int = 150,
) -> np.ndarray:
    """Create a synthetic fundus-like image for testing."""
    image = np.full((size, size, 3), bg_level, dtype=np.uint8)

    # Draw FOV circle (slightly brighter than pure bg to mimic retina)
    cv2.circle(
        image, (size // 2, size // 2), size // 2 - 10,
        (bg_level, bg_level, bg_level), -1,
    )

    # Draw OD (bright disc)
    cv2.circle(image, od_pos, 40, (od_brightness,) * 3, -1)

    # Draw fovea (dark region)
    cv2.circle(image, fovea_pos, 20, (fovea_darkness,) * 3, -1)

    # Add some Gaussian noise for realism
    rng = np.random.RandomState(42)
    noise = rng.normal(0, 5, image.shape).astype(np.float32)
    image = np.clip(image.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    return image


class TestODDetection:
    """Tests for OD center detection."""

    def test_finds_bright_region(self):
        image = _make_synthetic_fundus(od_pos=(350, 256))
        green = image[:, :, 1]
        center, radius = _detect_od_center(green)
        assert abs(center[0] - 350) < 20
        assert abs(center[1] - 256) < 20
        assert radius > 10

    def test_different_od_position(self):
        image = _make_synthetic_fundus(od_pos=(256, 150))
        green = image[:, :, 1]
        center, radius = _detect_od_center(green)
        assert abs(center[0] - 256) < 20
        assert abs(center[1] - 150) < 20


class TestFoveaDetection:
    """Tests for fovea center detection."""

    def test_finds_dark_region(self):
        image = _make_synthetic_fundus(od_pos=(350, 256), fovea_pos=(180, 256))
        green = image[:, :, 1]
        center, radius = _detect_fovea_center(green, (350, 256), 40.0)
        assert abs(center[0] - 180) < 30
        assert abs(center[1] - 256) < 30

    def test_fallback_when_no_annular_region(self):
        """When annular search mask is empty, returns image center."""
        green = np.full((100, 100), 128, dtype=np.uint8)
        center, radius = _detect_fovea_center(
            green, od_center=(50, 50), od_radius=1.0,
            inner_factor=100.0, outer_factor=200.0,  # impossible range
        )
        assert center == (50, 50)  # image center


class TestDetectODFovea:
    """Tests for the full detection pipeline."""

    def test_returns_valid_dataclass(self):
        image = _make_synthetic_fundus()
        result = detect_od_fovea(image)
        assert isinstance(result, ODFoveaResult)
        assert result.distance > 0
        assert result.rotation_sigma_deg > 0
        assert result.rotation_sigma_deg <= 15.0

    def test_horizontal_axis_angle_near_zero_or_180(self):
        image = _make_synthetic_fundus(od_pos=(350, 256), fovea_pos=(180, 256))
        result = detect_od_fovea(image)
        # OD right, fovea left → angle ≈ 180° (or ≈ -180°)
        assert abs(abs(result.angle_deg) - 180) < 20 or abs(result.angle_deg) < 20

    def test_tilted_axis_detected(self):
        image = _make_synthetic_fundus(od_pos=(350, 200), fovea_pos=(180, 310))
        result = detect_od_fovea(image)
        assert abs(result.angle_deg) > 5  # not horizontal

    def test_confidence_false_for_black_image(self):
        image = np.zeros((512, 512, 3), dtype=np.uint8)
        result = detect_od_fovea(image)
        assert result.confident is False

    def test_confidence_false_for_uniform_image(self):
        image = np.full((512, 512, 3), 128, dtype=np.uint8)
        result = detect_od_fovea(image)
        # Uniform image → OD and fovea detected at similar locations → distance too small
        assert result.confident is False

    def test_sigma_capped_at_maximum(self):
        image = _make_synthetic_fundus()
        result = detect_od_fovea(image)
        assert result.rotation_sigma_deg <= 15.0


class TestRotateToHorizontal:
    """Tests for rotation utility."""

    def test_zero_angle_is_identity(self):
        rng = np.random.RandomState(123)
        image = rng.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        rotated = rotate_to_horizontal(image, 0.0)
        np.testing.assert_array_equal(image, rotated)

    def test_preserves_shape(self):
        rng = np.random.RandomState(123)
        image = rng.randint(0, 255, (200, 300, 3), dtype=np.uint8)
        rotated = rotate_to_horizontal(image, 15.0)
        assert rotated.shape == image.shape

    def test_preserves_dtype(self):
        rng = np.random.RandomState(123)
        image = rng.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        rotated = rotate_to_horizontal(image, 10.0)
        assert rotated.dtype == np.uint8

    def test_180_rotation_flips(self):
        """Rotating 180° should roughly flip the image."""
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        image[10, 20] = 255  # single white pixel
        rotated = rotate_to_horizontal(image, 180.0)
        # After 180° rotation about center, (20,10) → roughly (79,89)
        assert rotated[10, 20, 0] == 0  # original pixel moved away
```

---

## STAGE 10: Update CLAUDE.md

In the `## V4 Preprocessing Pipeline (6-stage) — CANONICAL` section, replace the Stage 0 line:

```
Stage 0: Canonical flip (left→right eye orientation) — toggleable
```

With:

```
Stage 0: Canonical Orientation
  0a. Canonical flip (left→right eye orientation) — toggleable
  0b. OD-fovea rotation normalization (classical CV detection) — toggleable
      Detects OD (brightest region) and fovea (darkest region with distance prior)
      Rotates image so OD→fovea axis is horizontal
      When detection confidence is low, rotation is skipped (fallback)
```

And update the Stage 5 line to note adaptive σ:

```
Stage 5: Augmentation (unified affine + brightness/contrast + PCA color) — train only
  rotation_sigma: adaptive per-image (from OD/fovea uncertainty) or fallback 13.0°
```

Also add to the `## Project Structure` section:

```
src/preprocessing/od_fovea_detect.py  — V4 Stage 0b: OD/fovea detection (classical CV)
src/preprocessing/canonical_orientation.py — V4 Stage 0: canonical flip + OD-fovea rotation
src/preprocessing/canonical_flip.py   — backward-compat shim → canonical_orientation.py
```

---

## Execution Order for Claude Code

Execute stages in this exact order.  After each stage, run the verification command before proceeding.

| Step | Action | Verify |
|------|--------|--------|
| 1 | Create `src/preprocessing/od_fovea_detect.py` (STAGE 1) | `python -c "from src.preprocessing.od_fovea_detect import detect_od_fovea, ODFoveaResult; print('OK')"` |
| 2 | `git mv src/preprocessing/canonical_flip.py src/preprocessing/canonical_orientation.py` (STAGE 2.1) | `ls src/preprocessing/canonical_orientation.py` |
| 3 | Create backward-compat shim `src/preprocessing/canonical_flip.py` (STAGE 2.2) | `python -c "from src.preprocessing.canonical_flip import canonical_flip; print('shim OK')"` |
| 4 | Add import + `canonical_orientation()` to `canonical_orientation.py` (STAGE 2.3) | `python -c "from src.preprocessing.canonical_orientation import canonical_orientation; print('OK')"` |
| 5 | Update `config.py` — add fields + update presets + docstring (STAGE 3) | `python -c "from src.preprocessing.config import PreprocessingV4Config; c = PreprocessingV4Config(); print(f'rotation={c.use_od_fovea_rotation}, adaptive={c.adaptive_rotation_sigma}, fallback={c.fallback_rotation_sigma}')"` |
| 6 | Update `pipeline_v4.py` — imports + Stage 0 + Stage 5 (STAGE 4) | `python -c "from src.preprocessing.pipeline_v4 import PreprocessingPipelineV4; print('OK')"` |
| 7 | Update `augmentation_v4.py` — 3 surgical edits (STAGE 5) | `python -c "from src.data.augmentation_v4 import FundusAugmentationV4; print('OK')"` |
| 8 | Update `__init__.py` exports (STAGE 6) | `python -c "from src.preprocessing import canonical_orientation, detect_od_fovea, ODFoveaResult; print('OK')"` |
| 9 | Update YAML configs (STAGE 7) | `python -c "import yaml; c=yaml.safe_load(open('configs/default.yaml')); print(c['preprocessing_v4']['use_od_fovea_rotation'])"` |
| 10 | Create `scripts/visualize_od_fovea.py` (STAGE 8) | `python scripts/visualize_od_fovea.py --input /mnt/d/datasets/EyePACS/train/10_left.jpeg --output /tmp/test_viz.png` |
| 11 | Create `tests/test_od_fovea_detect.py` (STAGE 9) | `python -m pytest tests/test_od_fovea_detect.py -v` |
| 12 | Run smoke test (1% subset, config A = baseline, no OD rotation) | `python run_experiment.py --experiment exp1 --config configs/smoke_test_1pct.yaml --configs A` |
| 13 | Run smoke test (1% subset, config B = full pipeline, WITH OD rotation) | `python run_experiment.py --experiment exp1 --config configs/smoke_test_1pct.yaml --configs B` |
| 14 | Visual validation on 20 random images | `python scripts/visualize_od_fovea.py --input /mnt/d/datasets/EyePACS/train/ --output /tmp/od_fovea_viz/ --n 20` then inspect output images |
| 15 | Update CLAUDE.md (STAGE 10) | Visual inspection |

---

## Critical Notes for Claude Code

1. **`augmentation_v4.py` has EXACTLY 3 edit points.** (a) Add TYPE_CHECKING import block. (b) Add `od_fovea_result` param to `__call__` and pass to `_sample_affine_params`. (c) Add `od_fovea_result` param to `_sample_affine_params` and add 10-line rotation σ selection block replacing the 2-line fixed σ. Nothing else changes.

2. **The backward-compatibility shim for `canonical_flip.py` is essential.** The V3 pipeline, `__init__.py`, and experiments exp2–exp6 import `canonical_flip` by name. The 2-line shim file prevents import breakage.

3. **Detection runs on the FULL-SIZE image (before crop+resize).** The pipeline order guarantees this: Stage 0 (detection + rotation) → Stage 1 (crop + resize). OD/fovea detection is more reliable on the original resolution.

4. **When `confident=False`, two things happen:**
   - Stage 0b: rotation is SKIPPED (image passes through unchanged)
   - Stage 5: `fallback_rotation_sigma` (13.0°) is used instead of adaptive σ
   - This is NOT an error — it is expected behavior for ~5-10% of images

5. **This does NOT affect V3 pipeline.** `pipeline.py` (V3) is completely untouched. Only `pipeline_v4.py` is modified.

6. **Seed/reproducibility:** `detect_od_fovea()` is fully deterministic (no random operations). The stochastic element remains only in Stage 5 augmentation (`np.random.normal`), already controlled by the global seed.

7. **The `rotation_sigma` field in config still exists** and is still used by the affine matrix builder for the fixed-σ path (when adaptive is disabled). Do NOT remove it. The new `fallback_rotation_sigma` defaults to 13.0 — same value as the current `rotation_sigma`.

8. **Config backward compatibility:** `PreprocessingV4Config.from_dict()` handles missing keys gracefully (uses dataclass defaults). Old YAML configs without the new fields will still work — they will get `use_od_fovea_rotation=True` and `adaptive_rotation_sigma=True` by default. If this is undesirable for reproducibility of already-run experiments, set the defaults to `False` instead.

---

## Governance Notes

- **Pipeline stage count:** Still 6. Stage 0 is extended with a sub-step, not a new stage.
- **INVARIANTS compliance:** OD-3 (V4 pipeline definition) describes Stage 0 as "Canonical Flip." After implementation, update INVARIANTS.md §III OD-3 to read "Stage 0: Canonical Orientation — (a) horizontal flip for left-eye images; (b) OD–fovea axis rotation normalization via classical CV detection (toggleable, skipped when detection confidence is low)." This is a terminological update within VCR-5, not a structural change requiring VCR-1 re-ratification.
- **New contribution claims:** This adds two potential contributions:
  - **Method contribution:** Uncertainty-aware adaptive rotation augmentation derived from anatomical landmark localization uncertainty (σ_θ = arctan(√(r_od² + r_f²) / d))
  - **Engineering contribution:** Classical CV-based geometric normalization of fundus images via OD–fovea axis detection
- **Experiment impact:** The new features are toggleable. Experiment 1 configs B and D (full pipeline) will include them. Configs A and C (baseline) will not. This maintains the factorial design cleanly.
- **Default toggle concern:** New fields default to `True`. For already-completed experiment configs (A, B, C), this means re-running them would produce different results. **Decision needed:** either (a) set defaults to `False` and explicitly enable in configs, or (b) accept that new runs incorporate the feature. Recommendation: set `use_od_fovea_rotation: false` and `adaptive_rotation_sigma: false` as defaults, and explicitly enable in the "full pipeline" configs (B, D, E, F). This preserves reproducibility of baseline configs.
