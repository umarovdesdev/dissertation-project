# DISSERTATION INVARIANTS DOCUMENT
## Immutable Epistemic Structure for Doctoral Research
**Research Domain:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification  
**Candidate:** Yesmukhamedov N.S.  
**Document Status:** Binding constraint system — supersedes informal claim formulations across all dissertation chapters.  
**Version:** 6.3.0 | **Date:** 2026-07-09

**v6.3.0 Amendment Summary (vs v6.2.0):** Adds **supervised in-domain pretraining (SIP)** as an allowed integrated-arm initialization, selected against continual-SSL and ImageNet by the existing linear-probe acceptance gate. **Motivation:** from-scratch label-free CNN-SSL within the INV-SSL-6 family (BYOL / MoCo-v2 / DINO) **failed** the acceptance gate on the EyePACS-test corpus (best quadratic-κ ≈0.11 vs ImageNet ≈0.30; flat/declining ep50→ep100 — a robust negative result, `experiments/outputs/ssl/COMPARISON.txt`). SIP supervises the same CNN backbone on the 53,576-image EyePACS-test corpus **using its DR grades**, starting from ImageNet and adapting, then transfers to Experiment 1. This **relaxes SB-2.4's** label-use restriction to permit supervised use of the EyePACS-test grades for a distinct in-domain **pretraining** stage (the corpus stays disjoint from the Experiment-1 35,126 CV set by image + patient identity, INV-SSL-1/2, and is still **not folded** into Experiment-1 supervised training), and **extends CFC-2.8** to list SIP alongside fundus-SSL and the ImageNet→continual-SSL fallback as gate-selected integrated-arm inits. The label-free SSL objective is unchanged; SIP is a separate objective. **Adds an allowed initialization + relaxes one operational restriction; reverses no hypothesis, scope boundary, or forbidden-claim → MINOR bump** per VERSIONING_POLICY §4. CFC-2.8's core confound caveat is retained and applies identically to SIP (the integrated arm still differs from baseline along both the preprocessing and the initialization axis). Downstream governance sync (HYPOTHESIS Premise-4 wording, RESEARCH_ARCHITECTURE §4.2bis/§9.1, glossary) remains a pending pass; SIP build spec `experiments/docs/supervised_indomain_pretraining_brief.md`, amendment proposal `experiments/outputs/sip/v1.0/GOVERNANCE_AMENDMENT_PROPOSAL.md`.

**v6.2.0 Amendment Summary (vs v6.1.0):** Operationalizes the now-locked fundus self-supervised pretraining corpus and acceptance protocol for the integrated arm. **No binding is reversed** — the v6.0.0 ophthalmology-SSL decision (RETFound dropped; CNN-native in-domain initialization) is unchanged; this amendment only fixes operational specifics that were previously left open. Three refinements: (i) the integrated-arm SSL corpus is fixed to the **unlabeled EyePACS original "test" split (53,576 images)**, which is **disjoint** from the Experiment-1 evaluation corpus (the ~35,126 labeled images in the EyePACS "train" split, 5-fold patient-level CV) by image identity *and* patient identity — a no-pretraining-leakage constraint recorded as new clause **SB-2.4** and operationalized in the experiments code as the disjointness assertions INV-SSL-1/INV-SSL-2 (`experiments/docs/fundus_ssl_pretraining_brief.md`); (ii) **BYOL** (Grill et al., 2020) is recorded as the primary CNN-compatible SSL protocol (MoCo-v2 / SimSiam / DINO retained as alternatives), pretrained **from-scratch** (random initialization) on the 4-channel tensor, the final choice confirmed by a **linear-probe acceptance gate** requiring the SSL initialization to beat random init and be competitive with ImageNet before it may enter Experiment 1; (iii) DGL-6 is extended with these operational specifics. This **adds new referenceable entities** (SB-2.4 and the linear-probe acceptance gate) and reverses no binding constraint, hypothesis, or scope boundary → **MINOR** bump per VERSIONING_POLICY §4. CFC-2.8 (baseline ⟹ ImageNet, integrated ⟹ fundus-SSL) and the composite independent variable are retained; no SSL performance is asserted (the integrated arm is specified, not yet trained).

**v6.1.0 Amendment Summary (vs v6.0.0):** Refines the **OD-3 Stage 1** operational definition. The classical computer-vision OD/fovea detector (brightest-region OD, darkest-region-with-distance-prior fovea) is replaced by a **pre-trained, frozen heatmap-regression detector** (U-Net encoder + DSNT head) trained on IDRiD localization ground-truth; it predicts OD/fovea probability heatmaps on the FOV-cropped frame, yielding sub-pixel centers and a **genuine** per-landmark confidence (heatmap peak sharpness + spatial spread) that gates the rotation fallback and the Stage-5 polar-CLAHE pivot. Motivation: the classical detector localized the fovea unreliably (~5 OD-radii median error, ~0 % within 2 R at native resolution) and its confidence flag was non-informative; the learned detector meets the acceptance bar on the held-out IDRiD test split (OD median 0.066 R / 100 % within 1 R; fovea median 0.107 R / 99 % within 1 R; informative confidence). The **fallback rotation σ is reconciled to 15.0°** (the value the code and evaluation use; the prior text's 13.0° is corrected). The detector is **pre-trained and frozen — not co-trained with the DR classifier** — so preprocessing remains a fixed transform and the central thesis `model = preprocessing + CNN` is preserved. This **adds a new substantive entity** (the learned Stage-1 detector) and reverses no binding constraint, hypothesis, or scope boundary → **MINOR** bump per VERSIONING_POLICY §4. No other operational definition (Stages 0, 2–7), hypothesis, or scope boundary is modified.

**v6.0.0 Amendment Summary (vs v5.3):** Reverses the v5.1–v5.2 **RETFound** adoption. The integrated arm of Experiment 1 is no longer initialized from the RETFound ViT-Large foundation model; instead the existing CNN backbones (ResNet-50 / EfficientNet-B3) are initialized from **ophthalmology-specific self-supervised pretraining** on an unlabeled retinal fundus corpus (a CNN-compatible domain-adaptive SSL protocol — DINO / BYOL / SimCLR / MoCo family — selected empirically). Rationale: adopting RETFound changes both the architecture and the initialization, confounding the preprocessing contribution with an architecture change; a CNN-native SSL initialization changes only the initialization stage, preserving the CNN-centred design and a defensible causal interpretation. This resolves **AOQ-1** (→ option b), **AOQ-4** (the 2×2 *(preprocessing × architecture)* factorial symmetry is restored — both backbones run in both arms, configs A/B/C/D), and **AOQ-3** (RETFound license moot), and simplifies **AOQ-2** (SSL may be pretrained directly on 4-channel tensors). The composite independent variable and **CFC-2.8 are retained** — the integrated arm still differs from baseline along both the preprocessing and the pretraining axis (ImageNet → ophthalmology-SSL), so the H-1 effect remains non-attributable to preprocessing alone. Because this reverses a binding constraint, it is a **MAJOR** bump per VERSIONING_POLICY §4. The earlier amendment summaries below (v5.3, v5.2, v5.1) are retained as historical record; where they describe RETFound as the current integrated-arm source, they are superseded by this summary.

**v5.3 Amendment Summary (vs v5.2):** Introduces a uniform **paradigmatic framing** for the dissertation. Two paradigms are recognised: **P1 — the end-to-end CNN paradigm** ("preprocessing is ancillary data preparation, not requiring methodological discussion"), and **P2 — the integrated preprocessing-CNN paradigm** ("preprocessing is an integral model component"). Gulshan et al. (2016) is designated the **canonical representative of P1**; the dissertation's integrated configuration is the **paradigmatic instantiation of P2**. Three new clauses are added: **SB-1.12** (scope boundary — Gulshan functions as canonical representative of P1, not as an experimental control; no numerical comparison is performed), **CFC-2.9** (prohibits phrasings that attribute to Gulshan an explicit "preprocessing is unimportant" claim; only descriptions of methodological practice are permitted), and **SIR-9** (paradigmatic-attribution rule — a source may be designated "canonical representative of paradigm X" only if its methodological practice matches X and the citation targets that practice, not an absent theoretical statement). No operational definitions, hypotheses, or experimental protocols are modified by v5.3; the baseline configuration of Experiment 1 (configs A/C, OD-3) is unchanged. All v5.2 provisions (multi-modal pretraining-corpus refinement, CFP-checkpoint binding, CFC-2.8, AOQ-1 through AOQ-4) are retained.

**v5.2 Amendment Summary (vs v5.1):** Pretraining-corpus specification for the integrated arm is refined from "~1.6M color fundus photographs" (CFP-only) to the multi-modal retinal imaging corpus on which the RETFound foundation model was pretrained per Zhou et al. 2023, Nature — approximately 1.6M retinal images comprising ≈904K color fundus photographs (CFP) and ≈736K optical coherence tomography (OCT) scans. **Loaded-checkpoint binding:** for the dissertation's downstream fundus classification task, the integrated arm initializes from the CFP-pretrained RETFound checkpoint specifically; the multi-modal description characterizes the foundation model's full pretraining corpus at the publication level and does **not** imply OCT inputs to the dissertation's pipeline (SB-1.4 remains in force — the dissertation does not claim generalization to OCT). All other v5.1 provisions (composite independent variable, CFC-2.8, AOQ-1 through AOQ-4) are retained unchanged.

**v5.1 Amendment Summary (vs v5.0):** Pretraining source is no longer fixed at ImageNet for both arms of the Experiment 1 factorial design. The integrated (full pipeline) arm is amended to use **RETFound** (Zhou et al., 2023; retinal foundation model, MAE-pretrained on a multi-modal corpus of ~1.6M retinal images — ≈904K CFP + ≈736K OCT; CFP-checkpoint loaded per v5.2) as the source of initialization weights. The baseline arm retains ImageNet pretraining. This amendment is recorded under VCR-1 (which requires a new versioned Invariants for hypothesis modification) and is reflected in H-1 below. Two open technical questions remain (see Section X — Amendment Open Questions) and bind future operational specifications.

---

## I. CENTRAL THESIS (Immutable Formulation)

**IT-1.** An integrated preprocessing-CNN pipeline — comprising the 8-stage preprocessing system: canonical flip (Stage 0), OD-fovea rotation normalization (Stage 1), FOV crop + isotropic resize to 512×512 with centered zero-padding (Stage 2), FOV mask generation as 4th input channel (Stage 3), adaptive flat-field correction with σ = 0.07 × FOV diameter applied inside mask only (Stage 4), dual-constraint stochastic CLAHE on LAB L-channel (Stage 5), integrated augmentation at train time (Stage 6), and dataset-specific channel-wise normalization (Stage 7) — applied to fundus images sourced from EyePACS (primary training, ~35,126 images), APTOS 2019 (cross-dataset transferability, Experiment 3), IDRiD (explainability and clinical validation), Messidor-2 (clinical degradation evaluation), DDR/ODIR-5K/RFMiD (device domain shift), and a Kazakh clinical dataset (clinical validation), produces statistically measurable improvement in five-class diabetic retinopathy classification performance relative to a baseline CNN trained on images processed with stretch-resize to 512×512 + ImageNet normalize only (3 channels, no FOV mask), under constrained computational conditions defined by hardware limitations operative during experimental execution.

**Scope boundary embedded in IT-1:**
- The thesis is bounded to five-stage DR classification (DR 0–4 per standard clinical grading).
- The thesis does not extend to general retinal disease classification, to other ophthalmological imaging modalities, or to imaging contexts not representable by the dataset architecture specified above (EyePACS, APTOS 2019, IDRiD, Messidor-2, Clinical, RFMiD, DDR, ODIR-5K).
- "Improvement" is defined exclusively as measurable difference in primary metrics (see Section V) computed across matched experimental conditions.
- The dataset architecture enables evaluation of cross-database transferability (APTOS 2019), explainability via Grad-CAM with lesion mask comparison (IDRiD) and qualitative overlays (Clinical), clinical degradation resistance (IDRiD, Messidor-2), and device domain shift across camera hardware (RFMiD, DDR, ODIR-5K).
---

## II. CORE HYPOTHESES (Operational Form)

### Central Unifying Hypothesis

The proposed preprocessing pipeline reduces domain variability across fundus imaging devices and acquisition conditions while preserving diagnostically relevant retinal features, leading to improved CNN-based diabetic retinopathy detection. Hypotheses H-1, H-2, H-4, H-5, H-6, and H-7 are decompositions of this central hypothesis, each testing a specific aspect of the overarching claim.

---

**H-1 (Primary — Integrated Pipeline Dominance) [v5.1 amended]:**

*If* fundus images from EyePACS are processed through the 8-stage preprocessing pipeline comprising canonical flip (Stage 0), OD-fovea rotation normalization (Stage 1), FOV crop + isotropic resize to 512×512 with centered zero-padding (Stage 2), FOV mask generation as 4th input channel (Stage 3), adaptive flat-field correction with σ = 0.07 × FOV diameter (Stage 4), dual-constraint CLAHE on LAB L-channel with stochastic application at train time (Stage 5), integrated augmentation at train time (Stage 6), and dataset-specific channel-wise normalization (Stage 7), and a CNN classifier (ResNet-50 or EfficientNet-B3) initialized with **ophthalmology-specific self-supervised pretrained weights** (a CNN-compatible domain-adaptive self-supervised learning protocol — drawn from the DINO / BYOL / SimCLR / MoCo family, the specific protocol selected empirically — pretrained on an unlabeled retinal fundus corpus without diabetic-retinopathy labels) is fine-tuned on the processed images,
*then* classification accuracy, F1-score, ROC-AUC, and Cohen's Kappa will exceed those of the same downstream task trained on baseline images (stretch-resize to 512×512 + ImageNet normalize, 3 channels, no FOV mask) with a CNN classifier initialized with **ImageNet pretrained weights** (ResNet-50 / EfficientNet-B3), of equivalent source distribution.

- **Independent variable (composite, v5.1 amended; pretraining source revised in v6.0.0):** The combined factor *(preprocessing × pretraining source)*. The baseline arm and the integrated arm differ jointly along the preprocessing axis (stretch-resize + ImageNet normalize vs. full pipeline) **and** along the pretraining axis (ImageNet vs. ophthalmology-specific self-supervised pretraining). Single-factor isolation along preprocessing alone — the form of H-1 in v5.0 — is no longer obtained and is explicitly relinquished by this amendment.
- **Dependent variables:** Accuracy, F1-score (macro and weighted), ROC-AUC, Cohen's Kappa (quadratic weights), precision, recall — computed on the held-out test partition.
- **Control conditions:** Same dataset, same data partition strategy (5-fold cross-validation with patient-level stratified split), same computational hardware, same training epoch budget.
- **Factorial design (v6.0.0):** Because the ophthalmology-specific SSL initialization is CNN-native (unlike RETFound's ViT-Large), the 2×2 *(preprocessing × architecture)* factorial is restored: **both** ResNet-50 and EfficientNet-B3 appear in **both** the baseline and the integrated arm. The pretraining source is slaved to the preprocessing arm (baseline ⟹ ImageNet, integrated ⟹ ophthalmology-specific SSL). Configurations A/B/C/D are defined in RESEARCH_ARCHITECTURE.md. AOQ-1 and AOQ-4 are resolved by this amendment (Section X).
- **Validation criterion:** Integrated Pipeline Dominance is validated if Performance(integrated + SSL) > Performance(baseline + ImageNet) with EH-3 criteria satisfied. The attribution of the observed effect to preprocessing alone, pretraining alone, or their interaction is **not claimable** (see CFC-2.8) and must be deferred to a future ablation study not within the scope of this dissertation.

---

**H-2 (Secondary — CLAHE Threshold Sensitivity and Component Ablation):**

*If* the dual-constraint clip limit parameters (clip_factor and global_threshold) of the upgraded CLAHE are varied across controlled values on EyePACS, where clip_limit = min(clip_factor × tile_area / 256, global_threshold × tile_area) and CLAHE is applied stochastically at train time (80% probability),
*then* classification performance of the downstream CNN will exhibit a parameter-dependent sensitivity profile, identifiable as a non-trivial sensitivity curve with at least one local optimum within the tested range. Additionally, the flat-field correction parameter σ (expressed as a fraction of FOV diameter D) is varied across 0.05·D to 0.10·D to characterize the illumination correction sensitivity profile.

- **Independent variable:** CLAHE dual-constraint clip limit parameters (clip_factor and global_threshold); flat-field σ factor (fraction of FOV diameter D).
- **Dependent variables:** Per-class F1-score for DR stages with smallest lesion features (microaneurysms, small vessels — predominantly DR 1 and DR 2 classes).
- **Scope:** Bounded to the parameter range tested experimentally. No extrapolation to untested parameter values is permissible.

---

---

**H-4 (Secondary — Cross-Dataset Transferability):**

*If* a CNN model trained on EyePACS with the full preprocessing pipeline is evaluated on APTOS 2019 without retraining,
*then* the generalization ratio G = F1_APTOS / F1_EyePACS will be ≥ 0.85.

- **Independent variable:** Dataset (EyePACS training vs. APTOS 2019 external evaluation).
- **Dependent variables:** Accuracy, Weighted F1-score, ROC-AUC, generalization ratio G (per OD-4).
- **Scope:** No retraining is performed on external datasets. Results are bounded to the specific architectures and preprocessing configurations tested. The G ≥ 0.85 threshold is a pre-registered success criterion, not a guaranteed outcome.

---

**H-5 (Secondary — Explainability):**

*If* Grad-CAM activation maps are computed for a CNN (EfficientNet-B4) processing fundus images with the preprocessing pipeline vs. stretch-resize + ImageNet normalize baseline (3 channels),
*then* the Attention–Lesion Overlap (ALO) between Grad-CAM activation regions and pixel-level lesion masks from the IDRiD dataset will satisfy ALO_preproc > ALO_baseline, demonstrating that preprocessing directs model attention toward clinically relevant structures. ALO is defined as ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask) and serves as the primary explainability metric. IoU is retained as a secondary metric: IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask), with IoU_preproc > IoU_baseline as the secondary condition. Qualitative Grad-CAM overlays are additionally produced on the Kazakh clinical dataset.

- **Independent variable:** Presence vs. absence of the preprocessing pipeline.
- **Dependent variables:** ALO between Grad-CAM activations and IDRiD lesion masks, per lesion type (primary); IoU between Grad-CAM activations and IDRiD lesion masks, per lesion type (secondary); qualitative Grad-CAM overlays on Clinical dataset.
- **Scope:** Bounded to IDRiD images with available pixel-level lesion annotations (quantitative); Clinical dataset for qualitative overlays only. Grad-CAM activation does not constitute clinical localization of pathology (see NC-14). Results are bounded to EfficientNet-B4 architecture.

---

**H-6 (Secondary — Device Robustness):**

*If* a CNN model trained on EyePACS with the full preprocessing pipeline is evaluated on fundus images from datasets captured by different camera hardware (RFMiD: Topcon/Kowa; DDR: Canon/Topcon; ODIR-5K: Canon/Zeiss),
*then* classification performance will be maintained across camera domains, with cross-device performance variance remaining within acceptable bounds relative to in-domain performance. Preprocessing standardizes retinal image appearance and reduces distribution differences between camera devices, leading to improved cross-device generalization. DR labels only; non-DR disease labels are ignored or mapped to non-DR.

- **Independent variable:** Camera/device domain (grouped by camera model across DDR, ODIR-5K, and RFMiD).
- **Dependent variables:** Accuracy, F1-score, ROC-AUC per camera group.
- **Scope:** Results are bounded to the specific camera models represented in the tested datasets. Device domain shift results do not constitute device certification or regulatory compliance (see NC-16).

---

**H-7 (Secondary — Clinical Degradation Resistance):**

*If* a CNN model trained on EyePACS is evaluated on external clinical datasets (IDRiD, Messidor-2) with and without the preprocessing pipeline,
*then* the performance degradation Δ = F1_EyePACS_val − F1_external will be statistically smaller for the integrated-preprocessed model than for the baseline model, demonstrating that preprocessing reduces cross-dataset performance loss.

- **Independent variable:** Presence vs. absence of the preprocessing pipeline.
- **Dependent variable:** Degradation metric Δ = F1_EyePACS_val − F1_external, computed separately for IDRiD and Messidor-2.
- **Scope:** Bounded to the tested datasets (IDRiD, Messidor-2) and architectures (ResNet-50, EfficientNet-B3). Smaller Δ indicates more robust cross-dataset transfer.

---

## III. OPERATIONAL DEFINITIONS

**OD-1: Image Quality**  
Image quality is operationally defined as the measurable capacity of a fundus image to support automated detection of microvascular features relevant to DR staging. Image quality is assessed through downstream classification performance metrics (accuracy, F1-score, ROC-AUC) computed on the same classifier architecture under identical training conditions with varying preprocessing states (absent vs. applied). No standalone subjective image quality score is used as the primary quality measure. An image quality condition is considered degraded if baseline CNN accuracy on unprocessed images falls below the enhanced CNN accuracy by a statistically interpretable margin under matched conditions.

**OD-2: Architectural Complexity**  
Architectural complexity is operationally defined by the number of convolutional layers, total trainable parameter count, filter size range, and presence or absence of regularization components (batch normalization, dropout). The baseline architecture (two convolutional blocks, 32–64 filters, no batch normalization, no dropout, sigmoid output) constitutes the low-complexity reference. The enhanced architecture (four convolutional blocks, 32–256 filters, batch normalization, dropout rate 0.4, softmax 5-class output) constitutes the high-complexity reference. Architectures outside these bounds are not evaluated within this dissertation.

**OD-3: Preprocessing Pipeline (Canonical)**
The preprocessing pipeline is the ordered sequence of 8 stages applied to fundus images prior to CNN input:

- **Stage 0: Canonical Flip** — Left-eye images are horizontally flipped to right-eye canonical orientation (OD right, macula left). Always on.
- **Stage 1: OD-Fovea Rotation Normalization** — A **pre-trained, frozen** heatmap-regression detector (U-Net encoder + DSNT head, trained on IDRiD localization ground-truth) predicts probability heatmaps for the optic-disc and fovea centers on the FOV-cropped frame; the image is rotated so the OD→fovea axis is horizontal. Per-landmark confidence is derived from heatmap peak sharpness and spatial spread. Fallback: skip rotation when confidence is below threshold (and pivot Stage-5 polar CLAHE on the FOV-mask centroid rather than the detected fovea). Augmentation rotation σ is adaptive per-image from heatmap-derived localization uncertainty (fallback σ = 15.0°). The detector is pre-trained and **frozen — not co-trained with the DR classifier** — so the preprocessing pipeline remains a fixed transform and the central thesis "model = preprocessing + CNN" is preserved. Always on. (Operationally, detection runs on the FOV-cropped frame produced by Stage 2's crop/resize; stage numbering is retained.)
- **Stage 2: FOV Crop + Isotropic Resize** — Foreground detection, crop to FOV region, isotropic scale to 512×512 with centered zero-padding preserving fundus circle geometry. Always on.
- **Stage 3: FOV Mask Generation** — Binary mask (1.0 = real fundus data, 0.0 = zero-padding) appended as 4th input channel. Always on.
- **Stage 4: Flat-Field Correction** — Gaussian blur subtraction (corrected = image − GaussianBlur(image, σ) + 128) with adaptive σ = 0.07 × D (D = FOV diameter in pixels from mask). Applied inside FOV mask only. Always on.
- **Stage 5: CLAHE** — Dual-constraint clip limit on LAB L-channel: CL = min(clip_factor × tile_area / 256, global_threshold × tile_area). Tile grid 8×8. Stochastic at train time (p = 0.8); deterministic at inference. Always on.
- **Stage 6: Augmentation** — Train only. Applied on-the-fly in order: (1) unified affine transform (rotation σ adaptive from Stage 1, zoom [0.9, 1.1], optional shear/stretch); (2) ColorJitter — brightness, contrast, and saturation (each factor ∈ [0.9, 1.1]) and hue (shift ∈ [−0.02, 0.02]), each component applied independently with p = 0.5; (3) Gaussian noise (σ ∈ [2, 6] on the 8-bit RGB scale, p = 0.15); (4) JPEG compression (quality ∈ [70, 100], p = 0.20). Applied before Stage 7 (operates on uint8). Train only.
- **Stage 7: Dataset-Specific Normalization** — ToTensor (HWC uint8 → CHW float32 [0,1]) then channel-wise (x − mean) / std using mean and std computed from EyePACS training set after Stages 0–4, using only pixels where FOV mask = 1.0. Output: float32 tensor of shape (4, 512, 512). Always on. Always last.

Pipeline **ACTIVE** (full pipeline): All 8 stages applied. Stage 6 active during training only. Output: 4-channel tensor (3 RGB + 1 FOV mask). Pipeline **ABSENT** (baseline): Stretch-resize to 512×512 + ImageNet normalize (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]). Output: 3-channel tensor. No FOV mask. No preprocessing stages.

**Ablation exception:** Ablation configurations in Experiment 2 are experimental variants for analysis purposes only; they do not constitute valid production pipeline instances. The 8-stage pipeline remains mandatory for all operational deployment.

**OD-4: Generalization**  
Generalization is operationally defined as the difference between training-set performance and held-out test-set performance on the same evaluation metric. Overfitting is the condition wherein training precision exceeds test precision by more than 15 percentage points on any primary metric. Cross-database generalization is defined as the ratio of test-set F1-score on a secondary dataset (e.g., Messidor-2, IDRiD) to test-set F1-score on the primary dataset (EyePACS) under the same trained model, without retraining: G = F1_external / F1_EyePACS.

**OD-5: Diagnostic Effectiveness**  
Diagnostic effectiveness is operationally defined as the joint performance profile on four primary metrics — Accuracy, weighted F1-score, ROC-AUC, and Cohen's Kappa (quadratic weights) — computed on the held-out test partition. A preprocessing-CNN configuration is considered diagnostically effective when: Accuracy ≥ 0.80, weighted F1-score ≥ 0.80, ROC-AUC ≥ 0.90, and Cohen's Kappa ≥ 0.70, on the held-out EyePACS test partition. These threshold values are derived from the published empirical results in LC-SAPAKOVA-2025-01 (weighted F1 = 0.91, ROC-AUC = 0.9638) and LC-Yesmukhamedov-2025-SELF (Weighted Average = 0.81, Accuracy = 0.80).

**OD-6: Resource-Limited Environment**  
A resource-limited environment is defined as a deployment context characterized by at least two of the following conditions: (a) the absence of GPU acceleration for inference; (b) available RAM below 16 GB; (c) batch processing time constraints requiring inference completion within real-time or near-real-time clinical workflow; (d) network connectivity limitations precluding continuous cloud API reliance. The hardware conditions under which experiments were conducted operationalize this definition. Deployment in Kazakhstan's rural healthcare context (approximately 40% rural population, approximately 1,200 ophthalmologists nationally, per LC-2025-Yesmukhamedov-01, p. 77) provides the clinical framing but does not independently validate the computational definition.

---

## IV. SCOPE BOUNDARIES

**SB-1: What Is NOT Claimed**

- SB-1.1 The dissertation does not claim that the preprocessing pipeline achieves performance improvements on retinal imaging datasets other than those specified in the dataset architecture (EyePACS, APTOS 2019, IDRiD, Messidor-2, Clinical, RFMiD, DDR, ODIR-5K), unless additional cross-database generalization experiments are explicitly conducted and reported.
- SB-1.2 The dissertation does not claim that 100% classification accuracy, sensitivity, or specificity is achievable on any dataset in the dataset architecture. Values reported for the STARE-based CLAHE study (LC-AlTimemy-2021) achieving 100% accuracy on 157/152 images are not transferable to the dissertation's experimental context.
- SB-1.3 The dissertation does not claim that the proposed system is a standalone diagnostic device or replaces ophthalmologist assessment. The system is a decision-support tool within a physician-in-the-loop paradigm.
- SB-1.4 The dissertation does not claim generalization of results to imaging modalities other than fundus photography (e.g., OCT, fluorescein angiography).
- SB-1.5 The dissertation does not claim that the laser-tissue interaction mathematical model (Chapter 2, Section 2.4) constitutes an experimentally validated clinical model. The model in LC-Sapakova-2024-01 provides qualitative simulation results without quantitative validation against experimental or clinical data.
- SB-1.6 The dissertation does not claim that projected deployment outcomes for Kazakhstan (20–30% reduction in late-stage DR complications; 15–20% cost reduction, per LC-2025-Yesmukhamedov-01, p. 88) are demonstrated results of this research. These are externally projected figures cited for contextual framing only.
- SB-1.7 The dissertation does not claim that any single architecture (ResNet-50, EfficientNet-B3, EfficientNet-B4, or EfficientNetB0) represents the globally optimal architecture for DR classification. The dissertation evaluates specific architectures within the experimental design; no comparative claim across the full architecture space is permissible without additional experiments.
- SB-1.8 The dissertation does not claim that device domain shift results (Experiment 6) constitute device certification, regulatory approval, or compliance with medical device standards. Results are empirical observations of cross-device performance variability.
- SB-1.10 The dissertation does not claim that calibration metrics (ECE, Brier Score) establish clinical reliability of predicted probabilities. Calibration is reported as an empirical diagnostic property of the model, not as a guarantee of clinical decision-making reliability.
- SB-1.11 The dissertation does not claim that Grad-CAM explainability analysis constitutes clinical validation of the model's diagnostic reasoning. Grad-CAM provides post-hoc interpretability, not a mechanistic explanation of model decision processes (see NC-14).
- SB-1.12 [v5.3] The dissertation does not treat Gulshan et al. (2016) as an experimental control or as a numerical benchmark. Gulshan functions as the **canonical representative of paradigm P1** — the end-to-end CNN classification paradigm in which preprocessing is treated as ancillary data preparation rather than as an integral model component. No direct numerical comparison with Gulshan is performed in this dissertation; differences in classification task (binary referable-DR vs. five-class DR 0–4), backbone architecture (Inception-v3 vs. ResNet-50 / EfficientNet-B3), pretraining source, dataset partition, and validation protocol preclude a fair head-to-head comparison. Numerical figures from Gulshan are admitted into the dissertation only as **historical / contextual reference**, accompanied by an explicit caveat noting these methodological differences. The **experimental baseline** in Experiment 1 (configs A/C) — stretch-resize + ImageNet normalize, 3 channels — is an internal operational construct defined in OD-3; it operationally instantiates the paradigm represented by Gulshan but is not itself Gulshan's system. The two referents (the paradigmatic representative and the operational baseline) must remain terminologically distinct in all dissertation text (see also SIR-9, CFC-2.9).

**SB-2: Dataset Limitations**

- SB-2.1 The primary training dataset (EyePACS) uses ~35,126 labeled fundus images with 5-class DR grading. Class imbalance characteristics must be documented and all performance claims interpreted in the context of distributional asymmetry.
- SB-2.2 Supplementary clinical images from private medical centers (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-SAPAKOVA-2025-01) are not publicly available due to privacy agreements. Reproducibility of results dependent on supplementary data is structurally limited.
- SB-2.3 Cross-database comparisons between EyePACS and external datasets (APTOS 2019, IDRiD, Messidor-2, RFMiD, DDR, ODIR-5K, Clinical) must explicitly acknowledge differences in imaging equipment, patient demographics, grading protocols, and disease taxonomy where applicable. RFMiD and ODIR-5K use multi-disease taxonomies with DR subsets; taxonomic mapping must be documented.
- SB-2.4 [v6.2.0] The integrated-arm self-supervised pretraining corpus is the **unlabeled EyePACS original "test" split (53,576 images)**. This corpus is label-free for the pretext task — the `testLabels15.csv` grades are used only by the linear-probe acceptance gate (DGL-6), never by the SSL objective — and is **disjoint** from the Experiment-1 evaluation corpus (the ~35,126 labeled images of the EyePACS "train" split governed by 5-fold patient-level stratified CV, SB-2.1), sharing no image identifier and no patient identifier. This disjointness is a binding no-pretraining-leakage constraint (analogous to ImageNet being a separate corpus for the baseline arm) and is operationalized in the experiments implementation as the disjointness assertions **INV-SSL-1 / INV-SSL-2** (`experiments/docs/fundus_ssl_pretraining_brief.md` §2–§3). The 53,576-image pretraining corpus is pretraining-only and must **not** be folded into Experiment-1 supervised training; the Experiment-1 dataset (~35,126) is governance-fixed. **[v6.3.0]** The label-restriction in this clause governs the *self-supervised* pretext objective only. A distinct **supervised in-domain pretraining (SIP)** stage MAY use the EyePACS-test DR grades as its training target (CFC-2.8 lists SIP as a gate-selected integrated-arm init), provided (a) the corpus remains disjoint from the Experiment-1 evaluation corpus by image and patient identity (INV-SSL-1/2), (b) it is a separate pretraining stage and is **not folded** into Experiment-1 supervised training (the ~35,126 corpus stays governance-fixed), and (c) the SIP acceptance gate tests on a **patient-level holdout the backbone did not train on**. The label-free SSL corpus semantics above are otherwise unchanged.

**SB-3: Architectural Limitations**

- SB-3.1 The dissertation evaluates two primary architectures in the factorial ablation (ResNet-50, EfficientNet-B3), one architecture for explainability analysis (EfficientNet-B4), and documents prior results on EfficientNetB0 from self-publications. No claim of architectural optimality or exhaustive search over the architecture space is permissible.
- SB-3.2 Results obtained under the specific hyperparameter configurations documented in the methodology do not generalize to architecturally equivalent configurations with different hyperparameters.

**SB-4: Deployment Limitations**

- SB-4.1 The system architecture described in Chapter 6 is a conceptual and design contribution (LC-2025-Yesmukhamedov-01). No prototype implementation or clinical deployment testing results are available as of the literature card record date.
- SB-4.2 GDPR/HIPAA compliance framing is a design specification, not a certified compliance status.
- SB-4.3 Applicability claims to Kazakhstan healthcare infrastructure are bounded by the absence of field testing in Kazakhstan clinical settings.

---

## V. EVIDENCE HIERARCHY

**EH-1: Primary Evaluation Metrics**

In descending order of evidentiary weight for evaluating diagnostic effectiveness:
1. Weighted F1-score (accounts for class imbalance; directly interpretable under skewed distribution)
2. ROC-AUC (threshold-independent performance measure)
3. Cohen's Kappa with quadratic weights (penalizes clinically significant ordinal misclassification)
4. Accuracy (reported but subject to inflation under class imbalance; not sufficient alone)

**EH-2: Secondary Metrics**

The following metrics are reported as supplementary and cannot independently establish or refute the primary hypotheses:
- Per-class Precision and Recall (informative but unstable under severe class imbalance for minority classes)
- Macro Average Precision/Recall/F1-score (reported alongside weighted average)
- Training-set metrics (used only for overfitting diagnosis, not for hypothesis evaluation)
- Clinical screening metrics: Sensitivity, Specificity, PPV, NPV for referable DR (grade ≥ 2) — reported for Experiment 3
- Calibration metrics: Expected Calibration Error (ECE) and Brier Score — reported for Experiments 1 and 3- Image quality metrics: Contrast-to-Noise Ratio (CNR), Vessel Visibility Index, Entropy, SSIM — reported for pipeline analysis in Experiment 2
- Explainability metrics: Grad-CAM ALO (primary) and IoU (secondary) with lesion masks, attention consistency score — reported for Experiment 4- Generalization ratio: G = F1_external / F1_EyePACS per OD-4 — reported for Experiment 3
**EH-3: Empirical Dominance Criterion**

A preprocessing condition is considered empirically dominant over a no-preprocessing baseline if and only if:
- Weighted F1-score improvement ≥ 5 percentage points on the test partition, AND
- ROC-AUC improvement ≥ 0.02 on the test partition, AND
- No degradation in Cohen's Kappa relative to baseline.

All three conditions must hold simultaneously. Improvement on a subset of metrics without satisfying all three does not constitute empirical dominance under this document.

**EH-4: Sufficient Validation Criterion**

The preprocessing dominance hypothesis (H-1) is considered sufficiently validated if:
- The empirical dominance criterion (EH-3) is satisfied on the EyePACS test partition, AND
- The same direction of effect (preprocessing ≻ no-preprocessing on primary metrics) is confirmed on at least one external dataset (APTOS 2019, IDRiD, or Messidor-2), AND
- Results are replicated across both architectures in the factorial design (ResNet-50 and EfficientNet-B3).

---

## VI. CLAIM FORMULATION CONSTRAINTS

**CFC-1: Permissible Claim Types**

- CFC-1.1 *Comparative claims bounded to tested configurations:* "Under conditions [X], configuration [A] outperformed configuration [B] on metric [M] by [δ]."
- CFC-1.2 *Parameter sensitivity claims bounded to tested ranges:* "Within the tested ranges of CLAHE dual-constraint parameters (clip_factor ∈ [a₁, b₁], global_threshold ∈ [a₂, b₂]), classification performance on [metric] exhibited a sensitivity profile with optimum at (clip_factor = [v₁], global_threshold = [v₂])."
- CFC-1.3 *Architectural precedent claims with explicit limitation:* "The two-stage fine-tuning protocol demonstrated by [LC-SAPAKOVA-2025] achieved [metric values] on [dataset]; this dissertation extends this finding by [specific methodological extension]."
- CFC-1.4 *Conceptual contribution claims:* "The modified CLAHE formulation with simplified threshold control (CLIP LIMIT = T/80, per LC-AlTimemy-2021) was adapted and validated within the dissertation's preprocessing pipeline."
- CFC-1.5 *Design claims for the system architecture:* "The proposed system architecture specifies [component] intended to support [function]; empirical validation of the deployed system is reserved for future work."

**CFC-2: Forbidden Claim Types**

- CFC-2.1 Universal generalization claims: "The proposed method is effective for all fundus image datasets." — Forbidden: no cross-database exhaustive testing documented.
- CFC-2.2 Superiority claims without direct comparison: "The proposed pipeline outperforms existing DR diagnostic systems." — Forbidden unless accompanied by a direct controlled experiment against named systems under identical evaluation conditions.
- CFC-2.3 Deployment outcome claims stated as results: "The system reduces late-stage DR complications by 20–30% in Kazakhstan." — Forbidden: this figure is a third-party projection cited in LC-2025-Yesmukhamedov-01, p. 88; it is not a result of this dissertation's experiments.
- CFC-2.4 Validated clinical claims: "The system achieves clinical-grade diagnostic accuracy." — Forbidden: no clinical validation trial is documented in any literature card.
- CFC-2.5 Perfect performance generalizations: "The preprocessing pipeline achieves 100% accuracy on DR classification." — Forbidden: 100% accuracy reported in LC-AlTimemy-2021 is on a different dataset, classification task, and cannot be transferred to the dissertation's experimental framework.
- CFC-2.6 Amplified source claims: Any claim that attributes to a cited source a conclusion stronger than explicitly stated in that source. — Forbidden per Section VII rules.
- CFC-2.7 Retroactive re-characterization of prior self-publications: Prior publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-Sapakova-2024-01, LC-2025-Yesmukhamedov-01) must be cited as-is and may not be retroactively characterized as having claimed, proven, or demonstrated conclusions beyond what their texts state.
- CFC-2.8 [v5.1; pretraining source revised v6.0.0] Attribution of the H-1 effect to preprocessing alone: Under H-1, the baseline arm uses ImageNet pretrain while the integrated arm uses ophthalmology-specific self-supervised pretrain. Any observed performance difference therefore reflects the joint contribution of preprocessing and pretraining source. Claims of the form "the preprocessing pipeline produces the observed improvement" or "preprocessing dominates" are forbidden in the context of H-1 results. Permissible claims are restricted to the integrated pipeline as a whole: "the integrated preprocessing + ophthalmology-SSL configuration outperforms the baseline + ImageNet configuration on [metric] by [δ]." **[v6.3.0]** The integrated-arm initialization may be fundus-SSL, an ImageNet→continual-SSL fallback, or **supervised in-domain pretraining (SIP)** on the EyePACS-test corpus, whichever passes the linear-probe acceptance gate; the choice does not weaken this clause. Under every option the integrated arm still differs from baseline along **both** the preprocessing and the initialization axis, so the H-1 effect remains non-attributable to preprocessing alone, and the permissible-claim restriction applies unchanged (substitute the selected initialization name for "ophthalmology-SSL").
- CFC-2.9 [v5.3] False attribution of theoretical claims to Gulshan et al. (2016) is forbidden. The dissertation may describe Gulshan's *methodological practice* — that preprocessing is left unformalised in the main text and deferred to supplementary material — and may designate Gulshan as the canonical representative of paradigm P1 on that basis (per SIR-9). The dissertation may **not** attribute to Gulshan or its authors an explicit theoretical statement of the form "preprocessing is unimportant," "preprocessing does not require methodological discussion," or any equivalent: no such statement appears in the cited text, and attributing it would violate SIR-1. Permissible phrasings: "Gulshan et al. (2016) treat preprocessing as ancillary data preparation," "Gulshan et al. (2016) defer preprocessing details to the supplement," "Gulshan et al. (2016) exemplify the methodological practice that this dissertation identifies as paradigm P1." Forbidden phrasings: "Gulshan claims preprocessing is unimportant," "Gulshan rejects preprocessing," "Gulshan argued that preprocessing does not matter." The same constraint applies to every other P1-tagged source. Equally forbidden are framings of the form "Gulshan is our baseline" or "we outperform Gulshan" (the former conflicts with OD-3 and SB-1.12; the latter violates CFC-2.2).

**CFC-3: Non-Claims**

- NC-1 through NC-13: Retained from v1.0 (as specified in prior Argument Map and claim structure documents).
- NC-14: Grad-CAM activation does not constitute clinical localization of pathology — it is an interpretability tool, not a diagnostic output. Grad-CAM overlays indicate regions of high gradient-weighted activation in the final convolutional layer and do not represent pixel-level diagnostic delineation of lesion boundaries.
- NC-15: The dirty data pipeline (External Image Ingestion Protocol) is not validated for arbitrary clinical data sources — validation is bounded to specific Kazakh medical center data. Generalization of the ingestion protocol to other clinical data sources requires independent validation.
- NC-16: Device domain shift results do not constitute device certification or regulatory compliance — they are empirical observations of cross-device performance variability. No claim of device-agnostic deployment readiness is permissible based on Experiment 6 alone.
- NC-17: The preprocessing component ablation does not identify a universally optimal preprocessing configuration — the component hierarchy is bounded to the tested architectures (ResNet-50, EfficientNet-B3) and datasets (EyePACS). Extension to other architectures or datasets requires independent experimental validation.

---

## VII. SOURCE INTERPRETATION RULES

**SIR-1: Non-Amplification Rule**  
A cited source may only be attributed conclusions that are explicitly stated within the cited text. Implications, logical consequences, or extensions of a source's conclusions are attributed to the dissertation's own analysis, not to the source. The source is cited for what it states; the dissertation is credited for what it infers.

**SIR-2: Limitation Inheritance Rule**  
When a source's result is cited as supporting a dissertation claim, the limitations acknowledged in that source's literature card (Section II.6) are co-inherited by the claim unless the dissertation provides evidence that specifically addresses those limitations. The limitation must be noted at first citation of the relevant result.

**SIR-3: Metric Consistency Rule**  
When citing performance metrics from a source, the evaluation context (dataset, partition, class taxonomy, metric formula) must be replicated or the difference must be explicitly stated. The sensitivity formula anomaly in LC-AlTimemy-2021 (Eq. 3: Sen = TP/(TP+TN), deviating from standard Sen = TP/(TP+FN)) must be noted if that source's sensitivity figure is cited.

**SIR-4: Self-Citation Transparency Rule**  
All self-authored prior publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-Sapakova-2024-01, LC-2025-Yesmukhamedov-01) must be explicitly identified as prior own work at point of citation. Results from these sources cited in the dissertation must be framed as "previously published results" and must be accompanied by a statement of how the dissertation's treatment extends, validates, or formalizes those results.

**SIR-5: No Cross-Source Aggregation Without Independence Confirmation**  
Sources that share overlapping datasets, authors, or experimental configurations (notably LC-SAPAKOVA-2025 and LC-Yesmukhamedov-2025-SELF, which use identical experimental data) may not be cited as independent confirmatory evidence of the same claim. Independent confirmation requires methodologically distinct experiments on distinct data partitions or datasets.

**SIR-6: Modeling Study Non-Extrapolation Rule**  
LC-Sapakova-2024-01 presents computational simulation results without quantitative clinical validation. Results from this source may be cited as theoretical/computational grounding only. They may not be cited as empirical validation of physical or clinical outcomes. The statement that simulation results "confirm the effectiveness of laser therapy" (LC-Sapakova-2024-01, Results, p. 7) is a claim of the source and must be cited as such, not absorbed into the dissertation's own validated claims.

**SIR-7: Architecture Generalization Prohibition**  
Results obtained with EfficientNetB0 (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF) may not be generalized to the class of efficient CNN architectures without explicit comparative experiments. The source's own limitation (LC-SAPAKOVA-2025, Section II.6) that "alternative architectures were not evaluated at this stage" is binding.

**SIR-8: Projected Outcome Non-Attribution Rule**  
Projected outcomes for Kazakhstan deployment cited in LC-2025-Yesmukhamedov-01 (p. 88: 4+ million rural residents accessed; 20–30% late-stage DR reduction; 15–20% cost reduction) are third-party projections cited by the authors. They may not be attributed to the dissertation's own findings or used to substantiate claims about demonstrated system impact.

**SIR-9: Paradigmatic Attribution Rule [v5.3]**
A cited source may be designated the *"canonical representative of paradigm X"* only when **both** of the following conditions hold:
- **(a) Methodological match.** The source's *observed methodological practice* — what the authors actually do in the paper (e.g., the role assigned to preprocessing; the structure of the model/data pipeline; the locus of methodological emphasis) — matches the operational definition of paradigm X as stated in the dissertation.
- **(b) Attributional honesty.** The citation refers to the source for that practice, **not** for an explicit theoretical statement that does not appear in the text. The dissertation is credited for the paradigmatic reading (the act of grouping practices into paradigm X); the source is cited only for what it states or does.

Designation of a source as canonical representative of a paradigm is therefore a claim about practice, not about authorial intent. It must be supported in the relevant literature card by a Methodological-Practice note in §15 (Relevance to My Dissertation) or §18 (Analytical Synthesis), explicitly identifying the observable feature of the source that grounds the paradigmatic attribution. In the absence of such a Methodological-Practice note, the source may be cited only as a landmark or as a historical reference (not as a paradigmatic representative). SIR-9 is a strengthening of SIR-1 (Non-Amplification) for the specific case of paradigmatic grouping; CFC-2.9 specifies the forbidden phrasings that SIR-9 disallows.

---

## VIII. THESIS VERSION CONTROL RULE

**VCR-1:** The Central Thesis (Section I) and Core Hypotheses (Section II) are immutable post-ratification of this document. Modifications to the thesis or hypotheses require the creation of a new versioned Invariants document; they do not propagate retroactively to literature cards.

**VCR-2:** Literature cards record the state of source interpretation at the time of extraction. If new sources are added to the dissertation, new literature cards must be created and appended to the literature card corpus. Existing literature cards are not modified to accommodate new sources.

**VCR-3:** If experimental results contradict the direction of effect specified in H-1, H-2, H-4, H-5, H-6, or H-7, the hypothesis is not silently modified. The result is reported as a falsifying observation, and the dissertation text must explicitly account for the discrepancy between the null finding and the hypothesis as stated.
**VCR-4:** The scope boundaries defined in Section IV are fixed for the dissertation's primary experimental claims. If additional experiments are conducted beyond the scope defined here, those experiments constitute extended contributions and must be explicitly labeled as extensions, not revisions of the core thesis.

**VCR-5:** Terminology defined in Section III must remain stable across all dissertation chapters. Terminological drift — the use of operationally defined terms with different referents in different sections — constitutes a constraint violation.

---

## IX. DEPLOYMENT AND GENERALIZATION LIMITATIONS

**DGL-1: Dataset-Bound Generalization**
All performance claims are bounded to the dataset architecture: EyePACS (~35,126 labeled images, five-class DR staging, primary training), APTOS 2019 (cross-dataset transferability evaluation), IDRiD (clinical validation and lesion localization with pixel-level annotations), Messidor-2 (clinical degradation evaluation), Clinical (Kazakh medical center validation), and RFMiD/DDR/ODIR-5K (device domain shift evaluation across Topcon, Kowa, Canon, and Zeiss camera hardware). Extension to other fundus image datasets, other imaging devices not represented in the tested corpora, or other clinical populations requires independent experimental validation not currently available.

**DGL-2: Hardware-Specific Reproducibility**  
Experimental results are obtained under hardware constraints as documented in Section 4.1.3 of the dissertation. Claims about computational efficiency or real-time inference capability are bounded to the specific hardware configuration used. They do not generalize to substantially different hardware contexts (e.g., mobile inference on ARM processors, or server-class GPU clusters) without re-evaluation.

**DGL-3: Clinical Population Non-Extrapolation**  
The datasets in the dataset architecture and supplementary clinical images from private medical centers do not constitute a demographically characterized clinical population sample. No claims regarding system performance on specific ethnic, age-stratified, or comorbidity-defined patient groups are permissible.

**DGL-4: System Architecture Deployment Constraints**  
The system architecture described in Chapter 6 (LC-2025-Yesmukhamedov-01) has not been prototype-implemented or field-tested. All deployment-oriented statements (PACS integration, EHR interoperability, GDPR/HIPAA compliance, telemedicine support) are design specifications. Their operational realization in Kazakhstan's healthcare infrastructure is subject to infrastructure prerequisites acknowledged in the source (LC-2025-Yesmukhamedov-01, p. 90): investments in diagnostic equipment, adaptation of algorithms to local data, national standards development, and specialist training.

**DGL-5: CLAHE Parameter Portability**
CLAHE parameters validated in the dissertation context (dual-constraint clip limit on LAB L-channel per pipeline: clip_factor × tile_area/256, capped by global_threshold × tile_area; applied stochastically at train time with 80% probability; selected via parameter sweep in Experiment 2; and clip limit 2.0 / grid size 8×8 per prior self-publications LC-SAPAKOVA-2025-01) were optimized for specific image distributions and CNN architectures. The T/80 threshold formulation from LC-AlTimemy-2021 was derived on the STARE dataset with different image characteristics. No parameter-level equivalence between these configurations is asserted. If the dissertation adopts modified CLAHE parameters, those parameters must be independently validated within the dissertation's experimental framework.

**DGL-6: Transfer Learning Domain Gap [v5.1 amended; pretraining source revised v6.0.0]**
The dissertation operates under two distinct pretraining regimes:
- **Baseline arm (H-1 baseline configurations):** EfficientNetB0, EfficientNet-B3, EfficientNet-B4, and ResNet-50 weights were pre-trained on ImageNet (natural images). Transfer of these weights to fundus image classification represents a cross-domain shift (natural images → retinal imaging).
- **integrated arm (H-1 integrated configurations):** Initialization derived from **ophthalmology-specific self-supervised pretraining** of the same CNN backbone (ResNet-50 or EfficientNet-B3) on an unlabeled retinal fundus corpus, using a CNN-compatible domain-adaptive SSL protocol (the DINO / BYOL / SimCLR / MoCo family). No diabetic-retinopathy labels are used during pretraining; the objective is representation learning over fundus imagery (vascular topology, optic-disc and macular morphology, retinal texture, illumination variability, imaging artifacts). This represents an in-domain initialization with respect to the retinal-imaging domain while preserving the CNN architecture used in the baseline arm. **[v6.2.0 operational specifics]** The pretraining corpus is fixed to the unlabeled EyePACS "test" split (53,576 images), disjoint from the Experiment-1 corpus per SB-2.4. The **primary protocol is BYOL** (Grill et al., 2020), pretrained **from-scratch (random initialization)** directly on the 4-channel tensor (RGB + FOV mask), with **MoCo-v2 / SimSiam / DINO retained as alternatives** and the final selection confirmed by a **linear-probe acceptance gate**: with the backbone frozen, a single linear head is trained and evaluated on a label-bearing slice of the EyePACS-test corpus, and the SSL checkpoint may enter Experiment 1 only if it (a) beats a random-init backbone by a clear margin and (b) is competitive with (within a small quadratic-weighted-κ margin of, or better than) the ImageNet-init backbone, for **both** backbones. An ImageNet→continual-SSL initialization is a documented fallback should the gate fail; it is not the default and must be explicitly flagged if used.

The degree to which either pretraining source transfers to the dissertation's specific dataset architecture is not theoretically guaranteed and is evaluated empirically within the experimental framework only. Claims about feature transferability are bounded to the architectures, fine-tuning protocols, and datasets documented in the literature cards and current experimental protocol.

---

## X. AMENDMENT OPEN QUESTIONS (v5.1) — RESOLVED in v6.0.0

The v5.1 amendment introduced operational specifications that were left open as binding placeholders. The **v6.0.0 amendment resolves them** by replacing the RETFound foundation model with ophthalmology-specific self-supervised pretraining of the existing CNN backbones. The original question text is retained below for audit purposes, each prefixed with its v6.0.0 resolution status.

### v6.0.0 Resolution summary
- **AOQ-1 — RESOLVED → option (b).** The integrated arm uses a CNN-compatible domain-adaptive self-supervised pretraining protocol (DINO / BYOL / SimCLR / MoCo family) on an unlabeled fundus corpus, not RETFound's ViT-Large. Architecture is **not** confounded with preprocessing: the same CNN backbones (ResNet-50, EfficientNet-B3) are used in both arms.
- **AOQ-2 — SIMPLIFIED.** Because the SSL pretraining is performed by the candidate, it may be run directly on 4-channel tensors (RGB + FOV mask), eliminating any input-channel mismatch; alternatively the copy-and-mean-init protocol for channel 3 (`experiments/src/models/resnet.py` lines 47–52) remains available. No ViT patch-embedding adaptation is required. OD-3 Stage 3 (4-channel input) is preserved.
- **AOQ-3 — RETIRED (moot).** RETFound's CC BY-NC 4.0 license no longer applies; the SSL weights are trained in-house. No external weight-license precondition remains.
- **AOQ-4 — RESOLVED.** The 2×2 *(preprocessing × architecture)* factorial symmetry is restored: both ResNet-50 and EfficientNet-B3 run in both the baseline and the integrated arm (configs A/B/C/D in RESEARCH_ARCHITECTURE.md). The replication test across architecture families (EH-4) is reinstated.

The composite independent variable and CFC-2.8 are **retained**: the integrated arm still differs from baseline along both the preprocessing and the pretraining axis (ImageNet → ophthalmology-SSL), so the H-1 effect remains non-attributable to preprocessing alone.

---

**AOQ-1 [RESOLVED v6.0.0 → option (b)]: Backbone architecture in the integrated arm.**
RETFound is published as a ViT-Large vision transformer. The dissertation's v5.0 design used ResNet-50 and EfficientNet-B3 as the backbone families. Three resolution options are open:

- (a) Replace the integrated-arm backbone with RETFound's ViT-Large. This changes the architecture between baseline and integrated arms and introduces architecture as a third confound on top of preprocessing and pretrain.
- (b) Restrict the integrated arm to a CNN-compatible domain-adaptive pretraining protocol (e.g., SparK-style masked image modeling adapted for ResNet-50, or contrastive SSL such as SimCLR/MoCo on EyePACS), rather than using RETFound weights literally. Under this option the term "RETFound" in v5.1 must be replaced with the specific protocol used.
- (c) Run two integrated configurations: full pipeline + RETFound (ViT-L) and full pipeline + ImageNet (ResNet-50/EfficientNet-B3), allowing partial recovery of the preprocessing-vs-pretrain factor decomposition at the cost of additional compute.

AOQ-1 is unresolved as of 2026-05-13. Until resolved, statements in H-1 v5.1 referencing "RETFound pretrained weights" refer to *whichever resolution of AOQ-1 is ratified*, not to a guarantee of ViT-Large adoption.

**AOQ-2 [SIMPLIFIED v6.0.0]: Four-channel input adaptation.**
*(Note: with in-house SSL pretraining the encoder can be trained directly on 4-channel tensors, so the mismatch below — written for the externally-pretrained RETFound checkpoint — is largely moot. Retained for audit.)*
RETFound's CFP-pretrained checkpoint (the one loaded in v5.2) was trained on 3-channel RGB fundus images. The pipeline produces a 4-channel tensor (RGB + FOV mask, per Stage 3). (Note: the separately published OCT-pretrained RETFound checkpoint is single-channel and is not considered here; the integrated arm is bound to the CFP checkpoint per v5.2.) Adapting the first patch-embedding (ViT) or first convolution (CNN under AOQ-1 option (b)) to accept 4 channels requires either:

- (a) Copy pretrained weights to channels 0–2 and initialize channel 3 from the per-channel mean of pretrained weights (the protocol currently used for ImageNet weights in `experiments/src/models/resnet.py` lines 47–52). Under this option, a fraction of retina-specific pretrained representations is destroyed at channel 3.
- (b) Drop the FOV mask from the input to preserve all pretrained weights, at the cost of reverting to 3 channels (which contradicts OD-3 Stage 3, requiring an Invariants amendment of its own).
- (c) Concatenate the FOV mask in a non-input position (e.g., as a multiplicative gating mask at an intermediate layer), preserving the 3-channel input contract while still using the mask. Requires architectural extension not specified in v5.0 or v5.1.

AOQ-2 is unresolved as of 2026-05-13.

**AOQ-3 [RETIRED v6.0.0 — moot]: License and weight provenance.**
RETFound weights are published under a specific license (CC BY-NC 4.0 per the rmaphoh/RETFound_MAE repository at time of access). The dissertation must verify that the license terms permit the intended downstream use (including any commercial or clinical-deployment-adjacent framing). License verification is a precondition for any code-side adoption.

**AOQ-4 [RESOLVED v6.0.0 — symmetry restored]: Baseline asymmetry with v5.0 architecture comparison.**
The v5.0 factorial isolated two architecture families (ResNet-50 vs EfficientNet-B3) under a fixed pretrain. If the v5.1 baseline arm continues to evaluate both ResNet-50 and EfficientNet-B3 under ImageNet pretrain while the integrated arm uses a single backbone under RETFound (per AOQ-1), the factorial loses its 2×2 symmetry. A symmetric design requires either two RETFound-compatible backbones (none exist as published) or a reduction of the baseline arm to a single architecture for the H-1 comparison.

---

*Version: 6.0.0. Binding upon ratification. All subsequent dissertation drafts are subject to constraint verification against this document. The v6.0.0 amendment reverses the v5.1–v5.2 RETFound adoption: the integrated arm of Experiment 1 is initialized from **ophthalmology-specific self-supervised pretraining** of the existing CNN backbones (ResNet-50 / EfficientNet-B3) rather than from the RETFound ViT-Large foundation model. This resolves AOQ-1 (→ option b), AOQ-4 (factorial symmetry restored), and AOQ-3 (license moot), and simplifies AOQ-2. The composite independent variable and CFC-2.8 are retained (the integrated arm differs in both preprocessing and pretraining). Because this reverses a binding constraint, it is a MAJOR version bump per VERSIONING_POLICY §4. The v5.3 amendment introduces the paradigmatic framing (P1 / P2), designates Gulshan et al. (2016) as the canonical representative of P1, and adds clauses SB-1.12, CFC-2.9, and SIR-9. No operational definitions, hypotheses, or experimental protocols are modified by v5.3. The v5.2 amendment refines the RETFound pretraining-corpus description to the multi-modal CFP + OCT specification and binds the integrated arm to the CFP-pretrained checkpoint. The v5.1 amendment supersedes v5.0 for the H-1 hypothesis, the DGL-6 constraint, and adds CFC-2.8 and Section X. All other v5.0 provisions remain in force unchanged.*
