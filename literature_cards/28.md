# LITERATURE CARD

---

# 1. Bibliographic Metadata

**Full citation (APA 7):**
Morya, A. K., Ramesh, P. V., Nishant, P., Kaur, K., Gurnani, B., Heda, A., & Salodia, S. (2024). *Diabetic retinopathy: A review on its pathophysiology and novel treatment modalities*. World Journal of Methodology, 14(4), 95881. [https://doi.org/10.5662/wjm.v14.i4.95881](https://doi.org/10.5662/wjm.v14.i4.95881) 

**DOI:** 10.5662/wjm.v14.i4.95881 

**Journal:** World Journal of Methodology 

**Year:** 2024 

**Publication type:** Narrative Review 

**Research domain classification:**
Clinical Ophthalmology / Pathophysiology of Diabetic Retinopathy / Therapeutic Modalities Review

---

# 2. Study Type Classification

Applicable categories:

* Systematic review → **No**
* Meta-analysis → **No**
* External validation study → **No**
* CNN-based classification study → **No**
* Vision Transformer application → **No**

**Classification:** Narrative review of pathophysiology and treatment modalities.

**Justification:** The article synthesizes prior literature from multiple databases (1990–2022), without original dataset analysis or pooled meta-analysis .

---

# 3. Research Problem

**Problem addressed:**
To summarize the evolving understanding of diabetic retinopathy (DR) pathophysiology and discuss current and emerging treatment strategies.

**Specific focus areas:**

* Pathophysiological cascade (hyperglycemia, AGEs, PKC, oxidative stress, inflammation, neurodegeneration)
* Neurovascular unit involvement
* Current ocular therapies (PRP, anti-VEGF, corticosteroids, vitrectomy)
* Emerging therapeutic approaches
* Artificial intelligence in DR screening

**Relation to:**

* Generalization → No
* Preprocessing → No
* Architecture scaling → No
* Lesion detection → Discussed conceptually (AI), no empirical modeling
* Clinical deployment → Yes (treatment strategies, screening compliance)

---

# 4. Datasets Used

**None.**

This is a narrative review. No datasets were constructed, analyzed, or benchmarked .

External dataset used? → No
Cross-dataset testing performed? → No

---

# 5. Preprocessing Pipeline

Not applicable.

Resizing → [NOT REPORTED]
Cropping → [NOT REPORTED]
Normalization → [NOT REPORTED]
CLAHE → [NOT REPORTED]
Color normalization → [NOT REPORTED]
Augmentation → [NOT REPORTED]
Image quality filtering → [NOT REPORTED]
Lesion enhancement → [NOT REPORTED]

---

# 6. Model Architecture

Not applicable.

Although AI tools (IDxDR, Remidio Medios, DL-based binary classification) are discussed, no architecture details, hyperparameters, loss functions, or training protocols are reported in this article .

---

# 7. Validation Design

Not applicable.

No internal validation
No cross-validation
No external validation
No prospective study
No multi-center empirical study

---

# 8. Performance Metrics

Only secondary reporting of previously published AI systems:

* IDxDR sensitivity ≈ 80%

* IDxDR specificity < 90% 

* Remidio Medios:

  * Sensitivity: 98%
  * Specificity: 86% 

No AUC values reported.
No confidence intervals reported.
No confusion matrices.
No statistical testing performed in this review.

---

# 9. Authors’ Claims

### Performance claims

* AI-based systems demonstrate high sensitivity and specificity in DR detection.
* Anti-VEGF improves visual outcomes in DME and PDR.

### Generalization claims

* AI improves screening efficiency and reduces ophthalmologist workload.

### Clinical applicability claims

* Early detection and interdisciplinary management improve prognosis.
* Recognition of neurovascular unit involvement expands therapeutic targets.

### Superiority claims

* Aflibercept may provide better visual gains than bevacizumab and ranibizumab in poorer baseline vision cases .

---

# 10. Empirical Support Assessment

* No original data presented.
* Generalization claims are not empirically tested in this article.
* AI performance values are cited without reporting study design robustness.
* No confidence intervals provided.
* No discussion of dataset imbalance.
* No statistical comparisons presented.

Conclusion: Empirical support is entirely derivative and depends on cited studies.

---

# 11. Internal Validity

Not applicable (no original study design).

Risks:

* Narrative synthesis bias.
* Selection bias (English-only articles included) .
* No PRISMA or structured systematic methodology described.

---

# 12. External Validity

Since no empirical validation is conducted:

* Cross-population transferability → Not evaluated.
* Dataset portability → Not evaluated.
* Clinical feasibility → Discussed conceptually (AI screening, treatment strategies).
* Hardware constraints → IDxDR noted as bulky and expensive .

---

# 13. Strengths

* Comprehensive pathophysiological synthesis.
* Integration of neurodegeneration concept.
* Clear summary of classification systems (ETDRS, International Clinical DR scale).
* Discussion of emerging therapeutic paradigms.
* Inclusion of AI screening tools in clinical context.

---

# 14. Limitations

### Explicit (stated by authors)

* Need for further research into neurodegenerative mechanisms.
* Anti-VEGF incomplete response (~40–50% non-responders in DME) .

### Implicit (methodological)

* Not systematic.
* No quantitative synthesis.
* No risk-of-bias analysis.
* No structured evidence hierarchy.
* AI discussion lacks architectural or validation depth.

---

# 15. Relevance to My Dissertation

### Preprocessing dominance hypothesis

No direct relevance.

### Cross-database validation

None.

### EyePACS/Messidor benchmarking

None.

### Vision Transformer comparison

None.

### Risk of contradiction

Low — article does not make claims about CNN superiority or preprocessing effects.

Relevance classification: **Background/clinical context only.**

---

# 16. Citation-Ready Statements

1. “Diabetic retinopathy is present in one-third of patients with diabetes.” 
2. “Retinal neurodegeneration may precede microangiopathy in diabetic retinopathy.” 
3. “Only 35%–55% compliance is observed for annual ocular screening.” 
4. “Approximately 40%–50% of eyes with DME do not fully respond to anti-VEGF therapy.” 
5. “Remidio Medios demonstrated 98% sensitivity and 86% specificity.” 

---

# 17. Epistemic Classification

**Classification:** Peripheral / Background Clinical Review

**Justification:**

* No empirical modeling.
* No benchmarking.
* No methodological innovation.
* Provides pathophysiological and therapeutic context only.

Epistemic weight for AI-based dissertation: **Low-to-moderate (contextual support).**

---

# 18. Analytical Synthesis

This article functions as a comprehensive clinical-pathophysiological synthesis rather than a methodological contribution to automated DR diagnosis. It reinforces the concept of DR as a neurovascular unit disorder and highlights the limitations of current therapeutic modalities, particularly incomplete anti-VEGF response. Its discussion of AI remains high-level and does not engage with architecture design, preprocessing pipelines, or cross-dataset validation frameworks. Therefore, it does not materially impact arguments regarding preprocessing dominance or CNN generalization. Its primary utility lies in strengthening the clinical motivation and biological plausibility sections of a dissertation rather than informing experimental design or benchmarking strategy. It does not provide evidence of cross-dataset robustness or architectural superiority.

---

**End of Literature Card.**
