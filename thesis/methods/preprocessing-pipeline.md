# Preprocessing Pipeline Specification

## Design Principle

The preprocessing pipeline is defined as an integral component of the diagnostic model — Stage 1 of a two-stage system: `model = preprocessing + CNN`. This is the central design decision of this work: preprocessing is not ancillary data preparation but defines the feature space available to the CNN. The pipeline standardizes retinal image appearance across devices, illumination conditions, and noise levels while preserving diagnostically relevant features.

---

## V5 Pipeline Stages (8-Stage V5 Pipeline — Canonical)

### Stage 0 — Canonical Flip (always on)

- Horizontal flip for left-eye images → right-eye canonical orientation (OD right, macula left)
- Eye laterality determined from image metadata or heuristic detection
- Implementation: `canonical_orientation.py`, `canonical_flip.py`

### Stage 1 — OD-Fovea Rotation Normalization (always on)

- Classical CV: bright-region percentile thresholding for OD detection; darkest region with distance prior from OD for fovea detection
- Rotate image so OD→fovea axis is horizontal
- Fallback: skip rotation on low confidence (fallback rotation σ = 13.0°)
- Augmentation rotation σ is adaptive per-image from OD/fovea detection uncertainty
- Implementation: `od_fovea_detect.py`, `canonical_orientation.py`

### Stage 2 — FOV Crop + Isotropic Resize (always on)

- PIL-based foreground detection (NOT Hough circle)
- Crop to FOV region; isotropic scale to 512×512 with centered zero-padding
- Preserves fundus circle geometry
- Implementation: `crop_resize.py`

### Stage 3 — FOV Mask Generation (always on)

- Binary mask: 1.0 = real fundus data, 0.0 = zero-padding
- Appended as 4th input channel
- Generated during Stage 2 (implicit — returned alongside resized image from crop_resize module)

### Stage 4 — Flat-Field Correction (always on)

- `corrected = image − GaussianBlur(image, σ) + 128`
- Adaptive σ = 0.07 × D (D = FOV diameter in pixels, derived from Stage 3 mask)
- Applied inside FOV mask only
- Implementation: `flat_field.py`

### Stage 5 — Upgraded CLAHE (always on)

- LAB L-channel processing; dual-constraint clip limit
- `CL = min(clip_factor × tile_area / 256, global_threshold × tile_area)`
- Default parameters: clip_factor = 2.0, global_threshold = 0.01, tile_grid = (8, 8)
- Stochastic at train time (p = 0.8); deterministic at inference
- Implementation: `upgraded_clahe.py`

### Stage 6 — Augmentation (train only)

- Unified affine: rotation (σ adaptive from Stage 1 detection uncertainty), zoom [0.9, 1.1], shear, stretch
- Brightness/contrast jitter
- PCA color jitter (Krizhevsky-style, σ = 0.1)
- Horizontal re-flip for augmentation diversity (no vertical flip)
- Applied before Stage 7 (operates on uint8 images)
- Implementation: `augmentation_v4.py`

### Stage 7 — Dataset-Specific Normalization (always on, always last)

- ToTensor: HWC uint8 → CHW float32 [0, 1]
- Channel-wise: `(x − mean) / std` using mean and std computed from EyePACS training set after Stages 0–4
- Only mask = 1.0 pixels used for stats computation (D-2 design decision)
- FOV mask appended as 4th channel
- Output: float32 tensor of shape (4, 512, 512)
- Implementation: `imagenet_normalize.py` (handles both ImageNet and dataset-specific normalization modes)

---

## V5 Pipeline Active/Absent Definition

- **Pipeline ACTIVE (full V5):** All 8 stages applied. Stage 6 active during training only. Output: 4-channel tensor (3 RGB + 1 FOV mask).
- **Pipeline ABSENT (V5 baseline):** Stretch-resize to 512×512 + ImageNet normalize (mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]). Output: 3-channel tensor. No FOV mask. No preprocessing stages applied.

---

## Assertion

The preprocessing pipeline, as specified above, constitutes a deterministic, reproducible, and order-dependent transformation of raw fundus images into a standardized feature space. The pipeline is an integral component of the diagnostic model, not an external data preparation step.
