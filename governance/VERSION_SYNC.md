# VERSION SYNCHRONIZATION REGISTER

**Governance Version:** 4.0
**Last Sync Date:** 2026-03-24
**Synced by:** V3→V4 governance upgrade (V4 canonical pipeline, 6-stage)

## File Version Status

| File | Required Version | Current Version | Synced |
|------|-----------------|-----------------|--------|
| governance/INVARIANTS.md | 4.0 | 4.0 | ✅ |
| governance/ARGUMENT_MAP.md | 4.0 | 4.0 | ✅ |
| governance/RESEARCH_ARCHITECTURE.md | 4.0 | 4.0 | ✅ |
| governance/CONTRIBUTIONS.md | 4.0 | 4.0 | ✅ |
| governance/CENTRAL_THESIS.md | 4.0 | 4.0 | ✅ |
| governance/CORE_OBJECTIVE.md | 4.0 | 4.0 | ✅ |
| governance/HYPOTHESIS.md | 4.0 | 4.0 | ✅ |
| outline/MASTER_OUTLINE.md | 4.0 | 4.0 | ✅ |
| outline/TABLE_OF_CONTENTS_EN.md | 4.0 | 4.0 | ✅ |
| outline/TABLE_OF_CONTENTS_KZ.md | 4.0 | 4.0 | ✅ |
| glossary/GLOSSARY_EN.md | 4.0 | 4.0 | ✅ |
| glossary/GLOSSARY_KZ.md | 4.0 | 4.0 | ✅ |
| literature/LITERATURE_INDEX.md | 4.0 | 4.0 | ✅ (literature cards not modified) |
| experiments/experimental-protocol.md | 4.0 | 4.0 | ✅ |
| methods/preprocessing-pipeline.md | 4.0 | 4.0 | ✅ |
| methods/implementation.md | 4.0 | 4.0 | ✅ |

## V4 Changes Applied

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

## Sync Protocol

Before any chapter-writing AI session:
1. Verify all files in the session's input package are ✅ above.
2. If any file shows ❌, update it before proceeding.
3. After any governance document update, re-run verification on all dependent files.
