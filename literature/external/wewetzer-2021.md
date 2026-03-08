LITERATURE CARD
PhD Dissertation Literature Review
Wewetzer, Held, & Steinhäuser (2021) — Meta-Analysis of DL Screening for DR in Primary Care
1. Bibliographic Metadata
Full Citation (APA 7)	Wewetzer, L., Held, L. A., & Steinhäuser, J. (2021). Diagnostic performance of deep-learning-based screening methods for diabetic retinopathy in primary care—A meta-analysis. PLoS ONE, 16(8), e0255034. https://doi.org/10.1371/journal.pone.0255034
DOI	10.1371/journal.pone.0255034
Journal	PLoS ONE
Year	2021
Publication Type	Meta-analysis
Research Domain	Medical AI / Deep learning screening / Diabetic retinopathy / Primary care diagnostics
2. Study Type Classification
Primary Classification	Meta-analysis
Secondary Classification	Systematic review of diagnostic test accuracy
Applicable Labels	Meta-analysis; Clinical validation precedent (primary care focus)
Justification: The study pools sensitivity and specificity data from 10 primary studies evaluating deep learning systems for DR detection specifically in primary care settings. It follows PRISMA-DTA guidelines and uses Meta-Disc 1.4 for statistical synthesis including SROC, DOR, and I² heterogeneity analysis.
3. Research Problem
Problem addressed: Determining the current diagnostic performance of deep learning-based screening methods for diabetic retinopathy (DR) in primary care (PC) settings, where prevalence differs substantially from secondary/tertiary care.
Related to: Clinical deployment (PC-specific applicability); Generalization (performance across heterogeneous populations and camera systems); Prevalence-adjusted predictive values.
The study emphasizes that diagnostic performance must be interpreted relative to disease prevalence in the target setting, as identical sensitivity/specificity yield different predictive values in low- vs. high-prevalence environments.
4. Datasets Used
This meta-analysis synthesized results from 10 primary studies. The datasets used in those studies included both clinical (prospective and retrospective) datasets and publicly available benchmark datasets. Individual dataset details as reported:
Study	Sample	Type	Setting	DR Type
Abràmoff et al. (2018)	819 patients	Clinical	10 PC sites	any DR/DME
Natarajan et al. (2019)	Not specified	Clinical	Community	rDR, any DR
Verbraak et al. (2019)	1,600 patients	Clinical retro.	PC center	vtDR, >mild DR
Walton et al. (2016)	>15,000 patients	Clinical	PC (IRIS)	vtDR
Bhaskaranand et al. (2019)	>100,000 patients	Retrospective	Cloud-based	rDR
Bellemo et al. (2019)	4,504 images	Clinical	Mobile (Zambia)	rDR, vtDR, DME
Kanagasingam et al. (2018)	193 patients	Clinical	PC	any DR
Ting et al. (2017)	76,370 images	Clinical	Singapore	any DR, rDR, vtDR
Gulshan et al. (2016)	EyePACS: 9,963; Messidor: 1,748	Retrospective	Public datasets	rDR
Raju et al. (2017)	>50,000 images	Clinical	Community	5-class NPDR/PDR

Cross-dataset testing: Not systematically performed across studies. Gulshan et al. (2016) validated on both EyePACS and Messidor datasets. No formal cross-dataset generalization testing was the focus of this meta-analysis.
5. Preprocessing Pipeline
The meta-analysis does not report preprocessing details for the individual DL systems. Specific preprocessing parameters are not extracted or compared.
Resizing	[NOT REPORTED]
Cropping	[NOT REPORTED]
Normalization	[NOT REPORTED]
CLAHE	[NOT REPORTED]
Color Normalization	[NOT REPORTED]
Augmentation	[NOT REPORTED]
Image Quality Filtering	[NOT REPORTED]
Lesion Enhancement	[NOT REPORTED]
6. Model Architecture
The meta-analysis pools results from multiple DL systems. Individual architectures reported include:
System/Study	Architecture	Details
IDx-DR (Abràmoff; Verbraak)	Multilayer CNN	FDA-cleared autonomous AI system
Natarajan et al.	CNN (smartphone-based)	Offline AI on smartphone
IRIS (Walton et al.)	Teleretinal AI system	CenterVue camera integration
EyeArt (Bhaskaranand et al.)	Cloud-based AI	Over 100,000 patients evaluated
Bellemo et al.	Two combined CNNs	Mobile screening in Zambia
Kanagasingam et al.	CNN	Topcon fundus camera
Ting et al.	CNN-based DL system	Multiethnic population
Gulshan et al.	DL algorithm (Inception)	Validated on EyePACS & Messidor
Raju et al.	DL (EyePACS application)	Multiple fundus cameras

Pretraining source: [NOT REPORTED at meta-analysis level]
Transfer learning protocol: [NOT REPORTED at meta-analysis level]
Input resolution: [NOT REPORTED at meta-analysis level]
Loss function / Optimizer / Epochs / Hyperparameters: [NOT REPORTED]
7. Validation Design
Meta-analysis level	Pooled analysis of 10 studies using Meta-Disc 1.4
Internal validation	QUADAS quality assessment tool applied to all studies
External validation	Not performed at meta-analysis level; individual studies used various validation designs
Cross-validation	Not applicable at meta-analysis level
Prospective validation	Some included studies were prospective (Abràmoff, Natarajan, Walton, Kanagasingam); others retrospective
Multi-center	Studies from multiple countries/centers but not coordinated multi-center design
Statistical methods	Pooled sensitivity/specificity, SROC, DOR, I², Cochrane’s Q, Chi², funnel plot
8. Performance Metrics
8.1 Pooled Meta-Analytic Results
Metric	Value	95% CI
Pooled Sensitivity	0.87	0.86–0.87
Pooled Specificity	0.90	0.90–0.90
SROC AUC	0.9543	SE(AUC) = 0.0177
Q*	0.8964	SE(Q*) = 0.0246
Pooled DOR (Random Effects)	80.21	41.29–155.80
Cochran-Q (DOR)	1591.28 (df=9, p=0.0000)	—
I² (Sensitivity)	99.2%	—
I² (Specificity)	99.8%	—
I² (DOR)	99.4%	—
8.2 Predictive Values by Prevalence
Scenario	PPV	NPV
DM Type 1 (prevalence 24%)	73%	95%
DM Type 2 (prevalence 10%)	49%	98%
8.3 Individual Study Performance (Sensitivity)
Study	Sensitivity	95% CI
Abràmoff 2018	0.87	0.82–0.92
Bellemo 2019	0.92	0.90–0.94
Bhaskaranand 2019	0.91	0.91–0.92
Gulshan EP 2016	0.90	0.88–0.92
Kanagasingam 2018	1.00	0.69–1.00
Natarajan 2019	0.85	0.65–0.96
Raju 2017	0.80	0.79–0.81
Ting 2017	0.91	0.87–0.93
Verbraak 2019	1.00	0.79–1.00
Walton 2016	0.67	0.63–0.70
8.4 Individual Study Performance (Specificity)
Study	Specificity	95% CI
Abràmoff 2018	0.90	0.87–0.92
Bellemo 2019	0.89	0.88–0.90
Bhaskaranand 2019	0.91	0.91–0.91
Gulshan EP 2016	0.98	0.98–0.98
Kanagasingam 2018	0.92	0.87–0.95
Natarajan 2019	0.92	0.87–0.95
Raju 2017	0.92	0.92–0.92
Ting 2017	0.92	0.91–0.92
Verbraak 2019	0.98	0.97–0.99
Walton 2016	0.73	0.72–0.74
Statistical tests: Cochrane’s Q, Chi², I², SROC curve, funnel plot for publication bias.
Confusion matrix: Provided as decision trees for 100,000 hypothetical persons at DM Type 1 (24%) and Type 2 (10%) prevalence.
Cohen’s Kappa: [NOT REPORTED]
F1 Score: [NOT REPORTED]
9. Authors’ Claims
•	Performance claim: Pooled sensitivity of 87% and specificity of 90% across included DL systems for DR detection in PC.
•	Clinical applicability claim: DL screening tools may offer novel diagnostic strategies for DR in PC, but differences in patient populations, thresholds, and detection accuracy do not allow for a general recommendation at this point.
•	Prevalence-dependence claim: Diagnostic performance must always be evaluated with regard to prevalence; PPV is significantly lower in low-prevalence PC settings than in high-prevalence tertiary care.
•	Exclusion claim: NPV of 98% for DM Type 2 in PC makes DL tools potentially suitable as a rule-out screening test.
•	Research gap claim: Research on AI for DR screening in PC is scarce, and more prospective clinical studies demonstrating safety, efficacy, and equity are needed.
•	Reference standard claim: Clinician graders used as reference standard in included studies were not validated against prognostic standards; intergrader agreement was reported in only 2 of 10 studies.
10. Empirical Support Assessment
Does data support generalization claims? Partially. The pooled results show consistently high sensitivity/specificity across diverse settings (Singapore, Zambia, USA, Europe), but extreme heterogeneity (I² = 99.2–99.8%) undermines the interpretability of pooled estimates. The authors appropriately note this limits general recommendations.
Is external validation robust? No. The meta-analysis pools studies with varying validation designs. No standardized external validation protocol was applied across studies. Some used public datasets (EyePACS, Messidor) while others used clinical cohorts.
Are confidence intervals reported? Yes. 95% CIs are reported for all individual study sensitivities, specificities, and DOR values, as well as for pooled estimates.
Is dataset size adequate? Highly variable. Ranges from 193 patients (Kanagasingam) to >100,000 (Bhaskaranand). The total pooled sample is substantial, but small-study effects are visible.
Is class imbalance addressed? Implicitly. The authors explicitly discuss how low DR prevalence in PC (10% for DM Type 2) affects PPV, demonstrating awareness of class imbalance effects on clinical utility. However, class imbalance within training sets of individual studies is not assessed.
Is statistical testing adequate? Yes, for a diagnostic test accuracy meta-analysis. Appropriate use of SROC, DOR, I², and funnel plot. However, bivariate random-effects model would have been preferable to the univariate approach.
11. Internal Validity
Overfitting risk: Not directly assessable at meta-analysis level. Individual studies varied in rigor; some used retrospective public datasets (higher overfitting risk) while others were prospective clinical validations.
Dataset leakage risk: Not assessed. The meta-analysis does not evaluate whether individual studies had proper train/test separation.
Confounders: Multiple confounders identified: different camera systems, varying patient populations, mixed DM types, heterogeneous grading scales, and different DR severity thresholds pooled together.
Augmentation inflation risk: Not assessable; preprocessing/augmentation details not extracted.
Metric reliability: Moderate. The extreme heterogeneity (I² > 99%) suggests the pooled point estimates should be interpreted cautiously. The SROC AUC of 0.9543 provides a more robust summary measure.
Formula correctness: PPV/NPV calculations verified: ppv = (Sens × Prev) / (Sens × Prev + (1-Spec) × (1-Prev)). Figures 4 and 5 confirm correct application with explicit TP/FP/FN/TN counts.
12. External Validity
Cross-population transferability: Limited. Studies included populations from USA, Netherlands, India, Zambia, Singapore, and Australia, providing geographic diversity. However, the authors note that the study population was diverse in ethnicity and that it cannot be concluded whether DL tools are equally suitable for both DM types.
Dataset portability: Mixed. Some studies used publicly available datasets (EyePACS, Messidor); others used proprietary clinical data. The authors note that data obtained using publicly available datasets lack evaluation in real-life screening programs.
Clinical feasibility: Moderate. Several systems (IDx-DR, EyeArt, IRIS) are designed for PC deployment. The authors note that DL screening tools may be easily learned by non-ophthalmologist practitioners. Non-mydriatic fundus photography is feasible in PC.
Hardware constraints: Multiple camera systems used across studies (Topcon TRC-NW200, CenterVue, smartphones, digital retinopathy system cameras). Direct comparison is hindered by varying camera quality.
13. Strengths
•	First meta-analysis specifically evaluating DL-based DR screening in primary care settings (claimed by authors).
•	Prevalence-adjusted analysis: Explicitly calculates PPV and NPV for PC-specific DR prevalence rates (10% and 24%), demonstrating clinical utility in context.
•	Systematic methodology: PRISMA-DTA compliant, QUADAS quality assessment, dual-researcher screening and extraction, Meta-Disc statistical analysis.
•	Comprehensive heterogeneity analysis including I², Cochrane’s Q, Chi², and funnel plot for publication bias assessment.
•	Multi-perspective discussion covering physician, patient, and societal applicability.
14. Limitations
14.1 Explicit (Stated by Authors)
•	Included studies were very distinct and study quality was heterogeneous.
•	Presence of statistical heterogeneity (I² > 99%).
•	Lack of appropriate studies on AI in DR screening specifically in primary care.
•	Included studies lacked preregistration; safety and lack of bias cannot be proven.
•	Reference standard clinicians were not validated against prognostic standards.
•	Wide range in quality and quantity of training/validation data across studies.
•	Asymmetric funnel plot suggesting possible publication bias.
•	Multiple different camera systems with varying quality hinder direct comparison.
14.2 Implicit (Methodological Assessment)
•	Pooling of any DR, rDR, and vtDR as “any DR” introduces classification heterogeneity that inflates apparent agreement.
•	Univariate pooling of sensitivity and specificity separately rather than bivariate random-effects model (e.g., Reitsma model) may produce biased estimates.
•	No subgroup analysis by DL architecture type, camera system, or DR severity.
•	No extraction or analysis of preprocessing pipelines, preventing assessment of preprocessing impact on performance.
•	Search limited to 2015+ and English-only publications, potentially excluding relevant work.
•	Search conducted March 2020; does not capture subsequent significant publications in the field.
•	Only 10 studies included, limiting statistical power and generalizability of meta-analytic conclusions.
15. Relevance to My Dissertation
Preprocessing dominance hypothesis	LOW RELEVANCE. The meta-analysis does not extract or analyze preprocessing pipelines. It provides no evidence for or against preprocessing dominance. However, the extreme heterogeneity (I² > 99%) could partially reflect uncontrolled preprocessing variation across studies—a point that could be cited to argue for the need to investigate preprocessing as a confounding variable.
Cross-database validation	MODERATE RELEVANCE. The meta-analysis includes studies using different datasets (EyePACS, Messidor, proprietary clinical datasets) but does not perform formal cross-dataset analysis. The observed heterogeneity indirectly supports the argument that DL models behave differently across datasets.
EyePACS/Messidor benchmarking	MODERATE RELEVANCE. Gulshan et al. (2016) results on both EyePACS (AUC 0.991) and Messidor (AUC 0.990) are included. Raju et al. (2017) also used EyePACS. These provide reference performance values from benchmark datasets.
Vision Transformer comparison	NO RELEVANCE. All included studies use CNN-based architectures. No Vision Transformer studies are included (search conducted March 2020, before ViT publication).
Risk of contradiction	LOW. The meta-analysis makes cautious claims that do not contradict a preprocessing-dominance argument. The authors’ emphasis on heterogeneity and uncontrolled variables actually supports the dissertation’s premise that unexamined factors (like preprocessing) may explain performance variation.
16. Citation-Ready Statements
•	Wewetzer et al. (2021) reported a pooled sensitivity of 87% (95% CI: 0.86–0.87) and pooled specificity of 90% (95% CI: 0.90–0.90) across 10 DL-based DR screening studies in primary care, with substantial heterogeneity (I² = 99.2% for sensitivity). [p. 7, Fig. 2]
•	At a DR prevalence of 10% in DM Type 2 primary care patients, the calculated NPV was 98% and PPV was 49%, indicating that a positive DL screening result would be correct in fewer than half of cases (Wewetzer et al., 2021, pp. 7–8). [Figs. 4–5]
•	The SROC AUC across included studies was 0.9543 (SE = 0.0177), with a pooled diagnostic odds ratio of 80.21 (95% CI: 41.29–155.80) using a random effects model (Wewetzer et al., 2021, p. 7). [Figs. 2–3]
•	Wewetzer et al. (2021) observed that the reference standard clinicians in all included studies were not validated against prognostic standards, and intergrader agreement was reported in only 2 of 10 studies (p. 9).
•	The funnel plot demonstrated asymmetric distribution, suggesting possible publication bias favoring larger studies with positive outcomes (Wewetzer et al., 2021, p. 9, Fig. 6).
•	Wewetzer et al. (2021) concluded that despite overall high diagnostic performance values, differences in patient populations, thresholds, and detection accuracy do not allow for a general recommendation to use DL screening tools in clinical practice (p. 10).
•	The included studies showed a wide range in the quality and quantity of data used to train and validate DL systems, which aggravates direct comparison of outcomes (Wewetzer et al., 2021, p. 11).
17. Epistemic Classification
Classification	Limited-scope meta-analysis with clinical validation relevance
Justification	This meta-analysis provides a useful but constrained synthesis of DL screening performance in primary care. Its epistemic weight is limited by: (1) only 10 included studies, (2) extreme statistical heterogeneity (I² > 99%), (3) no analysis of preprocessing or architectural factors, (4) pooling of different DR severity types. It does not qualify as a high-impact benchmark study due to these limitations. However, it is the first meta-analysis to address PC-specific DL screening and provides important prevalence-adjusted predictive values. Its primary value is as a clinical deployment precedent documenting the gap between laboratory performance and clinical utility in low-prevalence settings.
18. Analytical Synthesis
This meta-analysis carries moderate epistemic weight as the first systematic pooled analysis of DL-based DR screening specifically targeting primary care settings. Its principal contribution is the explicit demonstration that high sensitivity and specificity (87%/90%) translate to a PPV of only 49% in the low-prevalence Type 2 DM primary care population, a critical insight for clinical deployment that many DL studies overlook. The extreme heterogeneity (I² > 99%) across all metrics substantially weakens the reliability of pooled point estimates, though the SROC AUC (0.9543) provides a more stable overall assessment.
For the dissertation, this study neither strengthens nor weakens the preprocessing-dominance argument directly, as preprocessing was not extracted or analyzed. However, the documented extreme heterogeneity across studies using different pipelines, cameras, and populations provides indirect support for the hypothesis that unexamined technical factors—including preprocessing—may account for significant performance variation. The absence of preprocessing analysis in this meta-analysis can be cited as a gap that the dissertation aims to address.
The study does not demonstrate cross-dataset robustness; rather, it reveals that pooling results across heterogeneous datasets and DL systems produces unstable estimates. This finding is consistent with the dissertation’s expected argument that generalization claims require explicit cross-dataset validation rather than aggregation of single-dataset results. The inclusion of both EyePACS and Messidor performance data (via Gulshan et al., 2016) provides reference benchmarks, though these are single-study values rather than meta-analytic pooled estimates for those specific datasets.
