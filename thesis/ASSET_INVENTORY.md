# ASSET INVENTORY — Dissertation Figures, Tables & Experimental Results

**Document type:** Resource inventory (prerequisite for the chapter-by-chapter writing PLAN)
**Candidate:** Yesmukhamedov N.S.
**Compiled:** 2026-06-08
**Scope:** Full monorepo scan (`experiments/`, `demo/`, `defense/`, `thesis/assets/`) reconciled against the required figures/tables derived from `thesis/outline/MASTER_OUTLINE.md`, every chapter `README.md`, `thesis/governance/RESEARCH_ARCHITECTURE.md` (v6.0.0), and `HYPOTHESIS.md`.

---

## 0. Provenance Policy (read first)

This inventory distinguishes three things that are easy to conflate:

1. **A file existing on disk** (a PNG, a CSV, a JSON).
2. **A real experimental result** produced by running the dr-classifier pipeline.
3. **A demo or slide preview figure** rendered for the *defense slides* or the *demo dashboard* to illustrate the intended layout of a result.

**Hard rule applied throughout:** A figure or JSON existing in `defense/` or `demo/` does **NOT** by itself mean the underlying experiment has been run. Several demo result files carry placeholder metrics authored for the dashboard preview — e.g. `demo/web/public/results/exp3/exp3_aptos_transfer.json` reports `G = 0.890`, `h4_satisfied: true`, and a DeLong `p = 0.015`, although **Experiment 3 has not yet been executed and no APTOS evaluation output exists on disk**. Such files are catalogued as demo assets; the corresponding dissertation result is flagged `❌ MISSING (real result)` until the experiment is run.

**Status legend:**
- `✅ AVAILABLE` — a real, citable artifact verified to exist at the stated path (real fundus image, real preprocessing render, real metrics from a training run, real validation JSON, or a conceptual/architecture diagram).
- `⏳ PENDING` — partial real data exists on disk but the full required result set (e.g. all configs × 5 folds) is not yet complete; or the artifact is derivable now from existing data but not yet rendered.
- `❌ MISSING` — no real result artifact on disk yet. A demo-dashboard preview may exist (path noted) and is catalogued as a demo asset.

---

## 1. Gap-Analysis Summary

### 1.1 Experiment result status (real data on disk)

| Exp | Hypothesis | Required | What is actually on disk | Verdict |
|-----|-----------|----------|--------------------------|---------|
| **Exp 1** | H-1 | 2×2 factorial A–D, EyePACS 100%, 5-fold CV, full metric suite | Config **A** fold 0 only (19 ep, full-data backup); Configs **A/B/C** folds 0–2 partial at **40% data**; a **broken Config D** fold 0 (ImageNet, diverged val_loss≈140); a **clean Config D** fold 0 (10 ep, EyePACS) + checkpoints | **⏳ PARTIAL** — no complete A–D × 5-fold at 100%; v6.0.0 ophthalmology-SSL arm (B/D) not yet trained |
| **Exp 2** | H-2 | 7-level ablation + CLAHE sweep + σ sweep + image-quality metrics | No real run; demo-dashboard preview PNGs + placeholder `exp2_ff_sweep.json` | **❌ NOT RUN** |
| **Exp 3** | H-4 | APTOS 2019 zero-shot transfer, G ratio | No real run; demo-dashboard preview `exp3_aptos_transfer.json` + PNG | **❌ NOT RUN** |
| **Exp 4** | H-5 | Grad-CAM ALO/IoU on IDRiD + Clinical | No real run; demo-dashboard preview gradcam/alo/iou PNGs | **❌ NOT RUN** |
| **Exp 5** | H-7 | Clinical degradation Δ on IDRiD + Messidor-2 | No real run; demo-dashboard preview `exp5_degradation.json` + PNG | **❌ NOT RUN** |
| **Exp 6** | H-6 | Device domain shift on DDR/ODIR-5K/RFMiD | No real run; demo-dashboard preview PNG | **❌ NOT RUN** |
| **Exp 7** | — | Small-data 5-fold IDRiD → Clinical | No real run; demo-dashboard preview `exp7_small_data.json` + PNG | **❌ NOT RUN** |
| **Validation** | — (supporting Ch 3/Exp 4) | OD/fovea detector accuracy on IDRiD | **Real** `od_fovea_idrid_metrics.json` + montage (516 imgs) | **✅ COMPLETE** |
| **Preproc artifacts** | — (Ch 3) | norm stats, PCA color basis | **Real** EyePACS + IDRiD norm stats, EyePACS PCA eigvals/eigvecs | **✅ COMPLETE** |

### 1.2 Resource tally

**Reconciliation table (§2) — required dissertation resources:** 78 catalogued.
- **✅ AVAILABLE (real, citable):** 33 — almost entirely **preprocessing stage renders, dataset sample images, conceptual/architecture diagrams, the OD/fovea validation, norm-stat artifacts, source code, and publication certificates**.
- **⏳ PENDING:** 6 — Exp 1 partial-data tables/curves derivable now from real `metrics.csv`, plus claim-strength/SOTA tables that depend on results.
- **❌ MISSING (real result):** 39 — **every result table/figure for Exp 2–7**, Exp 1 full 100% A–D suite, confusion matrices, ROC curves, calibration, statistical-test tables, Grad-CAM gallery, and UML diagrams. Demo-dashboard previews exist for many (catalogued in §4) but are not citable as results.

**Demo web asset manifest (§4) — files present in `demo/web/public/`:** 471 files, all `✅ AVAILABLE` on disk — `results/` (33), `diagrams/` (4), `pipeline/` (430 PNG + 1 helper JSON). The `pipeline/` preprocessing renders are real pipeline outputs; the `results/` figures and `pipeline/.../results/` overlays are dashboard previews whose result-level status is tracked in §2.

### 1.3 Implication for writing order

**Writable now (no result dependency):**
- **Chapter 1 (Problem Domain)** — literature review; dataset sample montages available for context.
- **Chapter 2 (Theoretical Foundations)** — pure theory; some diagrams reusable, others to draw.
- **Chapter 3 (Methodology)** — ✅ **fully unblocked.** Every pipeline stage has a real render; OD/fovea validation, norm stats, PCA basis, training-config and evaluation-framework tables all exist.
- **Chapter 6 (System Architecture)** — design-only chapter; system diagram + webapp screenshots available. **Only blocker:** UML diagrams (component/sequence/class/activity/ER) are not on disk.
- **§4.1 (Datasets & Configuration)** — dataset architecture table + class distribution + samples available.

**Blocked pending experiment execution:**
- **§4.2 (Exp 1)** — partially writable from real partial data, but the headline 2×2 factorial table and EH-3 dominance verdict require the full 100% A–D × 5-fold run (and the v6.0.0 ophthalmology-SSL B/D arm).
- **§4.3–§4.8 (Exp 2–7)** — fully blocked; no real data.
- **Chapter 5 (Validation)** — fully blocked; depends on Ch 4 results, statistical tests, and the Grad-CAM gallery.
- **Chapter 0 (Introduction) & Chapter 7 (Conclusion)** — depend on all results being final.
- **Appendices B, C, E, F** — confusion matrices, UML, Grad-CAM gallery, device tables: all missing.

---

## 2. Master Reconciliation Table

> Paths are relative to repo root `E:\dissertation-project\`. Every `✅ AVAILABLE` row points to a file verified to exist during this scan.

### 2.1 Chapter 1 — Problem Domain

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| FIG-1.1 | figure | Representative fundus images across DR grades 0–4 (clinical grading context) | §1.1.1 | EyePACS samples (demo) | `demo/web/public/datasets/eyepacs/samples/dr{0..4}/` | ✅ AVAILABLE |
| FIG-1.2 | figure | Cross-dataset / multi-camera landscape comparison | §1.2.3, §1.4 | defense | `defense/presentation/assets/datasets/27_overview/cross_dataset_comparison.png` | ✅ AVAILABLE |
| TAB-1.1 | table | Survey of existing automated DR systems (IDx-DR, EyeNuk, DeepMind, Gulshan et al.) | §1.4 | literature cards | `thesis/literature/external/` (text, not rendered) | ⏳ PENDING |

### 2.2 Chapter 2 — Theoretical Foundations

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| FIG-2.1 | diagram | Histogram equalization → CLAHE intensity redistribution concept | §2.1.1 | — | — | ❌ MISSING |
| FIG-2.2 | diagram | CNN feature-hierarchy / convolution-pooling schematic | §2.2.1 | defense | `defense/presentation/assets/architecture/07_cnn/cnn_architecture.png` | ✅ AVAILABLE |
| FIG-2.3 | diagram | Grad-CAM mathematical formulation schematic | §2.5.1 | — | — | ❌ MISSING |
| FIG-2.4 | diagram | Coupled thermal-optical laser-tissue model | §2.4.1 | — | — | ❌ MISSING |
| FIG-2.5 | diagram | Image-quality metrics (CNR/VVI/Entropy/SSIM) illustration | §2.6 | — | — | ❌ MISSING |
| TAB-2.1 | table | CLAHE clip-limit formulations (conventional vs T/80 vs dual-constraint) | §2.1.2 | governance (RESEARCH_ARCHITECTURE §3.2) | text | ✅ AVAILABLE |

### 2.3 Chapter 3 — Methodology (fully unblocked)

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| FIG-3.1 | diagram | 8-stage preprocessing pipeline overview (vertical) | §3.1.1 | defense | `defense/presentation/assets/preprocessing/10_input/04_preprocessing_pipeline_vertical.png` | ✅ AVAILABLE |
| FIG-3.2 | figure | Stage 0 — Canonical flip (L→R) | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/11_canonical_flip/stage0_canonical_flip.png`; `demo/web/public/pipeline/dr04/preprocessing/stage_0_canonical_flip/` | ✅ AVAILABLE |
| FIG-3.3 | figure | Stage 1 — OD-fovea rotation normalization | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/12_od_fovea_rotation/stage1_od_fovea_rotation.png`; `demo/web/public/pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/` | ✅ AVAILABLE |
| FIG-3.4 | figure | Stage 2 — FOV crop + isotropic resize | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/13_crop_resize/stage2_fov_crop_resize.png` | ✅ AVAILABLE |
| FIG-3.5 | figure | Stage 3 — FOV mask (4th channel) | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/14_fov_mask/stage3_fov_mask.png` | ✅ AVAILABLE |
| FIG-3.6 | figure | Stage 4 — Adaptive flat-field correction | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/15_flatfield/stage4_flatfield.png` | ✅ AVAILABLE |
| FIG-3.7 | figure | Stage 5 — Dual-constraint CLAHE (incl. polar variant + vessel maps) | §3.1.1, §3.1.2 | defense / demo | `defense/presentation/assets/preprocessing/17_clahe_polar/stage5_clahe.png`; `demo/web/public/pipeline/dr04/preprocessing/stage_5_clahe/polar/` | ✅ AVAILABLE |
| FIG-3.8 | figure | Stage 6 — Augmentation (rotation/translation/scale/shear/PCA-color/brightness) | §3.1.3 | defense / demo | `defense/presentation/assets/preprocessing/19_aug_rotation/ … 24_aug_brightness_contrast/stage6_augmentation.png` | ✅ AVAILABLE |
| FIG-3.9 | figure | Stage 7 — Dataset-specific normalization | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/25_normalization/stage7_normalize.png` | ✅ AVAILABLE |
| FIG-3.10 | figure | OD/fovea detector validation montage (IDRiD, 516 imgs) | §3.1.1 (Stage 1) | **Exp validation (real)** | `experiments/outputs/validation/od_fovea_idrid_montage.png` | ✅ AVAILABLE |
| FIG-3.11 | diagram | ResNet-50 / EfficientNet-B3 backbone architecture | §3.2.1 | defense | `defense/presentation/assets/architecture/08_comparison/01_abstract_model_architecture.png`; `defense/figures/figures_mine/fig5_architecture_artistic.png` | ✅ AVAILABLE |
| FIG-3.12 | diagram | Focal-loss weighting schematic | §3.3.4 | defense | `defense/presentation/assets/architecture/09_training/focal_loss.png` | ✅ AVAILABLE |
| FIG-3.13 | diagram | 5-fold patient-level CV split | §3.4.2 | defense | `defense/presentation/assets/architecture/09_training/cv_5fold.png` | ✅ AVAILABLE |
| FIG-3.14 | diagram | End-to-end pipeline flowchart (model = preprocessing + CNN) | §3.1, §3.2 | defense | `defense/figures/figures_mine/fig4_flowchart.png`; `defense/figures/figures_mine/fig6_model_graph.png` | ✅ AVAILABLE |
| TAB-3.1 | table | Standardized training configuration (optimizer, batch, epochs, loss, seed) | §3.4 / §4.1.3 | governance (RESEARCH_ARCHITECTURE §4.0) | text | ✅ AVAILABLE |
| TAB-3.2 | table | Multi-metric evaluation framework & diagnostic thresholds (EH-1, OD-5) | §3.4.1 | governance | text | ✅ AVAILABLE |
| TAB-3.3 | table | Image-quality metrics definitions (CNR/VVI/Entropy/SSIM) | §3.4.1 | governance (RESEARCH_ARCHITECTURE §3.3) | text | ✅ AVAILABLE |
| RES-NORM | result-set | Per-dataset normalization stats (EyePACS, IDRiD) — Stage 7 | §3.1.1 | **Exp (real)** | `experiments/data/processed/eyepacs_norm_stats.json`, `experiments/data/processed/idrid_norm_stats.json` | ✅ AVAILABLE |
| RES-PCA | result-set | EyePACS PCA color-jitter basis (Stage 6) | §3.1.3 | **Exp (real)** | `experiments/outputs/kaggle_config_d_v2/data/processed/eyepacs_pca_eigvals.npy`, `…_eigvecs.npy` | ✅ AVAILABLE |
| RES-VAL | result-set | OD/fovea detector accuracy metrics (IDRiD train/test) | §3.1.1 | **Exp (real)** | `experiments/outputs/validation/od_fovea_idrid_metrics.json` | ✅ AVAILABLE |

### 2.4 Chapter 4 — Experimental Research

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| TAB-4.1 | table | Tiered dataset architecture (8 datasets, roles, sizes, cameras) | §4.1.1 | governance (RESEARCH_ARCHITECTURE §2.1) | text | ✅ AVAILABLE |
| FIG-4.1 | figure | EyePACS class-distribution chart | §4.1.2 | defense | `defense/presentation/assets/datasets/27_overview/12_dataset_class_distribution.png` (+`.svg`); data `defense/figures/figures_mine/fig3_dataset_distribution.csv` | ✅ AVAILABLE |
| FIG-4.2 | figure | Sample fundus per DR grade — EyePACS (+ APTOS/IDRiD/Messidor2/DDR/ODIR5K/RFMiD/Clinical) | §4.1.1 | demo | `demo/web/public/datasets/<ds>/samples/dr{0..4}/` | ✅ AVAILABLE |
| FIG-4.3 | figure | Cross-dataset comparison / datasets matrix | §4.1.1 | defense | `defense/presentation/assets/datasets/28_experiments/datasets_matrix.png`; `…/29_cameras/cameras_alignment.png` | ✅ AVAILABLE |
| RES-EXP1 | result-set | Exp 1 training metrics (loss, weighted F1, ROC-AUC, κ, accuracy per epoch/fold/config) | §4.2 | **Exp (real, partial)** | `experiments/outputs/backup_exp1_full/metrics.csv` (A f0); `…/backup_exp1_abc_40pct_20260324/metrics.csv` (A/B/C f0–2 @40%); `…/kaggle_config_d_v2/outputs/exp1/metrics.csv` (D f0) | ⏳ PENDING |
| TAB-4.2 | table | **Exp 1 2×2 factorial results** — F1/ROC-AUC/κ/Acc (mean±std), configs A–D, EH-3 verdict | §4.2.3 | Exp 1 (full 100% A–D × 5-fold) | demo dashboard: `demo/web/public/results/exp1/02_exp1_all_metrics.png` | ❌ MISSING |
| FIG-4.4 | figure | Exp 1 factorial weighted-F1 bar chart (A–D) | §4.2.3 | Exp 1 | demo dashboard: `demo/web/public/results/exp1/01_exp1_factorial_f1.png`, `…/03_exp1_delta.png` | ❌ MISSING |
| FIG-4.5 | figure | Exp 1 training/validation convergence curves (A–D) | §4.2.2 | Exp 1 | derivable from real `metrics.csv` for A f0 & D f0 (partial); demo dashboard: `…/results/exp1/19_training_curves.png` | ⏳ PENDING |
| FIG-4.6 | figure | Exp 1 confusion matrices (per config) | §4.2.3 / App B | Exp 1 | demo dashboard: `…/results/exp1/20_confusion_matrix.png` (no per-sample preds saved) | ❌ MISSING |
| FIG-4.7 | figure | Exp 1 ROC curves (per config) | §4.2.3 | Exp 1 | demo dashboard: `…/results/exp1/24_roc_curves.png` | ❌ MISSING |
| FIG-4.8 | figure | Exp 1 per-class F1 under class imbalance | §4.2.3 | Exp 1 | demo dashboard: `…/results/exp1/18_per_class_f1.png` | ❌ MISSING |
| TAB-4.3 | table | Exp 1 calibration (ECE, Brier) per config | §4.2.2 | Exp 1 | demo dashboard: `…/results/general/15_calibration.png` | ❌ MISSING |
| TAB-4.4 | table | **Exp 2 ablation (Levels 0–6)** — weighted F1 per level | §4.3.1 | Exp 2 | demo dashboard: `…/results/exp2/04_exp2_ablation.png`, `…/05_exp2_per_stage.png` | ❌ MISSING |
| FIG-4.9 | figure | Exp 2 CLAHE clip-limit sensitivity curve | §4.3.2 | Exp 2 | demo dashboard: `…/results/exp2/13_exp2_clahe_sensitivity.png` | ❌ MISSING |
| FIG-4.10 | figure | Exp 2 flat-field σ sweep | §4.3.3 | Exp 2 | demo dashboard: `…/results/exp2/exp2_ff_sweep.json` | ❌ MISSING |
| TAB-4.5 | table | Exp 2 image-quality metrics per stage (CNR/VVI/Entropy/SSIM) | §4.3.3 | Exp 2 | demo dashboard: `…/results/general/16_image_quality.png` | ❌ MISSING |
| TAB-4.6 | table | **Exp 3 APTOS transfer** — G = F1_APTOS/F1_EyePACS per config | §4.4 | Exp 3 | demo dashboard: `…/results/exp3/exp3_aptos_transfer.json` (preview G=0.890) | ❌ MISSING |
| FIG-4.11 | figure | Exp 3 cross-dataset transfer chart | §4.4 | Exp 3 | demo dashboard: `…/results/exp3/29_exp3_aptos_transfer.png` | ❌ MISSING |
| FIG-4.12 | figure | **Exp 4 Grad-CAM overlays** per DR class, baseline vs integrated (IDRiD) | §4.5.1 / App E | Exp 4 | demo dashboard: `…/results/exp4/27_gradcam_overlay.png` | ❌ MISSING |
| TAB-4.7 | table | **Exp 4 ALO (primary) + IoU (secondary)** per lesion type | §4.5.2 | Exp 4 | demo dashboard: `…/results/exp4/06_exp4_alo.png`, `…/07_exp4_iou.png` | ❌ MISSING |
| FIG-4.13 | figure | Exp 4 attention-consistency across datasets | §4.5.3 | Exp 4 | demo dashboard: `…/results/exp4/28_attention_consistency.png` | ❌ MISSING |
| FIG-4.14 | figure | Exp 4 lesion-overlay reference (IDRiD masks) | §4.5.2 | Exp 4 | demo asset: `defense/figures/figures_mine/fig2_lesion_overlays.png` | ❌ MISSING |
| TAB-4.8 | table | **Exp 5 clinical degradation** Δ=F1_val−F1_ext (IDRiD, Messidor-2) | §4.6 | Exp 5 | demo dashboard: `…/results/exp5/exp5_degradation.json` | ❌ MISSING |
| FIG-4.15 | figure | Exp 5 degradation / generalization chart | §4.6 | Exp 5 | demo dashboard: `…/results/exp5/08_exp5_generalization.png`, `…/09_exp5_G_ratio.png` | ❌ MISSING |
| TAB-4.9 | table | **Exp 6 device domain shift** — per-camera F1/AUC (Canon/Topcon/Kowa/Zeiss) | §4.7 / App F | Exp 6 | demo dashboard: `…/results/exp6/10_exp6_device_shift.png` | ❌ MISSING |
| TAB-4.10 | table | **Exp 7 small-data** 5-fold IDRiD→Clinical (baseline vs integrated) | §4.8 | Exp 7 | demo dashboard: `…/results/exp7/exp7_small_data.json` | ❌ MISSING |
| FIG-4.16 | figure | Exp 7 small-data performance chart | §4.8 | Exp 7 | demo dashboard: `…/results/exp7/30_exp7_small_data.png` | ❌ MISSING |

### 2.5 Chapter 5 — Reliability Validation

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| FIG-5.1 | figure | Grad-CAM gallery (representative per class, baseline vs integrated) | §5.1 / App E | Exp 4 | — | ❌ MISSING |
| TAB-5.1 | table | Statistical tests (McNemar, DeLong, bootstrap 95% CI, mixed-effects) | §5.2.1 | Exp 1–7 | demo dashboard: `…/results/general/21_statistical_tests.png` | ❌ MISSING |
| TAB-5.2 | table | Final claim-strength classification PC-1…PC-10 (STRONG/MODERATE/CONDITIONAL) | §5.2.2 | governance + results | derivable once results exist | ⏳ PENDING |
| TAB-5.3 | table | Comparative analysis vs published systems (IDx-DR, EyeNuk, DeepMind, Gulshan — contextual only) | §5.3.1 | literature cards | text (numbers pending own results) | ⏳ PENDING |
| FIG-5.2 | figure | Performance–complexity trade-off | §5.3.2 | Exp 1/6 | demo dashboard: `…/results/general/17_computational.png` | ❌ MISSING |
| FIG-5.3 | figure | Summary radar across hypotheses / EH-3 dominance | §5.2 | all Exp | demo dashboard: `…/results/general/11_summary_radar.png`, `…/12_eh3_dominance.png` | ❌ MISSING |
| TAB-5.4 | table | Clinical screening metrics (Sensitivity/Specificity/PPV/NPV, referable DR) | §5.2 | Exp 1/3/5 | demo dashboard: `…/results/general/14_clinical_metrics.png` | ❌ MISSING |
| FIG-5.4 | figure | Precision–recall curves | §5.2 / App B | Exp 1 | demo asset: `defense/figures/figures_mine/fig7_pr_curves.png` | ❌ MISSING |

### 2.6 Chapter 6 — System Architecture (design-only)

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| DIA-6.1 | diagram | Modular system architecture (capture→preprocess→inference→report) | §6.1.2 | defense | `defense/presentation/assets/architecture/06_system/02_system_architecture.png` | ✅ AVAILABLE |
| DIA-6.2 | diagram | Preprocessing engine (configurable pipeline) | §6.2.1 | defense (reuse FIG-3.1) | `defense/presentation/assets/preprocessing/10_input/04_preprocessing_pipeline_vertical.png` | ✅ AVAILABLE |
| FIG-6.1 | figure | Deployed web-app / dashboard screenshots | §6.2, §6.3 | defense | `defense/figures/figures_mine/fig10_webapp_screenshot_1.png`, `…_2.png` | ✅ AVAILABLE |
| DIA-6.3 | diagram | UML component / sequence / class / activity / ER diagrams | §6.1.2 / App C | — | — | ❌ MISSING |

### 2.7 Appendices & Front Matter

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| APP-A | result-set | Source code of preprocessing pipeline | App A | experiments | `experiments/src/preprocessing/` (+ `experiments/src/`) | ✅ AVAILABLE |
| APP-B | figure-set | Supplementary confusion matrices & training curves | App B | Exp 1–7 | partial (Exp1 curves derivable); rest ❌ | ⏳ PENDING |
| APP-C | diagram-set | System architecture UML diagrams | App C | — | — | ❌ MISSING |
| APP-D | figure-set | Certificates / publication confirmations (Scopus, KBTU, KazUTB, NAS RK) | App D | defense | `defense/presentation/assets/publications/SCOPUS.png`, `…/PUBLICATIONS.png`, `…/KBTU.png`, `…/KAZTBU.png`, `…/AKADEMY.png`, `…/SCOPUS_CONF.png` | ✅ AVAILABLE |
| APP-E | figure-set | Grad-CAM visualization gallery (per class, both pipelines) | App E | Exp 4 | — | ❌ MISSING |
| APP-F | table-set | Device domain-shift supplementary per-camera tables/heatmaps | App F | Exp 6 | — | ❌ MISSING |

---

## 3. Real Result Files On Disk (verified manifest)

The complete set of **real, machine-produced result artifacts** found in `experiments/` (the demo-dashboard preview assets under `demo/`+`defense/` are catalogued separately in §4):

```
experiments/outputs/backup_exp1_full/metrics.csv                       # Exp1 Config A, fold 0, 19 epochs (full-data)
experiments/outputs/backup_exp1_abc_40pct_20260324/metrics.csv         # Exp1 A/B/C folds 0–2 (partial) @40% + broken D f0
experiments/outputs/kaggle_config_d_v2/outputs/exp1/metrics.csv        # Exp1 Config D, fold 0, 10 epochs (clean, EyePACS)
experiments/outputs/kaggle_config_d_v2/outputs/exp1/checkpoints/D_fold0/best_model.pt   # + epoch_05..09, last_checkpoint
experiments/outputs/kaggle_config_d/outputs/exp1/metrics.csv           # header-only (empty run)
experiments/outputs/validation/od_fovea_idrid_metrics.json             # OD/fovea detector accuracy (real)
experiments/outputs/validation/od_fovea_idrid_montage.png              # OD/fovea overlay montage (real)
experiments/data/processed/eyepacs_norm_stats.json                     # Stage-7 norm stats (real)
experiments/data/processed/idrid_norm_stats.json                       # Stage-7 norm stats (real)
experiments/outputs/kaggle_config_d_v2/data/processed/eyepacs_pca_eigvals.npy / eigvecs.npy   # Stage-6 PCA basis (real)
experiments/logs/exp1_*.log, smoke_test_*.log, exp2_remaining_smoke.log  # training/smoke logs
```

**Key honesty notes carried into the PLAN:**
1. **Exp 1 is the only experiment with any real metrics, and it is incomplete** — no complete A–D × 5-fold at 100% data; the v6.0.0 design (ophthalmology-SSL initialization for the integrated arm B/D) has **not** been trained at all (current Config-D checkpoints are the retired ImageNet artifact, per project memory). The clean Config-D fold-0 run reports strong numbers (e.g. weighted F1 ≈ 0.82, ROC-AUC ≈ 0.93 at epoch 4) but is a **single fold**.
2. **Exp 2–7 have produced no real result artifacts yet.** The corresponding figures/JSONs in `demo/` and `defense/` are **demo-dashboard preview assets** (catalogued in §4) and carry placeholder numbers until the experiments are run, so they are not citable as results.
3. **Confusion matrices, ROC curves, calibration, and statistical tests** cannot be derived even for Exp 1 from current outputs, because **per-sample predictions/probabilities were not saved** — only per-epoch aggregate metrics. Producing TAB-4.2 / FIG-4.6 / FIG-4.7 requires re-running inference with prediction dumps.
4. **Chapter 3 and §4.1 are the safe starting points** — every asset they need is real and on disk.

---

## 4. Demo Web Asset Manifest (`demo/web/public/`)

Complete enumeration of every PNG/JSON under `demo/web/public/results`, `demo/web/public/diagrams`, and `demo/web/public/pipeline`. All paths below are relative to `demo/web/public/` and all files were verified to exist during this scan. **Status `✅ AVAILABLE`** means the file is present on disk; for the `results/` group it does **not** assert that a real experiment backs the depicted numbers (see the Status column of §2.4–§2.5 for the result-level verdict).

### 4.1 `results/` — dashboard result figures (33 files)

| ID | Path (`demo/web/public/`) | Type | Linked resource | Status |
|----|---------------------------|------|-----------------|--------|
| DEMO-R-01 | `results/exp1/01_exp1_factorial_f1.png` | png | FIG-4.4 | ✅ AVAILABLE |
| DEMO-R-02 | `results/exp1/02_exp1_all_metrics.png` | png | TAB-4.2 | ✅ AVAILABLE |
| DEMO-R-03 | `results/exp1/03_exp1_delta.png` | png | FIG-4.4 | ✅ AVAILABLE |
| DEMO-R-04 | `results/exp1/18_per_class_f1.png` | png | FIG-4.8 | ✅ AVAILABLE |
| DEMO-R-05 | `results/exp1/19_training_curves.png` | png | FIG-4.5 | ✅ AVAILABLE |
| DEMO-R-06 | `results/exp1/20_confusion_matrix.png` | png | FIG-4.6 | ✅ AVAILABLE |
| DEMO-R-07 | `results/exp1/22_exp1_all_6_configs.png` | png | TAB-4.2 | ✅ AVAILABLE |
| DEMO-R-08 | `results/exp1/24_roc_curves.png` | png | FIG-4.7 | ✅ AVAILABLE |
| DEMO-R-09 | `results/exp2/04_exp2_ablation.png` | png | TAB-4.4 | ✅ AVAILABLE |
| DEMO-R-10 | `results/exp2/05_exp2_per_stage.png` | png | TAB-4.4 | ✅ AVAILABLE |
| DEMO-R-11 | `results/exp2/13_exp2_clahe_sensitivity.png` | png | FIG-4.9 | ✅ AVAILABLE |
| DEMO-R-12 | `results/exp2/23_exp2_individual_ablation.png` | png | TAB-4.4 | ✅ AVAILABLE |
| DEMO-R-13 | `results/exp2/exp2_ff_sweep.json` | json | FIG-4.10 | ✅ AVAILABLE |
| DEMO-R-14 | `results/exp3/29_exp3_aptos_transfer.png` | png | FIG-4.11 | ✅ AVAILABLE |
| DEMO-R-15 | `results/exp3/exp3_aptos_transfer.json` | json | TAB-4.6 | ✅ AVAILABLE |
| DEMO-R-16 | `results/exp4/06_exp4_alo.png` | png | TAB-4.7 | ✅ AVAILABLE |
| DEMO-R-17 | `results/exp4/07_exp4_iou.png` | png | TAB-4.7 | ✅ AVAILABLE |
| DEMO-R-18 | `results/exp4/27_gradcam_overlay.png` | png | FIG-4.12 | ✅ AVAILABLE |
| DEMO-R-19 | `results/exp4/28_attention_consistency.png` | png | FIG-4.13 | ✅ AVAILABLE |
| DEMO-R-20 | `results/exp5/08_exp5_generalization.png` | png | FIG-4.15 | ✅ AVAILABLE |
| DEMO-R-21 | `results/exp5/09_exp5_G_ratio.png` | png | FIG-4.15 | ✅ AVAILABLE |
| DEMO-R-22 | `results/exp5/exp5_degradation.json` | json | TAB-4.8 | ✅ AVAILABLE |
| DEMO-R-23 | `results/exp6/10_exp6_device_shift.png` | png | TAB-4.9 | ✅ AVAILABLE |
| DEMO-R-24 | `results/exp7/30_exp7_small_data.png` | png | FIG-4.16 | ✅ AVAILABLE |
| DEMO-R-25 | `results/exp7/exp7_small_data.json` | json | TAB-4.10 | ✅ AVAILABLE |
| DEMO-R-26 | `results/general/11_summary_radar.png` | png | FIG-5.3 | ✅ AVAILABLE |
| DEMO-R-27 | `results/general/12_eh3_dominance.png` | png | FIG-5.3 | ✅ AVAILABLE |
| DEMO-R-28 | `results/general/14_clinical_metrics.png` | png | TAB-5.4 | ✅ AVAILABLE |
| DEMO-R-29 | `results/general/15_calibration.png` | png | TAB-4.3 | ✅ AVAILABLE |
| DEMO-R-30 | `results/general/16_image_quality.png` | png | TAB-4.5 | ✅ AVAILABLE |
| DEMO-R-31 | `results/general/17_computational.png` | png | FIG-5.2 | ✅ AVAILABLE |
| DEMO-R-32 | `results/general/21_statistical_tests.png` | png | TAB-5.1 | ✅ AVAILABLE |
| DEMO-R-33 | `results/general/25_pipeline_stages_real.png` | png | FIG-3.1 | ✅ AVAILABLE |
| DEMO-R-34 | `results/general/26_bilateral_pair.png` | png | FIG-4.2 | ✅ AVAILABLE |

> Note: `results/exp3/exp3_aptos_transfer.json`, `results/exp5/exp5_degradation.json`, `results/exp7/exp7_small_data.json`, and `results/exp2/exp2_ff_sweep.json` contain dashboard preview numbers; the matching dissertation results remain `❌ MISSING` (§2.4) until the experiments are run.

### 4.2 `diagrams/` — architecture & pipeline diagrams (4 files)

| ID | Path (`demo/web/public/`) | Type | Linked resource | Status |
|----|---------------------------|------|-----------------|--------|
| DEMO-D-01 | `diagrams/01_abstract_model_architecture.png` | png | FIG-3.11 | ✅ AVAILABLE |
| DEMO-D-02 | `diagrams/02_system_architecture.png` | png | DIA-6.1 | ✅ AVAILABLE |
| DEMO-D-03 | `diagrams/03_preprocessing_stages_detailed.png` | png | FIG-3.1 | ✅ AVAILABLE |
| DEMO-D-04 | `diagrams/04_preprocessing_pipeline_vertical.png` | png | FIG-3.1 / DIA-6.2 | ✅ AVAILABLE |

### 4.3 `pipeline/` — per-DR-grade preprocessing renders (430 PNG + 1 JSON)

Real renders of the full preprocessing pipeline applied to one bilateral fundus pair (`left`/`right`) per DR grade. The directory holds **5 grade folders** — `dr00`, `dr01`, `dr02`, `dr03`, `dr04` — **each containing the identical 86-file structure** listed below (so 5 × 86 = 430 PNGs), plus one shared helper JSON. These back the Chapter 3 stage figures (FIG-3.2…FIG-3.9) and the Exp 4 Grad-CAM/attention previews.

**Shared helper:**

| ID | Path (`demo/web/public/`) | Type | Status |
|----|---------------------------|------|--------|
| DEMO-P-COORDS | `pipeline/helpers/coords.json` | json | ✅ AVAILABLE |

**Per-grade 86-file template** (shown for `dr04`; the same relative paths exist under `pipeline/dr00/`, `pipeline/dr01/`, `pipeline/dr02/`, `pipeline/dr03/`). Linked resource shown per stage group; all `✅ AVAILABLE`.

```
# input (2) — raw bilateral pair                                  [→ FIG-3.1]
pipeline/dr04/input/left.png
pipeline/dr04/input/right.png

# Stage 0 — canonical flip (2)                                    [→ FIG-3.2]
pipeline/dr04/preprocessing/stage_0_canonical_flip/left.png
pipeline/dr04/preprocessing/stage_0_canonical_flip/right.png

# Stage 1 — OD-fovea rotation (10: final + od/fovea/midpoint/image overlays) [→ FIG-3.3]
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/right.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/od/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/od/right.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/fovea/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/fovea/right.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/midpoint/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/midpoint/right.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/image/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/image/right.png

# Stage 2 — FOV crop + resize (2)                                 [→ FIG-3.4]
pipeline/dr04/preprocessing/stage_2_fov_crop_resize/left.png
pipeline/dr04/preprocessing/stage_2_fov_crop_resize/right.png

# Stage 3 — FOV mask (2)                                          [→ FIG-3.5]
pipeline/dr04/preprocessing/stage_3_fov_mask/left.png
pipeline/dr04/preprocessing/stage_3_fov_mask/right.png

# Stage 4 — flat-field correction (2)                            [→ FIG-3.6]
pipeline/dr04/preprocessing/stage_4_flatfield/left.png
pipeline/dr04/preprocessing/stage_4_flatfield/right.png

# Stage 5 — CLAHE: final + cv2 + polar variants (16)             [→ FIG-3.7]
pipeline/dr04/preprocessing/stage_5_clahe/left.png
pipeline/dr04/preprocessing/stage_5_clahe/right.png
pipeline/dr04/preprocessing/stage_5_clahe/cv2/left.png
pipeline/dr04/preprocessing/stage_5_clahe/cv2/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/1_vessel_detection/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/1_vessel_detection/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/2_vessel_density/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/2_vessel_density/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/3_polar_grid_adaptive/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/3_polar_grid_adaptive/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/4_density_grid_adaptive/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/4_density_grid_adaptive/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/5_clahe_no_interpolation/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/5_clahe_no_interpolation/right.png

# Stage 6 — augmentation (42)                                    [→ FIG-3.8]
#   1_rotation (22)
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/distribution_adaptive.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_contours.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_distribution_normal.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_distribution_step.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_distribution_step_mono.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_peaks.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_sectors.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_sectors_mono.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_variant_A.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_variant_B.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_contours.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_distribution_normal.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_distribution_step.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_distribution_step_mono.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_peaks.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_sectors.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_sectors_mono.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_variant_A.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_variant_B.png
#   2_scale (5)
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/left_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/left_min.png
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/right_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/right_min.png
#   3_shear (5)
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/left_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/left_min.png
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/right_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/right_min.png
#   4_pca_color_jitter (5)
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/left_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/left_min.png
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/right_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/right_min.png
#   5_brightness_contrast (5)
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/left_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/left_min.png
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/right_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/right_min.png

# Stage 7 — normalize (2)                                         [→ FIG-3.9]
pipeline/dr04/preprocessing/stage_7_normalize/left.png
pipeline/dr04/preprocessing/stage_7_normalize/right.png

# results — gradcam / attention / prediction overlays (6)        [→ FIG-4.12 / FIG-4.13]
pipeline/dr04/results/gradcam/left.png
pipeline/dr04/results/gradcam/right.png
pipeline/dr04/results/attention_overlay/left.png
pipeline/dr04/results/attention_overlay/right.png
pipeline/dr04/results/prediction/left.png
pipeline/dr04/results/prediction/right.png
```

> The `pipeline/dr0X/preprocessing/` renders (Stages 0–7) are **real pipeline outputs** and directly back Chapter 3's stage figures. The `pipeline/dr0X/results/` overlays (gradcam/attention/prediction) are dashboard previews; the corresponding quantitative Exp 4 results remain `❌ MISSING` (§2.4).
