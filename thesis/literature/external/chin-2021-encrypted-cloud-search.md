# 1. Bibliographic Metadata

**Full citation (APA 7)**
Chin, T.-L., & Shih, W.-N. (2021). *Concisely indexed multi-keyword rank search on encrypted cloud documents*. *Applied Sciences, 11*(23), 11529. [https://doi.org/10.3390/app112311529](https://doi.org/10.3390/app112311529) 

**DOI**
10.3390/app112311529 

**Journal**
*Applied Sciences* (MDPI) 

**Year**
2021 

**Publication type**
Empirical methodology study with simulation-based evaluation of a secure searchable-encryption scheme. 

**Research domain classification**
Cloud computing; searchable encryption; information security; encrypted document retrieval; multi-keyword ranked search; dimensionality reduction. 

---

# 2. Study Type Classification

| Category                        | Status | Justification                                                      |
| ------------------------------- | ------ | ------------------------------------------------------------------ |
| CNN-based classification study  | ❌      | No CNN model is used; study focuses on encrypted document search.  |
| External validation study       | ❌      | No external validation framework reported.                         |
| Cross-dataset validation        | ❌      | Only one text-document corpus is evaluated.                        |
| EyePACS benchmarking            | ❌      | EyePACS not used.                                                  |
| Messidor benchmarking           | ❌      | Messidor not used.                                                 |
| IDRiD lesion-level study        | ❌      | IDRiD not used.                                                    |
| Vision Transformer application  | ❌      | No transformer architecture involved.                              |
| Clinical prospective validation | ❌      | No clinical study conducted.                                       |

---

# 3. Research Problem

**Specific problem addressed**

The study addresses secure multi-keyword ranked search over encrypted cloud documents while reducing storage and computational costs caused by long document indexes. The proposed Condensed Index Multi-keyword Search (CIMS) scheme combines dimensionality reduction via PCA with searchable encryption. (Sections 1, 4) 

**Problem categories**

* Secure searchable encryption ✔
* Cloud document retrieval ✔
* Multi-keyword ranked search ✔
* Index compression / dimensionality reduction ✔
* Computational efficiency ✔

**Mapped categories from dissertation taxonomy**

* Generalization: ❌
* Class imbalance: ❌
* Architecture scaling: ❌
* Lesion segmentation: ❌
* Clinical applicability: ❌
* Preprocessing: ❌ (not image preprocessing; PCA-based index reduction)
* Explainability: ❌
* Device shift: ❌

**Explicitly not focused on**

* Medical imaging
* Diabetic retinopathy
* CNN classification
* Vision Transformers
* Clinical deployment
* Explainable AI
* Cross-domain robustness
* Lesion detection/segmentation

All absent from the article. 

---

# 4. Datasets Used

| Dataset     | Public/Private | Sample Size    | Task Type                 | Train/Val/Test Split | External Dataset | Cross-Dataset Testing | Class Balancing |
| ----------- | -------------- | -------------- | ------------------------- | -------------------- | ---------------- | --------------------- | --------------- |
| BBC Dataset | Public         | 2250 documents | Document retrieval/search | [NOT REPORTED]       | No               | No                    | [NOT REPORTED]  |

**Additional dataset details**

* Documents collected from typical news areas between 2004–2005. (Section 5) 
* Dictionary size after preprocessing: 26,685 words. (Section 5.1; Table 1) 

---

# 5. Preprocessing Pipeline

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

**Reported document preprocessing**

* Stop words removed.
* Punctuation characters removed.
* TF-IDF computation performed.
* Keyword-document matrix constructed.
* PCA applied to document-index matrix. (Sections 4 and 5.1) 

---

# 6. Model Architecture

**Architecture(s)**
No CNN, machine-learning classifier, or Vision Transformer architecture is reported. The method consists of:

* TF-IDF document indexing
* Principal Component Analysis (PCA)
* Searchable encryption scheme adapted from Cao et al. (2014)
* Condensed Index Multi-keyword Search (CIMS) framework

(Section 4) 

| Item               | Value                                |
| ------------------ | ------------------------------------ |
| Architecture       | CIMS searchable-encryption framework |
| Pretraining source | [NOT REPORTED]                       |
| Transfer learning  | [NOT REPORTED]                       |
| Input resolution   | [NOT REPORTED]                       |
| Final layer        | [NOT REPORTED]                       |
| Parameter count    | [NOT REPORTED]                       |
| Loss function      | [NOT REPORTED]                       |
| Optimizer          | [NOT REPORTED]                       |
| Learning rate      | [NOT REPORTED]                       |
| Scheduler          | [NOT REPORTED]                       |
| Batch size         | [NOT REPORTED]                       |
| Epochs             | [NOT REPORTED]                       |
| Ensemble           | No                                   |

---

# 7. Validation Design

**Validation type**

Simulation-based evaluation using a single public corpus. 

**Design characteristics**

* Internal evaluation only.
* No train/validation/test protocol reported.
* No external validation.
* No cross-dataset validation.
* No prospective evaluation.
* No multi-center evaluation.

**Confidence intervals reported?**
No.

**Statistical tests reported?**
No.

**Overfitting mitigation reported?**
Not applicable / not reported.

---

# 8. Performance Metrics

## Reported Metrics

### Search Precision

Defined as:

[
\text{precision}=\frac{|F_A \cap F_R|}{|F_A|}
]

where (F_A) are documents retrieved using original indexes and (F_R) are documents retrieved using condensed indexes. (Eq. 25) 

Reported observations:

* Precision approaches nearly 100% when condensed index length (r = 1500). (Figure 2) 

### Storage Efficiency

Reported qualitatively:

* CIMS uses less than 1/10 of the storage size required by MRSE. (Section 5.2; Figure 3) 

### Search Time

Reported qualitatively:

* Search time of CIMS is less than 1/10 of MRSE when corpus size exceeds 2000 documents. (Section 5.2; Figure 4) 

### Additional Evaluations

* PCA preprocessing time (Figure 5).
* Encryption time (Figure 6).
* Trapdoor generation time (Figure 7).
* Search time versus keyword count (Figure 8). 

## Metrics Not Reported

* Accuracy
* AUC
* Confidence intervals
* Sensitivity
* Specificity
* F1-score
* Cohen's Kappa
* Quadratic Weighted Kappa
* Calibration metrics
* Confusion matrices
* Statistical significance tests

---

# 9. Authors' Claims

* Document indexes can be significantly reduced using PCA while preserving search quality. 
* The condensed index can be seamlessly integrated into secure multi-keyword searchable encryption. 
* Data security and user privacy are protected during search. 
* The proposed approach improves search efficiency in both storage and computation. 
* Search quality remains largely unaffected when appropriate condensed-index dimensions are retained. 

---

# 10. Empirical Support Assessment

| Claim                                   | Empirical Support                                                                                                  |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Index size can be reduced substantially | Supported by storage measurements and dimensionality reduction experiments.                                        |
| Search quality is preserved             | Partially supported; precision approaches 100% for large retained dimensions, but no statistical testing provided. |
| Search becomes more efficient           | Supported by reported storage and runtime comparisons versus MRSE.                                                 |
| Security/privacy preserved              | Presented through algorithmic design and mathematical formulation, not through empirical attack evaluation.        |

**External validation robust?** No.

**Confidence intervals present?** No.

**Class imbalance handled?** Not applicable.

**Statistical testing performed?** No.

**Verdict**

Generalization and robustness claims are not evaluated; efficiency claims are supported within the single simulated dataset used.

---

# 11. Internal Validity

* Mathematical derivation is explicitly presented for PCA-based dimensionality reduction and encrypted search computation. 
* Single-dataset evaluation limits assessment of variability. 
* No statistical uncertainty estimates reported.
* No sensitivity analysis beyond varying condensed-index size (r).
* Security claims rely on theoretical construction rather than empirical adversarial testing.
* No apparent data-leakage discussion.
* No overfitting discussion.

---

# 12. External Validity

* Evaluated on a single document corpus. 
* No cross-corpus validation.
* No multi-source evaluation.
* No real-world deployment study.
* Hardware used: Intel Core i7 3.40 GHz, 16 GB RAM. (Section 5) 
* Transferability to other document collections is not empirically demonstrated.

---

# 13. Strengths

* Clear mathematical formulation of PCA-based index compression. 
* Integrates dimensionality reduction with searchable encryption. 
* Uses a real-world public corpus rather than synthetic data. 
* Evaluates storage, search time, encryption time, and trapdoor-generation time. 
* Compares against an established baseline (MRSE). 

---

# 14. Limitations

### Explicit (authors state)

* PCA requires substantial computation time during preprocessing. (Section 5.3; Figure 5) 
* Search precision depends on the retained index dimension (r). 

### Implicit (observed)

* Single dataset only.
* No statistical testing.
* No confidence intervals.
* No security attack simulations.
* No external validation.
* No robustness analysis.
* No comparison with modern retrieval approaches.
* Precision curves are largely descriptive.

---

# 15. Relevance to My Dissertation

| Dissertation Axis                  | Relevance  | Notes                                                                   |
| ---------------------------------- | ---------- | ----------------------------------------------------------------------- |
| Preprocessing-dominance hypothesis | Peripheral | PCA-based index compression is unrelated to fundus-image preprocessing. |
| Cross-database generalization      | Peripheral | No cross-dataset evaluation.                                            |
| CNN vs ViT comparison              | Peripheral | Neither CNNs nor ViTs are studied.                                      |
| EyePACS benchmarking               | Peripheral | Not used.                                                               |
| Messidor benchmarking              | Peripheral | Not used.                                                               |
| IDRiD benchmarking                 | Peripheral | Not used.                                                               |
| APTOS benchmarking                 | Peripheral | Not used.                                                               |
| Explainability (Grad-CAM IoU/ALO)  | Peripheral | No explainability analysis.                                             |
| Device domain shift                | Peripheral | Not investigated.                                                       |
| Clinical degradation robustness    | Peripheral | Not investigated.                                                       |

**Risk of contradicting preprocessing-driven generalization thesis**

None. The study concerns encrypted document retrieval and does not provide evidence relevant to image preprocessing or DR classification.

---

# 16. Citation-Ready Statements

1. “This paper proposes a secure multi-keyword search scheme with condensed index for encrypted cloud documents.” (Abstract, p. 1) 

2. “The proposed scheme resolves the issue of long document index and the problem of searching documents over encrypted data, simultaneously.” (Abstract, p. 1) 

3. “The sizes of document indexes are significantly reduced, with only a commensurate loss on search precision.” (Contributions, p. 2) 

4. “The results show that the proposed scheme significantly improves the search efficiency in terms of time and space.” (Contributions, p. 2) 

5. “The precision can reach near 100% when the length of the condensed document index is 1500.” (Section 5.1; Figure 2 discussion, p. 9) 

---

# 17. Epistemic Classification

**Peripheral**

**Justification:**
The study belongs to searchable encryption and cloud-document retrieval rather than medical imaging, diabetic retinopathy, computer vision classification, explainable AI, or clinical validation. It provides no direct evidence concerning preprocessing effects on CNN-based retinal image diagnosis. 

---

# 18. Analytical Synthesis

This article addresses a fundamentally different research domain from automated diabetic retinopathy diagnosis. Its contribution lies in combining PCA-based dimensionality reduction with searchable encryption for cloud document retrieval, demonstrating storage and runtime improvements within a single text corpus. The work contains no CNNs, no retinal images, no medical datasets, and no clinical evaluation. Consequently, it neither supports nor challenges the dissertation's central hypothesis that carefully designed preprocessing substantially influences CNN generalization performance in fundus-image analysis. The article also provides no evidence regarding cross-database transfer, explainability, domain shift, or CNN-versus-ViT comparisons. From the perspective of DR benchmarking literature, its epistemic relevance is minimal. It may only serve as a distant methodological example of dimensionality reduction for efficiency optimization, not as evidence for retinal-image preprocessing or diagnostic AI.

End of Literature Card.
