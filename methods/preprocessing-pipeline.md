# Preprocessing Pipeline Specification

## Design Principle

The preprocessing pipeline is defined as an integral component of the diagnostic model — Stage 1 of a two-stage system: `model = preprocessing + CNN`. This is the central design decision of this work: preprocessing is not ancillary data preparation but defines the feature space available to the CNN. The pipeline standardizes retinal image appearance across devices, illumination conditions, and noise levels while preserving diagnostically relevant features.

---

## V4 Pipeline Stages (6-Stage V4 Pipeline — Canonical)

The V4 pipeline comprises six ordered stages. All toggleable stages must be applied in the specified order for the pipeline to be considered **ACTIVE** (full V4). The pipeline is considered **ABSENT** (V4 baseline) when images are passed to the CNN with crop + resize + ImageNet normalize only (Stages 1 + 4).

### Stage 0 — Canonical Flip (toggleable)
- **Operation:** Left→right eye orientation normalization; flip image horizontally if the image is identified as a left-eye fundus image to produce a canonical right-eye orientation
- **Purpose:** Ensure consistent retinal orientation across bilateral image pairs; reduces orientation-induced distribution shift in training data
- **Output:** Canonically oriented fundus image (right-eye orientation)
- **V4 Status:** NEW in V4

### Stage 1 — PIL-based FOV Crop and Resize (always on)
- **Operation:** Foreground detection via PIL thresholding; black border removal; image centering; resize to 512×512 pixels
- **Purpose:** Remove non-retinal background; standardize the field of view across images from different devices and acquisition protocols
- **Output:** 512×512 pixel image with centered fundus
- **V4 Status:** Replaces V3 Hough circle detection with PIL-based foreground detection

### Stage 2 — Flat-Field Correction (toggleable)
- **Operation:** Gaussian blur subtraction with σ=45 to estimate and remove illumination gradient; corrects uneven illumination across the fundus image
- **Purpose:** Normalize illumination gradients that arise from different lighting conditions, camera designs, and acquisition angles; reduces device-specific illumination artifacts
- **Output:** Illumination-corrected image with uniform background
- **V4 Status:** NEW in V4; replaces V3 HSV contrast enhancement

### Stage 3 — Upgraded CLAHE (toggleable)
- **Operation:** Contrast-Limited Adaptive Histogram Equalization applied in LAB color space (L-channel) with dual-constraint clip limit
- **Configuration:**
  - Color space: LAB (L-channel processing)
  - Tile grid size: 8×8
  - Clip limit: Dual-constraint — clip_factor × tile_area/256, capped by global_threshold × tile_area
  - Train-time stochastic application: 80% probability (deterministic at inference)
  - Modified formulation reference: CL = T/80 (theoretical reference from LC-AlTimemy-2021; independently validated per DGL-5)
- **Purpose:** Enhance local contrast to improve visibility of small lesion features (microaneurysms, small hemorrhages) while controlling over-enhancement artifacts via dual-constraint clip limit control
- **Output:** Contrast-enhanced image
- **V4 Status:** UPGRADED from V3 dynamic clip limit to dual-constraint stochastic formulation

### Stage 4 — ImageNet Channel-wise Normalization (always on, always last)
- **Operation:** Channel-wise normalization: (x − mean)/std → tensor, using ImageNet statistics (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- **Purpose:** Normalize pixel intensity distributions to match the ImageNet distribution expected by pre-trained CNN backbone weights; convert to PyTorch tensor
- **Output:** Normalized tensor ready for CNN input
- **V4 Status:** Replaces V3 pixel normalization [0,1]

### Stage 5 — Integrated Augmentation (train only, inserted before Stage 4)
- **Operation:** Unified affine transformation (rotation + zoom + stretch + shear) + brightness/contrast adjustment + PCA color jitter
- **Purpose:** Expand effective training set diversity while preserving diagnostic features; model-specific presets ("resnet": full augmentation; "efficientnet": reduced augmentation)
- **Output:** Augmented image (applied stochastically at train time; identity transform at inference)
- **V4 Status:** NEW in V4; augmentation is INTEGRATED into the pipeline (not a separate layer as in V3)

---

## V4 Pipeline Active/Absent Definition

- **Pipeline ACTIVE (full V4):** All toggleable stages (0, 2, 3, 5) applied in specified order, combined with always-on stages (1, 4).
- **Pipeline ABSENT (V4 baseline):** Images processed with crop + resize + ImageNet normalize only (Stages 1 + 4). This is the V4 baseline for H-1 comparison.

---

## V3 Historical Pipeline (5-Component — for Exp 2 Ablation Reference)

The V3 pipeline is retained for Experiment 2 component-level ablation analysis (historical comparison). The V3 pipeline comprised 5 components implemented as 6 stages:

| Governance Component (V3) | Operation |
|---|---|
| 1. FOV Standardization | Hough circle detection + border removal + centering + resize to 512×512 |
| 2. CLAHE Enhancement | LAB color space (L-channel), dynamic clip limit |
| 3. HSV Contrast Enhancement | Additional contrast in HSV color space (V-channel) |
| 4. Green Channel Imaging | Extract green channel from RGB (highest vessel contrast) |
| 5. Normalization | Pixel intensity [0,1] range |

V3 augmentation (flip, rotate ±15°, zoom ±10%, brightness) was kept as a **separate** training-time layer, not integrated into the pipeline.

V3 baseline: "resize only" (FOV standardization without subsequent components).

---

## Upgraded CLAHE Modifications (V4)

The V4 CLAHE implementation differs from the V3 formulation in the following ways:

1. **LAB color space processing (retained from V3):** CLAHE is applied to the L-channel in LAB color space, preserving color information integrity
2. **Dual-constraint clip limit (NEW in V4):** CL_tile = min(clip_factor × tile_area/256, global_threshold × tile_area). Two-parameter constraint provides better control over local and global enhancement bounds than the single dynamic parameter of V3.
3. **Stochastic train-time application (NEW in V4):** CLAHE is applied with 80% probability during training (deterministic at inference), providing implicit data augmentation and regularization.
4. **Tile-based adaptive processing (retained):** 8×8 tile grid provides local contrast enhancement adapted to regional image characteristics

---

## Augmentation Integration (V4)

In V4, augmentation (Stage 5) is **integrated** into the preprocessing pipeline as the final stage before ImageNet normalization (Stage 4). Augmentation is applied at train time only (stochastic); at inference time, Stage 5 is an identity transform. This differs from V3 where augmentation was kept as a separate data augmentation layer.

The integration of augmentation into the pipeline (rather than applying it as a separate layer) enables end-to-end pipeline configuration management via a single pipeline object, supports model-specific augmentation presets, and allows per-patient binocular blending to be coordinated with augmentation state (configs E, F).

---

## Assertion

The preprocessing pipeline, as specified above, constitutes a deterministic, reproducible, and order-dependent transformation of raw fundus images into a standardized feature space. The pipeline is an integral component of the diagnostic model, not an external data preparation step.
