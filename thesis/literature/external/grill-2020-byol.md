# 1. Bibliographic Metadata

**Full citation (APA 7)**
Grill, J.-B., Strub, F., Altché, F., Tallec, C., Richemond, P. H., Buchatskaya, E., … Valko, M. (2020). Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning. *Advances in Neural Information Processing Systems (NeurIPS), 33*, 21271–21284. (arXiv:2006.07733)

**DOI:** 10.48550/arXiv.2006.07733

**Journal / Conference:** NeurIPS 2020

**Year:** 2020

**Publication type:** Empirical — self-supervised representation-learning method

**Research domain classification:** Self-supervised learning (non-contrastive), representation learning.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Self-supervised method | ✔ | BYOL: online/target networks, no negative pairs. |
| CNN classification study | ✔ | ResNet encoders, ImageNet linear-eval. |
| Retinal/DR | ❌ | General vision. |

**Justification:** Canonical negative-free SSL reference for §2.3.3.

---

# 3. Research Problem

Whether high-quality SSL representations can be learned **without negative pairs**, avoiding contrastive collapse via a momentum target network + predictor. Addresses **representation learning**.

---

# 4. Datasets Used

ImageNet pretraining/linear-eval; transfer to multiple classification and dense-prediction datasets.

---

# 5. Preprocessing Pipeline

Standard SSL augmentations; robustness to augmentation/batch-size choices highlighted.

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Mechanism | Online network predicts target network's representation of another view; target = EMA of online |
| Loss | Mean-squared error on normalized predictions (no negatives) |
| Encoder | ResNet-50 (and larger) |

---

# 7. Validation Design

ImageNet linear eval; semi-supervised; transfer. Internal benchmark.

---

# 8. Performance Metrics

ImageNet linear-eval top-1 **74.3%** (ResNet-50) and **79.6%** with larger ResNet — surpassing contrastive baselines without negatives. (Headline.)

---

# 9. Authors' Claims

Negative-free bootstrapping achieves state-of-the-art SSL, more robust to batch size and augmentation set than contrastive methods.

---

# 10. Empirical Support Assessment

Strong ImageNet + transfer evidence; ablations on collapse-avoidance. Robust method reference.

---

# 11. Internal Validity

Controlled; collapse-avoidance mechanism analyzed (predictor + stop-gradient via EMA).

---

# 12. External Validity

Broad transfer; robustness advantages aid low-resource regimes.

---

# 13. Strengths

No negatives, robustness to batch size, strong accuracy.

---

# 14. Limitations

**Implicit:** Non-medical; mechanism of collapse-avoidance debated; compute-heavy.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **SSL pretraining (§2.3.3/§3.3.2)** | **Supporting (foundational method)** | Negative-free SSL alternative relevant to designing retinal pretraining; complements [[chen-2020-simclr]], [[he-2020-moco]], [[zhou-2023-retfound]]. |
| Preprocessing-dominance | Peripheral | N/A. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "BYOL … achieves … state of the art without using negative pairs." (Abstract)
2. "BYOL is more robust to the choice of image augmentations than contrastive methods." (Results)

---

# 17. Epistemic Classification

**Methodological precedent / foundational (non-contrastive SSL).**

---

# 18. Analytical Synthesis

BYOL extends the SSL design space the dissertation surveys for retinal pretraining by showing that strong representations can be learned without negative pairs, using an online/target bootstrapping scheme robust to batch size and augmentation. It situates the choice among contrastive (SimCLR/MoCo) and non-contrastive/generative (BYOL/MAE) families that culminate in RETFound's MAE selection. It is non-medical and preprocessing-agnostic, cited only as foundational SSL background in §2.3.3/§3.3.2.

End of Literature Card.
