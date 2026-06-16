# 1. Bibliographic Metadata

> Source-access note: Compiled from the open-access record (arXiv:1706.04599) and the paper's
> abstract; the full ICML article body was not retrieved at card-writing time. The calibration
> apparatus (ECE binning, temperature scaling, reliability diagrams) is reported at the level the
> abstract states plus this method's standard, widely-cited formulation; exact per-model numbers
> are marked [VERIFY against full text]. No metric value is quoted that the source does not report.

**Full citation (APA 7)**
Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *Proceedings of the 34th International Conference on Machine Learning (ICML)*, PMLR 70, 1321–1330. (arXiv:1706.04599)

**DOI:** 10.48550/arXiv.1706.04599

**Journal / Conference:** ICML 2017 (PMLR 70)

**Year:** 2017

**Publication type:** Empirical — confidence-calibration analysis + post-hoc calibration method (temperature scaling)

**Research domain classification:** Deep learning; probabilistic prediction; confidence calibration; uncertainty quantification.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Methodology reference (metric + method) | ✔ | Defines/popularizes Expected Calibration Error (ECE) and temperature scaling. |
| CNN classification study | ◐ | Uses CNN classifiers as the object of study, not as a contribution. |
| Retinal/DR study | ❌ | General vision/NLP classification. |

**Justification:** Cited in this dissertation as the canonical reference for calibration evaluation (ECE / reliability diagrams) and temperature scaling — a methodology reference, paradigm N/A.

---

# 3. Research Problem

Modern high-accuracy neural networks output class probabilities that do not match empirical correctness frequencies — they are typically over-confident. The paper asks how badly modern networks are miscalibrated, what training factors drive it, and how to correct it post hoc. Addresses **probabilistic reliability / uncertainty**, not preprocessing or architecture scaling.

---

# 4. Datasets Used

Image and document-classification benchmarks (per abstract: "image and document classification datasets"). Commonly: CIFAR-10/100, SVHN, ImageNet, and NLP corpora; specific dataset/architecture combinations [VERIFY against full text]. No dataset is introduced.

---

# 5. Preprocessing Pipeline

Not a preprocessing study. [NOT REPORTED] — standard per-dataset pipelines for the classifiers studied.

---

# 6. Model Architecture

The object of study is a set of modern classifiers (ResNet / DenseNet / Wide-ResNet family and similar) compared against an older LeNet-style baseline to contrast calibration across eras [VERIFY exact models]. Calibration is a **post-hoc** transform on the trained logits, not an architecture.

| Item | Description |
| --- | --- |
| Method contribution | Temperature scaling — divide logits by a single scalar T (T learned on a validation set by minimizing NLL) before softmax; does not change the arg-max, so accuracy is unchanged |
| Baselines compared | Histogram binning, isotonic regression, Platt scaling (temperature scaling is its single-parameter variant), and matrix/vector scaling |

---

# 7. Validation Design

Held-out validation set used to fit the calibration map; calibration measured on the test set. Internal benchmark across multiple datasets/architectures. No external/prospective clinical validation.

---

# 8. Performance Metrics

- **Expected Calibration Error (ECE):** predictions are partitioned into M equal-width confidence bins; ECE is the weighted average of |accuracy − confidence| across bins (M = 15 in the standard setting). [VERIFY bin count / per-model ECE values against full text.]
- **Maximum Calibration Error (MCE)**, **Negative Log-Likelihood (NLL)**, and reliability diagrams are also used.
- The paper reports that temperature scaling reduces ECE substantially across most datasets; exact reductions [VERIFY].

---

# 9. Authors' Claims

- "Modern neural networks, unlike those from a decade ago, are poorly calibrated."
- "Depth, width, weight decay, and Batch Normalization are important factors influencing calibration."
- "On most datasets, temperature scaling — a single-parameter variant of Platt Scaling — is surprisingly effective at calibrating predictions."

---

# 10. Empirical Support Assessment

Broad multi-dataset, multi-architecture evidence supports the miscalibration finding and the temperature-scaling recommendation. The factor analysis (depth/width/weight-decay/BatchNorm) is observational/correlational. Robust as a methodology reference; per-model calibration figures should be read from the full text before quoting.

---

# 11. Internal Validity

Post-hoc calibration fit on a separate validation split avoids test leakage. The factor-influence claims are associational (training factors co-vary), not isolated causal ablations. Metric reliability: ECE is binning-sensitive (bin count/edges affect the value) — a known caveat the dissertation should respect when reporting it.

---

# 12. External Validity

Findings generalize across the standard vision/NLP classifiers of the era; temperature scaling is architecture-agnostic and cheap, so it ports directly to the dissertation's CNNs. Calibration behaviour on 4-channel fundus inputs is the dissertation's own to measure (not covered here).

---

# 13. Strengths

Simple, accuracy-preserving calibration method; clear metric apparatus (ECE/reliability diagrams) now standard; broad empirical coverage; identifies training factors that drive miscalibration.

---

# 14. Limitations

**Explicit:** [NOT REPORTED in retrieved abstract]. **Implicit:** ECE is binning-dependent; the factor analysis is correlational; non-medical data; calibration under distribution shift is not the focus.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Evaluation framework (§2.6, §3.4, §5.2)** | **Core (methodology)** | Canonical source for ECE / reliability-diagram calibration evaluation and temperature scaling — the calibration apparatus the dissertation adopts to report probability reliability. |
| Class imbalance / Focal loss | Supporting | Calibration interacts with re-weighted losses; motivates reporting calibration alongside discrimination metrics. |
| Preprocessing-dominance | Peripheral | Not a preprocessing study; neutral. |

**Risk of contradiction:** None. Used for metric/method definition, not for any comparative performance claim.

---

# 16. Citation-Ready Statements

1. "Modern neural networks, unlike those from a decade ago, are poorly calibrated." (Abstract)
2. "Depth, width, weight decay, and Batch Normalization are important factors influencing calibration." (Abstract)
3. "On most datasets, temperature scaling — a single-parameter variant of Platt Scaling — is surprisingly effective at calibrating predictions." (Abstract)
4. "Confidence calibration — the problem of predicting probability estimates representative of the true correctness likelihood — is important for classification models in many applications." (Abstract)

---

# 17. Epistemic Classification

**Foundational / Methodological precedent (calibration).** High weight as the standard reference for confidence calibration evaluation and correction in deep classifiers.

---

# 18. Analytical Synthesis

Guo et al. is the dissertation's methodological anchor for confidence calibration: it supplies the Expected Calibration Error / reliability-diagram apparatus and the temperature-scaling correction that the evaluation framework (§3.4) and statistical-validation chapter (§5.2) use to report whether the model's predicted probabilities are trustworthy, not merely discriminative. Its central finding — that accurate modern networks are systematically over-confident, with calibration shaped by depth, width, weight decay, and Batch Normalization — justifies reporting calibration as a first-class metric alongside weighted-F1/AUROC for a screening model whose probability outputs inform triage. The method is accuracy-preserving and architecture-agnostic, so it transfers cleanly to the dissertation's 4-channel CNNs; the one caveat to honour is ECE's binning sensitivity. It is non-medical and preprocessing-agnostic, hence neutral to the preprocessing-dominance argument; it is cited strictly as metric/method definition. Per-model ECE values should be taken from the full ICML text before any numerical quotation.

End of Literature Card.
