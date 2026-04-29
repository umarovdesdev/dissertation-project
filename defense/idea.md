# Original Solutions — Novelty Register

**Candidate:** Yesmukhamedov N.S., IITU (Almaty, Kazakhstan)
**Dissertation:** "Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification"
**Compiled:** 2026-04-24
**Sources:** `thesis/governance/` v5.0 (CONTRIBUTIONS.md, HYPOTHESIS.md, CENTRAL_THESIS.md, RESEARCH_ARCHITECTURE.md)

This document consolidates every original solution claimed in the dissertation, so novelty can be verified in one place against the literature and the implementation.

---

## 0. Central Scientific Idea

`model = V5_preprocessing + CNN`

The 8-stage V5 preprocessing pipeline is declared an **integral component of the diagnostic model**, not ancillary data preparation. It defines the feature space available to the CNN. This framing — treating preprocessing as Stage 1 of a two-stage diagnostic system — is the organizing idea the whole dissertation is built on.

The central hypothesis: the V5 pipeline reduces domain variability across fundus imaging devices and acquisition conditions while preserving diagnostically relevant retinal features, leading to improved CNN-based DR detection.

---

## 1. Primary Contributions

### C-1. Cross-Device Normalization Pipeline (V5, 8 stages)

Design, implementation, and experimental validation of an 8-stage V5 fundus preprocessing pipeline standardizing retinal image appearance across imaging devices and acquisition conditions while preserving diagnostic features. Output: 4-channel tensor (RGB + binary FOV mask), dataset-specific normalization.

Novelty components (what together has not been published as a single integrated pipeline):

- (a) Isotropic resize with centered zero-padding preserving fundus-circle geometry
- (b) Explicit FOV mask as a 4th input channel informing the CNN of valid pixel regions
- (c) Adaptive flat-field correction with σ proportional to FOV diameter (σ = 0.07·D) rather than a fixed global σ
- (d) Dataset-specific channel-wise normalization computed from training-set mask=1.0 pixels (not ImageNet defaults)
- (e) Canonical orientation via OD-fovea rotation normalization with adaptive augmentation σ
- Validated across 8 datasets (EyePACS, APTOS 2019, IDRiD, Messidor-2, DDR, ODIR-5K, RFMiD, Clinical) and two CNN families (ResNet-50, EfficientNet-B3)

**Evidence:** Exp 1 (2×2 factorial A–D), Exp 2 (7-level component ablation + parameter sweeps), Exp 6 (device domain shift).

### C-2. Cross-Dataset Generalization Evidence

Empirical demonstration that CNNs trained with V5 on EyePACS generalize zero-shot to APTOS 2019 with a pre-registered threshold G = F1_APTOS / F1_EyePACS ≥ 0.85.

**Novelty:** Systematic zero-shot transferability with a pre-registered generalization ratio on an independent 5-class DR dataset of mixed camera origins. **Evidence:** Exp 3.

### C-3. Lesion Feature Preservation Analysis via ALO

Quantitative demonstration, via Grad-CAM explainability, that V5 preprocessing directs CNN attention toward clinically relevant lesion regions (microaneurysms, hemorrhages, hard exudates, soft exudates).

**Novelty:** Introduction of **Attention–Lesion Overlap (ALO)** as a quantitative, asymmetric metric that directly measures lesion coverage by model attention:

```
ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask)
```

ALO is positioned as the **primary** explainability metric (clinically meaningful — what fraction of the lesion the model attends to). IoU retained as a **secondary** symmetric precision metric. ALO is systematically compared between preprocessed and unprocessed conditions per lesion type on IDRiD, with qualitative Grad-CAM overlays on the Kazakh Clinical dataset. **Evidence:** Exp 4.

---

## 2. Supporting Original Solutions

### SC-A. Adaptive Dual-Constraint CLAHE (Stage 5)

Modified CLAHE formulation applied on the **LAB L-channel** with a **dual-constraint clip limit**:

```
CL_tile = min(clip_factor × tile_area / 256, global_threshold × tile_area)
```

Tile grid 8×8. Stochastic at train time (p = 0.80), deterministic at inference. The stochastic application doubles as regularization. Transferability of clip parameters from STARE is **not** assumed — parameters are independently validated within the dissertation (DGL-5). **Evidence:** Exp 2 CLAHE sweep.

### SC-B. CLAHE Sensitivity Profile

Characterization of a **non-trivial parameter-dependent sensitivity curve** for per-class F1 (particularly DR 1 and DR 2) under (clip_factor, global_threshold) variation, with an identifiable local optimum. **Evidence:** Exp 2 parameter sweep on EyePACS.

### SC-C. Cross-Device Robustness Matrix

Systematic evaluation across **four fundus camera manufacturers** (Canon, Topcon, Kowa, Zeiss) using five datasets with documented camera metadata, producing a cross-device performance matrix. DR labels only; non-DR disease labels ignored or mapped. **Evidence:** Exp 6 (DDR, ODIR-5K, RFMiD).

### SC-D. Adaptive Flat-Field Illumination Normalization (Stage 4)

Adaptive Gaussian blur subtraction:

```
corrected = image − GaussianBlur(image, σ) + 128,   σ = 0.07 × D   (D = FOV diameter in px)
```

**Novelty:** σ scales with per-image FOV diameter (derived from the Stage 3 mask) rather than using a global fixed σ, accommodating device variability in fundus size/FOV coverage. Correction is applied **only inside the FOV mask** to prevent padding artifacts. **Evidence:** Exp 2 component ablation + σ sweep across 0.05–0.10·D; image quality metrics CNR, VVI, SSIM, Entropy measured before/after Stage 4.

### SC-E. FOV Mask as Explicit Pipeline Component (Stage 3)

Explicit binary FOV mask (1.0 = real fundus data, 0.0 = zero-padding) generated as a dedicated pipeline stage and **appended as the 4th CNN input channel**. Prevents the CNN from learning padding artifacts as features and informs downstream stages which pixels are valid. **Evidence:** Exp 1 configs B/D use 4-channel input; Exp 2 ablation isolates isotropic+mask stage.

### SC-F. OD-Fovea Rotation Normalization (Stage 1)

Classical-CV-based detection of optic disc (brightest region) and fovea (darkest region with distance prior); image rotated so the OD→fovea axis is horizontal. Two original design decisions:

- **Confidence fallback:** on low detection confidence the rotation is skipped (avoids injecting incorrect rotations).
- **Per-image adaptive augmentation σ:** Stage 6 rotation augmentation σ is derived from the Stage 1 detection uncertainty (fallback σ = 13.0°). Images with high detection confidence get narrow augmentation; low-confidence images get wider augmentation — augmentation magnitude is data-dependent rather than a global constant.

**Evidence:** Exp 2 component ablation, Stage 1 contribution. Code: `src/preprocessing/od_fovea_detect.py`, `src/preprocessing/canonical_orientation.py`.

### SC-G. Clinical Degradation Resistance (Δ metric)

Metric and evaluation protocol:

```
Δ = F1_EyePACS_val − F1_external
```

computed for baseline and V5 models on IDRiD and Messidor-2. Smaller Δ with V5 indicates more robust transfer. Pre-registered statistical criterion: Δ_V5 < Δ_baseline with statistical significance (paired test across folds). **Evidence:** Exp 5 (H-7).

---

## 3. Original Methodological Decisions (Pipeline-Level)

| # | Decision | Why it is original |
|---|----------|-------------------|
| M-1 | Stage 0 canonical flip (left→right eye) applied **always-on** | Eliminates the left/right axis of symmetry as a learnable nuisance; makes Stage 1 rotation well-defined |
| M-2 | Isotropic resize with **centered zero-padding** instead of stretch-resize | Preserves fundus-circle geometry — area and aspect-ratio-sensitive lesions remain geometrically faithful |
| M-3 | FOV mask as **4th channel** (not just a mask for loss weighting) | The CNN receives the mask as an input feature, not just a spatial selector |
| M-4 | Flat-field σ **adaptive to FOV diameter** (σ = 0.07·D) | Prior flat-field literature typically uses fixed σ; here σ scales with per-image geometry |
| M-5 | Flat-field restricted to **inside FOV mask only** | Avoids padding artifacts bleeding into correction |
| M-6 | CLAHE **dual-constraint clip limit** on LAB L-channel | Single-constraint CLAHE is standard; dual constraint + LAB L-channel + stochastic train-time application is the specific variant validated here |
| M-7 | CLAHE **stochastic at train (p=0.8), deterministic at inference** | Provides regularization at train time while guaranteeing reproducibility at inference |
| M-8 | **Per-image adaptive augmentation σ** driven by Stage 1 detection confidence | Couples augmentation strength to data-driven uncertainty, not a global schedule |
| M-9 | **Dataset-specific channel-wise normalization** from training-set FOV-masked pixels | Statistics computed on the *post-preprocessing* distribution, mask=1.0 pixels only — not ImageNet defaults |

---

## 4. Formal Hypotheses (H-1 … H-7)

| H | Hypothesis (condensed) | Experiment | Decision criterion |
|---|------------------------|-----------|--------------------|
| H-1 | Preprocessing Dominance — V5 beats baseline independently for ResNet-50 and EfficientNet-B3 | Exp 1 (2×2 factorial A–D) | Δ weighted F1 ≥ 5 pp AND Δ ROC-AUC ≥ 0.02 AND no Cohen κ degradation, for **both** architectures |
| H-2 | CLAHE threshold sensitivity + full component ablation | Exp 2 | Parameter-dependent per-class F1 sensitivity for DR 1 and DR 2 with at least one local optimum; flat-field σ swept 0.05–0.10·D |
| H-4 | Cross-dataset transferability | Exp 3 (EyePACS → APTOS 2019, zero-shot) | G = F1_APTOS / F1_EyePACS ≥ 0.85 |
| H-5 | Explainability | Exp 4 (IDRiD + Clinical, EfficientNet-B4) | ALO_preproc > ALO_baseline (primary); IoU_preproc > IoU_baseline (secondary) |
| H-6 | Device domain shift | Exp 6 (DDR, ODIR-5K, RFMiD) | Performance maintained across Canon / Topcon / Kowa / Zeiss within acceptable variance |
| H-7 | Clinical degradation resistance | Exp 5 (IDRiD + Messidor-2) | Δ_V5 < Δ_baseline with statistical significance (paired test across folds) |

H-3 was dropped in V3 of the governance; not claimed.

---

## 5. Experimental Originality

### Exp 1 — 2×2 Factorial with Confound Control

Four configurations A–D across `{baseline, V5} × {ResNet-50, EfficientNet-B3}`, plus **Config N (normalization control)**: baseline preprocessing + dataset-specific normalization without V5 stages. Config N disambiguates the normalization-statistics effect from the pipeline-stages effect — an explicit confound-isolation design rather than a single-variable ablation.

### Exp 2 — 7-Level V5 Component Ablation

Ordered addition of stages: baseline → +flip → +rotation → +isotropic+mask → +flat-field → +CLAHE → full V5. Plus two parameter sweeps: CLAHE (clip_factor, global_threshold) and flat-field σ (0.05–0.10·D). Image quality metrics (CNR, VVI, Entropy, SSIM) reported at each stage — originality is the combination of classification-level ablation with physical image-quality metrics on the same stages.

### Exp 3 — Pre-registered Generalization Threshold

Pre-registration of G ≥ 0.85 as success criterion **before** evaluation on APTOS 2019. Zero-shot (no weight updates). Original in its pre-registered threshold combined with a concrete G definition tied to weighted F1.

### Exp 4 — ALO + IoU with Dual-Domain Validation

Quantitative IDRiD evaluation (ALO primary, IoU secondary, 4 lesion types) **combined** with qualitative Clinical dataset overlays (Kazakh medical center data). Original in using ALO as a named, primary, asymmetric lesion-coverage metric, and in pairing a public-benchmark quantitative analysis with an institutional-dataset qualitative analysis.

### Exp 5 — Δ Metric for Degradation

Formal Δ = F1_val − F1_external as the degradation metric, evaluated for both baseline and V5, with paired-fold significance testing.

### Exp 6 — Four-Manufacturer Device-Shift Matrix

Cross-device matrix covering Canon, Topcon, Kowa, Zeiss on DDR, ODIR-5K, RFMiD. DR-only labels (non-DR mapped/ignored) — clean DR-only protocol on datasets originally multi-disease.

### Exp 7 — Small-Data Feasibility (IDRiD → Clinical)

Train on IDRiD (516 images, 5-fold CV), test on the Kazakh Clinical dataset (60 images). Bootstrap CI (≥1000) required given sizes. Probes V5 trainability outside the large EyePACS regime.

---

## 6. Statistical Validation Framework (Original Compositional Choices)

| Tool | Applied to |
|------|-----------|
| McNemar paired test | Exp 1 (paired classification comparison) |
| DeLong test | Exp 1, Exp 3 (ROC-AUC comparison) |
| Mixed-effects model (fold as random effect) | Exp 1 cross-fold analysis |
| Bonferroni/Holm correction | Exp 1, Exp 2 (multiple comparisons across configs / ablation levels) |
| Bootstrap CI (≥1000) | All experiments; **required** for Exp 7 (small data) |
| 5-fold patient-level stratified CV | All experiments (no patient in both train and val within any fold) |

Originality is in the **pre-specified composition**: which test at which experiment, with which correction and which threshold, written before results are obtained.

---

## 7. Non-Claims (What the Novelty Explicitly Does NOT Include)

These are recorded to prevent inadvertent over-claiming during defense:

- NOT global state-of-the-art on any public benchmark
- NOT clinical deployment validation or device certification (NC-16)
- NOT universal preprocessing optimality — the component hierarchy is bounded to the tested architectures (ResNet-50, EfficientNet-B3, EfficientNet-B4) and tested datasets (NC-17)
- NOT cross-modality transfer (fundus photography only)
- NOT replacement of an ophthalmologist

Scope boundaries enforced per INVARIANTS.md §IV and ARGUMENT_MAP.md §VII.

---

## 8. Summary — Where to Look to Verify Each Claim

| Solution | Governance doc | Code path |
|----------|---------------|-----------|
| V5 pipeline orchestration | `thesis/governance/RESEARCH_ARCHITECTURE.md §3.1` | `experiments/src/preprocessing/pipeline_v5.py` |
| Stage 1 OD-fovea rotation | CONTRIBUTIONS.md SC-F | `experiments/src/preprocessing/od_fovea_detect.py`, `canonical_orientation.py` |
| Stage 4 adaptive flat-field | CONTRIBUTIONS.md SC-D | `experiments/src/preprocessing/flat_field.py` |
| Stage 5 dual-constraint CLAHE | CONTRIBUTIONS.md SC-A | `experiments/src/preprocessing/upgraded_clahe.py` |
| Stage 7 dataset-specific norm | CONTRIBUTIONS.md C-1(d) | `experiments/src/preprocessing/imagenet_normalize.py` |
| ALO metric | CONTRIBUTIONS.md C-3 | `experiments/src/explainability/iou.py` |
| 2×2 factorial + Config N | RESEARCH_ARCHITECTURE.md §5.1 | `experiments/src/experiments/exp1_factorial.py` |
| 7-level ablation + sweeps | RESEARCH_ARCHITECTURE.md §5.2 | `experiments/src/experiments/exp2_ablation.py` |
| Transferability G | RESEARCH_ARCHITECTURE.md §5.3 | `experiments/src/experiments/exp3_transferability.py` |
| Grad-CAM ALO/IoU | RESEARCH_ARCHITECTURE.md §5.4 | `experiments/src/experiments/exp4_explainability.py` |
| Δ degradation | RESEARCH_ARCHITECTURE.md §5.5 | `experiments/src/experiments/exp5_clinical_degradation.py` |
| Device-shift matrix | RESEARCH_ARCHITECTURE.md §5.6 | `experiments/src/experiments/exp6_device_shift.py` |
| Small-data IDRiD→Clinical | RESEARCH_ARCHITECTURE.md §5.7 | `experiments/src/experiments/exp7_clinical.py` |
