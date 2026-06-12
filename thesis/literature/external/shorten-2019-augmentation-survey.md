# 1. Bibliographic Metadata

**Full citation (APA 7)**
Shorten, C., & Khoshgoftaar, T. M. (2019). A survey on Image Data Augmentation for Deep Learning. *Journal of Big Data, 6*(1), 60.

**DOI:** 10.1186/s40537-019-0197-0

**Journal (+ publisher):** Journal of Big Data (Springer)

**Year:** 2019

**Publication type:** Review / Survey

**Research domain classification:** Data augmentation, deep learning.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Review / Survey | ✔ | Taxonomy of image augmentation methods. |
| Empirical study | ❌ | No new experiments. |
| Retinal/DR | ❌ | General; includes medical examples. |

**Justification:** Survey grounding §2.2.3 augmentation.

---

# 3. Research Problem

Catalogs augmentation strategies (geometric, color, kernel filters, mixing, random erasing, GAN-based, neural style, meta-learned policies) to combat overfitting/limited data. Addresses **augmentation / data scarcity**.

---

# 4. Datasets Used

N/A (survey).

---

# 5. Preprocessing Pipeline

Reviews geometric (flip/rotate/crop), photometric (color/brightness), filtering, mixing (mixup/cutmix), erasing, GAN synthesis.

---

# 6. Model Architecture

N/A (method-agnostic survey).

---

# 7. Validation Design

N/A.

---

# 8. Performance Metrics

N/A — synthesizes reported gains; discusses test-time augmentation and policy search.

---

# 9. Authors' Claims

Augmentation is a powerful, underexploited regularizer; choice should be data-informed; combining methods and learned policies helps.

---

# 10. Empirical Support Assessment

Coverage-based; no primary metrics.

---

# 11. Internal Validity

Survey scope; no pooling.

---

# 12. External Validity

Broadly applicable; explicitly covers small/medical datasets.

---

# 13. Strengths

Comprehensive taxonomy; practical guidance.

---

# 14. Limitations

**Implicit:** Narrative; rapidly evolving field.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Augmentation (§2.2.3)** | **Supporting (survey)** | Frames the V5 Stage-6 augmentation choices; complements [[zhang-2018-mixup]], [[cubuk-2020-randaugment]], [[krizhevsky-2012-alexnet]] (PCA color). |
| Preprocessing-dominance | Supporting | Positions augmentation within the preprocessing/feature-space argument. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "Data Augmentation … encompasses a suite of techniques that enhance the size and quality of training datasets." (Abstract)
2. Taxonomy spans geometric transforms, color-space transforms, kernel filters, mixing images, random erasing, and GAN-based augmentation. (Survey body)

---

# 17. Epistemic Classification

**Review / Survey (augmentation).**

---

# 18. Analytical Synthesis

This survey supplies the organizing taxonomy for the dissertation's augmentation discussion in §2.2.3 and contextualizes the V5 Stage-6 design (unified affine geometric + PCA color + brightness/contrast). It frames augmentation as a regularizer that expands the effective training distribution, consistent with the dissertation's view of preprocessing/augmentation as shaping the feature space available to the CNN. It contributes no primary metrics and is preprocessing-method background rather than evidence; cite alongside the mixup, RandAugment, and AlexNet (PCA color) primaries.

End of Literature Card.
