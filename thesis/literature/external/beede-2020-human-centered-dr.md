# 1. Bibliographic Metadata

**Full citation (APA 7)**
Beede, E., Baylor, E., Hersch, F., Iurchenko, A., Wilcox, L., Ruamviboonsuk, P., & Vardoulakis, L. M. (2020). A Human-Centered Evaluation of a Deep Learning System Deployed in Clinics for the Detection of Diabetic Retinopathy. *Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems (CHI '20)*, 1–12.

**DOI:** 10.1145/3313831.3376718

**Conference:** ACM CHI 2020

**Year:** 2020

**Publication type:** Empirical — human-centered / socio-technical field study

**Research domain classification:** Human–computer interaction, clinical AI deployment, diabetic retinopathy screening.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Qualitative field study | ✔ | Interviews + observation across 11 clinics. |
| Clinical deployment study | ✔ | Real DL DR-screening deployment in Thailand. |
| CNN benchmarking | ❌ | Not a model-accuracy study. |

**Justification:** Socio-technical deployment evidence — supports §6.3 (clinical workflow), §6.1 (requirements).

---

# 3. Research Problem

How a deployed DL DR-screening system performs in real clinical workflows, and which socio-environmental factors affect model utility, nursing workflow, and patient experience. Addresses **clinical deployment / human factors**.

---

# 4. Datasets Used

Field study at **eleven clinics in Thailand** (interviews + observations); no image-benchmark dataset.

---

# 5. Preprocessing Pipeline

N/A — but reports that image-quality gating (model rejecting ungradable images) created workflow friction (lighting, time).

---

# 6. Model Architecture

The deployed Google DR-screening DL system (external to this study); evaluated as a socio-technical artifact, not re-benchmarked.

---

# 7. Validation Design

Qualitative human-centered evaluation (pre/post deployment).

---

# 8. Performance Metrics

N/A (qualitative). Findings: socio-environmental factors (lighting, internet, image quality thresholds, nurse workload) materially affect real-world utility and patient experience.

---

# 9. Authors' Claims

Lab-accurate DL systems can underperform or disrupt workflows in situ; human-centered design and deployment context are essential.

---

# 10. Empirical Support Assessment

Rich qualitative evidence; not generalizable as quantitative performance.

---

# 11. Internal Validity

Observation/interview rigor; single-country, limited clinics.

---

# 12. External Validity

Insights transfer to other resource-variable deployments (e.g., Kazakhstan context).

---

# 13. Strengths

Real deployment, socio-technical depth, workflow/patient focus.

---

# 14. Limitations

**Implicit:** Qualitative; single programme; no model metrics.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **Clinical workflow / system design (§6.1/§6.3)** | **Supporting** | Evidence that image-quality gating and deployment context shape real utility — informs the dissertation's system-requirements and quality-aware preprocessing rationale. |
| Image quality → utility (§1.2.2) | Supporting | Ungradable-image rejection friction. |
| Preprocessing-dominance | Peripheral-supporting | Underscores why robust preprocessing/quality handling matters in deployment. |

**Risk of contradiction:** None.

---

# 16. Citation-Ready Statements

1. The study characterizes "current eye-screening workflows, user expectations … and post-deployment experiences" across eleven clinics in Thailand. (Abstract)
2. "Several socio-environmental factors impact model performance, nursing workflows, and the patient experience." (Findings)

---

# 17. Epistemic Classification

**High-impact socio-technical evidence (clinical AI deployment).**

---

# 18. Analytical Synthesis

Beede et al. supplies rare in-situ deployment evidence for the dissertation's system-architecture and clinical-workflow chapters (§6.1, §6.3): a lab-accurate DR-screening model encountered real friction from lighting, connectivity, image-quality thresholds, and nurse workload. This both motivates the dissertation's emphasis on robust, quality-aware preprocessing (ungradable-image handling) and tempers purely accuracy-centric claims with deployment realism relevant to the under-resourced Kazakhstan setting. It is qualitative with no model metrics, so it informs requirements and framing rather than quantitative comparison, and is supportive-but-indirect on preprocessing-dominance.

End of Literature Card.
