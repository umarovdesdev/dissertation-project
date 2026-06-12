# 1. Bibliographic Metadata

**Full citation (APA 7)**
Simonyan, K., & Zisserman, A. (2015). Very Deep Convolutional Networks for Large-Scale Image Recognition. *Proceedings of the 3rd International Conference on Learning Representations (ICLR)*. (arXiv:1409.1556)

**DOI:** 10.48550/arXiv.1409.1556

**Conference:** ICLR 2015

**Year:** 2015

**Publication type:** CNN architecture reference (VGG)

**Research domain classification:** CNN architectures, image classification.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Architecture reference | ✔ | VGG-16/19; small 3×3 filters, increased depth. |
| Empirical study | ◐ | ILSVRC experiments. |
| Retinal/DR | ❌ | General (VGG used by some DR works, e.g., Rakhlin #05). |

**Justification:** Canonical architecture reference for §1.3.1; VGG appears in cited DR studies.

---

# 3. Research Problem

Effect of depth on accuracy using stacks of small 3×3 convolutions. Addresses **architecture design / scaling depth**.

---

# 4. Datasets Used

ImageNet ILSVRC-2012.

---

# 5. Preprocessing Pipeline

Mean RGB subtraction; multi-scale training/eval.

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Design | Deep stacks of 3×3 conv + 2×2 max-pool; 16–19 weight layers |
| Insight | Multiple small filters > fewer large filters at equal receptive field |

---

# 7. Validation Design

ILSVRC val/test; ensemble + multi-crop.

---

# 8. Performance Metrics

ILSVRC-2014 top-5 error **6.8%** (ensemble); strong single-model results; 1st/2nd places localization/classification. (Headline.)

---

# 9. Authors' Claims

Increasing depth with small filters substantially improves accuracy; VGG features transfer well.

---

# 10. Empirical Support Assessment

ILSVRC evidence strong; transferability widely confirmed.

---

# 11. Internal Validity

Controlled depth ablations; high parameter count.

---

# 12. External Validity

Excellent transfer features; widely reused (incl. medical/DR).

---

# 13. Strengths

Simplicity, uniform design, strong transfer.

---

# 14. Limitations

**Implicit:** Large (138M params), compute-heavy; superseded by ResNet/EfficientNet.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Architecture lineage (§1.3.1)** | **Supporting (foundational)** | Context for the CNN-depth lineage preceding ResNet/EfficientNet; basis of cited DR baselines (e.g., Rakhlin). |
| Preprocessing-dominance | Peripheral | N/A. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "Our main contribution is a thorough evaluation of networks of increasing depth using an architecture with very small (3×3) convolution filters." (Abstract)
2. Depth of 16–19 weight layers yields substantial accuracy improvement. (Abstract)

---

# 17. Epistemic Classification

**Foundational / architecture reference.**

---

# 18. Analytical Synthesis

VGG is a canonical architecture reference for §1.3.1, establishing the depth-with-small-filters principle that the dissertation's ResNet-50/EfficientNet-B3 backbones build upon and that underlies cited DR baselines (e.g., Rakhlin's VGGNet). It is a general-vision architecture with no DR-specific or preprocessing content, neutral to preprocessing-dominance; cite to situate the CNN-architecture lineage when introducing backbone choices.

End of Literature Card.
