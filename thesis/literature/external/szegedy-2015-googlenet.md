# 1. Bibliographic Metadata

**Full citation (APA 7)**
Szegedy, C., Liu, W., Jia, Y., Sermanet, P., Reed, S., Anguelov, D., … Rabinovich, A. (2015). Going Deeper with Convolutions. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 1–9. (arXiv:1409.4842)

**DOI:** 10.1109/CVPR.2015.7298594

**Conference:** CVPR 2015 (IEEE)

**Year:** 2015

**Publication type:** CNN architecture reference (GoogLeNet / Inception-v1)

**Research domain classification:** CNN architectures, image classification.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Architecture reference | ✔ | Inception module, GoogLeNet. |
| Empirical study | ◐ | ILSVRC-2014 winner. |
| Retinal/DR | ❌ | General (Inception family used by Gulshan #12). |

**Justification:** Canonical Inception-family reference (§1.3.1); precursor to Inception-v3 used in landmark DR work.

---

# 3. Research Problem

Increase depth/width while controlling compute via multi-scale "Inception" modules and 1×1 dimensionality reduction. Addresses **efficient architecture design**.

---

# 4. Datasets Used

ImageNet ILSVRC-2014.

---

# 5. Preprocessing Pipeline

Standard ImageNet preprocessing.

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Module | Inception: parallel 1×1/3×3/5×5 conv + pooling, concatenated; 1×1 bottlenecks |
| Net | 22 layers, ~5M params, auxiliary classifiers |

---

# 7. Validation Design

ILSVRC-2014 classification/detection.

---

# 8. Performance Metrics

ILSVRC-2014 classification winner, top-5 error **6.67%**. (Headline.)

---

# 9. Authors' Claims

Carefully designed multi-scale modules achieve high accuracy at modest compute/params.

---

# 10. Empirical Support Assessment

ILSVRC win corroborates; influential design.

---

# 11. Internal Validity

Complex hand-designed modules; auxiliary-loss heuristics.

---

# 12. External Validity

Inception family widely transferred (incl. DR — Gulshan 2016 Inception-v3).

---

# 13. Strengths

Compute-efficient, accurate, influential module design.

---

# 14. Limitations

**Implicit:** Architectural complexity; superseded by later Inception/ResNet/EfficientNet.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Architecture lineage (§1.3.1)** | **Supporting (foundational)** | Inception precursor to Inception-v3 used by the canonical DR study (Gulshan, #12). |
| Preprocessing-dominance | Peripheral | N/A. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "The main hallmark of this architecture is the improved utilization of the computing resources inside the network." (Abstract)
2. GoogLeNet, a 22-layer Inception network, won ILSVRC-2014 classification. (§Results)

---

# 17. Epistemic Classification

**Foundational / architecture reference.**

---

# 18. Analytical Synthesis

GoogLeNet introduces the Inception module that leads to Inception-v3 — the backbone of the field-defining DR study by Gulshan et al. (#12) — making it relevant architecture-lineage context for §1.3.1. Its contribution is compute-efficient multi-scale feature extraction, a general-vision advance with no DR or preprocessing content. Cite to trace the Inception lineage when situating backbone choices and the canonical DR literature; neutral to preprocessing-dominance.

End of Literature Card.
