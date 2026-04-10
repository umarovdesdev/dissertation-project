# V5 Data Processing Pipeline — Comprehensive Specification

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification  
**Candidate:** Yesmukhamedov N.S.  
**Pipeline Version:** 5.0  
**Binding Reference:** INVARIANTS.md v5.0, RESEARCH_ARCHITECTURE.md v5.0

---

## 1. Introduction

The proposed diagnostic model is defined as a two-stage system:

$$
\text{model} = \text{preprocessing} + \text{CNN}
$$

The preprocessing pipeline is not an ancillary data preparation step — it is an integral model component that defines the feature space available to the CNN classifier. The pipeline standardizes retinal image appearance across imaging devices, illumination conditions, and acquisition protocols while preserving diagnostically relevant microvascular features.

The V5 pipeline comprises **eight ordered stages** (Stages 0–7). All stages are **always-on** except Stage 6 (augmentation, train-only). The pipeline processes raw fundus photographs into 4-channel CNN-ready tensors (3 RGB channels + 1 FOV mask channel).

---

## 2. Pipeline Overview

### 2.1 Stage Execution Order

| Stage | Name | Mode | Domain | Output |
|-------|------|------|--------|--------|
| 0 | Canonical Flip | always on | RGB uint8 → RGB uint8 | Right-eye orientation |
| 1 | OD-Fovea Rotation Normalization | always on | RGB uint8 → RGB uint8 | Horizontal retinal axis |
| 2 | FOV Crop + Isotropic Resize + Zero-Padding | always on | RGB uint8 → RGB uint8 | 512×512 centered fundus |
| 3 | FOV Mask Generation | always on | RGB uint8 → float32 mask | Binary 1.0/0.0 mask |
| 4 | Flat-Field Correction | always on | RGB uint8 → RGB uint8 | Uniform illumination |
| 5 | CLAHE (LAB L-channel) | always on | RGB uint8 → RGB uint8 | Enhanced local contrast |
| 6 | Augmentation | train only | RGB uint8 → RGB uint8 | Augmented training image |
| 7 | Dataset-Specific Normalize + Mask Append | always on | RGB uint8 + mask → float32 tensor | CNN-ready (4, H, W) |

Stage 6 (augmentation) is inserted **before** Stage 7 (normalization) because augmentation operates on uint8 pixel values. Stage 7 is always the final transformation, converting to a normalized float32 tensor.

### 2.2 Pipeline Configurations

| Configuration | Stages Active | Input Channels | Role |
|---------------|---------------|----------------|------|
| **Baseline (Exp 1 A/C)** | Stretch-resize + ImageNet normalize | 3 (RGB only) | Control condition for H-1 |
| **Full V5 (Exp 1 B/D)** | 0–7 (all) | 4 (RGB + FOV mask) | Experimental condition for H-1 |
| **Ablation levels (Exp 2)** | Incremental subsets | 4 | Component contribution |

### 2.3 Global Variable Definitions

| Variable | Type | Dimensions | Description |
|----------|------|-----------|-------------|
| $I$ | uint8 ndarray | H×W×3 | Input RGB fundus image |
| $M$ | float32 ndarray | H×W | FOV binary mask (1.0 = fundus, 0.0 = padding) |
| $T$ | float32 tensor | 4×512×512 | CNN-ready output (RGB + FOV mask) |
| $D$ | float | scalar | FOV diameter in pixels |
| $\sigma$ | float | scalar | Flat-field Gaussian sigma = 0.07·D |

---

## 3. Stage Specifications

### Stage 0: Canonical Flip

**Purpose:** Normalize eye laterality so all images have optic disc on the right side (right-eye convention).

**Operation:**
- Detect laterality from metadata (left/right eye label)
- If left eye: apply horizontal mirror flip
- If right eye or unknown: no operation

**Output:** RGB uint8 image, same dimensions as input, right-eye orientation.

---

### Stage 1: OD-Fovea Rotation Normalization

**Purpose:** Align the optic disc–fovea axis to horizontal, removing rotational variation between acquisitions.

**Operation:**
- Detect optic disc (OD) center via classical CV (bright-region percentile thresholding (top percentile of green-channel intensity))
- Detect fovea center (darkest region in the macula zone)
- Compute angle θ between OD-fovea vector and horizontal axis
- Rotate image by −θ to align axis to horizontal

**Output:** RGB uint8 image, same dimensions, horizontally aligned retinal axis.

---

### Stage 2: FOV Crop + Isotropic Resize + Zero-Padding

**Purpose:** Remove non-retinal border artifacts, standardize to 512×512 while preserving fundus circle geometry via isotropic scaling and zero-padding.

**Operation:**
1. Detect FOV region using PIL-based foreground detection (brightness threshold above background)
2. Crop to bounding box with margin: [cy−R−m : cy+R+m, cx−R−m : cx+R+m]
3. Scale isotropically so that 2R maps to 512 pixels (preserving aspect ratio)
4. Zero-pad to exactly 512×512 (centered)

**Contrast with baseline:** Baseline uses direct stretch-resize (non-isotropic), distorting fundus geometry. V5 isotropic resize preserves the circular fundus shape.

**Output:** RGB uint8 image, exactly 512×512 pixels.

---

### Stage 3: FOV Mask Generation

**Purpose:** Generate a binary spatial mask separating real fundus pixels from zero-padded background, appended as the 4th input channel.

**Operation:**
- Threshold on padded pixels: M[i,j] = 1.0 if pixel (i,j) is within FOV circle, else 0.0
- Optionally smooth mask boundary with small Gaussian to soften edge

**Output:** float32 mask, 512×512, values ∈ {0.0, 1.0}.

---

### Stage 4: Adaptive Flat-Field Correction

**Purpose:** Remove uneven illumination (vignetting, lighting gradients) while preserving local contrast variations caused by pathology.

**Operation:**
- Estimate low-frequency illumination field: $B = \text{GaussianBlur}(I, \sigma=0.07 \cdot D)$
- Subtract background: $I' = I - B + 128$
- Clip to valid range [0, 255]

**Key parameter:** σ = 0.07·D, where D is the FOV diameter. Adaptive to image geometry — larger FOV images use a wider blur kernel, smaller FOV images use a narrower kernel. This is the primary V5 improvement over V4 (which used fixed σ=45).

**Output:** RGB uint8 image, 512×512.

---

### Stage 5: Upgraded CLAHE (Dual-Constraint, LAB L-channel)

**Purpose:** Enhance local contrast to improve microvascular feature visibility (microaneurysms, hemorrhages, exudates) without introducing global over-enhancement artifacts.

**Operation:**
1. Convert RGB → LAB color space
2. Apply dual-constraint CLAHE to L-channel only:
   - $\text{CL\_tile} = \min(\text{clip\_factor} \times \text{tile\_area}/256,\; \text{global\_threshold} \times \text{tile\_area})$
   - Default: clip_factor=2.0, global_threshold=0.01, tile_grid=(8,8)
3. At training time: apply stochastically (p=0.8); at inference: always apply
4. Convert LAB → RGB

**Output:** RGB uint8 image, 512×512.

---

### Stage 6: Augmentation (Train Only)

**Purpose:** Increase training data variability, reduce overfitting, mitigate class imbalance effects.

**Operation (unified affine + color):**
- Unified affine transform: rotation (σ adaptive from Stage 1 OD-fovea confidence, fallback σ=13.0°, clipped ±40°), zoom [0.9, 1.1], optional shear (±2°, p=0.3), optional stretch ([1/1.05, 1.05])
- Brightness/contrast jitter (α ∈ [0.9, 1.1], β ∈ [−10, 10], p=0.5)
- PCA color jitter (Krizhevsky-style, σ=0.1, p=0.5)
- Horizontal re-flip for augmentation diversity (no vertical flip)

Applied only during training. At inference: no augmentation (deterministic pipeline).

**Output:** RGB uint8 image, 512×512.

---

### Stage 7: Dataset-Specific Normalize + FOV Mask Append

**Purpose:** Normalize pixel values using dataset-specific statistics (mean/std computed from training set) and append the FOV mask as the 4th input channel.

**Operation:**
1. Convert RGB uint8 → float32, scale to [0, 1]
2. Normalize per channel: $(x - \mu_c) / \sigma_c$ using training-set statistics
3. Append FOV mask M as channel 4: tensor shape (4, 512, 512)

**V5 vs baseline:** Baseline uses ImageNet statistics (μ=[0.485, 0.456, 0.406], σ=[0.229, 0.224, 0.225]) for 3-channel input. V5 uses dataset-specific statistics for 4-channel input.

**Output:** float32 tensor, shape (4, 512, 512), CNN-ready.

---

## 4. CLAHE Parameter Sweep (Experiment 2)

Experiment 2 performs a systematic sweep over CLAHE parameters to validate H-2 (CLAHE Threshold Sensitivity):

| Parameter | Range | Step |
|-----------|-------|------|
| clip_factor | 1.0 – 4.0 | 0.5 |
| global_threshold | 0.01 – 0.05 | 0.01 |

Sweep is performed on EyePACS per-class F1 (DR Grades 1 and 2 as primary targets). Results reported as 2D sensitivity surface heatmap.

---

## 5. Ablation Levels (Experiment 2)

V5 ablation tests 7 incremental configurations:

| Level | Configuration | Channels |
|-------|--------------|----------|
| 0 | Baseline (stretch-resize + ImageNet norm) | 3 |
| 1 | Baseline + canonical flip (Stage 0) | 3 |
| 2 | + OD-fovea rotation (Stage 1) | 3 |
| 3 | + Isotropic resize (Stage 2 → Stage 3 → Stage 7) | 4 |
| 4 | + Flat-field correction (Stage 4) | 4 |
| 5 | + CLAHE (Stage 5) | 4 |
| 6 | Full V5 (all stages incl. augmentation Stage 6) | 4 |

---

## 6. Flat-Field σ Sweep (Experiment 2)

Sweep over flat-field correction sigma multiplier to validate adaptive parameter selection:

| Parameter | Range | Step |
|-----------|-------|------|
| σ multiplier (× D) | 0.05 – 0.10 | 0.01 |

Fixed at σ=0.07·D for the canonical V5 pipeline.

---

*End of V5 Pipeline Specification — Version 5.0*
