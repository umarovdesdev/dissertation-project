# RESEARCH_ARCHITECTURE_MASTER.md

## Integrated Preprocessing–CNN Framework for Multi-Stage Diabetic Retinopathy Classification

**Candidate:** Yesmukhamedov N.S.
**Status:** Binding Methodological Blueprint
**Function:** Experimental, statistical, and architectural formalization of the dissertation research
**Document Version:** 3.0. Supersedes v2.2. Consistent with INVARIANTS v3.0 and Dissertation Project v3.0. V3 changes: 4 experiments (not 7); H-3 dropped; "optimized clip limit" → "optimized clip limit"; EyePACS size → ~35,126 labeled; APTOS robustness role removed; old Exp 3 dropped; old Exp 5+6 merged into new Exp 3 (V3).

---

# 1. RESEARCH LOGIC STRUCTURE

## 1.1 Central Causal Chain

Contrast-Adaptive Preprocessing (5-component pipeline)
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
* **Approximate size:** ~35,126 labeled fundus images (Kaggle labeled partition)
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

All experiments use **5-fold cross-validation with patient-level split** to prevent data leakage. For each fold iteration, 4 folds serve as training data and 1 fold as test data. The process is repeated 5 times. All metrics are reported as mean ± standard deviation across folds. This replaces the v1.0 fixed 80/10/10 split.

Patient-level leakage control is mandatory: no patient's images may appear in both training and test partitions within any fold.

---

## 2.3 Cross-Database Generalization

Cross-database generalization defined as:

G = F1_external / F1_EyePACS

where F1_EyePACS is the test-set F1-score on the primary training dataset (EyePACS) and F1_external is the F1-score on external datasets (Messidor-2, IDRiD, or domain shift datasets) under the same trained model without retraining. Bounded strictly per OD-4.

---

# 3. PREPROCESSING PIPELINE ARCHITECTURE

Defined per OD-3 (v2.2).

**Key Scientific Framing:** The preprocessing pipeline is defined as an integral component of the diagnostic model — Stage 1 of a two-stage system: `model = preprocessing + CNN`. This is the central design decision of this work: preprocessing is not ancillary data preparation but defines the feature space available to the CNN. See `methods/preprocessing-pipeline.md` for the full 5-component pipeline specification (implemented as 6 ordered stages).

## 3.1 Ordered Pipeline (5-Component System)

The v2.1 preprocessing pipeline comprises five ordered components, replacing the v1.0 4-stage pipeline:

1. **FOV Standardization** — Fundus circle detection via Hough transform, black border removal, image centering, resize to 512×512. This formalizes and extends the v1.0 resize step with explicit circle detection.
2. **Green Channel Imaging** — Extraction of the green channel from RGB. The green channel provides the highest vessel-to-background contrast in retinal images. (NEW in v2.1)
3. **Normalization** — Pixel intensity normalization to [0, 1] range.
4. **CLAHE Enhancement** — Applied in LAB color space (L-channel) with optimized clip limit. The clip limit is now dynamic rather than fixed at 2.0 (v1.0). See §3.2 for mathematical formalization. (UPGRADED from v1.0)
5. **HSV Contrast Enhancement** — Additional contrast adjustment in HSV color space. (NEW in v2.1)

Pipeline considered **ACTIVE** only if all five components are applied in the specified order. Pipeline considered **ABSENT** when images are passed to the CNN with resize only (FOV standardization without subsequent pipeline components).

**Data augmentation separation:** Augmentation operations (horizontal flip, vertical flip, rotation ±15°, zoom ±10%, brightness variation) are applied during training as a separate data augmentation layer and are NOT a preprocessing component. This separation enables clean ablation in Experiment 2.

---

## 3.2 CLAHE Mathematical Formalization

Conventional:

CL = ⌈L/T⌉ + β(φ − ⌈L/T⌉)

Modified:

CL = T / 80

Transferability from STARE to APTOS is NOT assumed (DGL-5).

**Note (v2.1):** The clip limit in the dissertation's experimental pipeline is now dynamic rather than fixed at 2.0. The optimized clip limit is optimized within the dissertation's experimental framework per DGL-5 constraints. The T/80 formulation from LC-AlTimemy-2021 (STARE dataset) serves as theoretical reference; the dissertation validates its own clip limit configuration independently.

---

## 3.3 Image Quality Metrics

To quantify the effect of preprocessing independently of downstream classification, the following image quality metrics are measured at each pipeline stage (before and after each component):

| Metric | Measures | Expected Improvement |
| --- | --- | --- |
| Contrast-to-Noise Ratio (CNR) | Signal quality of vessel structures vs. background | Higher CNR after CLAHE and HSV stages |
| Vessel Visibility Index (VVI) | Detectability of retinal vasculature | Improved after green channel + CLAHE |
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
* Serves as one arm of the 2×2 factorial design in Experiment 1
* Represents the residual-connection architecture family

---

## 4.2 EfficientNet-B3 (Architecture B in Factorial Design)

* Pre-trained on ImageNet
* Adapted via fine-tuning for 5-class DR classification
* Serves as the second arm of the 2×2 factorial design in Experiment 1
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

Used in V3 Experiment 4 for Grad-CAM explainability analysis. EfficientNet-B4 provides higher-resolution feature maps suitable for activation visualization and ALO (primary) / IoU (secondary) computation against IDRiD pixel-level lesion masks.

---

# 5. EXPERIMENTAL DESIGN

## 5.0 Cross-Validation Protocol (Applies to All Experiments)

All experiments use 5-fold cross-validation with patient-level split. For each fold iteration, 4 folds serve as training data and 1 fold as test data. The process is repeated 5 times. All metrics are reported as mean ± standard deviation across folds.

---

## 5.1 Experiment 1 — Causal Improvement (Preprocessing vs. Architecture)

**Purpose:** Determine whether preprocessing improves classification independently of CNN architecture. This is the primary experiment validating H-1 and promoting PC-1.

**Dataset:** EyePACS

**Design:** 2×2 factorial using ResNet-50 and EfficientNet-B3.

| Configuration | Preprocessing | Architecture |
| --- | --- | --- |
| A | resize only | ResNet-50 |
| B | full preprocessing (all 5 components) | ResNet-50 |
| C | resize only | EfficientNet-B3 |
| D | full preprocessing (all 5 components) | EfficientNet-B3 |

**Dominance validation:** Preprocessing Dominance validated if Performance(B) > Performance(A) AND Performance(D) > Performance(C) with EH-3 criteria satisfied independently for both architectures.

**Statistical analysis:** Mixed-effects model across folds (fold as random effect). McNemar test for paired classification comparison. DeLong test for ROC-AUC comparison. Bonferroni/Holm correction for multiple comparisons.

---

## 5.2 Experiment 2 — Preprocessing Component Ablation

**Purpose:** Quantify the contribution of each preprocessing component to classification performance. Identifies which pipeline stages drive improvement.

**Dataset:** EyePACS

**Ablation configurations (5 levels):**

| Pipeline Configuration | Components Included |
| --- | --- |
| resize | Stage 1 only (FOV standardization) |
| resize + normalize | Stages 1 + 3 |
| resize + CLAHE | Stages 1 + 4 |
| resize + normalize + CLAHE | Stages 1 + 3 + 4 |
| full preprocessing pipeline | All 5 stages |

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
| Baseline | resize only |
| Proposed | resize + full preprocessing (all 5 stages) |

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

### V3 Experiment 3 (V3) — Cross-Dataset Generalization and Device Domain Shift

**V3 Experiment Number:** Experiment 3 (merged from old Experiments 5 + 6)

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

All primary metrics reported as **mean ± standard deviation** across 5-fold cross-validation.

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
* 5-fold cross-validation reporting (mean ± std) — All experiments
* Mixed-effects model for cross-fold analysis (fold as random effect) — Experiment 1
* Bonferroni/Holm correction for multiple comparisons — Experiments 1, 2

---

# 7. ABLATION PROTOCOL

To isolate driver of improvement (v2.1 Experiment 1 design):

| Configuration | Preprocessing | Architecture |
| --- | --- | --- |
| A | resize only | ResNet-50 |
| B | full preprocessing (all 5 components) | ResNet-50 |
| C | resize only | EfficientNet-B3 |
| D | full preprocessing (all 5 components) | EfficientNet-B3 |

**Dominance validation criterion (v2.1):** Preprocessing Dominance validated if:

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
* No patient overlap across splits (enforced by patient-level 5-fold CV)

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

* Formalization of preprocessing dominance hypothesis (validated via 2×2 factorial ablation on two established architectures)
* Threshold-controlled CLAHE validation within DR multi-class context (optimized clip limit in LAB color space)
* Unified ablation-driven causal validation
* Architecture constrained to resource-limited environments
* Cross-database transferability validation across 3+ independent datasets (Messidor, Messidor-2, IDRiD)
* Grad-CAM explainability with quantitative ALO (primary) and IoU (secondary) against pixel-level lesion masks (IDRiD)
* 5-component preprocessing pipeline with component-level ablation (Experiment 2)
* Device domain shift evaluation across 4 camera manufacturers (Canon, Topcon, Kowa, Zeiss)

---

# 11. DEFENSE-READY CLAIM MATRIX

| Claim | Validated By (V3) | V3 Status |
| --- | --- | --- |
| PC-1 | V3 Exp 1 (ResNet-50 + EfficientNet-B3) + EH-3 | Active |
| PC-2 | V3 Exp 2 curve (CLAHE threshold sensitivity on IDRiD) | Active |
| PC-3 (Two-Stage Fine-Tuning) | — | DEMOTED: Training strategy only; H-3 dropped |
| PC-4 | Mathematical derivation (laser-tissue model) | Secondary/supplementary |
| PC-5 | UML + system design | Secondary/supplementary |
| PC-6 | V3 Exp 3 generalization ratios (G = F1_external / F1_EyePACS) | Active (merged into Exp 3) |
| PC-7 | V3 Exp 4 Grad-CAM ALO (primary) + IoU (secondary) on IDRiD masks | Active |
| PC-8 | V3 Exp 2 component ablation (preprocessing component hierarchy) | Active |
| PC-9 | V3 Exp 3 cross-camera metrics (device domain shift robustness) | Active (merged into Exp 3) |
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
