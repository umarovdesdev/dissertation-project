# RESEARCH_ARCHITECTURE_MASTER.md

## Integrated Preprocessing–CNN Framework for Multi-Stage Diabetic Retinopathy Classification

**Candidate:** Yesmukhamedov N.S.
**Status:** Binding Methodological Blueprint
**Function:** Experimental, statistical, and architectural formalization of the dissertation research
**Version:** 5.2 | **Date:** 2026-05-28 | **Binding Reference:** INVARIANTS.md v5.2

**v5.2 Amendment:** RETFound's pretraining corpus is described as the multi-modal retinal imaging corpus on which the foundation model was actually pretrained per Zhou et al. 2023 — ≈904K color fundus photographs (CFP) + ≈736K OCT scans (~1.6M total). The V5 arm of Experiment 1 loads the CFP-pretrained RETFound checkpoint specifically (the OCT-pretrained checkpoint is published separately and is not used; the dissertation's inputs remain fundus-only per SB-1.4 in INVARIANTS.md). Section 4.2bis is updated accordingly. All other v5.1 provisions are retained.

**v5.1 Amendment:** The Experiment 1 factorial is amended so that the V5 arm uses RETFound (in-domain retinal pretrain) and the baseline arm retains ImageNet (cross-domain pretrain). Section 4 (Model Architecture Layer) and Section 5.1 (Experiment 1) reflect the amendment. The operational specifications listed under AOQ-1 through AOQ-4 (INVARIANTS v5.1, Section X) are open and must be resolved before experimental execution; cells marked "TBD per AOQ-x" in this document refer to those open questions.

---

# 1. RESEARCH LOGIC STRUCTURE

## 1.1 Central Causal Chain

V5 Preprocessing Pipeline (8-stage)
→ Improved Microvascular Feature Visibility (quantified via CNR, VVI, Entropy, SSIM)
→ Stabilized CNN Feature Extraction (validated via Grad-CAM ALO (primary) and IoU (secondary) with lesion masks)
→ Improved Multi-Class DR Classification (across multiple datasets and camera hardware)
→ Measurable Statistical Dominance (EH-3 criteria, independently for ResNet-50 and EfficientNet-B3)

Dominance is defined strictly per Invariants (Δ weighted F1 ≥ 5 pp; Δ ROC-AUC ≥ 0.02; no Cohen's Kappa degradation).

---

# 2. DATA ARCHITECTURE

## 2.1 Tiered Dataset Architecture

The dataset architecture comprises eight datasets organized into functional tiers: Training, External Generalization, Clinical Validation, and Device Domain Shift.

### 2.1.1 TRAINING Tier — EyePACS (Primary Training & Ablation)

* **Role:** Primary training dataset for Experiments 1, 2, 3, 4, 5, and 6
* **Approximate size:** ~35,126 labeled fundus images
* **Taxonomy:** Five-class DR staging (DR 0–4)
* **Camera models:** Canon CR-1
* **Public availability:** Yes (Kaggle)
* **Class imbalance:** Severe — must be documented and all performance claims interpreted in context of distributional asymmetry (per SB-2.1)

### 2.1.2 EXTERNAL Tier — APTOS 2019 (Cross-Dataset Transferability)

* **Role:** External test dataset for Experiment 3 — cross-dataset transferability (zero-shot transfer from EyePACS)
* **Approximate size:** ~3,662 labeled fundus images
* **Taxonomy:** Five-class DR staging (DR 0–4)
* **Camera models:** Mixed
* **Public availability:** Yes (Kaggle)

### 2.1.3 CLINICAL Tier — IDRiD (Clinical Validation + Lesion Localization)

* **Role:** Clinical validation dataset for Experiments 4 (quantitative explainability), 5 (clinical degradation), and 7 (training)
* **Approximate size:** 516 images (81 with pixel-level lesion annotations for four lesion types: microaneurysms, hemorrhages, hard exudates, soft exudates)
* **Taxonomy:** Five-class DR staging + pixel-level lesion masks
* **Camera models:** Kowa
* **Public availability:** Yes

### 2.1.4 EXTERNAL Tier — Messidor-2 (Clinical Degradation)

* **Role:** External evaluation for Experiment 5 — clinical degradation resistance
* **Approximate size:** ~1,748 images
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

### 2.1.8 CLINICAL Tier — Clinical (Kazakh Medical Center Validation)

* **Role:** Clinical validation dataset for Experiments 4 (qualitative Grad-CAM), 5 (clinical degradation, test), and 7 (held-out test)
* **Approximate size:** 60 images (30 patients × 2 eyes), balanced (12 per class)
* **Taxonomy:** Five-class DR staging (DR 0–4)
* **Camera models:** TBD
* **Public availability:** No (institutional agreement)
* **Format:** PNG

---

## 2.2 Split Strategy

All experiments use **5-fold cross-validation with patient-level stratified split** to prevent data leakage. For each fold iteration, 4 folds serve as training data and 1 fold as test data. The process is repeated 5 times. All metrics are reported as mean ± standard deviation across folds.

Patient-level leakage control is mandatory: no patient's images may appear in both training and test partitions within any fold.

---

## 2.3 Cross-Database Generalization

Cross-database generalization defined as:

G = F1_external / F1_EyePACS

where F1_EyePACS is the test-set F1-score on the primary training dataset (EyePACS) and F1_external is the F1-score on external datasets (APTOS 2019, IDRiD, Messidor-2, or domain shift datasets) under the same trained model without retraining. Bounded strictly per OD-4.

---

# 3. PREPROCESSING PIPELINE ARCHITECTURE

Defined per OD-3.

**Key Scientific Framing:** The preprocessing pipeline is defined as an integral component of the diagnostic model — Stage 1 of a two-stage system: `model = V5_preprocessing + CNN`. This is the central design decision of this work: preprocessing is not ancillary data preparation but defines the feature space available to the CNN.

## 3.1 V5 Ordered Pipeline (8-Stage System)

The V5 preprocessing pipeline comprises eight ordered stages. All stages are always on except Stage 6 (train only):

- **Stage 0: Canonical Flip** — Left-eye images are horizontally flipped to right-eye canonical orientation (OD right, macula left). Always on.
- **Stage 1: OD-Fovea Rotation Normalization** — Classical CV detection of OD (brightest region) and fovea (darkest region with distance prior); rotates image so OD→fovea axis is horizontal. Fallback: skip rotation on low confidence. Augmentation rotation σ is adaptive per-image from detection uncertainty (fallback σ = 13.0°). Always on.
- **Stage 2: FOV Crop + Isotropic Resize** — Foreground detection, crop to FOV region, isotropic scale to 512×512 with centered zero-padding preserving fundus circle geometry. Always on.
- **Stage 3: FOV Mask Generation** — Binary mask (1.0 = real fundus data, 0.0 = zero-padding) appended as 4th input channel. Always on.
- **Stage 4: Flat-Field Correction** — Gaussian blur subtraction (corrected = image − GaussianBlur(image, σ) + 128) with adaptive σ = 0.07 × D (D = FOV diameter in pixels from mask). Applied inside FOV mask only. Always on.
- **Stage 5: CLAHE** — Dual-constraint clip limit on LAB L-channel: CL = min(clip_factor × tile_area / 256, global_threshold × tile_area). Tile grid 8×8. Stochastic at train time (p = 0.8); deterministic at inference. Always on.
- **Stage 6: Augmentation** — Train only. Unified affine transform (rotation σ adaptive from Stage 1, zoom [0.9, 1.1], optional shear/stretch) + brightness/contrast + PCA color jitter. Applied before Stage 7 (operates on uint8).
- **Stage 7: Dataset-Specific Normalization** — ToTensor (HWC uint8 → CHW float32 [0,1]) then channel-wise (x − mean) / std using mean and std computed from EyePACS training set after Stages 0–4, using only pixels where FOV mask = 1.0. Output: float32 tensor of shape (4, 512, 512). Always on. Always last.

Pipeline **ACTIVE** (full V5): All 8 stages applied. Stage 6 active during training only. Output: 4-channel tensor (3 RGB + 1 FOV mask). Pipeline **ABSENT** (V5 baseline): Stretch-resize to 512×512 + ImageNet normalize (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]). Output: 3-channel tensor. No FOV mask. No preprocessing stages applied.

---

## 3.2 CLAHE Mathematical Formalization (V5)

V5 Dual-Constraint Clip Limit:

CL_tile = min(clip_factor × tile_area / 256, global_threshold × tile_area)

where clip_factor and global_threshold are tunable hyperparameters. Applied stochastically at train time (probability = 0.80); applied deterministically at inference time.

Transferability from STARE to EyePACS is NOT assumed (DGL-5). V5 clip limit parameters must be independently validated within the dissertation's experimental framework.

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
| Optimizer | Adam (lr=1e-4, weight_decay=1e-4) |
| Batch size | 16 |
| Maximum epochs | 20 (with early stopping, patience=5) |
| Loss function | Focal Loss (γ=2, α=inverse-frequency class weights) |
| Input resolution | 512×512 |
| Input channels | 3 (baseline) or 4 (full V5 with FOV mask) |
| Mixed precision (fp16) | Enabled for ResNet-50; DISABLED for EfficientNet (fp16 overflow fix) |
| Cross-validation | 5-fold, patient-level stratified split |
| Seed | 42, deterministic=true |

See `methods/implementation.md` for full implementation details.

---

## 4.1 ResNet-50 — Baseline Arm (v5.1)

* Pre-trained on **ImageNet** (IMAGENET1K_V2 weights via torchvision)
* Adapted via fine-tuning for 5-class DR classification
* Serves as a baseline-arm backbone in the v5.1 Experiment 1 factorial
* Represents the residual-connection architecture family
* Input: 3 channels (baseline configurations only)

---

## 4.2 EfficientNet-B3 — Baseline Arm (v5.1)

* Pre-trained on **ImageNet** (timm weights)
* Adapted via fine-tuning for 5-class DR classification
* Serves as a baseline-arm backbone in the v5.1 Experiment 1 factorial
* Represents the compound-scaling architecture family (EfficientNet)
* Input: 3 channels (baseline configurations only)

---

## 4.2bis RETFound — V5 Arm Pretraining Source (v5.2 — multi-modal corpus, CFP checkpoint loaded)

* Source: Zhou, Y., et al. (2023). *A foundation model for generalizable disease detection from retinal images.* Nature. Repository: `rmaphoh/RETFound_MAE`.
* Pretraining corpus (multi-modal, per Zhou et al. 2023): approximately 1.6M retinal images total, comprising:
  - ≈904K color fundus photographs (CFP) — produces the CFP-pretrained checkpoint.
  - ≈736K optical coherence tomography (OCT) scans — produces the OCT-pretrained checkpoint (published separately).
* Pretraining method: Masked Autoencoder (MAE) self-supervised learning. MAE masks 75% of input patches and reconstructs pixel content; the encoder learns retina-aware representations without supervision. Each modality is pretrained independently, yielding two separate checkpoints.
* Published architecture: ViT-Large (≈300M parameters), 16×16 patch size, 224×224 input resolution as released.
* **Checkpoint loaded in this dissertation (v5.2 binding):** the **CFP-pretrained** RETFound checkpoint. Justification: the V5 pipeline produces fundus-image tensors only; the OCT-pretrained checkpoint operates on single-channel OCT inputs and is not applicable here. The dissertation's input domain remains fundus photography (SB-1.4 in INVARIANTS.md unchanged).
* Role in v5.2: Initialization source for the V5 arm of Experiment 1, paired with the full V5 preprocessing pipeline (4 channels, 512×512). The multi-modal corpus description characterizes RETFound at the publication level; it does not extend the dissertation's operational input modality.
* Open operational questions (binding, must be resolved before Experiment 1 execution):
  - **AOQ-1 (backbone choice):** Whether the V5 arm uses (a) RETFound ViT-Large directly, (b) a CNN-compatible domain-adaptive pretraining protocol (SparK-style MIM or SimCLR/MoCo on EyePACS) labeled "RETFound-style," or (c) both V5+RETFound and V5+ImageNet runs for partial factor decomposition. See INVARIANTS v5.1 Section X.
  - **AOQ-2 (4-channel adaptation):** Whether the FOV mask channel is (a) added at the input via patch-embed/conv-stem extension with mean-init of channel 3, (b) dropped from the V5-arm input, or (c) injected at an intermediate layer as a gating mask.
  - **AOQ-3 (license):** Verification that RETFound weights' license terms (CC BY-NC 4.0 at last check) permit the intended downstream use.
  - **AOQ-4 (factorial symmetry):** Whether the baseline arm retains both ResNet-50 and EfficientNet-B3 (asymmetric 2×1 vs 1×1 factorial) or is reduced to a single backbone matched to the V5-arm backbone family for symmetric comparison.

The replication test across architecture families that v5.0 established via ResNet-50 + EfficientNet-B3 under fixed ImageNet pretrain is **suspended** under v5.1. EH-4 replication satisfaction in v5.1 must be re-derived after AOQ-1 and AOQ-4 are resolved.

---

## 4.3 Transfer Learning Layer

### EfficientNetB0 — Two-Stage Fine-Tuning Protocol

Backbone: EfficientNetB0 (ImageNet pre-trained)

Two strategies (used as training methods):

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

# 5. EXPERIMENTAL DESIGN

## 5.0 Cross-Validation Protocol (Applies to All Experiments)

All experiments use 5-fold cross-validation with patient-level stratified split. For each fold iteration, 4 folds serve as training data and 1 fold as test data. The process is repeated 5 times. All metrics are reported as mean ± standard deviation across folds.

---

## 5.1 Experiment 1 — Causal Improvement (Preprocessing vs. Architecture)

**Purpose [v5.1 amended]:** Determine whether the integrated configuration (V5 preprocessing + RETFound in-domain pretrain) outperforms the baseline configuration (stretch-resize + ImageNet pretrain) as a unitary system. This is the primary experiment validating H-1 v5.1 and promoting PC-1.

**Dataset:** EyePACS

**Design (v5.1):** Configurations are indexed by *(preprocessing, pretraining source)* pairs. The architecture used in each cell is bound by AOQ-1 and AOQ-4 (INVARIANTS v5.1 Section X) and is not yet finalized.

| Config | Preprocessing | Pretraining source | Backbone | Input channels |
| --- | --- | --- | --- | --- |
| A | baseline (stretch-resize + ImageNet norm) | ImageNet | ResNet-50 | 3 |
| C | baseline (stretch-resize + ImageNet norm) | ImageNet | EfficientNet-B3 | 3 |
| B' | full V5 pipeline | **RETFound** | TBD per AOQ-1 (ViT-Large or CNN-compatible RETFound-style) | 4 (subject to AOQ-2) |

The v5.0 designations B (V5 + ResNet-50 + ImageNet) and D (V5 + EfficientNet-B3 + ImageNet) are **retired** under v5.1. Config B' replaces both. If AOQ-1 resolves to option (c) (run both V5 + RETFound and V5 + ImageNet), the v5.0 B and D configurations are reinstated as auxiliary cells for factor decomposition.

**Dominance validation (v5.1):** Integrated Pipeline Dominance is validated if Performance(B') > max(Performance(A), Performance(C)) with EH-3 criteria satisfied. Attribution of the observed effect to preprocessing alone, pretraining alone, or their interaction is forbidden under CFC-2.8 (INVARIANTS v5.1).

**Config N (normalization control) — retained from v5.0:** Baseline preprocessing + dataset-specific normalization (no V5 pipeline stages). Continues to isolate the normalization statistics effect from other pipeline contributions, with the understanding that under v5.1 the V5 arm now also differs in pretrain source.

**Known limitations (v5.1):**
- The measured H-1 effect conflates (i) preprocessing pipeline stages, (ii) normalization statistics change, and (iii) pretraining source change. No single-factor attribution is recoverable from Config A/C vs Config B' alone.
- If AOQ-1 resolves to option (a) (ViT-Large) and AOQ-4 retains both ResNet-50 and EfficientNet-B3 in the baseline, the comparison further confounds architecture family. A symmetric design requires either reducing the baseline to one architecture or resolving AOQ-1 to option (c).

**Statistical analysis:** Mixed-effects model across folds (fold as random effect). McNemar test for paired classification comparison. DeLong test for ROC-AUC comparison. Bonferroni/Holm correction for multiple comparisons.

---

## 5.2 Experiment 2 — Preprocessing Component Ablation

**Purpose:** Quantify the contribution of each preprocessing component to classification performance. Identifies which pipeline stages drive improvement.

**Dataset:** EyePACS

**Architecture:** Best-performing from Experiment 1 (EfficientNet-B3 per preliminary results). Single architecture is sufficient — ablation quantifies stage contributions rather than architecture sensitivity.

**V5 Ablation configurations (7 levels):**

| Level | Pipeline Configuration | Stages Included |
| --- | --- | --- |
| 0 | baseline | stretch-resize + ImageNet normalize (3ch, no FOV mask) |
| 1 | baseline + flip | Stage 0 + stretch-resize + ImageNet norm |
| 2 | +rotation | Stages 0–1 + stretch-resize + ImageNet norm |
| 3 | +isotropic + mask | Stages 0–3 + Stage 7 (dataset-specific norm) |
| 4 | +flat-field | Stages 0–4 + Stage 7 |
| 5 | +CLAHE | Stages 0–5 + Stage 7 |
| 6 | full V5 pipeline | All Stages 0–7 |

**CLAHE parameter sweep:** clip_factor and global_threshold varied on EyePACS to identify sensitivity profile with local optimum (H-2). Stochastic application at 80% train probability.

**Flat-field σ sweep:** σ factor swept from 0.05·D to 0.10·D on EyePACS to characterize illumination normalization sensitivity.

**Metrics:** Primary metrics (Weighted F1, ROC-AUC, Cohen's Kappa, Accuracy) plus image quality metrics (CNR, VVI, Entropy, SSIM) measured at each pipeline stage.

**Statistical analysis:** Bonferroni/Holm correction for multiple comparisons across ablation levels.

---

## 5.3 Experiment 3 — Cross-Dataset Transferability

**Purpose:** Evaluate whether models trained on EyePACS with the V5 pipeline transfer to an independent dataset without retraining.

**Dataset:** Train on EyePACS, evaluate on APTOS 2019 (zero-shot, no retraining).

**Hypothesis tested:** H-4

**Metric:** Generalization ratio G = F1_APTOS / F1_EyePACS. Pre-registered success criterion: G ≥ 0.85.

**Protocol:** Best model from Experiment 1 (config B or D, whichever achieves higher EyePACS F1) is applied to APTOS 2019 test images with no weight updates. F1, AUC, κ reported.

---

## 5.4 Experiment 4 — Explainability Analysis (Grad-CAM / ALO)

**Experiment Number:** 4

**Purpose:** Determine whether preprocessing shifts CNN attention toward clinically relevant lesion regions. Closes the evidential gap in the causal chain: Preprocessing → Improved Feature Visibility → Improved Classification.

**Model:** EfficientNet-B4

**Sampling:** 10 randomly selected images per DR class (50 total). Two pipelines compared:

| Pipeline | Description |
| --- | --- |
| Baseline | stretch-resize + ImageNet normalize only (3ch, no FOV mask) |
| Proposed | full V5 pipeline (all 8 stages, 4ch) |

**Explainability method:** Grad-CAM (Gradient-weighted Class Activation Mapping).

**Quantitative evaluation (IDRiD):** Attention–Lesion Overlap (ALO, primary) and Intersection-over-Union (IoU, secondary) between Grad-CAM activation regions and pixel-level lesion masks from the IDRiD dataset. Four lesion types: microaneurysms, hemorrhages, hard exudates, soft exudates.

**Qualitative evaluation (Clinical):** Grad-CAM overlays generated for Clinical dataset images as qualitative evidence only (no lesion masks available). 10 images per DR class.

**Hypothesis:** ALO(preprocessing) > ALO(baseline) (primary), IoU(preprocessing) > IoU(baseline) (secondary), demonstrating that preprocessing directs model attention to clinically relevant structures.

**Deliverables:**

* Grad-CAM overlays for representative images from each DR class (0–4) — with vs. without preprocessing (IDRiD)
* ALO scores (primary) and IoU scores (secondary) between Grad-CAM activations and IDRiD pixel-level lesion masks (per lesion type)
* Qualitative Grad-CAM overlays on Clinical dataset images for visual validation

---

## 5.5 Experiment 5 — Clinical Degradation Resistance

**Purpose:** Quantify whether V5 preprocessing reduces the performance drop between EyePACS validation and external clinical datasets.

**Hypothesis tested:** H-7

**Training:** EyePACS (5-fold CV). Evaluation on IDRiD and Messidor-2.

**Protocol:** For each architecture × preprocessing combination (baseline vs V5), compute:
- F1_val = weighted F1 on EyePACS validation fold
- F1_ext = weighted F1 on external dataset (IDRiD or Messidor-2)
- Δ = F1_val − F1_ext

**Success criterion:** Δ_V5 < Δ_baseline with statistical significance (paired test across folds).

---

## 5.6 Experiment 6 — Device Domain Shift

**Purpose:** Evaluate whether V5 preprocessing maintains classification performance across images from different fundus camera manufacturers.

**Hypothesis tested:** H-6

**Training:** EyePACS (Canon CR-1). Evaluation on DDR (Canon, Topcon), ODIR-5K (Canon, Zeiss), RFMiD (Topcon, Kowa).

**Protocol:** DR-labeled images only; non-DR disease labels are excluded or mapped to non-DR category. F1 and AUC computed per camera group. Cross-device performance variance reported.

**Deliverables:** Cross-device performance matrix; camera-group F1/AUC bar charts.

---

## 5.7 Experiment 7 — Small Data Training

**Purpose:** Evaluate trainability of the V5 pipeline on a small clinical dataset.

**Training:** IDRiD (516 images), 5-fold cross-validation. Clinical dataset (60 images) held out as test.

**Protocol:** Train on IDRiD folds, evaluate on Clinical held-out. Report mean ± std across 5 folds. Both baseline and V5 preprocessing tested.

**Bootstrap requirement:** Bootstrap CI (≥ 1000 resamples) required given small dataset sizes (IDRiD=516, Clinical=60). See §6.8.

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

Reported for Experiments 1, 3, and 5.

---

## 6.4 Calibration Metrics

* Expected Calibration Error (ECE)
* Brier Score

Reported for Experiments 1 and 3.

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

Per OD-4. Reported for Experiment 3.

---

## 6.8 Statistical Tests

Mandatory:

* McNemar test (paired classification comparison) — Experiments 1
* DeLong test (ROC-AUC comparison) — Experiments 1 and 3
* 95% confidence intervals (bootstrap ≥ 1000 iterations) — All experiments
* 5-fold cross-validation reporting (mean ± std) — All experiments
* Mixed-effects model for cross-fold analysis (fold as random effect) — Experiment 1
* Bonferroni/Holm correction for multiple comparisons — Experiments 1, 2

---

# 7. ABLATION PROTOCOL [v5.1 amended]

Integrated Pipeline Dominance (Experiment 1 v5.1 design):

| Config | Preprocessing | Pretraining source | Backbone | Input channels |
| --- | --- | --- | --- | --- |
| A | baseline (stretch-resize + ImageNet norm) | ImageNet | ResNet-50 | 3 |
| C | baseline (stretch-resize + ImageNet norm) | ImageNet | EfficientNet-B3 | 3 |
| B' | full V5 pipeline | RETFound (resolution per AOQ-1) | TBD per AOQ-1 | 4 (per AOQ-2) |

**Dominance validation criterion (v5.1):** Integrated Pipeline Dominance is validated if:

* Performance(B') > max(Performance(A), Performance(C))

with EH-3 criteria (Δ weighted F1 ≥ 5 pp; Δ ROC-AUC ≥ 0.02; no Cohen's Kappa degradation) satisfied. Per CFC-2.8 (INVARIANTS v5.1), the attribution of the difference to preprocessing alone is forbidden — the dominance claim is over the integrated *(preprocessing, pretrain)* pair only.

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

* 8-stage V5 preprocessing pipeline with FOV mask as explicit stage (Stage 3), adaptive flat-field correction (σ proportional to FOV diameter), dataset-specific normalization, and canonical orientation via OD-fovea rotation normalization
* Formalization of preprocessing dominance hypothesis (validated via 2×2 factorial ablation on two established architectures, 4 configurations A–D)
* Dual-constraint stochastic CLAHE validation within DR multi-class context (LAB color space, dual-constraint clip limit, 80% train-time probability)
* Adaptive flat-field correction (σ = 0.07 × FOV diameter) scaling with per-image geometry
* Dataset-specific channel-wise normalization computed from training set mask=1.0 pixels
* Isotropic resize with centered zero-padding preserving fundus circle geometry
* V5 component ablation (7 levels: baseline → +flip → +rotation → +isotropic+mask → +flat-field → +CLAHE → full V5)
* Cross-dataset transferability validation on APTOS 2019 (G ≥ 0.85, zero-shot)
* Grad-CAM explainability with quantitative ALO (primary) and IoU (secondary) against pixel-level lesion masks (IDRiD) and qualitative overlays (Clinical)
* H-7 clinical degradation resistance — preprocessing reduces Δ = F1_val − F1_ext on IDRiD and Messidor-2
* Device domain shift evaluation across 4 camera manufacturers (Canon, Topcon, Kowa, Zeiss) on DDR, ODIR-5K, RFMiD
* Architecture constrained to resource-limited environments

---

# 11. DEFENSE-READY CLAIM MATRIX

| Claim | Validated By | Status |
| --- | --- | --- |
| PC-1 | Exp 1 (2×2 factorial A–D, ResNet-50 + EfficientNet-B3) + EH-3 | Active |
| PC-2 | Exp 2 CLAHE dual-constraint sweep + flat-field σ sweep on EyePACS | Active |
| PC-4 | Mathematical derivation (laser-tissue model) | Secondary/supplementary |
| PC-5 | UML + system design | Secondary/supplementary |
| PC-6 | Exp 3 generalization ratio G = F1_APTOS / F1_EyePACS (APTOS 2019) | Active |
| PC-7 | Exp 4 Grad-CAM ALO (primary) + IoU (secondary) on IDRiD; qualitative on Clinical | Active |
| PC-8 | Exp 2 component ablation (7 V5 levels: baseline → +flip → +rotation → +isotropic+mask → +flat-field → +CLAHE → full V5) | Active |
| PC-9 | Exp 6 cross-camera metrics (device domain shift across Canon, Topcon, Kowa, Zeiss on DDR, ODIR-5K, RFMiD) | Active |
| PC-10 | Exp 5 clinical degradation resistance (Δ comparison on IDRiD and Messidor-2, H-7) | Active |

Mapped to ARGUMENT_MAP.

---

# 12. FUNCTION OF THIS DOCUMENT

This file is:

* The methodological backbone of Chapter 2
* The execution blueprint for Chapter 4
* The validation structure for Chapter 5
* The defense shield during committee questioning

---
