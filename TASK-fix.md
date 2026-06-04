# TASK-fix.md — Three correctness fixes (FOV mask render · polar CLAHE · per-dataset configs)

**Owner:** Yesmukhamedov N.S. (IITU)
**Executor:** Claude Code (plan/review) — implementation between sessions
**Created:** 2026-06-03
**Branch:** `feat/v5-cache-colab`

Three issues raised for investigation. Each is diagnosed below with exact
file/line references, root cause, and a concrete fix plan. Items **1** and **2**
are confirmed bugs/divergences with a clear fix. Item **3** needs one design
decision before implementation (flagged at the end).

---

## 1. FOV mask is drawn incorrectly in the demo

### Where
- Render: `demo/src/tabs/_VisionWidget.js:55–74` (the `showMask` toggle).
- Payload source: `server/app/visualize.py:89–98` (`compute_visualization`).
- Mask origin: `experiments/src/preprocessing/pipeline.py:381–382`
  (`crop_and_resize(oriented, target_size)` → `fov_mask`).

### What happens now
`VisionWidget` toggles the **same `<img>` box** between two completely different
coordinate spaces:

```js
// _VisionWidget.js:62-66
<img src={showMask ? maskSrc : src} ... objectFit:'contain' />
```

- `src` = the **raw upload**: original resolution, original aspect ratio,
  **not** canonically flipped, **not** OD–fovea rotated.
- `maskSrc` = `data.fov_mask_png_b64` = the FOV mask returned by the backend,
  which is **512×512, square, post-flip (left→right), post-rotation** — it is
  produced *after* Stage 0 (flip), Stage 1 (rotation), Stage 2 (isotropic crop +
  resize) in `stage_breakdown` (`pipeline.py:381`).

So when the user flips the toggle, the mask does **not** overlay the fundus it
was computed from: for a left eye it appears mirrored, the aspect ratio differs
(square vs. original), and the rotation/crop shifts everything. Visually it
reads as "the mask is in the wrong place / wrong shape."

The OD–fovea overlay drawn on the **un-flipped raw `src`** (`_VisionWidget.js:67–73`)
has the same class of bug: `_od_payload` is built with `space_w=w0, space_h=h0`
(the *original* image dims, `visualize.py:87,98`) while the OD/fovea centres come
from `canonical_orientation(...)` which works in **oriented** space
(`pipeline.py:371`). `project()` then tries to undo the flip with a single
`flipped` mirror (`_VisionWidget.js:16–22`) but cannot undo the rotation or the
crop, so the markers can sit off the optic disc.

### Root cause
Two different coordinate spaces are being composited into one 200px box without
a common reference frame. The mask lives in **analysis space** (512², flipped,
rotated, cropped); the input image lives in **raw upload space**.

### Fix options (pick one)
**Option A — overlay the mask on the analysis-space image (recommended).**
Return the **oriented + cropped RGB** (the `fov_crop_resize` panel, which is
already computed at `pipeline.py:382`) as a base image, and render the mask as a
semi-transparent tinted overlay *on top of that* instead of on the raw upload.
Then mask and base share the same 512² flipped/rotated frame and align exactly.
- `visualize.py`: add `fov_base_png_b64` (the `fov_crop_resize` stage RGB) to the
  payload, alongside `fov_mask_png_b64`.
- `_VisionWidget.js`: when `showMask`, draw `fov_base` as the `<img>` and
  composite the mask as a green/teal alpha overlay (e.g. mask → RGBA where
  mask>0 ⇒ teal@40%). Keep `objectFit:'contain'` — both are 512² so they letterbox
  identically.

**Option B — keep raw input as base, transform the mask back to upload space.**
Backend would need to invert Stage 0–2 (un-rotate, un-crop, un-resize, un-flip)
to project the mask into raw-upload pixels. More code, more failure modes, and
the OD/fovea markers need the same inverse. Not recommended.

### Also fix (same change)
Make the OD/fovea markers consistent with whatever base image is chosen:
- If Option A: draw markers over the **oriented** image, set
  `space_w/space_h = 512/512`, and **drop the `flipped` re-mirror** in
  `project()` (the coords are already in flipped space). Verify against
  `od_fovea_detect` output space.

### Acceptance
- Toggle "Show FOV mask" on a **left** eye and a **right** eye: the white mask
  region coincides with the fundus disc area in the displayed base image; no
  mirroring, no aspect jump.
- OD circle sits on the optic disc, fovea circle near the macula, for confident
  cases.

---

## 2. CLAHE must run in **polar** (fovea-centred adaptive) form, not Cartesian tiles

### Where
- **Demo image generator (the intended algorithm):**
  `demo/public/pipeline/helpers/s5_polar_adaptive.py` — fovea-centred polar grid,
  log-spaced radial rings (`Nr_base=8`, `r∝(i/N)^1.5`), vessel-density-driven
  **non-uniform angular sectors** (72 fine bins → adaptive merge), dual-constraint
  clip, polar bilinear interpolation.
- **Production pipeline (what the model actually runs):**
  `experiments/src/preprocessing/upgraded_clahe.py:115–154`
  (`upgraded_clahe_l_channel`) — a plain **8×8 Cartesian tile** grid.
- Wired in at `experiments/src/preprocessing/pipeline.py:243–249` (train) and
  `pipeline.py:400–405` (inference / `stage_breakdown`).
- Backend `/api/visualize` CLAHE panel therefore also shows the **Cartesian**
  version (`server/app/visualize.py:89`, via `stage_breakdown`).

### The divergence
The dissertation describes Stage 5 as a **fovea-centred adaptive polar CLAHE**,
and the demo static images under `demo/public/.../stage_5_clahe/polar/` are
generated by `s5_polar_adaptive.py`. But the **real model** (training, caching,
and the live `/api/visualize` panel) uses a **rectangular tile** CLAHE
(`upgraded_clahe.py`). The feature space the CNN sees does **not** match the
pipeline the thesis claims (and the demo shows). Per the central thesis
("model = preprocessing + CNN"), this is a substantive mismatch, not cosmetic.

### Fix plan
Port the polar adaptive CLAHE from `s5_polar_adaptive.py` into the production
pipeline as the Stage 5 implementation.

1. **New module** `experiments/src/preprocessing/polar_clahe.py` containing a
   reusable, framework-clean port of the polar algorithm:
   - `vessel_detection(L)` — multi-scale Hessian vesselness (lines 64–79).
   - `compute_nonuniform_sectors(...)` — adaptive angular sectors (lines 105–160).
   - `build_luts(...)` + `interpolate_nonuniform(...)` — dual-constraint clip +
     polar bilinear interpolation (lines 163–242).
   - `apply_polar_clahe(image_rgb, fovea_xy, fov_mask, params)` public entry,
     mirroring `apply_upgraded_clahe`'s RGB→LAB(L)→RGB contract.
   - Reuse the dual-constraint params already in `ClaheParams`
     (`clip_factor=2.0`, `global_threshold=0.01` — identical constants to the
     demo script's `CLIP_FACTOR`/`GLOBAL_THRESHOLD`).
2. **Fovea centre is required.** The demo script reads it from `coords.json`;
   the production path must take it from the **Stage 1 OD-fovea detector**
   (`od_fovea_detect.ODFoveaResult.fovea_center`), transformed into post-crop
   512² space. The pipeline already carries `od_fovea_result` through
   `_precompute_rgb`/`stage_breakdown`, so thread the (already-computed) fovea
   centre into the CLAHE call. Add a deterministic fallback to **image centre**
   when `od_fovea_result.confident is False` (so low-quality uploads still run).
3. **Wire into pipeline.py** behind a config switch so we can A/B the two and
   keep the ablation honest:
   - `config.py`: add `clahe_mode: "polar" | "tiles"` (+ polar params:
     `clahe_radial_rings`, `clahe_fine_bins`, `clahe_min_sector_area_frac`).
   - `pipeline.py:243` and `:400`: dispatch to polar vs. tile CLAHE on
     `config.clahe_mode`; pass `fovea_xy` + `fov_mask`.
   - `configs/default.yaml:46–50`: add `clahe_mode: polar` and the polar params.
4. **Caching note (important):** the V5 Stage 0–4 cache (this branch's whole
   point) stops *before* CLAHE, so the cache is unaffected. But CLAHE now needs
   the **fovea centre + FOV mask** at Stage 5 — make sure both are persisted/
   recomputed for the cached path (`_finish` already receives `od_fovea_result`
   and the mask; verify the cached loader restores the fovea scalar, not just the
   two rotation scalars). See `pipeline.py:283,312`.
5. **Performance:** the polar path is heavier than 8×8 tiles (vessel detection +
   per-ring sector search). Since CLAHE is per-epoch (stochastic, Stage 5 is
   *after* the cache cut), benchmark cost per image; if it dominates, consider
   caching the **sector boundaries + LUTs** keyed on the cached Stage-0–4 image
   (they depend only on geometry + flat-fielded L, both deterministic per image).
6. **Tests:** add `tests/test_polar_clahe.py` — output shape/dtype preserved,
   masked region only, deterministic at inference, graceful fovea fallback.

### Acceptance
- `stage_breakdown(...)["stages"]` "clahe" panel matches the polar look of
  `demo/public/.../stage_5_clahe/polar/*.png` for the same input.
- The live `/api/visualize` CLAHE panel and the static demo image agree.
- Exp 2 CLAHE sweep (`exp2_ablation.py`, `clahe_sweep`) still runs (sweep now
  varies the polar `clip_factor`).

> ⚠ This changes the model's input feature space. Any **already-trained** Config-D
> checkpoint was trained on **tile** CLAHE and must be **retrained** to be
> thesis-faithful once polar CLAHE lands. Note this against the interim APTOS
> checkpoint and the in-flight EyePACS run (see `TASK.md §1`).

---

## 3. CNN configs/normalization — A & C ready, the rest must be prepared per-dataset

### Where
- Config matrix: `experiments/configs/default.yaml:138–204`.
- Stage 7 normalize: `default.yaml:71–79` (`dataset_mean/std: null` placeholders,
  `normalize_mode: dataset_specific`, ImageNet fallback for baseline).
- Stats script: `experiments/scripts/compute_dataset_stats.py` — **EyePACS-only**
  discovery (`_discover_eyepacs`), writes `data/processed/eyepacs_norm_stats.json`.
- Existing stats: only `eyepacs_norm_stats.json` exists (and an interim APTOS one
  per memory).

### Current state (what's actually ready)
| Exp / Config | Preproc | Channels | Normalization | Status |
|---|---|---|---|---|
| **Exp1 A** | baseline | 3 | ImageNet (`imagenet_mean/std`) | ✅ ready — no per-dataset stats needed |
| **Exp1 C** | baseline | 3 | ImageNet | ✅ ready |
| **Exp1 B** | full | 4 | `eyepacs_norm_stats.json` | ✅ stats exist |
| **Exp1 D** | full | 4 | `eyepacs_norm_stats.json` | ✅ stats exist |
| **Exp2** (ablation/sweeps) | mixed | 3/4 | EyePACS | ⚠ uses EyePACS stats; OK |
| **Exp3** EyePACS→APTOS | full | 4 | **decision needed** | ❌ |
| **Exp4** EyePACS→IDRiD/Clinical | full | 4 | **decision needed** | ❌ |
| **Exp5** EyePACS→IDRiD/Messidor-2 | full | 4 | **decision needed** | ❌ |
| **Exp6** EyePACS→DDR/ODIR/RFMiD | full | 4 | **decision needed** | ❌ |
| **Exp7** IDRiD→Clinical | full | 4 | **IDRiD stats needed** | ❌ |

So the user's framing is correct: **A and C (Exp1 baseline) are done**; the
remaining full-pipeline configs and the cross-dataset experiments need their
normalization prepared "based on the datasets."

### Decision (resolved 2026-06-03): convention (a) — EyePACS train stats
The candidate confirmed **convention (a)**: Exp 3–6 normalize their test sets
with the **EyePACS train** mean/std the model was trained on (no leakage,
standard transfer protocol, preserves the domain shift being measured). **No new
stats files are needed for Exp 3–6** — they reuse `eyepacs_norm_stats.json`. The
only new file required is **`idrid_norm_stats.json`** for Exp 7 (trains on IDRiD).
The two conventions, for the record:

- **(a) Train-set stats everywhere (no leakage, standard transfer protocol):**
  normalize the test datasets with the **EyePACS train** mean/std the model was
  trained on. This is the methodologically safe default for measuring domain
  shift — the test set must not re-centre itself. With this convention, **no new
  stats files are needed** for Exp 3–6; they reuse `eyepacs_norm_stats.json`.
- **(b) Per-dataset stats:** compute mean/std on each target dataset and
  normalize with those. This *removes* part of the domain shift you are trying to
  measure (it standardises away device/intensity differences), so it would
  understate Exp 5/6 degradation. Generally **not** what H-4/H-6/H-7 want.

**Exp 7** is different — it *trains* on IDRiD, so it genuinely needs an
**IDRiD-specific** `data/processed/idrid_norm_stats.json`.

### Plan
1. **Convention (a) adopted** for Exp 3–6 → reuse EyePACS train stats; document it
   explicitly in `experimental_protocol.md` so reviewers see the choice.
2. **Generalize `compute_dataset_stats.py`** beyond EyePACS so we can produce the
   one stats file Exp 7 needs (and any future train-on-X run):
   - Add `_discover_<dataset>` for IDRiD (and parameterize discovery by a
     `--dataset {eyepacs,idrid,aptos,...}` flag); reuse the dataset loaders in
     `src/data/datasets.py` rather than re-globbing.
   - Output `data/processed/<dataset>_norm_stats.json`.
3. **Compute IDRiD stats** for Exp 7 and wire its consumption in
   `exp7_clinical.py` (mirror how `exp1_factorial.py` auto-loads
   `eyepacs_norm_stats.json`).
4. **Verify the loader/fallback contract:** confirm that each experiment, when
   `normalize_mode: dataset_specific` and the relevant `*_norm_stats.json` is
   present, loads it; and that baseline configs (A/C) bypass it to ImageNet.
   Right now `default.yaml` has `dataset_mean/std: null`, so the load path must
   come from the per-dataset JSON, not the YAML — confirm exp scripts do that.

### Acceptance
- `data/processed/idrid_norm_stats.json` exists; Exp 7 loads it.
- Exp 3–6 documented + confirmed to normalize test sets with EyePACS train stats.
- Exp1 A/C confirmed still on ImageNet; B/D on EyePACS stats. No regression.
- Exp 3–6 normalize test sets with EyePACS train stats (convention a, confirmed).

---

## Suggested order of work
1. **#1 FOV mask render** — self-contained, demo-only, low risk, immediate visual win.
2. **#3 normalization decision + IDRiD stats** — unblocks Exp 3–7 planning; small code.
3. **#2 polar CLAHE** — largest change; touches the model's feature space and forces
   a Config-D retrain, so sequence it deliberately against the in-flight training in
   `TASK.md`.

All open questions resolved (normalization convention confirmed 2026-06-03).
