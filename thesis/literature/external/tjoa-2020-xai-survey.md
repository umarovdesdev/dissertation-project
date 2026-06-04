# 1. Bibliographic Metadata

**Full citation (APA 7):**
Tjoa, E., & Guan, C. (2020). *A Survey on Explainable Artificial Intelligence (XAI): towards Medical XAI*. arXiv preprint arXiv:1907.07374v5. 

**DOI:** [NOT REPORTED]

**Journal (+ publisher):** [NOT REPORTED; manuscript formatted as an arXiv preprint]

**Year:** 2020 (arXiv version dated 11 Aug 2020) 

**Publication type:** Survey / Narrative Review

**Research domain classification:** Explainable Artificial Intelligence (XAI), Machine Learning Interpretability, Medical AI Explainability. 

---

# 2. Study Type Classification

| Category                        | Status | Justification                                                                                        |
| ------------------------------- | ------ | ---------------------------------------------------------------------------------------------------- |
| CNN-based classification study  | ❌      | The article is a survey of interpretability methods, not an original CNN classification experiment.  |
| External validation study       | ❌      | No external validation experiment is conducted.                                                      |
| Cross-dataset validation        | ❌      | No original dataset transfer study is reported.                                                      |
| EyePACS benchmarking            | ❌      | Not reported.                                                                                        |
| Messidor benchmarking           | ❌      | Not reported.                                                                                        |
| IDRiD lesion-level study        | ❌      | Not reported.                                                                                        |
| Vision Transformer application  | ❌      | Vision Transformers are not discussed in the retrieved article sections.                             |
| Clinical prospective validation | ❌      | No prospective clinical validation study is presented.                                               |

---

# 3. Research Problem

**Specific problem addressed**

The article reviews and categorizes explainability and interpretability methods in machine learning and then applies the same framework to medical AI, with emphasis on accountability, transparency, and reliability of machine-learning systems in medicine.  

**Mapped problem categories**

* Explainability ✔
* Clinical applicability ✔
* Interpretability taxonomy ✔
* Accountability and transparency ✔
* Medical AI adoption ✔

**Explicitly not focused on**

* Diabetic retinopathy classification
* Cross-dataset generalization
* Domain shift
* Class imbalance
* CNN architecture optimization
* Lesion segmentation benchmarking
* Vision Transformer evaluation
* Image preprocessing pipelines

All above are not stated as primary objectives in the survey. 

---

# 4. Datasets Used

This article is a survey and does not conduct a primary experimental study.

| Dataset          | Public/Private | Sample Size    | Task           | Train/Val/Test | External Dataset | Cross-Dataset Testing |
| ---------------- | -------------- | -------------- | -------------- | -------------- | ---------------- | --------------------- |
| [NOT APPLICABLE] | [NOT REPORTED] | [NOT REPORTED] | Survey article | [NOT REPORTED] | [NOT REPORTED]   | [NOT REPORTED]        |

The paper references datasets from cited studies (e.g., PASCAL VOC 2009, AudioMNIST, Human Connectome Project), but these belong to reviewed literature rather than a dataset used by the survey itself. 

---

# 5. Preprocessing Pipeline

Because this is a survey article rather than an experimental model paper:

| Item                    | Status         |
| ----------------------- | -------------- |
| Resizing/resolution     | [NOT REPORTED] |
| Normalization           | [NOT REPORTED] |
| Augmentation            | [NOT REPORTED] |
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

**Architecture(s):** [NOT APPLICABLE — survey article]

| Component                  | Status         |
| -------------------------- | -------------- |
| Architecture               | [NOT REPORTED] |
| Pretraining source         | [NOT REPORTED] |
| Transfer learning protocol | [NOT REPORTED] |
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

**Validation design:** Not applicable; survey/review article.

**Internal split only:** ❌
**Cross-validation:** ❌
**External validation:** ❌
**Multi-center validation:** ❌
**Prospective validation:** ❌

**Confidence intervals reported:** [NOT REPORTED]

**Statistical tests reported:** [NOT REPORTED]

**Overfitting addressed:** [NOT REPORTED]

---

# 8. Performance Metrics

No original predictive model is evaluated.

**Accuracy:** [NOT REPORTED]
**AUC:** [NOT REPORTED]
**Sensitivity:** [NOT REPORTED]
**Specificity:** [NOT REPORTED]
**F1-score:** [NOT REPORTED]
**Cohen's Kappa:** [NOT REPORTED]
**Quadratic Weighted Kappa:** [NOT REPORTED]
**Calibration metrics:** [NOT REPORTED]
**Confusion matrix counts:** [NOT REPORTED]

The article discusses interpretability methodologies rather than reporting classification performance metrics. 

---

# 9. Authors' Claims

* Interpretability and explainability have become critical issues for machine learning, particularly in medicine. 
* Existing interpretability approaches can be categorized into distinct classes. 
* The proposed categorization can help clinicians and practitioners understand different forms of interpretability. 
* Many machine-learning publications assume interpretability without conducting human-subject validation. 
* Medical AI interpretability requires caution and stronger consideration of clinical practice. 

---

# 10. Empirical Support Assessment

| Claim                                                     | Support Assessment                                                                       |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Interpretability is important in medicine                 | Supported through literature review and examples, but not through new empirical data.    |
| Interpretability methods can be categorized               | Supported descriptively by the survey taxonomy presented throughout Section II.          |
| Many papers assume interpretability without human testing | Supported by the authors' tabulation (HSI column) of surveyed studies.                   |
| Categorization is useful for clinicians                   | Plausible conceptual claim; no direct user-study evidence reported by the survey itself. |

**Generalization/robustness verdict:** The article does not present original experimental evidence for robustness or generalization claims; conclusions are primarily literature-based and conceptual.

---

# 11. Internal Validity

Because the article is a survey:

* Overfitting risk: Not applicable.
* Data leakage risk: Not applicable.
* Balancing/sampling effects: Not applicable.
* Augmentation inflation: Not applicable.
* Metric reliability: Not applicable.
* Preprocessing–architecture confounding: Not applicable.

Methodological consideration:

* The taxonomy depends on authors' categorization choices.
* No formal quantitative meta-analysis is reported.
* No systematic review protocol is described in the retrieved sections.

---

# 12. External Validity

* Population transferability: Not applicable.
* Single-source vs multi-source evidence: Multi-source literature review.
* Real-world feasibility: Intended to inform practical medical AI deployment. 
* Hardware dependency: Not reported.

---

# 13. Strengths

* Provides a structured taxonomy of XAI approaches. 
* Explicitly bridges general XAI literature and medical AI applications. 
* Reviews both perceptive interpretability and mathematical-structure interpretability. 
* Includes discussion of saliency, signal methods, verbal explanations, feature extraction, sensitivity, and predefined models. 
* Highlights lack of human-subject validation in many interpretability studies. 

---

# 14. Limitations

### Explicit (authors state)

* The survey does not attempt to cover all related work. 
* Different definitions of interpretability remain difficult to reconcile. 
* Existing interpretability frameworks lack uniform adoption. 

### Implicit (observed)

* No systematic-review methodology reported in retrieved sections.
* No quantitative synthesis or meta-analysis.
* No empirical validation of the proposed taxonomy.
* No diabetic retinopathy–specific analysis.
* No benchmarking of explainability methods on a common dataset.

---

# 15. Relevance to My Dissertation

| Dissertation Axis                          | Relevance  |
| ------------------------------------------ | ---------- |
| Preprocessing-dominance hypothesis         | Peripheral |
| Cross-database generalization              | Peripheral |
| CNN vs Vision Transformer comparison       | Peripheral |
| EyePACS/Messidor/IDRiD/APTOS benchmarking  | Peripheral |
| Explainability (Grad-CAM, IoU, ALO)        | Core       |
| Device domain shift / clinical degradation | Supporting |

**Risk of contradicting preprocessing-driven generalization thesis:** None observed. The article does not evaluate preprocessing pipelines or cross-domain DR performance.

**Most relevant contribution:** Conceptual justification for explainability requirements in medical AI and discussion of saliency-map-based explanations (CAM, Grad-CAM, LRP, LIME).  

---

# 16. Citation-Ready Statements

1. “Interpretability and explainability of ML algorithms have thus become pressing issues.” (Introduction, p. 1) 

2. “The blackbox nature of deep learning is still unresolved, and many machine decisions are still poorly understood.” (Abstract, p. 1) 

3. “Visualization is capable of helping researchers detect erroneous reasoning in classification problems.” (Introduction, p. 1) 

4. “Many journal papers in the machine learning and AI community are algorithm-centric” and often assume interpretability without human-subject testing. (Introduction, p. 1–2) 

5. The survey categorizes interpretability into “perceptive interpretability” and “interpretability via mathematical structure.” (Section II, p. 2) 

---

# 17. Epistemic Classification

**Label:** Foundational

**Justification:**
The article provides a broad conceptual framework and taxonomy for explainable AI, particularly in medical contexts, rather than introducing a new predictive architecture, benchmark, dataset, or clinical validation study. Its primary contribution is theoretical organization of the interpretability literature.  

---

# 18. Analytical Synthesis

This article does not materially contribute evidence regarding diabetic retinopathy classification performance, preprocessing effectiveness, cross-dataset transfer, or CNN-versus-Vision-Transformer comparisons. Its value for the dissertation lies almost entirely in the explainability component. The survey provides a structured taxonomy covering saliency-based methods (including CAM, Grad-CAM-related families, LRP, and LIME), signal-based methods, verbal explanations, feature-extraction approaches, and sensitivity-based analyses. It can therefore serve as a theoretical foundation for motivating explainability requirements in automated retinal-disease diagnosis. The article neither strengthens nor weakens the preprocessing-based generalization hypothesis because no preprocessing or domain-shift experiments are performed. Relative to DR benchmarking literature, its epistemic weight is conceptual rather than empirical. It is most appropriate as a foundational citation in the dissertation's explainable-AI and medical-AI interpretability background sections.

End of Literature Card.
