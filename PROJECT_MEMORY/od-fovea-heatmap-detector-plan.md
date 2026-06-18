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
