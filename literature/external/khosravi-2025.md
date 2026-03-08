# 1. Bibliographic Metadata

**Full citation (APA 7)**
Khosravi, P., Huck, N. A., Shahraki, K., Ghafari, E., Azimi, R., Kim, S. Y., Crouch, E., Xie, X., & Suh, D. W. (2025). External validation of deep learning models for classifying etiology of retinal hemorrhage using diverse fundus photography datasets. *Bioengineering, 12*(1), 20. [https://doi.org/10.3390/bioengineering12010020](https://doi.org/10.3390/bioengineering12010020)

**DOI**
10.3390/bioengineering12010020

**Journal**
*Bioengineering* (MDPI)

**Year**
2025

**Publication type**
Empirical study – external validation

**Research domain classification**
Medical AI / Ophthalmology / Retinal hemorrhage classification / External validation study

---

# 2. Study Type Classification

* External validation study ✔
* Cross-dataset validation ✔
* Vision Transformer application ✔
* CNN-based classification study ✔

**Justification:**
The study evaluates pretrained ResNet18 (CNN) and FastViT-SA12 (Vision Transformer hybrid) on external datasets comprising 2661 images from multiple public and private sources (pp. 3–6).

---

# 3. Research Problem

**Specific problem addressed:**
Classification of retinal hemorrhage (RH) etiology into:

* Traumatic
* Medical

using fundus photography.

**Primary methodological concern:**
Generalization and external validation of deep learning models across heterogeneous datasets (p. 2).

**Problem category:**

* Generalization ✔
* Cross-dataset robustness ✔
* Clinical applicability ✔

Not focused on:

* Preprocessing innovation
* Lesion segmentation
* Architecture scaling

---

# 4. Datasets Used

Total external validation dataset: **2661 images** (p. 5)

## Private Datasets

### 1. South Korea Dataset

* Private
* n = 114
* Trauma only (114)
* No medical cases
* Used for external validation
* Cross-dataset testing: Yes

### 2. Virginia Dataset

* Private
* n = 192
* Trauma only (192 AHT cases)
* Used for external validation
* Cross-dataset testing: Yes

---

## Public Datasets

### 3. RFMiD + RFMiD 2.0

* Public
* n = 1924 RH images

  * Medical: 1918
  * Trauma: 6
* Binary classification (medical vs trauma)
* Used for external validation
* Cross-dataset testing: Yes

### 4. DeepEyeNet

* Public
* n = 335

  * Medical: 332
  * Trauma: 3
* Binary classification
* Used for external validation

### 5. BRSET

* Public
* 96 RH images selected from 16,266
* Medical only (96)
* Used for external validation

---

## Dataset Structure Summary

| Etiology | Total |
| -------- | ----- |
| Medical  | 2346  |
| Trauma   | 315   |
| Total    | 2661  |

(Table 1, p. 5)

---

# 5. Preprocessing Pipeline

(Section 2.2, p. 3)

* Resize to 256×256 (bilinear interpolation)
* Zero-padding as needed
* Data augmentation:

  * Random contrast adjustment
  * Gaussian noise
  * Horizontal flipping
  * Cropping
  * Cutout
* Final resize to 224×224
* Normalization: ImageNet per-channel normalization
* Testing: Direct resize to 224×224 + normalization

Not reported:

* CLAHE
* Color normalization beyond ImageNet
* Lesion enhancement
* Image quality filtering

---

# 6. Model Architecture

## 1. ResNet18

* CNN architecture
* Pretrained on ImageNet
* Transfer learning (fine-tuned)
* Input size: 224×224

## 2. FastViT-SA12

* Hybrid Vision Transformer
* Pretrained on ImageNet
* Fine-tuned
* Input size: 224×224

Training dataset:

* 597 images

  * Medical: 298 (49.9%)
  * Trauma: 299 (50.1%)

Loss function: [NOT REPORTED]
Optimizer: [NOT REPORTED]
Epochs: [NOT REPORTED]
Learning rate: [NOT REPORTED]

---

# 7. Validation Design

* External validation ✔
* Multi-source dataset ✔
* No prospective validation
* No cross-validation reported
* No confidence intervals reported

Models trained on 597 images, validated on independent 2661-image external dataset.

---

# 8. Performance Metrics

## FastViT-SA12

* Accuracy: **96.99%**
* AUC: **0.9811**
* Medical:

  * Precision: 0.9935
  * Recall: 0.9723
  * F1: 0.9828
* Trauma:

  * Precision: 0.8219
  * Recall: 0.9524
  * F1: 0.8824
* Specificity (Youden Index): 97.23%
* Sensitivity: 95.56%

Correct classifications:

* Medical: 2281
* Trauma: 300

---

## ResNet18

* Accuracy: **94.66%**
* AUC: **0.9626**
* Medical:

  * Precision: 0.9893
  * Recall: 0.9497
  * F1: 0.9691
* Trauma:

  * Precision: 0.7115
  * Recall: 0.9238
  * F1: 0.8039
* Specificity: 94.97%
* Sensitivity: 92.70%

Correct classifications:

* Medical: 2228
* Trauma: 291

No confidence intervals reported.

---

# 9. Authors’ Claims

* Models demonstrate strong external generalization.
* FastViT-SA12 outperforms ResNet18.
* Models have clinical utility.
* External validation is essential for trustworthy deployment.
* FastViT focuses on clinically relevant regions (optic disk).

---

# 10. Empirical Support Assessment

* External validation robust? → Yes (multi-source, 2661 images).
* Confidence intervals? → No.
* Class imbalance handled? → Severe imbalance (2346 vs 315).
* Statistical testing? → Not reported.
* Generalization claim partially supported.

Limitations:

* Trauma class underrepresented in public datasets.
* No statistical comparison test between models.

---

# 11. Internal Validity

* Balanced training dataset (597 images).
* No leakage evidence reported.
* Augmentation moderate.
* Overfitting risk unclear (no training curves reported).
* No hyperparameter transparency.

---

# 12. External Validity

* Multi-country dataset (USA, South Korea, Brazil).
* Public + private mix.
* Cross-dataset robustness demonstrated.
* Clinical feasibility plausible.
* Hardware constraints: Not discussed.

---

# 13. Strengths

* Large external validation set (n=2661).
* Multi-center dataset.
* Vision Transformer vs CNN comparison.
* Grad-CAM interpretability analysis.
* Transparent confusion matrix reporting.

---

# 14. Limitations

## Explicit (stated)

* Underrepresentation of trauma cases in public datasets.
* Misclassification in low-quality images.
* Limited global diversity.
* No prospective testing.

## Implicit

* No CI reporting.
* No statistical comparison tests.
* Class imbalance bias.
* Limited training size (597 images).

---

# 15. Relevance to Dissertation

**Preprocessing dominance hypothesis:**
Weak relevance. Preprocessing was standard; no enhancement focus.

**Cross-database validation:**
Highly relevant — strong external validation design.

**Vision Transformer comparison:**
Directly relevant. FastViT outperformed ResNet18.

**EyePACS/Messidor benchmarking:**
Not applicable.

**Risk of contradiction:**
If dissertation argues CNN superiority → potential contradiction.

---

# 16. Citation-Ready Statements

1. “Only 6% of AI medical imaging studies incorporate external validation” (p. 2).
2. FastViT-SA12 achieved an AUC of 0.9811 on a 2661-image external dataset (p. 6).
3. External validation included public and private datasets from multiple regions (p. 5).
4. Trauma class contained only 315 of 2661 images (Table 1, p. 5).
5. FastViT demonstrated higher trauma precision (0.8219) than ResNet18 (0.7115) (Table 2, p. 6).

---

# 17. Epistemic Classification

**Clinical validation precedent**
**Transformer-era empirical study**

Justification:

* Real external validation.
* Transformer vs CNN comparison.
* Multi-center dataset.
* Not DR-focused; limited to RH etiology.

---

# 18. Analytical Synthesis

This study provides strong empirical evidence for cross-dataset generalization in retinal hemorrhage classification. Its external validation design strengthens claims about robustness relative to many ophthalmic AI studies lacking such validation. However, absence of confidence intervals and statistical testing limits inferential strength. The Vision Transformer outperforming ResNet18 suggests architectural advantages independent of advanced preprocessing. The study does not address preprocessing dominance; instead, it highlights model architecture and dataset diversity as primary drivers of performance. Its epistemic weight is moderate-to-high within retinal hemorrhage classification but peripheral to diabetic retinopathy benchmarking.
