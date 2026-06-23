---
name: od-fovea-heatmap-detector-plan
description: "Plan + PENDING governance edit for replacing the classical OD/fovea detector with a learned heatmap-regression detector; build spec lives in experiments/docs/od_fovea_heatmap_detector_brief.md; apply the INVARIANTS OD-3 edit only AFTER the detector is implemented & validated"
metadata:
  type: project
---

Decided 2026-06-18. Supersedes the classical Stage-1 detector (see [[preprocessing-od-fovea-polar]]).
The current classical detector localizes fovea unreliably (~5 OD-radii median, ~0 % within 2R;
it latches onto the dark vignette at native res) and its `confident` flag is fake (True for 100 %).

## Plan

- **Approach:** pre-trained, **frozen** heatmap-regression detector — U-Net (timm ResNet-18 /
  EfficientNet-B0 encoder) + **DSNT** head, 2 channels (OD, fovea) → probability heatmaps +
  sub-pixel coords + real confidence from heatmap peak/spread.
- **Trained on:** IDRiD localization GT (413 train; **103 test = honest hold-out, never trained on**).
- **References:** FundusPosNet (IEEE Access 2021, `github.com/bhargav-jb/FundusPosNet`); DSNT
  (`anibali/dsntnn`, also in Kornia); `berenslab/fundus_image_toolbox` (MIT) as baseline/fallback.
- **Build spec (for ChatGPT Codex, standalone repo):** `experiments/docs/od_fovea_heatmap_detector_brief.md`.
- **Integration contract:** keep `detect_od_fovea(image_rgb) -> ODFoveaResult` stable; add
  additive fields `od_confidence`, `fovea_confidence`, optional `od_heatmap`/`fovea_heatmap`.
  Detection must run on the FOV-cropped 512 frame (kills the vignette failure), then map coords
  back to input-image pixels. Re-validate with `scripts/validate_od_fovea_idrid.py` (test split).
- **Acceptance (IDRiD test):** fovea median < 1 OD-radius & ≥90 % within 1R; OD ≤0.5R & ≥95 % within 1R;
  confidence Spearman-correlates with actual error.
- **Post-integration:** reorder early stages (`flip → FOV crop+resize → detect → rotate → mask →
  flat-field → CLAHE`); cache OD/fovea coords+confidence into the Stage 0–4 cache; let polar CLAHE
  pivot on detected fovea when confident.

## PHASE 1 — TRAINED & VALIDATED (2026-06-23) ✅

Trained in WSL2 Ubuntu / `dr-classifier` conda env, RTX 3060 (Windows-native torch is CPU-only).
Canonical `configs/default.yaml` unchanged; a WSL-path copy is generated at
`experiments/od_fovea_detector/outputs/_wsl_config.yaml` (idrid_root → `/mnt/e/...`, absolute
weights/output paths; gitignored via `outputs/*.yaml`). Re-create it from `default.yaml` whenever
training on a WSL machine.

- **Run:** DSNT loss, seed=42, ResNet-18 U-Net, batch 8, lr 1e-3. Early-stopped at **epoch 136**
  (best val 0.0171 @ epoch 76, patience 60). ~41 s/epoch. Weights → `weights/od_fovea_unet.pt`
  (57 MB, gitignored — travels on E:). Artifacts: `outputs/{eval_report.json, montage.png, train_log.txt}`.
- **IDRiD TEST (103 imgs, honest hold-out) — acceptance PASSED:**
  - Fovea: median **0.107 R** (<1.0 ✓), **99.0 %** within 1R (≥90 % ✓).
  - OD: median **0.066 R** (≤0.5 ✓), **100 %** within 1R (≥95 % ✓). (vs classical baseline ~5R / ~0 %.)
  - Confidence: **fovea Spearman(σ_eff, err) ρ=0.441**, n=103, significant ✓. OD ρ=0.081 **n.s.** —
    acceptable: OD error is saturated (max 0.32R) so there's no error variance for confidence to track.
  - Runtime: GPU net-forward **34.6 ms/img** (≤50 ms ✓). Full-res standalone FOV crop adds ~176 ms CPU,
    but that crop becomes shared Stage 2 in-pipeline, so detector marginal cost ≈ the 35 ms forward.
- **Honest caveats (carry into Phase 2/4):** the single fovea failure >1R (IDRiD_053, 2.25R) was
  **NOT** caught by the low-confidence gate (conf 0.561 > 0.5 threshold). 10/103 flagged not-confident
  (captures elevated-error cases 0.6–0.7R but misses this one outlier). Threshold 0.5 is the config
  default; revisit calibration if the gate needs to catch catastrophic misses. Fovea mean (56 px) is
  pulled up by this one outlier; median (33 px) is the honest central tendency.
- **Next:** Phase 3 (demo overlay + clinician correction UI) — NOT started.

## PHASE 2 — INTEGRATED & GOVERNANCE APPLIED (2026-06-23) ✅

Learned detector ported to `experiments/src/preprocessing/od_fovea_net/` (model, dsnt, geometry,
confidence, utils, infer + `config.yaml`; weights resolved repo-relative to the standalone
`od_fovea_detector/weights/od_fovea_unet.pt` via the bundled config, overridable by
`OD_FOVEA_WEIGHTS`). The monorepo facade `src/preprocessing/od_fovea_detect.detect_od_fovea`
now **delegates to the learned net** (classical kept as `detect_od_fovea_classical` for
reference/tests); `ODFoveaResult` extended with additive `od_confidence`, `fovea_confidence`,
`od_heatmap`, `fovea_heatmap` (defaults preserve classical/cache-namespace callers).

- **No pipeline reorder needed:** the learned detector **FOV-crops internally** (geometry.crop_and_resize,
  mirroring Stage 2) and returns coords in input-image pixels — so "detection runs on the FOV-cropped
  frame" holds without physically reordering `pipeline.py` (which would double-crop and rotate a padded
  canvas). Call order unchanged; `canonical_orientation`/`stage_breakdown`/validate script untouched.
- **Real fallback gate (TASK #4):** when confident, Stage-5 polar CLAHE pivots on the detected fovea
  **projected into analysis space** (`_project_to_analysis` in pipeline.py); when not confident → FOV
  centroid. Pivot is plumbed through `_finish`, `precompute_deterministic`, `finish_from_cache`, and the
  cache (`cache_meta.csv` gains `fovea_x,fovea_y`; `load_cache_meta` returns 3-tuple, backward-compatible
  with old caches → None → centroid). **Live==cache verified bit-identical** (inference + seeded training,
  both fallback and confident paths, through the CSV+PNG round-trip).
- **In-repo validation reproduces acceptance** (`scripts/validate_od_fovea_idrid.py --splits test`,
  103 imgs): OD median 0.066 R / 100 % @1R; fovea median 0.107 R / 99 % @1R — matches the standalone
  eval_report.json. (Fixed a pre-existing Windows cp1251 unicode-arrow crash in that script's prints.)
- Tests: full `experiments/tests/` suite green (24 passed); `test_od_fovea_detect` repointed to the
  classical alias; `test_cache` updated for the new arities.

## GOVERNANCE — APPLIED at v6.1.0 (MINOR) on 2026-06-23 ✅

OD-3 / Stage-1 replacement text applied to `INVARIANTS.md` (and mirrored in
`RESEARCH_ARCHITECTURE.md`, `methods/preprocessing-pipeline.md`). **Fallback σ adopted as 15.0°**
(not the draft's 13.0°, per the code/eval value — resolved-decision 4b). Version bumped **6.0.0 → 6.1.0**
(MINOR: new substantive entity, no binding reversed); `VERSION_SYNC.md` scope block + file-status table
updated; `CHANGELOG.md` entry added. Explicitly states the detector is **pre-trained and frozen, not
co-trained** with the DR-CNN. HYPOTHESIS.md unaffected (H-1/Premise-3 name Stage 1 generically; H-2 does
not reference the detector implementation). **Still pending (separate narrative pass, does not gate the
bump):** chapter drafts (3.1.1, 3.1.3, 1.1.1, 2.2.1), assembled dissertation bundles, abstracts, glossary
entries that still describe the classical detector; and the formal git commit + `git tag v6.1.0` release step.

## (historical) PENDING governance edit — superseded by the APPLIED block above

`thesis/governance/INVARIANTS.md` is the supreme authority. Changing the
canonical OD-3 / Stage-1 definition is a MINOR-or-MAJOR version bump — also update
`VERSION_SYNC.md` and any downstream mentions (RESEARCH_ARCHITECTURE.md, methods/preprocessing-pipeline.md,
CLAUDE.md stage tables, HYPOTHESIS H-2 ablation if it references the classical detector).

**Current text (INVARIANTS.md, OD-3, Stage 1 bullet ~line 119):**

> - **Stage 1: OD-Fovea Rotation Normalization** — Classical CV detection of OD (brightest
>   region) and fovea (darkest region with distance prior); rotates image so OD→fovea axis is
>   horizontal. Fallback: skip rotation on low confidence. Augmentation rotation σ is adaptive
>   per-image from detection uncertainty (fallback σ = 13.0°). Always on.

**Proposed replacement text:**

> - **Stage 1: OD-Fovea Rotation Normalization** — A **pre-trained, frozen** heatmap-regression
>   detector (U-Net encoder + DSNT head, trained on IDRiD localization ground-truth) predicts
>   probability heatmaps for the optic-disc and fovea centers on the FOV-cropped frame; the image
>   is rotated so the OD→fovea axis is horizontal. Per-landmark confidence is derived from heatmap
>   peak sharpness and spatial spread. Fallback: skip rotation when confidence is below threshold.
>   Augmentation rotation σ is adaptive per-image from heatmap-derived localization uncertainty
>   (fallback σ = 13.0°). The detector is pre-trained and **frozen — not co-trained with the DR
>   classifier** — so the preprocessing pipeline remains a fixed transform and the central thesis
>   "model = preprocessing + CNN" is preserved. Always on. (Operationally, detection runs on the
>   FOV-cropped frame produced by Stage 2's crop/resize; stage numbering is retained.)

**Note for the editor:** confirm the fallback σ value (INVARIANTS says 13.0°; code constant
`_MAX_ROTATION_SIGMA` = 15.0° — reconcile during the edit). Also reconsider whether the literal
"fovea-centred" polar-CLAHE claim can now be made truthfully for high-confidence images.

---

## Implementation status (2026-06-23)

- **Phase 1 (train+validate):** DONE — frozen `weights/od_fovea_unet.pt`; IDRiD test acceptance met.
- **Phase 2 (pipeline integrate):** DONE — live pipeline uses the learned detector via the
  `src/preprocessing/od_fovea_detect.detect_od_fovea` facade (detector FOV-crops internally; no
  physical stage reorder). INVARIANTS OD-3 updated, versions synced to v6.1.0, σ reconciled to **15.0°**.
- **Phase 3 (demo discs + heatmap + drag-correct):** DONE.
  - Server: `ODFoveaPayload` gained `od_confidence`, `fovea_confidence`, `od_heatmap_png_b64`,
    `fovea_heatmap_png_b64` (analysis-space RGBA heatmaps); new `POST /api/od_fovea/correct`
    recomputes the overlay from corrected centers, inverts the Stage 0/1/2 affine to original-image
    pixels (exact round-trip verified for both flip states), and persists JSONL + content-addressed
    original images under `demo/server/data/od_fovea_corrections/` (gitignored; `OD_FOVEA_CORRECTIONS_DIR`).
  - Pipeline: `PreprocessingPipeline.stage_breakdown(with_heatmaps=…)` warps detector heatmaps into
    analysis space and returns a `transform` handle; `canonical_orientation(return_heatmaps=…)`.
  - Frontend: probability discs (opacity ∝ confidence), heatmap toggle, draggable OD/fovea markers,
    Save-correction button in `demo/web/src/tabs/_VisionWidget.js`; wired for non-GT uploads in `Demo.js`;
    EN/KZ i18n added. `correctOdFovea()` client in `_apiPredict.js`.
- **Phase 4 (feedback fine-tune):** DONE (2026-06-23, code) — two offline scripts in
  `od_fovea_detector/scripts/`:
  - `export_corrections.py` (torch-free): parses the demo `corrections.jsonl` store →
    deduped (latest-per-image) `Sample(image_id=hash, image_path, od_xy, fovea_xy)` in
    **original-image pixels** (the store already records `od/fovea_center_original`), dropping
    any correction whose SHA-256 matches an IDRiD **test** image (`idrid_test_hashes`) — no
    leakage. Reusable `load_correction_samples()` + CLI manifest.
  - `finetune_corrections.py`: starts from the frozen base `od_fovea_unet.pt`, mixes IDRiD-train
    + corrections oversampled by `finetune.correction_repeat`, early-stops on the held-out
    IDRiD-train slice (test never fit), saves a **versioned** `od_fovea_unet_vN.pt` + sidecar
    `.json` (base weights, exact correction hashes, acceptance), then runs the IDRiD-test
    acceptance gate (reuses `src.eval.evaluate_split`): exit 0 promotable / 2 regressed / 1
    nothing-to-do. Base weights never overwritten in place; promote by repointing
    `io.weights_path` / `OD_FOVEA_WEIGHTS`.
  - Config: new `finetune:` block in `configs/default.yaml` (epochs, lr 1e-4, correction_repeat,
    corrections_dir, acceptance bar). Detector stays **frozen vs the DR-CNN** (offline loop only).
  - Tests: 5 torch-free export tests (`tests/test_corrections_export.py`); full detector suite 16
    passed. **Operator step (needs WSL2/GPU + a non-empty store):** run the two scripts once real
    clinician corrections exist — no run has been executed yet (store is currently empty).
