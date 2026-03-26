# Claude Code Prompt: Synchronize Dissertation Repo with DR-Classifier

**Context:** The `dr-classifier` repo has been upgraded with major V4 changes (OD-fovea alignment, expanded Stage 0, updated CLAUDE.md, refined governance docs). The `dissertation` repo's governance, methods, experiments, outline, and glossary files were partially synced during a prior V3→V4 pass but are now **behind** the latest dr-classifier state. This prompt instructs Claude Code to bring `dissertation` into exact alignment with `dr-classifier/docs/` as the single source of truth.

**Repos:**
- Source of truth: `~/dr-classifier/` (specifically `docs/`, `CLAUDE.md`, `src/preprocessing/`, `IMPLEMENTATION_PLAN_OD_FOVEA_v2.md`)
- Target: `~/dissertation/`

**Operating principle:** Where dr-classifier/docs/ and dissertation/governance/ diverge, dr-classifier wins. The dissertation files must be updated to match. Preserve dissertation-only structural elements (e.g., `<!-- DROPPED V3 -->` comments for audit trail, V3 historical notes) but update all V4 substance to match dr-classifier exactly.

---

## PRE-FLIGHT: Read Both Repos

Before making any changes, read `~/CLAUDE.md` (root-level file unifying both repos), then:

1. Read `~/dr-classifier/CLAUDE.md` — this is the authoritative project context.
2. Read `~/dr-classifier/docs/VERSION_SYNC.md` — this documents V4 changes already applied.
3. Read `~/dr-classifier/docs/INVARIANTS.md` in full.
4. Read `~/dr-classifier/docs/HYPOTHESIS.md` in full.
5. Read `~/dr-classifier/docs/ARGUMENT_MAP.md` in full.
6. Read `~/dr-classifier/docs/RESEARCH_ARCHITECTURE.md` in full.

Then read these dissertation files to understand current state:
7. Read `~/dissertation/governance/INVARIANTS.md` in full.
8. Read `~/dissertation/governance/HYPOTHESIS.md` in full.
9. Read `~/dissertation/governance/ARGUMENT_MAP.md` in full.
10. Read `~/dissertation/governance/RESEARCH_ARCHITECTURE.md` in full.
11. Read `~/dissertation/governance/CONTRIBUTIONS.md` in full.
12. Read `~/dissertation/governance/CENTRAL_THESIS.md` in full.
13. Read `~/dissertation/methods/preprocessing-pipeline.md` in full.
14. Read `~/dissertation/methods/implementation.md` in full.
15. Read `~/dissertation/experiments/experimental-protocol.md` in full.
16. Read `~/dissertation/glossary/GLOSSARY_EN.md` in full.
17. Read `~/dissertation/outline/MASTER_OUTLINE.md` in full.

**CHECK before proceeding:** Confirm you have read all 17 files. List each file and its document version. Do NOT proceed until all files are loaded.

---

## CHANGE CATEGORY 1: Cross-Validation Fold Count (5-fold → 3-fold)

**Problem:** DR-classifier uses 3-fold CV everywhere. The dissertation has an inconsistency: some files say 3-fold (implementation.md, experimental-protocol.md, MASTER_OUTLINE.md partially), but the governance core files still say 5-fold.

**Files to fix and what to change:**

### 1a. `dissertation/governance/INVARIANTS.md`
- **Line with H-1 control conditions:** Change `5-fold cross-validation with patient-level split` → `3-fold cross-validation with patient-level stratified split`
- Verify: search for ALL occurrences of `5-fold` in this file and replace with `3-fold` where they refer to CV protocol (NOT the V3 historical reference).

**CHECK:** Run `grep -n "5-fold" ~/dissertation/governance/INVARIANTS.md` — the only remaining `5-fold` references should be inside `[V3 Historical]` markers or in VCR-1 notes about version changes. Zero `5-fold` references should describe the active protocol.

### 1b. `dissertation/governance/ARGUMENT_MAP.md`
- PC-1 Required Evidence Type: Change `5-fold cross-validation with patient-level split` → `3-fold cross-validation with patient-level stratified split`
- PC-1 Strength Promotion criteria: Change `5-fold cross-validation` → `3-fold cross-validation`
- Search for ALL `5-fold` in this file. Fix every active protocol reference.

**CHECK:** Run `grep -n "5-fold" ~/dissertation/governance/ARGUMENT_MAP.md` — zero results for active protocol references.

### 1c. `dissertation/governance/RESEARCH_ARCHITECTURE.md`
- §2.2 Split Strategy: Change `5-fold` to `3-fold`, `4 folds serve as training` to `2 folds serve as training`, `repeated 5 times` to `repeated 3 times`. Add the sentence about replacing v2.1 5-fold CV (match dr-classifier wording).
- §5.0 CV Protocol section: Same 5→3 fold changes.
- §6.1 primary metrics reporting: `5-fold` → `3-fold`
- §6.8 Statistical Tests: `5-fold` → `3-fold`
- §9.1 Leakage Control: `patient-level 5-fold CV` → `patient-level 3-fold CV`

**CHECK:** Run `grep -n "5-fold" ~/dissertation/governance/RESEARCH_ARCHITECTURE.md` — zero active results.

### 1d. `dissertation/outline/MASTER_OUTLINE.md`
- Find the line referencing `EyePACS class distribution and 5-fold cross-validation` → change to `3-fold`
- Verify: the outline already has `3-fold` in most places. Fix any remaining `5-fold` occurrences.

**CHECK:** `grep -n "5-fold" ~/dissertation/outline/MASTER_OUTLINE.md` — zero active references (the footer version note mentioning the change `5-fold CV → 3-fold` is fine as a changelog entry).

---

## CHANGE CATEGORY 2: Stage 0 Expansion (Canonical Flip → Canonical Orientation with OD-Fovea)

**Problem:** DR-classifier's CLAUDE.md and source code now define Stage 0 as a two-part stage:
- Stage 0a: Canonical flip (left→right eye orientation) — toggleable
- Stage 0b: OD-fovea rotation normalization (classical CV detection) — toggleable

The dissertation still describes Stage 0 as simple "canonical flip" only. The OD-fovea rotation normalization is a major new feature that the dissertation must document.

**Source references:**
- `~/dr-classifier/CLAUDE.md` lines 83–88 (Stage 0 expanded description)
- `~/dr-classifier/src/preprocessing/od_fovea_detect.py` (OD/fovea detection module)
- `~/dr-classifier/src/preprocessing/canonical_orientation.py` (combined flip + rotation)
- `~/dr-classifier/IMPLEMENTATION_PLAN_OD_FOVEA_v2.md` (full spec)

Also: Stage 5 augmentation now has an **adaptive rotation σ** derived from OD/fovea detection uncertainty (replaces fixed σ=13.0° as fallback).

**Files to update:**

### 2a. `dissertation/methods/preprocessing-pipeline.md`

Update the Stage 0 section:

**Current:** Stage 0 describes only "Canonical Flip — horizontal flip for left-eye images..."

**Change to:** Stage 0 is now "Canonical Orientation" with two sub-stages:
```
### Stage 0 — Canonical Orientation (toggleable)

#### Stage 0a — Canonical Flip
- **Operation:** Horizontal flip for left-eye images to right-eye canonical orientation
  (optic disc right, macula left).
- **Purpose:** Ensure consistent retinal orientation across bilateral image pairs.
- **Output:** Canonically oriented fundus image (right-eye orientation).

#### Stage 0b — OD-Fovea Rotation Normalization
- **Operation:** Classical CV detection of optic disc (brightest region via
  Gaussian-blurred green channel) and fovea (darkest region in temporal half
  with distance prior from OD center). Computes OD→fovea vector angle and
  rotates image to make this axis horizontal.
- **Confidence gating:** When detection confidence is low (sanity checks fail on
  distance, radius, or relative position), rotation is skipped (fallback to
  unrotated image).
- **Purpose:** Normalize anatomical orientation so the OD→fovea axis is
  consistently horizontal across all images, reducing rotational variability.
- **Output:** Rotationally normalized fundus image.
- **V4 Status:** NEW — extends Stage 0 from simple flip to full orientation
  normalization.
```

Also update Stage 5 augmentation to mention adaptive rotation σ:
```
- **Rotation σ:** Adaptive per-image (derived from OD/fovea localization
  uncertainty when detection is confident) or fallback σ=13.0° (when OD/fovea
  detection is not confident or disabled).
```

### 2b. `dissertation/governance/INVARIANTS.md`

In IT-1, the pipeline description currently says `canonical orientation normalization`. This is fine as an umbrella term. However, in the OD-3 definition (Section III, where the pipeline stages are listed individually), add Stage 0b as a sub-stage of Stage 0. Specifically:

- Find the Stage 0 definition in OD-3. Currently it says: `Stage 0: Canonical Flip — horizontal flip for left-eye images...`
- Expand to:
  ```
  Stage 0: Canonical Orientation (toggleable)
    0a. Canonical flip — left→right eye orientation normalization
    0b. OD-fovea rotation normalization — detects optic disc and fovea via
        classical CV; rotates image so OD→fovea axis is horizontal; skips
        rotation when detection confidence is low (toggleable independently)
  ```

### 2c. `dissertation/governance/RESEARCH_ARCHITECTURE.md`

In §3.1 V4 Ordered Pipeline, update the Stage 0 bullet to include both 0a and 0b (match the CLAUDE.md description). Also update Stage 5 to mention adaptive rotation σ.

### 2d. `dissertation/governance/HYPOTHESIS.md`

In H-1, the pipeline component list mentions `canonical flip (left→right orientation)`. Update to `canonical orientation (left→right flip + OD-fovea rotation normalization)`.

### 2e. `dissertation/governance/ARGUMENT_MAP.md`

In IT-1, PC-1, and any other pipeline component listings: update `canonical flip` → `canonical orientation (Stage 0a flip + Stage 0b OD-fovea rotation)` where the pipeline stages are enumerated.

### 2f. `dissertation/governance/CONTRIBUTIONS.md`

Add a new supporting contribution:

```
### SC-F: Anatomical Orientation Normalization via OD-Fovea Detection

**Contribution:** Design and implementation of a classical computer vision
module that detects optic disc and fovea landmarks in fundus images, computes
the OD→fovea vector angle, and rotates the image to normalize anatomical
orientation. Includes confidence gating that skips rotation when detection
is unreliable.

**Evidence:** Experiment 1 (Stage 0b is part of the full V4 pipeline) and
Experiment 2 (component-level ablation, Stage 0 contribution).

**Novelty:** Combines OD-fovea geometric normalization with uncertainty-aware
adaptive rotation augmentation (Stage 5 σ derived from detection confidence),
providing both deterministic preprocessing (Stage 0b) and informed stochastic
augmentation (Stage 5) from a single classical CV module.
```

Update the Contributions table to include SC-F:
```
| SC-F | PC-1, PC-8 |
```

### 2g. `dissertation/glossary/GLOSSARY_EN.md`

Add new entry:
```
| **OD-Fovea Rotation Normalization** | Stage 0b of the V4 pipeline. Classical
computer vision detection of optic disc (OD) and fovea centers, followed by
rotation to make the OD→fovea axis horizontal. Detection uses Gaussian-blurred
green channel for OD (brightest region) and darkest-region-with-distance-prior
for fovea. Confidence gating skips rotation when detection is unreliable. |
Operational Definition | Ch. 3 (§3.1) | Is a sub-stage of: Canonical
Orientation (Stage 0); Produces: rotation-normalized fundus image |
```

Update existing "Canonical Flip" entry to "Canonical Orientation" with sub-entries for 0a and 0b.

### 2h. `dissertation/glossary/GLOSSARY_KZ.md`

Same changes as GLOSSARY_EN.md but in Kazakh. Use appropriate translations:
- Optic Disc → Оптикалық диск
- Fovea → Фовеа / Сары дақтың орталық шұңқыры
- OD-Fovea Rotation Normalization → ОД-фовеа айналу нормалау

### 2i. `dissertation/experiments/experimental-protocol.md`

Update Experiment 2 V4 ablation table: Stage 0 should be described as "Canonical Orientation (flip + OD-fovea rotation)" rather than just "canonical flip."

### 2j. `dissertation/outline/MASTER_OUTLINE.md`

Update any pipeline stage listings to include Stage 0b. Search for `canonical flip` and update to `canonical orientation (flip + OD-fovea rotation normalization)` where pipeline stages are enumerated.

**GLOBAL CHECK after Category 2:** Run:
```bash
grep -rn "canonical flip" ~/dissertation/ | grep -v "V3 Historical\|v3.0\|Historical:\|DROPPED\|was V3"
```
Any remaining `canonical flip` references (outside historical markers) should now read `canonical orientation` or `canonical flip (Stage 0a)` within a broader Stage 0 description. Pure standalone `canonical flip` as the entire Stage 0 description is outdated.

---

## CHANGE CATEGORY 3: IT-1 and Pipeline Description Alignment

**Problem:** The IT-1 wording in dissertation/governance/INVARIANTS.md differs from dr-classifier/docs/INVARIANTS.md. The dr-classifier version is more specific (includes Stage 0, PIL-based, σ=45, etc.) while the dissertation version uses more abstract wording.

**Rule:** DR-classifier is the source of truth. Update dissertation IT-1 to match dr-classifier IT-1 verbatim.

### 3a. `dissertation/governance/INVARIANTS.md` — IT-1

Replace the current IT-1 text with the exact IT-1 from `~/dr-classifier/docs/INVARIANTS.md` (which begins: "An integrated preprocessing-CNN pipeline — comprising canonical flip (Stage 0)..."). **Include the APTOS 2019 DROPPED annotation** from dr-classifier.

**Important update for Stage 0:** After copying, update `canonical flip (Stage 0)` → `canonical orientation (Stage 0: Stage 0a canonical flip + Stage 0b OD-fovea rotation normalization)` to reflect the new Stage 0 expansion (Change Category 2).

### 3b. `dissertation/governance/ARGUMENT_MAP.md` — IT-1

Same: copy the IT-1 blockquote from dr-classifier's ARGUMENT_MAP.md, then apply the Stage 0 expansion.

### 3c. Verify H-1 in both INVARIANTS and HYPOTHESIS match dr-classifier

Compare H-1 text between the two repos. The dr-classifier version should be more explicit. Copy it, then apply Stage 0 expansion.

**CHECK:** After updating, run:
```bash
diff <(grep "IT-1" ~/dr-classifier/docs/INVARIANTS.md) <(grep "IT-1" ~/dissertation/governance/INVARIANTS.md)
```
The only diff should be the Stage 0 expansion (0a/0b) which the dissertation adds on top of dr-classifier's description.

---

## CHANGE CATEGORY 4: EyePACS Size Description Alignment

**Problem:** DR-classifier consistently says `~35,126 labeled images (40% subset of full EyePACS; ~14,050 used for experiments)`. The dissertation says `~35,126 labeled images (Kaggle labeled partition)` without the 40% subset or ~14,050 details.

### 4a. Update ALL EyePACS size references in dissertation to match dr-classifier:

Files to check:
- `governance/INVARIANTS.md` (SB-2.1): Add `(40% subset of the full dataset; ~14,050 used for experiments)`
- `governance/ARGUMENT_MAP.md` (dataset scope): Add `40% subset` and `~14,050 used`
- `governance/RESEARCH_ARCHITECTURE.md` (§2.1.1): Match dr-classifier's wording
- `experiments/experimental-protocol.md` (§1 Datasets table): Update EyePACS size description

**CHECK:**
```bash
grep -rn "35,126" ~/dissertation/ | grep -v "40%"
```
Should return zero results (all 35,126 references should now also mention 40% subset context).

---

## CHANGE CATEGORY 5: APTOS 2019 Dropped Status Consistency

**Problem:** DR-classifier INVARIANTS IT-1 explicitly mentions `APTOS 2019 (robustness — DROPPED, Experiment 3 not conducted; dataset retained in architecture but not used in active experiments)`. The dissertation IT-1 simply omits APTOS 2019 from the dataset list. The dr-classifier approach is more explicit and should be adopted.

### 5a. `dissertation/governance/INVARIANTS.md` — IT-1

When updating IT-1 per Category 3, include the APTOS 2019 DROPPED annotation from dr-classifier.

### 5b. `dissertation/governance/INVARIANTS.md` — DGL-1

Match dr-classifier's DGL-1 which explicitly includes `APTOS 2019 (robustness testing — DROPPED, Experiment 3 not conducted; dataset retained in architecture as reserved)`.

### 5c. `dissertation/governance/INVARIANTS.md` — SB-1.1

Match dr-classifier's SB-1.1 which lists `APTOS 2019` in the dataset architecture list (with DROPPED status implied by IT-1 context).

**CHECK:**
```bash
grep -n "APTOS" ~/dissertation/governance/INVARIANTS.md
```
Verify APTOS appears with DROPPED annotation wherever the dataset architecture is listed.

---

## CHANGE CATEGORY 6: SC-1.3 Removal vs. DR-Classifier

**Problem:** The dissertation ARGUMENT_MAP removed SC-1.3 (the implausible 8× processing speed claim) with a `<!-- REMOVED V3 -->` comment. The dr-classifier ARGUMENT_MAP still has SC-1.3 as a live sub-claim. This is a case where the dissertation is actually **more correct** — the claim was correctly identified as implausible.

**Decision:** Keep the dissertation's SC-1.3 removal. However, verify that the dependency tree in the dr-classifier ARGUMENT_MAP's Section V (hierarchy visualization) does not create an inconsistency. If dr-classifier shows `SC-1.3` in its tree, note this as a known divergence that should be patched in dr-classifier separately (out of scope for this sync — document it in VERSION_SYNC.md).

### 6a. `dissertation/governance/VERSION_SYNC.md`

Add a note:
```
## Known Divergences (Dissertation Leads)

| Item | Dissertation | DR-Classifier | Resolution |
|------|-------------|---------------|------------|
| SC-1.3 | REMOVED (implausible processing time claim) | Still present as live sub-claim | DR-classifier should be patched to match dissertation |
```

---

## CHANGE CATEGORY 7: Experiment 3 Status and Experiment Numbering

**Problem:** DR-classifier has Experiment 3 (robustness) as a file (`exp3_robustness.py`) but marks it DROPPED in governance. The dissertation uses V3 numbering where old Exp 5+6 were merged into V3 Exp 3, then V4 split them back to Exp 5 and Exp 6. The numbering schemes are now aligned at V4 (Exp 1–6 + dropped Exp 3 + future Exp 7) but some internal references in the dissertation still use "V3 Experiment 3" to mean "merged generalization + device shift."

### 7a. Verify experiment numbering consistency

Run:
```bash
grep -rn "V3 Exp\|V3 Experiment" ~/dissertation/governance/ ~/dissertation/experiments/ ~/dissertation/outline/
```

All "V3 Experiment 3" references should be clearly marked as historical/merged and should point readers to V4 Experiments 5 and 6. No ambiguity should remain.

### 7b. Update `dissertation/governance/RESEARCH_ARCHITECTURE.md` Experiment 3

The dissertation currently has `~~Experiment 3~~` with a DROPPED marker. Match dr-classifier's Experiment 3 section which keeps it as a live section marked DROPPED (dr-classifier's approach is cleaner — it doesn't use strikethrough, just states DROPPED status and preserves historical content). Standardize the markup.

---

## CHANGE CATEGORY 8: Mixed Precision and Hardware Details

**Problem:** DR-classifier CLAUDE.md explicitly states `mixed_precision: true for ResNet-50, DISABLED for EfficientNet (fp16 overflow fix)`. The dissertation `methods/implementation.md` already has this (line 81). But `governance/RESEARCH_ARCHITECTURE.md` has a training configuration table that may not include this. DR-classifier's RESEARCH_ARCHITECTURE §4.0 table has `Maximum epochs | 50 (with early stopping)` while the implementation file says `20`.

### 8a. `dissertation/governance/RESEARCH_ARCHITECTURE.md` — §4.0 Training Config

Verify the training config table matches dr-classifier. Add `Mixed precision (fp16)` row with value `Enabled for ResNet-50; DISABLED for EfficientNet (fp16 overflow fix)` if missing. Verify max_epochs matches (dr-classifier says 50 in RESEARCH_ARCHITECTURE but 20 in CLAUDE.md — use 20 as the actual operational value from CLAUDE.md and implementation.md).

### 8b. `dissertation/governance/RESEARCH_ARCHITECTURE.md` — §4.0

Add the row if missing:
```
| Mixed precision (fp16) | Enabled for ResNet-50; DISABLED for EfficientNet (fp16 overflow fix) |
```

Fix max_epochs to 20 if it says 50 (match CLAUDE.md operational config).

**CHECK:** Verify `methods/implementation.md` and `governance/RESEARCH_ARCHITECTURE.md` agree on all training parameters.

---

## CHANGE CATEGORY 9: Per-Patient Binocular Blending in RESEARCH_ARCHITECTURE

**Problem:** DR-classifier's RESEARCH_ARCHITECTURE mentions per-patient binocular blending as an optional extension paragraph (§3.1). The dissertation's RESEARCH_ARCHITECTURE has this information scattered differently — it has a full section on PatientHead in the Model Architecture Layer but the §3.1 pipeline section doesn't include the binocular blending paragraph.

### 9a. `dissertation/governance/RESEARCH_ARCHITECTURE.md` — §3.1

Add after the augmentation integration paragraph:
```
**Optional Extension — Per-Patient Binocular Blending:** Applied in Experiment 1
configurations E and F. Blends paired left/right eye images per patient before
or during feature extraction, providing additional regularization via bilateral
context.
```

Verify this matches dr-classifier's §3.1 wording.

---

## CHANGE CATEGORY 10: VERSION_SYNC.md Updates

### 10a. `dissertation/governance/VERSION_SYNC.md`

Update the sync register to reflect all changes made in this session:

```
**Last Sync Date:** [TODAY'S DATE]
**Synced by:** Claude Code (sync with dr-classifier post-OD-fovea implementation)

## New Changes Applied (Post-V4.0)

| Change | Description |
|--------|-------------|
| CV folds | 5-fold → 3-fold in governance/INVARIANTS, governance/ARGUMENT_MAP, governance/RESEARCH_ARCHITECTURE |
| Stage 0 expansion | Stage 0 → Stage 0a (canonical flip) + Stage 0b (OD-fovea rotation normalization) |
| Stage 5 rotation σ | Fixed σ=13.0° → adaptive per-image σ from OD/fovea uncertainty (fallback 13.0°) |
| IT-1 wording | Updated to match dr-classifier verbatim (with Stage 0 expansion) |
| EyePACS size | Added "40% subset" and "~14,050 used for experiments" context |
| APTOS 2019 | Added explicit DROPPED annotation in IT-1 and DGL-1 |
| SC-1.3 | Confirmed REMOVED in dissertation (divergence from dr-classifier noted) |
| Mixed precision | Added fp16 details to RESEARCH_ARCHITECTURE training config |
| Binocular blending | Added optional extension paragraph to §3.1 pipeline section |
| SC-F contribution | Added OD-Fovea orientation normalization as supporting contribution |
| Glossary entries | Added OD-Fovea Rotation Normalization, updated Canonical Flip → Canonical Orientation |
```

### 10b. `~/dr-classifier/docs/VERSION_SYNC.md`

Add a "Third Sync Pass" section documenting that the dissertation was updated to reflect OD-fovea alignment, 3-fold CV corrections, and EyePACS 40% subset wording.

---

## POST-SYNC VERIFICATION

Run these checks after all changes are complete. Fix any failures before finishing.

### Check 1: No stale 5-fold references in active protocol
```bash
grep -rn "5-fold" ~/dissertation/governance/ ~/dissertation/methods/ ~/dissertation/experiments/ | grep -v "V3 Historical\|v1.0\|Historical:\|DROPPED\|was V3\|v2.1\|replaced\|replaces\|Note.*v3\|Note.*V3\|v3.0\|footnote\|changelog\|VERSION_SYNC\|5-fold CV →"
```
**Expected:** Zero results.

### Check 2: No standalone "canonical flip" as entire Stage 0
```bash
grep -rn "Stage 0.*Canonical Flip" ~/dissertation/governance/ ~/dissertation/methods/ | grep -v "Stage 0a\|Historical\|V3\|0b"
```
**Expected:** Zero results. Stage 0 should always mention both 0a and 0b, or use "Canonical Orientation" as the umbrella term.

### Check 3: EyePACS 40% subset mentioned
```bash
grep -rn "35,126" ~/dissertation/governance/ ~/dissertation/methods/ ~/dissertation/experiments/ | grep -v "40%\|Kaggle labeled partition"
```
**Expected:** Zero results for governance files (all should include 40% context). The `experiments/experimental-protocol.md` may use "Kaggle labeled partition" which is acceptable if consistent.

### Check 4: OD-fovea appears in pipeline descriptions
```bash
grep -rn "Stage 0" ~/dissertation/governance/INVARIANTS.md ~/dissertation/governance/RESEARCH_ARCHITECTURE.md ~/dissertation/methods/preprocessing-pipeline.md | grep -v "0b\|OD-fovea\|rotation normalization"
```
**Expected:** Zero results for lines that describe Stage 0 without mentioning 0b.

### Check 5: Document versions are consistent
```bash
for f in ~/dissertation/governance/INVARIANTS.md ~/dissertation/governance/ARGUMENT_MAP.md ~/dissertation/governance/RESEARCH_ARCHITECTURE.md ~/dissertation/governance/HYPOTHESIS.md ~/dissertation/governance/CONTRIBUTIONS.md ~/dissertation/governance/CENTRAL_THESIS.md; do
  echo "$f: $(head -5 "$f" | grep -i 'version')"
done
```
**Expected:** All show version 4.0 or 4.1 (if bumping version for this sync).

### Check 6: No internal contradictions on max_epochs
```bash
grep -rn "max.*epoch\|Maximum epoch\|max_epoch" ~/dissertation/governance/ ~/dissertation/methods/ ~/dissertation/experiments/ | grep -v "#\|comment"
```
**Expected:** All references agree (20 epochs, matching CLAUDE.md operational config).

### Check 7: Glossary completeness
```bash
grep -l "OD-Fovea\|od_fovea" ~/dissertation/glossary/GLOSSARY_EN.md
```
**Expected:** File found (new entry exists).

---

## COMPLETION CHECKLIST

Before finishing, confirm all of the following:

- [ ] All 5-fold → 3-fold changes applied in governance files
- [ ] Stage 0 expanded to include 0a (canonical flip) and 0b (OD-fovea rotation normalization)
- [ ] Stage 5 adaptive rotation σ documented
- [ ] IT-1 in INVARIANTS and ARGUMENT_MAP matches dr-classifier (with Stage 0 expansion)
- [ ] H-1 in INVARIANTS and HYPOTHESIS matches dr-classifier (with Stage 0 expansion)
- [ ] EyePACS "40% subset" and "~14,050 used" added everywhere
- [ ] APTOS 2019 DROPPED annotation added to IT-1 and DGL-1
- [ ] SC-F (OD-Fovea contribution) added to CONTRIBUTIONS.md
- [ ] Glossary updated (EN and KZ) with OD-Fovea entries
- [ ] preprocessing-pipeline.md Stage 0 section fully rewritten
- [ ] experimental-protocol.md Exp 2 ablation table updated
- [ ] MASTER_OUTLINE.md pipeline references updated
- [ ] Mixed precision row added to RESEARCH_ARCHITECTURE training config
- [ ] Binocular blending paragraph added to §3.1
- [ ] VERSION_SYNC.md updated in both repos
- [ ] All 7 verification checks pass

**Total estimated files modified:** 14–16 files across dissertation repo + 1 file in dr-classifier repo.
