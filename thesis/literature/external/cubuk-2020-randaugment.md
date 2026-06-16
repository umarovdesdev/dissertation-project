# 1. Bibliographic Metadata

**Full citation (APA 7)**
Cubuk, E. D., Zoph, B., Shlens, J., & Le, Q. V. (2020). RandAugment: Practical automated data augmentation with a reduced search space. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, 702–703. (arXiv:1909.13719)

**DOI:** 10.1109/CVPRW50498.2020.00359

**Conference:** CVPR Workshops 2020 (IEEE)

**Year:** 2020

**Publication type:** Methodology reference — automated augmentation policy

**Research domain classification:** Data augmentation, AutoML.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Methodology reference (augmentation) | ✔ | Two-parameter automated augmentation. |
| Empirical study | ◐ | ImageNet/CIFAR/detection experiments. |
| Retinal/DR | ❌ | General. |

**Justification:** Supports §2.2.3 augmentation (practical policy used in EfficientNet-era training).

---

# 3. Research Problem

AutoAugment's huge search space is costly; RandAugment reduces it to **2 hyperparameters** (N transforms, magnitude M), removing a separate proxy search. Addresses **augmentation policy**.

---

# 4. Datasets Used

ImageNet, CIFAR-10/100, SVHN, COCO (detection).

---

# 5. Preprocessing Pipeline

Uniformly samples N augmentation ops at global magnitude M from a fixed set.

---

# 6. Model Architecture

Architecture-agnostic; tested with ResNet/EfficientNet/detectors.

---

# 7. Validation Design

Benchmark internal evaluation; matches/exceeds AutoAugment without proxy search.

---

# 8. Performance Metrics

Matches or exceeds AutoAugment/Fast-AutoAugment accuracy with far less search cost (e.g., strong ImageNet top-1 with EfficientNet). (Headline.)

---

# 9. Authors' Claims

A two-parameter, search-free augmentation policy matches learned policies and is practical at scale.

---

# 10. Empirical Support Assessment

Multi-benchmark evidence; simplicity validated. Robust augmentation reference.

---

# 11. Internal Validity

Controlled; N/M grid search only.

---

# 12. External Validity

General; widely adopted in modern CNN training.

---

# 13. Strengths

Simplicity, no proxy task, strong results.

---

# 14. Limitations

**Implicit:** Fixed transform set may include medically-inappropriate ops (must curate for fundus); non-medical evaluation.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Augmentation (§2.2.3)** | **Supporting** | Practical augmentation-policy reference; informs the unified-augmentation design; complements [[shorten-2019-augmentation-survey]], [[zhang-2018-mixup]]. |
| Preprocessing-dominance | Supporting | Augmentation as feature-space shaping. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "RandAugment … has a significantly reduced search space which allows it to be trained on the target task with no need for a separate proxy task." (Abstract)
2. The policy is parameterized by just two values, N and M. (§Method)

---

# 17. Epistemic Classification

**Methodological precedent (augmentation policy).**

---

# 18. Analytical Synthesis

RandAugment provides a practical, search-free augmentation-policy reference for §2.2.3 and is representative of the augmentation regimes used to train EfficientNet-class models like the dissertation's EfficientNet-B3 backbone. Its two-parameter design is directly relevant when justifying the unified-augmentation stage, though its generic transform set must be curated to avoid medically-inappropriate operations on fundus images. It is non-medical and cited as augmentation-method background; neutral-to-supportive for the preprocessing/feature-space thesis.

End of Literature Card.
