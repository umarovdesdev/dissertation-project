# Literature Card: Tabari et al. (2024) — FHIR Data Models Scoping Review

---

## ⚠️ CRITICAL DOMAIN MISMATCH NOTICE

**This article is NOT about diabetic retinopathy, deep learning, or medical image classification.** It is a systematic scoping review of FHIR-based data models for healthcare interoperability. Many sections of the standard DR/AI Literature Card template are inapplicable and are marked as **[NOT APPLICABLE — DOMAIN MISMATCH]**. The card is completed in full where the template sections can be meaningfully adapted.

---

# 1. Bibliographic Metadata

- **Full citation (APA 7):** Tabari, P., Costagliola, G., De Rosa, M., & Boeker, M. (2024). Best practices for implementation and development of data models and structures based on FHIR: A systematic scoping review. *JMIR Preprints*. https://doi.org/10.2196/preprints.58445
- **DOI:** 10.2196/preprints.58445
- **Journal / Conference:** JMIR Medical Informatics (submitted); currently hosted as JMIR Preprint
- **Year:** 2024 (submitted March 17, 2024)
- **Publication type:** Systematic scoping review (unpublished, non-peer-reviewed preprint)
- **Research domain classification:** Health informatics; healthcare interoperability; FHIR data modeling; clinical data standardization

---

# 2. Study Type Classification

- **Systematic review:** Yes — systematic scoping review following PRISMA-ScR guidelines
- **External validation study:** No
- **Cross-dataset validation:** No
- **EyePACS benchmarking:** No
- **Messidor benchmarking:** No
- **IDRiD lesion-level study:** No
- **Vision Transformer application:** No
- **CNN-based classification study:** No
- **Meta-analysis:** No
- **Clinical prospective validation:** No

**Justification:** This is a systematic scoping review that synthesizes 27 primary studies on FHIR-based data models and infrastructures in healthcare. It follows the PRISMA-ScR methodology and does not involve any original empirical experimentation, model training, or image-based AI.

---

# 3. Research Problem

- **Specific problem addressed:** The lack of a comprehensive assessment of data models and infrastructures using the HL7 FHIR standard for healthcare interoperability. The authors aim to identify best practices, tools, mappings, and limitations in developing FHIR-based data models.
- **Related to:**
  - **Generalization?** Partially — the review addresses scalability and generalizability challenges of FHIR-based data models across healthcare settings.
  - **Preprocessing?** No (not image preprocessing).
  - **Architecture scaling?** No (not neural network architecture).
  - **Lesion detection?** No.
  - **Clinical deployment?** Indirectly — the review examines clinical data interoperability as a prerequisite for deploying health IT systems, including AI-ready data pipelines.

---

# 4. Datasets Used

This is a scoping review. No imaging datasets were used. The "dataset" is the corpus of 27 included primary studies.

- **Search sources:** PubMed, Scopus, Web of Science, IEEE Xplore, ACM Digital Library, Google Scholar
- **Total records identified:** 466
- **Duplicates removed:** 238
- **Records screened:** 228
- **Full-text assessed:** 108
- **Studies included:** 27
- **External dataset used?** Not applicable
- **Cross-dataset testing performed?** Not applicable

---

# 5. Preprocessing Pipeline

**[NOT APPLICABLE — DOMAIN MISMATCH]**

This study does not involve image data or any image preprocessing pipeline. No resizing, cropping, normalization, CLAHE, color normalization, augmentation, image quality filtering, or lesion enhancement methods are reported or relevant.

---

# 6. Model Architecture

**[NOT APPLICABLE — DOMAIN MISMATCH]**

No deep learning or classification model architecture was developed or evaluated. The review discusses NLP tools (cTAKES, MedXN, MedTime, NLP2FHIR pipeline) and machine learning algorithms (SVM, random forest, logistic regression, decision tree, deep neural networks, GCN, CNN) used in some of the 27 included studies for tasks such as EHR phenotyping and cancer prediction — but these are summarized from the reviewed papers, not developed by the authors.

---

# 7. Validation Design

- **Internal validation only?** Not applicable — this is a scoping review.
- **Cross-validation?** Not applicable.
- **External validation?** Not applicable.
- **Prospective validation?** Not applicable.
- **Multi-center validation?** Not applicable.

**Review methodology validation:** Two reviewers (PT and MDR) independently screened articles with consensus resolution. Critical appraisal of each study was conducted for methodological appropriateness. Final analysis reviewed by all co-authors.

---

# 8. Performance Metrics

**[NOT APPLICABLE — DOMAIN MISMATCH]**

No AUC, sensitivity, specificity, accuracy, F1, Cohen's Kappa, or confusion matrices are reported by this review as its own outputs. The review notes that several included studies used Precision, Recall, F1, AUROC, and AUPRC as evaluation metrics for their NLP/ML components, but these are not synthesized quantitatively (no meta-analysis).

---

# 9. Authors' Claims

1. **FHIR is a promising standard** for developing interoperable data models and infrastructures, despite challenges in the development phase.
2. **Two main categories** of FHIR data models were identified: pipeline-based (21/27 studies) and non-linear data models (6/27 studies).
3. **Most frequently used FHIR resources** were Observation (19 articles), Patient (16), and Condition (16).
4. **Key challenges** were categorized into five areas: data integration, interoperability, data standardization, performance, and scalability/generalizability.
5. **FHIR can be integrated with other health-related standards** (OMOP, SNOMED-CT, LOINC, ICD-10, etc.) to enhance interoperability.
6. **No prior review** had comprehensively assessed FHIR-based data models and infrastructures specifically.
7. The authors propose a **high-level workflow for developing FHIR-based models** from initial steps to final phase.

---

# 10. Empirical Support Assessment

- **Does data support generalization claims?** The review is qualitative; claims about FHIR's promise are supported by narrative synthesis of 27 studies but no meta-analytic pooling.
- **Is external validation robust?** Not applicable to this study type.
- **Are confidence intervals reported?** No — no quantitative synthesis performed.
- **Is dataset size adequate?** 27 included studies is a modest corpus for a scoping review; the authors acknowledge this as a limitation.
- **Is class imbalance addressed?** Not applicable.
- **Is statistical testing adequate?** No statistical testing was performed; this is a narrative/qualitative scoping review, which is appropriate for the stated objectives.

---

# 11. Internal Validity

- **Overfitting risk:** Not applicable (no model training).
- **Dataset leakage risk:** Not applicable.
- **Confounders:** Selection bias is possible — only English-language articles with specific disease contexts and at least one architecture diagram were included. This excludes general-purpose FHIR models and non-English research.
- **Augmentation inflation risk:** Not applicable.
- **Metric reliability:** Not applicable.
- **Formula correctness:** Not applicable.

**Methodological concern:** The inclusion criterion requiring "at least one informative model/infrastructure visualization" may bias the review toward better-documented studies, potentially excluding valid but poorly illustrated implementations.

---

# 12. External Validity

- **Cross-population transferability:** The review covers diverse medical domains (chronic diseases, COVID-19, cancer, intensive care, maternal health), providing reasonable breadth.
- **Dataset portability:** The review discusses portability challenges extensively, noting issues with hard-coded mappings, synchronization, and SNOMED-CT licensing.
- **Clinical feasibility:** Several included studies were deployed in clinical settings (Mayo Clinic, German cancer registries, Chilean COVID-19 reporting), providing some evidence of real-world feasibility.
- **Hardware constraints:** Not discussed (not relevant to this study type).

---

# 13. Strengths

1. Follows PRISMA-ScR guidelines with transparent search strategy and PRISMA flow diagram.
2. Comprehensive search across six databases (PubMed, Scopus, Web of Science, IEEE Xplore, ACM, Google Scholar) with no time limit.
3. Dual-reviewer screening with consensus resolution and co-author verification.
4. Useful categorization into pipeline-based vs. non-linear data models.
5. Systematic extraction of FHIR resources, tools, technologies, standards, and mappings across all 27 studies.
6. FHIR resource frequency analysis provides actionable insight for future developers.
7. Comprehensive categorization of limitations into five domains (data integration, interoperability, standardization, performance, scalability/generalizability).
8. Proposed high-level workflow for FHIR-based modeling derived from empirical patterns in the literature.
9. Comparison with 11 existing FHIR review articles to position the contribution.

---

# 14. Limitations

## Explicit (stated by authors)

1. Only articles dealing with specific disease real-world data were included; general-purpose FHIR data models were excluded, potentially introducing bias in resources and methodologies observed.
2. Only English-language articles were included.
3. Grey literature was not thoroughly analyzed.
4. The relatively small number of included articles (n=27) may limit generalizability to the entire field of FHIR data modeling.

## Implicit (methodological)

1. **Preprint status:** This manuscript is an unpublished, non-peer-reviewed preprint. Findings should be treated with appropriate caution.
2. **No quality scoring:** No formal quality assessment tool (e.g., AMSTAR, Newcastle-Ottawa) was applied to the included studies; only narrative appraisal was performed.
3. **No quantitative synthesis:** Despite some studies reporting P, R, F1, AUROC metrics, no meta-analytic pooling was attempted, limiting the ability to draw quantitative conclusions about FHIR model performance.
4. **Search conducted in May 2023:** Given rapid FHIR adoption, studies published after this date are not captured.
5. **Inclusion criterion requiring architecture diagrams** may bias toward more elaborately documented studies.
6. **Limited risk-of-bias assessment** for individual included studies.

---

# 15. Relevance to My Dissertation

**Assessment: This article has NO direct relevance to a dissertation on diabetic retinopathy deep learning, preprocessing dominance, cross-database validation, EyePACS/Messidor benchmarking, or Vision Transformer comparison.**

- **Relevance to preprocessing dominance hypothesis:** None. The paper does not address image preprocessing.
- **Relevance to cross-database validation:** None. No imaging cross-dataset validation is performed.
- **Relevance to EyePACS/Messidor benchmarking:** None.
- **Relevance to Vision Transformer comparison:** None.
- **Risk of contradiction:** None — the domains do not overlap.

**Potential tangential relevance:** If the dissertation discusses clinical deployment infrastructure or data interoperability as a downstream consideration for DR AI systems (e.g., integrating DR screening results into EHR systems via FHIR), this paper could provide background context on FHIR-based data models. However, this would be peripheral at best.

---

# 16. Citation-Ready Statements

1. Tabari et al. (2024) conducted a PRISMA-ScR systematic scoping review of 27 studies implementing FHIR-based data models, categorizing them into pipeline-based (n=21) and non-linear (n=6) architectures.

2. The most frequently used FHIR resources across the 27 reviewed studies were Observation (n=19), Patient (n=16), and Condition (n=16) (Tabari et al., 2024).

3. Tabari et al. (2024) identified five categories of challenges in FHIR-based data model development: data integration, interoperability, data standardization, performance, and scalability/generalizability.

4. According to Tabari et al. (2024), FHIR-based data normalization pipelines such as NLP2FHIR were used in four of the reviewed studies for standardizing unstructured EHR data into interoperable formats.

5. Tabari et al. (2024) found that the year 2021 had the highest number of FHIR data model publications (10 articles), suggesting accelerating adoption during the COVID-19 pandemic period.

**Note:** Page numbers are not consistently available due to preprint formatting. All statements derive from the body text of the manuscript.

---

# 17. Epistemic Classification

**Classification: Peripheral**

**Justification:** This systematic scoping review addresses healthcare data interoperability standards (FHIR), which is entirely outside the domain of diabetic retinopathy deep learning, image preprocessing, model architecture comparison, or cross-dataset validation. It has no bearing on the core epistemic questions of a DR AI dissertation. It could only be classified as peripheral background if the dissertation briefly addresses clinical deployment infrastructure for DR screening AI systems.

---

# 18. Analytical Synthesis

This scoping review by Tabari et al. (2024) provides a structured overview of FHIR-based data models in healthcare but operates in an entirely different epistemic domain from diabetic retinopathy deep learning research. Its epistemic weight for a DR AI dissertation is negligible, as it addresses data interoperability standards rather than image classification, preprocessing pipelines, or model generalization. The review does not strengthen or weaken the preprocessing-dominance argument, as it does not engage with image preprocessing in any form. It demonstrates no cross-dataset robustness relevant to imaging benchmarks. The only conceivable connection to a DR dissertation would be if FHIR served as the interoperability layer for deploying DR screening results into clinical EHR systems, but even this would be a distant downstream concern rather than a core methodological issue. The preprint status further limits its citability for formal academic purposes. This article should not be included in a DR-focused literature review unless the dissertation explicitly addresses health informatics infrastructure for AI deployment.

---

*End of Literature Card.*
