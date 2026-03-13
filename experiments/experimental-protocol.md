# Experimental Protocol

Automated Diabetic Retinopathy Detection via Preprocessing and CNN Classification

**Document Version:** 3.0 — V3 sync: Experiment 3 (robustness/APTOS) DROPPED; old Experiments 5+6 MERGED into V3 Experiment 3; Experiment 7 → future work placeholder; formerly "dynamic clip limit" renamed to "optimized clip limit"; formerly "6-stage pipeline" reframed as "5-component pipeline".

---

## Research Objective

To evaluate whether preprocessing-based normalization of fundus images improves robustness of CNN-based diabetic retinopathy detection across imaging devices, illumination conditions, and noise levels, while preserving clinically relevant retinal features.

---

## Central Hypothesis

The proposed preprocessing pipeline reduces domain variability across fundus imaging devices and acquisition conditions while preserving diagnostically relevant retinal features, leading to improved CNN-based diabetic retinopathy detection. See `governance/HYPOTHESIS.md` for the full central hypothesis formulation and decomposition into H-1 through H-6.

---

## 1. Datasets

The study uses multiple publicly available retinal image datasets.

| Dataset               | Role                                                                              |
| --------------------- | --------------------------------------------------------------------------------- |
| EyePACS               | Primary training (V3 Experiments 1 and 2). ~35,126 labeled images (Kaggle labeled partition). |
| APTOS 2019            | [V3: NOT ACTIVE — old Experiment 3 (robustness under image degradation) is DROPPED in V3] |
| IDRiD                 | Clinical validation, CLAHE sweep, lesion localization (V3 Experiments 2, 3, 4)   |
| Messidor / Messidor-2 | External generalization (V3 Experiment 3)                                         |
| RFMiD / DDR / ODIR    | Device domain shift evaluation (V3 Experiment 3)                                  |

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

**Dataset:** EyePACS

Two architectures are evaluated:

* ResNet-50
* EfficientNet-B3

Four configurations are trained:

| Config | Preprocessing                   | CNN             |
| ------ | ------------------------------- | --------------- |
| A      | resize only                     | ResNet50        |
| B      | resize + proposed preprocessing | ResNet50        |
| C      | resize only                     | EfficientNet-B3 |
| D      | resize + proposed preprocessing | EfficientNet-B3 |

Statistical analysis:

* mixed-effects model across folds

Hypothesis:

\[
Performance_{preprocessing} > Performance_{baseline}
\]

---

# 5. Experiment 2 — Preprocessing Component Ablation

**Purpose:**
Quantify the contribution of each preprocessing component.

**Tests whether:** Individual preprocessing components contribute differentially to classification performance (H-1 decomposition).

Preprocessing pipeline consists of:

1. **FOV standardization**

   * fundus circle detection
   * black border removal
   * image centering
   * resize

2. **Green channel imaging**

3. **Normalization**

4. **CLAHE enhancement**

   * LAB color space
   * optimized clip limit (selected via parameter sweep in V3 Experiment 2; per DGL-5)

5. **HSV contrast enhancement**

Ablation configurations:

| Pipeline                    |
| --------------------------- |
| resize                      |
| resize + normalize          |
| resize + CLAHE              |
| resize + normalize + CLAHE  |
| full preprocessing pipeline |

Purpose: determine which components contribute most to performance.

---

<!-- DROPPED V3: Experiment 3 (Robustness to Image Degradation) is DROPPED in V3. Old Exp 3 tested robustness under Gaussian noise, blur, and low illumination using APTOS 2019. This experiment and APTOS 2019 are no longer active in V3. Historical content preserved below. -->

### DROPPED (V3): Old Experiment 3 — Robustness to Image Degradation

> **V3 NOTE:** This experiment is DROPPED in V3. The old Exp 3 (robustness under image degradation, using APTOS 2019) is not executed. APTOS 2019 is not an active V3 experimental dataset. Cross-device generalization is instead handled by V3 Experiment 3 (merged from old Exp 5+6). The content below is preserved for historical reference only.

**Purpose:**
Evaluate model robustness under degraded imaging conditions.

**Tests whether:** The preprocessing pipeline provides robustness to noise and illumination variation (H-1 extension).

**Dataset:** APTOS 2019

Image perturbations:

| Distortion       | Parameter            |
| ---------------- | -------------------- |
| Gaussian noise   | σ                    |
| Gaussian blur    | kernel size          |
| Low illumination | brightness reduction |

Noise levels:

* low
* medium
* high

Performance drop is measured relative to clean images.

---

## Clinical threshold experiment (DROPPED V3 — part of old Exp 3)

Binary classification:

* non-referable DR (0–1)
* referable DR (2–4)

Metrics:

* sensitivity
* specificity
* ROC-AUC

---

# 7. V3 Experiment 4 — Explainability Analysis

**Purpose:**
Determine whether preprocessing shifts CNN attention toward clinically relevant lesion regions.

**Tests whether:** Preprocessing directs CNN attention toward clinically relevant lesion regions, quantified by ALO and IoU (H-5).

**Model:** EfficientNet-B4

Images:

* 10 randomly sampled images per DR class from IDRiD (with lesion annotations)

Two pipelines:

| Pipeline | Description                 |
| -------- | --------------------------- |
| baseline | resize only                 |
| proposed | resize + full preprocessing |

Explainability method:

* Grad-CAM

Quantitative evaluation:

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
ALO_{preprocessing} > ALO_{baseline} \quad \text{(primary)}
\]
\[
IoU_{preprocessing} > IoU_{baseline} \quad \text{(secondary)}
\]

Lesion masks obtained from **IDRiD dataset**.

---

## 7.1 Lesion Alignment Analysis

To verify that preprocessing improves clinically relevant feature extraction, Grad-CAM attention maps are compared with lesion segmentation masks from IDRiD. This analysis is performed per lesion type (microaneurysms, hemorrhages, hard exudates, soft exudates) and produces:

* Per-lesion-type ALO scores for baseline vs. proposed preprocessing
* Per-lesion-type IoU scores for baseline vs. proposed preprocessing
* Visual overlays showing Grad-CAM activation relative to annotated lesion regions
* Statistical comparison (paired test across IDRiD images) for at least 3 of 4 lesion types

This subsection provides the quantitative bridge between "preprocessing improves classification" (PC-1) and "preprocessing improves attention to clinically relevant structures" (PC-7).

---

<!-- MERGED V3: Old Experiments 5 and 6 are MERGED into V3 Experiment 3 (Generalization + Device Robustness). Historical content preserved below. -->

# 8. V3 Experiment 3 — Cross-Dataset Generalization and Device Robustness (Merged from old Exp 5+6)

> **V3 NOTE:** Old Experiments 5 (Clinical Generalization) and 6 (Device Domain Shift) are MERGED into a single V3 Experiment 3. This combined experiment tests both H-4 (cross-database transferability) and H-6 (device robustness) in one experimental design.

**Purpose:**
Evaluate generalization to independent clinical datasets and robustness across imaging devices without retraining.

**Tests whether:** The preprocessing pipeline enables cross-database generalization (H-4) and reduces cross-device performance variance (H-6).

**Training dataset:** EyePACS (checkpoints from V3 Experiment 1)

**Testing datasets:**

| Dataset       | Role                        | Cameras                |
| ------------- | --------------------------- | ---------------------- |
| Messidor      | External generalization     | Topcon                 |
| Messidor-2    | External generalization     | Topcon                 |
| IDRiD         | External generalization     | Kowa                   |
| RFMiD         | Device domain shift         | Topcon, Kowa           |
| DDR           | Device domain shift         | Canon, Topcon          |
| ODIR-5K       | Device domain shift         | Canon, Zeiss           |

No retraining performed. Models evaluated in zero-shot transfer.

**Metrics:**
* Accuracy, Weighted F1, ROC-AUC (per dataset and per camera group)
* Generalization ratio G = F1_external / F1_EyePACS per OD-4 (H-4 criterion: G ≥ 0.85)
* Cross-device performance variance (H-6 criterion: lower variance for preprocessed models)

**Statistical analysis:** Bootstrap 95% CI across datasets; DeLong test for ROC-AUC comparison.

---

### DROPPED (V3): Old Experiment 5 — Clinical Generalization (historical reference)

> Subsumed into V3 Experiment 3 above.

Training dataset: EyePACS. Testing: Messidor, Messidor-2, IDRiD. No retraining. Metrics: Accuracy, Weighted F1, ROC-AUC.

---

### DROPPED (V3): Old Experiment 6 — Device Domain Shift (historical reference)

> Subsumed into V3 Experiment 3 above.

Tested H-6: preprocessing standardizes retinal image appearance and reduces distribution differences between camera devices. Datasets grouped by camera model. Evaluated device-induced distribution shift.

---

<!-- FUTURE WORK V3: Experiment 7 (Clinical Validation with Kazakh medical center data) is NOT an active V3 experiment. No Kazakh clinical data is available. This experiment is preserved as future work placeholder. -->

# 10. FUTURE WORK (V3): Old Experiment 7 — Clinical Validation (Dirty Data Pipeline)

> **V3 NOTE:** This experiment is NOT part of V3 active experiments. Kazakh clinical data is not yet available (no institutional agreements). This section is preserved as a future work placeholder per VCR-4 and NC-15. The dissertation references this as planned future work only.

**Purpose:**
Test the full 5-component preprocessing pipeline on clinical fundus images from Kazakh medical centers. These images represent "dirty data" — variable quality, non-standardized acquisition protocols, potential artifacts, and diverse camera hardware.

**Tests whether:** The preprocessing pipeline maintains effectiveness under real-world clinical imaging conditions outside of curated benchmark datasets.

**Dataset:** Clinical fundus images from Kazakh medical centers (access pending institutional agreements). **NOT AVAILABLE — future work only.**

**Protocol (future):**
1. Apply the full 5-component preprocessing pipeline (implemented as 6 ordered stages) to clinical images
2. Evaluate classification performance using the CNN model trained on EyePACS (no retraining)
3. Compare performance with and without preprocessing on the clinical images
4. Document image quality characteristics and preprocessing effects

**Metrics (future):**

* Accuracy, Weighted F1, ROC-AUC on clinical images
* ALO and IoU on images with available lesion annotations (if applicable)
* Qualitative assessment of preprocessing effects on clinical image characteristics

**Linkage:** Results would supplement PC-1 (preprocessing dominance under real-world conditions). Bounded per NC-15.

---

# 11. Image Quality Improvement Analysis

To quantify the effect of preprocessing, image quality metrics are calculated:

* Contrast-to-Noise Ratio (CNR)
* Vessel Visibility Index
* Image Entropy
* Structural Similarity Index (SSIM)

These metrics measure improvement in vascular feature visibility.

---

# 12. Argument Map

The experimental protocol is grounded in the following causal argument:

**Causal Chain 1 (Problem):**
Device variability → image distribution shift → degraded CNN performance

**Causal Chain 2 (Solution):**
Preprocessing pipeline → image normalization → improved feature visibility → improved CNN generalization

**Experiment-to-Argument Mapping:**

| Experiment | Tests | V3 Status |
|---|---|---|
| V3 Exp 1 | Preprocessing improves CNN performance (Chain 2, terminal node) — H-1 | ACTIVE |
| V3 Exp 2 | Which preprocessing components drive improvement; CLAHE threshold sensitivity (Chain 2, decomposition) — H-1, H-2 | ACTIVE |
| V3 Exp 3 | Cross-database generalization + cross-device generalization (merged) (Chain 2, generalization+device variability) — H-4, H-6 | ACTIVE (merged from old Exp 5+6) |
| V3 Exp 4 | Preprocessing directs attention to lesions, ALO primary (Chain 2, feature visibility node) — H-5 | ACTIVE |
| ~~Exp 3~~ | ~~Robustness to noise and illumination (Chain 1, resistance to variability)~~ | DROPPED V3 — old Exp 3 |
| ~~Exp 7~~ | ~~Clinical validation under real-world conditions (Chain 2, external validation)~~ | FUTURE WORK — no data available |
