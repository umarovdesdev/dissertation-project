# 1. Bibliographic Metadata

**Full citation (APA 7)**
Son, J., Shin, J. Y., Kim, H. D., Jung, K.-H., Park, K. H., & Park, S. J. (2020). Development and Validation of Deep Learning Models for Screening Multiple Abnormal Findings in Retinal Fundus Images. *Ophthalmology, 127*(1), 85–94.

**DOI:** 10.1016/j.ophtha.2019.05.029

**Journal (+ publisher):** Ophthalmology (AAO / Elsevier)

**Year:** 2020

**Publication type:** Empirical — multi-finding fundus screening + external validation

**Research domain classification:** Retinal fundus screening, multi-label deep learning.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| CNN classification study | ✔ | 12-finding multi-label fundus models. |
| External validation | ✔ | In-house + external datasets. |
| Retinal/DR | ◐ | Includes hemorrhage/exudate (DR-relevant findings). |

**Justification:** Multi-abnormality fundus screening with external validation — supports §1.3.1, §4.7 (multi-finding), §4.4.

---

# 3. Research Problem

Detect **12 major fundus findings** (hemorrhage, hard exudate, cotton-wool patch, drusen, membrane, macular hole, myelinated nerve fiber, chorioretinal atrophy/scar, vascular abnormality, RNFL defect, glaucomatous/non-glaucomatous disc change) and validate externally. Addresses **multi-label screening / generalization**.

---

# 4. Datasets Used

Large in-house labeled fundus dataset; multiple external datasets. Cross-dataset: Yes.

---

# 5. Preprocessing Pipeline

Standard CNN preprocessing; [details in paper].

---

# 6. Model Architecture

CNN multi-label classifiers (one per finding / shared backbone); activation maps for localization.

---

# 7. Validation Design

Internal hold-out + external datasets per finding.

---

# 8. Performance Metrics

AUROC **96.2–99.9%** (in-house) and **94.7–98.0%** (external) across the 12 findings. (Headline.)

---

# 9. Authors' Claims

DL can screen many fundus abnormalities at high AUROC with reasonable external generalization, supporting broad fundus screening.

---

# 10. Empirical Support Assessment

External AUROC drop (≈1–2 pts) supports generalization with realistic degradation; many findings covered. Strong evidence.

---

# 11. Internal Validity

Per-finding label quality varies; activation-map localization qualitative.

---

# 12. External Validity

Multi-dataset external validation — relevant to device/domain shift (§4.7).

---

# 13. Strengths

Breadth (12 findings), external validation, quantified internal-vs-external gap.

---

# 14. Limitations

**Implicit:** Korean-population-centric; not DR-grade-specific; preprocessing not ablated.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Device/domain shift (§4.7)** | **Supporting** | Quantifies in-house→external AUROC degradation, the phenomenon H-6/H-7 examine. |
| Cross-dataset transferability (§4.4) | Supporting | External validation. |
| DR screening systems (§1.3.1) | Supporting | Includes DR-relevant findings. |
| Preprocessing-dominance | Peripheral | Not ablated. |

**Risk of contradiction:** Low.

---

# 16. Citation-Ready Statements

1. "The AUROC for the 12 fundus features ranged from 96.2% to 99.9% for the in-house datasets while performance was lower (94.7%–98.0%) in the external datasets." (Results)
2. The system screens 12 major fundus findings including hemorrhage and hard exudate. (Methods)

---

# 17. Epistemic Classification

**High-impact empirical evidence (multi-finding screening).**

---

# 18. Analytical Synthesis

Son et al. quantify the in-house-to-external performance gap (AUROC 96.2–99.9% → 94.7–98.0%) across twelve fundus findings, providing concrete external-validation evidence for the degradation-under-domain-shift phenomena the dissertation studies in §4.7 (device shift, H-6) and §4.6 (clinical degradation, H-7). Its breadth and realistic external drop make it a useful comparative reference, though it is multi-finding rather than DR-grade-specific and does not ablate preprocessing, leaving it neutral on preprocessing-dominance. Cite for cross-dataset/device-shift framing.

End of Literature Card.
