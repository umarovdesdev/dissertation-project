# Claude Code Prompt: OD–Fovea Distance Prior + Binary Fallback

**Context:** This is a surgical addition to the existing V4 preprocessing pipeline in `dr-classifier`. Read `CLAUDE.md` and `IMPLEMENTATION_PLAN_OD_FOVEA_v2.md` first for full project context.

**Scope:** We are implementing a MINIMAL version of OD–fovea alignment — only the distance prior filter and binary fallback. We are NOT implementing composite confidence scoring, vessel suppression, TTA weighting, or structure constraints. These were evaluated and rejected as adding instability without sufficient value.

---

## What We Are Building

Two features, both minimal:

### Feature 1: OD–Fovea Detection with Distance Prior (Stage 0b)

Detect OD and fovea centers via classical CV. Apply ONE sanity check: the anatomical distance prior. If it fails → mark as low confidence and skip rotation.

### Feature 2: Binary Fallback in Augmentation (Stage 5)

If OD–fovea detection succeeded → use adaptive σ_θ for rotation augmentation.  
If OD–fovea detection failed → use fixed fallback σ=13.0° (existing default).

No gradients of confidence. No weighted scores. Binary: confident or not.

---

## Implementation Steps

### Step 1: Create `src/preprocessing/od_fovea_detect.py`

```python
"""
OD–Fovea detection via classical CV with anatomical distance prior.

Detection method:
- OD: brightest region in green channel (Gaussian blur σ=15, 
  97th percentile threshold, morphological cleanup, centroid via moments)
- Fovea: darkest region in annular search zone around OD
  (Gaussian blur σ=25 for vessel suppression, 
  search zone: 1.5–3.5 OD diameters from OD center)

Confidence is BINARY (not a score):
- confident=True: OD found, fovea found, distance in [1.5D, 3.5D]
- confident=False: anything else → skip rotation, use fallback σ

Returns ODFoveaResult dataclass with all fields needed downstream.
"""

import numpy as np
import cv2
from dataclasses import dataclass
from typing import Optional


@dataclass
class ODFoveaResult:
    """Result of OD–fovea detection."""
    confident: bool                    # Binary: True if detection passed all checks
    theta: float                       # Rotation angle in degrees (0.0 if not confident)
    sigma_theta: float                 # Adaptive σ for augmentation (fallback if not confident)
    od_center: Optional[tuple] = None  # (x, y) or None
    fovea_center: Optional[tuple] = None  # (x, y) or None
    od_radius: float = 0.0            # Detected OD radius in pixels
    fovea_radius: float = 0.0         # Detected fovea radius in pixels
    distance: float = 0.0             # OD–fovea distance in pixels


# Constants
FALLBACK_SIGMA = 13.0          # Fixed fallback σ (degrees), matches existing config default
SIGMA_CAP = 15.0               # Max adaptive σ (degrees)
OD_BLUR_SIGMA = 15             # Gaussian blur σ for OD detection
FOVEA_BLUR_SIGMA = 25          # Gaussian blur σ for fovea detection (vessel suppression)
OD_PERCENTILE = 97             # Brightness percentile for OD thresholding
DISTANCE_MIN_FACTOR = 1.5      # Minimum OD–fovea distance as multiple of OD diameter
DISTANCE_MAX_FACTOR = 3.5      # Maximum OD–fovea distance as multiple of OD diameter


def detect_od_fovea(
    image: np.ndarray,
    fallback_sigma: float = FALLBACK_SIGMA,
    sigma_cap: float = SIGMA_CAP,
) -> ODFoveaResult:
    """
    Detect optic disc and fovea, compute rotation angle and adaptive σ.
    
    Args:
        image: RGB uint8 image (after canonical flip + crop/resize, before flat-field).
               Expected shape: (H, W, 3).
        fallback_sigma: σ to use when detection fails (degrees).
        sigma_cap: Maximum allowed adaptive σ (degrees).
    
    Returns:
        ODFoveaResult with confident=True/False and appropriate theta/sigma_theta.
    
    Algorithm:
        1. Extract green channel (best vessel/OD contrast in fundus images)
        2. Detect OD: blur → threshold at 97th percentile → morphological cleanup → 
           largest contour → centroid + equivalent radius
        3. Detect fovea: heavy blur (σ=25, suppresses vessels) → 
           create annular mask (1.5–3.5 OD diameters from OD) →
           find minimum intensity point → centroid + equivalent radius
        4. Distance prior check: d must be in [1.5 * OD_diameter, 3.5 * OD_diameter]
        5. If all checks pass: compute theta = arctan2(dy, dx), 
           sigma_theta = arctan(sqrt(r_od² + r_f²) / d), cap at sigma_cap
        6. If any check fails: return confident=False, theta=0, sigma=fallback_sigma
    """
    h, w = image.shape[:2]
    
    # --- Step 1: Green channel extraction ---
    green = image[:, :, 1]  # RGB format, green channel index 1
    
    # --- Step 2: OD detection (brightest region) ---
    od_result = _detect_od(green, h, w)
    if od_result is None:
        return ODFoveaResult(confident=False, theta=0.0, sigma_theta=fallback_sigma)
    
    od_x, od_y, od_r = od_result
    od_diameter = 2 * od_r
    
    # Sanity: OD radius should be reasonable (between 2% and 15% of image dimension)
    min_r = 0.02 * min(h, w)
    max_r = 0.15 * min(h, w)
    if not (min_r < od_r < max_r):
        return ODFoveaResult(
            confident=False, theta=0.0, sigma_theta=fallback_sigma,
            od_center=(od_x, od_y), od_radius=od_r
        )
    
    # --- Step 3: Fovea detection (darkest region in annular zone) ---
    fovea_result = _detect_fovea(green, od_x, od_y, od_diameter, h, w)
    if fovea_result is None:
        return ODFoveaResult(
            confident=False, theta=0.0, sigma_theta=fallback_sigma,
            od_center=(od_x, od_y), od_radius=od_r
        )
    
    fovea_x, fovea_y, fovea_r = fovea_result
    
    # --- Step 4: Distance prior check ---
    d = np.sqrt((fovea_x - od_x) ** 2 + (fovea_y - od_y) ** 2)
    
    if not (DISTANCE_MIN_FACTOR * od_diameter < d < DISTANCE_MAX_FACTOR * od_diameter):
        return ODFoveaResult(
            confident=False, theta=0.0, sigma_theta=fallback_sigma,
            od_center=(od_x, od_y), fovea_center=(fovea_x, fovea_y),
            od_radius=od_r, fovea_radius=fovea_r, distance=d
        )
    
    # --- Step 5: Compute rotation angle and adaptive σ ---
    theta_rad = np.arctan2(fovea_y - od_y, fovea_x - od_x)
    theta_deg = np.degrees(theta_rad)
    
    sigma_pos = np.sqrt(od_r ** 2 + fovea_r ** 2)
    sigma_theta_rad = np.arctan(sigma_pos / d)
    sigma_theta_deg = np.degrees(sigma_theta_rad)
    sigma_theta_deg = min(sigma_theta_deg, sigma_cap)
    
    return ODFoveaResult(
        confident=True,
        theta=theta_deg,
        sigma_theta=sigma_theta_deg,
        od_center=(od_x, od_y),
        fovea_center=(fovea_x, fovea_y),
        od_radius=od_r,
        fovea_radius=fovea_r,
        distance=d,
    )


def _detect_od(
    green: np.ndarray, h: int, w: int
) -> Optional[tuple]:
    """
    Detect optic disc as brightest region in green channel.
    
    Returns (center_x, center_y, equivalent_radius) or None if detection fails.
    """
    blurred = cv2.GaussianBlur(green, (0, 0), OD_BLUR_SIGMA)
    
    # Threshold at 97th percentile
    threshold = np.percentile(blurred, OD_PERCENTILE)
    _, binary = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
    
    # Morphological cleanup: close small gaps, then open to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # Find contours, take largest
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    
    largest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest)
    if area < 100:  # Too small to be OD
        return None
    
    # Centroid via moments
    M = cv2.moments(largest)
    if M["m00"] == 0:
        return None
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    
    # Equivalent radius from area
    radius = np.sqrt(area / np.pi)
    
    return (cx, cy, radius)


def _detect_fovea(
    green: np.ndarray, od_x: int, od_y: int, od_diameter: float, h: int, w: int
) -> Optional[tuple]:
    """
    Detect fovea as darkest region in annular zone around OD.
    
    Heavy Gaussian blur (σ=25) suppresses vessels (dark and narrow → blur erases them).
    Search zone: annular region 1.5–3.5 OD diameters from OD center.
    
    Returns (center_x, center_y, equivalent_radius) or None if detection fails.
    """
    # Heavy blur to suppress vessels
    blurred = cv2.GaussianBlur(green, (0, 0), FOVEA_BLUR_SIGMA)
    
    # Create annular mask: ring from 1.5D to 3.5D centered on OD
    Y, X = np.ogrid[:h, :w]
    dist_from_od = np.sqrt((X - od_x) ** 2 + (Y - od_y) ** 2)
    
    inner_r = DISTANCE_MIN_FACTOR * od_diameter
    outer_r = DISTANCE_MAX_FACTOR * od_diameter
    annular_mask = (dist_from_od >= inner_r) & (dist_from_od <= outer_r)
    
    # Also exclude area too close to image border (10% margin)
    margin = int(0.1 * min(h, w))
    border_mask = np.zeros((h, w), dtype=bool)
    border_mask[margin:h-margin, margin:w-margin] = True
    
    search_mask = annular_mask & border_mask
    
    if not np.any(search_mask):
        return None
    
    # Find darkest region: set non-search areas to 255, then find minimum
    search_image = blurred.copy()
    search_image[~search_mask] = 255
    
    # Find minimum location
    min_val, _, min_loc, _ = cv2.minMaxLoc(search_image)
    fovea_x, fovea_y = min_loc  # cv2 returns (x, y)
    
    # Estimate fovea radius: threshold around minimum, find connected region
    # Use a local threshold: pixels within 10% of the min value in the search zone
    local_threshold = min_val + 0.10 * (np.mean(blurred[search_mask]) - min_val)
    fovea_binary = (blurred < local_threshold) & search_mask
    fovea_binary = fovea_binary.astype(np.uint8) * 255
    
    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    fovea_binary = cv2.morphologyEx(fovea_binary, cv2.MORPH_CLOSE, kernel)
    fovea_binary = cv2.morphologyEx(fovea_binary, cv2.MORPH_OPEN, kernel)
    
    contours, _ = cv2.findContours(fovea_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        # Fallback: use a nominal fovea radius (typically ~0.5 OD radius)
        return (fovea_x, fovea_y, od_diameter * 0.25)
    
    # Find contour containing the minimum point
    best_contour = None
    for c in contours:
        if cv2.pointPolygonTest(c, (fovea_x, fovea_y), False) >= 0:
            best_contour = c
            break
    
    if best_contour is None:
        # Use largest contour as fallback
        best_contour = max(contours, key=cv2.contourArea)
    
    area = cv2.contourArea(best_contour)
    radius = np.sqrt(area / np.pi) if area > 0 else od_diameter * 0.25
    
    # Refine center using contour moments if possible
    M = cv2.moments(best_contour)
    if M["m00"] > 0:
        fovea_x = int(M["m10"] / M["m00"])
        fovea_y = int(M["m01"] / M["m00"])
    
    return (fovea_x, fovea_y, radius)
```

**Verification:** `python -c "from src.preprocessing.od_fovea_detect import detect_od_fovea, ODFoveaResult; print('OK')"` from repo root.

---

### Step 2: Add config fields to `src/preprocessing/config.py`

Add THREE new fields to `PreprocessingV4Config` dataclass:

```python
# OD-Fovea alignment (Stage 0b)
use_od_fovea_rotation: bool = False       # Toggle OD-fovea rotation normalization
adaptive_rotation_sigma: bool = False     # Use per-image adaptive σ instead of fixed
fallback_rotation_sigma: float = 13.0     # σ when detection fails or feature disabled
```

**CRITICAL:** Defaults are `False` to preserve reproducibility of already-completed experiments (configs A, B, C). The feature is opt-in.

**Verification:** `python -c "from src.preprocessing.config import PreprocessingV4Config; c = PreprocessingV4Config(); print(c.use_od_fovea_rotation, c.adaptive_rotation_sigma, c.fallback_rotation_sigma)"` should print `False False 13.0`.

---

### Step 3: Rename `canonical_flip.py` → `canonical_orientation.py`

1. Copy `src/preprocessing/canonical_flip.py` to `src/preprocessing/canonical_orientation.py`
2. In the new file, keep ALL existing functions (`detect_eye_side`, `canonical_flip`)
3. Add a NEW function `canonical_orientation()` that calls canonical_flip AND optionally calls OD-fovea rotation:

```python
def canonical_orientation(
    image: np.ndarray,
    eye_side: str = "unknown",
    use_od_fovea_rotation: bool = False,
    fallback_sigma: float = 13.0,
    sigma_cap: float = 15.0,
) -> tuple:
    """
    Stage 0: Full canonical orientation.
    
    Sub-step 0a: Canonical flip (existing).
    Sub-step 0b: OD-fovea rotation normalization (new, optional).
    
    Args:
        image: RGB uint8 image.
        eye_side: "left", "right", or "unknown".
        use_od_fovea_rotation: Whether to perform OD-fovea rotation.
        fallback_sigma: Fallback σ for augmentation when detection fails.
        sigma_cap: Maximum adaptive σ.
    
    Returns:
        (image, od_fovea_result) where od_fovea_result is ODFoveaResult or None.
        Image is flipped and optionally rotation-normalized.
    """
    from .od_fovea_detect import detect_od_fovea, ODFoveaResult
    
    # Sub-step 0a: canonical flip
    image = canonical_flip(image, eye_side)
    
    # Sub-step 0b: OD-fovea rotation (optional)
    od_fovea_result = None
    if use_od_fovea_rotation:
        od_fovea_result = detect_od_fovea(image, fallback_sigma, sigma_cap)
        if od_fovea_result.confident:
            # Rotate image so OD-fovea axis is horizontal
            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, od_fovea_result.theta, 1.0)
            image = cv2.warpAffine(
                image, M, (w, h),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REFLECT,
            )
    
    return image, od_fovea_result
```

4. Replace `canonical_flip.py` with a 2-line backward-compatibility shim:

```python
"""Backward compatibility shim. Use canonical_orientation instead."""
from .canonical_orientation import detect_eye_side, canonical_flip  # noqa: F401
```

**Verification:** `python -c "from src.preprocessing.canonical_flip import detect_eye_side, canonical_flip; print('shim OK')"` and `python -c "from src.preprocessing.canonical_orientation import canonical_orientation; print('OK')"`.

---

### Step 4: Update `pipeline_v4.py` — Stage 0

In `PreprocessingPipelineV4.__call__()`, replace the Stage 0 section.

**Find** the line (around line 131):
```python
image = canonical_flip(image, eye_side)
```

**Replace with:**
```python
image, self._last_od_fovea_result = canonical_orientation(
    image, eye_side,
    use_od_fovea_rotation=self.config.use_od_fovea_rotation,
    fallback_sigma=self.config.fallback_rotation_sigma,
)
```

Also update the import at the top of the file:
- **Remove:** `from .canonical_flip import canonical_flip, detect_eye_side`
- **Add:** `from .canonical_orientation import canonical_orientation, detect_eye_side`

Add instance variable in `__init__`:
```python
self._last_od_fovea_result = None
```

**Verification:** Instantiate pipeline with default config (all OD-fovea features disabled), process a dummy image. Should produce identical output to before.

---

### Step 5: Update `augmentation_v4.py` — Adaptive σ

Three surgical edits to `src/data/augmentation_v4.py`:

**Edit 5a — Add TYPE_CHECKING import block** (at top of file, after existing imports):

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.preprocessing.od_fovea_detect import ODFoveaResult
```

**Edit 5b — Update `__call__` signature** (around line 56):

Current: `def __call__(self, image: np.ndarray) -> np.ndarray:`

New: 
```python
def __call__(self, image: np.ndarray, od_fovea_result=None) -> np.ndarray:
```

Inside `__call__`, find where `_sample_affine_params` is called and pass `od_fovea_result` through:

Current: `params = self._sample_affine_params()`  
New: `params = self._sample_affine_params(od_fovea_result=od_fovea_result)`

**Edit 5c — Update `_sample_affine_params`** (around line 100):

Current: `def _sample_affine_params(self):`

New:
```python
def _sample_affine_params(self, od_fovea_result=None):
```

Find the rotation sampling line (around line 107) where `self.cfg.rotation_sigma` is used. Replace the rotation σ logic:

Current (approximately):
```python
rotation_sigma = self.cfg.rotation_sigma
```

New:
```python
# Rotation σ: 3-branch logic
if (
    od_fovea_result is not None 
    and self.cfg.adaptive_rotation_sigma 
    and od_fovea_result.confident
):
    # Branch 1: Adaptive σ from OD-fovea uncertainty
    rotation_sigma = od_fovea_result.sigma_theta
elif (
    od_fovea_result is not None 
    and self.cfg.adaptive_rotation_sigma 
    and not od_fovea_result.confident
):
    # Branch 2: Detection failed → fallback σ
    rotation_sigma = self.cfg.fallback_rotation_sigma
else:
    # Branch 3: Feature disabled → original fixed σ
    rotation_sigma = self.cfg.rotation_sigma
```

---

### Step 6: Update `pipeline_v4.py` — Pass ODFoveaResult to augmentation

In `PreprocessingPipelineV4.__call__()`, find the Stage 5 augmentation call (around line 153):

Current: `image = self._augmentation(image)`

New: `image = self._augmentation(image, od_fovea_result=self._last_od_fovea_result)`

---

### Step 7: Update `__init__.py` exports

In `src/preprocessing/__init__.py`, add:

```python
from .canonical_orientation import canonical_orientation, detect_eye_side, canonical_flip
from .od_fovea_detect import detect_od_fovea, ODFoveaResult
```

Remove or update the old `canonical_flip` import line to avoid conflicts.

---

### Step 8: Update `configs/default.yaml`

Add under the preprocessing section:

```yaml
# OD-Fovea alignment (Stage 0b) — disabled by default for reproducibility
use_od_fovea_rotation: false
adaptive_rotation_sigma: false
fallback_rotation_sigma: 13.0
```

---

### Step 9: Create visualization script `scripts/visualize_od_fovea.py`

Create a script that:
1. Takes a directory of fundus images as input
2. Runs `detect_od_fovea()` on each
3. Draws OD center (green circle), fovea center (red circle), OD→fovea axis (blue line), and annular search zone (dashed gray circles) on each image
4. Saves annotated images to an output directory
5. Prints a summary: total images, confident detections, failed detections, confidence rate

Usage: `python scripts/visualize_od_fovea.py --input_dir /path/to/images --output_dir /path/to/output --max_images 20`

This is the validation tool for Step 14 (visual inspection).

---

### Step 10: Create unit test `tests/test_od_fovea_detect.py`

Test cases:
1. **Synthetic test:** Create a 512×512 black image with a white circle (OD) and a dark circle (fovea) at known positions. Verify `detect_od_fovea` returns `confident=True` with theta and sigma close to expected values.
2. **Distance prior rejection:** Place OD and fovea too close together (< 1.5D). Verify `confident=False`.
3. **Distance prior rejection:** Place OD and fovea too far apart (> 3.5D). Verify `confident=False`.
4. **No bright region:** All-black image. Verify `confident=False`, `sigma_theta == fallback_sigma`.
5. **ODFoveaResult dataclass:** Verify all fields populated correctly.
6. **Fallback σ:** When `confident=False`, verify `sigma_theta` equals `fallback_sigma` parameter.

---

### Step 11: Update `CLAUDE.md`

Add to Stage 0 description:

```
Stage 0: Canonical Orientation (expanded from Canonical Flip in v4.1)
  0a. Canonical flip — left→right eye orientation (existing, toggleable)
  0b. OD–fovea rotation normalization — detect OD/fovea via classical CV, 
      rotate to horizontal axis (new, toggleable via use_od_fovea_rotation)
  Fallback: when detection confidence is low, rotation is skipped.
  
Stage 5: Augmentation — rotation σ can be:
  - Fixed (rotation_sigma from config, default 13°) — when adaptive disabled
  - Per-image adaptive (σ_θ from OD/fovea uncertainty) — when adaptive enabled
  - Fallback (fallback_rotation_sigma, default 13°) — when adaptive enabled but detection failed
```

---

## Execution Order

| # | Step | Files | Verification |
|---|------|-------|-------------|
| 1 | Create od_fovea_detect.py | NEW: `src/preprocessing/od_fovea_detect.py` | Import test |
| 2 | Add config fields | EDIT: `src/preprocessing/config.py` | Print defaults |
| 3 | Rename + create shim | NEW: `src/preprocessing/canonical_orientation.py`, EDIT: `src/preprocessing/canonical_flip.py` | Both import tests |
| 4 | Update pipeline Stage 0 | EDIT: `src/preprocessing/pipeline_v4.py` | Dummy image test |
| 5 | Update augmentation σ | EDIT: `src/data/augmentation_v4.py` | Import test |
| 6 | Pass result to augmentation | EDIT: `src/preprocessing/pipeline_v4.py` | Dummy image test |
| 7 | Update exports | EDIT: `src/preprocessing/__init__.py` | Import test |
| 8 | Update YAML config | EDIT: `configs/default.yaml` | Validate YAML loads |
| 9 | Create viz script | NEW: `scripts/visualize_od_fovea.py` | `--help` works |
| 10 | Create unit tests | NEW: `tests/test_od_fovea_detect.py` | `pytest tests/test_od_fovea_detect.py` passes |
| 11 | Update CLAUDE.md | EDIT: `CLAUDE.md` | Visual inspection |

**After all steps:** Run `python scripts/visualize_od_fovea.py` on 20 EyePACS images including some Grade 3–4. Inspect results visually.

---

## CRITICAL CONSTRAINTS

1. **All defaults are `False`/disabled.** Existing experiment configs A/B/C must produce IDENTICAL results. Zero behavioral change when features are off.
2. **No composite confidence scoring.** Confidence is BINARY: detection passed all sanity checks or it didn't.
3. **The only sanity check is the distance prior** (1.5D–3.5D) plus basic OD radius range check (2%–15% of image dimension). No vessel direction fields, no circularity scoring, no stability checks.
4. **No TTA weighting.** The dual confidence (geom × margin) system is NOT implemented. It goes in Chapter 5 "Future Work."
5. **No vessel suppression module.** The heavy Gaussian blur (σ=25) in fovea detection is sufficient. No separate vessel map computation.
6. **Backward compatibility:** `canonical_flip.py` becomes a shim. All existing imports from it continue to work.
7. **Test with `use_od_fovea_rotation=False` first** to confirm zero behavioral change. Then enable and test.
