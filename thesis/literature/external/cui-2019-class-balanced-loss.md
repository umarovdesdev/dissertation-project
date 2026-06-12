# 1. Bibliographic Metadata

**Full citation (APA 7)**
Cui, Y., Jia, M., Lin, T.-Y., Song, Y., & Belongie, S. (2019). Class-Balanced Loss Based on Effective Number of Samples. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 9268–9277. (arXiv:1901.05555)

**DOI:** 10.1109/CVPR.2019.00949

**Journal / Conference:** CVPR 2019 (IEEE)

**Year:** 2019

**Publication type:** Empirical — loss re-weighting methodology

**Research domain classification:** Class imbalance, long-tailed classification, loss functions.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Methodology reference (loss) | ✔ | Class-balanced re-weighting via effective number of samples. |
| CNN study | ✔ | Long-tailed CIFAR/iNaturalist/ImageNet-LT. |
| Retinal/DR | ❌ | General, but applicable to DR grade imbalance. |

**Justification:** Supports §2.2.2 (loss functions for imbalanced medical datasets), complementing Focal Loss.

---

# 3. Research Problem

Naïve inverse-frequency re-weighting over-weights rare classes because samples overlap; the paper introduces the **effective number** (1−β^n)/(1−β) to re-weight per class. Addresses **class imbalance / loss design**.

---

# 4. Datasets Used

Long-tailed CIFAR-10/100, iNaturalist 2017/2018, ImageNet-LT.

---

# 5. Preprocessing Pipeline

Standard classification preprocessing.

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Method | Class-Balanced term weights each class by 1/effective-number |
| Combinable with | Softmax CE, sigmoid CE, **Focal Loss** |
| Hyperparameter | β ∈ [0,1) controls re-weighting strength |

---

# 7. Validation Design

Long-tailed benchmark internal evaluation; ablations over β.

---

# 8. Performance Metrics

Consistent accuracy gains on long-tailed benchmarks over standard and inverse-frequency baselines (headline; exact per-dataset figures).

---

# 9. Authors' Claims

Re-weighting by effective number of samples better handles imbalance than inverse-frequency and improves long-tailed classification.

---

# 10. Empirical Support Assessment

Multiple long-tailed datasets support the claim; theoretically motivated. Robust loss reference.

---

# 11. Internal Validity

Controlled; β sensitivity analyzed.

---

# 12. External Validity

General re-weighting scheme, applicable to DR grade imbalance.

---

# 13. Strengths

Principled effective-number formulation; composable with focal loss.

---

# 14. Limitations

**Implicit:** β tuning; non-medical evaluation.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Loss for imbalanced DR data (§2.2.2)** | **Supporting** | Alternative/complement to the dissertation's inverse-frequency α; complements [[lin-2017-focal-loss]]. |
| Evaluation framework (§3.4) | Supporting | Imbalance handling. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "We design a re-weighting scheme that uses the effective number of samples for each class to re-balance the loss." (Abstract)
2. Effective number of samples: E_n = (1 − β^n)/(1 − β). (§3)

---

# 17. Epistemic Classification

**Methodological precedent (imbalanced-data loss).**

---

# 18. Analytical Synthesis

This paper strengthens §2.2.2 by providing a principled alternative to inverse-frequency class weighting — the effective-number re-weighting — that can be composed with the dissertation's Focal Loss. It is directly relevant because EyePACS DR grades are heavily long-tailed, the exact regime the method targets, and it offers a justification (sample overlap) for why naïve inverse-frequency weighting can be suboptimal, informing the dissertation's α choice. It is non-medical and preprocessing-agnostic, cited as loss-design background rather than DR evidence.

End of Literature Card.
