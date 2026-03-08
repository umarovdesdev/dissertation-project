# Experimental Protocol

Automated Diabetic Retinopathy Detection via Preprocessing and CNN Classification

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

[
mean \pm std
]

This reduces variance due to random data splits.

---

# 3. Evaluation Metrics

## 3.1 Primary performance metrics

* ROC-AUC
* Weighted F1-score
* Quadratic Cohen’s Kappa
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

## 3.4 Computational metrics

To evaluate computational efficiency:

* training time
* inference latency
* GPU memory usage
* parameter count

---

## 3.5 Statistical validation

Statistical significance is evaluated using:

* **McNemar test** – classification comparison
* **DeLong test** – ROC-AUC comparison
* **Bootstrap confidence intervals (95%)**

---

# 4. Experiment 1 — Causal Improvement (Preprocessing vs Architecture)

Purpose:
Determine whether preprocessing improves classification independently of CNN architecture.

Dataset: **EyePACS**

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

[
Performance_{preprocessing} > Performance_{baseline}
]

---

# 5. Experiment 2 — Preprocessing Component Ablation

Purpose:
Quantify the contribution of each preprocessing component.

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

Purpose:
Evaluate model robustness under degraded imaging conditions.

Dataset: **APTOS 2019**

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

Purpose:
Determine whether preprocessing shifts CNN attention toward clinically relevant lesion regions.

Model: **EfficientNet-B4**

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

[
IoU = GradCAM \cap lesion\ mask
]

Hypothesis:

[
IoU_{preprocessing} > IoU_{baseline}
]

Lesion masks obtained from **IDRiD dataset**.

---

# 8. Experiment 5 — Clinical Generalization

Purpose:
Evaluate generalization to independent clinical datasets.

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

Purpose:
Evaluate robustness to images captured by different fundus cameras.

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

# 10. Image Quality Improvement Analysis

To quantify the effect of preprocessing, image quality metrics are calculated:

* Contrast-to-Noise Ratio (CNR)
* Vessel Visibility Index
* Image Entropy
* Structural Similarity Index (SSIM)

These metrics measure improvement in vascular feature visibility.

---