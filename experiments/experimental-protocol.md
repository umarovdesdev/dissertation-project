# Experimental Protocol

Automated Diabetic Retinopathy Detection via Preprocessing and CNN Classification

---

## Research Objective

To evaluate whether preprocessing-based normalization of fundus images improves robustness of CNN-based diabetic retinopathy detection across imaging devices, illumination conditions, and noise levels, while preserving clinically relevant retinal features.

---

## Central Hypothesis

The proposed preprocessing pipeline reduces domain variability across fundus imaging devices and acquisition conditions while preserving diagnostically relevant retinal features, leading to improved CNN-based diabetic retinopathy detection. See `governance/HYPOTHESIS.md` for the full central hypothesis formulation and decomposition into H-1 through H-6.

---

## 1. Datasets

The study uses multiple publicly available retinal image datasets.

| Dataset               | Role                                        |
| --------------------- | ------------------------------------------- |
| EyePACS               | Primary training and ablation experiments   |
| APTOS 2019            | Robustness experiments                      |
| IDRiD                 | Clinical validation and lesion localization |
| Messidor / Messidor-2 | External generalization                     |
| RFMiD / DDR / ODIR    | Device domain shift evaluation              |

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
   * dynamic clip limit

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

# 6. Experiment 3 — Robustness to Image Degradation

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

## Clinical threshold experiment

Binary classification:

* non-referable DR (0–1)
* referable DR (2–4)

Metrics:

* sensitivity
* specificity
* ROC-AUC

---

# 7. Experiment 4 — Explainability Analysis

**Purpose:**
Determine whether preprocessing shifts CNN attention toward clinically relevant lesion regions.

**Tests whether:** Preprocessing directs CNN attention toward clinically relevant lesion regions, quantified by ALO and IoU (H-5).

**Model:** EfficientNet-B4

Images:

* 10 randomly sampled images per DR class
* additional degraded images

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

# 8. Experiment 5 — Clinical Generalization

**Purpose:**
Evaluate generalization to independent clinical datasets.

**Tests whether:** The preprocessing pipeline enables cross-database generalization without retraining (H-4).

Training dataset:

* EyePACS

Testing datasets:

* Messidor
* Messidor-2
* IDRiD

No retraining is performed.

Metrics:

* Accuracy
* Weighted F1
* ROC-AUC

---

# 9. Experiment 6 — Device Domain Shift

**Purpose:**
Evaluate robustness to images captured by different fundus cameras.

**Tests whether:** Preprocessing standardizes retinal image appearance and reduces distribution differences between camera devices, leading to improved cross-device generalization (H-6).

**Hypothesis:** Preprocessing standardizes retinal image appearance and reduces distribution differences between camera devices, leading to improved cross-device generalization. Models with preprocessing will exhibit lower cross-device performance variance than models without preprocessing.

Datasets and devices:

| Dataset  | Cameras       |
| -------- | ------------- |
| RFMiD    | Topcon, Kowa  |
| DDR      | Canon, Topcon |
| EyePACS  | Canon CR-1    |
| ODIR-5K  | Canon, Zeiss  |
| IDRiD    | Kowa          |
| Messidor | Topcon        |

Dataset subsets are grouped by camera model.

Performance comparison across domains evaluates **device-induced distribution shift**.

Metrics:

* Accuracy
* F1-score
* ROC-AUC

---

# 10. Experiment 7 — Clinical Validation (Dirty Data Pipeline)

**Purpose:**
Test the full preprocessing pipeline on clinical fundus images from Kazakh medical centers. These images represent "dirty data" — variable quality, non-standardized acquisition protocols, potential artifacts, and diverse camera hardware.

**Tests whether:** The preprocessing pipeline maintains effectiveness under real-world clinical imaging conditions outside of curated benchmark datasets.

**Dataset:** Clinical fundus images from Kazakh medical centers (access pending institutional agreements).

**Protocol:**
1. Apply the full 6-stage preprocessing pipeline to clinical images
2. Evaluate classification performance using the CNN model trained on EyePACS (no retraining)
3. Compare performance with and without preprocessing on the clinical images
4. Document image quality characteristics and preprocessing effects

**Metrics:**

* Accuracy, Weighted F1, ROC-AUC on clinical images
* ALO and IoU on images with available lesion annotations (if applicable)
* Qualitative assessment of preprocessing effects on clinical image characteristics

**Linkage:** Results supplement PC-1 (preprocessing dominance under real-world conditions). Bounded per NC-15 (validation is specific to the tested clinical data source).

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

| Experiment | Tests |
|---|---|
| Exp 1 | Preprocessing improves CNN performance (Chain 2, terminal node) |
| Exp 2 | Which preprocessing components drive improvement (Chain 2, decomposition) |
| Exp 3 | Robustness to noise and illumination (Chain 1, resistance to variability) |
| Exp 4 | Preprocessing directs attention to lesions (Chain 2, feature visibility node) |
| Exp 5 | Cross-database generalization (Chain 2, generalization node) |
| Exp 6 | Cross-device generalization (Chain 1 + Chain 2, device variability) |
| Exp 7 | Clinical validation under real-world conditions (Chain 2, external validation) |
