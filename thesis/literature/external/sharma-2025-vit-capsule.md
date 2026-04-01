# LITERATURE CARD

---

# 1. Bibliographic Metadata

**Full citation (APA 7)**
Sharma, V., Rishu, Kukreja, V., Dogra, A., & Goyal, B. (2025). Transforming retinal diagnostics: Advanced detection of diabetic retinopathy using vision transformers and capsule networks. *Journal of Computer Science, 21*(2), 304–321. [https://doi.org/10.3844/jcssp.2025.304.321](https://doi.org/10.3844/jcssp.2025.304.321) 

**DOI:** 10.3844/jcssp.2025.304.321 

**Journal:** Journal of Computer Science

**Year:** 2025

**Publication type:** Empirical deep learning study

**Research domain classification:** Automated diabetic retinopathy grading using Vision Transformer–Capsule Network hybrid architecture

---

# 2. Study Type Classification

Applicable classifications:

* EyePACS benchmarking
* Vision Transformer application
* CNN-based classification study
* Hybrid architecture study

**Justification:**
The study trains and evaluates a ViT–CapsNet model on the EyePACS dataset (public Kaggle version). No external validation or cross-dataset testing is performed.

---

# 3. Research Problem

**Problem addressed:**
Development of a hybrid Vision Transformer–Capsule Network (ViT–CapsNet) model for early-stage multi-class DR classification from fundus images.

**Related to:**

* Architecture design (ViT + CapsNet integration)
* Feature extraction enhancement
* Multi-class DR grading (5-class ICDR scale)

**Not related to:**

* Cross-dataset generalization
* External validation
* Clinical deployment validation
* Lesion-level segmentation

---

# 4. Datasets Used

### EyePACS (Kaggle version)

* **Name:** EyePACS
* **Public / Private:** Public (Kaggle) 
* **Total sample size:** 30,262 images 
* **Class taxonomy:** 5-class ICDR grading

  * No DR: 22,116
  * Mild DR: 2,106
  * Moderate DR: 4,368
  * Severe DR: 845
  * Proliferative DR: 827 
* **Train/Validation/Test split:**

  * Training: 70%
  * Validation: 15%
  * Test: 15% 
* **External dataset used:** No
* **Cross-dataset testing performed:** No

---

# 5. Preprocessing Pipeline

Explicitly reported:

* Resizing: Bicubic interpolation 
* Augmentation:

  * Brightness adjustment
  * Contrast modification
  * Saturation adjustment
  * Hue modification
  * Rotation
  * Cropping
  * Noise removal 
* Normalization: Min–Max normalization to [0,1] range 

Not reported:

* CLAHE: [NOT REPORTED]
* Color normalization protocol: [NOT REPORTED]
* Image quality filtering: [NOT REPORTED]
* Lesion enhancement methods: [NOT REPORTED]

---

# 6. Model Architecture

**Architecture type:** Hybrid Vision Transformer + Capsule Network

Components:

* Patch embedding (16×16 patches)
* 4096 patches per image (1024×1024 resolution) 
* Linear projection
* Positional encoding (sin/cos formulation)
* Multi-head attention (8 heads)
* Convolutional layer
* Primary capsules
* Digit capsules with dynamic routing
* Dense classification layer

**Input resolution:** 1024×1024 

**Pretraining source:** [NOT REPORTED]
**Transfer learning:** [NOT REPORTED]
**Loss function:** [NOT REPORTED]
**Optimizer:** [NOT REPORTED]
**Epochs:** [NOT REPORTED]
**Learning rate / batch size:** [NOT REPORTED]

---

# 7. Validation Design

* Internal validation only
* Single-dataset split (70/15/15)
* No cross-validation
* No external validation
* No multi-center validation
* No prospective validation

---

# 8. Performance Metrics

## Overall Performance (ViT–CapsNet)

* Accuracy: 94% 
* Precision: 0.92 
* Recall: 0.91 
* F1-score: 0.91 

## Class-wise Metrics

| Class         | Precision | Recall | F1   | Accuracy |   |
| ------------- | --------- | ------ | ---- | -------- | - |
| No DR         | 0.95      | 0.93   | 0.94 | 95%      |   |
| Mild          | 0.88      | 0.85   | 0.86 | 92%      |   |
| Moderate      | 0.83      | 0.80   | 0.82 | 89%      |   |
| Severe        | 0.77      | 0.75   | 0.76 | 84%      |   |
| Proliferative | 0.70      | 0.68   | 0.69 | 80%      |   |

## Comparison Models

| Model        | Accuracy |   |
| ------------ | -------- | - |
| CNN          | 88%      |   |
| ResNet       | 90%      |   |
| EfficientNet | 92%      |   |
| ViT–CapsNet  | 94%      |   |

## AUC-ROC (reported in abstract)

* No DR: 0.56
* Mild DR: 0.48
* Moderate DR: 0.44
* Severe DR: 0.45
* Proliferative DR: 0.51 

No confidence intervals reported.
No statistical tests reported.
Confusion matrix mentioned but numerical values not provided.

---

# 9. Authors’ Claims

**Performance claims**

* Hybrid model improves classification performance.
* Achieves 94% accuracy outperforming CNN, ResNet, EfficientNet.

**Superiority claims**

* Better feature extraction due to ViT.
* Better spatial hierarchy preservation due to CapsNet.

**Generalization claims**

* Model demonstrates robustness (stated).

**Clinical applicability claims**

* Early detection capability improves diagnostic support.

---

# 10. Empirical Support Assessment

* No external validation → generalization not empirically demonstrated.
* No confidence intervals → uncertainty not quantified.
* Severe class imbalance present (No DR 22,116 vs Severe 845).
* No class-weighting strategy explicitly described.
* No statistical comparison tests.
* AUC values reported in abstract (0.44–0.56 for classes) are inconsistent with claimed high performance.

Generalization claims are not supported beyond internal split.

---

# 11. Internal Validity

* High risk of overfitting due to single-dataset training.
* Severe class imbalance.
* Extensive augmentation → potential augmentation inflation.
* No leakage prevention strategy described.
* Hyperparameters not reported.
* Mathematical derivations included but not empirically validated.

---

# 12. External Validity

* No cross-population validation.
* No cross-dataset transferability testing.
* Hardware constraints: [NOT REPORTED]
* Clinical workflow integration: [NOT REPORTED]

External validity: Limited.

---

# 13. Strengths

* Clear architectural description.
* Detailed mathematical formulation.
* Large dataset size (30,262 images).
* Multi-class ICDR grading.

---

# 14. Limitations

## Explicit (stated)

* Performance decreases for severe classes.
* Difficulty identifying advanced DR stages.

## Implicit

* No external validation.
* No multi-center validation.
* No statistical testing.
* Class imbalance not methodologically addressed.
* AUC inconsistency with claimed accuracy.
* No reproducibility details (optimizer, epochs).

---

# 15. Relevance to Dissertation

* Relevant for Vision Transformer comparison.
* Relevant for EyePACS benchmarking.
* Not relevant for cross-database validation.
* Weak evidence for generalization.
* Does not strengthen preprocessing-dominance hypothesis.
* Architecture-focused rather than validation-focused.

Risk of contradiction: Low (due to lack of external validation).

---

# 16. Citation-Ready Statements

1. The proposed ViT–CapsNet model achieved 94% accuracy on the EyePACS dataset (p. 315). 
2. The dataset consisted of 30,262 fundus images graded into five ICDR classes (p. 308). 
3. The data split was 70% training, 15% validation, and 15% testing (p. 309). 
4. Class-wise F1-score decreased to 0.69 for Proliferative DR (p. 315). 
5. No external dataset validation was performed. 

---

# 17. Epistemic Classification

**Classification:** Transformer-era study / Limited-scope empirical study

**Justification:**
Single-dataset internal validation only; no cross-dataset evidence; architecture-driven rather than generalization-driven contribution.

---

# 18. Analytical Synthesis

This article represents a Transformer-era architectural exploration rather than a validation-driven benchmark. Its epistemic weight is moderate due to reliance on a single dataset and absence of external validation. While it reports 94% accuracy, the lack of cross-database testing limits generalization claims. The study strengthens architectural comparison arguments but does not address robustness or international benchmarking gaps. For a dissertation emphasizing preprocessing dominance and cross-dataset generalization, this paper serves primarily as a comparative Transformer baseline rather than high-impact evidence.
