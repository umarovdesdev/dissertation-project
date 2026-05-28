LITERATURE CARD
PhD Dissertation Literature Review
1. Bibliographic Metadata
Full citation (APA 7): Voets, M., Møllersen, K., & Bongo, L. A. (2019). Reproduction study using public data of: Development and validation of a deep learning algorithm for detection of diabetic retinopathy in retinal fundus photographs. PLoS ONE, 14(6), e0217541.
DOI: https://doi.org/10.1371/journal.pone.0217541
Journal: PLoS ONE
Year: 2019
Publication type: Empirical (reproduction/reproducibility study)
Research domain: Deep learning for diabetic retinopathy detection; reproducibility in medical AI
2. Study Type Classification
•	Reproduction study of Gulshan et al. (JAMA, 2016)
•	EyePACS benchmarking (Kaggle EyePACS distribution)
•	Messidor-2 benchmarking
•	CNN-based classification study (InceptionV3)
Justification: The study explicitly re-implements the Gulshan et al. (2016) deep learning algorithm for referable diabetic retinopathy detection using publicly available datasets (Kaggle EyePACS and Messidor-2). It is a direct reproduction attempt, not a novel architecture or clinical validation study. It constitutes cross-dataset testing insofar as the training data (Kaggle EyePACS) differs from the original study’s proprietary training data, and performance is evaluated on both a held-out EyePACS test set and the external Messidor-2 benchmark.
3. Research Problem
The study addresses the reproducibility of deep learning results in medical image analysis, specifically attempting to reproduce the high-performing DR detection algorithm published by Gulshan et al. (JAMA 2016; 316(22)) using only publicly available data and a re-implemented codebase (original source code was not published).
This is related to:
•	Generalization: Whether performance reported on proprietary data can be achieved with public data.
•	Preprocessing: Differences in image quality, grading, and normalization between the original and reproduction data.
•	Clinical deployment: Demonstrates the gap between reported performance and what independent researchers can achieve, raising questions about real-world deployability of non-reproducible results.
4. Datasets Used
4.1 Kaggle EyePACS
Public/Private: Public (Kaggle competition)
Sample size: 88,702 total images; 57,146 for training/validation; 8,790 for testing
Class taxonomy: Binary (referable DR: moderate or worse DR vs. no/mild DR). Original 5-class ICDR scale grades available but collapsed to binary.
Train/validation/test split: 80%/20% of 57,146 for train/validation; 8,790 separate test set
External dataset: No (used for both training and internal testing)
Cross-dataset testing: Yes (model also tested on Messidor-2)
4.2 Messidor-2
Public/Private: Public (different distribution from original study; obtained from Abramoff)
Sample size: 1,748 images
Class taxonomy: Binary (referable DR). Per-patient grades (maximum grade of two eyes), not per-image as in original study.
Train/validation/test split: Used entirely as external test set
External dataset: Yes
Cross-dataset testing: Yes
5. Preprocessing Pipeline
Resizing: Images resized to 299×299 pixels (to match InceptionV3 input and ImageNet pretrained weights)
Cropping: Center and radius of fundus located; fundus centered in image
Normalization: Images normalized to [–1, 1] range
CLAHE: [NOT REPORTED]
Color normalization: [NOT REPORTED]
Augmentation: Applied same data augmentation settings as reported in Krause et al. (2017) [ref 23]; specific parameters not enumerated in this paper
Image quality filtering: One author (MV, non-ophthalmologist) manually graded all images for gradability using original study’s grading instructions. 19.9% of Kaggle images found ungradable. Training with vs. without ungradable images showed no significant performance difference.
Lesion enhancement: [NOT REPORTED]
6. Model Architecture
Architecture: InceptionV3 (CNN)
Pretraining source: ImageNet
Transfer learning: Weights pre-initialized from ImageNet; fine-tuned on DR data
Input resolution: 299×299 pixels
Loss function: [NOT REPORTED explicitly; binary prediction output]
Optimizer: RMSProp (following Krause et al., 2017)
Learning rate: 0.001
Weight decay: 4 × 10⁻⁵
Epochs: Early stopping with patience of 10 epochs; peak AUC on validation set as criterion (minimum AUC improvement of 0.01 required)
Ensemble: 10 networks trained on same data; final prediction = mean of ensemble predictions
Batch normalization: Applied after each convolutional layer
Output: Single binary prediction (moderate or worse DR), unlike original study which had 4 binary outputs
7. Validation Design
•	Internal validation: Yes (80/20 train/validation split of Kaggle EyePACS; AUC on validation set used for early stopping)
•	Cross-validation: No
•	External validation: Yes (Messidor-2 as external test set)
•	Prospective validation: No
•	Multi-center validation: No (Kaggle EyePACS provenance unclear; Messidor-2 is multi-center but used only as test set)
8. Performance Metrics
8.1 Reproduced Algorithm Results
Test Set	High Sens. (Sens.)	High Sens. (Spec.)	High Spec. (Sens.)	High Spec. (Spec.)
Kaggle EyePACS	90.6%	84.7%	83.6%	92.0%
Messidor-2	81.8%	71.2%	68.7%	88.5%

8.2 AUC Scores
Test Set	Reproduced AUC (95% CI)	Original AUC
Kaggle EyePACS	0.951 (0.947–0.956)	0.991
Messidor-2	0.853 (0.835–0.871)	0.990

Confusion matrix: [NOT REPORTED]
F1 / Cohen’s Kappa: [NOT REPORTED]
Statistical tests: 95% confidence intervals for AUC reported. No formal statistical comparison tests between reproduced and original results.
9. Authors’ Claims
Performance Claims
•	The reproduced algorithm achieved substantially lower performance than the original study on both test sets (AUC 0.951 vs. 0.991 on EyePACS; 0.853 vs. 0.990 on Messidor-2).
Generalization Claims
•	The results demonstrate the challenges of reproducing deep learning results when original data and code are unavailable.
•	Training on a single Kaggle EyePACS dataset may cause overfitting to camera and patient characteristics (per private communication with original authors, up to 10% AUC impact).
Clinical Applicability Claims
•	The authors do not claim clinical applicability of their reproduced algorithm.
•	They do not believe their results invalidate the original study’s main finding that deep learning can detect DR.
Recommendations
•	Deep learning studies should: (i) use public data or provide detailed data descriptions, (ii) publish source code or full preprocessing details, and (iii) report all hyperparameters.
10. Empirical Support Assessment
Does data support generalization claims? Partially. The large AUC gap (especially 0.853 on Messidor-2 vs. 0.990 original) robustly demonstrates that public-data reproduction fails to achieve original performance. However, the study cannot disentangle whether this is due to data quality, label quality (single vs. multiple grades), or methodological differences.
Is external validation robust? Limited. Messidor-2 serves as external validation but uses per-patient grades rather than per-image grades, introducing a systematic grading discrepancy.
Are confidence intervals reported? Yes, 95% CIs for AUC on both test sets.
Is dataset size adequate? The authors cite Gulshan et al.’s finding that performance plateaus around 40,000 images, and their training set (57,146) exceeds this threshold. However, the Messidor-2 test set (1,748 images) is relatively small.
Is class imbalance addressed? The authors maintained the same binary rDR class balance as the original study’s training set. Leftover images (mostly no-DR) were excluded to achieve this balance.
Is statistical testing adequate? Minimal. CIs are reported but no formal hypothesis tests comparing reproduced vs. original performance.
11. Internal Validity
Overfitting risk: Moderate. Early stopping with patience of 10 epochs mitigates overfitting. Ensemble of 10 networks also helps. However, the original authors noted potential overfitting to Kaggle camera/patient characteristics. The study acknowledges an overfitting component in the original study’s Figure 4B (100% vs. 65% specificity for training vs. test set).
Dataset leakage risk: Low. Training and test sets are separated. Kaggle EyePACS test set sampled independently.
Confounders: Multiple confounders make it impossible to attribute the performance gap to a single cause: (1) different data distribution, (2) single vs. multiple grades, (3) per-patient vs. per-image Messidor-2 grades, (4) absence of macular edema prediction, (5) potential hyperparameter suboptimality.
Augmentation inflation risk: Low. Augmentation settings adopted from the original study.
Metric reliability: AUC with 200 thresholds is standard. CIs reported.
12. External Validity
Cross-population transferability: The large performance drop on Messidor-2 (AUC 0.853) relative to EyePACS (AUC 0.951) suggests limited cross-dataset transferability when trained on a single data source. The original authors confirmed that single-source training can cause up to 10% AUC degradation.
Dataset portability: Low. The study directly demonstrates that switching from proprietary to public data, and from multi-graded to single-graded labels, substantially degrades performance.
Clinical feasibility: Not addressed. The reproduced algorithm’s performance levels (68.7% sensitivity on Messidor-2 at high-specificity operating point) would be clinically inadequate for screening.
Hardware constraints: No distributed training used (vs. original study); authors state this should not influence accuracy.
13. Strengths
•	Transparent reproduction methodology with open-source code and gradability grades published on GitHub.
•	Follows original study methodology as closely as possible given data constraints.
•	Uses ensemble of 10 networks as in the original study.
•	Reports 95% confidence intervals for AUC.
•	Private communication with original authors (Gulshan et al.) to understand discrepancies.
•	Systematic assessment of image gradability for all Kaggle images.
•	Clear articulation of four possible sources of performance deviation.
14. Limitations
14.1 Explicit (Stated by Authors)
•	Only one DR grade per image vs. multiple ophthalmologist grades in original study.
•	No macular edema grades available, so model outputs only one binary prediction.
•	Different EyePACS data distribution (Kaggle vs. proprietary).
•	Different Messidor-2 distribution (original no longer available).
•	Per-patient Messidor-2 grades may result in overcalling DR.
•	Gradability assessment by non-ophthalmologist.
•	Cannot determine which of four possible reasons caused performance deviation.
14.2 Implicit (Methodological)
•	No ablation study to isolate the contribution of individual factors (data quality, grading, hyperparameters) to the performance gap.
•	No formal statistical comparison test between original and reproduced results.
•	No analysis of failure cases or error patterns.
•	299×299 resolution acknowledged as potentially problematic for lesion detection, but no experiments with higher resolution.
•	Single preprocessing pipeline tested; no exploration of alternative preprocessing (e.g., CLAHE, green channel extraction).
•	No class-level performance analysis (e.g., per-severity breakdown).
15. Relevance to My Dissertation

Position in paradigm space (v5.3): P1 (end-to-end CNN; preprocessing as auxiliary step). Grounds (per SIR-9): although the paper is a *reproduction* of Gulshan 2016 rather than an original method paper, it operates within the same P1 framing (Inception-v3, end-to-end training, preprocessing as a fixed tuning configuration). Its principal finding is that *data provenance and labelling quality* drive performance, again treating preprocessing as an exogenous input condition rather than as an integral model component. Per CFC-2.9 / SIR-1, no theoretical "preprocessing is unimportant" claim is attributed to the authors.

Preprocessing dominance hypothesis: MODERATE-HIGH. The study implicitly supports the hypothesis that data quality and preprocessing (including label quality/multi-grading) are critical determinants of performance, potentially more so than architecture choice. The identical InceptionV3 architecture achieved vastly different results depending on data provenance and labeling quality. However, the study does not isolate preprocessing effects from data distribution effects.
Cross-database validation: HIGH. The study provides direct empirical evidence of cross-dataset performance degradation (AUC drop from 0.951 to 0.853 when moving from EyePACS to Messidor-2), which is a central concern in the dissertation.
EyePACS/Messidor benchmarking: HIGH. Provides concrete AUC benchmarks on both Kaggle EyePACS (0.951) and Messidor-2 (0.853) using InceptionV3 with ImageNet pretraining, serving as a baseline for comparison with other methods.
Vision Transformer comparison: LOW. No ViT architectures used; pre-Transformer-era study.
Risk of contradiction: LOW. The study’s findings (performance degradation with public data, cross-dataset drop) align with the dissertation’s expected arguments about the importance of preprocessing, data quality, and external validation.
16. Citation-Ready Statements
•	Voets et al. (2019) attempted to reproduce Gulshan et al.’s (2016) DR detection algorithm using publicly available data and achieved an AUC of 0.951 (95% CI, 0.947–0.956) on the Kaggle EyePACS test set and 0.853 (95% CI, 0.835–0.871) on Messidor-2, substantially below the originally reported AUC of 0.99 on both test sets (Table 1, p. 7).
•	The reproduction study demonstrated that training on a single public dataset (Kaggle EyePACS) with single-grade labels produced a 0.04 AUC drop on the same-source test set and a 0.137 AUC drop on the external Messidor-2 benchmark relative to the original study’s results (Table 1, p. 7).
•	Private communication with the original study’s authors indicated that training on a single EyePACS data source can cause overfitting to camera and patient characteristics, with up to 10% AUC impact on performance (p. 8).
•	The original study reported that performance declines by 36% when using only one grade per image instead of consensus grades, suggesting that label quality is a major factor in model evaluation (p. 8).
•	Voets et al. (2019) found that excluding ungradable images (19.9% of Kaggle EyePACS) during training did not significantly improve algorithm performance (p. 7–8).
•	The authors recommend that deep learning studies should (i) use public data or provide detailed data descriptions, (ii) publish source code or all preprocessing details, and (iii) report all hyperparameters (p. 9).
17. Epistemic Classification
Classification: Methodological Precedent / High-Impact Empirical Evidence
Justification: This study is one of the first published reproduction attempts of a landmark medical AI paper (Gulshan et al., 2016), making it a methodological precedent for reproducibility research in DR deep learning. The empirical evidence—specifically the quantified performance gap between original and reproduced results—carries high epistemic weight for arguments about data dependency, label quality, and the limitations of reported benchmark performance. It is not a foundational study (no novel method) nor a clinical validation, but it provides critical empirical grounding for claims about the fragility of deep learning performance under dataset shift.
18. Analytical Synthesis
Voets et al. (2019) carries substantial epistemic weight as one of the few rigorous reproduction studies targeting a landmark medical AI paper. The demonstrated AUC gap—particularly the 0.137 drop on Messidor-2—provides direct empirical evidence that reported deep learning performance in DR detection is not automatically transferable across data distributions or labeling protocols. For the dissertation, this study strongly supports the argument that preprocessing quality, data provenance, and label reliability (multi-grading vs. single-grading) are critical performance determinants, potentially overshadowing architecture choice (the same InceptionV3 architecture produces drastically different results depending on data conditions). The cross-dataset degradation from EyePACS to Messidor-2 directly reinforces the dissertation’s emphasis on external validation as a necessary condition for performance claims. However, the study’s inability to isolate individual contributing factors limits its utility for making precise causal claims about preprocessing dominance. The study does not contradict but rather complements the dissertation’s positioning: it demonstrates that high reported AUCs (0.99) may not generalize, and that reproduction with public data yields substantially lower but more realistic performance estimates. The open-source nature of this work also provides a reproducible baseline against which Transformer-era methods can be compared.


End of Literature Card
