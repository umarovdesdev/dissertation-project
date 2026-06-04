# 1. Bibliographic Metadata

**Full citation (APA 7)**
Cheplygina, V., de Bruijne, M., & Pluim, J. P. W. (2018). *Not-so-supervised: A survey of semi-supervised, multi-instance, and transfer learning in medical image analysis*. [Preprint]. arXiv. 

**DOI:** [NOT REPORTED]

**Journal (+ publisher):** Preprint submitted to Elsevier; arXiv preprint. 

**Year:** 2018 

**Publication type:** Review / survey article. 

**Research domain classification:** Medical image analysis; machine learning; semi-supervised learning (SSL); multiple instance learning (MIL); transfer learning (TL). 

---

# 2. Study Type Classification

| Category                        | Status | Justification                                                                 |
| ------------------------------- | ------ | ----------------------------------------------------------------------------- |
| CNN-based classification study  | ❌      | Survey of learning paradigms; not an original CNN classification experiment.  |
| External validation study       | ❌      | No original validation study conducted.                                       |
| Cross-dataset validation        | ❌      | Discusses prior literature; does not perform cross-dataset evaluation itself. |
| EyePACS benchmarking            | ❌      | EyePACS benchmarking not reported in provided article text.                   |
| Messidor benchmarking           | ❌      | Not reported.                                                                 |
| IDRiD lesion-level study        | ❌      | Not reported.                                                                 |
| Vision Transformer application  | ❌      | Vision Transformers are not discussed in the provided article text.           |
| Clinical prospective validation | ❌      | No prospective clinical study reported.                                       |

---

# 3. Research Problem

**Specific problem addressed**

The article addresses the challenge that medical image analysis often suffers from limited labeled data and reviews three learning paradigms that reduce dependence on fully annotated datasets:

1. Semi-supervised learning (SSL)
2. Multiple instance learning (MIL)
3. Transfer learning (TL)

The authors aim to:

* Provide an overview of these learning scenarios.
* Describe connections among them.
* Identify research gaps.
* Discuss opportunities for future research. 

**Mapped problem categories**

* Generalization ✔
* Clinical applicability ✔
* Preprocessing ❌ (not a primary focus)
* Explainability ❌
* Device/domain shift ✔ (via transfer learning discussion)
* Lesion segmentation ✔ (reviewed applications)
* Class imbalance ❌
* Architecture scaling ❌

**Explicitly not focused on**

* Active learning (covered only marginally). 
* Crowdsourcing. 
* Detailed comparison of specific classifiers. 

---

# 4. Datasets Used

This article is a survey and does **not** introduce or evaluate a single experimental dataset.

| Dataset                           | Public/Private | Sample Size    | Task                      | Split          | External Dataset | Cross-Dataset Testing |
| --------------------------------- | -------------- | -------------- | ------------------------- | -------------- | ---------------- | --------------------- |
| [NOT APPLICABLE – Review Article] | [NOT REPORTED] | [NOT REPORTED] | Multiple reviewed studies | [NOT REPORTED] | [NOT REPORTED]   | [NOT REPORTED]        |

The paper summarizes prior studies across brain imaging, retinal imaging, breast imaging, lung imaging, abdominal imaging, histology, microscopy, and other medical domains.  

---

# 5. Preprocessing Pipeline

Because this is a survey article, no single preprocessing pipeline is proposed or evaluated.

| Component               | Status         |
| ----------------------- | -------------- |
| Resizing/resolution     | [NOT REPORTED] |
| Normalization           | [NOT REPORTED] |
| Data augmentation       | [NOT REPORTED] |
| CLAHE                   | [NOT REPORTED] |
| CLAHE parameters        | [NOT REPORTED] |
| Color normalization     | [NOT REPORTED] |
| Illumination correction | [NOT REPORTED] |
| Flat-field correction   | [NOT REPORTED] |
| FOV crop                | [NOT REPORTED] |
| FOV mask                | [NOT REPORTED] |
| Image-quality filtering | [NOT REPORTED] |
| Lesion enhancement      | [NOT REPORTED] |

---

# 6. Model Architecture

Not applicable as an original model-development study.

| Item                       | Value          |
| -------------------------- | -------------- |
| Architecture(s)            | [NOT REPORTED] |
| Pretraining source         | [NOT REPORTED] |
| Transfer-learning protocol | [NOT REPORTED] |
| Input resolution           | [NOT REPORTED] |
| Final layer                | [NOT REPORTED] |
| Parameter count            | [NOT REPORTED] |
| Loss function              | [NOT REPORTED] |
| Optimizer                  | [NOT REPORTED] |
| Learning rate              | [NOT REPORTED] |
| Scheduler                  | [NOT REPORTED] |
| Batch size                 | [NOT REPORTED] |
| Epochs                     | [NOT REPORTED] |
| Ensemble                   | [NOT REPORTED] |

---

# 7. Validation Design

**Study design:** Literature survey/review.

**Internal split only:** ❌
**k-fold CV:** ❌
**External validation:** ❌
**Multi-center:** ❌
**Prospective:** ❌

**Confidence intervals reported:** Not applicable.

**Statistical testing reported:** Not applicable.

**Overfitting addressed:** Not applicable.

---

# 8. Performance Metrics

The article does not report original experimental performance metrics.

| Metric                   | Status         |
| ------------------------ | -------------- |
| Accuracy                 | [NOT REPORTED] |
| AUC                      | [NOT REPORTED] |
| Sensitivity              | [NOT REPORTED] |
| Specificity              | [NOT REPORTED] |
| F1-score                 | [NOT REPORTED] |
| Cohen's Kappa            | [NOT REPORTED] |
| Quadratic Weighted Kappa | [NOT REPORTED] |
| Calibration metrics      | [NOT REPORTED] |
| Confusion matrix counts  | [NOT REPORTED] |

---

# 9. Authors' Claims

* Lack of labeled data is a major obstacle in medical image analysis. 
* SSL, MIL, and TL provide mechanisms to learn from less supervision or alternative supervision. 
* These learning scenarios are related but are often studied separately. 
* Greater interaction between these paradigms could benefit the field. 
* Medical image analysis provides many naturally occurring SSL, MIL, and TL settings.  

---

# 10. Empirical Support Assessment

| Claim                                                 | Support Assessment                                                                   |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Labeled data scarcity is important in medical imaging | Supported by broad literature surveyed, but not tested experimentally in this paper. |
| SSL, MIL, and TL are useful alternatives              | Supported through numerous cited studies summarized in review tables.                |
| Connections exist between paradigms                   | Conceptually argued throughout the survey.                                           |
| Increased integration across paradigms is desirable   | Presented as an expert synthesis rather than experimentally demonstrated evidence.   |

**Generalization/robustness verdict:** The article provides a broad literature-based argument but does not contribute new empirical evidence for generalization or robustness claims.

---

# 11. Internal Validity

* Overfitting risk: Not applicable.
* Data leakage risk: Not applicable.
* Balancing/sampling effects: Not applicable.
* Augmentation inflation: Not applicable.
* Metric reliability: Depends on reviewed studies; not evaluated systematically.
* Preprocessing–architecture confounding: Not analyzed.

As a review, validity depends on completeness and accuracy of literature selection rather than experimental design. The paper explicitly states its selection process. 

---

# 12. External Validity

* Population transferability: Not directly evaluated.
* Single vs multi-source evidence: Multi-source literature survey across many medical domains.  
* Real-world feasibility: Discussed through reviewed applications.
* Hardware dependency: [NOT REPORTED]

The review has broad disciplinary coverage, increasing conceptual external validity.

---

# 13. Strengths

* Integrates SSL, MIL, and TL within one framework. 
* Covers both diagnosis and segmentation applications. 
* Provides formal definitions of learning scenarios. 
* Includes extensive tabular summaries of prior work.  
* Explicitly discusses relationships between paradigms. 

---

# 14. Limitations

### Explicit (authors state)

* The survey is not intended to provide a complete summary of all related papers. 
* Active learning and crowdsourcing are not covered in detail. 
* Focus is limited primarily to classification-related medical imaging scenarios. 

### Implicit (observed)

* No original empirical validation.
* No quantitative meta-analysis.
* No systematic quality assessment of included studies.
* No direct comparison between CNNs and Vision Transformers.
* No dedicated analysis of retinal DR benchmarks such as EyePACS, IDRiD, or Messidor.

---

# 15. Relevance to My Dissertation

| Dissertation Axis                          | Relevance  | Notes                                                                                   |
| ------------------------------------------ | ---------- | --------------------------------------------------------------------------------------- |
| Preprocessing-dominance hypothesis         | Peripheral | Preprocessing is not a central topic.                                                   |
| Cross-database generalization              | Supporting | Transfer learning section discusses domain adaptation and dataset shift.                |
| CNN vs ViT comparison                      | Peripheral | Vision Transformers not discussed.                                                      |
| EyePACS benchmarking                       | Peripheral | Not reported.                                                                           |
| Messidor benchmarking                      | Peripheral | Not reported.                                                                           |
| IDRiD benchmarking                         | Peripheral | Not reported.                                                                           |
| Explainability (Grad-CAM IoU/ALO)          | Peripheral | Not discussed.                                                                          |
| Device domain shift / clinical degradation | Supporting | Domain differences due to scanners and acquisition protocols are explicitly discussed.  |

**Risk of contradicting preprocessing-driven generalization thesis:** Low. The paper emphasizes transfer learning and domain adaptation but does not present evidence against preprocessing-based generalization.

---

# 16. Citation-Ready Statements

1. “A frequent problem when applying machine learning methods to medical images is the lack of labeled data.” (Introduction, p. 1) 

2. “The lack of labeled data motivates approaches that go beyond traditional supervised learning by incorporating other data and/or labels that might be available.” (Introduction, p. 1) 

3. “We aim to provide an overview of the learning scenarios, describe their connections, identify gaps in the current approaches, and provide several opportunities for future research.” (Introduction, p. 1) 

4. “In semi-supervised learning, in addition to the training set we have an unlabeled set of data U.” (Section 2, p. 2) 

5. “Transfer learning” addresses situations where training and test data originate from different domains and/or different tasks. (Section 5, pp. 10–11) 

---

# 17. Epistemic Classification

**Foundational**

**Justification:** The article is a broad conceptual survey that formalizes and synthesizes three major weak-supervision paradigms (SSL, MIL, TL) in medical image analysis. It is not a benchmark paper, architecture paper, dataset paper, or clinical validation study. Its primary contribution is theoretical organization and literature integration. 

---

# 18. Analytical Synthesis

This study does not directly influence the empirical positioning of a diabetic retinopathy classification dissertation because it provides no original retinal benchmark results, preprocessing experiments, or CNN-versus-transformer comparisons. Its value lies in framing learning under limited annotation regimes and in discussing transfer learning under domain shift. The transfer-learning sections are relevant to arguments about cross-database generalization, especially when moving between retinal datasets acquired under different imaging conditions. However, the article neither supports nor refutes a preprocessing-dominance hypothesis because preprocessing is not analyzed as an experimental variable. Likewise, it does not address Grad-CAM lesion localization, explainability metrics, or retinal lesion overlap evaluation. For a DR dissertation, the paper functions primarily as a conceptual background reference for domain adaptation and learning with limited labels rather than as direct evidence regarding retinal diagnostic performance. Its epistemic role is foundational rather than benchmark-defining.

End of Literature Card.
