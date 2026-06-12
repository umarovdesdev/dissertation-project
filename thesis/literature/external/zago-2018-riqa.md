# 1. Bibliographic Metadata

**Full citation (APA 7)**
Zago, G. T., Andreão, R. V., Dorizzi, B., & Teatini Salles, E. O. (2018). Retinal image quality assessment using deep learning. *Computers in Biology and Medicine, 103*, 64–70.

**DOI:** 10.1016/j.compbiomed.2018.10.004

**Journal (+ publisher):** Computers in Biology and Medicine (Elsevier)

**Year:** 2018

**Publication type:** Empirical — retinal image quality assessment via transfer learning

**Research domain classification:** Retinal image quality assessment (RIQA), transfer learning, preprocessing/quality control.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| CNN classification study | ✔ | Inception-v3 fine-tuned for quality classes. |
| Cross-dataset (inter-database) validation | ✔ | DRIMDB ↔ ELSA-Brasil inter-database test. |
| Retinal/DR | ✔ | Fundus quality. |

**Justification:** Supports §2.6 (image quality metrics/assessment) and §1.2.2 (quality → performance).

---

# 3. Research Problem

Automatically assess retinal fundus image quality (good vs poor) to gate downstream analysis, using transfer learning with limited labels. Addresses **image quality / preprocessing**.

---

# 4. Datasets Used

- **DRIMDB**: 216 retinal images (125 good, 69 poor, plus outliers).
- **ELSA-Brasil**: used for inter-database testing.
- Intra-database and inter-database cross-validation.

---

# 5. Preprocessing Pipeline

CNN pretrained on non-medical images; fine-tuning for quality classifier; standard resize/normalize for Inception-v3.

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Backbone | Inception-v3 (ImageNet-pretrained), fine-tuned |
| Task | Binary/quality classification |
| Strategy | Transfer learning with few labeled images |

---

# 7. Validation Design

Intra-database CV + inter-database cross-validation (train one DB, test another). No prospective.

---

# 8. Performance Metrics

- DRIMDB: **AUC 99.98%**.
- Inter-database (ELSA-Brasil): **AUC 98.56%**.

---

# 9. Authors' Claims

A transfer-learned CNN achieves near-perfect intra-database and strong inter-database retinal quality classification with few labels.

---

# 10. Empirical Support Assessment

Inter-database test supports generalization; small DRIMDB size tempers the near-perfect AUC. Reasonable evidence.

---

# 11. Internal Validity

Small dataset → high-AUC optimism; outlier handling; limited class diversity.

---

# 12. External Validity

Inter-database evaluation is a strength; two databases only.

---

# 13. Strengths

Inter-database protocol; label-efficient transfer; high accuracy.

---

# 14. Limitations

**Implicit:** Tiny DRIMDB; binary quality; no DR end-task.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Image quality metrics (§2.6)** | **Supporting** | Strengthens previously THIN §2.6 with a fundus-specific RIQA study; complements [[fu-2020-eyeq-riqa]]. |
| Image quality → performance (§1.2.2) | Supporting | Motivates quality gating before classification. |
| Device domain shift | Supporting | Inter-database transfer. |
| Preprocessing-dominance | Peripheral-supporting | Quality control as a preprocessing concern. |

**Risk of contradiction:** Low.

---

# 16. Citation-Ready Statements

1. "A CNN achieved an AUC of 99.98% on DRIMDB and 98.56% on ELSA-Brasil in the inter-database experiment." (Results)
2. Transfer learning from non-medical images enables a performant quality classifier with few labeled retinal images. (Method)

---

# 17. Epistemic Classification

**Empirical evidence (RIQA).** Limited-scale but methodologically sound.

---

# 18. Analytical Synthesis

This study adds fundus-specific retinal image-quality assessment evidence to the previously thin §2.6, complementing the EyeQ dataset/MCF-Net reference. Its inter-database protocol (DRIMDB ↔ ELSA-Brasil) makes a modest but credible case that transfer-learned CNNs generalize for quality gating, motivating quality-aware preprocessing in the dissertation pipeline. The very small DRIMDB set inflates the near-perfect AUC, so the figure should be cited with that caveat. It evaluates quality, not DR grading, so it is supportive-but-indirect for preprocessing-dominance; cite in §2.6 and §1.2.2.

End of Literature Card.
