# 1. Bibliographic Metadata

**Full citation (APA 7)**
Burlina, P. M., Joshi, N., Pekala, M., Pacheco, K. D., Freund, D. E., & Bressler, N. M. (2017). Automated Grading of Age-Related Macular Degeneration From Color Fundus Images Using Deep Convolutional Neural Networks. *JAMA Ophthalmology, 135*(11), 1170–1176.

**DOI:** 10.1001/jamaophthalmol.2017.3782

**Journal (+ publisher):** JAMA Ophthalmology (American Medical Association)

**Year:** 2017

**Publication type:** Empirical — CNN fundus grading (AMD)

**Research domain classification:** Age-related macular degeneration, deep learning, fundus classification.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| CNN classification study | ✔ | DCNN AMD grading from color fundus. |
| Transfer learning | ✔ | ImageNet-pretrained backbone fine-tuned. |
| Retinal/DR | ◐ | AMD (not DR) but same modality (color fundus). |

**Justification:** Color-fundus CNN-grading precedent (transfer learning) — supports §1.3.1; AMD-domain peripheral like #18.

---

# 3. Research Problem

Automate AMD severity grading from color fundus photographs using deep CNNs with transfer learning on the AREDS dataset. Addresses **classification / architecture-transfer**.

---

# 4. Datasets Used

NIH **AREDS** dataset: ~130,000 color fundus images from ~4,600 patients (large public AMD dataset).

---

# 5. Preprocessing Pipeline

Standard CNN preprocessing (resize/crop/normalize); ImageNet-style.

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Backbone | Deep CNN (AlexNet/OverFeat-style), ImageNet-pretrained, fine-tuned |
| Task | AMD severity grading / referability |

---

# 7. Validation Design

Internal cross-validation on AREDS; multiple grading granularities (2-class to multi-class).

---

# 8. Performance Metrics

Reported accuracy in the range of **~88.4–91.6%** depending on classification granularity (≈92–95% for coarser tasks per reports); AUC and weighted-kappa reported in paper. (Headline; exact figures **[VERIFY against source before quoting]**.)

---

# 9. Authors' Claims

DCNNs with transfer learning achieve clinically relevant automated AMD grading comparable to human performance on AREDS.

---

# 10. Empirical Support Assessment

Large dataset supports the claim; internal validation only (no external dataset). Reasonable evidence.

---

# 11. Internal Validity

Large AREDS data; single-dataset; preprocessing/feature pipeline standard.

---

# 12. External Validity

No external dataset — generalization beyond AREDS unverified.

---

# 13. Strengths

Large dataset, transfer learning, multiple granularities, high-impact venue.

---

# 14. Limitations

**Implicit:** AMD not DR; single-dataset (no external validation); exact metrics require source verification.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **CNN fundus grading / transfer learning (§1.3.1)** | **Supporting** | Color-fundus CNN-grading + transfer-learning precedent (parallels DR pipeline); AMD-domain peripheral like [[gonzalez-diaz-2024]] (#18). |
| Cross-dataset transferability | Peripheral | No external validation. |
| Preprocessing-dominance | Peripheral | Not ablated. |

**Risk of contradiction:** Low.

---

# 16. Citation-Ready Statements

1. "Deep convolutional neural networks … automatically grade age-related macular degeneration from color fundus images." (Abstract)
2. Transfer learning from ImageNet-pretrained networks was applied to the AREDS dataset. (Methods)
3. [Exact accuracy/AUC/κ values — VERIFY against the JAMA Ophthalmology source before citation.]

---

# 17. Epistemic Classification

**Empirical evidence (AMD CNN grading).** Peripheral domain (AMD), same modality.

---

# 18. Analytical Synthesis

Burlina et al. is a same-modality (color fundus), different-disease (AMD) precedent demonstrating that ImageNet-pretrained CNNs with transfer learning can grade retinal disease at clinically relevant accuracy on a large dataset (AREDS). It parallels the dissertation's transfer-learning-on-fundus pipeline and supports the general feasibility argument in §1.3.1, while remaining peripheral because it concerns AMD rather than DR and lacks external validation. It does not ablate preprocessing, so it is neutral on preprocessing-dominance; its exact numeric metrics should be verified against the JAMA Ophthalmology source before any quantitative citation.

End of Literature Card.
