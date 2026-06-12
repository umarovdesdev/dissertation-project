# 1. Bibliographic Metadata

**Full citation (APA 7)**
Quellec, G., Charrière, K., Boudi, Y., Cochener, B., & Lamard, M. (2017). Deep image mining for diabetic retinopathy screening. *Medical Image Analysis, 39*, 178–193. (arXiv:1610.07086)

**DOI:** 10.1016/j.media.2017.04.012

**Journal (+ publisher):** Medical Image Analysis (Elsevier)

**Year:** 2017

**Publication type:** Empirical — CNN DR screening + heatmap explainability

**Research domain classification:** Diabetic retinopathy, CNN classification, weakly-supervised lesion localization.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| CNN classification study | ✔ | ConvNet referable-DR detection. |
| Explainability / lesion localization | ✔ | Backprop-generalization heatmaps. |
| External / cross-dataset validation | ✔ | Kaggle + e-ophtha + DiaretDB1. |
| EyePACS benchmarking | ✔ | 2015 Kaggle (EyePACS) dataset. |

**Justification:** DR-specific explainability + EyePACS benchmark — supports §1.3.1, §1.3.3, §4.5, §4.4.

---

# 3. Research Problem

Detect referable DR and generate lesion heatmaps from image-level labels (weakly-supervised), via a generalized backpropagation producing high-quality heatmaps. Addresses **classification + explainability/lesion localization**.

---

# 4. Datasets Used

- 2015 **Kaggle DR (EyePACS)**: ~90,000 fundus photographs.
- Private **e-ophtha**: ~110,000 photographs.
- **DiaretDB1**: lesion-level (MA, hemorrhages, exudates, cotton-wool spots).
- External/cross-dataset: Yes.

---

# 5. Preprocessing Pipeline

Fundus normalization/resize for ConvNet; [detailed parameters in paper].

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Model | ConvNet (trained for image-level referable-DR) |
| Explainability | Generalized backpropagation → high-quality lesion heatmaps |
| Supervision | Image-level labels only (weakly-supervised lesion detection) |

---

# 7. Validation Design

Image-level detection on Kaggle/e-ophtha; lesion-level evaluation on DiaretDB1. Cross-dataset.

---

# 8. Performance Metrics

Referable-DR detection **Az (AUC) = 0.954** (Kaggle) and **0.949** (e-ophtha); lesion-level evaluation on DiaretDB1 (four lesion types). (Headline.)

---

# 9. Authors' Claims

A single image-level-trained ConvNet both screens DR at high AUC and localizes lesions via heatmaps, offering interpretable screening.

---

# 10. Empirical Support Assessment

Large datasets + cross-dataset + lesion-level evidence support the claims. Robust DR-explainability evidence.

---

# 11. Internal Validity

Heatmap quality vs ground-truth lesions evaluated; private-data portion limits reproducibility.

---

# 12. External Validity

Cross-dataset (Kaggle↔e-ophtha) + lesion-level transfer. Strong.

---

# 13. Strengths

Large-scale; interpretable heatmaps from weak labels; lesion-level validation.

---

# 14. Limitations

**Implicit:** Heatmap method predates Grad-CAM standardization; private data; binary referable focus.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Explainability / lesion localization (§1.3.3/§4.5)** | **Core-adjacent** | DR-specific precedent for weakly-supervised lesion heatmaps — the very task Exp 4 pursues with Grad-CAM ALO/IoU. |
| **Cross-dataset transferability (§4.4)** | **Supporting** | Kaggle↔e-ophtha AUC stability. |
| EyePACS benchmarking | Supporting | Uses Kaggle/EyePACS. |
| Preprocessing-dominance | Peripheral | Preprocessing not the focus. |

**Risk of contradiction:** Low.

---

# 16. Citation-Ready Statements

1. "Very good detection performance was achieved: Az = 0.954 in Kaggle's dataset and Az = 0.949 in e-ophtha." (Abstract)
2. A generalization of backpropagation produces high-quality heatmaps showing which pixels drive image-level predictions. (Abstract)

---

# 17. Epistemic Classification

**High-impact empirical evidence (DR explainability).**

---

# 18. Analytical Synthesis

Quellec et al. is a strong DR-specific precedent for the dissertation's explainability experiment (Exp 4, §4.5): it shows a ConvNet trained only on image-level labels can both screen referable DR at high AUC (0.954 Kaggle, 0.949 e-ophtha) and localize lesions via heatmaps validated against DiaretDB1 lesion annotations. This directly anticipates the dissertation's attention-lesion-overlap (ALO/IoU) evaluation, while using a pre-Grad-CAM heatmap method, positioning the dissertation's Grad-CAM-based approach as a methodological successor. It also contributes cross-dataset (Kaggle↔e-ophtha) stability evidence for §4.4. Preprocessing is not its focus, so it is neutral on preprocessing-dominance.

End of Literature Card.
