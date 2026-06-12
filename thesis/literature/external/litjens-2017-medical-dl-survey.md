# 1. Bibliographic Metadata

**Full citation (APA 7)**
Litjens, G., Kooi, T., Bejnordi, B. E., Setio, A. A. A., Ciompi, F., Ghafoorian, M., … Sánchez, C. I. (2017). A survey on deep learning in medical image analysis. *Medical Image Analysis, 42*, 60–88. (arXiv:1702.05747)

**DOI:** 10.1016/j.media.2017.07.005

**Journal (+ publisher):** Medical Image Analysis (Elsevier)

**Year:** 2017

**Publication type:** Review / Survey (>300 works)

**Research domain classification:** Deep learning, medical image analysis.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Review / Survey | ✔ | Surveys >300 deep-learning medical-imaging contributions. |
| Empirical study | ❌ | No new experiments. |
| Retinal/DR | ◐ | Includes retinal/ophthalmology among modalities. |

**Justification:** Canonical medical-DL survey grounding §1.3.1/§1.3.2 field framing.

---

# 3. Research Problem

Synthesizes deep-learning methods (classification, detection, segmentation, registration) across medical-imaging tasks and anatomies; identifies trends/challenges. Addresses **field landscape**.

---

# 4. Datasets Used

N/A (survey).

---

# 5. Preprocessing Pipeline

Reviews preprocessing/augmentation practices across studies.

---

# 6. Model Architecture

Reviews CNNs, RBMs/autoencoders, RNNs across tasks.

---

# 7. Validation Design

N/A.

---

# 8. Performance Metrics

N/A — synthesizes trends; notes CNNs dominate and that challenges include data scarcity and class imbalance.

---

# 9. Authors' Claims

Deep learning (esp. CNNs) rapidly became dominant across medical imaging; key challenges: limited labeled data, class imbalance, interpretability, standardization.

---

# 10. Empirical Support Assessment

Coverage-based authority; widely cited landmark survey.

---

# 11. Internal Validity

Survey scope; field has advanced since 2017.

---

# 12. External Validity

Broadly applicable landscape; foundational reference.

---

# 13. Strengths

Comprehensive, organized, highly cited.

---

# 14. Limitations

**Implicit:** Pre-transformer/pre-foundation-model era; narrative.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Field framing (§1.3.1/§1.3.2)** | **Supporting (survey)** | Establishes CNN dominance and the data-scarcity/imbalance/interpretability challenges the dissertation tackles (preprocessing, focal loss, Grad-CAM). |
| Preprocessing-dominance | Supporting (contextual) | Notes preprocessing/augmentation heterogeneity across studies. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "We survey the use of deep learning for image classification, object detection, segmentation, registration, and other tasks" across medical imaging. (Abstract)
2. CNNs became the methodology of choice across medical-image-analysis tasks. (Findings)

---

# 17. Epistemic Classification

**Foundational / survey (medical DL).**

---

# 18. Analytical Synthesis

Litjens et al. is the landmark medical-deep-learning survey that frames §1.3.1/§1.3.2 by documenting CNN dominance and the field's recurring challenges — limited labeled data, class imbalance, and interpretability — each of which the dissertation addresses (in-domain SSL pretraining, Focal Loss, Grad-CAM explainability). It is a narrative survey with no primary metrics, predating the transformer/foundation-model era, so it is cited for field framing rather than current state-of-the-art. It is neutral to preprocessing-dominance but useful for situating preprocessing heterogeneity across the literature.

End of Literature Card.
