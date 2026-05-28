# Literature Card: Saxena et al. (2020)

---

# 1. Bibliographic Metadata

- **Full citation (APA 7):** Saxena, G., Verma, D. K., Paraye, A., Rajan, A., & Rawat, A. (2020). Improved and robust deep learning agent for preliminary detection of diabetic retinopathy using public datasets. *Intelligence-Based Medicine, 3–4*, 100022.
- **DOI:** https://doi.org/10.1016/j.ibmed.2020.100022
- **Journal:** Intelligence-Based Medicine (Elsevier)
- **Year:** 2020
- **Publication type:** Empirical / benchmark validation
- **Research domain classification:** Medical image analysis; automated diabetic retinopathy screening; CNN-based binary classification; cross-dataset generalization

---

# 2. Study Type Classification

- **CNN-based classification study** — primary classification
- **Cross-dataset validation** — models trained on EyePACS, tested on Messidor-1 and Messidor-2
- **EyePACS benchmarking** — EyePACS used as training and internal test source
- **Messidor benchmarking** — both Messidor-1 and Messidor-2 used as external benchmark test sets

**Justification:** The study trains InceptionResNetV2-based CNN ensemble models on a non-adjudicated EyePACS subset and evaluates performance on held-out EyePACS images and two external benchmark datasets (Messidor-1, Messidor-2). No prospective clinical deployment is performed.

---

# 3. Research Problem

- **Specific problem:** Binary classification of fundus images for any-grade DR detection (DR grades 1–4 vs. grade 0) using only publicly available, non-adjudicated datasets.
- **Related to:**
  - **Generalization:** Explicitly addressed — authors test whether models trained on EyePACS generalize to Messidor datasets.
  - **Preprocessing:** Central concern — intelligent cropping, augmentation strategy, and image resolution are extensively analyzed.
  - **Architecture scaling:** Examined through comparison of InceptionV3 vs. InceptionResNetV2 and ablation of input resolution (299×299 vs. 512×512).
  - **Clinical deployment:** Addressed via runtime testing on commodity hardware and web-based prototype demonstration.
  - **Lesion detection:** Not the primary focus; heatmaps are generated post hoc for visualization only.

---

# 4. Datasets Used

**Dataset 1: EyePACS (Training + Internal Test)**
- Public (available via Kaggle)
- Total: 88,702 images; 71,049 selected as gradable
- Class taxonomy: 5-class (0–4); reframed as binary (0 vs. 1–4)
- From 71,049 gradable images: 14,210 randomly held aside as test set; remaining 56,839 used as train set; within train set, 80%/20% random split for train/validation per run
- Train set: 56,839 images (42,197 negative, 14,642 positive — ~26% positive)
- Test set: 14,210 images (~26% positive, inferred from Fig. 4: 10,501 negative, 3,709 positive)
- External dataset used: No (same source as training)
- Cross-dataset testing performed: No (internal test only for EyePACS)

**Dataset 2: Messidor-2 (External Test)**
- Public
- 1,748 images (1,017 negative, 727 positive — ~41% positive per text; Fig. 4 shows 1,017 negative and 727 positive… note: abstract states 1,017 negative and 727 positive adding to 1,744 — minor discrepancy, article states 1,748)
- Class taxonomy: binary (positive/negative per retinopathy grade)
- No train/validation split — used as test only
- External dataset: Yes
- Cross-dataset testing: Yes

**Dataset 3: Messidor-1 (External Test)**
- Public
- 1,200 images (546 negative, 654 positive — ~54% positive per Fig. 4)
- Acquired from 3 ophthalmologic departments; 800 images with pupil dilation, 400 without
- Class taxonomy: retinopathy grade (0–3) mapped to binary; risk of macular edema (0–2) [NOT REPORTED how macular edema labels were handled in binary mapping]
- No train/validation split — used as test only
- External dataset: Yes
- Cross-dataset testing: Yes

---

# 5. Preprocessing Pipeline

**Offline (applied to all sets):**
- Cropping: Black border removal; circular disk centered; images cropped to square shape
- Resizing: Multiple resolutions tested — 256, 299, 512, 598 pixels; optimal identified as 512×512
- Normalization: Pixel values normalized between 0.0 and 1.0

**Online augmentation (training only):**
- Rotation: Random angle 0–10°
- Flips: Random vertical flips
- Brightness: Additive random factor β ∈ [−0.3, 0.3]; X'ᵢⱼ = Xᵢⱼ + β
- Contrast: Per-channel multiplicative factor α ∈ [0.8, 1.2]; X'ch = (Xch − Xch_mean) × α + Xch_mean

**Not applied:**
- CLAHE: [NOT REPORTED / NOT APPLIED]
- Color normalization (beyond per-channel contrast): [NOT REPORTED]
- Image quality filtering: Gradability scores from external reference [26] used for selection; non-detectable retinal disk images excluded algorithmically
- Lesion enhancement: [NOT APPLIED]

---

# 6. Model Architecture

- **Architecture type:** CNN ensemble — InceptionV3 and InceptionResNetV2; final best results from InceptionResNetV2; ensemble via averaging
- **Pretraining source:** [NOT REPORTED explicitly — ImageNet pretraining implied by reference to "pre-trained models built on ImageNet dataset" in discussion but not confirmed as the initialization source for their specific models]
- **Transfer learning protocol:** [NOT REPORTED — fine-tuning vs. feature extraction distinction not stated]
- **Input resolution:** 512×512 pixels (optimal; also tested 256, 299, 598)
- **Loss function:** Binary cross-entropy, weighted by class weights
- **Optimizer:** RMSProp
- **Epochs:** Early stopping triggered in range 50–70 epochs; initial learning rate 10⁻³, reduced by factor 10⁻¹ twice across three training stages
- **Batch size:** 16
- **Additional hyperparameters:** Early stopping delta = 10⁻⁴, patience = 10; monitoring parameter = validation AUC; model checkpointed at each epoch saving best weights; brute-force search for optimal ensemble weight combination
- **Ensemble:** Multiple models trained on different random 80/20 splits of EyePACS train set; outputs averaged
- **Classifier head experiments:** CNN features tested with XGBoost, SVM, and ANN — ANN found best; over/under-sampling found unhelpful

---

# 7. Validation Design

- **Internal validation:** Yes — 20% random split of EyePACS train set used as validation during hyperparameter tuning per training run
- **Cross-validation:** No — random split approach used instead of k-fold
- **External validation:** Yes — Messidor-1 and Messidor-2 used as external test sets (no overlap with training data)
- **Prospective validation:** No
- **Multi-center validation:** Not prospective; Messidor datasets derive from multiple clinical sites but were used retrospectively as benchmark test sets
- **Note:** EyePACS test set (14,210 images) is held out from the same distribution as training data; Messidor datasets constitute the only true external/cross-dataset evaluation

---

# 8. Performance Metrics

**Messidor-1:**
- AUC: 0.958
- Sensitivity: 88.84%
- Specificity: 89.92%
- Confidence intervals: [NOT REPORTED]

**Messidor-2:**
- AUC: 0.92
- Sensitivity: 81.02%
- Specificity: 86.09%
- Confidence intervals: [NOT REPORTED]

**EyePACS Test Set (14,210 images):**
- AUC: 0.927
- Sensitivity: 83.74% [Note: Table 2 reports 84.74% for sensitivity on EyePACS — discrepancy between text (p.6: "83.74%") and Table 2 ("84.74%"); exact value unclear]
- Specificity: 89.65%
- Confidence intervals: [NOT REPORTED]

**Additional metrics reported for ablation (299×299 input):**
- Messidor-1 AUC: 0.91
- Messidor-2 AUC: 0.86

**Future work preliminary results (Messidor-2):**
- Binary classification DR grades 1–2 vs. 0: AUC 0.91
- Multi-class classification: AUC 0.95

**Accuracy:** [NOT REPORTED as primary metric]
**F1 score:** Mentioned as a metric used but results [NOT REPORTED in main tables]
**Cohen's Kappa:** [NOT REPORTED for model output; cited from literature for inter-grader agreement range 0.40–0.65]
**Confusion matrix:** [NOT REPORTED]
**Statistical tests:** [NOT REPORTED — no significance testing, no CIs]
**Operating point selection:** Shortest Euclidean distance from (0,1) on ROC curve

---

# 9. Authors' Claims

**Performance claims:**
- AUC values on Messidor-1 and Messidor-2 are higher than closest non-adjudicated comparison studies by ~7.8% and ~6.4%, respectively
- InceptionResNetV2 outperforms all other CNN versions tested
- 512×512 input resolution outperforms 299×299 (Messidor-1 AUC: 0.958 vs. 0.91; Messidor-2: 0.92 vs. 0.86)

**Generalization claims:**
- Small AUC differences between EyePACS test set and Messidor datasets (~0.03 and ~0.007) indicate models have not overfitted to EyePACS-specific features
- Authors conclude models "have learned just the right set of features; specific to DR and not specific to the EyePACS dataset"

**Clinical applicability claims:**
- Response time of 0.5–2.0 seconds on commodity hardware makes system suitable for clinical settings
- Batch processing and minimal domain knowledge requirement increase operational feasibility
- System can be deployed on smartphones, laptops, desktops, and servers

**Superiority claims:**
- Results "stand competitive" with adjudicated-dataset studies, achieving AUC only ~2.1% below nearest adjudicated study [12] and ~7.0% below highest [13] on Messidor-2
- Among non-adjudicated studies, authors claim best published results on both Messidor-1 and Messidor-2

---

# 10. Empirical Support Assessment

**Does data support generalization claims?**
Partially. The AUC consistency across EyePACS test, Messidor-1, and Messidor-2 (0.927, 0.958, 0.920) is a reasonable indicator of cross-dataset robustness. However, all three datasets are public, English/Western, and photograph-based, limiting claims of broad generalizability to diverse clinical populations or imaging systems.

**Is external validation robust?**
Moderate. Both Messidor sets are well-established benchmarks. However, neither dataset was prospectively collected for this study; both are small (1,200 and 1,748 images). No confidence intervals are reported, undermining precision of performance estimates.

**Are confidence intervals reported?**
No. This is a significant methodological gap for a clinical application paper.

**Is dataset size adequate?**
Training size (56,839 images) is reasonable. External test sets are small (1,200 and 1,748), limiting statistical power of benchmark comparisons.

**Is class imbalance addressed?**
Yes — class-weighted loss function applied; sensitivity/specificity/AUC selected over accuracy as primary metrics; over/under-sampling tested and found ineffective.

**Is statistical testing adequate?**
No. No significance tests, no confidence intervals, no bootstrapping reported. All comparisons with other studies are descriptive percentage differences only.

---

# 11. Internal Validity

**Overfitting risk:** Authors use early stopping, dropout, batch normalization, and class weighting. Multiple random-split training runs and ensemble averaging reduce individual model variance. However, the absence of k-fold cross-validation means validation performance estimates may be less stable. The brute-force ensemble search on test sets introduces selection bias risk.

**Dataset leakage risk:** EyePACS test set was held out prior to training. However, the brute-force search for optimal ensemble weights was performed by evaluating on test sets directly (p. 6: "we identified a few best-performing weights from multiple models...The best combination...was obtained with the help of a brute force search"), which constitutes implicit test set optimization — a methodological concern.

**Confounders:** EyePACS dataset contains non-gradable images; authors filtered using external gradability ratings [26] and their own disk-detection algorithm. The filtering criteria are not fully specified. Messidor-1 mixing of mydriatic and non-mydriatic images is acknowledged but not controlled for.

**Augmentation inflation risk:** Augmentation applied online during training only; not applied during testing. This is methodologically sound.

**Metric reliability:** AUC is appropriate for imbalanced datasets. Sensitivity and specificity reported at a single operating point (shortest distance), limiting clinical comparability across studies that use different operating point strategies.

**Formula correctness:** Brightness and contrast augmentation formulas are explicitly stated and appear correct.

---

# 12. External Validity

**Cross-population transferability:** Limited. All datasets are public benchmark sets collected in clinical environments in the US (EyePACS) and France (Messidor). No Indian patient population data was used despite the study's stated motivation addressing Indian DR burden. No demographic or population metadata reported.

**Dataset portability:** Demonstrated across two external benchmark sets. AUC consistency is suggestive but not definitive without confidence intervals.

**Clinical feasibility:** Partially demonstrated. Runtime tests on commodity hardware confirm technical feasibility (0.5–2.0 s). However, the system has not been deployed in actual clinical settings; authors acknowledge this limitation explicitly.

**Hardware constraints:** Reported — system tested on laptop (Intel i5-7200U, 8 GB RAM: 1.8–1.9 s), desktop PC (Intel i5-4590, 4 GB RAM: 1.0–1.3 s), and server (2× Intel Xeon Gold 6142, 384 GB RAM: 0.5–1.0 s). Training performed on HPC cluster Kshitij-5.

---

# 13. Strengths

- Explicit separation of adjudicated vs. non-adjudicated comparison tables allows fair benchmarking within the same data-quality tier
- Systematic ablation of input resolution (256, 299, 512, 598 pixels) with quantitative AUC consequences reported
- Ensemble design using multiple random-split training runs reduces individual model variance
- Class-weighted loss function to address class imbalance is methodologically appropriate
- Cross-dataset evaluation on two established external benchmark sets (Messidor-1 and Messidor-2)
- Runtime profiling on commodity hardware provides concrete clinical feasibility data
- Augmentation limited to training phase only — no test-time leakage
- AUC differences between EyePACS and Messidor test sets are small and explicitly quantified as a generalization indicator

---

# 14. Limitations

**Explicit (stated by authors):**
- Non-adjudicated labels reduce label quality; authors expect adjudication would improve performance
- Public datasets contain noisy/non-gradable images (artifacts, over/underexposure, out-of-focus)
- Application not yet deployed in real clinical conditions
- General-purpose architectures (InceptionResNetV2) may be suboptimal for fixed-feature-size medical images; custom models recommended for future work

**Implicit (methodological):**
- No confidence intervals on any reported metric — precludes statistical comparison with other studies
- Brute-force ensemble selection performed against test sets — constitutes implicit test set optimization, inflating reported ensemble performance
- Random-split validation instead of k-fold yields less stable hyperparameter estimates
- No statistical significance testing for inter-study comparisons (all comparisons are descriptive)
- EyePACS test set is not truly external — same source, same distribution as training data
- Sensitivity/specificity reported at a single operating point (shortest distance), complicating comparability with studies using clinically motivated thresholds (e.g., high-sensitivity point)
- Dataset population not described (age, diabetes duration, ethnicity, camera type) — limits generalizability assessment
- Indian patient population not represented despite stated motivation
- Messidor-1 binary mapping from 4-class grading system not fully described; handling of macular edema labels not reported

---

# 15. Relevance to My Dissertation

**Position in paradigm space (v5.3):** P1 (end-to-end CNN; preprocessing as auxiliary step). Grounds (per SIR-9): although the paper reports preprocessing choices (intelligent cropping, resolution selection, targeted augmentation) and acknowledges their impact, preprocessing is treated as a tuning factor for the architecture rather than as a formalised model component, and the conceptual emphasis remains on backbone selection (InceptionResNetV2 vs. InceptionV3) and ensemble methods. The authors' five-factor framing of performance gains (model structure, image size, dataset splitting, preprocessing/augmentation, ensembles) is precisely the P1 framing of preprocessing as one factor among several rather than as an integral part of the model. Per CFC-2.9 / SIR-1, no theoretical "preprocessing is unimportant" claim is attributed to the authors.

**Relevance to preprocessing dominance hypothesis:**
High. The study provides direct empirical evidence that preprocessing choices — specifically intelligent cropping, resolution selection (512×512 vs. 299×299), and targeted augmentation — materially affect AUC on external benchmarks. The resolution ablation (Messidor-2 AUC: 0.92 at 512×512 vs. 0.86 at 299×299) is a concrete, citable quantification of preprocessing impact. This directly supports a preprocessing-dominance argument.

**Relevance to cross-database validation:**
High. EyePACS → Messidor-1 and Messidor-2 cross-dataset testing with small AUC deltas (~0.03, ~0.007) is a direct empirical case study in cross-database robustness. The authors' interpretation that consistent AUC indicates generalization beyond dataset-specific features is a relevant argument to engage with or contest.

**Relevance to EyePACS/Messidor benchmarking:**
High. The study uses the canonical benchmark setup (EyePACS training, Messidor-1/2 external testing) and provides a direct performance table comparing adjudicated vs. non-adjudicated approaches — a useful structural reference for dissertation benchmarking chapters.

**Relevance to Vision Transformer comparison:**
Low. No Vision Transformer architectures are used or referenced. The study is pre-Transformer-era in methodology.

**Risk of contradiction:**
Moderate. If your dissertation argues preprocessing dominates over architecture, this study partially supports that view but also attributes performance gains to the InceptionResNetV2 architecture (vs. InceptionV3) — complicating a pure preprocessing-dominance narrative. The authors explicitly cite five factors for improvement: model structure, image size, dataset splitting, preprocessing/augmentation, and ensemble methods — assigning no single dominant factor.

---

# 16. Citation-Ready Statements

1. "The model has achieved an AUC of 0.92 on benchmark test dataset Messidor-2 with sensitivity and specificity of 81.02% and 86.09%, respectively. AUC, Sensitivity and Specificity on Messidor-1 are 0.958, 88.84% and 89.92%, respectively" (Saxena et al., 2020, p. 1 / Abstract).

2. "Using the image size of 299 × 299 pixels, our models have scored an AUC of 0.91 and 0.86 on Messidor-1 and Messidor-2 dataset, respectively. These AUC values are low in comparison with their 512 × 512 counterpart" (Saxena et al., 2020, p. 9).

3. "The said differences between the AUC values of the EyePACS test set with Messidor-1 and Messidor-2 are quite small; ~0.03 and ~0.007, respectively. Producing similar AUC values across different datasets indicates that our models are prone to [resistant to] over-fitting" (Saxena et al., 2020, p. 9).

4. "We consider random splitting of the EyePACS dataset, minimalistic set of image pre-processing and data augmentation methods, and methods for the ensemble as the significant reasons" [for generalization performance] (Saxena et al., 2020, p. 10).

5. "We found that pre-processing methods like intelligent cropping (remove black border and centering), random brightness change (~12–13%) and random contrast change (~20%) give better results. Also, the optimal image size is nearly 512 × 512 pixels" (Saxena et al., 2020, p. 10).

6. "The labels used in our training and validation set are not adjudicated by any human experts" — distinguishing this study from higher-performing adjudicated-dataset studies (Saxena et al., 2020, p. 2 / Related Works).

7. "Our AUC value for Messidor-2 is ~2.1% less than the nearest AUC value [Gargeya et al.] and only ~7.0% less than the highest AUC value [Gulshan et al.]" despite using non-adjudicated data (Saxena et al., 2020, p. 6–7).

---

# 17. Epistemic Classification

**Classification: Benchmark study / Methodological precedent**

**Justification:** The study does not introduce a novel architecture or theoretical framework. Its epistemic contribution is a systematic empirical demonstration that non-adjudicated public datasets, combined with careful preprocessing (resolution, cropping, targeted augmentation) and ensemble methods, can approach the performance of adjudicated-dataset studies on established external benchmarks. It provides a structured comparison table separating adjudicated from non-adjudicated prior work — a methodologically useful reference scaffold. It is not foundational (no novel algorithmic contribution) and not a clinical validation precedent (no prospective deployment). Its primary value is as a reproducible benchmark point within the EyePACS/Messidor ecosystem.

---

# 18. Analytical Synthesis

This study carries moderate epistemic weight as a benchmark reference within the CNN-based DR screening literature, primarily because it provides one of the few explicit comparisons of adjudicated vs. non-adjudicated training performance within a consistent experimental framework. Its cross-dataset AUC consistency (EyePACS: 0.927, Messidor-1: 0.958, Messidor-2: 0.920) provides usable empirical support for the claim that models trained on EyePACS can generalize to Messidor-class distributions, though the absence of confidence intervals limits the inferential force of this claim. For dissertation positioning, the study's resolution ablation data (AUC loss of ~0.04–0.06 when reducing from 512×512 to 299×299) constitutes the most directly citable evidence for a preprocessing-dominance argument, as it isolates a single preprocessing variable with measurable outcome consequence. However, the authors attribute performance improvement to five concurrent factors rather than isolating preprocessing, which constrains the strength of inference available from this paper alone. The study does not engage with Vision Transformers, limiting its relevance to architecture comparison chapters. The implicit test set optimization via brute-force ensemble search is a methodological vulnerability that should be noted when citing its benchmark figures. Overall, this paper strengthens the cross-dataset robustness narrative and provides useful resolution-preprocessing evidence, but requires corroboration from studies with more rigorous statistical reporting to support strong dissertation claims.

---