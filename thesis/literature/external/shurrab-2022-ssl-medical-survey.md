# 1. Bibliographic Metadata

**Full citation (APA 7)**
Shurrab, S., & Duwairi, R. (2022). Self-supervised learning methods and applications in medical imaging analysis: a survey. *PeerJ Computer Science, 8*, e1045.

**DOI:** 10.7717/peerj-cs.1045

**Journal (+ publisher):** PeerJ Computer Science (PeerJ)

**Year:** 2022

**Publication type:** Systematic / scoping review (survey)

**Research domain classification:** Self-supervised learning, medical image analysis.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Review / Survey | ✔ | Surveys SSL pretext tasks + contrastive/generative methods in medical imaging. |
| Empirical study | ❌ | No new experiments. |
| Retinal/DR specific | ◐ | Covers retinal among medical modalities. |

**Justification:** Survey directly supporting §2.3.3 (in-domain SSL for medical/retinal imaging) framing.

---

# 3. Research Problem

Synthesizes SSL approaches (predictive/pretext, contrastive, generative) and their applications across medical imaging modalities under label scarcity. Addresses **transfer learning / label efficiency**.

---

# 4. Datasets Used

N/A (survey of others' datasets across modalities — radiology, pathology, ophthalmology, etc.).

---

# 5. Preprocessing Pipeline

N/A (survey).

---

# 6. Model Architecture

Reviews CNN/ViT backbones and SSL frameworks (rotation, jigsaw, colorization, SimCLR, MoCo, BYOL, MAE-style) as applied to medical data.

---

# 7. Validation Design

N/A (narrative/scoping synthesis).

---

# 8. Performance Metrics

N/A — reports trends/comparisons from surveyed works, not new metrics.

---

# 9. Authors' Claims

SSL reduces dependence on expensive medical annotations; in-domain SSL and contrastive/generative methods are increasingly effective; open challenges remain (evaluation, domain shift).

---

# 10. Empirical Support Assessment

Coverage-based; no primary evidence. Useful for landscape mapping.

---

# 11. Internal Validity

Survey selection scope; no meta-analytic pooling.

---

# 12. External Validity

Cross-modality breadth; guidance generalizable to retinal SSL design.

---

# 13. Strengths

Organized taxonomy of medical SSL; identifies gaps; recent.

---

# 14. Limitations

**Implicit:** Narrative survey; no quantitative synthesis; field moves fast (pre-RETFound emphasis).

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Medical/retinal SSL (§2.3.3/§3.3.2)** | **Supporting (survey)** | Provides the survey-level grounding the index flagged as THIN; complements [[cheplygina-2018-not-so-supervised-survey]] and [[zhou-2023-retfound]]. |
| Preprocessing-dominance | Peripheral | N/A. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. "Self-supervised learning … reduces the need for large annotated medical datasets by leveraging unlabeled data." (Abstract/Intro)
2. Taxonomy: predictive/pretext, contrastive, and generative SSL methods applied across medical imaging modalities. (Survey body)

---

# 17. Epistemic Classification

**Review / Survey (medical SSL).**

---

# 18. Analytical Synthesis

This survey supplies the dedicated medical self-supervised-learning landscape that the LITERATURE_INDEX previously flagged as thin for §2.3.3/§3.3.2 (covered only by the general Cheplygina survey). It organizes SSL pretext, contrastive, and generative families and their medical applications, providing examiner-facing breadth that situates RETFound and MICLe within a broader trend toward annotation-efficient in-domain pretraining. It contributes no primary metrics and is preprocessing-agnostic, so it serves as survey scaffolding rather than evidence; cite alongside the primary SSL method cards to frame the dissertation's pretraining axis.

End of Literature Card.
