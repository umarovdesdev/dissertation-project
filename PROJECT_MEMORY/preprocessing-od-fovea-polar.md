---
name: preprocessing-od-fovea-polar
description: "OD/fovea classical detector unreliable (fovea fails); DECIDED 2026-06-18 to replace it with a learned heatmap detector (see [[od-fovea-heatmap-detector-plan]]); polar CLAHE is Stage-5 default, pivots on FOV centroid until the new detector lands"
metadata:
  type: project
---

Consolidates the former `od-fovea-detector-unreliable-polar-centroid` + `polar-clahe-now-default-retrain` memories. TASK-fix.md #4 + #2 resolved 2026-06-07 on `feat/v5-cache-colab`.

## DECISION 2026-06-18 — replace classical detector with a learned heatmap detector

The classical detector below is being retired. Approach chosen: a **pre-trained, frozen
heatmap-regression detector** (U-Net timm encoder + DSNT head, 2 channels OD/fovea, trained
on IDRiD localization GT) producing **probability heatmaps** + sub-pixel coords + a **real
confidence** from heatmap peak/spread. Reference: FundusPosNet (IEEE Access 2021), DSNT
(anibali/dsntnn / Kornia), berenslab/fundus_image_toolbox (MIT) as baseline. Full build
spec for the standalone Codex project: `experiments/docs/od_fovea_heatmap_detector_brief.md`.
Integration contract keeps `detect_od_fovea(image_rgb) -> ODFoveaResult` stable (+ new
`od_confidence`/`fovea_confidence`/heatmap fields). Pending governance edit (apply after
implementation): see [[od-fovea-heatmap-detector-plan]]. **Once it lands, polar CLAHE will
pivot on the detected fovea when confidence is high**, falling back to FOV centroid otherwise
— so the divergence noted in #2 below closes for high-confidence images.

## #4 — OD/fovea detector is unreliable (IDRiD-validated)

`scripts/validate_od_fovea_idrid.py` vs IDRiD localization GT (516 imgs, `experiments/outputs/validation/od_fovea_idrid_metrics.json`):
- OD localization: median ~0.67 OD-radii error, ~65% within 1R — mediocre but usable.
- **Fovea localization fails**: median ~5 OD-radii (~0% within 2R). The darkest-in-annulus search latches onto the dark vignette at native resolution.
- **`ODFoveaResult.confident` is useless as a gate**: `True` for 100% of images including every fovea failure. Do NOT rely on it to trigger fallbacks.
- Detection runs at native full-res in the pipeline (`canonical_orientation` before crop), so this is representative of production, and also makes Stage-1 rotation suspect.

## #2 — Polar adaptive CLAHE is now the Stage-5 default

Stage 5 has two modes via `config.clahe_mode`: `"polar"` (new, `polar_clahe.py`) and `"tiles"` (old `upgraded_clahe.py`). **Presets + `configs/default.yaml` set `polar`** (dataclass default stays `tiles` so bare `PreprocessingConfig()` and pre-existing tests keep tile behaviour). So real training (exp1 B/D via `from_preset`), Exp 2 sweep, and the demo backend (`server` via `from_preset`) all run polar now.

Polar CLAHE pivots the polar grid on the **FOV-mask centroid, NOT the detected fovea** (because the detector fails). Centroid is deterministic, needs no new cache scalar (derived from cached `fov_mask` in `_finish`), and ≈ central retina in a centred crop. `apply_polar_clahe` accepts an optional `fovea_xy` override used only if it lands inside the FOV. Divergence from the thesis's literal "fovea-centred" claim — the live `/api/visualize` polar panel matches the static demo images in algorithm/look but not pixel-exactly.

**Retrain consequence:** polar **changes the CNN input feature space**. Any already-trained Config-D checkpoint (interim APTOS + in-flight EyePACS) was trained on **tile** CLAHE and must be **retrained** to be thesis-faithful. The demo `/api/visualize` panel is preprocessing-only so it shows polar today regardless of checkpoint. See [[config-d-kaggle-source]], [[demo-stack]].

**Server == experiments:** `server/app/__init__.py` puts `experiments/` on `sys.path`; the server imports the same `src.preprocessing` (no copy) and builds via `from_preset` → polar.

**Performance (open):** polar ≈160 ms/512² img vs ≈6 ms tiles (~26×). Fine for the demo (1 img/request); the concern is **training** — Stage 5 runs per-epoch *after* the Stage 0–4 cache cut (see [[v5-cache-throughput]]), so 160 ms/img on CPU can re-starve the GPU on a full EyePACS epoch. Mitigation (not yet done): cache per-image sector boundaries + LUTs. If detector params are ever retuned (`od_blur_sigma`/`fovea_*` in `configs/default.yaml`), re-run the #4 validation before trusting the fovea pivot.
