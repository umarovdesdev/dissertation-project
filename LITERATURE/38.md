# 1. Bibliographic Metadata

**Full citation (APA 7)**
Zhang, G., Lin, J.-W., Wang, J., Ji, J., Cen, L.-P., Chen, W., Xie, P., Zheng, Y., Xiong, Y., Wu, H., Li, D., Ng, T. K., Pang, C. P., & Zhang, M. (2022). Automated multidimensional deep learning platform for referable diabetic retinopathy detection: A multicentre, retrospective study. *BMJ Open, 12*, e060155. [https://doi.org/10.1136/bmjopen-2021-060155](https://doi.org/10.1136/bmjopen-2021-060155)

**DOI:** 10.1136/bmjopen-2021-060155
**Journal:** *BMJ Open*
**Year:** 2022
**Publication type:** Empirical multicentre external validation study
**Research domain classification:** Clinical deep learning system for diabetic retinopathy screening

---

# 2. Study Type Classification

* CNN-based classification study
* External validation study
* Multicentre validation study
* Clinical comparative validation (human–machine comparison)

**Justification:**
The study develops a multidimensional CNN-based system and evaluates it on an external validation dataset from different centers and devices (pp. 1–3, Table 1). It further compares the system against three retinal specialists (p. 5, Table 3).

---

# 3. Research Problem

**Problem addressed:**
Development and validation of a real-world, guideline-based deep learning system for automated detection of referable diabetic retinopathy (DR) incorporating multidimensional classification.

**Specific focus areas:**

* Clinical deployment in screening programs
* Multidimensional lesion classification
* Real-world generalization across centers
* Automated referable decision integration (image/eye/patient level)

The study explicitly aims to move beyond single-dimension referable DR classification toward guideline-consistent screening logic (pp. 1–2).

---

# 4. Datasets Used

## Primary Dataset (Private, Multicentre)

**Source centers:**

* Joint Shantou International Eye Center (JSIEC)
* Lifeline Express DR Screening Program (LEDRSP)
* Liuzhou City Red Cross Hospital
* Second Affiliated Hospital of Shantou University Medical College

**Total images:** 83,465
**Eyes:** 39,836
**Patients:** 21,716
(p. 5, Table 1)

### Dataset Structure

| Component               | Images | Percentage |
| ----------------------- | ------ | ---------- |
| Development set         | 53,211 | 63.8%      |
| External validation set | 30,254 | 36.2%      |

(p. 5, Table 1)

**Image acquisition:**

* Mydriatic retinal images
* Two 45° fields (macula-centered, optic disc-centered)
* Multiple camera types (Topcon Top-2000, NIDEK AFC-230, Canon CR-DGi) (p. 2, Table 1)

---

### Class Taxonomy

Five independent classifiers:

1. Image quality (Q0/Q1)
2. Retinopathy (R0–R3; referable = R2/R3)
3. Maculopathy gradability
4. Maculopathy (M0/M1)
5. Photocoagulation (P0/P1)

Referable DR = any referable retinopathy or maculopathy (p. 3).

---

### Train/Validation/Test Split

Development set:

* Split 75:10:15
* Patient-level split
  (p. 3)

External validation:

* Images from different hospitals and time periods
* No overlap with development data
  (p. 3, Table 1)

---

### Cross-Dataset Testing

Yes.
External validation dataset from different centers and periods (p. 3).

---

# 5. Preprocessing Pipeline

**Reported:**

* Image quality assessment preceding classification (p. 3)
* Exclusion of non-fundus images and non-DR ocular diseases (p. 2)

**NOT REPORTED:**

* Resizing parameters
* Cropping procedure
* Normalization method
* CLAHE usage
* Color normalization
* Data augmentation specifics
* Image resolution
* Lesion enhancement techniques

---

# 6. Model Architecture

**Architecture type:**
Ensemble of CNNs

Base models:

* Inception-V3
* Xception
* Inception-ResNet-V2
  (p. 3)

**Ensemble method:**
Unweighted average

**Pretraining source:** [NOT REPORTED]

**Loss function:** [NOT REPORTED]
**Optimizer:** [NOT REPORTED]
**Epochs:** [NOT REPORTED]
**Input resolution:** [NOT REPORTED]
**Hyperparameters:** [NOT REPORTED]

Explainability:

* SHAP-CAM (combining CAM and DeepSHAP)
  (pp. 3, 7)

---

# 7. Validation Design

* Internal training/validation/test split (75:10:15)
* External validation (different centers and periods)
* Multicentre design
* Retrospective
* Human–machine comparison on independent 253-image dataset (2019–2020)
  (p. 5)

No prospective validation reported.

---

# 8. Performance Metrics

## External Validation – Image Level

### Retinopathy classifier

* Accuracy: 0.966
* F1: 0.870
* Sensitivity: 0.978
* Specificity: 0.965
* AUROC: 0.9944 (95% CI 0.9936–0.9952)

### Maculopathy classifier

* Accuracy: 0.965
* F1: 0.885
* Sensitivity: 0.949
* Specificity: 0.967
* AUROC: 0.9904 (95% CI 0.9888–0.9919)

### Referable DR (image level)

* Accuracy: 0.967
* F1: 0.918
* Sensitivity: 0.971
* Specificity: 0.967
* AUROC: 0.9931 (95% CI 0.9920–0.9942)

### Referable DR (patient level)

* Accuracy: 0.918
* F1: 0.822
* Sensitivity: 0.971
* Specificity: 0.905
* AUROC: 0.9848 (95% CI 0.9819–0.9877)

(pp. 4–5, Table 2)

---

### Human–System Agreement

Cohen’s κ (DL vs ground truth): 0.86–0.93
Gwet’s AC1: 0.89–0.94
(p. 5)

---

### Statistical methods

* AUROC with 95% CI using DeLong method
* F1, sensitivity, specificity
* Cohen’s κ
* Gwet’s AC1
  (pp. 4–5)

---

# 9. Authors’ Claims

1. High accuracy in multidimensional classification.
2. Comparable performance to DR experts.
3. Suitability for large-scale real-world screening.
4. SHAP-CAM improves interpretability.
5. Guideline-based multidimensional approach is superior to single-dimension screening logic.

---

# 10. Empirical Support Assessment

* External validation dataset large (30,254 images).
* Multi-device, multi-center validation supports generalization within Chinese screening programs.
* Confidence intervals reported for AUROC.
* Class imbalance handling: [NOT REPORTED]
* No stratified device-wise performance analysis.
* Statistical testing adequate for classification metrics.

Generalization supported regionally; not internationally validated.

---

# 11. Internal Validity

* Patient-level splitting reduces leakage risk.
* External dataset temporally and geographically distinct.
* Overfitting risk mitigated via ensemble.
* Hyperparameter transparency absent.
* Augmentation strategy not reported.
* Retrospective design limits control of confounders.

---

# 12. External Validity

* Multicenter (China only).
* Multiple camera types used.
* Clinical screening alignment (NHS-based grading).
* No cross-ethnic external dataset.
* No public dataset benchmarking.

---

# 13. Strengths

* Large dataset (83,465 images).
* True external validation.
* Multidimensional classification aligned with screening guidelines.
* Human comparison study.
* Explainability integration (SHAP-CAM).
* Multi-level referable decision (image/eye/patient).

---

# 14. Limitations

## Explicit (stated by authors)

* DME graded without stereoscopic imaging or OCT.
* Fine lesions may be underdetected.
* Binary referable classification only.
* No stratified analysis by age/device.
* Retrospective design.
  (pp. 8–9)

## Implicit

* No hyperparameter transparency.
* No public dataset benchmarking.
* No cross-country validation.
* No prospective trial.
* Class imbalance strategy not described.

---

# 15. Relevance to Dissertation

* Strong relevance to cross-dataset validation (multicenter external).
* Not relevant to EyePACS/Messidor benchmarking.
* Not a Vision Transformer study.
* Does not evaluate preprocessing dominance explicitly.
* Shows architecture ensemble without preprocessing disclosure.
* May challenge preprocessing-dominance hypothesis due to lack of reported preprocessing pipeline.

---

# 16. Citation-Ready Statements

1. “The five-dimensional classifiers achieved AUROC values ranging from 0.9639 to 0.9944 in the external validation set” (Table 2, p. 4).
2. “Referable DR detection at the patient level achieved an AUROC of 0.9848 (95% CI 0.9819–0.9877)” (Table 2, p. 4).
3. “The DL system showed comparable performance (Cohen’s κ: 0.86–0.93) with three DR experts” (p. 5).
4. “The dataset consisted of 83,465 images from 21,716 patients collected from multiple centers and devices” (Table 1, p. 5).
5. “Three neural networks (Inception-V3, Xception and Inception-ResNet-V2) were used as base models with unweighted averaging” (p. 3).

---

# 17. Epistemic Classification

**Clinical validation precedent**

Justification:
Large multicentre dataset, external validation, human comparison, and guideline-based deployment orientation make this a clinically oriented validation study rather than a benchmarking or architectural innovation study.

---

# 18. Analytical Synthesis

This article represents high-quality empirical evidence for CNN-based DR screening under real-world clinical conditions. The external validation across multiple centers and devices strengthens internal and regional generalization claims. However, absence of reported preprocessing details limits mechanistic interpretation and prevents evaluation of preprocessing contribution. The study demonstrates strong performance using ensemble CNNs but does not benchmark against public datasets or alternative architectures such as Vision Transformers. It reinforces the feasibility of guideline-based multidimensional DR screening but does not directly inform preprocessing-dominance hypotheses. Its epistemic weight lies primarily in clinical deployment validation rather than methodological innovation.

---

End of Literature Card.
