# VERSION SYNCHRONIZATION REGISTER

**Governance Version:** 4.1
**Last Sync Date:** 2026-03-26
**Synced by:** Post-V4 sync pass — Stage 0 expansion (0a+0b), 5-fold→3-fold, EyePACS 40% subset, max_epochs 50→20, APTOS DROPPED annotations, binocular blending extension note, SC-1.3 divergence documented

## File Version Status

| File | Required Version | Current Version | Synced |
|------|-----------------|-----------------|--------|
| governance/INVARIANTS.md | 4.1 | 4.1 | ✅ |
| governance/ARGUMENT_MAP.md | 4.1 | 4.1 | ✅ |
| governance/RESEARCH_ARCHITECTURE.md | 4.1 | 4.1 | ✅ |
| governance/CONTRIBUTIONS.md | 4.1 | 4.1 | ✅ |
| governance/CENTRAL_THESIS.md | 4.0 | 4.0 | ✅ (no changes required) |
| governance/CORE_OBJECTIVE.md | 4.0 | 4.0 | ✅ (no changes required) |
| governance/HYPOTHESIS.md | 4.1 | 4.1 | ✅ |
| outline/MASTER_OUTLINE.md | 4.1 | 4.1 | ✅ |
| outline/TABLE_OF_CONTENTS_EN.md | 4.0 | 4.0 | ✅ (no changes required) |
| outline/TABLE_OF_CONTENTS_KZ.md | 4.0 | 4.0 | ✅ (no changes required) |
| glossary/GLOSSARY_EN.md | 4.1 | 4.1 | ✅ |
| glossary/GLOSSARY_KZ.md | 4.1 | 4.1 | ✅ |
| literature/LITERATURE_INDEX.md | 4.0 | 4.0 | ✅ (literature cards not modified) |
| experiments/experimental-protocol.md | 4.1 | 4.1 | ✅ |
| methods/preprocessing-pipeline.md | 4.1 | 4.1 | ✅ |
| methods/implementation.md | 4.0 | 4.0 | ✅ (no changes required — already correct) |

## V4.1 Changes Applied (2026-03-26)

| Change Category | Old (V4.0) | New (V4.1) |
|----------------|------------|------------|
| Stage 0 | Canonical Flip (single stage) | Canonical Orientation: Stage 0a (Canonical Flip) + Stage 0b (OD-Fovea Rotation Normalization) |
| Stage 5 rotation_sigma | Fixed 13° reference | Adaptive per-image from Stage 0b OD/fovea detection uncertainty; fallback σ=13.0° |
| Cross-validation | 5-fold | 3-fold (patient-level stratified) |
| EyePACS size | ~35,126 labeled (Kaggle partition) | ~35,126 labeled (40% subset); ~14,050 used for experiments |
| max_epochs | 50 (with early stopping) | 20 (with early stopping, patience=5) |
| APTOS 2019 | Present in dataset architecture without DROPPED annotation | DROPPED annotation added in IT-1, DGL-1, scope boundary in INVARIANTS; ARGUMENT_MAP scope boundary |
| SC-F contribution | Absent | Added (OD-Fovea Rotation Normalization as Stage 0b contribution) |
| Per-patient binocular blending | Mentioned in §4.3 | Added as explicit Optional Extension paragraph in RESEARCH_ARCHITECTURE §3.1 |
| Exp 2 ablation table | 6 rows (baseline through full V4) | 7 rows: added Stage 0a-only vs Stage 0a+0b distinction |

## V4 Changes Applied (2026-03-24, preserved for audit trail)

| Change Category | V3 (Old) | V4 (New) |
|----------------|----------|----------|
| Pipeline stages | 5 components | 6 stages |
| Stage 0 | (absent) | Canonical flip (toggleable) |
| Stage 1 (FOV) | Hough circle detection | PIL-based foreground detection |
| Stage 2 | (absent) | Flat-field correction, σ=45 Gaussian blur subtraction |
| Stage 3 (CLAHE) | Dynamic clip limit, LAB L-channel | Dual-constraint clip limit (clip_factor × tile_area/256, capped); stochastic 80% prob at train time |
| Stage 4 (Normalization) | Pixel values [0,1] | ImageNet channel-wise (x − mean)/std → tensor |
| Stage 5 (Augmentation) | Separate training-time layer | Integrated into pipeline at train time |
| Removed: Green channel | Was V3 component | REMOVED |
| Removed: HSV enhancement | Was V3 component | REMOVED |
| Baseline definition | "resize only" | "crop + resize + ImageNet normalize" (Stages 1+4) |
| Exp 1 configurations | 4 (A–D) | 6 (A–F; E/F add per-patient binocular blending) |

## Known Divergences Between dissertation/ and dr-classifier/

| ID | Divergence | dissertation/ | dr-classifier/ | Status |
|----|-----------|---------------|----------------|--------|
| DIV-1 | SC-1.3 (processing time / 8× speedup claim) | REMOVED V3 — implausible claim deleted from ARGUMENT_MAP | SC-1.3 retained as secondary metric (processing time) | INTENTIONAL. Dissertation removed the implausible "1s 108ms vs 8s 986ms" claim. dr-classifier retains SC-1.3 as a tracking stub. No action required. |

## Sync Protocol

Before any chapter-writing AI session:
1. Verify all files in the session's input package are ✅ above.
2. If any file shows ❌, update it before proceeding.
3. After any governance document update, re-run verification on all dependent files.
