# Preprocessing Pipeline Specification

## Design Principle

The preprocessing pipeline is defined as an integral component of the diagnostic model — Stage 1 of a two-stage system: `model = preprocessing + CNN`. This is the central design decision of this work: preprocessing is not ancillary data preparation but defines the feature space available to the CNN. The pipeline standardizes retinal image appearance across devices, illumination conditions, and noise levels while preserving diagnostically relevant features.

---

## Pipeline Stages (6-Stage Ordered System)

The pipeline comprises six ordered stages. All stages must be applied in the specified order for the pipeline to be considered **ACTIVE**. The pipeline is considered **ABSENT** when images are passed to the CNN with resize only.

### Stage 1 — FOV Standardization
- **Operation:** Fundus circle detection via Hough transform; black border removal
- **Purpose:** Remove non-retinal background; standardize the field of view across images from different devices and acquisition protocols
- **Output:** Cropped fundus region with standardized circular boundary

### Stage 2 — Image Centering and Resize
- **Operation:** Center the detected fundus region; resize to 512×512 pixels
- **Purpose:** Ensure uniform spatial dimensions for CNN input; center the retinal disc for consistent feature positioning
- **Output:** 512×512 pixel image with centered fundus

### Stage 3 — Green Channel Extraction
- **Operation:** Extract the green channel from the RGB image
- **Purpose:** The green channel provides the highest vessel-to-background contrast in retinal images, maximizing visibility of microvascular structures (microaneurysms, hemorrhages, vessel patterns)
- **Output:** Single-channel (grayscale) image from green channel

### Stage 4 — Pixel Intensity Normalization
- **Operation:** Normalize pixel intensities to [0, 1] range via min-max normalization
- **Purpose:** Standardize intensity distributions across images from different devices and illumination conditions
- **Output:** Normalized single-channel image with pixel values in [0, 1]

### Stage 5 — CLAHE Enhancement (Upgraded)
- **Operation:** Contrast-Limited Adaptive Histogram Equalization applied in LAB color space (L-channel) with dynamic clip limit
- **Configuration:**
  - Color space: LAB (L-channel processing)
  - Tile grid size: 8×8
  - Clip limit: Dynamic (optimized within experimental framework per DGL-5)
  - Modified formulation: CL = T/80 (theoretical reference from LC-AlTimemy-2021; independently validated)
- **Purpose:** Enhance local contrast to improve visibility of small lesion features (microaneurysms, small hemorrhages) while controlling over-enhancement artifacts via clip limit control
- **Output:** Contrast-enhanced image

### Stage 6 — HSV Contrast Enhancement
- **Operation:** Additional contrast adjustment in HSV color space (V-channel manipulation)
- **Purpose:** Fine-tune overall image contrast and brightness for optimal feature presentation to the CNN
- **Output:** Final preprocessed image ready for CNN input

---

## Relationship to 5-Component Governance Definition

The governance documents (INVARIANTS OD-3, RESEARCH_ARCHITECTURE Section 3.1) define a 5-component pipeline. This 6-stage specification is a more granular description of the same operations, splitting "FOV standardization" (governance component 1) into two explicit stages (Stage 1: circle detection/cropping, Stage 2: centering/resize). The mapping is:

| Governance Component | Pipeline Stage(s) |
|---|---|
| 1. FOV Standardization | Stage 1 + Stage 2 |
| 2. Green Channel Imaging | Stage 3 |
| 3. Normalization | Stage 4 |
| 4. CLAHE Enhancement | Stage 5 |
| 5. HSV Contrast Enhancement | Stage 6 |

---

## Upgraded CLAHE Modifications

The CLAHE implementation in this pipeline differs from standard OpenCV CLAHE in the following ways:

1. **LAB color space processing:** CLAHE is applied to the L-channel in LAB color space rather than directly to grayscale, preserving color information integrity
2. **Dynamic clip limit:** The clip limit is not fixed at a conventional default (e.g., 2.0) but is treated as an optimizable parameter within the experimental framework (H-2)
3. **Tile-based adaptive processing:** 8×8 tile grid provides local contrast enhancement adapted to regional image characteristics

---

## Data Augmentation Separation

Data augmentation operations (horizontal flip, vertical flip, rotation ±15°, zoom ±10%, brightness variation) are applied during training as a **separate data augmentation layer** and are NOT part of the preprocessing pipeline. This separation is critical: it enables clean ablation in component-level experiments (Experiment 2) by isolating the effect of preprocessing from the effect of augmentation.

---

## Assertion

The preprocessing pipeline, as specified above, constitutes a deterministic, reproducible, and order-dependent transformation of raw fundus images into a standardized feature space. The pipeline is an integral component of the diagnostic model, not an external data preparation step.
