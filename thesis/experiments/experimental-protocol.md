# Experimental Protocol

Automated Diabetic Retinopathy Detection via Preprocessing and CNN Classification

**Version:** 5.0 | **Date:** 2026-04-XX

---

## Research Objective

To evaluate whether preprocessing-based normalization of fundus images improves robustness of CNN-based diabetic retinopathy detection across imaging devices, illumination conditions, and noise levels, while preserving clinically relevant retinal features.

---

## Central Hypothesis

The proposed preprocessing pipeline reduces domain variability across fundus imaging devices and acquisition conditions while preserving diagnostically relevant retinal features, leading to improved CNN-based diabetic retinopathy detection. See `governance/HYPOTHESIS.md` for the full central hypothesis formulation and decomposition into H-1, H-2, H-4, H-5, H-6, and H-7.

---

## 1. Datasets

The study uses eight publicly available or institutionally accessible retinal image datasets.

| Dataset               | ~Images | Classes | Camera | Experiments |
| --------------------- | ------- | ------- | ------ | ----------- |
| EyePACS               | ~35,126 | 5-class (DR 0–4) | Canon CR-1 | 1, 2, 3, 4, 5, 6 |
| APTOS 2019            | ~3,662  | 5-class | Mixed | 3 |
| IDRiD                 | 516     | 5-class + lesion masks | Kowa | 4, 5, 7 (train) |
| Messidor-2            | ~1,748  | Referable/non-referable | Topcon | 5 |
| DDR                   | ~13,673 | 5-class | Canon, Topcon | 6 |
| ODIR-5K               | ~5,000 bilateral | Multi-disease → DR subset | Canon, Zeiss | 6 |
| RFMiD                 | ~3,200  | Binary DR | Topcon, Kowa | 6 |
| Clinical (Kazakh)     | 60 (30 patients × 2 eyes) | 5-class balanced (12/class) | TBD | 4, 5, 7 (test) |

---

# 2. Cross-Validation Protocol

To ensure robustness of the results, **5-fold cross-validation with patient-level split** is used.

Procedure:

1. Dataset divided into **5 folds**.
2. For each iteration:

   * **4 folds → training**
   * **1 fold → test**
3. Process repeated **5 times**.
4. Final metrics reported as:

\[
mean \pm std
\]

This reduces variance due to random data splits.

---

# 3. Evaluation Metrics

## 3.1 Primary performance metrics

* ROC-AUC
* Weighted F1-score
* Quadratic Cohen's Kappa
* Accuracy

These are standard metrics for DR severity grading.

---

## 3.2 Clinical metrics

Evaluation for **referable diabetic retinopathy (DR ≥ 2)**:

* Sensitivity
* Specificity
* Positive Predictive Value (PPV)
* Negative Predictive Value (NPV)

These metrics correspond to clinical screening requirements.

---

## 3.3 Calibration metrics

To evaluate probability calibration:

* Expected Calibration Error (ECE)
* Brier Score

Calibration curves are also generated.

---

## 3.4 Explainability metrics

* **ALO (Attention–Lesion Overlap)** — Primary explainability metric: `ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask)`. Measures what fraction of the lesion is covered by model attention. Clinically relevant — directly answers "Does the model attend to the lesion?"
* **IoU (Intersection-over-Union)** — Secondary explainability metric: `IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask)`. Measures symmetric spatial precision of attention overlap.
* Attention consistency score

---

## 3.5 Computational metrics

To evaluate computational efficiency:

* training time
* inference latency
* GPU memory usage
* parameter count

---

## 3.6 Statistical validation

Statistical significance is evaluated using:

* **McNemar test** – classification comparison
* **DeLong test** – ROC-AUC comparison
* **Bootstrap confidence intervals (95%)**

---

# 4. Experiment 1 — Causal Improvement (Preprocessing vs Architecture)

**Purpose:**
Determine whether preprocessing improves classification independently of CNN architecture.

**Tests whether:** Preprocessing improves CNN performance independently of architecture (H-1).

**Dataset:** EyePACS (~35,126 images, 5-fold CV)

Two architectures are evaluated:

* ResNet-50
* EfficientNet-B3

Four configurations (2×2 factorial design):

| Config | Preprocessing                                      | CNN             | Input channels |
| ------ | -------------------------------------------------- | --------------- | -------------- |
| A      | baseline (stretch-resize + ImageNet normalize)     | ResNet-50       | 3 |
| B      | full pipeline                                   | ResNet-50       | 4 |
| C      | baseline (stretch-resize + ImageNet normalize)     | EfficientNet-B3 | 3 |
| D      | full pipeline                                   | EfficientNet-B3 | 4 |

**Baseline:** stretch-resize to 512×512 + ImageNet normalize only, no FOV mask, 3-channel input.
**Full pipeline:** all 8 stages, dataset-specific normalization, FOV mask as 4th channel, 4-channel input.

Statistical analysis:

* mixed-effects model across folds

Hypothesis:

\[
Performance_{integrated} > Performance_{baseline}
\]

independently for both ResNet-50 and EfficientNet-B3. EH-3 dominance criterion: ΔF1 ≥ 5 pp, ΔAUC ≥ 0.02, no Cohen's Kappa degradation.

---

# 5. Experiment 2 — Preprocessing Component Ablation

**Purpose:**
Quantify the contribution of each preprocessing component.

**Tests whether:** Individual preprocessing components contribute differentially to classification performance (H-1 decomposition, H-2).

**Dataset:** EyePACS

**Ablation (7 levels):**

| Level | Pipeline Configuration | Stages | Input channels |
| ----- | ---------------------- | ------ | -------------- |
| 0 | baseline | stretch-resize + ImageNet normalize | 3 |
| 1 | +canonical flip | Stage 0 | 3 |
| 2 | +OD-fovea rotation | Stages 0–1 | 3 |
| 3 | +isotropic resize + FOV mask | Stages 0–3 + Stage 7 | 4 |
| 4 | +flat-field correction | Stages 0–4 + Stage 7 | 4 |
| 5 | +CLAHE | Stages 0–5 + Stage 7 | 4 |
| 6 | full pipeline | All Stages 0–7 | 4 |

**CLAHE parameter sweep (H-2):** clip_factor and global_threshold varied on EyePACS. Stochastic application at 80% train probability. Objective: identify sensitivity profile with local optimum in per-class F1 for DR 1 and DR 2.

**Flat-field σ sweep:** σ factor swept from 0.05·D to 0.10·D on EyePACS to characterize illumination normalization sensitivity.

**Metrics:** Primary metrics (Weighted F1, ROC-AUC, Cohen's Kappa, Accuracy) plus image quality metrics (CNR, VVI, Entropy, SSIM) measured at each ablation level.

---

# 6. Experiment 3 — Cross-Dataset Transferability

**Purpose:**
Evaluate whether models trained on EyePACS with the pipeline transfer to APTOS 2019 without retraining.

**Tests whether:** The preprocessing pipeline enables cross-dataset generalization without retraining (H-4).

**Training dataset:** EyePACS (best model from Experiment 1, config B or D)

**Test dataset:** APTOS 2019 (zero-shot, no retraining)

**Metrics:**
* Accuracy, Weighted F1, ROC-AUC
* Generalization ratio G = F1_APTOS / F1_EyePACS (H-4 criterion: G ≥ 0.85)

**Statistical analysis:** Bootstrap 95% CI; DeLong test for ROC-AUC comparison.

---

# 7. Experiment 4 — Explainability Analysis (Grad-CAM / ALO)

**Purpose:**
Determine whether preprocessing shifts CNN attention toward clinically relevant lesion regions.

**Tests whether:** Preprocessing directs CNN attention toward clinically relevant lesion regions, quantified by ALO and IoU (H-5).

**Model:** EfficientNet-B4

**Sampling:** 10 randomly selected images per DR class (50 total) from IDRiD (with lesion annotations). Clinical dataset for qualitative overlays.

Two pipelines:

| Pipeline | Description                                         |
| -------- | --------------------------------------------------- |
| Baseline | stretch-resize + ImageNet normalize (3ch, no FOV mask) |
| Proposed | full pipeline (all 8 stages, 4ch) |

**Explainability method:** Grad-CAM (Gradient-weighted Class Activation Mapping).

**Quantitative evaluation (IDRiD):**

**Primary metric — Attention–Lesion Overlap (ALO):**

\[
ALO = \frac{area(GradCAM \cap lesion\_mask)}{area(lesion\_mask)}
\]

**Secondary metric — Intersection-over-Union (IoU):**

\[
IoU = \frac{area(GradCAM \cap lesion\_mask)}{area(GradCAM \cup lesion\_mask)}
\]

Hypothesis:

\[
ALO_{integrated} > ALO_{baseline} \quad \text{(primary)}
\]
\[
IoU_{integrated} > IoU_{baseline} \quad \text{(secondary)}
\]

Lesion masks from **IDRiD dataset** (microaneurysms, hemorrhages, hard exudates, soft exudates).

**Qualitative evaluation (Clinical dataset):** Grad-CAM overlays generated for Clinical dataset images as qualitative evidence only. No lesion masks available; visual interpretation only.

---

## 7.1 Lesion Alignment Analysis

Per-lesion-type ALO and IoU scores computed on IDRiD for baseline vs. proposed preprocessing. Visual overlays showing Grad-CAM activation relative to annotated lesion regions. Statistical comparison (paired test across IDRiD images) for at least 3 of 4 lesion types.

---

# 8. Experiment 5 — Clinical Degradation Resistance

**Purpose:**
Quantify whether preprocessing reduces the performance drop between EyePACS validation and external clinical datasets.

**Tests whether:** Preprocessing reduces cross-dataset performance degradation (H-7).

**Training dataset:** EyePACS (5-fold CV)

**Evaluation datasets:** IDRiD, Messidor-2

**Protocol:** For each architecture (ResNet-50, EfficientNet-B3) × preprocessing (baseline vs integrated), compute:
- F1_val = weighted F1 on EyePACS validation fold
- F1_ext = weighted F1 on external dataset (IDRiD or Messidor-2)
- Δ = F1_val − F1_ext

**Success criterion:** Δ_integrated < Δ_baseline with statistical significance (paired test across 5-fold CV results).

---

# 9. Experiment 6 — Device Domain Shift

**Purpose:**
Evaluate classification robustness across images from different fundus camera manufacturers without retraining.

**Tests whether:** The preprocessing pipeline reduces cross-device performance variance (H-6).

**Training dataset:** EyePACS (checkpoints from Experiment 1)

**Testing datasets:**

| Dataset       | Role                        | Cameras                |
| ------------- | --------------------------- | ---------------------- |
| DDR           | Device domain shift         | Canon, Topcon          |
| ODIR-5K       | Device domain shift         | Canon, Zeiss           |
| RFMiD         | Device domain shift         | Topcon, Kowa           |

DR labels only; non-DR disease labels are excluded or mapped to non-DR category.

**Metrics:**
* Accuracy, Weighted F1, ROC-AUC per camera group
* Cross-device performance variance

**Statistical analysis:** Bootstrap 95% CI across camera groups; DeLong test for ROC-AUC comparison.

---

# 10. Experiment 7 — Small Data Training (IDRiD → Clinical)

**Purpose:**
Evaluate trainability of the pipeline on a small clinical dataset.

**Training dataset:** IDRiD (516 images), 5-fold cross-validation.

**Test dataset:** Clinical (60 images, held-out).

**Protocol:** Train on IDRiD folds, evaluate on Clinical held-out. Report mean ± std across 5 folds. Both baseline (3ch) and integrated (4ch) preprocessing tested.

**Metrics:** Accuracy, Weighted F1, ROC-AUC on Clinical images.

---

# 11. Image Quality Improvement Analysis

To quantify the effect of preprocessing, image quality metrics are calculated:

* Contrast-to-Noise Ratio (CNR)
* Vessel Visibility Index
* Image Entropy
* Structural Similarity Index (SSIM)

These metrics measure improvement in vascular feature visibility. Reported for Experiment 2.

---

# 12. Argument Map

The experimental protocol is grounded in the following causal argument:

**Causal Chain 1 (Problem):**
Device variability → image distribution shift → degraded CNN performance

**Causal Chain 2 (Solution):**
preprocessing pipeline → image normalization → improved feature visibility → improved CNN generalization

**Experiment-to-Argument Mapping:**

| Experiment | Tests | Hypothesis | Status |
|---|---|---|---|
| Exp 1 | Preprocessing improves CNN performance (2×2 factorial A–D) | H-1 | ACTIVE |
| Exp 2 | Which stages contribute most; CLAHE + flat-field σ sweep | H-1, H-2 | ACTIVE |
| Exp 3 | Cross-dataset transferability to APTOS 2019 (G ≥ 0.85) | H-4 | ACTIVE |
| Exp 4 | Preprocessing directs attention to lesions (ALO primary; Clinical qualitative) | H-5 | ACTIVE |
| Exp 5 | Clinical degradation resistance (Δ comparison IDRiD + Messidor-2) | H-7 | ACTIVE |
| Exp 6 | Cross-device generalization (DDR, ODIR-5K, RFMiD) | H-6 | ACTIVE |
| Exp 7 | Small data trainability (IDRiD → Clinical) | — | ACTIVE |
