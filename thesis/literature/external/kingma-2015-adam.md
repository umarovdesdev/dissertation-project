# 1. Bibliographic Metadata

**Full citation (APA 7)**
Kingma, D. P., & Ba, J. (2015). Adam: A Method for Stochastic Optimization. *Proceedings of the 3rd International Conference on Learning Representations (ICLR)*. (arXiv:1412.6980)

**DOI:** 10.48550/arXiv.1412.6980

**Conference:** ICLR 2015

**Year:** 2015

**Publication type:** Methodology reference — optimization algorithm

**Research domain classification:** Stochastic optimization, deep-network training.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Methodology reference | ✔ | Defines the Adam optimizer. |
| Empirical study | ◐ | Includes convergence experiments. |
| Retinal/DR | ❌ | General. |

**Justification:** Canonical optimizer reference for §2.2.2/§3.x training methodology.

---

# 3. Research Problem

First-order stochastic optimization needing adaptive per-parameter learning rates with low memory. Adam combines momentum (1st moment) and RMSProp-style (2nd moment) estimates with bias correction. Addresses **optimization**.

---

# 4. Datasets Used

MNIST, CIFAR-10, IMDB (logistic regression/MLP/CNN convergence demos).

---

# 5. Preprocessing Pipeline

N/A.

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Method | Adaptive moment estimation (Adam) |
| Updates | Exponential moving averages of gradient (β1) and squared gradient (β2) + bias correction |
| Defaults | β1=0.9, β2=0.999, ε=1e-8 |

---

# 7. Validation Design

Convergence comparisons vs SGD/AdaGrad/RMSProp.

---

# 8. Performance Metrics

Faster/robust convergence across tasks; theoretical regret bound provided. (Headline.)

---

# 9. Authors' Claims

Adam is computationally efficient, low-memory, invariant to gradient rescaling, well-suited to large/noisy/sparse problems.

---

# 10. Empirical Support Assessment

Demos + theory support claims; ubiquitous adoption corroborates.

---

# 11. Internal Validity

Small-scale demos; later work notes generalization-gap vs SGD in some settings.

---

# 12. External Validity

Universal applicability to deep-network training.

---

# 13. Strengths

Robust defaults, adaptivity, efficiency, ease of use.

---

# 14. Limitations

**Implicit:** Can generalize worse than tuned SGD+momentum on some vision tasks (subsequent literature).

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Training methodology (§2.2.2/§3)** | **Supporting (method used)** | Citable source if Adam/AdamW is the optimizer in the experiments. |
| Preprocessing-dominance | Peripheral | N/A. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "Adam … computes individual adaptive learning rates for different parameters from estimates of first and second moments of the gradients." (Abstract)
2. Recommended defaults: β1=0.9, β2=0.999, ε=10⁻⁸. (§Algorithm)

---

# 17. Epistemic Classification

**Foundational / methodological precedent (optimizer).**

---

# 18. Analytical Synthesis

Adam is the canonical citable source for the adaptive optimizer commonly used to train the dissertation's CNN backbones, grounding the optimization details of the training methodology. Its adaptive per-parameter learning rates and robust defaults make it a standard choice for fine-tuning ResNet-50/EfficientNet-B3 under the project's constraints. It is a general optimization method with no DR or preprocessing content, neutral to the central thesis; cite at first description of the training procedure (noting AdamW if weight decay is decoupled).

End of Literature Card.
