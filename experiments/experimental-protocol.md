# Experimental Protocol

Automated Diabetic Retinopathy Detection via Preprocessing and CNN Classification

**Document Version:** 4.0 — V4 sync: V4 6-stage pipeline replacing V3 5-component pipeline; canonical flip (Stage 0) and flat-field correction (Stage 2) added; CLAHE upgraded to dual-constraint stochastic; normalization changed to ImageNet; augmentation integrated as Stage 5; Experiment 1 expanded to 6 configurations (A–F); baseline updated from "resize only" to "crop+resize+ImageNet normalize".

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
| EyePACS               | Primary training (V4 Experiments 1 and 2). ~35,126 labeled images (40% subset of full EyePACS; ~14,050 used for experiments). |
| APTOS 2019            | [NOT ACTIVE — old Experiment 3 (robustness under image degradation) is DROPPED] |
| IDRiD                 | Clinical validation, CLAHE sweep, lesion localization (V4 Experiments 2, 4, 5)   |
| Messidor / Messidor-2 | External generalization (V4 Experiment 5)                                         |
| RFMiD / DDR / ODIR    | Device domain shift evaluation (V4 Experiment 6)                                  |

---

# 2. Cross-Validation Protocol

To ensure robustness of the results, **3-fold cross-validation with patient-level split** is used.

Procedure:

1. Dataset divided into **3 folds**.
2. For each iteration:

   * **2 folds → training**
   * **1 fold → test**
3. Process repeated **3 times**.
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

Six configurations are trained (A–D: core 2×2 factorial; E–F: optional per-patient binocular blending extension):

| Config | Preprocessing                                      | CNN             |
| ------ | -------------------------------------------------- | --------------- |
| A      | baseline (crop+resize+ImageNet normalize)          | ResNet50        |
| B      | full V4 pipeline                                   | ResNet50        |
| C      | baseline (crop+resize+ImageNet normalize)          | EfficientNet-B3 |
| D      | full V4 pipeline                                   | EfficientNet-B3 |
| E      | full V4 pipeline + per-patient binocular blending  | ResNet50        |
| F      | full V4 pipeline + per-patient binocular blending  | EfficientNet-B3 |

*[V3 Historical: 4 configs A–D; baseline was "resize only"; pipeline was V3 5-component]*

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

**V4 Ablation (primary):** Experiment 2 tests V4 stage contributions:

| V4 Pipeline Configuration | Stages Included |
| ------------------------- | --------------- |
| baseline | Stages 1 + 4 (crop+resize + ImageNet normalize) |
| baseline + canonical flip (Stage 0a only) | Stages 0a + 1 + 4 |
| baseline + canonical orientation (Stage 0a + 0b) | Stages 0a + 0b + 1 + 4 |
| baseline + flat-field correction | Stages 1 + 2 + 4 |
| baseline + CLAHE | Stages 1 + 3 + 4 |
| baseline + augmentation | Stages 1 + 4 + 5 |
| full V4 pipeline | All stages (0a+0b+1+2+3+4+5) |

**V3 Ablation (historical reference):** The V3 5-component pipeline stages are also studied for historical component-level analysis:

*V3 pipeline components:*
1. **FOV standardization (V3)** — Hough circle detection, border removal, centering, resize
2. **Green channel imaging (V3)** — Extract green channel from RGB
3. **Normalization (V3)** — Pixel values [0,1]
4. **CLAHE enhancement (V3)** — LAB color space (L-channel), dynamic clip limit
5. **HSV contrast enhancement (V3)** — Additional contrast in HSV space

*V3 ablation sequence:* resize only → +CLAHE → +HSV → +green channel → +normalization = full V3 pipeline

Purpose: determine which V4 stages contribute most to performance (primary), with V3 component reference for historical comparison.

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

# 7. V4 Experiment 4 — Explainability Analysis

**Purpose:**
Determine whether preprocessing shifts CNN attention toward clinically relevant lesion regions.

**Tests whether:** Preprocessing directs CNN attention toward clinically relevant lesion regions, quantified by ALO and IoU (H-5).

**Model:** EfficientNet-B4

Images:

* 10 randomly sampled images per DR class from IDRiD (with lesion annotations)

Two pipelines:

| Pipeline | Description                                         |
| -------- | --------------------------------------------------- |
| baseline | crop + resize + ImageNet normalize only (Stages 1+4) |
| proposed | full V4 pipeline (all 6 stages)                     |

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

# 8. V4 Experiment 5 — Cross-Dataset Generalization

> **V4 NOTE:** V3 merged Experiment 3 is split back into two separate V4 experiments. Experiment 5 tests H-4 (cross-database transferability); Experiment 6 tests H-6 (device robustness). This restores the original Exp 5/6 split from the pre-V3 protocol.

**Purpose:**
Evaluate generalization to independent clinical datasets without retraining.

**Tests whether:** The preprocessing pipeline enables cross-database generalization (H-4).

**Training dataset:** EyePACS (checkpoints from V4 Experiment 1)

**Testing datasets (Experiment 5 — generalization):**

| Dataset       | Role                        | Cameras                |
| ------------- | --------------------------- | ---------------------- |
| Messidor      | External generalization     | Topcon                 |
| Messidor-2    | External generalization     | Topcon                 |
| IDRiD         | External generalization     | Kowa                   |

No retraining performed. Models evaluated in zero-shot transfer.

**Metrics:**
* Accuracy, Weighted F1, ROC-AUC (per dataset)
* Generalization ratio G = F1_external / F1_EyePACS per OD-4 (H-4 criterion: G ≥ 0.85)

**Statistical analysis:** Bootstrap 95% CI across datasets; DeLong test for ROC-AUC comparison.

---

# 8b. V4 Experiment 6 — Device Domain Shift

**Purpose:**
Evaluate classification robustness across images from different fundus camera manufacturers without retraining.

**Tests whether:** The preprocessing pipeline reduces cross-device performance variance (H-6).

**Training dataset:** EyePACS (checkpoints from V4 Experiment 1)

**Testing datasets (Experiment 6 — device domain shift):**

| Dataset       | Role                        | Cameras                |
| ------------- | --------------------------- | ---------------------- |
| RFMiD         | Device domain shift         | Topcon, Kowa           |
| DDR           | Device domain shift         | Canon, Topcon          |
| ODIR-5K       | Device domain shift         | Canon, Zeiss           |

No retraining performed. Models evaluated in zero-shot transfer.

**Metrics:**
* Accuracy, Weighted F1, ROC-AUC per camera group
* Cross-device performance variance (H-6 criterion: lower variance for preprocessed models)

**Statistical analysis:** Bootstrap 95% CI across camera groups; DeLong test for ROC-AUC comparison.

---

<!-- FUTURE WORK V3: Experiment 7 (Clinical Validation with Kazakh medical center data) is NOT an active V3 experiment. No Kazakh clinical data is available. This experiment is preserved as future work placeholder. -->

# 10. FUTURE WORK (V3): Old Experiment 7 — Clinical Validation (Dirty Data Pipeline)

> **V3 NOTE:** This experiment is NOT part of V3 active experiments. Kazakh clinical data is not yet available (no institutional agreements). This section is preserved as a future work placeholder per VCR-4 and NC-15. The dissertation references this as planned future work only.

**Purpose:**
Test the full V4 6-stage preprocessing pipeline on clinical fundus images from Kazakh medical centers. These images represent "dirty data" — variable quality, non-standardized acquisition protocols, potential artifacts, and diverse camera hardware.

**Tests whether:** The preprocessing pipeline maintains effectiveness under real-world clinical imaging conditions outside of curated benchmark datasets.

**Dataset:** Clinical fundus images from Kazakh medical centers (access pending institutional agreements). **NOT AVAILABLE — future work only.**

**Protocol (future):**
1. Apply the full V4 6-stage preprocessing pipeline to clinical images
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

| Experiment | Tests | V4 Status |
|---|---|---|
| V4 Exp 1 | Preprocessing improves CNN performance (Chain 2, terminal node) — H-1 | ACTIVE |
| V4 Exp 2 | Which preprocessing components drive improvement; CLAHE threshold sensitivity (Chain 2, decomposition) — H-1, H-2 | ACTIVE |
| V4 Exp 4 | Preprocessing directs attention to lesions, ALO primary (Chain 2, feature visibility node) — H-5 | ACTIVE |
| V4 Exp 5 | Cross-database generalization (Chain 2, generalization) — H-4 | ACTIVE |
| V4 Exp 6 | Cross-device generalization (Chain 2, device variability) — H-6 | ACTIVE |
| ~~Exp 3~~ | ~~Robustness to noise and illumination (Chain 1, resistance to variability)~~ | DROPPED — old Exp 3 |
| ~~Exp 7~~ | ~~Clinical validation under real-world conditions (Chain 2, external validation)~~ | FUTURE WORK — no data available |
