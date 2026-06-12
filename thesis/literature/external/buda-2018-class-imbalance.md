# 1. Bibliographic Metadata

**Full citation (APA 7)**
Buda, M., Maki, A., & Mazurowski, M. A. (2018). A systematic study of the class imbalance problem in convolutional neural networks. *Neural Networks, 106*, 249–259. (arXiv:1710.05381)

**DOI:** 10.1016/j.neunet.2018.07.011

**Journal (+ publisher):** Neural Networks (Elsevier)

**Year:** 2018

**Publication type:** Empirical — systematic comparison study

**Research domain classification:** Class imbalance, CNN training methodology.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Systematic empirical study | ✔ | Compares imbalance-handling methods across datasets/imbalance levels. |
| CNN study | ✔ | MNIST/CIFAR/ImageNet-scale experiments. |
| Retinal/DR | ❌ | General; method guidance applies to DR. |

**Justification:** Evidence base for §2.2.2/§2.2.3 imbalance-handling choices.

---

# 3. Research Problem

Which methods best address class imbalance in CNNs (oversampling, undersampling, thresholding, cost-sensitive), and how performance degrades with imbalance. Addresses **class imbalance**.

---

# 4. Datasets Used

MNIST, CIFAR-10, ImageNet (with controlled artificial imbalance).

---

# 5. Preprocessing Pipeline

Standard; sampling-based interventions are the variable.

---

# 6. Model Architecture

CNNs of varying depth; methods compared: oversampling, undersampling, two-phase training, thresholding, cost-sensitive.

---

# 7. Validation Design

Controlled imbalance sweeps; multi-dataset internal evaluation.

---

# 8. Performance Metrics

Key findings: **oversampling generally best** and does not necessarily cause overfitting in CNNs; thresholding output probabilities helps; imbalance harms performance increasingly with severity. (Headline conclusions.)

---

# 9. Authors' Claims

Oversampling (to fully balance) is typically the most effective method; combine with thresholding; imbalance impact grows with task complexity.

---

# 10. Empirical Support Assessment

Systematic sweeps support the conclusions; controlled and broad. Robust methodological-guidance reference.

---

# 11. Internal Validity

Artificial imbalance is controlled; real-world label noise not modeled.

---

# 12. External Validity

Guidance generalizes; directly relevant to DR grade imbalance.

---

# 13. Strengths

Systematic, multi-dataset, actionable recommendations.

---

# 14. Limitations

**Implicit:** Synthetic imbalance; non-medical; pre-dates focal-loss-heavy practice.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Imbalance handling (§2.2.2/§2.2.3)** | **Supporting** | Empirical grounding for sampling/threshold choices alongside Focal Loss; complements [[lin-2017-focal-loss]], [[cui-2019-class-balanced-loss]]. |
| Evaluation framework (§3.4) | Supporting | Metric choice under imbalance. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "The method that in most cases outperforms others is oversampling." (Findings)
2. "Oversampling does not cause overfitting of convolutional neural networks, as opposed to … classical machine learning models." (Findings)

---

# 17. Epistemic Classification

**Methodological precedent (imbalance study).**

---

# 18. Analytical Synthesis

Buda et al. provide the systematic empirical basis for the dissertation's imbalance-handling decisions in §2.2.2/§2.2.3, complementing the focal-loss and class-balanced-loss method cards. Their finding that oversampling — without the overfitting penalty seen in classical models — and probability thresholding are effective informs how the dissertation balances EyePACS's long-tailed DR grades alongside its Focal-Loss objective. The study uses synthetic imbalance on non-medical data, so it is guidance rather than DR-specific evidence; it is preprocessing-agnostic and neutral to preprocessing-dominance.

End of Literature Card.
