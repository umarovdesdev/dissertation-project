LITERATURE CARD
Impact of CLAHE-Based Image Enhancement for Diabetic Retinopathy Classification Through Deep Learning
1. Bibliographic Metadata
Full Citation (APA 7): Hayati, M., Muchtar, K., Roslidar, Maulina, N., Syamsuddin, I., Elwirehardja, G. N., & Pardamean, B. (2023). Impact of CLAHE-based image enhancement for diabetic retinopathy classification through deep learning. Procedia Computer Science, 216, 57–66.
DOI: 10.1016/j.procs.2022.12.111
Journal / Conference: Procedia Computer Science (7th International Conference on Computer Science and Computational Intelligence 2022)
Year: 2023
Publication Type: Empirical study
Research Domain: Medical AI – Diabetic retinopathy classification – Image preprocessing (CLAHE) – CNN-based deep learning
2. Study Type Classification
Classification: CNN-based classification study; Preprocessing impact evaluation
Justification: The study evaluates the impact of CLAHE preprocessing on four CNN architectures (VGG16, ResNet34, InceptionV3, EfficientNetB4) for binary DR classification. It is not an external validation, cross-dataset, or clinical validation study. All experiments use a single dataset (APTOS 2019) with internal train/validation/test splits only.
3. Research Problem
Problem Addressed: Whether CLAHE-based image enhancement improves the accuracy of deep learning models for binary diabetic retinopathy classification compared to using original (unenhanced) fundus images.
Relation to: Preprocessing impact; Architecture comparison
The study is primarily related to preprocessing effects on classification accuracy. It does not address generalization, cross-dataset portability, lesion detection, clinical deployment, or architecture scaling in depth.
4. Datasets Used
Attribute	Value
Name	APTOS 2019 Blindness Detection (Kaggle)
Public / Private	Public
Sample Size	3,288 images total (1,489 positive / 1,799 negative)
Class Taxonomy	Binary (DR positive vs. negative). Note: APTOS 2019 originally has 5-class grading; authors collapsed to binary.
Train/Val/Test Split	70:20:10 per class. Train: 1,040+1,259=2,299; Val: 297+362=659; Test: 149+178=327
External Dataset Used?	No
Cross-Dataset Testing?	No

5. Preprocessing Pipeline
Resizing: 224 × 224 pixels (stated in hyperparameter table)
Cropping: [NOT REPORTED]
Normalization: [NOT REPORTED]
CLAHE: Applied; formula for clip limit (β) provided (Eq. 1) involving area size M, grey-level N=256, clip factor α (1–100), and S_max. Specific parameter values (clip limit, tile grid size) NOT explicitly reported.
Color Normalization: [NOT REPORTED]
Augmentation: [NOT REPORTED]
Image Quality Filtering: [NOT REPORTED]
Lesion Enhancement: Not applicable (binary classification, no lesion-level task)
6. Model Architecture
Attribute	Value
Architectures	VGG16, ResNet34, InceptionV3, EfficientNetB4
Architecture Type	CNN (multiple backbone comparison)
Pretraining Source	[NOT REPORTED] (implied ImageNet via transfer learning convention, not explicitly stated)
Transfer Learning Protocol	[NOT REPORTED] (fine-tuning implied but specifics such as frozen layers not stated)
Input Resolution	224 × 224
Loss Function	[NOT REPORTED]
Optimizer	SGD
Epochs	16
Batch Size	4
Learning Rate	0.01, decay 0.5, step size 3
Weight Decay	1×10⁻⁵
Hyperparameter Tuning	Random search (stated); no grid search performed

7. Validation Design
Internal Validation: Yes – 70/20/10 train/validation/test split from a single dataset
Cross-Validation: No
External Validation: No
Prospective Validation: No
Multi-Center Validation: No
All evaluation is performed on a single held-out test set from the same APTOS 2019 dataset. No external or cross-dataset testing was conducted.
8. Performance Metrics
8.1 Test Set Accuracy
Model	Original Accuracy	CLAHE Accuracy	Improvement
VGG16	0.8740 (87.40%)	0.9187 (91.87%)	+5.11%
ResNet34	0.9596 (95.96%)	0.8443 (84.43%)	−12.02%
InceptionV3	0.9080 (90.80%)	0.9520 (95.20%)	+4.85%
EfficientNetB4	0.9557 (95.57%)	0.9783 (97.83%)	+2.36%

8.2 Validation Set Accuracy (CLAHE)
Model	Val Accuracy (CLAHE)
VGG16	0.9803
ResNet34	0.9772
InceptionV3	0.9757
EfficientNetB4	0.9833

AUC: [NOT REPORTED]
Sensitivity: [NOT REPORTED]
Specificity: [NOT REPORTED]
F1 Score: [NOT REPORTED]
Cohen’s Kappa: [NOT REPORTED]
Confusion Matrix: [NOT REPORTED]
Statistical Tests: [NOT REPORTED]
Confidence Intervals: [NOT REPORTED]
9. Authors’ Claims
Performance Claim: CLAHE improves accuracy on 3 of 4 models (VGG16: +5.11%, InceptionV3: +4.85%, EfficientNetB4: +2.36%). Best result: EfficientNetB4 with CLAHE at 97.83% test accuracy.
Generalization Claim: CLAHE allows models to extract “more general features,” reducing the accuracy drop between validation and test sets for VGG16 and InceptionV3.
Clinical Applicability: Results are described as “useful in the computer-aided diagnosis of diabetic retinopathy.”
Superiority Claim: EfficientNetB4 with compound scaling outperforms other architectures; CLAHE enhancement benefits most models.
ResNet34 Anomaly: Authors attribute ResNet34’s accuracy drop with CLAHE (−12.02%) to suboptimal hyperparameters and lack of grid search, citing residual attention mechanisms as possibly requiring different tuning.
10. Empirical Support Assessment
Generalization Claims Supported?: Weakly. No external validation or cross-dataset testing was performed. Claims about “more general features” are inferred only from comparing validation vs. test accuracy drops on the same dataset.
External Validation Robust?: Not applicable – no external validation conducted.
Confidence Intervals Reported?: No.
Dataset Size Adequate?: Marginal. 3,288 images with a 327-image test set is small for robust conclusions across four architectures.
Class Imbalance Addressed?: Not explicitly. The dataset has moderate imbalance (1,489 vs. 1,799), and no resampling, class weighting, or imbalance-aware metrics (F1, AUC) are reported.
Statistical Testing Adequate?: No. No statistical significance tests, confidence intervals, or repeated runs reported. All conclusions are based on single-run accuracy comparisons.
11. Internal Validity
Overfitting Risk: High. Training accuracy reaches 0.9957–1.0000 across all models with only 16 epochs. Authors acknowledge VGG16 and ResNet34 show large drops from validation to test accuracy. EfficientNetB4 appears more stable.
Dataset Leakage Risk: Low. Per-class stratified split (7:2:1) is stated. However, no mention of patient-level splitting; if multiple images per patient exist in APTOS 2019, leakage is possible.
Confounders: Uniform hyperparameters across all architectures is a significant confounder. Authors acknowledge that per-model hyperparameter tuning was not performed, which particularly impacts ResNet34.
Augmentation Inflation Risk: Not applicable – no augmentation reported.
Metric Reliability: Low. Only accuracy is reported for a moderately imbalanced dataset. Accuracy alone is insufficient for clinical or robust scientific evaluation.
Formula Correctness: Questionable. The accuracy formula (Eq. 2) is stated as “Number of true positives / Number of data,” which is technically incorrect (should be TP+TN / Total). This may be a transcription error, but it raises concerns about methodological rigor.
12. External Validity
Cross-Population Transferability: Unknown. Single dataset from APTOS 2019 (Indian population). No testing on other demographics or imaging conditions.
Dataset Portability: Not demonstrated. No cross-dataset experiments (e.g., EyePACS, Messidor, IDRiD).
Clinical Feasibility: Not assessed. No clinical workflow integration, no ophthalmologist comparison, no prospective evaluation.
Hardware Constraints: Partially mentioned. Training times range from 13.8 minutes (ResNet34/CLAHE) to 4h30m (EfficientNetB4/CLAHE). Batch size of 4 suggests GPU memory constraints. Specific hardware not stated.
13. Strengths
• Direct comparative evaluation of CLAHE vs. original images across four architectures using a controlled experimental design (same hyperparameters, same split).
• Independent test set separate from validation set (10% held out).
• Detailed hyperparameter reporting (Table 2) enables partial reproducibility.
• Softmax confidence scores provided for EfficientNetB4 predictions (Tables 6–7), offering qualitative insight into model certainty.
• Acknowledges limitations honestly, including the ResNet34 anomaly and absence of hyperparameter grid search.
14. Limitations
14.1 Explicit (Stated by Authors)
• No hyperparameter grid search performed; uniform hyperparameters may disadvantage certain architectures (particularly ResNet34).
• No deeper analysis (e.g., Class Activation Maps) to explain how CLAHE affects feature extraction.
14.2 Implicit (Methodological)
• Only accuracy reported; no AUC, sensitivity, specificity, F1, or Cohen’s Kappa.
• No confidence intervals or statistical significance testing.
• No external/cross-dataset validation.
• No augmentation employed.
• CLAHE parameters (clip limit, tile size) not explicitly specified.
• Accuracy formula (Eq. 2) appears incorrect (TP/Total instead of (TP+TN)/Total).
• Small test set (327 images) limits statistical power.
• Single run per experiment; no repeated trials or variance reporting.
• Binary classification collapses APTOS 2019’s original 5-class grading, losing clinical granularity.
• Pretraining source not explicitly stated.
• No patient-level split verification.
15. Relevance to My Dissertation
Preprocessing Dominance Hypothesis: MODERATE-HIGH. Directly evaluates CLAHE’s impact on classification accuracy. Provides empirical evidence that preprocessing improves 3 of 4 models but also demonstrates that CLAHE can degrade performance for ResNet34, complicating a simple “preprocessing always helps” narrative.
Cross-Database Validation: LOW. No cross-dataset experiments conducted.
EyePACS/Messidor Benchmarking: NONE. Neither dataset used.
Vision Transformer Comparison: NONE. No ViT or transformer architectures evaluated.
Risk of Contradiction: MODERATE. The ResNet34 result (−12.02% with CLAHE) could be cited against a preprocessing-dominance argument if not contextualized with the authors’ explanation of uniform hyperparameters. The lack of robust metrics weakens the evidentiary weight in either direction.
16. Citation-Ready Statements
1. Hayati et al. (2023) demonstrated that CLAHE preprocessing improved binary DR classification accuracy for EfficientNetB4 from 95.57% to 97.83% on the APTOS 2019 dataset (p. 62, Table 5).
2. CLAHE yielded accuracy improvements for VGG16 (+5.11%), InceptionV3 (+4.85%), and EfficientNetB4 (+2.36%), but degraded ResNet34 performance by 12.02% under uniform hyperparameter settings (Hayati et al., 2023, p. 64).
3. The authors attributed ResNet34’s performance degradation under CLAHE to the use of uniform hyperparameters across all architectures, noting that per-model tuning was not conducted (Hayati et al., 2023, p. 64).
4. Training accuracy reached near-perfect values (0.9957–1.0000) across all models, while test accuracy ranged from 84.43% to 97.83%, suggesting possible overfitting in several architectures (Hayati et al., 2023, pp. 61–62).
5. The study reported only accuracy as the evaluation metric, without AUC, sensitivity, specificity, F1, or statistical significance testing, limiting the robustness of its conclusions (Hayati et al., 2023, pp. 60–64).
6. Hayati et al. (2023) inferred that CLAHE allowed models to extract “more general features,” as evidenced by smaller accuracy drops between validation and test sets for VGG16 and InceptionV3 (p. 64).
17. Epistemic Classification
Classification: Limited-Scope Study
Justification: The study addresses a narrow but relevant question (CLAHE’s impact on CNN-based DR classification) using a single public dataset without external validation, robust metrics, or statistical testing. The conference proceedings venue (Procedia Computer Science), small test set, and methodological gaps (single metric, no CI, possible formula error) place this firmly in the limited-scope category. It provides suggestive evidence for CLAHE’s utility but lacks the rigor to serve as high-impact empirical evidence or a benchmark study.
18. Analytical Synthesis
This study provides preliminary empirical evidence that CLAHE preprocessing can improve binary DR classification accuracy for most CNN architectures, with EfficientNetB4 achieving the highest accuracy at 97.83%. However, its epistemic weight is substantially limited by the absence of external validation, the reliance on a single evaluation metric (accuracy), and the lack of statistical testing or confidence intervals. The ResNet34 anomaly (−12.02% with CLAHE) introduces an important nuance: preprocessing effects are architecture-dependent and sensitive to hyperparameter configuration, which complicates any universal preprocessing-dominance argument. For dissertation positioning, this paper can be cited as supporting evidence that CLAHE enhances contrast-dependent feature extraction in CNNs, but it cannot be relied upon for generalization claims due to the absence of cross-dataset evaluation. The study does not engage with EyePACS, Messidor, or IDRiD benchmarks, nor with Vision Transformer architectures, limiting its direct utility for comparative framework construction. Its primary value lies in demonstrating that preprocessing impact is model-contingent, which actually strengthens the argument that preprocessing pipelines must be evaluated per-architecture rather than assumed universally beneficial. The conference venue and methodological limitations warrant cautious citation with appropriate caveats about evidentiary strength.
