# 1. Bibliographic Metadata

**Full citation (APA 7)**
Decencière, E., Zhang, X., Cazuguel, G., Lay, B., Cochener, B., Trone, C., Gain, P., Ordóñez-Varela, J.-R., Massin, P., Erginay, A., Charton, B., & Klein, J.-C. (2014). Feedback on a Publicly Distributed Image Database: The Messidor Database. *Image Analysis & Stereology, 33*(3), 231–234.

**DOI:** 10.5566/ias.1155

**Journal (+ publisher):** Image Analysis & Stereology (International Society for Stereology / Slovenian Society for Stereology and Quantitative Image Analysis). Short Research Communication.

**Year:** 2014 (received April 18, 2014; accepted July 31, 2014)

**Publication type:** Dataset descriptor + bibliometric feedback report. NOT an empirical model study.

**Research domain classification:** Retinal image database curation, diabetic retinopathy screening, biomedical image processing, research-data management.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Dataset descriptor | ✔ | Authoritative description + usage feedback for the Messidor database. |
| Messidor benchmarking | ✔ (provenance) | Citable origin/descriptor of Messidor acquisition characteristics. |
| Bibliometric / usage-analysis study | ✔ | Analyzes citations, downloads, and web access 2008–2014. |
| CNN-based classification study | ❌ | No model trained. |
| External / cross-dataset validation | ❌ | N/A. |
| IDRiD lesion / ViT / prospective clinical | ❌ | N/A. |

**Justification:** A short communication that (a) describes the Messidor database and (b) reports on its uptake by the research community. It is a **provenance descriptor**, not an ML benchmark.

---

# 3. Research Problem

**Specific problem addressed:** Quantifying the real research value and uptake of a publicly distributed retinal image database (Messidor) after 6+ years, and deriving recommendations for designing/maintaining future databases.

- Generalization? No.
- Preprocessing? No.
- Architecture scaling? No.
- Lesion detection? The database *enables* lesion-segmentation/DR-grading research, but the paper itself runs none.
- Clinical deployment? Indirect (screening-research infrastructure).

---

# 4. Datasets Used

## Messidor database (the subject of the paper)

| Attribute | Description |
| --- | --- |
| Name | Messidor |
| Public/private | Public (distributed since 2008) |
| Total images | **1,200** color eye-fundus images of the posterior pole |
| Acquiring sites | 3 ophthalmologic departments |
| Camera | **Topcon TRC NW6 non-mydriatic retinograph**, color video 3CCD, 45° field of view |
| Resolutions | 1440×960, 2240×1488, or 2304×1536 px; 8 bits/color plane |
| Dilation | 800 images with pupil dilation (Tropicamide 0.5%), 400 without |
| Purpose | Evaluate automatic lesion segmentation and DR grading methods |
| Grading | DR grade + risk of macular edema (per Messidor documentation) |

**Bibliometric data reported:** download requests totaling **1,324** (table of per-country requests); web visitors rising from 54 (2008) to 669 (2013); Google-Scholar citations rising 1 (2008) → 89 (2013), total **189**; of 47 DR papers in Medical Image Analysis + IEEE TMI since 2008, **10** cite Messidor.

**External dataset:** No. **Cross-dataset testing:** No.

> **Disambiguation:** This is the original **Messidor** (1,200 images, Topcon TRC NW6). The dissertation's Exp 3/5 use **Messidor-2** (1,748 images), a distinct later release. Cite this card for Messidor provenance, but do not conflate the image counts.

---

# 5. Preprocessing Pipeline

[NOT REPORTED] — the paper describes raw acquisition parameters (resolution, bit depth, FOV, dilation) only. No CLAHE, normalization, FOV masking, resizing, or augmentation; the database is delivered as acquired.

---

# 6. Model Architecture

[NOT REPORTED] — no model. The paper is a database-feedback communication.

---

# 7. Validation Design

Not applicable (no model). "Validation" here is bibliometric: citation counts (Google Scholar, June 19, 2014), download/web-access statistics, and comparison with peer databases (DIARETDB1 cited 295×; HEI-MED 26×).

---

# 8. Performance Metrics

No diagnostic metrics. Usage metrics: 189 total citations (2008–2013); ~1,324 download requests; visitor counts 54→669 (2008→2013). AUC/sensitivity/specificity/F1/κ: [NOT REPORTED].

---

# 9. Authors' Claims

- Public databases are precious tools enabling development, testing, and quantitative comparison of methods.
- Messidor, despite serving a specialized domain, gathered substantial citations; downloads/web access correlate with citations.
- An automatic validation procedure suffices to handle download requests.
- The images are progressively outdated (acquired before 2007); new databases matching current clinical practice are needed.

---

# 10. Empirical Support Assessment

| Claim | Evidence | Support |
| --- | --- | --- |
| Strong community uptake | 189 citations; download/visitor growth | Supported |
| Downloads correlate with citations | parallel ~3× growth 2011→2013 | Supported (descriptive correlation) |
| Images becoming outdated | acquired pre-2007; modern cameras higher-res | Supported (factual) |

Descriptive/observational; no inferential statistics or CIs. Adequate for a usage-feedback note.

---

# 11. Internal Validity

- No model → no overfitting/leakage concerns.
- Citation/download counts are confounded (non-research downloads, search-engine indexing); authors acknowledge the link to research contribution "is not necessarily simple to apprehend."

---

# 12. External Validity

- Messidor acquired with a single camera model (Topcon TRC NW6) at 3 French departments → limited device/population diversity, relevant to device-domain-shift framing.
- Findings about database-uptake generalize as guidance for other medical-imaging databases (authors' stated intent).

---

# 13. Strengths

- Authoritative, citable description of Messidor acquisition (Topcon TRC NW6, 45° FOV, 1,200 images, resolutions, dilation split).
- Transparent bibliometric reporting and database-design recommendations.

---

# 14. Limitations

**Explicit (authors):** Images progressively outdated (pre-2007 acquisition); link between downloads/web-access and actual research contribution is imperfect; only two new comparable databases (HEI-MED, e-ophtha) released after 2010.

**Implicit:** Single-camera, single-country acquisition; no per-grade image distribution in this note; no lesion-level annotation described here (that lives in the original Messidor documentation, not this feedback paper).

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| Preprocessing-dominance | Peripheral | Acquisition only. |
| Cross-database generalization | Supporting | Source-domain descriptor for Messidor; Exp 3/5 use Messidor-2 (distinct). |
| **Messidor benchmarking** | **Core (provenance)** | Citable descriptor for Messidor camera (Topcon TRC NW6) and acquisition (§4.1, §4.4, §4.6, INTRO). |
| Device domain shift | Supporting | Single-camera acquisition; multi-resolution. |
| Explainability / ViT | Peripheral | N/A. |

**Risk of contradiction:** None. Cite as **#48** Messidor descriptor; explicitly distinguish Messidor (1,200) from Messidor-2 (1,748) wherever cited.

---

# 16. Citation-Ready Statements

1. "The 1200 eye fundus color numerical images of the posterior pole for the MESSIDOR database were acquired by 3 ophthalmologic departments using a color video 3CCD camera on a Topcon TRC NW6 non-mydriatic retinograph with a 45 degree field of view." (The Messidor Database)
2. "800 images were acquired with pupil dilation (one drop of Tropicamide at 0.5%) and 400 without dilation." (The Messidor Database)
3. "The Messidor database … was created by the Messidor project in order to evaluate automatic lesion segmentation and diabetic retinopathy grading methods." (Abstract)
4. "The number of web site visitors, as well as the number of download requests, seem to be correctly correlated with the number of citations." (Conclusion)
5. "They were acquired before 2007, and modern fundus cameras offer increasing image resolutions and sensitivities … This stresses the importance of new databases, corresponding to the current clinical practice." (Conclusion)

---

# 17. Epistemic Classification

**Dataset descriptor (provenance reference).**

**Justification:** The paper is the citable feedback/descriptor for the Messidor database, documenting acquisition hardware and parameters that characterize a benchmark the dissertation references for cross-dataset framing. No ML-benchmark value; its weight is provenance/curation.

---

# 18. Analytical Synthesis

This source provides the citable provenance and acquisition characteristics of the Messidor database (Topcon TRC NW6, 45° FOV, 1,200 posterior-pole images, mixed dilation, multi-resolution 8-bit capture). For the dissertation it grounds §4.1 dataset characterization and §1.2.3/§4.7 device-variability framing, and supplies the camera-model fact used when discussing Messidor-family acquisition. It is bibliometric in its main thrust and presents no diagnostic-model metrics, so it is neutral to the preprocessing-dominance hypothesis and offers no cross-dataset robustness evidence. The critical handling note is the Messidor vs Messidor-2 distinction: the dissertation's transfer/degradation experiments use Messidor-2 (1,748 images), so this descriptor must be cited for Messidor-family provenance without importing the 1,200 count into Messidor-2 contexts. Use strictly as the Messidor descriptor (#48).

End of Literature Card.
