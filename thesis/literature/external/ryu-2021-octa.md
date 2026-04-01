# 1. Bibliographic Metadata

* **Full citation (APA 7)**
  Ryu, G., Lee, K., Park, D., Park, S. H., & Sagong, M. (2021). *A deep learning model for identifying diabetic retinopathy using optical coherence tomography angiography*. Scientific Reports, 11, 23024. [https://doi.org/10.1038/s41598-021-02479-6](https://doi.org/10.1038/s41598-021-02479-6) 

* **DOI:** 10.1038/s41598-021-02479-6

* **Journal:** Scientific Reports

* **Year:** 2021 (corrected publication 2022)

* **Publication type:** Empirical study with external validation

* **Research domain classification:** Medical AI; OCTA-based diabetic retinopathy classification; CNN clinical validation

---

# 2. Study Type Classification

* CNN-based classification study
* External validation study

**Justification:**
The study develops a ResNet101-based CNN for DR detection using OCTA and evaluates performance on a separate external dataset collected in a different time period (Feb 2019–Jan 2020) .

---

# 3. Research Problem

**Specific problem addressed:**
Develop an end-to-end deep CNN classifier for:

1. Detecting onset of DR
2. Identifying referable DR (severe NPDR or worse)

Using **OCTA images only**, with ground truth defined by ultra-widefield fluorescein angiography (UWF FA).

**Related to:**

* Clinical deployment
* Imaging modality comparison (OCTA vs fundus)
* Generalization (internal + external validation)
* Feature representation (CNN vs handcrafted features)

---

# 4. Datasets Used

## Primary Dataset

* **Name:** [NOT NAMED – institutional dataset]

* **Public/Private:** Private

* **Initial recruitment:** 301 eyes

  * 51 healthy
  * 51 DM without DR
  * 53 mild NPDR
  * 49 moderate NPDR
  * 48 severe NPDR
  * 49 PDR

* After quality exclusion:

  * 240 datasets
  * 40 datasets per DR stage
  * For each: 3×3 mm² and 6×6 mm² OCTA scans

* **Class taxonomy:**

  * Multiclass (6 severity grades: DR 0–5)
  * Binary tasks:

    * DR detection (mild NPDR or worse)
    * Referable DR detection (severe NPDR or worse)

* **Split design:** 4-fold cross-validation

* **External dataset used:** Yes

* **Cross-dataset testing:** No (same institution, later time period)

## External Dataset

* **Sample size:** 195 eyes recruited
* After exclusion:

  * 120 datasets
  * 20 per DR stage
  * 3×3 and 6×6 scans

---

# 5. Preprocessing Pipeline

* Resizing: [NOT REPORTED]
* Cropping: Centered macular OCTA scans
* Normalization: [NOT REPORTED]
* CLAHE: [NOT REPORTED]
* Color normalization: Not applicable (OCTA grayscale)
* Augmentation: [NOT REPORTED]
* Image quality filtering:

  * Signal strength ≤6 excluded
  * Motion artifacts excluded
  * Projection artifacts excluded
* Lesion enhancement: None

---

# 6. Model Architecture

## CNN-Based Model

* **Architecture:** ResNet101
* **Type:** CNN, end-to-end
* **Input:** Concatenated SCP, DCP, full-thickness OCTA images
* **Pretraining:** ImageNet (excluding first and last layers)
* **Transfer learning:** All parameters retrained on OCTA dataset
* **Loss function:** Cross-entropy
* **Optimizer:** Adam
* **Learning rate:** 0.0001
* **Epochs:** [NOT REPORTED]
* **Hyperparameters:** Not fully reported

## Machine Learning Baseline

* U-Net segmentation
* Extracted features:

  * Vessel density
  * Skeletal vessel density
  * Fractal dimension
  * FAZ area
* Neural network classifier

---

# 7. Validation Design

* 4-fold cross-validation (internal)
* External validation on separate dataset
* Not prospective
* Not multi-center

---

# 8. Performance Metrics

## DR Detection (Internal)

CNN (3×3 mm², combined):

* AUC: 0.960
* Sensitivity: 96%
* Specificity: 89%

CNN (6×6 mm², combined):

* AUC: 0.967
* Sensitivity: 97%
* Specificity: 93%

Machine learning:

* AUC: 0.713 (3×3)
* AUC: 0.742 (6×6)

## Referable DR (Internal)

CNN (6×6 mm², combined):

* AUC: 0.976
* Sensitivity: 96%
* Specificity: 98%

Machine learning:

* AUC: 0.837 (6×6)

## External Validation

DR detection (6×6 mm², combined):

* AUC: 0.962

Referable DR (6×6 mm², combined):

* AUC: 0.938

No confidence intervals reported.

No F1, no Kappa reported.

Confusion matrices: Provided in supplementary material.

---

# 9. Authors’ Claims

* CNN achieved high diagnostic performance (AUC 0.93–0.98).
* Comparable performance across OCTA slab types and scan sizes.
* Outperforms machine learning with handcrafted features.
* OCTA may provide sufficient information for DR classification.
* Potential to create a novel diagnostic workflow.
* Could reduce need for invasive FA.

---

# 10. Empirical Support Assessment

* External validation present but from same institution.
* No confidence intervals → uncertainty unquantified.
* Dataset relatively small (240 + 120).
* Class balance artificially equalized.
* No cross-institutional validation.
* Statistical tests not reported.

Generalization claims moderately supported but limited.

---

# 11. Internal Validity

* Overfitting risk: Moderate (small dataset, deep model).
* Transfer learning reduces but does not eliminate risk.
* No augmentation details → unknown inflation risk.
* Dataset leakage risk: Not indicated.
* Metrics: Standard and correctly computed.

---

# 12. External Validity

* Single-center dataset.
* External validation temporal, not geographic.
* OCTA device: Optovue RTVue XR AVANTI.
* Generalizability to other OCTA devices unproven.
* Clinical feasibility plausible but not tested prospectively.

---

# 13. Strengths

* UWF FA-based ground truth.
* External validation.
* Direct comparison with handcrafted ML baseline.
* Slab-level and scan-size analysis.
* CAM interpretability provided.

---

# 14. Limitations

## Explicit (stated)

* Small sample size.
* No FA for normal subjects.
* Not tested on fully independent multi-center dataset.
* Excluded macular edema cases.

## Implicit

* No confidence intervals.
* No augmentation description.
* No statistical hypothesis testing.
* No cross-device validation.

---

# 15. Relevance to My Dissertation

* Strong relevance to OCTA-based DR classification.
* Supports modality-shift argument (beyond fundus).
* Limited relevance to EyePACS/Messidor benchmarking.
* Not a Vision Transformer study.
* Does not address preprocessing dominance directly.
* Demonstrates external validation but not cross-database robustness.

Risk of contradiction: Low.

---

# 16. Citation-Ready Statements

1. “The proposed CNN classifier achieved an AUC of 0.960–0.967 for detecting DR and 0.940–0.976 for detecting referable DR using OCTA images.”
2. “Ground truths were determined using ultra-widefield fluorescein angiography to improve labeling accuracy.”
3. “External validation demonstrated similar performance, with AUC differences of −0.02 to +0.02.”
4. “The CNN outperformed the machine learning classifier using handcrafted OCTA features (AUC 0.713–0.742).”
5. “DR could be satisfactorily classified even with 3×3 mm² macular OCTA scans.”

---

# 17. Epistemic Classification

**Clinical validation precedent**
+
**Methodological precedent**

Justification:
Introduces OCTA-only CNN classification with UWF FA ground truth and includes external validation.

---

# 18. Analytical Synthesis

This study provides moderate epistemic weight as one of the early OCTA-only CNN DR classification works with external validation. Its methodological rigor is strengthened by UWF FA-based ground truth and balanced class design. However, absence of multi-center validation and confidence intervals limits generalization strength. It does not address cross-dataset benchmarking or preprocessing dominance explicitly. The study strengthens the argument that end-to-end CNNs outperform handcrafted OCTA feature pipelines. It does not demonstrate cross-database robustness beyond temporal validation. For a dissertation focused on cross-dataset generalization and preprocessing dominance, this paper serves as supportive but limited-scope empirical evidence.

---

End of Literature Card.
