# VERSION_SYNC.md

## V3 → V4 Documentation Sync Status

**Sync Date:** 2026-03-24
**Sync Scope:** V3.0 → V4.0
**Performed by:** Claude Code

---

## Summary of V4 Changes Applied

| Change Category | V3 (Old) | V4 (New) |
|----------------|----------|----------|
| Pipeline stages | 5 components | 6 stages |
| Stage 0 | (absent) | Canonical flip (toggleable) |
| Stage 1 (FOV) | Hough circle detection | PIL-based foreground detection |
| Stage 2 | (absent) | Flat-field correction, σ=45 Gaussian blur subtraction |
| Stage 3 (CLAHE) | Dynamic clip limit, LAB L-channel | Dual-constraint clip limit (clip_factor × tile_area/256, capped by global_threshold × tile_area); stochastic 80% prob at train time |
| Stage 4 (Normalization) | Pixel values [0,1] | ImageNet channel-wise (x − mean)/std → tensor |
| Stage 5 (Augmentation) | Separate training-time layer | Integrated into pipeline at train time |
| Removed: Green channel | Was Stage 2 | REMOVED |
| Removed: HSV enhancement | Was Stage 5 | REMOVED |
| Baseline definition | "resize only" | "crop + resize + ImageNet normalize" (Stages 1+4) |
| EyePACS size | ~88,000 images | ~35,126 labeled (40% subset); ~14,050 used |
| Cross-validation | 5-fold | 3-fold |
| Exp 1 configurations | 4 (A–D) | 6 (A–F; E/F add per-patient binocular blending) |
| Per-patient binocular blending | (absent) | Optional extension (configs E, F) |
| Model-specific augmentation | (absent) | "resnet" (full) vs. "efficientnet" (reduced) presets |

---

## Files Updated

### dr-classifier/docs/ ✅

| File | Status | Key Changes |
|------|--------|-------------|
| `docs/INVARIANTS.md` | ✅ v4.0 | Document version updated; IT-1 updated; H-1 updated; OD-3 updated; SB-2.1 updated; DGL-1 updated; DGL-5 updated; VCR-1 updated; footer updated |
| `docs/HYPOTHESIS.md` | ✅ v4.0 | Document version added; H-1 pipeline description updated; H-2 parameter description updated; H-3 demoted marker added; Argument Structure Premise 3 updated |
| `docs/ARGUMENT_MAP.md` | ✅ v4.0 | Binding reference updated; IT-1 verbatim updated; PC-1 updated; PC-2 updated; PC-6 updated; PC-7 updated; PC-8 updated; PC-9 updated; SC-6.1 updated; SC-7.1 updated; SC-8.1 updated; SC-9.1 updated; PC-1 strength promotion criteria updated; footer updated |
| `docs/RESEARCH_ARCHITECTURE.md` | ✅ v4.0 | Document version; causal chain; dataset architecture (EyePACS size); split strategy (3-fold); pipeline section (§3.1 rewritten, §3.2 updated); Exp 1 table; Exp 2 ablation levels; Exp 4 pipeline comparison; CV protocol; ablation protocol; novelty layer; risk control layer |
| `docs/experimental_protocol.md` | ✅ v4.0 | Exp 1 and Exp 2 comments updated |

---

## Files Updated in Second Sync Pass (2026-03-24)

The following files in `~/dissertation/` were updated in the V3→V4 governance upgrade pass:

| File | Status | Changes Applied |
|------|--------|-----------------|
| `dissertation/governance/INVARIANTS.md` | ✅ v4.0 | IT-1, H-1, OD-3 updated to V4 6-stage pipeline; DGL-5 updated; footer updated |
| `dissertation/governance/ARGUMENT_MAP.md` | ✅ v4.0 | IT-1, PC-1, PC-2, PC-6, PC-7, PC-8, PC-9, SC-6.1, SC-7.1, SC-8.1, SC-9.1 updated |
| `dissertation/governance/HYPOTHESIS.md` | ✅ v4.0 | H-1, H-4 pipeline descriptions updated; Premise 3 updated |
| `dissertation/governance/CONTRIBUTIONS.md` | ✅ v4.0 | C-1, SC-A pipeline descriptions updated |
| `dissertation/governance/CENTRAL_THESIS.md` | ✅ v4.0 | Pipeline description updated to V4 6-stage |
| `dissertation/governance/RESEARCH_ARCHITECTURE.md` | ✅ v4.0 | §3.1 rewritten V4; §3.2 updated; Exp 1 table 6 configs; Exp 2 ablation levels V4; ablation protocol updated; novelty layer updated |
| `dissertation/methods/preprocessing-pipeline.md` | ✅ v4.0 | Full V4 pipeline spec; V3 kept as historical section |
| `dissertation/methods/implementation.md` | ✅ v4.0 | CLAHE config updated to dual-constraint; augmentation updated |
| `dissertation/outline/MASTER_OUTLINE.md` | ✅ v4.0 | All pipeline references updated to V4; factorial design updated to 6 configs |
| `dissertation/glossary/GLOSSARY_EN.md` | ✅ v4.0 | New entries: Canonical Flip, Flat-Field Correction, PIL-based FOV Crop and Resize, ImageNet Normalization; updated: Preprocessing Pipeline, Upgraded CLAHE, Green Channel Imaging (historical), HSV Contrast Enhancement (historical) |
| `dissertation/glossary/GLOSSARY_KZ.md` | ✅ v4.0 | Same changes as GLOSSARY_EN.md in Kazakh |
| `dissertation/governance/VERSION_SYNC.md` | ✅ v4.0 | Updated to v4.0 with all files marked ✅ |

---

## Invariant Constraints Preserved

The following were NOT changed (as required):
- EH-3 dominance thresholds: Δ weighted F1 ≥ 5 pp; Δ ROC-AUC ≥ 0.02; no Kappa degradation — UNCHANGED
- PC-1 through PC-9 claim dependency structure — UNCHANGED
- H-3 kept but marked as DEMOTED/HISTORICAL — PRESERVED
- PC-4 (thermal-optical model) — PRESERVED as supplementary
- PC-5 (system architecture) — PRESERVED as supplementary
- All V3 pipeline descriptions kept as [V3 Historical] markers — PRESERVED
- Literature card content — NOT MODIFIED

---

*VERSION_SYNC.md updated: 2026-03-24. Both dr-classifier/docs/ and dissertation/ governance files synced to V4.0.*
