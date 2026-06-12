# 1. Bibliographic Metadata

**Full citation (APA 7)**
Cuadros, J., & Bresnick, G. (2009). EyePACS: An Adaptable Telemedicine System for Diabetic Retinopathy Screening. *Journal of Diabetes Science and Technology, 3*(3), 509–516.

**DOI:** 10.1177/193229680900300315

**Journal (+ publisher):** Journal of Diabetes Science and Technology (Diabetes Technology Society / SAGE)

**Year:** 2009 (Vol. 3, Issue 3, May 2009)

**Publication type:** System-description / program report (telemedicine screening infrastructure). NOT an empirical model-benchmarking study.

**Research domain classification:** Telemedicine, diabetic retinopathy screening (DRS), clinical informatics, ophthalmic imaging workflow.

> **Note (citation anomaly):** The article's own abstract line reads "J Diabetes Sci Technol 2008;2(3):509-516", but the running header and masthead read "Vol 3, Issue 3, May 2009". The canonical citation is **2009;3(3):509–516** (DOI 10.1177/193229680900300315). Flag retained for the index.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Dataset descriptor / system descriptor | ✔ | Describes the EyePACS telemedicine screening system and grading protocol that underlies the EyePACS/Kaggle DR corpus. |
| EyePACS benchmarking | ✔ (provenance) | Authoritative descriptor of the EyePACS acquisition/grading origin. |
| CNN-based classification study | ❌ | No deep learning; no automated classifier. |
| External / cross-dataset validation | ❌ | Not a model-validation study. |
| Clinical prospective validation | ◐ partial | Reports program-level screening encounters and referral rates, not a controlled diagnostic-accuracy trial. |
| Vision Transformer / IDRiD lesion study | ❌ | N/A. |

**Justification:** This is the **provenance descriptor** for the EyePACS data acquisition and grading system (cameras, protocol, ERGS grading, severity levels). It is the citable origin of the EyePACS dataset characteristics, not an ML benchmark.

---

# 3. Research Problem

**Specific problem addressed:** Low compliance with annual retinal screening for diabetes patients due to access barriers (geographic remoteness, limited resources, lack of experience). EyePACS is presented as a license-free, web-based DRS system to lower these barriers.

- Generalization? No.
- Preprocessing? No (it defines *acquisition*, not algorithmic preprocessing).
- Architecture scaling? No.
- Lesion detection? Human grading of discrete lesions (ERGS), not automated.
- **Clinical deployment? Yes — core (screening workflow, EHR/HL7 integration, reader certification).**

---

# 4. Datasets Used

| Attribute | Description |
| --- | --- |
| System | EyePACS web-based DRS platform |
| Acquisition cameras | Nonmydriatic digital retinal cameras; protocol for **Canon CR-DGi and Canon CR-1** documented on the EyePACS site |
| Imaging protocol (California) | 1 external image/eye; **three internal fields/eye** (primary disk+macula, disk-centered, temporal); undilated pupils unless inadequate |
| Image format | JPEG (predominant device output) |
| Grading | EyePACS Retinopathy Grading System (ERGS), ETDRS-based; rule-based algorithm computes overall retinopathy severity + macular-edema severity |
| Severity taxonomy | No apparent DR; **Mild / Moderate / Severe NPDR; PDR** (NPDR collapsed to 3 levels, PDR to 1) → 5 overall levels |
| Macular edema | No ME / not-clinically-significant / clinically-significant (HE-distance surrogate) |
| Program scale | Pilot (2005–2006): 3,562 encounters; by end-2008: **>34,100 DRS encounters** across **>120 primary-care sites**; referral rate 8.21% sight-threatening, 7.83% other |

**Public/Private:** The *system* is license-free; the research dataset later distributed via the Kaggle "Diabetic Retinopathy Detection" competition (~35,126 labeled images) derives from EyePACS but is not enumerated in this paper. **External dataset:** No. **Cross-dataset testing:** No.

---

# 5. Preprocessing Pipeline

[NOT REPORTED] in the algorithmic sense. The paper specifies **acquisition** standards (three-field protocol, nonmydriatic capture, JPEG, image-quality categories: excellent/good/adequate/insufficient) and reader display requirements (monitor ≥1000:1 contrast, 32-bit color, 1200×1024). No CLAHE, color normalization, FOV masking, resizing, or augmentation — these are downstream of this descriptor.

---

# 6. Model Architecture

[NOT REPORTED] — no computational model. Grading is performed by certified human readers; a **rule-based algorithm** aggregates per-lesion severities into summary levels (no machine learning).

---

# 7. Validation Design

- Three-field imaging strategy cited as validated against the seven-field ETDRS gold standard in prior work: **sensitivity 89%, specificity 97%** for proliferative retinopathy (Bursell et al.); **89.3% agreement within one level** (Cavellerano et al.).
- Macular-edema surrogate (HE within disk diameters) reported to detect CSME with **sensitivity 94%, specificity 54%** (from a retrospective ETDRS-database analysis).
- Quality control: 3–5% of graded eyes re-graded by a retinal subspecialist.
- These are **borrowed/cited validation figures**, not a primary diagnostic-accuracy trial conducted in this paper.

---

# 8. Performance Metrics

Program/operational metrics (not model metrics):
- >34,100 DRS encounters by end of 2008; >120 sites.
- Referral rate: **8.21%** sight-threatening retinopathy; **7.83%** other conditions (cataract, glaucoma).
- Cited diagnostic figures: 3-field vs 7-field ETDRS sensitivity 89% / specificity 97% (PDR); CSME surrogate sensitivity 94% / specificity 54%.

AUC, F1, Cohen's κ, confusion matrix: [NOT REPORTED] (not an ML study).

---

# 9. Authors' Claims

- License-free, web-based software with standard interfaces and flexible protocols lets primary-care providers adopt retinopathy screening with minimal effort/resources.
- A rule-based grading algorithm affords greater standardization and reproducibility than reader gestalt.
- Telemedicine-based DRS can increase compliance and detect sight-threatening retinopathy effectively.

---

# 10. Empirical Support Assessment

| Claim | Evidence | Support |
| --- | --- | --- |
| Scalable, low-barrier screening | >34,100 encounters, >120 sites | Supported (program data) |
| Rule-based grading improves reproducibility | Design argument | Plausible; not directly measured here |
| Effective detection | Cited 3-field vs ETDRS figures | Supported by external prior studies, not this paper's own trial |

No internal model evaluation; figures are operational or borrowed. Adequate as a **descriptor**, not as evidence of automated-classifier performance.

---

# 11. Internal Validity

- No automated classifier → no overfitting/leakage/augmentation risks.
- Diagnostic-accuracy figures are cited from prior literature, not re-derived; selection and population context apply to those source studies.
- Program statistics are observational (referral rates depend on case mix).

---

# 12. External Validity

- Demonstrated multi-site deployment in California and Guanajuato (Mexico) — supports real-world feasibility in resource-limited primary care.
- Acquisition heterogeneity (multiple camera sources accommodated) is directly relevant to device-domain-shift framing.
- Generalizability of the *dataset* to other populations/devices is inherited by downstream ML users (e.g., Kaggle/EyePACS).

---

# 13. Strengths

- Authoritative description of EyePACS acquisition protocol and grading system (Canon CR-DGi/CR-1, three-field, ERGS, 5-level severity).
- Large operational footprint (>34,100 encounters).
- Detail on quality control, reader certification, EHR/HL7 integration.

---

# 14. Limitations

**Explicit (authors):** Nonstereo images preclude direct retinal-thickening (macular-edema) grading → HE surrogate used; ongoing validation of 3-field protocol against 7-field ETDRS at time of writing.

**Implicit:** No primary diagnostic-accuracy data generated here; citation-year inconsistency; no per-image dataset enumeration (the ML-usable labeled partition came later via Kaggle); multi-camera/quality variability not quantified.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| Preprocessing-dominance | Peripheral | Defines acquisition, not algorithmic preprocessing. |
| Cross-database generalization | Supporting | Describes the source domain (EyePACS) used as the dissertation's training corpus. |
| **EyePACS benchmarking** | **Core (provenance)** | Citable descriptor for EyePACS camera models (Canon CR-1), grading taxonomy, and origin of the ~35,126-image Kaggle partition (§4.1, §1.2.3, INTRO). |
| Device domain shift | Supporting | Multi-camera acquisition; nonmydriatic protocol. |
| Clinical deployment | Supporting | Telemedicine workflow, reader certification, EHR integration (§6.3). |

**Risk of contradiction:** None. Cite as **#47** dataset-descriptor provenance for EyePACS.

---

# 16. Citation-Ready Statements

1. "EyePACS is a license-free Web-based DRS system designed to simplify the process of image capture, transmission, and review." (Abstract)
2. "The protocol using the Canon CR-DGi and Canon CR-1 nonmydriatic cameras can be accessed on the EyePACS Web site." (Methodology)
3. "At the end of 2008, EyePACS recorded over 34,100 DRS encounters … The overall rate of referral is 8.21% for sight-threatening retinopathy and 7.83% for other conditions." (Results)
4. "Calculating the overall retinopathy severity … with a computer algorithm, rather than having each reader determine the levels, affords greater standardization and reliability to the system." (Structured Image Evaluation Protocol)
5. "Sensitivity and specificity, when compared to the seven-field ETDRS gold standard, were found to be 89% and 97%, respectively … for proliferative retinopathy." (Methodology)

---

# 17. Epistemic Classification

**Dataset / system descriptor (provenance reference).**

**Justification:** The paper is the authoritative origin description of the EyePACS screening system whose images and ETDRS-based grading underlie the EyePACS/Kaggle DR dataset central to the dissertation's training data. It carries no ML-benchmark value but is the correct citable source for dataset attributes (camera models, severity taxonomy, acquisition protocol).

---

# 18. Analytical Synthesis

This source anchors the provenance of the dissertation's primary training corpus (EyePACS). Its epistemic role is descriptive: it documents the acquisition hardware (Canon CR-DGi/CR-1 nonmydriatic cameras), the three-field protocol, JPEG output, and the ETDRS-derived five-level severity taxonomy and rule-based grading that define the label space later inherited by the Kaggle Diabetic Retinopathy Detection partition. It does not engage the preprocessing-dominance hypothesis and presents no automated-classifier metrics, so it can neither strengthen nor weaken that argument; its value is in grounding §4.1 dataset characterization, §1.2.3 device variability (multi-camera, nonmydriatic acquisition), and §6.3 clinical-workflow framing. The citation-year inconsistency in the article should be handled by citing the canonical 2009;3(3):509–516 form. Use strictly as the EyePACS descriptor (#47); the ~35,126-image labeled count is a Kaggle-competition attribute and should be attributed accordingly, not to this paper.

End of Literature Card.
