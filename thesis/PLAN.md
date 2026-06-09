# MASTER WRITING PLAN — Dissertation, Section by Section

**Document type:** Execution plan (the live to-do board for drafting the entire dissertation)
**Candidate:** Yesmukhamedov N.S.
**Compiled:** 2026-06-09
**Grounded in:**
- `thesis/ASSET_INVENTORY.md` (resource IDs, real-vs-demo provenance, §2 reconciliation table)
- `thesis/governance/` v6.0.0 (INVARIANTS, HYPOTHESIS, ARGUMENT_MAP, RESEARCH_ARCHITECTURE, CONTRIBUTIONS)
- `thesis/prompts/` v6.0.0 pipeline (`section-brief-template.md`, `writing-session-system-prompt.md`, `verification-protocol.md`, `continuity-note-template.md`)
- `thesis/outline/MASTER_OUTLINE.md` (§-level content spec) reconciled to the **v6.0.0 Section Map Key** in `thesis/literature/LITERATURE_INDEX.md` (authoritative numbering)
- `thesis/literature/LITERATURE_INDEX.md` Coverage Matrix (literature-card IDs per section)

> **Scope of this document:** This is the plan only. **No chapter draft is written here.** Drafting begins only after the candidate reviews and approves this plan.

---

## 0. How to read this plan

1. **Progress Tracker (§1)** is the master checklist — every section with a live status box. Update it as you go.
2. **Phasing (§2)** orders the work by *data-readiness*: what is writable now vs. what is gated on experiment execution, with the exact unblocking resource IDs.
3. **Resource Honesty Policy (§3)** is the binding rule that decides whether a section may be drafted at all.
4. **Section Task Tables (§4–§9)** give, for every `§x.x.x`: target word count, governance bindings, literature-card IDs, the figure/table Resource IDs it must reference, and the ✅/⛔ verdict.
5. **Per-Section Execution Loop (§10)** is the exact a–f procedure to run for each *writable* section.
6. **Final Assembly (§11, Phase 3)** is the LAST step — concatenate, resolve placeholders, convert to `.docx`. It depends on Phase 2 completion.

**Literature-card IDs** are given as `#NN`, matching the Source Index numbers in `LITERATURE_INDEX.md` (e.g. `#12` = `gulshan-2016.md`; `#19–#24` = self-publications in `literature/self/`). **Resource IDs** (`FIG-x.x`, `TAB-x.x`, `RES-*`, `DIA-*`, `APP-*`) match `ASSET_INVENTORY.md §2`.

**Status legend (per-section):**
- ⬜ not started · 🟦 brief done · 🟩 draft done · ✅ verified (APPROVED by verification-protocol)

**Writability flag (per-section):**
- ✅ **writable-now** — every result-dependent resource it needs is `✅ AVAILABLE` or literature-derived; safe to draft.
- ⛔ **blocked-by-[ID]** — requires a resource that is `❌ MISSING (real result)`; stays blocked until the experiment is run.
- ⚠️ **writable-now (deferred asset)** — prose is writable now; a *conceptual/UML diagram* it references is not yet drawn (not experiment-gated). The diagram is queued as an asset task and inserted as a `TO BE CREATED` placeholder — see §3.2.

---

## 1. PROGRESS TRACKER (live to-do board)

> Update the status box (⬜/🟦/🟩/✅) after each pipeline stage. "Flag" column repeats the writability verdict for at-a-glance triage.

### Phase 1 — writable now

**Chapter 1 — Problem Domain**
- [x] ✅ §1.1.1 Pathophysiology and Clinical Grading Systems — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.1.2 Screening Requirements in Resource-Limited Healthcare Settings — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.2.1 Sources of Image Degradation in Clinical Practice — ✅ verified (APPROVED 2026-06-09; lit-GAP candidate analysis; brief/draft/continuity/review saved)
- [x] ✅ §1.2.2 Impact of Image Quality on Diagnostic Model Performance — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.2.3 Device-Specific Variability in Fundus Imaging — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; flagged: #47/#49/#50/#51 lack card files)
- [x] ✅ §1.3.1 CNN Architectures for Medical Imaging — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.3.2 Transfer Learning and SSL in Ophthalmic Diagnostics — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.3.3 Explainability Methods in Medical Image Classification — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.4 Critical Analysis of Existing Automated DR Screening Systems — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; TAB-1.1 rendered inline)
- [x] ✅ §1.5 Formulation of the Research Problem — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.C Conclusions to Chapter 1 — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved) — **Chapter 1 COMPLETE**

**Chapter 2 — Theoretical Foundations**
- [x] ✅ §2.1.1 Histogram Equalization and Adaptive Contrast Enhancement — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; FIG-2.1 deferred → asset queue; #23 card integrity flag noted)
- [x] ✅ §2.1.2 Formalization of CLAHE with Dual-Constraint Clip Limit — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; TAB-2.1 inline; Eqs. 2.1–2.3; resolves glossary clip-limit/tile-grid flags)
- [x] ✅ §2.1.3 Spatial Filtering and Noise Reduction Methods — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; bilateral/NLM as backdrop, V5 non-adoption framed)
- [x] ✅ §2.2.1 Convolution, Pooling, and Feature Extraction Operations — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; FIG-2.2 referenced; CFC-2.8 pre-honored via #08 counter-position)
- [x] ✅ §2.2.2 Loss Functions and Optimization for Imbalanced Medical Datasets — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; SIR-5 #19/#21 one thread, SIR-7 honored; focal-loss source gap flagged → §3.3.4)
- [x] ✅ §2.2.3 Regularization Techniques — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; augmentation dual-role → V5 Stage 6/OD-3; SIR-5/SIR-7 honored)
- [x] ✅ §2.3.1 Feature Transferability Across Visual Domains — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; DGL-6 two regimes; §2.3.3 SSL theory named-only/deferred; CFC-2.8 neutrality)
- [x] ✅ §2.3.2 Frozen-Layer vs Progressive Fine-Tuning Strategies — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; glossary fine-tuning disambiguation; SIR-5/SIR-7/CFC-2.8; hands off to §2.4.1)
- [ ] ⏸️ §2.3.3 In-Domain Self-Supervised Pretraining for Retinal Imaging (NEW v6.0.0) — **DEFERRED (candidate directive 2026-06-09): hold until in-domain SSL cards (DINO/BYOL/SimCLR/MoCo-on-fundus) are acquired; #73 general survey only.** Named-only in §2.3.1/§2.3.2; to be drafted after SSL acquisition.
- [x] ✅ §2.4.1 Coupled Thermal-Optical Model of Fundus Tissue Response — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; Eqs. 2–5,7,8; simulation-only bounding SB-1.5/SIR-6/CFC-2.4; THIN #20-self; FIG-2.4 deferred → asset queue)
- [x] ✅ §2.5.1 CAM / Grad-CAM Theory and Formalization — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; CAM/Grad-CAM/Grad-CAM++ eqs; NC-14 central; FIG-2.3 deferred; #46 Selvaraju card absent/index-only — flagged)
- [x] ✅ §2.5.2 Attention Map Interpretation — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; NC-14 reinforced; interpretation bounded to attention-plausibility)
- [x] ✅ §2.5.3 ALO and IoU as Quantitative Explainability Metrics — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; ALO primary/IoU secondary eqs; IoU borrowed-not-benchmark; NC-14)
- [x] ✅ §2.6 Image Quality Metrics for Preprocessing Evaluation — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; CNR/VVI/Entropy/SSIM; THIN/SIR-1 flagged; EH-2; FIG-2.5 deferred → asset queue; TAB-3.3 referenced)
- [x] ✅ §2.C Conclusions to Chapter 2 — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; experimentally-grounded vs simulation-only partition; §2.3.3 deferral noted) — **Chapter 2 COMPLETE except deferred §2.3.3**

**Chapter 3 — Methodology (fully unblocked)**
- [x] ✅ §3.1.1 Pipeline Stage Specification: V5 8-Stage System — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; Stage-1 RES-VAL honesty disclosure + Stage-7 RES-NORM grounded; P2/P1 framing; ~2,030 w)
- [x] ✅ §3.1.2 Upgraded CLAHE with Dual-Constraint Clip Limit — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; realizes §2.1.2 rule; FIG-3.7 polar variant tied to §3.1.1 fovea finding; [VERIFY] Stage-5 governance divergence; ~1,010 w)
- [x] ✅ §3.1.3 Augmentation Strategy for Class Imbalance Mitigation — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; real RES-PCA basis interpreted; dual role SC-1.4 one of two levers; ~915 w)
- [x] ✅ §3.1.4 External Image Ingestion Protocol — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; lit-GAP candidate contribution; NC-15 bound, 1 intentional [UNSOURCED CLAIM]; ~790 w) — **§3.1 COMPLETE**
- [x] ✅ §3.2.1 ResNet-50 and EfficientNet-B3 as Primary Architectures — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; two-family EH-4 rationale; CNN-centred/AOQ-2; SB-3.1/NC-6/SIR-7; ~1,015 w)
- [x] ✅ §3.2.2 Historical v1.0 Architectures (Reference Only) — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; OD-2 references; SIR-4/5/7; reference-only; ~600 w) — **§3.2 COMPLETE**
- [x] ✅ §3.3.1 Architecture Adaptation for Five-Class DR Classification — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; 5-way softmax head; identical adaptation → EH-4; DGL-6/SIR-7; ~690 w)
- [x] ✅ §3.3.2 Ophthalmology-Specific Self-Supervised Pretraining (NEW v6.0.0) — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; CFC-2.8 composite IV central; lit-GAP #73-only flagged + 1 [UNSOURCED CLAIM]; spec-not-result, SSL arm untrained; ~1,000 w)
- [x] ✅ §3.3.3 Two-Stage Fine-Tuning Protocol Design — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; H-3-dropped training-method framing; SIR-4/5/7; identical schedule→EH-4; ~660 w)
- [x] ✅ §3.3.4 Weighted Loss Function Formulation — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; focal loss γ=2 inverse-freq; SC-1.4 principal lever; κ ordinal tie; focal-loss source gap [VERIFY]; ~700 w) — **§3.3 COMPLETE**
- [x] ✅ §3.4.1 Multi-Metric Assessment Framework — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; TAB-3.2 + TAB-3.3 inline & interpreted; EH-1/2, OD-4/5, NC-14, SB-1.10; ~1,210 w)
- [x] ✅ §3.4.2 Cross-Validation and Statistical Reliability Protocols — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; patient-level 5-fold CV + test suite; TAB-3.1 inline; EH-3/4 restated; DGL-2/SB-2.2; ~1,000 w) — **§3.4 COMPLETE**
- [x] ✅ §3.C Conclusions to Chapter 3 — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; synthesis, no new claims; reproducibility + bounded commitments consolidated; ~560 w) — **Chapter 3 COMPLETE**

**Chapter 6 — System Architecture (design-only)**
- [ ] ⬜ §6.1.1 Functional and Non-Functional Requirements — ✅
- [ ] ⬜ §6.1.2 Modular Architecture with PACS and EHR Integration — ⚠️ (DIA-6.3 UML deferred)
- [ ] ⬜ §6.2.1 Preprocessing Engine with Configurable Pipeline — ✅
- [ ] ⬜ §6.2.2 Inference Module with Model Selection Logic — ✅ (design-only; no Exp-6 numbers)
- [ ] ⬜ §6.3.1 Telemedicine and Portable Device Support (incl. 6.3.1.1–6.3.1.3) — ✅
- [ ] ⬜ §6.3.2 Physician-in-the-Loop Decision Support Interface — ✅
- [ ] ⬜ §6.4.1 GDPR/HIPAA-Aligned Data Management Protocols — ✅
- [ ] ⬜ §6.4.2 Applicability to Kazakhstan Healthcare Infrastructure — ✅
- [ ] ⬜ §6.C Conclusions to Chapter 6 — ✅

**Chapter 4 — §4.1 only (Datasets & Configuration)**
- [ ] ⬜ §4.1.1 Dataset Architecture V5 — ✅
- [ ] ⬜ §4.1.2 Class Distribution Analysis and Data Partitioning — ✅
- [ ] ⬜ §4.1.3 Hardware Specification and Reproducibility Protocol — ✅

**Appendices writable now**
- [ ] ⬜ App A — Source Code of the Preprocessing Pipeline — ✅
- [ ] ⬜ App D — Certificates and Publication Confirmations — ✅

### Phase 2 — blocked, gated on experiment execution

**Chapter 4 — Experiments (results)**
- [ ] ⬜ §4.2.1 Factorial Design (Configs A–D) — 🟨 design-writable; grouped under Exp 1 (see §5.1)
- [ ] ⬜ §4.2.2 Training Dynamics and Convergence Analysis — ⛔ blocked-by RES-EXP1(full), FIG-4.5, TAB-4.3
- [ ] ⬜ §4.2.3 Quantitative Comparison of Diagnostic Metrics — ⛔ blocked-by TAB-4.2, FIG-4.4, FIG-4.6, FIG-4.7, FIG-4.8
- [ ] ⬜ §4.3.1 V5 Ablation Design (Levels 0–6) — ⛔ blocked-by TAB-4.4
- [ ] ⬜ §4.3.2 CLAHE Threshold Sensitivity Analysis (H-2) — ⛔ blocked-by FIG-4.9
- [ ] ⬜ §4.3.3 Feature Preservation + σ Sweep + Image Quality — ⛔ blocked-by FIG-4.10, TAB-4.5
- [ ] ⬜ §4.4.1 Zero-Shot Transfer to APTOS 2019 — ⛔ blocked-by TAB-4.6
- [ ] ⬜ §4.4.2 Baseline vs V5 Pipeline Comparison — ⛔ blocked-by FIG-4.11
- [ ] ⬜ §4.5.1 Grad-CAM Generation Protocol — ⛔ blocked-by FIG-4.12
- [ ] ⬜ §4.5.2 Quantitative ALO and IoU with IDRiD Lesion Masks — ⛔ blocked-by TAB-4.7, FIG-4.14
- [ ] ⬜ §4.5.3 Attention Consistency Across Datasets — ⛔ blocked-by FIG-4.13
- [ ] ⬜ §4.6 Experiment 5 — Clinical Degradation Resistance (H-7) — ⛔ blocked-by TAB-4.8, FIG-4.15
- [ ] ⬜ §4.7 Experiment 6 — Device Domain Shift (H-6) — ⛔ blocked-by TAB-4.9
- [ ] ⬜ §4.8 Experiment 7 — Small Data Training — ⛔ blocked-by TAB-4.10, FIG-4.16
- [ ] ⬜ §4.C Conclusions to Chapter 4 — ⛔ blocked-by (all of §4.2–§4.8)

**Chapter 5 — Validation**
- [ ] ⬜ §5.1 Explainability Results — ⛔ blocked-by FIG-5.1, TAB-4.7, FIG-4.12 (Exp 4)
- [ ] ⬜ §5.2.1 Bootstrap CI and Mixed-Effects Model — ⛔ blocked-by TAB-5.1
- [ ] ⬜ §5.2.2 Final Claim-Strength Classifications — ⛔ blocked-by TAB-5.2, FIG-5.3
- [ ] ⬜ §5.3.1 Benchmarking Against Published Systems — ⛔ blocked-by TAB-5.3, TAB-5.4
- [ ] ⬜ §5.3.2 Performance–Complexity Trade-Off Analysis — ⛔ blocked-by FIG-5.2
- [ ] ⬜ §5.4 Limitations and Boundary Conditions — ⛔ blocked-by (final H-1…H-7 outcomes)
- [ ] ⬜ §5.C Conclusions to Chapter 5 — ⛔ blocked-by TAB-5.2

**Chapter 0 — Introduction & Front Matter** (depends on all results being final)
- [ ] ⬜ §0.FM1 Normative References — 🟨 writable now (deferrable formatting)
- [ ] ⬜ §0.FM2 Definitions (OD-1…OD-6 verbatim) — 🟨 writable now
- [ ] ⬜ §0.FM3 Designations and Abbreviations — 🟨 writable now
- [ ] ⬜ §0.1 Relevance of the Research — 🟨 writable now (no results)
- [ ] ⬜ §0.2 Scientific Novelty — 🟨 writable now
- [ ] ⬜ §0.3 Research Goal — 🟨 writable now
- [ ] ⬜ §0.4 Research Objectives — 🟨 writable now
- [ ] ⬜ §0.5 Object and Subject of Research — 🟨 writable now
- [ ] ⬜ §0.6 Research Hypothesis (H-1…H-7 verbatim) — 🟨 writable now
- [ ] ⬜ §0.7 Methodological Basis — 🟨 writable now
- [ ] ⬜ §0.8 Provisions Submitted for Defense — ⛔ blocked-by (final claim strengths, §5.2.2)
- [ ] ⬜ §0.9 Theoretical Significance — 🟨 writable now
- [ ] ⬜ §0.10 Practical Significance — 🟨 writable now
- [ ] ⬜ §0.11 Approbation of Research Results — ✅ writable now (App D)
- [ ] ⬜ §0.12 Publications — ✅ writable now

**Chapter 7 — Conclusion** (depends on all chapters)
- [ ] ⬜ §7 Conclusion — ⛔ blocked-by (all of Ch 4 + §5.2.2)

**Appendices blocked**
- [ ] ⬜ App B — Confusion Matrices & Training Curves — ⛔ blocked-by FIG-4.6, FIG-4.5(full), TAB-4.3, App B set
- [ ] ⬜ App C — System Architecture UML Diagrams — ⛔ blocked-by DIA-6.3 (asset creation, not experiment-gated)
- [ ] ⬜ App E — Grad-CAM Visualization Gallery — ⛔ blocked-by FIG-5.1, FIG-4.12 (Exp 4)
- [ ] ⬜ App F — Device Domain-Shift Supplementary Tables — ⛔ blocked-by TAB-4.9, App F set (Exp 6)

### Phase 3 — final assembly
- [ ] ⬜ §11.1 Concatenate all approved drafts per MASTER_OUTLINE order
- [ ] ⬜ §11.2 Resolve every `[FIG/TAB]` placeholder to its real asset path
- [ ] ⬜ §11.3 Convert assembled Markdown → single `.docx`

---

## 2. PHASING BY DATA-READINESS

### Phase 1 — writable now (no real-result dependency)

Narrative order is fixed by the task:

> **Ch 1 (Problem Domain) → Ch 2 (Theoretical Foundations) → Ch 3 (Methodology, fully unblocked) → Ch 6 (System Architecture, design-only) → §4.1 (Datasets & Configuration).**

Rationale (from `ASSET_INVENTORY.md §1.3`): these chapters draw only on real artifacts already on disk — preprocessing stage renders (FIG-3.1…FIG-3.9), the OD/fovea validation (RES-VAL, FIG-3.10), norm-stats (RES-NORM), the PCA basis (RES-PCA), conceptual/architecture diagrams, dataset sample montages, the publication certificates (APP-D), and the literature corpus. No experimental *result* is required. App A (source code) and App D (certificates) are also writable now and are produced alongside Phase 1.

### Phase 2 — blocked, gated on experiment execution

Order (as instructed): **§4.2 → §4.3–§4.8 → Ch 5 → Ch 0 → Ch 7 → Appendices B/C/E/F.** For each, the exact missing Resource IDs (from `ASSET_INVENTORY.md §2`) that unblock it:

| Gate | Section(s) | Unblocking experiment | Missing Resource IDs that must become real |
|------|-----------|------------------------|--------------------------------------------|
| G-1 | §4.2.2, §4.2.3 (+ §4.C dependency) | **Exp 1** full A–D × 5-fold @100% incl. ophthalmology-SSL B/D arm + per-sample prediction dumps | TAB-4.2, FIG-4.4, FIG-4.5(full), FIG-4.6, FIG-4.7, FIG-4.8, TAB-4.3; RES-EXP1 upgraded ⏳→✅ |
| G-2 | §4.3.1–§4.3.3 | **Exp 2** (V5 ablation + CLAHE sweep + σ sweep + image-quality) | TAB-4.4, FIG-4.9, FIG-4.10, TAB-4.5 |
| G-3 | §4.4.1, §4.4.2 | **Exp 3** (APTOS 2019 zero-shot transfer, G ratio) | TAB-4.6, FIG-4.11 |
| G-4 | §4.5.1–§4.5.3 | **Exp 4** (Grad-CAM ALO/IoU on IDRiD + Clinical) | FIG-4.12, TAB-4.7, FIG-4.13, FIG-4.14 |
| G-5 | §4.6 | **Exp 5** (clinical degradation, IDRiD + Messidor-2) | TAB-4.8, FIG-4.15 |
| G-6 | §4.7 | **Exp 6** (device domain shift, DDR/ODIR-5K/RFMiD) | TAB-4.9, App F set |
| G-7 | §4.8 | **Exp 7** (small-data IDRiD → Clinical) | TAB-4.10, FIG-4.16 |
| G-8 | §4.C | All of Exp 1–7 | (all of the above) |
| G-9 | §5.1 | Exp 4 | FIG-5.1, TAB-4.7, FIG-4.12 |
| G-10 | §5.2.1 | Exp 1–7 statistical suite | TAB-5.1 |
| G-11 | §5.2.2 | All Exp + claim-strength derivation | TAB-5.2, FIG-5.3 |
| G-12 | §5.3.1 | Own results + Exp 1/3/5 | TAB-5.3, TAB-5.4 |
| G-13 | §5.3.2 | Exp 1/6 | FIG-5.2, FIG-5.4 |
| G-14 | §5.4, §5.C | Final H-1…H-7 verdicts | (none new; depends on §4.C + §5.2.2) |
| G-15 | §0.8, §7 | Final claim strengths | depends on §5.2.2 (TAB-5.2) |
| G-16 | App B | Exp 1–7 | FIG-4.6, FIG-4.5(full), TAB-4.3 + per-Exp confusion/curves |
| G-17 | App C | UML drawing (asset, not experiment) | DIA-6.3 |
| G-18 | App E | Exp 4 | FIG-5.1, FIG-4.12 |
| G-19 | App F | Exp 6 | TAB-4.9 + per-camera matrices |

> **Note on Exp 1 partial data:** `RES-EXP1` is `⏳ PENDING` — real per-epoch metrics exist for Config A f0, A/B/C f0–2 @40%, and a clean Config D f0 (EyePACS). These are **not** sufficient for §4.2: the headline 2×2 factorial table (TAB-4.2) and the EH-3 dominance verdict require the full 100% A–D × 5-fold run, and the v6.0.0 ophthalmology-SSL initialization for the V5 arm (B/D) has not been trained at all. Confusion matrices / ROC / calibration (FIG-4.6/4.7, TAB-4.3) are *not derivable* from current outputs because per-sample predictions were not saved (`ASSET_INVENTORY.md §3 note 3`). §4.2 therefore stays blocked.

### Phase 3 — final assembly (LAST step, depends on Phase 2 completion)

See §11.

---

## 3. RESOURCE HONESTY POLICY (binding)

### 3.1 Hard honesty rule

**A section may NEVER be drafted if any *result-dependent* resource it requires is `❌ MISSING (real result)` in `ASSET_INVENTORY.md`.** Such sections stay ⛔ blocked and are skipped until the experiment is run. Specifically:

- **No fabricated metrics.** No number may be written into a results table/figure unless it comes from a real, machine-produced artifact verified in `ASSET_INVENTORY.md §3`.
- **No demo-dashboard previews as if real.** The files in `demo/web/public/results/` and the preview JSONs (`exp3_aptos_transfer.json` G=0.890, `exp5_degradation.json`, `exp7_small_data.json`, `exp2_ff_sweep.json`) carry placeholder numbers authored for the dashboard. They are **demo assets**, not results, and must not be cited as evidence (per **CFC-2.x / SIR-1**, and the §0 Provenance Policy of the inventory).
- **CFC-2.8 reminder for §4.2 / H-1:** the V5 arm uses ophthalmology-SSL pretraining and the baseline uses ImageNet; once results exist, any difference is attributed to the **integrated configuration**, never to "preprocessing alone."

### 3.2 Conceptual / UML diagrams are *deferred assets*, not blockers

A resource that is `❌ MISSING` but is a **conceptual or architecture/UML diagram with no experimental dependency** (FIG-2.1, FIG-2.3, FIG-2.4, FIG-2.5, DIA-6.3 / App C) does **not** hard-block its section — the prose carries no fabricated data. For these:

- The section is **⚠️ writable-now (deferred asset)**.
- Insert the figure as a placeholder marked **TO BE CREATED**, e.g. `[FIG-2.1: Histogram equalization → CLAHE intensity redistribution — ASSET TO BE CREATED]`.
- Log the diagram in the asset-creation queue (it is resolved during Phase 3 §11.2, or earlier if drawn).
- This distinction is consistent with `ASSET_INVENTORY.md §1.3`, which lists Ch 2 and Ch 6 as writable-now despite these missing diagrams ("some diagrams reusable, others to draw"; Ch 6 "only blocker: UML").

This is the **only** relaxation of the hard rule. It applies to non-result diagrams exclusively. Any figure/table tied to an unrun experiment remains a hard block.

---

## 4. CHAPTER 1 — PROBLEM DOMAIN (Phase 1, ✅ writable)

**Chapter function:** establish clinical/epidemiological/technical context; identify the research gap. Tense: present (definitions) + past (cited findings). Chapter target ≈ 10,700 words.

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 1.1.1 | Pathophysiology & Clinical Grading Systems | 1,100–1,300 | OD (5-class grading defn); SIR-2; CFC-2.3 (no deployment outcomes) | #31, #32, #33, #34, #35 | FIG-1.1 ✅ |
| 1.1.2 | Screening in Resource-Limited Settings | 800–1,000 | SB-1.6, SIR-8 (epi. contextual, not results); SIR-4 (#22 self) | #06/#10, #22, #34 | — |
| 1.2.1 | Sources of Image Degradation | 700–900 | OD-1 (image-quality operational def); SIR-1 (lit-GAP → flag candidate analysis) | *(GAP — candidate analysis; no external card)* | — |
| 1.2.2 | Impact of Image Quality on Performance | 900–1,100 | OD-1; DGL-6; CFC-2.1 (no universal); SIR-4 (#24 self) | #05, #15, #17, #24, #78 | — |
| 1.2.3 | Device-Specific Variability | 800–1,000 | NC-16 foreshadow (≠ certification); SIR-3 (camera/dataset context) | #47, #49, #50, #51, #74, #75 | FIG-1.2 ✅ |
| 1.3.1 | CNN Architectures for Medical Imaging | 1,100–1,300 | SB-3.1, NC-6 (no architectural optimality); CFC-2.2 | #01, #04, #05, #08, #09, #12, #15, #16, #18, #37, #38, #41–#43, #65–#70 | FIG-2.2 (reuse) ✅ |
| 1.3.2 | Transfer Learning & SSL in Ophthalmics | 900–1,100 | DGL-6; CFC-2.9/SIR-9 (Gulshan paradigm practice only) | #02, #09, #12, #73 | — |
| 1.3.3 | Explainability Methods | 800–1,000 | NC-14 (Grad-CAM ≠ clinical localization) | #46, #57, #58, #59, #60, #61, #62 | — |
| 1.4 | Critical Analysis of Existing DR Systems | 1,400–1,600 | CFC-2.2, NC-2 (no superiority vs named systems); SB-1.12 (Gulshan not a benchmark); CFC-2.9/SIR-9; SIR-3 | #02, #03, #07, #11, #12, #14, #22, #39, #43, #44, #45, #77 | TAB-1.1 (lit-derived) |
| 1.5 | Formulation of the Research Problem | 700–900 | synthesis; align to CORE_OBJECTIVE; SIR-1 | #17, #39 | — |
| 1.C | Conclusions to Chapter 1 | 400–600 | synthesis; no new claims | — | — |

---

## 5. CHAPTER 2 — THEORETICAL FOUNDATIONS (Phase 1, ✅ writable; 4 deferred diagrams)

**Chapter function:** mathematical/theoretical grounding for Chs 3–4. Tense: present (definitions/derivations). Chapter target ≈ 13,000 words. Note `#25` (Wikipedia-CLAHE) is **not citable** — cite `#54` (Pizer 1987) instead.

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 2.1.1 | Histogram Equalization & Adaptive Contrast | 900–1,100 | SIR-4 (#23 self); #25 not citable→#54 | #26, #27, #30, #23, #54 | ⚠️ FIG-2.1 (deferred) |
| 2.1.2 | Formalization of CLAHE (Dual-Constraint Clip Limit) | 1,300–1,500 | DGL-5 (T/80 portability); SIR-3 (sensitivity-formula anomaly in #23/#24); CFC-2.5; SIR-4/SIR-5 (#23/#24 self+overlap). Eq.1, Eq.2 | #23, #24, #27, #54 | TAB-2.1 ✅ |
| 2.1.3 | Spatial Filtering & Noise Reduction | 600–800 | cite as algorithmic foundations, not DR gains | #55, #56 | — |
| 2.2.1 | Convolution, Pooling, Feature Extraction | 900–1,100 | GLOSSARY (CNN defn) | #08, #65, #66, #67 | FIG-2.2 ✅ |
| 2.2.2 | Loss Functions for Imbalanced Datasets | 900–1,100 | SIR-4/SIR-5 (#19/#21 overlap); SIR-7 (no efficient-CNN-class generalization) | #01, #19, #21, #39, #40, #42 | — |
| 2.2.3 | Regularization Techniques | 700–900 | OD-3 (augmentation operational def); SIR-4/5/7 | #01, #19, #21, #65 | — |
| 2.3.1 | Feature Transferability Across Domains | 700–900 | DGL-6 (transfer not guaranteed) | #04, #71, #72, #73 | — |
| 2.3.2 | Frozen-Layer vs Progressive Fine-Tuning | 700–900 | GLOSSARY (canonical fine-tuning terms); SIR-4/5 | #19, #21, #71, #72, #76 | — |
| 2.3.3 | In-Domain SSL for Retinal Imaging (NEW) | 800–1,000 | DGL-6; SIR-1 (lit-THIN → flag where primary SSL sources absent) | #73 *(THIN — acquire DINO/BYOL/SimCLR/MoCo-on-fundus)* | — |
| 2.4.1 | Coupled Thermal-Optical Model | 1,100–1,300 | SB-1.5, SIR-6, CFC-2.4 (simulation only, not clinical validation); SIR-4 (#20 self). Eq.1–8 | #20 *(self, THIN)* | ⚠️ FIG-2.4 (deferred) |
| 2.5.1 | CAM / Grad-CAM Formalization | 900–1,100 | NC-14. Grad-CAM eq. | #46, #57, #58 | ⚠️ FIG-2.3 (deferred) |
| 2.5.2 | Attention Map Interpretation | 600–800 | NC-14 | #46, #57, #58 | — |
| 2.5.3 | ALO (primary) & IoU (secondary) | 700–900 | define ALO primary / IoU secondary; frame IoU as borrowed overlap metric | #63, #64 | — |
| 2.6 | Image Quality Metrics (CNR/VVI/Entropy/SSIM) | 900–1,100 | SIR-1 (THIN; general refs, not DR-specific) | #52, #53 | ⚠️ FIG-2.5 (deferred); TAB-3.3 (defn) |
| 2.C | Conclusions to Chapter 2 | 400–600 | distinguish experimentally-grounded (§2.1–2.3,2.5–2.6) vs theoretical (§2.4) | — | — |

---

## 6. CHAPTER 3 — METHODOLOGY (Phase 1, ✅ fully unblocked)

**Chapter function:** specify all methodological decisions; make the framework reproducible. Tense: present. Chapter target ≈ 12,000 words. Every asset here is real and on disk (`ASSET_INVENTORY.md §2.3`).

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 3.1.1 | V5 8-Stage Pipeline Specification | 1,800–2,200 | OD defs; SIR-4/5 (self); model = preprocessing + CNN (CENTRAL_THESIS) | #19, #21, #23, #24, #02, #15, #26, #27, #53, #78 | FIG-3.1, FIG-3.2…FIG-3.9, FIG-3.10, FIG-3.14, RES-NORM, RES-VAL ✅ |
| 3.1.2 | Upgraded CLAHE (Dual-Constraint) | 900–1,100 | DGL-5; SIR-3 | #23, #24 | FIG-3.7 ✅ |
| 3.1.3 | Augmentation Strategy | 800–1,000 | OD-3; SC-1.4 (class dist.) | #19 (LC-CONF) | FIG-3.8, RES-PCA ✅ |
| 3.1.4 | External Image Ingestion Protocol | 700–900 | NC-15 (bound to Kazakh data); SIR-1 (candidate contribution) | *(GAP — candidate methodological contribution)* | — |
| 3.2.1 | ResNet-50 & EfficientNet-B3 | 900–1,100 | SB-3.1, NC-6, DGL-6 | #66, #68, #24, #09, #69, #70 | FIG-3.11, FIG-3.14 ✅ |
| 3.2.2 | Historical v1.0 Architectures (reference) | 500–700 | OD-2 (low/high-complexity reference); SIR-4 (#19) | #19 | — |
| 3.3.1 | Architecture Adaptation (5-class) | 600–800 | DGL-6; EH-4 (replication ≥ 2 architectures) | #19, #21, #23 | — |
| 3.3.2 | Ophthalmology-Specific SSL Pretraining (NEW) | 900–1,100 | DGL-6 (V5 arm = ophthalmology-SSL); CFC-2.8 (composite IV); SIR-1 (GAP) | #73 *(GAP — acquire SSL primary sources)* | — |
| 3.3.3 | Two-Stage Fine-Tuning Protocol | 600–800 | SIR-4/5; H-3 dropped (training method only) | #19, #21 | — |
| 3.3.4 | Weighted Loss Function Formulation | 600–800 | SC-1.4 (imbalance) | #21, #40 | FIG-3.12 ✅ |
| 3.4.1 | Multi-Metric Assessment Framework | 1,100–1,300 | EH-1, EH-2, OD-4, OD-5 | #21, #40, #52, #64 | TAB-3.2, TAB-3.3 ✅ |
| 3.4.2 | Cross-Validation & Statistical Reliability | 900–1,100 | EH-3, EH-4; multiple-comparison correction | #21 | FIG-3.13, TAB-3.1 ✅ |
| 3.C | Conclusions to Chapter 3 | 400–600 | confirm reproducibility conditions | — | — |

---

## 7. CHAPTER 6 — SYSTEM ARCHITECTURE (Phase 1, ✅ writable; design-only; 1 deferred UML asset)

**Chapter function:** translate (eventual) validated results into a design specification. **Epistemic status of entire chapter: design specification only — no prototype, no field test (SB-4.1).** Tense: present. Chapter target ≈ 7,200 words.

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 6.1.1 | Functional & Non-Functional Requirements | 800–1,000 | OD-6 (resource-limited def); SB-4.1; SIR-4 (#22 self) | #22 | — |
| 6.1.2 | Modular Architecture (PACS/EHR Integration) | 1,100–1,300 | SB-4.1; SC-5.1 (UML); SIR-4 (#22) | #22, #36 | DIA-6.1 ✅; ⚠️ DIA-6.3 (UML, deferred) |
| 6.2.1 | Preprocessing Engine (Configurable) | 800–1,000 | link to PC-1 (validated pipeline = module core); SB-4.1 | #22 | DIA-6.2 / reuse FIG-3.1 ✅ |
| 6.2.2 | Inference Module / Model Selection | 700–900 | **design-only — must NOT cite Exp-6 numbers**; SB-4.1; DGL-2 | #22 | FIG-6.1 ✅ |
| 6.3.1 | Telemedicine & Portable Support (6.3.1.1–.3) | 1,100–1,300 | SB-4.1, SB-4.3 (no field testing); SIR-8 (no projected outcomes as findings) | #22, #34, #44, #45, #11, #03, #14 | FIG-6.1 ✅ |
| 6.3.2 | Physician-in-the-Loop Interface | 600–800 | SB-1.3 (decision-support, not standalone) | #22, #34 | — |
| 6.4.1 | GDPR/HIPAA-Aligned Data Management | 600–800 | SB-4.2, NC-9 (design spec, not certified) | *(candidate design spec)* | — |
| 6.4.2 | Applicability to Kazakhstan Infrastructure | 600–800 | SB-4.3; SIR-8 | #22 | — |
| 6.C | Conclusions to Chapter 6 | 400–600 | reaffirm design-only status (SB-4.1) | — | — |

---

## 8. CHAPTER 4 — §4.1 DATASETS & CONFIGURATION (Phase 1, ✅ writable)

**Chapter function (this part only):** specify datasets, partitioning, hardware. Tense: present/past. Target ≈ 2,900 words. (The experiment sections §4.2–§4.8 are Phase 2 — see §9.)

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 4.1.1 | Dataset Architecture V5 | 1,100–1,300 | SIR-3 (dataset/taxonomy context); DGL-1 | #06/#10, #15, #47, #48, #49, #50, #51, #19, #21, #24, #41 | TAB-4.1, FIG-4.2, FIG-4.3 ✅ |
| 4.1.2 | Class Distribution & Data Partitioning | 900–1,100 | SC-1.4 (imbalance → weighted F1/κ); label harmonization | #06/#10, #24 | FIG-4.1 ✅ |
| 4.1.3 | Hardware & Reproducibility Protocol | 600–800 | DGL-2 (hardware-specific); fixed seeds/versioned code | #21 | TAB-3.1 ✅ |

---

## 9. CHAPTER 4 §4.2–§4.8, CHAPTER 5, CHAPTER 0, CHAPTER 7, APPENDICES (Phase 2, ⛔ blocked)

> These tables document the *intended* spec so a brief can be generated the moment the gating experiment completes. Each row's **Unblock** column repeats the missing Resource ID(s); until they flip `❌→✅` in the inventory, the section stays ⛔ and is skipped (§3.1).

### 9.1 Chapter 4 — Experiments (results)

| § | Title | Words | Governance bindings | Lit cards | Unblock (missing IDs) |
|---|-------|-------|---------------------|-----------|------------------------|
| 4.2.1 | Factorial Design (A–D) | 800–1,000 | EH-3; CFC-2.8 (composite IV) | #19, #21, #24 | *design-writable*; grouped under Exp 1 |
| 4.2.2 | Training Dynamics & Convergence | 900–1,100 | EH-3; calibration (ECE/Brier) | #19, #21, #24 | RES-EXP1(full), FIG-4.5(full), TAB-4.3 |
| 4.2.3 | Quantitative Diagnostic Metrics | 1,100–1,300 | EH-3, EH-4; CFC-2.8; CFC-2.1/2.2; VCR-3 (report falsification) | #19, #21, #24 | TAB-4.2, FIG-4.4, FIG-4.6, FIG-4.7, FIG-4.8 |
| 4.3.1 | V5 Ablation Design (Levels 0–6) | 900–1,100 | NC-17 (≠ universally optimal); PC-8 | #27, #23 | TAB-4.4 |
| 4.3.2 | CLAHE Threshold Sensitivity (H-2) | 800–1,000 | H-2; DGL-5; CFC-1.2 (no extrapolation); VCR-3; SIR-3 | #27, #23 | FIG-4.9 |
| 4.3.3 | Feature Preservation + σ Sweep + IQ | 800–1,000 | DGL-5; SIR-3 | #27, #23 | FIG-4.10, TAB-4.5 |
| 4.4.1 | Zero-Shot Transfer to APTOS (H-4) | 700–900 | OD-4 (G ratio); DGL-1; H-4 (G ≥ 0.85) | #02, #04, #05, #07, #11, #12, #16, #17, #38, #44, #48 | TAB-4.6 |
| 4.4.2 | Baseline vs V5 Comparison | 600–800 | OD-4; CFC-2.8 | (same as 4.4.1) | FIG-4.11 |
| 4.5.1 | Grad-CAM Generation Protocol | 700–900 | NC-14 | #06/#10, #46, #57, #58 | FIG-4.12 |
| 4.5.2 | ALO (primary) & IoU (secondary) | 900–1,100 | H-5 (ALO primary); NC-14 | #06/#10, #46, #63, #64 | TAB-4.7, FIG-4.14 |
| 4.5.3 | Attention Consistency Across Datasets | 600–800 | NC-14 | #46, #57, #58 | FIG-4.13 |
| 4.6 | Exp 5 — Clinical Degradation (H-7) | 1,000–1,300 | H-7; OD-4; DGL-1; DeLong | #06/#10, #17, #44, #48, #78 | TAB-4.8, FIG-4.15 |
| 4.7 | Exp 6 — Device Domain Shift (H-6) | 1,000–1,300 | H-6; NC-16 (≠ certification); DGL-1 | #38, #49, #50, #51, #74, #75, #76, #78 | TAB-4.9, App F set |
| 4.8 | Exp 7 — Small Data Training | 900–1,100 | DGL-1; SIR-1 (THIN) | #06/#10 | TAB-4.10, FIG-4.16 |
| 4.C | Conclusions to Chapter 4 | 700–900 | state H-1,H-2,H-4,H-5,H-6,H-7 outcomes; VCR-3 | — | all of §4.2–§4.8 |

### 9.2 Chapter 5 — Reliability Validation

| § | Title | Words | Governance bindings | Lit cards | Unblock (missing IDs) |
|---|-------|-------|---------------------|-----------|------------------------|
| 5.1 | Explainability Results | 1,000–1,300 | NC-14; H-5 | #06/#10, #16, #17, #27, #46, #24, #57, #58 | FIG-5.1, TAB-4.7, FIG-4.12 |
| 5.2.1 | Bootstrap CI & Mixed-Effects Model | 900–1,100 | EH-3, EH-4; multiple-comparison correction | #16, #17, #27, #52, #24 | TAB-5.1 |
| 5.2.2 | Final Claim-Strength Classifications | 900–1,100 | ARGUMENT_MAP §VI (STRONG/MODERATE/CONDITIONAL); EH-4 | #16, #17, #27, #24 | TAB-5.2, FIG-5.3 |
| 5.3.1 | Benchmarking vs Published Systems | 900–1,100 | CFC-2.2, NC-2 (contextual only); SB-1.12; SIR-3 | #02, #05, #07, #11, #12, #14, #23, #44, #45 | TAB-5.3, TAB-5.4 |
| 5.3.2 | Performance–Complexity Trade-Off | 700–900 | DGL-2 (hardware-specific); SIR-7 | #23 | FIG-5.2, FIG-5.4 |
| 5.4 | Limitations & Boundary Conditions | 1,000–1,300 | full SB-1…SB-4, DGL-1…DGL-6, NC-1…NC-17 enumeration | — | final H-1…H-7 outcomes (§4.C, §5.2.2) |
| 5.C | Conclusions to Chapter 5 | 600–800 | final claim strengths; VCR-3 | — | TAB-5.2 |

### 9.3 Chapter 0 — Introduction & Front Matter

> Per task phasing, Ch 0 is Phase 2 (final framing depends on results). Items marked 🟨 below are *content-writable now* and may be pulled forward at the candidate's discretion; **§0.8 is a hard block** (needs final claim strengths). Tense: present.

| § | Title | Words | Governance bindings | Lit cards | Status / Unblock |
|---|-------|-------|---------------------|-----------|------------------|
| 0.FM1 | Normative References | 200–400 | GLOSSARY; format standards | — | 🟨 writable now |
| 0.FM2 | Definitions (OD-1…OD-6 verbatim) | 600–900 | OD-1…OD-6 verbatim | — | 🟨 writable now |
| 0.FM3 | Designations & Abbreviations | 300–500 | GLOSSARY §6 standardization | — | 🟨 writable now |
| 0.1 | Relevance of the Research | 800–1,000 | SB-1.6, SIR-8 (projections not findings) | #01, #33, #35, #14 + LC-NAN_RK(#22) | 🟨 writable now |
| 0.2 | Scientific Novelty | 800–1,000 | SB-1.5/4.1; CFC-2.8; PC-1…PC-9 framing | self #19–#24 | 🟨 writable now |
| 0.3 | Research Goal | 300–500 | CORE_OBJECTIVE | — | 🟨 writable now |
| 0.4 | Research Objectives | 400–600 | maps objectives→chapters | — | 🟨 writable now |
| 0.5 | Object & Subject of Research | 200–400 | — | — | 🟨 writable now |
| 0.6 | Research Hypothesis (H-1…H-7 verbatim) | 600–900 | HYPOTHESIS.md verbatim; EH-3 | — | 🟨 writable now |
| 0.7 | Methodological Basis | 400–600 | EH-1…EH-4 | — | 🟨 writable now |
| 0.8 | Provisions Submitted for Defense | 700–900 | PC-1…PC-9 with final strengths | — | ⛔ blocked-by TAB-5.2 (§5.2.2) |
| 0.9 | Theoretical Significance | 300–500 | SB-1.5 (laser model theoretical) | #20, #23 | 🟨 writable now |
| 0.10 | Practical Significance | 300–500 | SB-1.3, SB-4.1; SIR-8 | #22 | 🟨 writable now |
| 0.11 | Approbation of Research Results | 200–300 | SIR-4 | — | ✅ writable now (App D) |
| 0.12 | Publications | 200–300 | SIR-4, SIR-5 | #19–#24 | ✅ writable now |

### 9.4 Chapter 7 — Conclusion

| § | Title | Words | Governance bindings | Lit cards | Unblock |
|---|-------|-------|---------------------|-----------|---------|
| 7 | Conclusion | 1,500–2,000 | restate IT-1 (Central Thesis); H-1…H-7 verdicts (VCR-3); PC-1…PC-9 final strengths; NC-1…NC-17; future work | — | all of Ch 4 + §5.2.2 (TAB-5.2) |

### 9.5 Appendices

| ID | Title | Governance bindings | Status / Unblock |
|----|-------|---------------------|------------------|
| App A | Source Code of the Preprocessing Pipeline | APP-A ✅ | ✅ writable now |
| App B | Confusion Matrices & Training Curves | — | ⛔ blocked-by FIG-4.6, FIG-4.5(full), TAB-4.3 (Exp 1–7) |
| App C | System Architecture UML Diagrams | SC-5.1 | ⛔ blocked-by DIA-6.3 (asset creation, not experiment-gated — §3.2) |
| App D | Certificates & Publication Confirmations | APP-D ✅; SIR-4 | ✅ writable now |
| App E | Grad-CAM Visualization Gallery | NC-14 | ⛔ blocked-by FIG-5.1, FIG-4.12 (Exp 4) |
| App F | Device Domain-Shift Supplementary Tables | NC-16 | ⛔ blocked-by TAB-4.9 + per-camera matrices (Exp 6) |

---

## 10. AUTONOMOUS PER-SECTION EXECUTION LOOP

For **each writable section, in the Phase-1 narrative order** (then Phase-2 order as gates open), run steps **a → f**. Do not skip a step; do not batch across sections.

**Pre-step (gate check):** Confirm against `ASSET_INVENTORY.md §2` that no result-dependent resource the section requires is `❌ MISSING`. If one is, **STOP** — leave the section ⛔ and move to the next writable section (§3.1). Deferred conceptual/UML diagrams (§3.2) do not stop the loop.

**a. Section Brief.** Generate the brief from `prompts/section-brief-template.md` v6.0.0. Fill *all* fields, in particular: **Argumentative Spine** (thesis / reasoning chain / hand-off), **Acceptance Criteria**, **Paradigm positioning** (P1/P2, permitted vs forbidden Gulshan phrasings per CFC-2.9/SIR-9), plus the governance bindings, lit-card source mapping, and required Resource IDs from this plan's section row.
→ Save to `thesis/chapters/<NN-chapter>/briefs/<§x.x.x>-brief.md`. Set tracker to **🟦**.

**b. Self-review the brief.** Check the brief against governance (INVARIANTS v6.0.0 + the bindings listed for the section). Flag any **coverage gap** (a required content element with no mapped literature card → mark for `[UNSOURCED CLAIM]` handling or candidate-original analysis; note lit-THIN/GAP sections from the Coverage Matrix). Resolve or explicitly accept each gap before drafting.

**c. Draft.** Generate the section using `prompts/writing-session-system-prompt.md` v6.0.0 (load: system prompt → INVARIANTS.md → the Brief → relevant literature cards → preceding Continuity Note). Output PART 1 (prose + tables in Markdown), PART 2 (Continuity Note), PART 3 (compliance checklist).
- **Figures:** reference by Resource ID with a caption and the **real file path from `ASSET_INVENTORY.md`**. **Do NOT embed images.** Insert a placeholder the later `.docx` step can resolve, e.g.
  `[FIG-3.6: Stage 4 — Adaptive flat-field correction — defense/presentation/assets/preprocessing/15_flatfield/stage4_flatfield.png]`
  For a deferred conceptual/UML diagram, use `… — ASSET TO BE CREATED` (§3.2).
- **Tables** that are `✅ AVAILABLE` as governance text (TAB-2.1, TAB-3.1/3.2/3.3, TAB-4.1) are rendered inline as Markdown.

**d. Verify.** Run `prompts/verification-protocol.md` v6.0.0 against the draft + brief + INVARIANTS (sections A–H: claim compliance, forbidden-content scan CFC-2.1…2.9, terminology, source handling SIR-1…9, structural integrity, scope/paradigm, evidence thresholds). Verdict: **APPROVED** or **REVISION NEEDED**. If revision needed → run `prompts/revision-session-template.md`, re-verify. Only APPROVED advances.

**e. Continuity note.** Confirm PART 2 is complete and accurate (key concepts, terms introduced, argument thread, final topic, setup for next section, unresolved threads).
→ Save to `thesis/chapters/<NN-chapter>/continuity/<§x.x.x>-continuity.md`.

**f. Save draft.** Save the approved PART 1 to `thesis/chapters/<NN-chapter>/drafts/<§x.x.x>-draft.md` (and the verification record to `reviews/`, session transcript to `sessions/`). Set tracker to **🟩** on save, **✅** once verification is APPROVED.

> Carry the saved Continuity Note into step **c** of the *next* section so its opening paragraph connects to the prior argument thread.

---

## 11. PHASE 3 — FINAL ASSEMBLY (LAST step; depends on Phase 2 completion)

Run only after **every** section in §1 is ✅ verified (all Phase-1 *and* Phase-2 gates cleared). Do not start earlier.

**§11.1 Concatenate.** Assemble all approved `drafts/*.md` in exact `MASTER_OUTLINE.md` order: Front Matter → Introduction (Ch 0) → Ch 1 → Ch 2 → Ch 3 → Ch 4 (§4.1 → §4.2 → … → §4.8 → §4.C) → Ch 5 → Ch 6 → Ch 7 (Conclusion) → References → Appendices A–F.

**§11.2 Resolve placeholders.** Replace every `[FIG-x.x: …]` / `[TAB-x.x: …]` placeholder with its real asset, using the file path from `ASSET_INVENTORY.md §2`. Any remaining `ASSET TO BE CREATED` (FIG-2.1, FIG-2.3, FIG-2.4, FIG-2.5, DIA-6.3/App C) must be drawn and dropped in here before conversion. Verify no placeholder, no `[UNSOURCED CLAIM]`, and no `[TERM NOT IN GLOSSARY]` flag survives.

**§11.3 Convert to `.docx`.** Convert the single assembled Markdown document to one `.docx` (e.g. via Pandoc with a reference docx for dissertation styling), embedding the resolved figures and rendering tables. Output: one defense-ready `.docx`. (Kazakh translation is a separate downstream pipeline — Stages E/F — and is out of scope for this plan.)

---

## 12. SUMMARY

- **Writable now (Phase 1): 51 sections** — Ch 1 (11) + Ch 2 (15) + Ch 3 (13) + Ch 6 (9) + §4.1 (3) — **plus Appendix A and Appendix D** (already `✅ AVAILABLE`). Four of these (§2.1.1, §2.4.1, §2.5.1, §2.6) and §6.1.2/App C carry **deferred conceptual/UML diagrams**, which do not block the prose (§3.2).
- **Blocked (Phase 2): 42 sections** — Ch 4 §4.2–§4.8 + §4.C (15) + Ch 5 (7) + Ch 0 (15, of which 13 are content-writable-now and 2 hard-blocked) + Ch 7 (1) + Appendices B/C/E/F (4) — each gated on the missing Resource IDs catalogued in §2 and §9.
- **Hard honesty rule is in force:** no section is drafted while a result-dependent resource it needs is `❌ MISSING`; no demo-dashboard preview numbers are ever used as real results (CFC-2.x / SIR-1).
- **Phase 3 is last** and runs only after all sections verify.

**First section to execute: §1.1.1 — Pathophysiology and Clinical Grading Systems.** ✅ Confirmed.

> Awaiting candidate review of this plan before any section is drafted.
