LITERATURE CARD
PhD Dissertation Literature Review
1. Bibliographic Metadata
Full Citation (APA 7): Ting, D. S. W., Cheung, C. Y.-L., Lim, G., Tan, G. S. W., Quang, N. D., Gan, A., Hamzah, H., Garcia-Franco, R., San Yeo, I. Y., Lee, S. Y., Wong, E. Y. M., Sabanayagam, C., Baskaran, M., Ibrahim, F., Tan, N. C., Finkelstein, E. A., Lamoureux, E. L., Wong, I. Y., Bressler, N. M., ... Wong, T. Y. (2017). Development and validation of a deep learning system for diabetic retinopathy and related eye diseases using retinal images from multiethnic populations with diabetes. JAMA, 318(22), 2211–2223.
DOI: 10.1001/jama.2017.18152
Journal: JAMA (Journal of the American Medical Association)
Year: 2017
Publication Type: Empirical — Clinical validation study
Research Domain: Deep learning for automated diabetic retinopathy screening; multiethnic, multi-center clinical validation
2. Study Type Classification
•	External validation study — Primary validation on SIDRP 2014–2015 plus 10 external multiethnic datasets from different countries.
•	Cross-dataset validation — Model trained on SIDRP 2010–2013, validated on temporally separate SIDRP 2014–2015 and 10 geographically/ethnically distinct cohorts.
•	CNN-based classification study — Convolutional neural network architecture for binary classification of referable DR, vision-threatening DR, glaucoma, and AMD.
•	Clinical prospective-like validation — Evaluated within an ongoing national screening program (SIDRP), though retrospective in design.
Justification: The study is classified as a large-scale external validation study because it systematically evaluates a DLS trained on one temporal cohort against multiple independent datasets spanning different ethnicities, camera types, grading standards, and clinical settings. It is among the first to demonstrate cross-population transferability at this scale.
3. Research Problem
The study addresses the problem of validating a deep learning system (DLS) for detecting referable diabetic retinopathy, vision-threatening diabetic retinopathy, referable possible glaucoma, and referable age-related macular degeneration (AMD) using retinal images from multiethnic populations with diabetes. Specifically, it investigates whether a DLS trained on community-based screening images from Singapore can generalize to diverse populations with varying fundus pigmentation, image quality, and camera types.
Primary Focus: Generalization and clinical deployment feasibility
•	Generalization across ethnicities (Chinese, Malay, Indian, African American, Hispanic, Caucasian)
•	Generalization across camera types (Topcon, Canon, FundusVue, Carl Zeiss)
•	Generalization across clinical settings (community-based, population-based, clinic-based)
•	Clinical deployment models: fully-automated vs. semi-automated screening
4. Datasets Used
Training Dataset
Name: SIDRP 2010–2013 (Singapore National Diabetic Retinopathy Screening Program)
Public/Private: Private (national screening program)
Sample Size (DR training): 76,370 images; 38,185 eyes; 13,099 patients
Sample Size (Glaucoma training): 125,189 images; 59,616 eyes; 23,978 patients
Sample Size (AMD training): 72,610 images; 58,599 eyes; 23,306 patients
Class Taxonomy: Binary (referable vs. non-referable) for each condition
External Dataset: No (used as training source)
Primary Validation Dataset
Name: SIDRP 2014–2015
Public/Private: Private
Sample Size: 71,896 images; 35,948 eyes; 14,880 patients
Class Taxonomy: Binary (referable DR, vision-threatening DR, glaucoma, AMD)
Prevalence: Referable DR 3.0%; vision-threatening DR 0.6%; possible glaucoma 0.1%; AMD 2.5%
External Dataset: Yes (temporally separated from training set)
10 External Validation Datasets
Dataset	Images	Eyes	Patients	AUC	Setting
Guangdong (China)	15,798	7,899	3,970	0.949	Community
Singapore Malay Eye Study	3,052	1,526	763	0.889	Population
Singapore Indian Eye Study	4,512	2,256	1,128	0.917	Population
Singapore Chinese Eye Study	1,936	968	484	0.919	Population
Beijing Eye Study	1,052	526	263	0.929	Population
African American Eye Disease Study	1,968	984	492	0.980	Population
Royal Victoria Eye & Ear Hospital	2,302	1,151	588	0.983	Clinic
Mexican Study	1,172	586	343	0.950	Clinic
Chinese Univ. of Hong Kong	1,254	627	314	0.948	Clinic
Univ. of Hong Kong	7,706	3,853	1,932	0.964	Clinic

Total external validation: 40,752 images; n = 10 datasets. AUC range: 0.889–0.983.
Cross-dataset testing performed: Yes
5. Preprocessing Pipeline
•	Resizing: [NOT REPORTED]
•	Cropping: [NOT REPORTED]
•	Normalization: [NOT REPORTED]
•	CLAHE: [NOT REPORTED]
•	Color normalization: [NOT REPORTED]
•	Augmentation: [NOT REPORTED]
•	Image quality filtering: Not applied as primary analysis; subsidiary analysis performed on subset with no media opacity (n = 35,055 eyes, 97.4%)
•	Lesion enhancement methods: [NOT REPORTED]
Note: The article provides minimal preprocessing details. Technical details are referenced in eFigure 1 in the Supplement, which is not available in this document. The study explicitly notes that images were of varying quality, including ungradable images, and were captured in JPEG format at 5–7 megapixels (except Hispanic cohort at <1 megapixel).
6. Model Architecture
Architecture Type: Convolutional Neural Network (CNN) — specific architecture not named in the main text
Pretraining Source: [NOT REPORTED in main text]
Transfer Learning Protocol: [NOT REPORTED in main text]
Input Resolution: [NOT REPORTED]
Loss Function: [NOT REPORTED]
Optimizer: [NOT REPORTED]
Epochs: [NOT REPORTED]
Hyperparameters: [NOT REPORTED] — Technical details deferred to eFigure 1 in the Supplement
Note: The authors describe the DLS as a convolutional neural network that implicitly recognizes characteristics of the target conditions from retinal image appearance. Three separate networks were trained for DR, glaucoma, and AMD respectively. The operating threshold was selected to achieve a predetermined optimal sensitivity of 90% on the training set.
7. Validation Design
•	Internal validation: No pure internal validation reported; threshold selected on training data (SIDRP 2010–2013).
•	Cross-validation: Not performed.
•	External validation: Yes — Primary validation on temporally separate SIDRP 2014–2015; additional validation on 10 independent multiethnic datasets.
•	Prospective validation: No (retrospective study design using anonymized retinal images).
•	Multi-center validation: Yes — 11 validation datasets across multiple countries, ethnicities, camera types, and clinical settings (community-based, population-based, clinic-based).
Subsidiary analyses: (1) Excluding 6,291 overlapping patients between training and validation; (2) High-quality image subset; (3) Subgroup analysis by age, sex, HbA1c; (4) Fully-automated and semi-automated screening model evaluation.
8. Performance Metrics
Primary Validation (SIDRP 2014–2015)
Condition	AUC (95% CI)	Sensitivity (95% CI)	Specificity (95% CI)
Referable DR	0.936 (0.925–0.943)	90.5% (87.3–93.0%)	91.6% (91.0–92.2%)
Vision-threatening DR	0.958 (0.956–0.961)	100% (94.1–100.0%)	91.1% (90.7–91.4%)
Possible Glaucoma	0.942 (0.929–0.954)	96.4% (81.7–99.9%)	87.2% (86.8–87.5%)
AMD	0.931 (0.928–0.935)	93.2% (91.1–99.8%)	88.7% (88.3–89.0%)

DLS vs. Trained Professional Graders (Primary Validation)
•	Referable DR sensitivity: DLS 90.5% vs. graders 91.2% (P = .68, not significant)
•	Referable DR specificity: DLS 91.6% vs. graders 99.3% (P < .001, graders significantly higher)
•	Vision-threatening DR sensitivity: DLS 100% vs. graders 88.5% (P < .001, DLS significantly higher)
•	Vision-threatening DR specificity: DLS 91.1% vs. graders 99.6% (P < .001, graders significantly higher)
External Validation (10 Datasets)
AUC Range for Referable DR: 0.889 to 0.983
Sensitivity Range: 91.8% to 100%
Specificity Range: 72.7% to 92.2%
Concordance: Most datasets showed >80% concordance between DLS and professional graders
Subgroup Analysis (AUC for Referable DR)
•	Age <60 years: AUC 0.980 (95% CI, 0.975–0.984)
•	Age ≥60 years: AUC 0.920 (95% CI, 0.899–0.940)
•	Men: AUC 0.952 (95% CI, 0.925–0.963)
•	Women: AUC 0.948 (95% CI, 0.933–0.956)
•	HbA1c <8%: AUC 0.938 (95% CI, 0.892–0.958)
•	HbA1c ≥8%: AUC 0.954 (95% CI, 0.942–0.964)
High-Quality Image Subset
AUC (no media opacity, n = 35,055): 0.968–0.973
Statistical Tests Used
•	McNemar test (comparing DLS vs. professional graders)
•	Cluster-bootstrap, biased-corrected 95% CIs (adjusted for patient-level clustering)
•	Exact Clopper-Pearson method for sensitivity estimates at boundary (100%)
•	2-sided tests; P < .05 significance level; no multiple comparison adjustment
•	Accuracy: [NOT REPORTED]
•	F1 Score: [NOT REPORTED]
•	Cohen’s Kappa: [NOT REPORTED]
•	Confusion matrix: Not provided as standard matrix; concordance/discordance counts reported in Table 5
9. Authors’ Claims
Performance Claims
•	The DLS had high sensitivity and specificity for identifying DR and related eye diseases using retinal images from multiethnic populations.
•	Sensitivity of the DLS for referable DR was comparable to trained professional graders (90.5% vs. 91.2%; P = .68).
•	For vision-threatening DR, the DLS achieved higher sensitivity than professional graders (100% vs. 88.5%; P < .001).
Generalization Claims
•	The DLS showed clinically acceptable performance (sensitivity ≥90%) across multiethnic populations of different communities, clinics, and settings.
•	AUCs >0.90 achieved for different camera types (FundusVue, Canon, Topcon, Carl Zeiss).
•	Comparable performance across subgroups stratified by age, sex, and glycemic control.
Clinical Applicability Claims
•	The DLS could be deployed in two screening models: a fully-automated model for communities without screening programs and a semi-automated model augmenting existing programs.
•	Simultaneous detection of DR, glaucoma, and AMD from a single retinal photograph is clinically valuable.
Superiority Claims
•	No explicit superiority claim over Gulshan et al. (2016); acknowledged lower AUC (0.936 vs. ~0.99) likely due to use of real-world screening images of varying quality rather than curated high-quality public datasets.
10. Empirical Support Assessment
Does data support generalization claims? Partially. The DLS demonstrated AUC >0.90 in 9 of 10 external datasets (exception: Singapore Malay Eye Study, AUC = 0.889). This provides strong evidence for cross-ethnic and cross-camera generalization, though specificity was notably lower in some populations (e.g., Singapore Indian Eye Study: 73.3%; Singapore Chinese Eye Study: 76.3%).
Is external validation robust? Yes. The use of 10 independent datasets spanning 6 ethnicities, 4 camera types, and 3 clinical settings represents one of the most comprehensive external validation designs in the DR deep learning literature as of 2017.
Are confidence intervals reported? Yes. Cluster-bootstrap, biased-corrected 95% CIs were reported for all AUC, sensitivity, and specificity values, appropriately accounting for patient-level clustering.
Is dataset size adequate? Yes. Total of 494,661 images (76,370 training; 71,896 primary validation; 40,752 external validation for DR). This was among the largest datasets in the field at time of publication.
Is class imbalance addressed? Partially. The low prevalence of referable DR (3.0%) and especially vision-threatening DR (0.6%) in the primary validation set reflects real-world screening conditions. However, no explicit class balancing techniques (e.g., oversampling, class weighting) are described.
Is statistical testing adequate? Largely yes. McNemar test is appropriate for paired comparisons. However, no adjustment for multiple comparisons across the 10 external datasets was performed, and the authors acknowledge this limitation.
11. Internal Validity
Overfitting Risk: Moderate-Low. The authors addressed the overlap of 6,291 patients appearing in both training (SIDRP 2010–2013) and primary validation (SIDRP 2014–2015) sets by performing a subsidiary analysis excluding these patients, which showed similar performance. However, both datasets originate from the same screening program, introducing potential distributional similarity bias.
Dataset Leakage Risk: Low for external datasets. Partially mitigated for primary validation through temporal separation and subsidiary exclusion analysis. The 6,291 overlapping patients represent a notable methodological concern that was appropriately addressed.
Confounders: Reference standards varied across datasets (retinal specialists, ophthalmologists, trained graders, optometrists), introducing measurement heterogeneity. This could inflate or deflate reported performance depending on grader quality.
Augmentation Inflation Risk: [NOT ASSESSABLE] — No augmentation details reported.
Metric Reliability: High. Use of cluster-bootstrap CIs accounting for bilateral eye correlation is methodologically appropriate. AUC as the primary metric is suitable for the binary classification task with class imbalance.
12. External Validity
Cross-Population Transferability: Strong. Demonstrated across Chinese, Malay, Indian, African American, Hispanic, and Caucasian populations. This multiethnic validation is a key strength and addresses a critical gap in prior DR-DLS literature (e.g., Gulshan et al., 2016, validated only on curated US-based datasets).
Dataset Portability: Demonstrated across 4 camera types (Topcon, Canon, FundusVue, Carl Zeiss) and 3 clinical settings. However, all training data originated from a single national program in Singapore, limiting assessment of training data portability.
Clinical Feasibility: Supported by the evaluation of fully-automated and semi-automated deployment models. The semi-automated model achieved sensitivity 91.3% and specificity 99.5% for overall referable status, closely approximating existing grader performance.
Hardware Constraints: [NOT REPORTED]
13. Strengths
•	Largest multiethnic validation of a DR deep learning system at the time of publication (494,661 total images).
•	Ten independent external validation datasets spanning 6 ethnicities, 4 camera types, and 3 clinical settings.
•	Simultaneous evaluation of DR, glaucoma, and AMD from the same retinal images.
•	Use of a real-world screening program (SIDRP) rather than curated public datasets, enhancing ecological validity.
•	Appropriate statistical methods: cluster-bootstrap CIs, McNemar test, Clopper-Pearson for boundary estimates.
•	Subsidiary analyses addressing patient overlap, image quality effects, and demographic subgroups.
•	Direct comparison of DLS performance against trained professional graders using the same reference standard.
•	Evaluation of both fully-automated and semi-automated clinical deployment models.
14. Limitations
Explicit (Stated by Authors)
•	Training set grading was not entirely based on retinal specialist assessment; reference standards varied across external datasets.
•	The DLS is a black-box model that does not show actual DR lesions, which may affect physician acceptance.
•	Identification of diabetic macular edema from fundus photographs may miss cases requiring OCT.
Implicit (Methodological)
•	Preprocessing pipeline and architectural details are insufficiently reported in the main text, severely limiting reproducibility.
•	No lesion-level analysis; only image-level binary classification assessed.
•	No comparison with other published DLS architectures (e.g., Inception used by Gulshan et al.).
•	Specificity was consistently lower for the DLS compared to professional graders, suggesting a systematic trade-off that may increase false-positive burden in screening programs.
•	The very low prevalence of vision-threatening DR (0.6%) and possible glaucoma (0.1%) in the primary validation set limits the statistical power and reliability of performance estimates for these conditions.
•	No cost-effectiveness analysis or implementation feasibility data provided.
•	Retrospective study design; no prospective real-world deployment evaluation.
•	F1 score, Cohen’s Kappa, and accuracy not reported, limiting comparability with other studies.
15. Relevance to My Dissertation
 
Relevance to preprocessing dominance hypothesis: HIGH. This study provides indirect evidence that preprocessing may not be the dominant factor in DR classification performance. The DLS was validated on images of varying quality from different cameras without reported preprocessing standardization, yet achieved AUC >0.90 in most datasets. The subsidiary analysis showing improved AUC (0.968–0.973) on high-quality images (no media opacity) vs. the full dataset (AUC 0.936) provides quantitative evidence that image quality affects but does not determine DLS performance.
Relevance to cross-database validation: CRITICAL. This is one of the most comprehensive cross-database validation studies in DR deep learning, validating across 10 independent datasets. It directly supports the dissertation argument that cross-database validation is essential for establishing DLS generalizability.
Relevance to EyePACS/Messidor benchmarking: LOW–MODERATE. The study does not use EyePACS or Messidor datasets. However, it explicitly contrasts its approach (real-world screening images) with studies using these public databases and argues that public database performance may overestimate clinical performance.
Relevance to Vision Transformer comparison: LOW. Published in 2017, this study predates the Vision Transformer era. It serves as a CNN-era baseline for comparison with subsequent ViT-based approaches.
Risk of contradiction: MODERATE. The strong cross-dataset generalization achieved without reported preprocessing could be interpreted as evidence against the preprocessing dominance hypothesis. However, the consistent drop in specificity across datasets and the AUC improvement with higher-quality images suggest that image characteristics do meaningfully influence performance.
16. Citation-Ready Statements
1.	Ting et al. (2017) validated a deep learning system for detecting referable DR across 10 multiethnic external datasets spanning 6 ethnicities and 4 camera types, achieving AUC values ranging from 0.889 to 0.983 (n = 40,752 images).
2.	In the primary validation dataset (n = 71,896 images; 14,880 patients), the DLS achieved an AUC of 0.936 (95% CI, 0.925–0.943) for referable DR with sensitivity of 90.5% and specificity of 91.6%, compared to professional graders who achieved 91.2% sensitivity and 99.3% specificity (Ting et al., 2017).
3.	The DLS demonstrated 100% sensitivity (95% CI, 94.1%–100.0%) for vision-threatening DR, significantly exceeding trained professional graders at 88.5% (P < .001), though with lower specificity (91.1% vs. 99.6%, P < .001; Ting et al., 2017).
4.	When evaluated on a high-quality image subset with no media opacity (n = 35,055 eyes), the DLS AUC for referable DR increased to 0.968–0.973, compared to 0.936 on the full dataset, indicating that image quality meaningfully affects but does not determine DLS diagnostic performance (Ting et al., 2017).
5.	Ting et al. (2017) demonstrated that a single DLS could simultaneously detect referable DR (AUC 0.936), possible glaucoma (AUC 0.942), and AMD (AUC 0.931) from retinal photographs, representing one of the first multi-disease DLS evaluations in ophthalmology.
6.	The study by Ting et al. (2017) used nearly 500,000 retinal images from a national screening program in Singapore with varying image quality, including ungradable images, rather than curated public databases, providing one of the most ecologically valid evaluations of DLS performance for DR screening.
7.	A semi-automated screening model combining DLS triage with secondary professional grader assessment achieved 91.3% sensitivity and 99.5% specificity for detecting overall referable status, suggesting a practical deployment pathway for augmenting existing screening programs (Ting et al., 2017).
17. Epistemic Classification
Classification: Foundational + High-impact empirical evidence + Clinical validation precedent
Justification: This study is foundational because it established the paradigm for multiethnic, multi-center DLS validation in diabetic retinopathy, moving the field beyond single-dataset public benchmark evaluations. It constitutes high-impact empirical evidence by providing the largest external validation dataset (at the time) with rigorous statistical methodology and 95% CIs. It also serves as a clinical validation precedent by evaluating the DLS within an ongoing national screening program and proposing fully-automated and semi-automated deployment models. Published in JAMA, it set the standard for subsequent clinical validation studies in ophthalmic AI.
18. Analytical Synthesis
This study carries substantial epistemic weight in the DR deep learning literature as one of the first large-scale, multiethnic clinical validation studies published in a top-tier medical journal. Its primary contribution to the dissertation is the demonstration that cross-dataset generalization is achievable with a CNN-based DLS, even when trained on data from a single national screening program, across diverse populations and camera systems. The consistent AUC >0.90 across most external datasets (9 of 10) supports the feasibility of generalized DR screening but with an important caveat: specificity was consistently lower for the DLS than for human graders, and performance varied by ethnicity and dataset characteristics. The finding that AUC improved from 0.936 to 0.968–0.973 on high-quality images provides partial support for the preprocessing dominance hypothesis, as it quantifies the performance cost of image quality variability. However, the overall strong performance without reported preprocessing standardization could also be interpreted as evidence that raw model capacity can partially compensate for image quality variation. The lack of detailed preprocessing and architectural reporting limits the extent to which this study can inform specific preprocessing pipeline recommendations. For the dissertation, this paper is best positioned as foundational evidence for the importance of cross-database validation and as a benchmark against which preprocessing-enhanced approaches can be compared.

