# RESEARCH_ARCHITECTURE_MASTER.md

## Integrated Preprocessing–CNN Framework for Multi-Stage Diabetic Retinopathy Classification

**Candidate:** Yesmukhamedov N.S.
**Status:** Binding Methodological Blueprint
**Function:** Experimental, statistical, and architectural formalization of the dissertation research
**Document Version:** 4.0. Supersedes v2.2/V3. Consistent with INVARIANTS v4.0 and Dissertation Project V4.0.

---

# 1. RESEARCH LOGIC STRUCTURE

## 1.1 Central Causal Chain

V4 Preprocessing Pipeline (6-stage)
→ Improved Microvascular Feature Visibility (quantified via CNR, VVI, Entropy, SSIM)
→ Stabilized CNN Feature Extraction (validated via Grad-CAM ALO/IoU with lesion masks)
→ Improved Multi-Class DR Classification (across multiple datasets and camera hardware)
→ Measurable Statistical Dominance (EH-3 criteria, independently for ResNet-50 and EfficientNet-B3)

Dominance is defined strictly per Invariants (Δ weighted F1 ≥ 5 pp; Δ ROC-AUC ≥ 0.02; no Cohen's Kappa degradation).

---

# 2. DATA ARCHITECTURE

## 2.1 Tiered Dataset Architecture (V4)

The V4 dataset architecture comprises seven datasets organized into four functional tiers: Training, Robustness, Clinical, External Generalization, and Device Domain Shift.

### 2.1.1 TRAINING Tier — EyePACS (Primary Training & Ablation)

* **Role:** Primary training dataset for Experiments 1 and 2 (causal ablation and component ablation)
* **Approximate size:** ~35,126 labeled fundus images (40% subset of full EyePACS; ~14,050 used for experiments)
* **Taxonomy:** Five-class DR staging (DR 0–4)
* **Camera models:** Canon CR-1
* **Public availability:** Yes (Kaggle)
* **Class imbalance:** Severe — must be documented and all performance claims interpreted in context of distributional asymmetry (per SB-2.1)

### 2.1.2 ROBUSTNESS Tier — APTOS 2019 (Robustness Experiments)

* **Role:** Dataset for Experiment 3 — robustness to synthetic image degradation (Gaussian noise, blur, low illumination)
* **Approximate size:** ~3,662 labeled fundus images
* **Taxonomy:** Five-class DR staging (DR 0–4)
* **Camera models:** Mixed
* **Public availability:** Yes (Kaggle)

### 2.1.3 CLINICAL Tier — IDRiD (Clinical Validation + Lesion Localization)

* **Role:** Clinical validation dataset for Experiments 4 and 5 — explainability analysis (Grad-CAM IoU with pixel-level lesion masks) and external generalization evaluation
* **Approximate size:** ~516 images (81 with pixel-level lesion annotations for four lesion types: microaneurysms, hemorrhages, hard exudates, soft exudates)
* **Taxonomy:** Five-class DR staging + pixel-level lesion masks
* **Camera models:** Kowa
* **Public availability:** Yes

### 2.1.4 EXTERNAL Tier — Messidor / Messidor-2 (External Generalization)

* **Role:** External generalization targets for Experiment 5 — model trained on EyePACS evaluated without retraining
* **Approximate size:** Messidor: ~1,200 images; Messidor-2: ~1,748 images
* **Taxonomy:** Referable/non-referable DR grading + severity grade
* **Camera models:** Topcon
* **Public availability:** Yes (upon registration)

### 2.1.5 DOMAIN Tier — RFMiD (Device Domain Shift)

* **Role:** Device domain shift evaluation for Experiment 6 — cross-camera performance testing
* **Approximate size:** ~3,200 images
* **Taxonomy:** Multi-disease taxonomy with DR subset (taxonomic mapping to 5-class must be documented)
* **Camera models:** Topcon, Kowa
* **Public availability:** Yes

### 2.1.6 DOMAIN Tier — DDR (Device Domain Shift)

* **Role:** Device domain shift evaluation for Experiment 6
* **Approximate size:** ~13,673 images
* **Taxonomy:** Five-class DR staging
* **Camera models:** Canon, Topcon
* **Public availability:** Yes

### 2.1.7 DOMAIN Tier — ODIR-5K (Device Domain Shift)

* **Role:** Device domain shift evaluation for Experiment 6
* **Approximate size:** ~5,000 images (bilateral)
* **Taxonomy:** Multi-disease taxonomy with DR subset (taxonomic mapping to 5-class must be documented)
* **Camera models:** Canon, Zeiss
* **Public availability:** Yes

---

## 2.2 Split Strategy

All experiments use **3-fold cross-validation with patient-level stratified split** to prevent data leakage. For each fold iteration, 2 folds serve as training data and 1 fold as test data. The process is repeated 3 times. All metrics are reported as mean ± standard deviation across folds. This replaces the v2.1 5-fold CV and the v1.0 fixed 80/10/10 split.

Patient-level leakage control is mandatory: no patient's images may appear in both training and test partitions within any fold.

---

## 2.3 Cross-Database Generalization

Cross-database generalization defined as:

G = F1_external / F1_EyePACS

where F1_EyePACS is the test-set F1-score on the primary training dataset (EyePACS) and F1_external is the F1-score on external datasets (Messidor-2, IDRiD, or domain shift datasets) under the same trained model without retraining. Bounded strictly per OD-4.

---

# 3. PREPROCESSING PIPELINE ARCHITECTURE

Defined per OD-3 (V4.0).

**Key Scientific Framing:** The preprocessing pipeline is defined as an integral component of the diagnostic model — Stage 1 of a two-stage system: `model = preprocessing + CNN`. This is the central design decision of this work: preprocessing is not ancillary data preparation but defines the feature space available to the CNN.

## 3.1 V4 Ordered Pipeline (6-Stage System)

The V4 preprocessing pipeline comprises six stages, replacing the V3 5-component pipeline:

- **Stage 0: Canonical Flip** — Left→right eye orientation normalization (toggleable). Ensures consistent retinal orientation across bilateral image pairs.
- **Stage 1: PIL-based FOV Crop and Resize** — Foreground detection via PIL, black border removal, image centering, resize to 512×512. Always on. Replaces V3 Hough circle detection.
- **Stage 2: Flat-Field Correction** — Gaussian blur subtraction with σ=45 to normalize illumination gradients across the fundus image (toggleable). NEW in V4; replaces HSV enhancement.
- **Stage 3: Upgraded CLAHE** — Applied in LAB color space (L-channel) with dual-constraint clip limit: clip_factor × tile_area/256, capped by global_threshold × tile_area. Stochastic application at train time (80% probability). Toggleable. (UPGRADED from V3 dynamic clip limit)
- **Stage 4: ImageNet Channel-wise Normalization** — (x − mean)/std → tensor, using ImageNet statistics. Always on, always applied last to image. Replaces V3 pixel normalization [0,1].
- **Stage 5: Integrated Augmentation** — Unified affine (rotation + zoom + stretch + shear) + brightness/contrast + PCA color jitter. Train time only, inserted before Stage 4. Model-specific presets: "resnet" (full aug) vs. "efficientnet" (reduced aug). NEW in V4; replaces separate augmentation layer.

Pipeline considered **ACTIVE** (full V4) when all toggleable stages (0, 2, 3, 5) are applied in specified order. Pipeline considered **ABSENT** (V4 baseline) when images are processed with crop + resize + ImageNet normalize only (Stages 1 + 4).

**Augmentation integration:** Augmentation (Stage 5) is integrated into the pipeline at train time and is NOT a separate data augmentation layer. This differs from V3 where augmentation was kept separate.

*[V3 Historical Pipeline (5-component): (1) FOV Standardization via Hough circle detection, (2) Green channel extraction, (3) Pixel normalization [0,1], (4) CLAHE with dynamic clip limit on LAB L-channel, (5) HSV contrast enhancement. Augmentation was separate.]*

**Optional Extension — Per-Patient Binocular Blending:** Applied in Experiment 1 configurations E and F. Blends paired left/right eye images per patient before or during feature extraction, providing additional regularization via bilateral context.

---

## 3.2 CLAHE Mathematical Formalization (V4)

V4 Dual-Constraint Clip Limit:

CL_tile = min(clip_factor × tile_area / 256, global_threshold × tile_area)

where clip_factor and global_threshold are tunable hyperparameters. Applied stochastically at train time (probability = 0.80); applied deterministically at inference time.

V3 Reference Formulations (Historical):
- Conventional: CL = ⌈L/T⌉ + β(φ − ⌈L/T⌉)
- LC-AlTimemy-2021 (STARE dataset): CL = T / 80

Transferability from STARE to EyePACS is NOT assumed (DGL-5). V4 clip limit parameters must be independently validated within the dissertation's experimental framework.

---

## 3.3 Image Quality Metrics

To quantify the effect of preprocessing independently of downstream classification, the following image quality metrics are measured at each pipeline stage (before and after each component):

| Metric | Measures | Expected Improvement |
| --- | --- | --- |
| Contrast-to-Noise Ratio (CNR) | Signal quality of vessel structures vs. background | Higher CNR after flat-field correction and CLAHE |
| Vessel Visibility Index (VVI) | Detectability of retinal vasculature | Improved after flat-field correction + CLAHE |
| Image Entropy | Information content of the image | Increased after contrast enhancement |
| Structural Similarity (SSIM) | Preservation of structural information relative to original | High SSIM confirms no destructive artifacts introduced |

These metrics are reported in Experiment 2 (pipeline analysis) and provide evidence for the causal chain link: preprocessing → improved microvascular feature visibility.

---

# 4. MODEL ARCHITECTURE LAYER

## 4.0 Standardized Training Configuration

| Parameter | Value |
| --- | --- |
| Optimizer | Adam |
| Learning rate | 1e-4 |
| Batch size | 16 |
| Maximum epochs | 50 (with early stopping) |
| Loss function | Cross-entropy |
| Input resolution | 512×512 |

See `methods/implementation.md` for full implementation details.

---

## 4.1 ResNet-50 (Architecture A in Factorial Design)

* Pre-trained on ImageNet
* Adapted via fine-tuning for 5-class DR classification
* Serves as Architecture A in the Experiment 1 factorial design (baseline and full V4 pipeline configs A, B, E)
* Uses "resnet" augmentation preset (full augmentation)
* Represents the residual-connection architecture family

---

## 4.2 EfficientNet-B3 (Architecture B in Factorial Design)

* Pre-trained on ImageNet
* Adapted via fine-tuning for 5-class DR classification
* Serves as Architecture B in the Experiment 1 factorial design (baseline and full V4 pipeline configs C, D, F)
* Represents the compound-scaling architecture family (EfficientNet)

The use of two established pretrained backbone families (ResNet, EfficientNet) provides a replication test across architecture families and satisfies the EH-4 replication requirement.

---

## 4.3 Transfer Learning Layer

### EfficientNetB0 — Two-Stage Fine-Tuning Protocol

Backbone: EfficientNetB0 (ImageNet pre-trained)

Two strategies (tested in Experiment 3):

**Method 1 — Frozen:**

* Train classification head only

**Method 2 — Progressive Fine-Tuning:**

* Stage 1: Frozen base layers with classification head training
* Stage 2: Unfreeze upper layers for progressive fine-tuning

Expected empirical baseline (self-publications):

* Frozen F1 ≈ 0.62
* Fine-tuned F1 ≈ 0.74

**Note (v2.1):** This protocol is now replicated on EyePACS instead of APTOS 2019. Prior self-publication results (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF) constitute the foundational empirical record and must be cited per SIR-4.

### EfficientNet-B4 — Explainability Analysis

Backbone: EfficientNet-B4 (ImageNet pre-trained)

Used in Experiment 4 for Grad-CAM explainability analysis. EfficientNet-B4 provides higher-resolution feature maps suitable for activation visualization and IoU computation against IDRiD pixel-level lesion masks.

---

# 5. EXPERIMENTAL DESIGN

## 5.0 Cross-Validation Protocol (Applies to All Experiments)

All experiments use 3-fold cross-validation with patient-level stratified split. For each fold iteration, 2 folds serve as training data and 1 fold as test data. The process is repeated 3 times. All metrics are reported as mean ± standard deviation across folds.

---

## 5.1 Experiment 1 — Causal Improvement (Preprocessing vs. Architecture)

**Purpose:** Determine whether preprocessing improves classification independently of CNN architecture. This is the primary experiment validating H-1 and promoting PC-1.

**Dataset:** EyePACS

**Design:** Factorial using ResNet-50 and EfficientNet-B3, 6 configurations.

| Configuration | Preprocessing | Architecture |
| --- | --- | --- |
| A | baseline (crop + resize + ImageNet normalize) | ResNet-50 |
| B | full V4 pipeline | ResNet-50 |
| C | baseline (crop + resize + ImageNet normalize) | EfficientNet-B3 |
| D | full V4 pipeline | EfficientNet-B3 |
| E | full V4 pipeline + per-patient binocular blending (optional) | ResNet-50 |
| F | full V4 pipeline + per-patient binocular blending (optional) | EfficientNet-B3 |

*[V3 Historical: 4 configurations A–D; baseline was "resize only"; pipeline was 5-component V3]*

**Dominance validation:** Preprocessing Dominance validated if Performance(B) > Performance(A) AND Performance(D) > Performance(C) with EH-3 criteria satisfied independently for both architectures.

**Statistical analysis:** Mixed-effects model across folds (fold as random effect). McNemar test for paired classification comparison. DeLong test for ROC-AUC comparison. Bonferroni/Holm correction for multiple comparisons.

---

## 5.2 Experiment 2 — Preprocessing Component Ablation

**Purpose:** Quantify the contribution of each preprocessing component to classification performance. Identifies which pipeline stages drive improvement.

**Dataset:** EyePACS

**Ablation configurations (V4 levels):**

| Pipeline Configuration | Stages Included |
| --- | --- |
| baseline | Stages 1 + 4 only (FOV crop+resize + ImageNet normalize) |
| baseline + canonical flip | Stages 0 + 1 + 4 |
| baseline + flat-field correction | Stages 1 + 2 + 4 |
| baseline + CLAHE | Stages 1 + 3 + 4 |
| baseline + augmentation | Stages 1 + 4 + 5 |
| full V4 pipeline | All stages (0 + 1 + 2 + 3 + 4 + 5) |

*[V3 Historical: resize → resize + normalize → resize + CLAHE → resize + normalize + CLAHE → full 5-component pipeline]*

**Metrics:** Primary metrics (Weighted F1, ROC-AUC, Cohen's Kappa, Accuracy) plus image quality metrics (CNR, VVI, Entropy, SSIM) measured at each pipeline stage.

**Statistical analysis:** Bonferroni/Holm correction for multiple comparisons across ablation levels.

---

## 5.3 Experiment 3 — Robustness to Image Degradation

**Purpose:** Evaluate model robustness under degraded imaging conditions that simulate real clinical variability.

**Dataset:** APTOS 2019

**Image perturbations** applied at three severity levels (low, medium, high):

| Distortion Type | Control Parameter | Simulates |
| --- | --- | --- |
| Gaussian noise | σ (noise standard deviation) | Sensor noise, low-light acquisition |
| Gaussian blur | Kernel size | Focus errors, motion blur |
| Low illumination | Brightness reduction factor | Poor lighting conditions in clinical settings |

Performance drop is measured relative to clean (undistorted) images.

**Binary clinical threshold experiment:** Evaluates binary classification (non-referable DR: grades 0–1 vs. referable DR: grades 2–4) under degraded conditions. Reports sensitivity, specificity, PPV, NPV, and ROC-AUC for the clinical screening use case.

---

## 5.4 Experiment 4 — Explainability Analysis

**Purpose:** Determine whether preprocessing shifts CNN attention toward clinically relevant lesion regions. Closes the evidential gap in the causal chain: Preprocessing → Improved Feature Visibility → Improved Classification.

**Model:** EfficientNet-B4

**Sampling:** 10 randomly selected images per DR class (50 total), plus additional degraded images from Experiment 3. Two pipelines compared:

| Pipeline | Description |
| --- | --- |
| Baseline | crop + resize + ImageNet normalize only (Stages 1 + 4) |
| Proposed | full V4 pipeline (all 6 stages) |

**Explainability method:** Grad-CAM (Gradient-weighted Class Activation Mapping).

**Quantitative evaluation:** Attention–Lesion Overlap (ALO, primary) and Intersection-over-Union (IoU, secondary) between Grad-CAM activation regions and pixel-level lesion masks from the IDRiD dataset. Four lesion types: microaneurysms, hemorrhages, hard exudates, soft exudates.

**Hypothesis:** ALO(preprocessing) > ALO(baseline) (primary), IoU(preprocessing) > IoU(baseline) (secondary), demonstrating that preprocessing directs model attention to clinically relevant structures.

**Deliverables:**

* Grad-CAM overlays for representative images from each DR class (0–4) — with vs. without preprocessing
* ALO scores (primary) and IoU scores (secondary) between Grad-CAM activations and IDRiD pixel-level lesion masks (per lesion type)
* Attention consistency maps across datasets — whether the model attends to similar features on EyePACS, Messidor, and IDRiD images

---

## 5.5 Experiment 5 — Clinical Generalization

**Purpose:** Evaluate generalization to independent clinical datasets. No retraining is performed — the model trained on EyePACS is applied directly.

**Evaluation datasets:**

| | Dataset | Role |
| --- | --- | --- |
| TRAIN | EyePACS | Training source |
| TEST | Messidor | External generalization |
| TEST | Messidor-2 | External generalization |
| TEST | IDRiD | Clinical validation (Indian population) |

**Metrics:** Accuracy, Weighted F1, ROC-AUC. Generalization ratio G = F1_external / F1_EyePACS per OD-4.

**Published benchmarks for comparison:** Gulshan 2016 (AUC 0.990 on Messidor-2), Rakhlin 2017 (AUC 0.967 on Messidor-2), Saxena 2020 (AUC 0.92 on Messidor-2), Ting 2017 (AUC 0.936 referable DR across 10 datasets).

**Clinical screening metrics:** Sensitivity, Specificity, PPV, NPV for referable DR (grade ≥ 2).

---

## 5.6 Experiment 6 — Device Domain Shift

**Purpose:** Evaluate robustness to images captured by different fundus cameras. Tests whether the preprocessing pipeline normalizes device-specific characteristics.

**Dataset subsets grouped by camera model:**

| Dataset | Camera Models | Taxonomy |
| --- | --- | --- |
| EyePACS | Canon CR-1 | 5-class DR |
| RFMiD | Topcon, Kowa | Multi-disease (DR subset) |
| DDR | Canon, Topcon | 5-class DR |
| ODIR-5K | Canon, Zeiss | Multi-disease (DR subset) |
| IDRiD | Kowa | 5-class DR + lesion masks |
| Messidor | Topcon | Referable/Non-ref + grade |

**Cross-camera evaluation:** Performance comparison across four camera manufacturer domains (Canon, Topcon, Kowa, Zeiss). Evaluates device-induced distribution shift.

**Metrics:** Accuracy, F1-score, ROC-AUC per camera group. Generalization ratio G per camera domain.

---

## 5.7 Experiment 7 — Clinical Validation (Dirty Data Pipeline)

**Purpose:** Test the preprocessing pipeline on clinical fundus images from Kazakh medical centers. These images represent real-world clinical data with variable quality and non-standardized acquisition.

**Dataset:** Clinical fundus images from Kazakh medical centers.

**Protocol:** Apply full preprocessing pipeline to clinical images; evaluate classification using EyePACS-trained model without retraining; compare performance with and without preprocessing.

**Metrics:** Primary metrics (Weighted F1, ROC-AUC, Accuracy); ALO and IoU where lesion annotations are available.

**Linkage:** Results supplement PC-1. Bounded per NC-15.

---

# 6. STATISTICAL VALIDATION FRAMEWORK

## 6.1 Primary Metrics (EH-1)

In descending order of evidentiary weight:

1. Weighted F1-score (accounts for class imbalance)
2. ROC-AUC (threshold-independent performance measure)
3. Cohen's Kappa with quadratic weights (penalizes clinically significant ordinal misclassification)
4. Accuracy (reported but subject to inflation under class imbalance; not sufficient alone)

All primary metrics reported as **mean ± standard deviation** across 3-fold cross-validation.

---

## 6.2 Secondary Metrics

* Per-class F1 (per class Precision and Recall)
* Confusion matrix (normalized, per configuration × dataset)
* Training–Test gap (overfitting threshold = 15 pp)

---

## 6.3 Clinical Screening Metrics

* Sensitivity (for referable DR, grade ≥ 2)
* Specificity (for referable DR, grade ≥ 2)
* Positive Predictive Value (PPV)
* Negative Predictive Value (NPV)

Reported for Experiments 3 and 5.

---

## 6.4 Calibration Metrics

* Expected Calibration Error (ECE)
* Brier Score

Reported for Experiments 1 and 5.

---

## 6.5 Image Quality Metrics

* Contrast-to-Noise Ratio (CNR)
* Vessel Visibility Index (VVI)
* Image Entropy
* Structural Similarity (SSIM)

Reported for pipeline analysis in Experiment 2.

---

## 6.6 Explainability Metrics

* **ALO (Attention–Lesion Overlap)** — Primary: `ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask)` — measures lesion coverage by attention
* **IoU (Intersection-over-Union)** — Secondary: `IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask)` — measures symmetric spatial precision
* Attention consistency score

Reported for Experiment 4.

---

## 6.7 Generalization Ratio

G = F1_external / F1_EyePACS

Per OD-4. Reported for Experiments 5 and 6.

---

## 6.8 Statistical Tests

Mandatory:

* McNemar test (paired classification comparison) — Experiments 1
* DeLong test (ROC-AUC comparison) — Experiments 1, 5
* 95% confidence intervals (bootstrap ≥ 1000 iterations) — All experiments
* 3-fold cross-validation reporting (mean ± std) — All experiments
* Mixed-effects model for cross-fold analysis (fold as random effect) — Experiment 1
* Bonferroni/Holm correction for multiple comparisons — Experiments 1, 2

---

# 7. ABLATION PROTOCOL

To isolate driver of improvement (V4 Experiment 1 design):

| Configuration | Preprocessing | Architecture |
| --- | --- | --- |
| A | baseline (crop + resize + ImageNet normalize) | ResNet-50 |
| B | full V4 pipeline | ResNet-50 |
| C | baseline (crop + resize + ImageNet normalize) | EfficientNet-B3 |
| D | full V4 pipeline | EfficientNet-B3 |
| E | full V4 pipeline + binocular blending (optional) | ResNet-50 |
| F | full V4 pipeline + binocular blending (optional) | EfficientNet-B3 |

**Dominance validation criterion (V4):** Preprocessing Dominance validated if:

* Performance(B) > Performance(A) — independently for ResNet-50, AND
* Performance(D) > Performance(C) — independently for EfficientNet-B3

with EH-3 criteria (Δ weighted F1 ≥ 5 pp; Δ ROC-AUC ≥ 0.02; no Cohen's Kappa degradation) satisfied for both comparisons.

*[V3 Historical: 4 configs A–D only; baseline was "resize only"; pipeline was 5-component V3. This V4 update adds configs E, F and updates baseline definition.]*

This replaces the v1.0 criterion of (B−A) > (C−A), which confounded preprocessing effect with architecture effect.

---

# 8. COMPUTATIONAL CONSTRAINT MODEL

Resource-limited defined per OD-6:

* No guaranteed GPU
* <16GB RAM
* Real-time constraint
* Limited network access

All experiments bounded to actual hardware conditions.

---

# 8.5 Implementation Details

Software stack: Python 3.11, PyTorch, Torchvision, OpenCV, NumPy, Scikit-learn, Matplotlib. Hardware configuration documented at experiment execution time (TBD). See `methods/implementation.md` for full specification.

---

# 9. RISK CONTROL LAYER

## 9.1 Leakage Control

* No augmented images in validation/test
* No patient overlap across splits (enforced by patient-level 3-fold CV)

## 9.2 Overfitting Control

* Early stopping
* Dropout
* Batch normalization
* Weighted loss

## 9.3 Reproducibility

* Fixed random seed
* Fixed augmentation parameters
* Fixed learning rate schedule

---

# 10. FORMAL NOVELTY LAYER

Novelty does NOT claim:

* Global SOTA
* Clinical deployment validation
* Cross-modality transfer
* Replacement of ophthalmologist
* NC-16: Device certification or regulatory compliance
* NC-17: Universal preprocessing optimality — the component hierarchy is bounded to the tested architectures (ResNet-50, EfficientNet-B3) and datasets (EyePACS)

Boundaries enforced per SB-1.

Novelty IS:

* Formalization of preprocessing dominance hypothesis (validated via factorial ablation on two established architectures, 6 configurations)
* Dual-constraint stochastic CLAHE validation within DR multi-class context (LAB color space, 80% train-time probability)
* Flat-field correction via Gaussian blur subtraction as novel preprocessing stage
* Canonical flip (left→right eye orientation normalization) as novel preprocessing stage
* Per-patient binocular blending as optional extension (configs E, F)
* Integrated augmentation within pipeline (Stage 5), not separate layer
* Unified ablation-driven causal validation
* Architecture constrained to resource-limited environments
* Cross-database transferability validation across 3+ independent datasets (Messidor, Messidor-2, IDRiD)
* Grad-CAM explainability with quantitative ALO (primary) and IoU (secondary) against pixel-level lesion masks (IDRiD)
* V4 6-stage preprocessing pipeline with component-level ablation (Experiment 2)
* Device domain shift evaluation across 4 camera manufacturers (Canon, Topcon, Kowa, Zeiss)

---

# 11. DEFENSE-READY CLAIM MATRIX

| Claim | Validated By |
| --- | --- |
| PC-1 | Exp 1 (ResNet-50 + EfficientNet-B3) + EH-3 |
| PC-2 | Exp 2 curve (CLAHE threshold sensitivity) |
| PC-3 | Exp 3 metrics (fine-tuning strategy) |
| PC-4 | Mathematical derivation (laser-tissue model) |
| PC-5 | UML + system design |
| PC-6 | Exp 5 generalization ratios (G = F1_external / F1_EyePACS) |
| PC-7 | Exp 4 Grad-CAM IoU (IoU_preproc > IoU_baseline on IDRiD masks) |
| PC-8 | Exp 2 component ablation (preprocessing component hierarchy) |
| PC-9 | Exp 6 cross-camera metrics (device domain shift robustness) |
| PC-1 (supplementary) | Exp 7 clinical validation (dirty data pipeline) |

Mapped to ARGUMENT_MAP.

---

# 12. FUNCTION OF THIS DOCUMENT

This file is:

* The methodological backbone of Chapter 2
* The execution blueprint for Chapter 4
* The validation structure for Chapter 5
* The defense shield during committee questioning

---

## Protocol Revision — Exp1 Supplement (2026-04-01)

The following changes were made to all Exp1 configurations (A–F) after initial scaffold completion. All configs must be re-run from scratch after these changes.

### 1. Loss Function: Weighted CrossEntropyLoss → Focal Loss

All Exp1 configurations now use `FocalLoss(γ=2, α=inverse-frequency class weights)` instead of `nn.CrossEntropyLoss(weight=class_weights)`. Implementation in `src/training/losses.py`. Config keys: `training.loss_type: focal`, `training.focal_gamma: 2.0`.

Rationale: DR is severely class-imbalanced (grade 0 dominates). Focal Loss down-weights easy, well-classified examples and focuses gradient on hard/rare-grade samples. The α weights (inverse-frequency) are identical to those used in the old weighted CE, so class balance is preserved while the γ=2 focusing term adds additional emphasis on hard examples.

### 2. Image Input: 3-Channel RGB → 4-Channel RGB + FOV Mask

All Exp1 configurations now receive 4-channel input tensors. Channel 4 is a binary FOV mask (1.0 = real pixel data, 0.0 = zero-padding added by isotropic resize). Generated in `src/preprocessing/crop_resize.py`, appended in `src/preprocessing/pipeline_v4.py` after ImageNet normalization.

Both ResNet-50 (`conv1`) and EfficientNet-B3 (`conv_stem`) first Conv2d layers are replaced with 4-channel equivalents. Pretrained RGB weights are copied for channels 1–3; channel 4 is initialized with the mean of the RGB weights.

### 3. Resize Strategy: Direct Resize → Isotropic Resize with Centered Padding

`crop_and_resize()` in `src/preprocessing/crop_resize.py` now uses isotropic scaling (scale = target_size / max(crop_h, crop_w)) followed by centered zero-padding, instead of direct stretch-resize. This preserves the circular geometry of the fundus FOV.

### 4. Factorial Design Integrity

All six configurations (A–F) use both changes. The factorial contrast (baseline vs. full V4 pipeline) is clean: the only difference between A/C and B/D is the V4 preprocessing stages (flat-field, CLAHE, canonical flip), NOT the mask channel or loss function — those are universal infrastructure present in all configs.

---
