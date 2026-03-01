# Literature Card: Sánchez-Gutiérrez et al. (2022)

---

## 1. Bibliographic Metadata

- **Full citation (APA 7):** Sánchez-Gutiérrez, V., Hernández-Martínez, P., Muñoz-Negrete, F. J., Engelberts, J., Luger, A. M., & van Grinsven, M. J. J. P. (2022). Performance of a deep learning system for detection of referable diabetic retinopathy in real clinical settings. *[Journal name NOT REPORTED in preprint]*.
- **DOI:** arXiv:2205.05554v1
- **Journal / Conference:** [NOT REPORTED — arXiv preprint]
- **Year:** 2022
- **Publication type:** Clinical validation (retrospective, real-world)
- **Research domain classification:** Medical AI; Diabetic retinopathy screening; Clinical deployment of deep learning

---

## 2. Study Type Classification

**Primary classifications:**
- Clinical prospective validation (retrospective real-world equivalent)
- CNN-based classification study
- External validation study (the RetCAD system was trained on independent data; this dataset was not used for training)

**Justification:** The study evaluates a commercially deployed, CE-marked AI system (RetCAD v.1.3.1) on a fully independent, real-world clinical dataset from a tertiary hospital screening program. The model was not trained on this data. The study is not a benchmark against EyePACS/Messidor, not an IDRiD lesion-level study, and not a Vision Transformer application.

---

## 3. Research Problem

**Specific problem addressed:** Evaluation of a commercially available deep learning system (RetCAD v.1.3.1) for automated detection of referable DR in a real-world, routine clinical setting, with quantification of achievable workload reduction.

**Problem dimensions:**
- **Clinical deployment:** Primary focus — assessing whether a CE-marked AI tool performs adequately in operational screening conditions.
- **Generalization:** Secondary — authors assess whether the system trained on external data transfers to a Spanish tertiary care population.
- **Preprocessing:** Not addressed as a research variable.
- **Architecture scaling:** Not addressed.
- **Lesion detection:** Not the primary focus; system outputs a severity score, not lesion-level annotations.

---

## 4. Datasets Used

**Dataset: Ramon y Cajal Hospital Screening Dataset**

| Attribute | Detail |
|---|---|
| Name | Ramon y Cajal University Hospital DR Screening Dataset |
| Public / Private | Private |
| Sample size | 7,195 images from 6,325 eyes of 3,189 patients (after quality filtering from initial 7,454 images of 3,270 patients) |
| Class taxonomy | Binary: referable DR (ICDR stages 3–5) vs. non-referable DR (ICDR stages 1–2); 5-class ICDR grading used as intermediate reference |
| Train/validation/test split | No split — entire dataset used for evaluation only (no training performed on this data) |
| External dataset used? | No — evaluation only dataset |
| Cross-dataset testing performed? | Yes — RetCAD was trained on independent data (not specified in this article); this constitutes cross-dataset inference |

**Class distribution (eye-level, Grader 1):**
- Stage 1 (no DR): 6,055
- Stage 2 (mild): 175
- Stage 3 (moderate): 76
- Stage 4 (severe): 18
- Stage 5 (proliferative): 1
- **Referable DR prevalence: 1.5%** (95 of 6,325 eyes)

---

## 5. Preprocessing Pipeline

| Step | Detail |
|---|---|
| Resizing | [NOT REPORTED] |
| Cropping | [NOT REPORTED] |
| Normalization | [NOT REPORTED] |
| CLAHE | [NOT REPORTED — Fig.1 shows a contrast-enhanced output image produced by RetCAD internally, but parameters are not disclosed] |
| Color normalization | [NOT REPORTED] |
| Augmentation | [NOT REPORTED — evaluation study; no training augmentation described] |
| Image quality filtering | Yes — all images scored for gradeability (contrast, clarity, focus) during routine clinical practice; only gradable images included. 259 images excluded (7,454 → 7,195) |
| Lesion enhancement | [NOT REPORTED — RetCAD produces internal heatmaps; methodology not disclosed] |

**Note:** RetCAD is a black-box commercial system; its internal preprocessing is proprietary and not described in this paper.

---

## 6. Model Architecture

| Attribute | Detail |
|---|---|
| Architecture type | CNN-based (convolutional neural networks — stated explicitly) |
| Pretraining source | [NOT REPORTED] |
| Transfer learning protocol | [NOT REPORTED] |
| Input resolution | [NOT REPORTED] |
| Loss function | [NOT REPORTED] |
| Optimizer | [NOT REPORTED] |
| Epochs | [NOT REPORTED] |
| Hyperparameters | [NOT REPORTED] |
| Output | DR severity score 0–100; threshold ≥50 = referable; heatmaps of detected abnormalities |
| Regulatory status | CE-marked Class IIa medical device software (RetCAD v.1.3.1, Thirona, Nijmegen, The Netherlands) |

All architectural details are proprietary. The paper describes the system only functionally.

---

## 7. Validation Design

- **Internal validation only:** No
- **Cross-validation:** No
- **External validation:** Yes — the evaluation dataset is fully independent from the training data
- **Prospective validation:** No — retrospective collection (February–December 2019); authors explicitly note prospective evaluation remains future work
- **Multi-center validation:** No — single tertiary hospital (Ramon y Cajal, Madrid, Spain)

**Reference standard construction:** Primary grading by Grader 1 (ophthalmologist, >5 years experience) using ICDR scale. Adjudication by Grader 2 (3 years experience) performed only for cases where RetCAD scored ≥50 OR where RetCAD and Grader 1 disagreed. The 6,042 cases where both RetCAD and Grader 1 agreed as non-referable were **not** reviewed by Grader 2.

---

## 8. Performance Metrics

| Metric | Value |
|---|---|
| AUC | 0.988 [95% CI: 0.981–0.993] |
| Sensitivity (at threshold 50) | 90.53% (86/95 eyes) |
| Specificity (at threshold 50) | 97.13% (6,051/6,230 eyes) |
| Accuracy | [NOT REPORTED as standalone metric] |
| F1 (macro/weighted) | [NOT REPORTED] |
| Cohen's Kappa | [NOT REPORTED] |
| Confusion matrix | Derivable from text: TP=86, FN=9 (6 confirmed by Grader 2), TN=6,051, FP=188 (38 confirmed non-referable by Grader 2, 150 reclassified referable) |
| Statistical tests | Bootstrap analysis for 95% CI on ROC/AUC; ROC curve analysis |
| Workload reduction | 96% (only 274 of 6,325 cases require human review) |
| False negatives (confirmed) | 6 (confirmed referable by both Grader 1 and Grader 2) |

---

## 9. Authors' Claims

**Performance claims:**
- RetCAD achieved AUC of 0.988 [0.981–0.993] for referable DR detection.
- Sensitivity 90.53% and specificity 97.13% exceed screening guideline recommendations.
- Both sensitivity and specificity surpass guideline thresholds cited in references [18, 19].

**Workload reduction claims:**
- 96% workload reduction achievable with only 6 false negatives.
- This reduction exceeds previously reported proportions of 26.4%–60%.
- Authors attribute the high workload reduction partly to the very low prevalence of referable DR (1.5%) in this well-controlled population.

**Generalization claims:**
- Authors assert the system "may be reasonably applied in other real clinical cohorts" based on large, consecutively recruited real-world sample.
- Authors note the system has been evaluated on several datasets (reference [16]).

**Clinical applicability claims:**
- RetCAD can function as a triage instrument, flagging cases for human review.
- AI may increase additional referral detection when used as first-stage operator.
- Operating threshold can be adjusted for different clinical settings.

**Superiority claims:**
- Authors note both human graders had "a comparable or more number of missed cases" compared to RetCAD's 6 false negatives.

---

## 10. Empirical Support Assessment

**Does data support generalization claims?** Partially. The dataset is large (6,325 eyes) and consecutively recruited, which supports real-world representativeness within this specific Spanish tertiary care population. However, single-center, single-country, single-camera design limits generalizability claims. The 1.5% referable DR prevalence is atypical and explicitly acknowledged by the authors as potentially inflating workload reduction figures.

**Is external validation robust?** Moderate. The system is evaluated on fully independent data, which is a genuine external validation. However, single-site, single-country, and lack of multi-reader adjudication for the non-flagged majority substantially limit robustness.

**Are confidence intervals reported?** Yes — for AUC only: [0.981–0.993]. No CIs for sensitivity or specificity.

**Is dataset size adequate?** The overall sample is large, but the referable DR class is very small (95 eyes), which reduces the statistical power for sensitivity estimation. The 86 true positives represent a small absolute number for robust performance characterization.

**Is class imbalance addressed?** Not methodologically. The extreme imbalance (95 referable vs. 6,230 non-referable; ratio ~1:66) is noted descriptively but no resampling, weighting, or adjusted threshold analysis is reported.

**Is statistical testing adequate?** Minimal — bootstrap CI for AUC is appropriate. No formal statistical comparison with human graders, no Delong test, no McNemar test for sensitivity/specificity comparison.

---

## 11. Internal Validity

**Overfitting risk:** Not applicable — this is an evaluation-only study; the model was not trained on this data.

**Dataset leakage risk:** Low. Authors explicitly state none of the study images were used for training RetCAD.

**Confounders:** The grading reference standard is constructed by a single primary grader (Grader 1). Grader 2 adjudication was applied selectively (only to cases flagged by RetCAD or disagreements), meaning the 6,042 jointly negative cases were never independently verified. This introduces a **verification bias**: the true false negative rate of Grader 1 alone (and potentially of RetCAD) in the non-flagged set cannot be determined.

**Augmentation inflation risk:** Not applicable.

**Metric reliability:** Sensitivity estimate (86/95) is based on a small numerator; point estimates without CI for sensitivity/specificity limit reliability assessment.

**Formula correctness:** Sensitivity = 86/95 = 90.53% ✓; Specificity = 6,051/6,230 = 97.13% ✓. Note: denominator for specificity is 6,230 (non-referable eyes per Grader 1), not 6,325 total eyes.

---

## 12. External Validity

**Cross-population transferability:** Limited. Single center, single country (Spain), single camera model (Topcon TRC-NW400, 45° FOV, non-mydriatic), single acquisition period. Mean patient age 64.7 years, 85% type 2 DM. Performance in different demographics, camera types, or higher-prevalence settings is untested in this study.

**Dataset portability:** The private dataset is available from corresponding author on request but is not a public benchmark. No cross-dataset comparison is performed within this paper.

**Clinical feasibility:** High within this specific setting. Real-world operational workflow integration is described. Authors acknowledge that integration into existing workflow "remains challenging" and prospective evaluation is needed.

**Hardware constraints:** [NOT REPORTED]

---

## 13. Strengths

- Fully independent evaluation dataset — no overlap with training data.
- Large, consecutively recruited real-world cohort from operational clinical practice.
- Commercially deployed, CE-marked system tested under genuine screening conditions.
- Dual-grader adjudication for cases of interest, with detailed flowchart of case distribution (Fig. 3).
- Bootstrap-derived 95% CI reported for AUC.
- Transparent reporting of false negative characteristics (scores, severity grades).
- Explicit acknowledgment of low prevalence as a confounding factor in workload reduction interpretation.

---

## 14. Limitations

**Explicit (stated by authors):**
- Single macular-centered field used rather than the preferred 7-field stereophotographic protocol (ETDRS); nasal DR lesions may be missed.
- Grader 2 adjudication only applied to RetCAD-flagged and discordant cases; false negatives shared by both RetCAD and Grader 1 were not detectable.
- Very low referable DR prevalence (1.5%) limits comparability to higher-prevalence populations.
- Prospective validation not performed.

**Implicit (methodological):**
- **Verification bias:** The 6,042 cases in the jointly negative bin were never independently verified; the true false negative rate in this set is unknown.
- **Conflict of interest:** Three authors (Engelberts, Luger, van Grinsven) are employees of Thirona, the developer of RetCAD; van Grinsven is also a shareholder. No independent replication.
- **No confidence intervals for sensitivity/specificity:** Point estimates only; uncertainty of key operating-point metrics is unreported.
- **Single camera, single site:** Limits generalizability to other imaging platforms and populations.
- **No comparison to alternative AI systems:** No benchmarking against other DR detection algorithms.
- **No Cohen's Kappa or inter-rater reliability for reference standard:** Grader agreement is described qualitatively, not quantified.
- **Class imbalance not methodologically addressed.**

---

## 15. Relevance to Dissertation

**Relevance to preprocessing dominance hypothesis:** Low direct relevance. Preprocessing is not a study variable; the RetCAD internal pipeline is proprietary and undisclosed. This study cannot be cited as evidence for or against preprocessing dominance.

**Relevance to cross-database validation:** Moderate. This study demonstrates that a system trained on one dataset can perform well on a fully independent real-world dataset, supporting the feasibility of cross-dataset generalization. However, it does not compare performance across multiple public benchmarks (EyePACS, Messidor, IDRiD).

**Relevance to EyePACS/Messidor benchmarking:** Low. Neither EyePACS nor Messidor is used or referenced as a comparator dataset.

**Relevance to Vision Transformer comparison:** None. The architecture is CNN-based and proprietary; no ViT comparison is made or discussed.

**Risk of contradiction:** Moderate. The extremely high AUC (0.988) and workload reduction (96%) achieved without disclosed preprocessing could be cited by reviewers to argue that preprocessing optimization is secondary to model quality and data volume — potentially weakening a preprocessing-dominance argument if not contextualized carefully. The very low disease prevalence (1.5%) must be emphasized when interpreting these results.

---

## 16. Citation-Ready Statements

1. "The RetCAD software obtained an AUC value of 0.988 [0.981:0.993] for the detection of referable DR" at the eye level, with sensitivity of 90.53% and specificity of 97.13% at a pre-defined threshold of 50 (Results, p. 6).

2. "Only 274 of the 6325 cases have to be checked for referable DR, whereas only six cases would have been missed. This is a workload reduction of 96%" (Results, p. 6).

3. "The prevalence of referrable DR was 1.5% in this study population" and "this might have influenced on achieving such a high workload reduction" (Discussion, p. 7).

4. "It is important to test a DL system using independent datasets and in different populations, as this will assure the generalizability of the software in any clinical setting" (Discussion, p. 7).

5. "Integration into existing workflow remains challenging and prospective evaluation needs to be carried out to assess the discrimination performance of the system in normal procedure screening workflow" (Discussion, p. 7).

6. "None of the images included in the dataset for this study were used for training the system" (Methods, p. 4), confirming fully independent evaluation.

7. The system "missed six cases with referable DR according to both human graders; none of them had sight-threatening disease and all six cases were scored just below the threshold of 50" (Discussion, p. 8).

---

## 17. Epistemic Classification

**Classification: Clinical validation precedent / Limited-scope study**

**Justification:** The study provides genuine real-world clinical validation evidence for a commercial CNN-based DR screening system on an independent dataset. Its epistemic weight is constrained by single-center design, conflict of interest from developer co-authorship, absence of comparative benchmarking, verification bias in the reference standard construction, and the atypically low disease prevalence that inflates workload reduction metrics. It is valuable as evidence of real-world deployability but does not constitute high-impact methodological evidence or a contribution to architectural or preprocessing knowledge.

---

## 18. Analytical Synthesis

This study provides clinically relevant but methodologically constrained evidence for the deployment of a CNN-based commercial DR detection system in a real-world screening setting. Its principal epistemic contribution is demonstrating that a system trained on independent data can achieve an AUC of 0.988 on a consecutively recruited tertiary care population, supporting the feasibility of cross-dataset transfer in operational clinical contexts. However, the study's epistemic weight for dissertation positioning is limited by several structural weaknesses: the 1.5% referable DR prevalence is exceptionally low and the authors themselves acknowledge it inflates the 96% workload reduction figure, making this metric non-comparable to standard benchmarks. The verification bias introduced by selective Grader 2 adjudication means the true false negative rate of the system in the non-flagged majority cannot be established, undermining the safety profile claim. The conflict of interest — three co-authors are employees of the system's commercial developer — further limits independence of interpretation. For a dissertation addressing preprocessing dominance, this article is largely neutral: preprocessing is not a study variable and the proprietary pipeline precludes any inference about its contribution to performance. The study could be cited to illustrate that commercial systems achieve high performance in real-world settings, but must be paired with methodologically stronger comparative studies to situate it appropriately. It neither strongly supports nor contradicts a preprocessing-dominance argument; it simply does not address the question.

---