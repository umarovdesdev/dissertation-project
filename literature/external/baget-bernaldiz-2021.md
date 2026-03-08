# Literature Card: Baget-Bernaldiz et al. (2021)

---

## 1. Bibliographic Metadata

- **Full citation (APA 7):** Baget-Bernaldiz, M., Romero-Aroca, P., Santos-Blanco, E., Navarro-Gil, R., Valls, A., Moreno, A., Rashwan, H. A., & Puig, D. (2021). Testing a deep learning algorithm for detection of diabetic retinopathy in a Spanish diabetic population and with MESSIDOR database. *Diagnostics*, *11*(8), 1385.
- **DOI:** https://doi.org/10.3390/diagnostics11081385
- **Journal:** *Diagnostics* (MDPI)
- **Year:** 2021
- **Publication type:** Empirical — external validation / clinical testing study
- **Research domain classification:** Medical AI; diabetic retinopathy screening; CNN-based fundus image classification; clinical deployment

---

## 2. Study Type Classification

**Classifications applicable:**
- External validation study ✓
- Cross-dataset validation ✓
- Messidor benchmarking ✓
- CNN-based classification study ✓
- Clinical prospective validation (partial) ✓

**Justification:** The study tests a previously constructed CNN-based DLA on two distinct datasets: a real-world clinical population (internal cohort, different patients from training/validation) and the public MESSIDOR database. This constitutes both clinical testing on a prospective-style population sample and cross-dataset external validation. It is not a systematic review, meta-analysis, or Vision Transformer study.

---

## 3. Research Problem

**Specific problem addressed:** Testing the diagnostic performance of a previously developed CNN-based DLA for DR detection and classification on an unseen clinical population and an independent public database (MESSIDOR), comparing DLA output against consensus grading by four masked retinal specialists.

**Related to:**
- **Clinical deployment:** Primary concern — evaluating DLA fitness for real-world screening
- **Generalization:** Tested across two populations with different demographics, imaging equipment, and class distributions
- **Preprocessing:** Partially — a gradeability filter is incorporated to exclude low-quality images prior to classification

---

## 4. Datasets Used

**Dataset 1 — Internal Spanish Population Cohort**
- **Name:** Hospital Universitat Sant Joan screening programme (Reus/Tarragona, Spain)
- **Public/Private:** Private
- **Sample size (testing):** 14,186 retinographies from 7,164 patients (testing phase); 5,000 retinographies (validation phase); 15,123 images (training phase, different patients)
- **Class taxonomy:** 4-class ICDR scale (Level 0: no DR; Level 1: mild; Level 2: moderate; Level 3: severe/proliferative) + binary referable DR (RDR) classification
- **Train/validation/test split:** Training: 15,123 (own population) + 88,692 (EyePACS) = 103,815 total; Validation: 5,000; Testing: 14,186 (all different patients)
- **External dataset used:** Yes (EyePACS used in training)
- **Cross-dataset testing performed:** Yes (MESSIDOR)

**Dataset 2 — MESSIDOR**
- **Name:** MESSIDOR (Méthodes d'Evaluation de Systèmes de Segmentation et d'Indexation Dédiées à l'Ophtalmologie)
- **Public/Private:** Public
- **Sample size:** 1,200 retinal images from 874 unique individuals
- **Class taxonomy:** 4-class (same ICDR scale applied) + binary RDR
- **Train/validation/test split:** Used exclusively as independent test set; not used in training or validation
- **External dataset used:** N/A (this is itself the external dataset)
- **Cross-dataset testing performed:** Yes

**Dataset 3 — EyePACS (training only)**
- **Name:** EyePACS
- **Public/Private:** Public (Kaggle competition dataset)
- **Sample size (used):** 88,692 retinal images
- **Role:** Training only; not used for validation or testing
- **Class taxonomy:** [NOT REPORTED in detail within this article; referenced via citation 18]

**Class distribution (test sets):**

| Level | Own Population | MESSIDOR |
|---|---|---|
| No DR (0) | 11,827 (83.4%) | 625 (52.0%) |
| Mild DR (1) | 778 (5.5%) | 197 (16.4%) |
| Moderate DR (2) | 984 (6.9%) | 130 (10.8%) |
| Severe/Proliferative DR (3) | 597 (4.2%) | 248 (20.6%) |
| Referable DR | 1,503 (10.6%) | 378 (31.5%) |

---

## 5. Preprocessing Pipeline

- **Resizing:** Input image size: 3 × 640 × 640 pixels
- **Cropping:** [NOT REPORTED]
- **Normalization:** [NOT REPORTED]
- **CLAHE:** [NOT REPORTED]
- **Color normalization:** [NOT REPORTED]
- **Augmentation:** [NOT REPORTED]
- **Image quality filtering:** Yes — a "gradeability" function built into the DLA screens for image quality and macula centration prior to classification. Images failing gradeability are discarded and excluded from analysis. Gradeability rate: 99.0% (own population), 100% (MESSIDOR).
- **Lesion enhancement methods:** [NOT REPORTED]

---

## 6. Model Architecture

- **Architecture type:** CNN — custom convolutional neural network
- **Architecture details:** 7 blocks of 2 layers each; each layer = 3×3 convolution (stride 1×1, padding 1×1) + batch normalization + ReLU activation; receptive field reduced progressively to 64×5×5; 4×4 average pooling yields 64-feature final vector; linear classifier + softmax output layer
- **Pretraining source:** [NOT REPORTED — no mention of ImageNet or other pretraining]
- **Transfer learning protocol:** [NOT REPORTED]
- **Input resolution:** 640 × 640 pixels (3-channel)
- **Loss function:** Quadratic weighted kappa (described as appropriate for ordinal classification)
- **Optimizer:** [NOT REPORTED]
- **Epochs:** [NOT REPORTED]
- **Hyperparameters:** [NOT REPORTED beyond architecture details above]

*Note: Full architecture details are cited as reported in a prior publication (reference 14 in article; De la Torre et al. 2018/2020).*

---

## 7. Validation Design

- **Internal validation only:** No
- **Cross-validation:** No
- **External validation:** Yes — MESSIDOR used as independent external test set; the internal population test cohort uses entirely different patients from training/validation phases
- **Prospective validation:** Partial — the clinical cohort was drawn from routine screening records (2019), constituting a real-world population sample, but the design is retrospective testing rather than a prospective clinical trial
- **Multi-center validation:** Partial — MESSIDOR originated from three French hospitals with different cameras; the authors' own population is single-center (Hospital Universitat Sant Joan)

---

## 8. Performance Metrics

**Own Population — Any DR detection:**
- ACC = 99.75 (95% CI: 99.65–99.82)
- S = 97.92 (95% CI: 97.26–98.46)
- SP = 99.91 (95% CI: 99.83–99.95)
- PPV = 98.92 (95% CI: 98.07–99.40)
- NPV = 99.82 (95% CI: 99.76–99.86)
- AUC = 0.983
- Error type I = 0.0009; Error type II = 0.004

**Own Population — Referable DR detection:**
- ACC = 99.66 (95% CI: 99.55–99.75)
- S = 96.7 (95% CI: 95.69–99.49)
- SP = 99.92 (95% CI: 99.85–99.96)
- PPV = 99.07 (95% CI: 98.28–97.46) *[note: CI lower bound as reported in article]*
- NPV = 99.71 (95% CI: 99.63–99.78)
- AUC = 0.988
- Error type I = 0.0041; Error type II = 0.033

**MESSIDOR — Any DR detection:**
- ACC = 94.79 (95% CI: 93.38–95.98)
- S = 97.32 (95% CI: 95.62–98.49)
- SP = 94.57 (95% CI: 92.53–96.19)
- PPV = 60.93 (95% CI: 53.04–68.28)
- NPV = 99.75 (95% CI: 99.60–99.85) *[note: NPV reported as 99.75 in abstract but text table reports same]*
- AUC = 0.959
- Error type I = 0.054; Error type II = 0.026

**MESSIDOR — Referable DR detection:**
- ACC = 98.78 (95% CI: 97.99–99.32)
- S = 94.64 (95% CI: 91.93–96.65)
- SP = 99.14 (95% CI: 98.24–99.65)
- PPV = 90.54 (95% CI: 82.06–95.24)
- NPV = 99.53 (95% CI: 99.29–99.69)
- AUC = 0.968
- Error type I = 0.009; Error type II = 0.053

**Confusion matrices:** Provided in Tables 2 and 4 (4-class level) and Tables 3 and 5 (binary any-DR and RDR)

**Statistical tests used:** Cohen's Weighted Kappa (CWK) with 95% CI (inter-rater and DLA-vs-specialist agreement); SPSS 22.0; significance threshold p < 0.05. CWK values for testing phase are referenced to a prior publication (Romero-Aroca et al. 2020, ref. 19) rather than reported directly in this paper.

**F1 / Cohen's Kappa (direct values):** [NOT REPORTED in this paper — referenced to prior publication]

---

## 9. Authors' Claims

**Performance claims:**
- The DLA "performed well" in detecting any DR and classifying RDR in both the own population and MESSIDOR
- AUC of 0.983 (any DR) and 0.988 (RDR) in own population; 0.959 and 0.968 in MESSIDOR
- Gradeability rate of 99–100% demonstrates reliable image quality filtering

**Generalization claims:**
- The DLA generalizes across populations (Spanish clinical cohort and French MESSIDOR images from 3 hospitals with different cameras)
- Higher false positive and false negative rates on MESSIDOR are attributed to inter-camera pixel-definition differences rather than model failure

**Clinical applicability claims:**
- The DLA "can be used as a reliable diagnostic tool to ease the screening for DR"
- It is cost-effective and could increase annual screening capacity
- False negatives are predominantly mild DR cases where visual acuity is not typically compromised and patients would be caught at later check-ups

**Superiority claims:**
- DLA performance compares favorably to FDA-approved systems: IDx-DR (S=91%, SP=84%), EyeArt (S=91.3%, SP=91.1%, AUC=0.965), Retmarker (S=73%, SP=85% for RDR), and RetCAD (S=90.1%, SP=90.6%)
- Authors state their DLA "performed very well in both samples in detecting RDR, compared to those that have already been approved by the FDA or that have obtained the CE Class IIa mark"

---

## 10. Empirical Support Assessment

**Does data support generalization claims?**
Partially. The DLA was tested on two datasets from different countries, camera types, and ethnic compositions, showing reasonable cross-dataset portability. However, performance degraded meaningfully on MESSIDOR — PPV dropped from 98.92% to 60.93% for any-DR detection, reflecting the severe class imbalance difference between the two cohorts (83.4% no-DR in own population vs. 52.0% in MESSIDOR). The authors' attribution of performance differences to camera pixel definition is plausible but unverified empirically.

**Is external validation robust?**
Moderately. MESSIDOR (n=1,200) is a well-established benchmark but relatively small for robust external validation. The internal test cohort (n=14,186) is large and drawn from real-world screening, strengthening clinical applicability claims.

**Are confidence intervals reported?**
Yes — 95% CIs are provided for ACC, S, SP, PPV, NPV, and AUC across all four performance tables.

**Is dataset size adequate?**
For the internal cohort: yes (14,186 images, 7,164 patients). For MESSIDOR: adequate for benchmarking but limited for robust generalization inference.

**Is class imbalance addressed?**
Not explicitly addressed in preprocessing or loss function design for the test phase. The training set composition is reported (81,266 no-DR; 8,771 mild; 14,097 moderate; 4,588 severe) but no oversampling, undersampling, or class-weighting strategy is described. The dramatic PPV drop on MESSIDOR (60.93%) for any-DR detection directly reflects the lower prevalence gap between classes compared to own population.

**Is statistical testing adequate?**
Partial. 95% CIs are provided. Cohen's Weighted Kappa is used for agreement assessment. No formal hypothesis testing comparing DLA performance between datasets or against comparator systems is performed. Comparisons to FDA-approved systems are descriptive, not statistical.

---

## 11. Internal Validity

**Overfitting risk:** Low-to-moderate. Training used 103,815 images across two datasets (own population + EyePACS), with patient-level separation between training, validation, and test sets explicitly stated. The large training corpus reduces overfitting risk. However, the internal test cohort comes from the same hospital and camera as part of the training data, which introduces domain-homogeneity bias.

**Dataset leakage risk:** Low. Authors explicitly state test patients are "different from those used to train and validate the DLA."

**Confounders:** Single camera type (TOPCON TRC-NW6S) for own population — acknowledged as a limitation. Patient demographics differ substantially between cohorts (mean age 67.3 vs. 57.6; DR distribution heavily skewed in own population).

**Augmentation inflation risk:** [NOT REPORTED] — no augmentation strategy described; cannot assess.

**Metric reliability:** ACC is inflated by the highly skewed class distribution in own population (83.4% no-DR). Authors acknowledge this explicitly: "accuracy is affected by prevalence." AUC and NPV are more reliable metrics in this context.

**Formula correctness:** The PPV CI for RDR in own population (95% CI: 98.28–97.46) has an inverted lower/upper bound as reported in the article — likely a typographical error.

---

## 12. External Validity

**Cross-population transferability:** Demonstrated at a basic level — the model transfers from a Spanish Type 2 DM population to a French multi-center dataset. Performance remains clinically acceptable for RDR detection (AUC 0.968 on MESSIDOR). However, the model has not been tested on non-European populations or with diverse ethnic compositions; authors acknowledge absence of ethnic variety as a limitation.

**Dataset portability:** MESSIDOR testing demonstrates portability across camera types and acquisition settings, but PPV degradation for any-DR detection is notable.

**Clinical feasibility:** Supported by the real-world population design (consecutive screening patients, 2019), single-camera deployment, and integrated gradeability filter. Authors frame the system as a triage tool rather than a replacement for ophthalmologist review.

**Hardware constraints:** [NOT REPORTED] — no inference time, GPU requirements, or deployment infrastructure described.

---

## 13. Strengths

- Large real-world clinical test cohort (14,186 images, 7,164 patients) drawn from unselected screening population, enhancing ecological validity
- Strict patient-level separation between training, validation, and test phases
- Cross-dataset testing with MESSIDOR provides independent external benchmarking
- 95% CIs reported for all primary performance metrics
- Four masked retinal specialists used as consensus reference standard, reducing reference standard bias
- Integrated gradeability filter addresses image quality confounding prior to classification
- 4-class ordinal classification using ICDR scale rather than binary-only output, enabling clinical staging beyond referable/non-referable dichotomy

---

## 14. Limitations

**Explicit (stated by authors):**
- Testing limited to retinographies from a single camera type (TOPCON TRC-NW6S); generalizability to other fundus cameras unknown
- Limited ethnic diversity in test population; model should be tested on larger samples with greater ethnic variety
- No independent validation of the screening algorithm by external parties prior to clinical use recommended

**Implicit (methodological):**
- Full architecture details, optimizer, training hyperparameters, and augmentation strategy are offloaded to a prior publication rather than reported in this article, hampering reproducibility assessment
- No preprocessing pipeline details (normalization, CLAHE, color correction) reported; preprocessing role in performance cannot be assessed
- Comparison to FDA-approved systems is descriptive and draws on different study populations — no head-to-head validation performed
- MESSIDOR class distribution (48% DR prevalence) vs. own population (16.6% DR prevalence) makes direct metric comparison misleading, particularly PPV; this is not fully disentangled analytically
- Cohen's Weighted Kappa values for the test phase are not reported in this paper but referenced to a prior publication
- The gradeability filter exclusion of 141 images (0.98% of own population) may introduce selection bias if systematically poorer images correlate with more severe or less severe DR
- No subgroup analyses by DR severity grade, age, or sex

---

## 15. Relevance to Dissertation

**Relevance to preprocessing dominance hypothesis:** Low-to-indirect. Preprocessing details are not reported in this paper. The gradeability filter represents a form of quality-based image selection, but its specific preprocessing steps are not described. This article cannot be used to support or refute preprocessing-dominance claims.

**Relevance to cross-database validation:** High. The article directly demonstrates cross-database validation between an internal Spanish clinical cohort and MESSIDOR, with quantified performance differences. The PPV drop (98.92% → 60.93% for any-DR) illustrates how domain shift affects specific metrics while AUC remains relatively robust (0.983 → 0.959), a distinction highly relevant to cross-database validation methodology.

**Relevance to EyePACS/Messidor benchmarking:** High for MESSIDOR benchmarking. EyePACS is used only in training, not for testing benchmarking; thus EyePACS benchmark comparisons are not possible from this article alone.

**Relevance to Vision Transformer comparison:** None. The study uses a custom CNN; no transformer architectures are employed or discussed.

**Risk of contradiction:** Moderate. If your dissertation argues for preprocessing dominance as a key determinant of cross-dataset performance, this article does not provide evidence for or against that position — but the authors attribute cross-dataset performance differences to camera/pixel differences rather than to preprocessing choices, which implicitly places emphasis on input domain factors rather than algorithmic preprocessing. This is compatible with but does not directly support a preprocessing-dominance argument.

---

## 16. Citation-Ready Statements

1. "The results of testing the DLA for identifying any DR in our population were: ACC = 99.75, S = 97.92, SP = 99.91, PPV = 98.92, NPV = 99.82, and AUC = 0.983" (Baget-Bernaldiz et al., 2021, p. 1 [abstract]).

2. "When detecting RDR [on MESSIDOR], the results were: ACC = 98.78, S = 94.64, SP = 99.14, PPV = 90.54, NPV = 99.53, and AUC = 0.968" (Baget-Bernaldiz et al., 2021, p. 1 [abstract]).

3. "A higher proportion of false positives and false negatives [was found] when testing the retinographies from MESSIDOR compared to our own population. This might be due to differences in pixel definition of the pictures, as the dataset was compiled using different cameras, rather than our own images that were taken with the same model of non-mydriatic fundus camera" (Baget-Bernaldiz et al., 2021, p. 8).

4. "The gradeability test allowed the algorithm to read 99% and 100% retinographies from the two sample origins, respectively" (Baget-Bernaldiz et al., 2021, p. 8).

5. "A limitation of our study is that we tested our DLA using retinographies taken by only one type of non-mydriatic fundus camera, so further study is essential into whether other models might change the results. In addition, our algorithm should be tested on larger samples of patients and with greater ethnic variety" (Baget-Bernaldiz et al., 2021, p. 9).

6. The DLA was trained on 103,815 images combining the authors' own population (15,123 images) and the EyePACS database (88,692 images), and tested on entirely separate patients, with the authors stating this large training corpus was used "to better adjust the algorithm and minimise the overfitting" (Baget-Bernaldiz et al., 2021, p. 7).

7. "The DLA correctly identified 99.9% (our population) and 94.6% (MESSIDOR) of the retinographies without DR. False positives yielded from the two samples were 0.09% and 5.4%, respectively" (Baget-Bernaldiz et al., 2021, p. 8).

---

## 17. Epistemic Classification

**Classification: Benchmark study / Clinical validation precedent**

**Justification:** The article provides a quantified, real-world clinical validation of a CNN-based DLA against a large unselected population and the established MESSIDOR benchmark, with full performance metrics and 95% CIs. It does not introduce a novel architecture, preprocessing technique, or theoretical framework. Its epistemic value lies in demonstrating cross-dataset portability of a CNN-based system under realistic conditions, with direct comparisons to FDA-approved DLAs. It constitutes a clinical validation precedent for the MESSIDOR cross-dataset paradigm, rather than a foundational or high-impact theoretical contribution.

---

## 18. Analytical Synthesis

This article occupies a mid-tier epistemic position: it is a competent clinical validation study with a large real-world test cohort, but its methodological transparency is constrained by its reliance on prior publications for architecture and preprocessing details, making independent reproducibility difficult. Its primary dissertation value is as empirical evidence for cross-dataset generalization behavior: the AUC remains robust (0.983 → 0.959) across two populations with markedly different class distributions, while PPV collapses (98.92% → 60.93%), demonstrating that prevalence-sensitive metrics are unreliable indicators of cross-dataset portability — a point directly relevant to dissertation methodology on benchmark comparability. The article does not contribute to the preprocessing-dominance argument because preprocessing choices are not disclosed; it implicitly attributes cross-dataset performance differences to acquisition hardware (camera type, pixel definition) rather than algorithmic factors. The comparison to FDA-approved systems is descriptive rather than experimental, limiting its value as a superiority claim but providing useful contextual positioning for CNN-era clinical benchmarks. For a dissertation examining cross-database validation and the role of preprocessing in DR detection, this paper is most useful as a case study in how domain shift manifests in specific metrics and as a MESSIDOR benchmarking data point, but should not be cited as evidence regarding preprocessing effects.

---