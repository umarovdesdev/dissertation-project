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
- **Next:** Phase 2 (integrate into live pipeline) — NOT started.

## PENDING governance edit — apply ONLY after the detector is implemented & validated

`thesis/governance/INVARIANTS.md` is the supreme authority (currently v6.0.0). Changing the
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
