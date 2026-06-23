# TASK — Learned OD/Fovea Heatmap Detector: train → integrate → demo correction → feedback retraining

**Status date:** 2026-06-23
**Branch of origin:** `feat/od-fovea-heatmap-detector` (commit `ab2491f`)
**Owner:** Yesmukhamedov N.S.
**Audience:** the next chat session (Claude/ChatGPT) that picks up implementation.

> This file is the single working brief for finishing the learned OD/fovea
> detector. It states **what already exists**, **what is left to do**, and the
> **exact contracts / files** to touch, so the work can be resumed cold in a
> different chat. Read it together with:
> - `experiments/docs/od_fovea_heatmap_detector_brief.md` — full build spec (§1–§11).
> - `PROJECT_MEMORY/od-fovea-heatmap-detector-plan.md` — plan + **PENDING INVARIANTS OD-3 governance edit**.
> - `PROJECT_MEMORY/preprocessing-od-fovea-polar.md` — why the classical detector is being replaced.

---

## 0. One-paragraph goal

We built a learned heatmap-regression detector that, for any color fundus image,
predicts probability heatmaps (and sub-pixel centers + genuine confidence) for the
**optic disc (OD)** and **fovea**. We must now (1) **train it on IDRiD** and pass the
acceptance criteria, (2) **wire it into the live preprocessing pipeline** in place of
the brittle classical detector, (3) **surface it in the demo web app** — draw the
probability discs/heatmaps over the fundus and let a clinician **drag/correct** the OD
and fovea centers, and (4) **persist those corrections and use them to fine-tune** the
detector (human-in-the-loop / active learning). The detector stays **pre-trained and
frozen** relative to the DR classifier, so the central thesis "model = preprocessing +
CNN" is preserved.

---

## 1. What already EXISTS (do not rebuild)

### 1.1 Standalone detector — `experiments/od_fovea_detector/` (committed, code-complete, UNTRAINED)
- U-Net (`timm` ResNet-18 default / EfficientNet-B0 option) + vendored **DSNT** head, 2 channels (OD, fovea). `src/model.py`, `src/dsnt.py`.
- IDRiD localization data loader + FOV-crop affine + Gaussian heatmap targets + augmentation. `src/data.py`, `src/geometry.py`.
- Losses: DSNT (Euclidean + Jensen–Shannon) default; MSE/BCE baseline behind a flag. `src/losses.py`.
- Training loop (deterministic, seed=42, early stop on held-out TRAIN slice). `src/train.py`.
- **Inference API** `detect_od_fovea(image_rgb) -> ODFoveaResult` reproducing the monorepo dataclass **plus** additive fields `od_confidence`, `fovea_confidence`, `od_heatmap`, `fovea_heatmap`. `src/infer.py`.
- Confidence from heatmap peak/spread: `confidence = exp(-sigma_eff / sigma_ref)`. `src/confidence.py`.
- Eval → metrics JSON (monorepo shape) + Spearman(σ_eff, error) + montage. `src/eval.py`.
- Config: `configs/default.yaml` (paths, σ, lr, epochs, backbone, heatmap size, seed).
- Tests: 9/9 torch-free passing; torch-gated contract + synthetic smoke test (`scripts/smoke_test.py`).
- **`weights/` and `outputs/` are EMPTY** (only `.gitkeep`). → **NOT trained yet.**

### 1.2 Live pipeline — still on the CLASSICAL detector (untouched on purpose)
- `experiments/src/preprocessing/od_fovea_detect.py` — classical CV `detect_od_fovea() -> ODFoveaResult` (no confidence fields; `confident` flag is effectively always True — the bug we are fixing).
- Called via `canonical_orientation(...)` inside `experiments/src/preprocessing/pipeline.py` (`_precompute_rgb` ~L205, `stage_breakdown` ~L399). `stage_breakdown` projects OD/fovea into analysis space as `od_fovea_analysis` and gates on `od_fovea_result.confident`.
- Stage order today: `flip → rotate(Stage1, classical detect) → FOV crop+resize(Stage2) → mask → flat-field → CLAHE`. **Detection currently runs BEFORE the FOV crop** — the root cause of the vignette failure.

### 1.3 Demo — shows the classical OD/fovea result (read-only, no correction)
- Server `demo/server/app/visualize.py` — `/api/visualize` returns `od_fovea` payload in **analysis space** (cropped 512² frame), schema `ODFoveaPayload` in `demo/server/app/schemas.py` (`od_center`, `od_radius`, `fovea_center`, `fovea_radius`, `angle_deg`, `rotation_sigma_deg`, `confident`, `space_w/h`, `flipped`). **No heatmap, no confidence fields, no correction endpoint.**
- Frontend renders the overlay in `demo/web/src/tabs/Demo.js` + `_VisionWidget.js` (also referenced in `ModelPipeline.js`, `ModelMethods.js`, `_idridSamples.js`). Static markers only — no drag/edit UI.
- Endpoints live in `demo/server/app/main.py`; `_predict_lock` serializes GPU calls.

### 1.4 Governance / docs
- **PENDING** INVARIANTS OD-3 / Stage-1 edit is written out verbatim in `PROJECT_MEMORY/od-fovea-heatmap-detector-plan.md` (apply ONLY after train+validate). Reconcile fallback σ (INVARIANTS says 13.0°, code constant `_MAX_ROTATION_SIGMA`=15.0°).

---

## 2. What is LEFT to do (the actual task)

Four phases. Phases 1→2 are required and ordered. Phases 3→4 (demo + feedback) can
start once Phase 2 lands a working facade, but need the trained weights from Phase 1.

### PHASE 1 — TRAIN + VALIDATE on IDRiD  *(blocking; produces the weights)*
Goal: a frozen `weights/od_fovea_unet.pt` that beats the classical baseline on the **103-image IDRiD test split**.

1. Dataset path **VERIFIED present 2026-06-23** — `configs/default.yaml::data.idrid_root` = `E:/datasets/IDRiD/C. Localization` exists with the expected layout:
   - `1. Original Images/{a. Training Set (413), b. Testing Set (103)}`
   - `2. Groundtruths/1. Optic Disc Center Location/{a. IDRiD_OD_Center_Training Set_Markups.csv, b. ...Testing Set...csv}`
   - `2. Groundtruths/2. Fovea Center Location/{IDRiD_Fovea_Center_Training Set_Markups.csv, ...Testing Set...csv}`
   No path change needed — go straight to training.
2. Train (in `dr-classifier` conda env, WSL2, RTX 3060):
   ```bash
   conda activate dr-classifier
   cd experiments/od_fovea_detector
   python -m src.train --config configs/default.yaml      # full run
   ```
   Early-stop/calibrate on a held-out slice of TRAIN only. **Never tune on the 103 test images.**
3. Evaluate on the honest hold-out:
   ```bash
   python -m src.eval --config configs/default.yaml --weights weights/od_fovea_unet.pt --split test
   ```
4. **Acceptance (test split only)** — must all hold:
   - **Fovea:** median error < 1.0 OD-radius AND ≥ 90% within 1 OD-radius (classical baseline: ~5 R, ~0% within 2R).
   - **OD:** median error ≤ 0.5 OD-radius AND ≥ 95% within 1 OD-radius.
   - **Confidence is informative:** positive, significant Spearman between σ_eff and actual error; low-confidence flag captures the worst cases.
   - Runtime ≤ ~50 ms/img GPU, ≤ ~300 ms CPU.
5. If fovea fails the bar with IDRiD alone: add §3.2 auxiliary OD-segmentation data (REFUGE/ADAM/RIGA → OD-center heatmaps) and/or re-sweep σ + augmentation **before** touching architecture.
6. Save `outputs/eval_report.json` + `outputs/montage.png`. Record exact train/test IDs (reproducibility, seed=42).
7. **Deliverable:** trained weights + eval report meeting acceptance. Decide weight storage (likely too big for git — keep under `experiments/od_fovea_detector/weights/` with a download link or Git LFS; keep `.gitignore` honest).

### PHASE 2 — INTEGRATE into the live monorepo pipeline  *(blocking; depends on Phase 1)*
Goal: the pipeline uses the learned detector, on the FOV-cropped frame, with real confidence and fallback.

1. **Port** `experiments/od_fovea_detector/src/infer.py` (+ `model.py`, `dsnt.py`, `confidence.py`, `geometry.py` as needed) into a new package `experiments/src/preprocessing/od_fovea_net/`. Drop weights into a configured path (no hardcoded paths — read from config YAML).
2. **Wrap behind the existing facade** `detect_od_fovea(image_rgb) -> ODFoveaResult` so `pipeline.py`, the demo server, and `scripts/validate_od_fovea_idrid.py` need no call-site changes. Extend the monorepo `ODFoveaResult` with the additive fields (`od_confidence`, `fovea_confidence`, `od_heatmap`, `fovea_heatmap`) — additive only, keep existing fields intact.
3. **Reorder early stages** so detection runs on the FOV-cropped frame:
   `flip → FOV crop+resize → detect → rotate → mask → flat-field → CLAHE`.
   Touch `pipeline.py` (`_precompute_rgb`, `_finish`, `stage_breakdown`) and `canonical_orientation`. Keep INVARIANTS stage **numbering** ("Stage 1") even though detection now executes after the Stage-2 crop — note this operationally (the governance text already accounts for it).
4. **Real fallback gate:** when `od_confidence`/`fovea_confidence` < threshold → skip rotation normalization AND pivot polar-CLAHE on the FOV centroid instead of the detected fovea (the `fovea_xy` override already exists in `polar_clahe.py`). When confident → pivot polar-CLAHE on the detected fovea.
5. **Re-validate in-repo:** `python scripts/validate_od_fovea_idrid.py` → confirm the Phase-1 acceptance numbers reproduce inside the monorepo (this script historically reported train+test together — make sure the comparison is test-split honest).
6. **Cache:** add OD/fovea coords + confidence into the Stage 0–4 precompute cache (see `PROJECT_MEMORY/v5-cache-throughput.md`) so detection isn't recomputed per epoch. Coords are deterministic once weights are frozen.
7. **GOVERNANCE (apply only now, after validation passes):** apply the OD-3 / Stage-1 replacement text from `PROJECT_MEMORY/od-fovea-heatmap-detector-plan.md` to `thesis/governance/INVARIANTS.md`; bump version (MINOR or MAJOR per `VERSIONING_POLICY.md`); update `VERSION_SYNC.md` and downstream mentions (`RESEARCH_ARCHITECTURE.md`, `thesis/.../methods/preprocessing-pipeline.md`, `CLAUDE.md` stage tables, `experiments/CLAUDE.md`, HYPOTHESIS H-2 ablation if it references the classical detector). Reconcile fallback σ (13.0° vs 15.0°). State explicitly: detector is **pre-trained and frozen, not co-trained** with the DR-CNN.

### PHASE 3 — DEMO: draw heatmap discs + clinician correction UI  *(depends on Phase 2 facade)*
Goal: the web demo shows the OD/fovea probability discs/heatmaps and lets the user drag the centers to correct them.

1. **Server:** extend `ODFoveaPayload` (`demo/server/app/schemas.py`) with `od_confidence`, `fovea_confidence`, and base64 heatmap PNGs (`od_heatmap_png_b64`, `fovea_heatmap_png_b64`) aligned to the analysis-space `fov_base` frame. Update `demo/server/app/visualize.py::_od_payload` / `compute_visualization` to emit them from the new facade.
2. **Correction endpoint:** add `POST /api/od_fovea/correct` in `demo/server/app/main.py` accepting `{image_id|image hash, eye, od_center_corrected, fovea_center_corrected, space_w/h, original_payload, user/notes}`. Validate password gate (reuse `_require_password`). Persist each correction record (see Phase 4 store). Return the corrected payload (recompute angle/distance/rotation_sigma from the corrected centers so the overlay updates).
3. **Frontend overlay + edit (`demo/web/src/tabs/Demo.js`, `_VisionWidget.js`):**
   - Render the OD/fovea **probability discs** (radius = detected radius; opacity from confidence) and an optional heatmap layer toggle, over the analysis-space `fov_base` image.
   - Make OD and fovea center markers **draggable** (pointer events → coords in `space_w/h`). Show confidence + "low-confidence, please verify" when below threshold.
   - "Save correction" button → calls `/api/od_fovea/correct`; re-render with returned payload. Keep coordinate frame consistent (analysis space, `flipped=false`).
4. i18n: add EN/KZ strings (`demo/web/src/i18n.js`) for the new controls. Keep version-marker policy (no `V5`/version strings outside `thesis/`).

### PHASE 4 — FEEDBACK LOOP: persist corrections → fine-tune the detector  *(depends on Phase 3)*
Goal: turn clinician corrections into new training signal and (re)fine-tune the frozen detector offline.

1. **Correction store:** define a durable schema/location for corrections — e.g. `demo/server/data/od_fovea_corrections/` (JSONL or SQLite): record image hash/id, eye, **original image bytes or a stable reference**, corrected OD/fovea coords mapped back to **original-image pixels** (invert the analysis-space affine — reuse the detector's forward/inverse affine), space dims, confidence-at-capture, timestamp, reviewer. NOT in git (datasets live on `E:/`); document the path in config.
2. **Export → training format:** a script `experiments/od_fovea_detector/scripts/export_corrections.py` that converts the correction store into the same `(image, od_xy, fovea_xy)` format `src/data.py` consumes (original-pixel coords + FOV-crop affine → 512 frame → Gaussian targets).
3. **Fine-tune (offline, human-in-the-loop / active learning):**
   - New mode in `src/train.py` (or `scripts/finetune_corrections.py`): start from `weights/od_fovea_unet.pt`, mix IDRiD train + corrections (weight corrections up; small lr; few epochs; keep IDRiD-test held out for acceptance).
   - **Re-run Phase-1 acceptance on the IDRiD test split after each fine-tune** — never regress below the acceptance bar. Version the weights (`od_fovea_unet_vN.pt`) and log which corrections went into each.
   - The detector remains **frozen during DR-classifier training** — fine-tuning happens only in this offline detector loop, so "model = preprocessing + CNN" is preserved. Make this explicit in any governance note.
4. **Active-learning prioritization (optional, nice-to-have):** surface lowest-confidence detections first for review (σ_eff ranking) so corrections target the worst cases.

---

## 3. Binding contracts (don't drift)

- **Inference signature** stays `detect_od_fovea(image_rgb: np.ndarray) -> ODFoveaResult`; new fields are **additive only**. Input = RGB uint8 `(H,W,3)` arbitrary resolution; function FOV-crops internally and returns coords in **input-image pixels**. Weights load once (lazy singleton), CPU+CUDA, no hardcoded paths, `pathlib.Path`, type hints + Args/Returns docstrings, all code/comments in English.
- **Confidence must track error** (proven by Spearman in the eval report) — it gates the fallback. A diffuse/multi-modal heatmap ⇒ low confidence.
- **No test-set leakage** ever: train on 413 IDRiD, evaluate on 103. Corrections in Phase 4 must NOT include the 103 IDRiD test images.
- **Detector is frozen** relative to the DR classifier. Preprocessing stays a fixed transform.
- **Governance is supreme:** the OD-3 edit lands only after in-repo validation; bump versions and sync per `thesis/governance/VERSIONING_POLICY.md`.

## 4. Acceptance for "task complete"
- [x] Phase 1: trained weights + `eval_report.json` meet all acceptance criteria on IDRiD test. *(2026-06-23)*
- [x] Phase 2: live pipeline uses the learned detector on the FOV-cropped frame (detector crops internally — no physical stage reorder needed); `validate_od_fovea_idrid.py` reproduces the numbers (OD 0.066 R/100 % @1R, fovea 0.107 R/99 % @1R); INVARIANTS OD-3 updated + versions synced to **v6.1.0** (σ reconciled to 15.0°). *(2026-06-23)* — remaining: narrative chapter/abstract/glossary sync + `git tag v6.1.0` (separate doc-release pass).
- [x] Phase 3: demo draws OD/fovea probability discs (opacity ∝ confidence) + a togglable analysis-space probability-heatmap layer; the clinician can drag both centers and save the correction. Server: `ODFoveaPayload` extended (`od_confidence`, `fovea_confidence`, `od_heatmap_png_b64`, `fovea_heatmap_png_b64`); `POST /api/od_fovea/correct` recomputes the overlay from the corrected centers, maps them back to original-image pixels (inverse Stage 0/1/2 affine — exact round-trip verified), and persists a JSONL record + content-addressed original image to `demo/server/data/od_fovea_corrections/` (gitignored, configurable via `OD_FOVEA_CORRECTIONS_DIR`). Pipeline: `stage_breakdown(with_heatmaps=…)` warps detector heatmaps into analysis space + emits an inverse-transform handle. Frontend: discs/heatmap/drag/save in `_VisionWidget.js`, wired for non-GT uploads in `Demo.js`, EN/KZ i18n. *(2026-06-23)* — remaining for Phase 4: export script + offline fine-tune loop consuming the store.
- [x] Phase 4: corrections persisted (Phase 3 store), **exportable**, and an offline fine-tune loop regenerates versioned frozen weights gated on IDRiD-test acceptance. *(2026-06-23)* — `scripts/export_corrections.py` parses the JSONL store → deduped (latest-per-image) `(image, od_xy, fovea_xy)` samples in original-image pixels, dropping any correction whose SHA-256 matches an IDRiD **test** image (no leakage). `scripts/finetune_corrections.py` starts from the frozen base weights, mixes IDRiD-train + corrections (oversampled `finetune.correction_repeat`), early-stops on the held-out IDRiD-train slice, saves a versioned `weights/od_fovea_unet_vN.pt` + sidecar JSON (base weights, exact correction hashes, acceptance), then runs the IDRiD-test acceptance gate — exit 0 promotable / 2 regressed / 1 nothing-to-do; the base weights are never overwritten in place. Config: new `finetune:` block in `configs/default.yaml`. Detector stays **frozen vs the DR-CNN** (offline loop only). Tests: 5 torch-free export tests (`tests/test_corrections_export.py`); full detector suite green (16 passed). — operator step (needs WSL2/GPU + a non-empty store): run the two commands above once corrections exist.

## 4b. Resolved decisions / chosen defaults (override only with a reason)
These were the only genuinely open points; defaults are chosen so the task is unblocked end-to-end. None block Phase 1.
- **Weight storage:** keep trained weights under `experiments/od_fovea_detector/weights/od_fovea_unet.pt`, **gitignored** (already in `.gitignore`). They travel via the E: drive like the datasets, so git-LFS is not required. If the weights must be shared off-drive, add a download link in the detector README. Version fine-tuned weights as `od_fovea_unet_vN.pt`.
- **Fallback σ reconcile:** code uses `15.0°` (`_MAX_ROTATION_SIGMA` and `config.max_rotation_sigma_deg`); INVARIANTS text says `13.0°`. **Adopt 15.0°** as the single source of truth and fix the INVARIANTS number during the Phase-2 governance edit (it is the value the code/eval actually use).
- **Confidence threshold:** `config.threshold = 0.5` on `confidence = exp(-σ_eff/σ_ref)`; recalibrate on the held-out TRAIN slice in Phase 1, then freeze. Below threshold ⇒ `confident=False` ⇒ skip rotation + FOV-centroid polar-CLAHE pivot.
- **Corrections store format (Phase 4):** JSONL at `demo/server/data/od_fovea_corrections/corrections.jsonl` (one record/line; gitignored). Promote to SQLite only if volume/concurrency demands it.
- **Image identity for corrections (Phase 3/4):** key each correction by a content hash (SHA-256 of the original upload bytes) + eye; store corrected centers in **original-image pixels** (invert the analysis-space affine using the detector's forward/inverse transform). The demo is otherwise stateless — corrections are the only persisted state.
- **Auxiliary OD-seg data (REFUGE/ADAM/RIGA):** contingency only — pull in **only if** fovea fails the Phase-1 bar with IDRiD alone. Not required to start.

## 5. Key files index
| Area | Path |
|------|------|
| Standalone detector | `experiments/od_fovea_detector/` (src/, configs/default.yaml, weights/, outputs/) |
| Build spec | `experiments/docs/od_fovea_heatmap_detector_brief.md` |
| Classical detector (to be replaced) | `experiments/src/preprocessing/od_fovea_detect.py` |
| Pipeline integration points | `experiments/src/preprocessing/pipeline.py` (`_precompute_rgb`, `_finish`, `stage_breakdown`), `canonical_orientation.py`, `polar_clahe.py` |
| In-repo validation | `experiments/scripts/validate_od_fovea_idrid.py` |
| Demo server | `demo/server/app/{main,visualize,schemas,preprocessing,inference}.py` |
| Demo frontend | `demo/web/src/tabs/{Demo,_VisionWidget,ModelPipeline}.js`, `i18n.js` |
| Governance (pending edit) | `thesis/governance/INVARIANTS.md` + `VERSION_SYNC.md`; text in `PROJECT_MEMORY/od-fovea-heatmap-detector-plan.md` |
