# RESEARCH_ARCHITECTURE_MASTER.md

## Integrated Preprocessing–CNN Framework for Multi-Stage Diabetic Retinopathy Classification

**Candidate:** Yesmukhamedov N.S.
**Status:** Binding Methodological Blueprint
**Function:** Experimental, statistical, and architectural formalization of the dissertation research
**Document Version:** 4.1. Supersedes V3/v2.2. Consistent with INVARIANTS v4.1 and Dissertation Project V4.1. V4.0 changes: 6-stage pipeline replacing 5-component V3; green channel and HSV enhancement removed; flat-field correction (Stage 2) and canonical flip (Stage 0) added; CLAHE upgraded to dual-constraint stochastic; normalization changed to ImageNet channel-wise; augmentation integrated as Stage 5; Experiment 1 expanded to 6 configurations (A–F) including binocular blending; baseline updated from "resize only" to "crop+resize+ImageNet normalize". V4.1 changes (2026-03-26): Stage 0 expanded to Stage 0a (Canonical Flip) + Stage 0b (OD-Fovea Rotation Normalization); 5-fold → 3-fold; EyePACS 40% subset (~14,050 used); max_epochs 50 → 20; binocular blending Optional Extension paragraph added to §3.1.

---

# 1. RESEARCH LOGIC STRUCTURE

## 1.1 Central Causal Chain

V4 Preprocessing Pipeline (6-stage)
→ Improved Microvascular Feature Visibility (quantified via CNR, VVI, Entropy, SSIM)
→ Stabilized CNN Feature Extraction (validated via Grad-CAM ALO (primary) and IoU (secondary) with lesion masks)
→ Improved Multi-Class DR Classification (across multiple datasets and camera hardware)
→ Measurable Statistical Dominance (EH-3 criteria, independently for ResNet-50 and EfficientNet-B3)

Dominance is defined strictly per Invariants (Δ weighted F1 ≥ 5 pp; Δ ROC-AUC ≥ 0.02; no Cohen's Kappa degradation).

---

# 2. DATA ARCHITECTURE

## 2.1 Tiered Dataset Architecture (v2.1)

The v2.1 dataset architecture comprises seven datasets organized into four functional tiers: Training, Robustness, Clinical, External Generalization, and Device Domain Shift.

### 2.1.1 TRAINING Tier — EyePACS (Primary Training & Ablation)

* **Role:** Primary training dataset for Experiments 1 and 2 (causal ablation and component ablation)
* **Approximate size:** ~35,126 labeled fundus images (40% subset of full EyePACS; ~14,050 used for experiments)
* **Taxonomy:** Five-class DR staging (DR 0–4)
* **Camera models:** Canon CR-1
* **Public availability:** Yes (Kaggle)
* **Class imbalance:** Severe — must be documented and all performance claims interpreted in context of distributional asymmetry (per SB-2.1)

### 2.1.2 ~~ROBUSTNESS Tier~~ — APTOS 2019 [DROPPED V3 — No Active Role]

<!-- DROPPED V3: Old Experiment 3 (robustness to synthetic image degradation) has been removed from V3 scope. APTOS 2019 no longer serves as an active experimental dataset. Historical entry preserved for audit trail. -->

* **Role [V3: DROPPED]:** Was dataset for old Experiment 3 — robustness to synthetic image degradation (Gaussian noise, blur, low illumination). This experiment is not part of V3.
* **Approximate size:** ~3,662 labeled fundus images
* **Taxonomy:** Five-class DR staging (DR 0–4)
* **Camera models:** Mixed
* **Public availability:** Yes (Kaggle)
* **V3 Note:** APTOS 2019 may be referenced as a secondary/supplementary dataset in historical or methodological context but is NOT an active V3 experimental dataset.

### 2.1.3 CLINICAL Tier — IDRiD (Clinical Validation + Lesion Localization)

* **Role:** Clinical validation dataset for V3 Experiments 2 (CLAHE sweep), 3 (generalization), and 4 (explainability) — explainability analysis (Grad-CAM ALO/IoU with pixel-level lesion masks), CLAHE parameter sweep, and external generalization evaluation
* **Approximate size:** ~516 images (81 with pixel-level lesion annotations for four lesion types: microaneurysms, hemorrhages, hard exudates, soft exudates)
* **Taxonomy:** Five-class DR staging + pixel-level lesion masks
* **Camera models:** Kowa
* **Public availability:** Yes

### 2.1.4 EXTERNAL Tier — Messidor / Messidor-2 (External Generalization)

* **Role:** External generalization targets for V3 Experiment 3 — model trained on EyePACS evaluated without retraining
* **Approximate size:** Messidor: ~1,200 images; Messidor-2: ~1,748 images
* **Taxonomy:** Referable/non-referable DR grading + severity grade
* **Camera models:** Topcon
* **Public availability:** Yes (upon registration)

### 2.1.5 DOMAIN Tier — RFMiD (Device Domain Shift)

* **Role:** Device domain shift evaluation for V3 Experiment 3 — cross-camera performance testing
* **Approximate size:** ~3,200 images
* **Taxonomy:** Multi-disease taxonomy with DR subset (taxonomic mapping to 5-class must be documented)
* **Camera models:** Topcon, Kowa
* **Public availability:** Yes

### 2.1.6 DOMAIN Tier — DDR (Device Domain Shift)

* **Role:** Device domain shift evaluation for V3 Experiment 3
* **Approximate size:** ~13,673 images
* **Taxonomy:** Five-class DR staging
* **Camera models:** Canon, Topcon
* **Public availability:** Yes

### 2.1.7 DOMAIN Tier — ODIR-5K (Device Domain Shift)

* **Role:** Device domain shift evaluation for V3 Experiment 3
* **Approximate size:** ~5,000 images (bilateral)
* **Taxonomy:** Multi-disease taxonomy with DR subset (taxonomic mapping to 5-class must be documented)
* **Camera models:** Canon, Zeiss
* **Public availability:** Yes

---

## 2.2 Split Strategy

All experiments use **3-fold cross-validation with patient-level stratified split** to prevent data leakage. For each fold iteration, 2 folds serve as training data and 1 fold as test data. The process is repeated 3 times. All metrics are reported as mean ± standard deviation across folds. This replaces the v2.1 5-fold CV and the v1.0 fixed 80/10/10 split.

<!-- 5-fold CV → 3-fold CV change: updated 2026-03-26 per dr-classifier/CLAUDE.md: "Current config: 3-fold CV with patient-level split (stratified). (changed from 5-fold)" -->

Patient-level leakage control is mandatory: no patient's images may appear in both training and test partitions within any fold.

---

## 2.3 Cross-Database Generalization

Cross-database generalization defined as:

G = F1_external / F1_EyePACS

where F1_EyePACS is the test-set F1-score on the primary training dataset (EyePACS) and F1_external is the F1-score on external datasets (Messidor-2, IDRiD, or domain shift datasets) under the same trained model without retraining. Bounded strictly per OD-4.

---

# 3. PREPROCESSING PIPELINE ARCHITECTURE

Defined per OD-3 (v2.2).

**Key Scientific Framing:** The preprocessing pipeline is defined as an integral component of the diagnostic model — Stage 1 of a two-stage system: `model = V4_preprocessing + CNN`. This is the central design decision of this work: preprocessing is not ancillary data preparation but defines the feature space available to the CNN. See `methods/preprocessing-pipeline.md` for the full V4 6-stage pipeline specification.

## 3.1 V4 Ordered Pipeline (6-Stage System)

The V4 preprocessing pipeline comprises six ordered stages, replacing the V3 5-component pipeline:

- **Stage 0: Canonical Orientation** — Two-sub-stage orientation normalization (toggleable):
  - **Stage 0a: Canonical Flip** — Left→right eye horizontal flip (toggleable). Ensures consistent retinal orientation so the optic disc is on the right and the macula on the left.
  - **Stage 0b: OD-Fovea Rotation Normalization** — Classical CV detection of optic disc (brightest region) and fovea (darkest region with distance prior); rotates image so the OD→fovea axis is horizontal (toggleable). When detection confidence is low, rotation is skipped (fallback). Augmentation rotation_sigma is adaptive per-image from OD/fovea detection uncertainty, or fallback 13.0°.
- **Stage 1: PIL-based FOV Crop and Resize** — Foreground detection via PIL, black border removal, image centering, resize to 512×512. Always on. Replaces V3 Hough circle detection.
- **Stage 2: Flat-Field Correction** — Gaussian blur subtraction with σ=45 to normalize illumination gradients across the fundus image (toggleable). NEW in V4.
- **Stage 3: Upgraded CLAHE** — Applied in LAB color space (L-channel) with dual-constraint clip limit: clip_factor × tile_area/256, capped by global_threshold × tile_area. Stochastic application at train time (80% probability). Toggleable. (UPGRADED from V3 dynamic clip limit)
- **Stage 4: ImageNet Channel-wise Normalization** — (x − mean)/std → tensor, using ImageNet statistics. Always on, always applied last to image. Replaces V3 pixel normalization [0,1].
- **Stage 5: Integrated Augmentation** — Unified affine (rotation + zoom + stretch + shear) + brightness/contrast + PCA color jitter. Train time only, inserted before Stage 4. NEW in V4; replaces separate augmentation layer.

Pipeline considered **ACTIVE** (full V4) when all toggleable stages (0, 2, 3, 5) are applied in specified order. Pipeline considered **ABSENT** (V4 baseline) when images are processed with crop + resize + ImageNet normalize only (Stages 1 + 4).

Augmentation is integrated as Stage 5 of the V4 pipeline. Individual augmentation sub-transforms are toggleable via config flags, enabling ablation within the pipeline framework.

*[V3 Historical Pipeline (5-component): (1) FOV Standardization via Hough circle detection, (2) CLAHE enhancement (LAB, dynamic clip limit), (3) HSV contrast enhancement, (4) Green channel imaging, (5) Pixel normalization [0,1]. Augmentation was separate. V3 pipeline is used for Exp 2 ablation historical comparison.]*

**Optional Extension — Per-Patient Binocular Blending:** When both left-eye and right-eye images are available for a patient, the backbone CNN extracts feature vectors independently for each eye; the left-eye and right-eye feature vectors are combined via concatenation + element-wise absolute difference → MLP → 5-class logits (PatientHead architecture). Stage 0a (canonical flip) is a necessary prerequisite: without standardized eye orientation, bilateral feature alignment is undefined. Per-patient blending is applied in Experiment 1 configurations E (ResNet-50) and F (EfficientNet-B3) as optional supplementary evidence for PC-1; it is not required for EH-4 satisfaction.

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
| Vessel Visibility Index (VVI) | Detectability of retinal vasculature | Improved after flat-field correction and CLAHE |
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
| Maximum epochs | 20 (with early stopping, patience=5) |
| Loss function | Cross-entropy |
| Input resolution | 512×512 |
| Mixed precision (fp16) | Enabled for ResNet-50; DISABLED for EfficientNet (fp16 overflow fix) |

See `methods/implementation.md` for full implementation details.

---

## 4.1 ResNet-50 (Architecture A in Factorial Design)

* Pre-trained on ImageNet
* Adapted via fine-tuning for 5-class DR classification
* Serves as one architecture arm of the 6-config factorial design (A–F) in Experiment 1
* Represents the residual-connection architecture family

---

## 4.2 EfficientNet-B3 (Architecture B in Factorial Design)

* Pre-trained on ImageNet
* Adapted via fine-tuning for 5-class DR classification
* Serves as the second architecture arm of the 6-config factorial design (A–F) in Experiment 1
* Represents the compound-scaling architecture family (EfficientNet)

The use of two established pretrained backbone families (ResNet, EfficientNet) provides a replication test across architecture families and satisfies the EH-4 replication requirement.

---

## 4.3 Transfer Learning Layer

### EfficientNetB0 — Two-Stage Fine-Tuning Protocol

Backbone: EfficientNetB0 (ImageNet pre-trained)

Two strategies (used as training methods; H-3 dropped in V3, not tested as independent hypothesis):

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

Used in V4 Experiment 4 for Grad-CAM explainability analysis. EfficientNet-B4 provides higher-resolution feature maps suitable for activation visualization and ALO (primary) / IoU (secondary) computation against IDRiD pixel-level lesion masks.

---

### Per-Patient Binocular Blending — Configs E, F (Optional Extension)

PatientHead model for per-patient fusion of bilateral fundus images (left eye + right eye):

**Architecture:** Backbone (ResNet-50 or EfficientNet-B3) extracts feature vectors independently for each eye. Left-eye and right-eye feature vectors are combined via concatenation + element-wise absolute difference → MLP → 5-class logits.

**Purpose:** Tests whether bilateral information improves DR grading beyond single-image classification. Config E uses ResNet-50 backbone; Config F uses EfficientNet-B3 backbone.

**Scope:** Configs E and F provide supplementary evidence for PC-1 (H-1) but are not required for EH-4 satisfaction. Results reported alongside A–D as optional extension evidence.

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

## 5.3 ~~Experiment 3 — Robustness to Image Degradation~~ [DROPPED V3]

<!-- DROPPED V3: Old Experiment 3 (robustness to synthetic image degradation on APTOS 2019) has been removed. Old Experiment 3 tested H-3 which is also dropped. Historical content preserved below. -->

### DROPPED (V3): Old Experiment 3 — Robustness to Image Degradation

> **V3 Status:** DROPPED. This experiment is not part of V3 scope. The robustness to synthetic image degradation experiment (Gaussian noise, blur, low illumination on APTOS 2019) has been removed. APTOS 2019 is no longer an active V3 experimental dataset.

**Was:** Old Experiment 3 — testing model robustness under degraded imaging conditions (APTOS 2019, Gaussian noise/blur/illumination at three severity levels).

<!-- END DROPPED V3 -->

---

## 5.4 Experiment 4 (V3) — Explainability Analysis (Grad-CAM / ALO)

**V3 Experiment Number:** Experiment 4 (renumbered from old Experiment 4 — number unchanged)

**Purpose:** Determine whether preprocessing shifts CNN attention toward clinically relevant lesion regions. Closes the evidential gap in the causal chain: Preprocessing → Improved Feature Visibility → Improved Classification.

**Model:** EfficientNet-B4

**Sampling:** 10 randomly selected images per DR class (50 total). Two pipelines compared:

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

## 5.5 ~~Experiment 5 — Clinical Generalization~~ [MERGED INTO V3 EXP 3]
## 5.6 ~~Experiment 6 — Device Domain Shift~~ [MERGED INTO V3 EXP 3]

<!-- V3: Old Experiments 5 and 6 have been merged into V3 Experiment 3. See §5.3-NEW below. -->

### V4 Experiments 5 + 6 — Cross-Dataset Generalization and Device Domain Shift

**V3 Historical:** Experiment 3 (merged from old Experiments 5 + 6). In V4, these are split into Experiment 5 (cross-database generalization, H-4) and Experiment 6 (device domain shift, H-6).

**Preprocessing:** All trained models use the V4 6-stage preprocessing pipeline. Baseline models use crop+resize+ImageNet normalize only (Stages 1+4).

**Purpose:** Evaluate generalization to independent clinical datasets (no retraining) AND robustness to images captured by different fundus cameras. Tests H-4 (cross-database transferability) and H-6 (device robustness).

**Hypotheses tested:** H-4 (Cross-Database Transferability), H-6 (Device Robustness)

**Evaluation datasets:**

| | Dataset | Role | Camera |
| --- | --- | --- | --- |
| TRAIN | EyePACS | Training source | Canon CR-1 |
| TEST | Messidor | External generalization | Topcon |
| TEST | Messidor-2 | External generalization | Topcon |
| TEST | IDRiD | Clinical validation (Indian population) | Kowa |
| TEST | RFMiD | Device domain shift | Topcon, Kowa |
| TEST | DDR | Device domain shift | Canon, Topcon |
| TEST | ODIR-5K | Device domain shift | Canon, Zeiss |

**Metrics:**
- Accuracy, Weighted F1, ROC-AUC.
- Generalization ratio G = F1_external / F1_EyePACS per OD-4.
- F1-score, ROC-AUC per camera group (cross-device performance matrix).
- Clinical screening metrics: Sensitivity, Specificity, PPV, NPV for referable DR (grade ≥ 2).

**Published benchmarks for comparison:** Gulshan 2016 (AUC 0.990 on Messidor-2), Rakhlin 2017 (AUC 0.967 on Messidor-2), Saxena 2020 (AUC 0.92 on Messidor-2), Ting 2017 (AUC 0.936 referable DR across 10 datasets).

---

## 5.7 ~~Experiment 7 — Clinical Validation (Dirty Data Pipeline)~~ [FUTURE WORK — V3]

<!-- V3: Experiment 7 (Kazakh clinical validation) is not an active V3 experiment. No data available. Marked as future work. -->

### FUTURE WORK: Kazakh Clinical Validation

**V3 Status:** Not an active experiment. Retained as future work placeholder.

**Was:** Old Experiment 7 — testing the preprocessing pipeline on clinical fundus images from Kazakh medical centers (dirty data, variable quality, non-standardized acquisition).

**Future work note:** When Kazakh medical center data becomes available under institutional agreements, this experiment may be executed as an extension (VCR-4). Results would supplement PC-1 under NC-15 constraints.

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

Reported for V3 Experiments 1 and 3.

---

## 6.4 Calibration Metrics

* Expected Calibration Error (ECE)
* Brier Score

Reported for V3 Experiments 1 and 3.

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

Per OD-4. Reported for V3 Experiment 3.

---

## 6.8 Statistical Tests

Mandatory:

* McNemar test (paired classification comparison) — Experiments 1
* DeLong test (ROC-AUC comparison) — V3 Experiments 1 and 3
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

*[V3 Historical: 4 configs A–D only; baseline was "resize only"; pipeline was 5-component V3. This V4 update adds configs E, F and updates baseline definition.]*

**Dominance validation criterion (V4):** Preprocessing Dominance validated if:

* Performance(B) > Performance(A) — independently for ResNet-50, AND
* Performance(D) > Performance(C) — independently for EfficientNet-B3

with EH-3 criteria (Δ weighted F1 ≥ 5 pp; Δ ROC-AUC ≥ 0.02; no Cohen's Kappa degradation) satisfied for both comparisons.

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

* Formalization of preprocessing dominance hypothesis (validated via factorial ablation on two established architectures, 6 configurations A–F)
* Dual-constraint stochastic CLAHE validation within DR multi-class context (LAB color space, dual-constraint clip limit, 80% train-time probability)
* Flat-field correction via Gaussian blur subtraction as novel preprocessing stage (Stage 2)
* Canonical orientation as novel preprocessing stage (Stage 0): Stage 0a (canonical flip, left→right eye normalization) + Stage 0b (OD-fovea rotation normalization so OD→fovea axis is horizontal)
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

| Claim | Validated By (V4) | V4 Status |
| --- | --- | --- |
| PC-1 | V4 Exp 1 (6 configs A–F, ResNet-50 + EfficientNet-B3) + EH-3 | Active |
| PC-2 | V4 Exp 2 CLAHE dual-constraint parameter sweep (clip_factor, global_threshold) on IDRiD | Active |
| PC-3 (Two-Stage Fine-Tuning) | — | DEMOTED: Training strategy only; H-3 dropped |
| PC-4 | Mathematical derivation (laser-tissue model) | Secondary/supplementary |
| PC-5 | UML + system design | Secondary/supplementary |
| PC-6 | V4 Exp 5 generalization ratios (G = F1_external / F1_EyePACS) on Messidor, Messidor-2, IDRiD | Active |
| PC-7 | V4 Exp 4 Grad-CAM ALO (primary) + IoU (secondary) on IDRiD masks | Active |
| PC-8 | V4 Exp 2 component ablation (V4 Levels 0–4: baseline → +flip → +flat-field → +CLAHE → full V4 pipeline) | Active |
| PC-9 | V4 Exp 6 cross-camera metrics (device domain shift robustness across Canon, Topcon, Kowa, Zeiss) | Active |
| PC-1 (supplementary) | Future work: Kazakh clinical validation (dirty data pipeline) | Future work |

Mapped to ARGUMENT_MAP.

---

# 12. FUNCTION OF THIS DOCUMENT

This file is:

* The methodological backbone of Chapter 2
* The execution blueprint for Chapter 4
* The validation structure for Chapter 5
* The defense shield during committee questioning

---
