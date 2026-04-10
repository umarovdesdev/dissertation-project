# Seminar Presentation — Slide Plan with Context Materials

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification  
**Candidate:** Yesmukhamedov N.S.

---

## How to use this document

Each slide lists the **files to load into the Claude Opus 4.6 chat context** before requesting that slide. Files are given as paths within the monorepo (`thesis/` and `experiments/`). Where a file is large, a specific section or line range is noted to stay within token budget.

**Batch strategy:** Slides that share materials are grouped into sessions. A single chat session can typically handle 3–5 slides that draw from the same governance files.

---

## SESSION A — Title + Introduction Block (Slides 1–7)

These slides draw heavily from the governance constraint system and require a consistent voice. Load them together.

### Slide 1 — Title Slide

**Content:** Dissertation title, candidate name, supervisor, university (IITU), defense date.

**Files to load:**
- `thesis/governance/CENTRAL_THESIS.md` — *full file (short, 5 lines)* — for the exact thesis title formulation
- `thesis/governance/CORE_OBJECTIVE.md` — *full file (short, 5 lines)* — for the research goal wording

**Instructions to Claude:** Generate a title slide with the exact dissertation title from CENTRAL_THESIS.md, candidate name "Yesmukhamedov N.S.", university "IITU — International Information Technology University", and a placeholder for supervisor name and defense date.

---

### Slide 2 — Research Motivation and Relevance

**Content:** DR prevalence statistics, Kazakhstan healthcare context, screening gap.

**Files to load:**
- `thesis/literature/external/gulshan-2016.md` — *Section 1 (Bibliographic) + Section 4 (Key Findings)* — for the landmark 34.6% prevalence figure and AUC 0.991 reference
- `thesis/literature/self/yesmukhamedov-nan-rk.md` — *Sections 4 (Key Findings) and 12 (Relevance)* — for Kazakhstan-specific statistics (40% rural population, ~1,200 ophthalmologists, projected deployment impact)
- `thesis/literature/self/yesmukhamedov-scopus-q2.md` — *Sections 4 and 12* — for screening gap framing and resource-limited context
- `thesis/literature/external/ruamviboonsuk-2022.md` — *Section 4 (Key Findings)* — for LMIC deployment precedent (Thailand prospective study)
- `thesis/governance/INVARIANTS.md` — *Section IX: DGL-4* — for the Kazakhstan infrastructure constraints (ensures no overclaiming)

**Instructions to Claude:** Use the epidemiological data and Kazakhstan-specific statistics to build the motivation slide. Do NOT claim deployment outcomes — frame as screening need vs. clinical capacity gap per DGL-4.

---

### Slide 3 — Problem Statement

**Content:** Fundus image variability, device diversity, the preprocessing-as-ancillary gap.

**Files to load:**
- `thesis/governance/HYPOTHESIS.md` — *Premises 1–3* — for the causal argument (domain variability → distribution shift → degraded CNN)
- `thesis/governance/INVARIANTS.md` — *Section I: IT-1* — for the scope-bounded problem statement
- `thesis/methods/preprocessing-pipeline.md` — *"Design Principle" section* — for the `model = preprocessing + CNN` formalization
- `thesis/literature/external/voets-2019.md` — *Section 4 (Key Findings)* — for evidence of cross-dataset performance degradation
- `thesis/literature/external/liu-2022.md` — *Section 4 (Key Findings)* — for device-specific variability evidence (DeepDRiD benchmark)

**Instructions to Claude:** Frame the problem as the three-step causal chain from HYPOTHESIS.md Premises 1–3. Cite Voets 2019 and Liu 2022 as evidence of the problem. Introduce the gap: most systems treat preprocessing as ancillary.

---

### Slide 4 — Research Goal and Objectives

**Content:** Overarching goal + specific research tasks.

**Files to load:**
- `thesis/governance/CORE_OBJECTIVE.md` — *full file* — the canonical goal statement
- `thesis/experiments/experimental-protocol.md` — *"Research Objective" section + Experiment-to-Argument Mapping table* — for the task breakdown
- `thesis/governance/CONTRIBUTIONS.md` — *Primary Contributions section* — to ensure objectives align with claimed contributions

**Instructions to Claude:** Decompose the CORE_OBJECTIVE into 6 specific tasks matching the 5 active experiments + the pipeline design task. Each task should map to a hypothesis (H-1 through H-6).

---

### Slide 5 — Research Object and Subject

**Content:** Object = automated DR diagnosis process; Subject = image enhancement + CNN methods.

**Files to load:**
- `thesis/governance/CENTRAL_THESIS.md` — *full file* — for the exact thesis scope
- `thesis/governance/INVARIANTS.md` — *Section I: scope boundary paragraph* — for what the subject does NOT cover
- `thesis/outline/TABLE_OF_CONTENTS_EN.md` — for the Introduction section structure showing Object and Subject as formal entries

**Instructions to Claude:** Define the research object and subject in the formal Kazakh doctoral style (object = process being studied, subject = specific methods applied). Keep tightly bounded to INVARIANTS scope.

---

### Slide 6 — Scientific Novelty

**Content:** The six novel elements of the dissertation.

**Files to load:**
- `thesis/governance/CONTRIBUTIONS.md` — *full file* — the authoritative contributions register (C-1 through C-3, SC-A through SC-F)
- `thesis/methods/preprocessing-pipeline.md` — *V4 Pipeline Stages section* — for the pipeline novelty details (Stage 0, Stage 2 as new, Stage 3 upgraded)
- `thesis/governance/HYPOTHESIS.md` — *H-5 definition* — for ALO as a novel metric

**Instructions to Claude:** Present exactly 6 novelty elements derived from CONTRIBUTIONS.md. Map each to its evidence base. Use the formal novelty language expected in Kazakh doctoral defenses.

---

### Slide 7 — Central Hypothesis and Decomposition

**Content:** Central hypothesis + H-1 through H-6 tree.

**Files to load:**
- `thesis/governance/HYPOTHESIS.md` — *full file* — the authoritative hypothesis decomposition with argument structure
- `thesis/governance/INVARIANTS.md` — *Section II: Core Hypotheses* — for the operational form of each hypothesis with IV/DV/control specifications

**Instructions to Claude:** Present the central unifying hypothesis, then decompose into H-1 through H-6 as a visual tree. Note H-3 is DROPPED. For each hypothesis, include the one-line operational summary from HYPOTHESIS.md.

---

## SESSION B — Literature + Methodology (Slides 8–12)

### Slide 8 — Review of Existing Approaches

**Content:** Landscape of prior work + key gap identification.

**Files to load:**
- `thesis/literature/LITERATURE_INDEX.md` — *Source Index table* — for the full source landscape with key results
- `thesis/literature/external/gulshan-2016.md` — *Section 4 (Key Findings) + Section 8 (Limitations)* — Gulshan 2016 (AUC 0.991)
- `thesis/literature/external/ting-2017.md` — *Section 4 + Section 8* — Ting 2017 (10 datasets, AUC 0.936)
- `thesis/literature/external/rakhlin-2017.md` — *Section 4* — Rakhlin 2017 (Kaggle 2nd place)
- `thesis/literature/external/saxena-2020.md` — *Section 4 + Section 13 (Gaps)* — Saxena 2020 (cross-dataset AUC 0.958)
- `thesis/literature/external/senapati-2024.md` — *Section 4 + Section 13* — for field landscape and gap identification

**Instructions to Claude:** Create a compact "prior work landscape" table with 4–5 landmark systems (Gulshan, Ting, Rakhlin, Saxena + one recent). Then state the gap: systematic preprocessing validation and cross-device robustness are underexplored.

---

### Slide 9 — Proposed Model: The Central Design Decision

**Content:** The `model = preprocessing + CNN` formalization with diagram.

**Files to load:**
- `thesis/methods/preprocessing-pipeline.md` — *"Design Principle" + "Assertion"* — the core `model = preprocessing + CNN` framing
- `thesis/governance/CENTRAL_THESIS.md` — *full file* — the thesis formulation embedding the two-stage system
- `thesis/methods/implementation.md` — *Section 3: "Model Definition"* — the `model = V4_preprocessing + CNN_classifier` specification with architecture table

**Instructions to Claude:** This is the dissertation's central intellectual contribution. Present a clear two-stage diagram with the pipeline as "Stage 1" and the CNN as "Stage 2." Emphasize: preprocessing *defines the feature space*, it is not external data prep. Quote the Assertion from preprocessing-pipeline.md.

---

### Slide 10 — V4 Preprocessing Pipeline Architecture

**Content:** Visual diagram of all 6 stages with active/baseline definitions.

**Files to load:**
- `thesis/methods/preprocessing-pipeline.md` — *full file* — the authoritative V4 pipeline specification
- `experiments/CLAUDE.md` — *"V4 Preprocessing Pipeline" section* — the implementation-level stage descriptions
- `experiments/src/preprocessing/pipeline_v4.py` — *full file* — the actual pipeline code showing execution order
- `experiments/src/preprocessing/config.py` — *PIPELINE_PRESETS dict* — for the "resnet" vs "efficientnet" preset differences

**Instructions to Claude:** Create a pipeline flow diagram showing: Stage 0a → 0b → 1 → 2 → 3 → [5 train only] → 4. Mark each stage as "toggleable" or "always on." Show the baseline path (Stages 1+4 only) vs. full path. Include the resnet/efficientnet preset differences.

---

### Slide 11 — CLAHE Mathematical Formalization

**Content:** Dual-constraint formula, stochastic application, LAB processing.

**Files to load:**
- `thesis/methods/implementation.md` — *Section 4: "CLAHE Configuration"* — parameter table and theoretical reference
- `thesis/methods/preprocessing-pipeline.md` — *"Stage 3 — Upgraded CLAHE" subsection + "Upgraded CLAHE Modifications (V4)" section* — the four V4 upgrades
- `experiments/src/preprocessing/upgraded_clahe.py` — *full file* — the implementation with ClaheParams dataclass and dual-constraint formula
- `thesis/governance/INVARIANTS.md` — *DGL-5* — for the parameter portability constraint

**Instructions to Claude:** Present the formula `CL = min(clip_factor × tile_area/256, global_threshold × tile_area)` prominently. Show the four V4 upgrades over V3. Note the stochastic 80% train-time application as regularization. Reference LC-AlTimemy-2021 T/80 as theoretical origin.

---

### Slide 12 — CNN Architectures

**Content:** ResNet-50 vs. EfficientNet-B3 + training configuration.

**Files to load:**
- `thesis/methods/implementation.md` — *Section 3: "CNN Architectures" table + Section 5: "Training Configuration"* — architecture roles and training params
- `experiments/src/models/resnet.py` — *full file* — ResNet-50 implementation
- `experiments/src/models/efficientnet.py` — *full file* — EfficientNet implementation
- `experiments/CLAUDE.md` — *"Hardware Constraints" section* — for the actual training configuration including the fp16 fix

**Instructions to Claude:** Present ResNet-50 (residual connections, 2048-dim features) and EfficientNet-B3 (compound scaling) side by side. Show the standardized training config: Adam lr=1e-4, batch 16, 20 epochs, early stopping patience=5. Note: mixed precision disabled for EfficientNet due to fp16 overflow.

---

## SESSION C — Datasets + Experimental Design (Slides 13–19)

### Slide 13 — Dataset Architecture

**Content:** 7-dataset tiered architecture with roles and camera metadata.

**Files to load:**
- `thesis/experiments/experimental-protocol.md` — *Section 1: "Datasets" table* — role assignments
- `experiments/configs/default.yaml` — *"paths" section + "subset" section* — actual dataset paths and 40% subset config
- `thesis/governance/INVARIANTS.md` — *DGL-1* — dataset-bound generalization constraint
- `experiments/src/data/label_harmonization.py` — *get_dataset_camera_groups() function* — camera-to-dataset mapping
- `thesis/literature/LITERATURE_INDEX.md` — *entries for IDRiD (#06/#10), RFMiD (#49), DDR (#50), ODIR-5K (#51)* — dataset descriptors

**Instructions to Claude:** Create a tiered table: Tier 1 (Training) = EyePACS 14,050 images; Tier 2 (Validation) = IDRiD 516 images; Tier 3 (Generalization) = Messidor/Messidor-2; Tier 4 (Device Shift) = RFMiD/DDR/ODIR-5K. Add camera hardware column: Canon (EyePACS, DDR, ODIR), Topcon (Messidor, RFMiD, DDR), Kowa (IDRiD, RFMiD), Zeiss (ODIR).

---

### Slide 14 — Experimental Design Overview

**Content:** Map of all active experiments linked to hypotheses.

**Files to load:**
- `thesis/experiments/experimental-protocol.md` — *Experiment-to-Argument Mapping table* — the definitive experiment-hypothesis linkage
- `thesis/governance/HYPOTHESIS.md` — *H-1 through H-6 one-line summaries* — for the hypothesis labels
- `thesis/governance/ARGUMENT_MAP.md` — *first 100 lines* — for the PC-1 through PC-9 claim structure (trim to fit)

**Instructions to Claude:** Create a visual map: 5 active experiments (Exp 1, 2, 4, 5, 6) each linked by arrows to their hypotheses (H-1 through H-6) and primary claims (PC-1 through PC-9). Mark Exp 3 as DROPPED. Show the causal chain: Problem → Solution → Evidence.

---

### Slide 15 — Experiment 1: Factorial Design

**Content:** 6-configuration table, dominance criterion, CV protocol.

**Files to load:**
- `thesis/experiments/experimental-protocol.md` — *Section 4: "Experiment 1"* — factorial design specification
- `experiments/src/experiments/exp1_factorial.py` — *_CONFIGS dict + dominance test logic* — implementation-level config definitions
- `experiments/src/evaluation/metrics.py` — *check_dominance() function* — the EH-3 criterion implementation
- `thesis/governance/INVARIANTS.md` — *EH-3 and EH-4* — the dominance and sufficient validation criteria

**Instructions to Claude:** Present the 6-config table (A–F). Highlight the EH-3 dominance criterion (all three must hold: ΔF1 ≥ 5pp, ΔAUC ≥ 0.02, Δκ ≥ 0). Note: 3-fold patient-level CV, seed=42, no patient leakage. Configs E–F are optional extensions.

---

### Slide 16 — Experiment 2: Ablation + CLAHE Sensitivity

**Content:** V4 ablation levels, image quality metrics, CLAHE sweep design.

**Files to load:**
- `thesis/experiments/experimental-protocol.md` — *Section 5: "Experiment 2" + Section 11: "Image Quality"* — ablation design and IQ metrics
- `thesis/governance/HYPOTHESIS.md` — *H-2 definition* — CLAHE sensitivity hypothesis
- `thesis/governance/CONTRIBUTIONS.md` — *SC-A and SC-B entries* — the contributions this experiment supports

**Instructions to Claude:** Show the 7-row V4 ablation table (baseline → +flip → +flip+rotation → +flat-field → +CLAHE → +augmentation → full). List the 4 image quality metrics (CNR, VVI, Entropy, SSIM). Show the CLAHE parameter sweep grid on IDRiD.

---

### Slide 17 — Experiment 4: Grad-CAM Explainability

**Content:** Grad-CAM protocol, ALO/IoU definitions, lesion types.

**Files to load:**
- `thesis/experiments/experimental-protocol.md` — *Section 7: "V4 Experiment 4"* — full explainability protocol
- `thesis/methods/implementation.md` — *Section 7: "Grad-CAM Explainability"* — ALO and IoU formulas
- `experiments/src/explainability/iou.py` — *compute_alo() and compute_iou() functions* — implementation
- `thesis/governance/INVARIANTS.md` — *NC-14* — the critical non-claim (Grad-CAM ≠ clinical localization)

**Instructions to Claude:** Present ALO formula prominently: `ALO = area(GradCAM ∩ lesion) / area(lesion)`. Show the comparison protocol: baseline vs. preprocessed models on IDRiD, 10 images × 5 classes × 4 lesion types. State NC-14 explicitly as a boundary.

---

### Slide 18 — Experiments 5 & 6: Generalization + Device Shift

**Content:** Zero-shot transfer protocol, G ≥ 0.85 criterion, camera mapping.

**Files to load:**
- `thesis/experiments/experimental-protocol.md` — *Section 8: "V4 Experiment 5" + Section 8b: "V4 Experiment 6"* — both protocols
- `thesis/governance/HYPOTHESIS.md` — *H-4 and H-6 definitions* — the two generalization hypotheses
- `experiments/src/data/label_harmonization.py` — *get_dataset_camera_groups()* — camera → dataset mapping
- `thesis/governance/INVARIANTS.md` — *NC-16* — device results ≠ device certification

**Instructions to Claude:** Present Exp 5 (H-4: G = F1_ext / F1_EyePACS ≥ 0.85 on Messidor-2 and IDRiD) and Exp 6 (H-6: cross-device variance on RFMiD/DDR/ODIR across Canon/Topcon/Kowa/Zeiss) as linked but distinct experiments. Emphasize: zero-shot transfer, no retraining.

---

### Slide 19 — Evaluation Metrics Framework

**Content:** Complete metric hierarchy across all experiments.

**Files to load:**
- `thesis/experiments/experimental-protocol.md` — *Sections 3.1–3.6* — all metric categories
- `experiments/src/evaluation/metrics.py` — *full file* — primary, secondary, clinical metric implementations
- `experiments/src/evaluation/calibration.py` — *full file* — ECE and Brier score
- `experiments/src/evaluation/statistical_tests.py` — *(docstring listing all tests)* — test inventory

**Instructions to Claude:** Present as a 5-layer hierarchy: (1) Primary: Weighted F1, ROC-AUC, Cohen's κ, Accuracy; (2) Clinical: Sensitivity, Specificity, PPV, NPV for referable DR ≥ 2; (3) Calibration: ECE, Brier Score; (4) Explainability: ALO (primary), IoU (secondary); (5) Statistical: McNemar, DeLong, bootstrap CI, Holm-Bonferroni.

---

## SESSION D — Results + Discussion (Slides 20–22)

### Slide 20 — Experimental Results (Exp 1)

**Content:** Per-configuration metrics for A–D (and D pending folds).

**Files to load:**
- `experiments/outputs/backup_exp1_abc_40pct_20260324/metrics.csv` — *full file* — all training logs for configs A, B, C, D
- `experiments/logs/exp1_configD_40pct.log` — *full file* — Config D fold 0 + fold 1 start (best metrics visible)
- `experiments/logs/exp1_D_fold2.log` — *full file* — Config D fold 2 complete
- `experiments/logs/exp1_remaining.log` — *full file* — Configs A/B/C fold 2 results
- `experiments/logs/exp1_folds_1_2.log` — *full file* — additional fold logs
- `experiments/src/evaluation/metrics.py` — *check_dominance()* — to verify dominance calculations
- `thesis/governance/INVARIANTS.md` — *EH-3 criterion* — the dominance thresholds

**Instructions to Claude:** Compile the best-fold metrics into a summary table for configs A–D across 3 folds. Compute mean ± std for each config. Run the EH-3 dominance check (B vs A, D vs C). NOTE: Config C fold 2 and Config D fold 1 are missing — mark as "pending" and present partial results with appropriate caveats. Flag the EfficientNet overfitting pattern (train loss ~0.14, val loss ~2.6).

**⚠️ IMPORTANT:** If experiments are not yet complete at the time of slide creation, present available results with "[PENDING — N/3 folds complete]" annotations. Do NOT fabricate missing results.

---

### Slide 21 — Experimental Results (Exp 2, 4, 5–6)

**Content:** Component ablation, CLAHE sensitivity, ALO/IoU, generalization ratios.

**Files to load:**
- *No experimental result files exist yet for Experiments 2, 4, 5, 6 — these experiments have not been run.*
- `thesis/experiments/experimental-protocol.md` — *Sections 5, 7, 8, 8b* — experiment designs (for placeholder structure)
- `thesis/governance/HYPOTHESIS.md` — *H-2, H-4, H-5, H-6 definitions* — success criteria

**Instructions to Claude:** Create placeholder result tables with column headers and success criteria thresholds. Mark all cells as "[PENDING — experiment not yet run]". Structure: (a) V4 ablation table with 7 rows; (b) CLAHE sensitivity curve placeholder; (c) ALO/IoU comparison table (4 lesion types × baseline/preprocessed); (d) Generalization ratio table (Messidor-2, IDRiD, DDR) and cross-device matrix.

---

### Slide 22 — Discussion of Results

**Content:** Interpretation of findings, causal chain evaluation, benchmark comparison.

**Files to load:**
- `thesis/governance/HYPOTHESIS.md` — *Argument Structure section* — the causal chain to evaluate
- `thesis/governance/INVARIANTS.md` — *CFC-1: Permissible Claim Types + CFC-2: Forbidden Claims* — what the discussion CAN and CANNOT say
- `thesis/literature/LITERATURE_INDEX.md` — *entries for Gulshan (#12), Ting (#11), Saxena (#02), Liu (#15)* — benchmark comparison references
- `thesis/governance/CONTRIBUTIONS.md` — *Relationship to Primary Claims table* — contribution → evidence mapping

**Instructions to Claude:** Structure the discussion around three questions: (1) Is preprocessing dominance (H-1) supported? (2) Which pipeline stages contribute most? (3) Does the causal chain (preprocessing → feature visibility → classification) hold? Compare to published benchmarks (Gulshan AUC 0.991, Ting AUC 0.936) with appropriate caveats per CFC-2.2 (no superiority claims without direct comparison). If results are pending, state what WOULD be concluded under each outcome.

---

## SESSION E — Contributions + Conclusion (Slides 23–28)

### Slide 23 — Key Findings and Contributions

**Content:** 3 primary + 4 supporting contributions mapped to evidence.

**Files to load:**
- `thesis/governance/CONTRIBUTIONS.md` — *full file* — the authoritative contributions register
- `thesis/governance/ARGUMENT_MAP.md` — *first 150 lines* — PC-1 through PC-9 claim structure (trim for token budget)

**Instructions to Claude:** Present the 3 primary contributions (C-1: pipeline, C-2: cross-dataset, C-3: lesion attention via ALO) and the supporting contributions (SC-A: adaptive CLAHE, SC-B: CLAHE sensitivity, SC-C: cross-device robustness, SC-D: flat-field, SC-E: binocular fusion, SC-F: OD-fovea rotation). Map each to its experimental evidence and primary claims.

---

### Slide 24 — Theoretical and Practical Significance

**Content:** Theoretical formalization + practical deployment context.

**Files to load:**
- `thesis/governance/CONTRIBUTIONS.md` — *Novelty paragraphs under C-1, C-2, C-3* — for theoretical significance
- `thesis/governance/CORE_OBJECTIVE.md` — *full file* — for the "constrained computational conditions" framing
- `experiments/CLAUDE.md` — *"Hardware Constraints" section* — RTX 3060 12GB as representative of resource-limited hardware
- `thesis/literature/self/yesmukhamedov-nan-rk.md` — *Section 12 (Relevance)* — Kazakhstan healthcare infrastructure relevance
- `thesis/governance/INVARIANTS.md` — *DGL-4* — deployment constraints boundary

**Instructions to Claude:** Split into Theoretical (formalization of preprocessing dominance, ALO metric, dual-constraint CLAHE) and Practical (deployable on <16GB RAM, applicable to Kazakhstan's rural screening infrastructure). Caveat per DGL-4: system architecture is design specification, not field-tested.

---

### Slide 25 — Limitations and Boundary Conditions

**Content:** Comprehensive non-claims and scope boundaries.

**Files to load:**
- `thesis/governance/INVARIANTS.md` — *Section IV: Scope Boundaries (if present, else Section VI: CFC-2 Forbidden Claims + Section IX: DGL-1 through DGL-6)* — the full limitations framework
- `thesis/governance/CONTRIBUTIONS.md` — *"Boundary Conditions" section* — contribution-level boundaries

**Instructions to Claude:** Present 7–8 key limitations: (1) no SOTA claim (CFC-2.2), (2) no clinical certification (NC-16), (3) bounded to tested architectures and datasets (DGL-1), (4) calibration ≠ clinical reliability, (5) Grad-CAM is post-hoc interpretability not mechanistic explanation (NC-14), (6) no Kazakhstan field testing (DGL-4), (7) hardware-specific reproducibility (DGL-2), (8) CLAHE parameters not universally portable (DGL-5).

---

### Slide 26 — Future Work

**Content:** Kazakh clinical data, ViT architectures, OCT, deployment.

**Files to load:**
- `thesis/experiments/experimental-protocol.md` — *Section 10: "FUTURE WORK"* — Kazakh clinical validation protocol
- `thesis/governance/INVARIANTS.md` — *VCR-4* — extended contributions labeling rule
- `thesis/literature/external/goh-2024-vit-vs-cnn.md` — *Section 4 (Key Findings)* — ViT as future architecture direction
- `thesis/literature/external/ryu-2021-octa.md` — *Section 4* — OCT modality extension precedent

**Instructions to Claude:** Present 5 future directions: (1) Kazakh clinical validation with real-world data per Exp 7 protocol, (2) ViT architectures, (3) OCT modality, (4) clinical deployment prototype, (5) national eHealth platform integration. Frame each as an "extended contribution" per VCR-4.

---

### Slide 27 — Publications and Approbation

**Content:** 6 self-publications with key results.

**Files to load:**
- `thesis/literature/LITERATURE_INDEX.md` — *Self-Publication Registry table* — the publication list with DOIs
- `thesis/literature/self/yesmukhamedov-conf.md` — *Sections 1, 4, 12* — conference proceedings
- `thesis/literature/self/yesmukhamedov-kazutb.md` — *Sections 1, 4, 12* — KazUTB journal (laser-tissue)
- `thesis/literature/self/yesmukhamedov-kbtu.md` — *Sections 1, 4, 12* — KBTU journal
- `thesis/literature/self/yesmukhamedov-nan-rk.md` — *Sections 1, 4, 12* — NAS RK journal (system architecture)
- `thesis/literature/self/yesmukhamedov-scopus-q2.md` — *Sections 1, 4, 12* — Scopus Q2
- `thesis/literature/self/yesmukhamedov-scopus-q3.md` — *Sections 1, 4, 12* — Scopus Q3
- `thesis/governance/INVARIANTS.md` — *SIR-4 and SIR-5* — self-citation transparency and non-aggregation rules

**Instructions to Claude:** Present as a numbered publication list: venue, year, DOI, key result, and which dissertation claim each supports. Flag #23/#24 as the same article (duplicate DOI). Note CONF and KBTU share the same experiment per SIR-5 (not independent confirmation). Identify 2 Scopus-indexed + 1 conference + 3 other.

---

### Slide 28 — Thank You / Q&A

**Content:** Closing slide.

**Files to load:**
- *No governance files needed.*

**Instructions to Claude:** Generate a clean closing slide with: candidate name, email placeholder, GitHub repository links (yesmukhamedov/dissertation, yesmukhamedov/dr-classifier), and "Thank you — questions welcome." Keep minimal.

---

## Quick Reference: Files by Frequency of Use

| File | Slides Used In |
|------|---------------|
| `thesis/governance/INVARIANTS.md` | 2, 3, 5, 7, 11, 13, 15, 17, 18, 20, 22, 24, 25, 26, 27 |
| `thesis/governance/HYPOTHESIS.md` | 3, 7, 14, 16, 17, 18, 21 |
| `thesis/governance/CONTRIBUTIONS.md` | 4, 6, 16, 23, 25 |
| `thesis/governance/CENTRAL_THESIS.md` | 1, 5, 9 |
| `thesis/governance/CORE_OBJECTIVE.md` | 1, 4, 24 |
| `thesis/experiments/experimental-protocol.md` | 4, 13, 14, 15, 16, 17, 18, 19, 21, 26 |
| `thesis/methods/preprocessing-pipeline.md` | 3, 6, 9, 10, 11 |
| `thesis/methods/implementation.md` | 11, 12, 17 |
| `experiments/CLAUDE.md` | 10, 12, 24 |
| `thesis/literature/LITERATURE_INDEX.md` | 8, 13, 27 |
| `experiments/outputs/backup_exp1_abc_40pct_20260324/metrics.csv` | 20 |

---

## Token Budget Notes

- **INVARIANTS.md** is 42KB (~12K tokens). For most slides, load only the cited section (lines given above), not the full file.
- **ARGUMENT_MAP.md** is 59KB (~17K tokens). Only load for Slides 14 and 23, and only the first ~150 lines.
- **Literature cards** are 7–37KB each. Load only Sections 1, 4, 8, 12, 13 (Bibliographic, Key Findings, Limitations, Relevance, Gaps) — skip the full 18-section cards.
- **Source code files** are generally 3–17KB. Load full files for short modules (metrics.py, iou.py, config.py); load only key functions for large files (exp1_factorial.py, trainer.py).
- **Aim for ~35K–50K tokens of context per session** to leave room for Claude's response.
