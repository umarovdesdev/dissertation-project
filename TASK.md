# TASK.md — Config-D training (Kaggle/Colab) + Real Demo + Academic Beta launch

**Owner:** Yesmukhamedov N.S. (IITU)
**Executor:** Claude Code (plan/review) — implementation between sessions
**Updated:** 2026-06-02

This file consolidates the two former task docs (`TASK-Config-D.md` + `TASK-Demo.md`)
into one. It carries the full context: what is **done**, what is **blocked on the
candidate's manual steps**, and the **active next action** (launch Config-D on Colab).

---

## ⓪ TL;DR — where we are and the one thing to do next

- **Goal:** a trained **Config D** checkpoint (Full V5 + EfficientNet-B3, 4-channel,
  Focal Loss, 5-fold patient-level CV) → drop it into the FastAPI backend → the React
  demo serves **real** predictions to a closed academic audience (~15 people).
- **All code is complete and on `main`** (training notebooks, FastAPI server, frontend
  wiring, Grad-CAM, V5 visualizer, password gate). **Nothing here is blocked on more
  code.** The remaining work is the candidate's manual run + deploy.
- **Two parallel training tracks (fixed split, confirmed 2026-06-02):**
  - **Kaggle = APTOS — definitively.** Functional pipeline test. Already running.
    EyePACS is **never** run on Kaggle.
  - **Colab = EyePACS — definitively, and only here.** The real Config-D run. **← the
    active task.** Candidate may pay for Colab Pro/Pro+ for more vCPU + background
    execution.
- **Interim-checkpoint strategy:** as soon as **any APTOS epoch finishes on Kaggle**,
  drop that checkpoint onto the server and bring the full service up **now** — to validate
  the end-to-end demo (backend + frontend) against a real checkpoint. Later, when the
  **EyePACS** run finishes on Colab, **swap the APTOS checkpoint for the EyePACS one** —
  same server, same wiring, only the weights + `*_norm_stats.json` change. The APTOS
  checkpoint is a stand-in for plumbing validation; only the EyePACS checkpoint is
  thesis-faithful for the defense.
- **⚠ Hard blocker before EyePACS is viable on any platform:** the **V5 preprocessing
  throughput bottleneck** (§2). On Kaggle, **not a single epoch finished in 12 h** — not
  because the GPU is slow, but because the GPU **starves** waiting on CPU-side V5
  preprocessing recomputed per-image, per-epoch. A faster GPU (A100) will **not** fix
  this. The real fix is **precompute-and-cache V5 Stages 0–4** (§2). Until that lands,
  EyePACS will hit the same wall on Colab.

**The single next action:** the Kaggle `KGAT_…` token is now in hand and cell 3 accepts
it, so Config-D on Colab is launchable (§1 checklist). But a Colab T4 is ~2 vCPU =
identical to Kaggle, so EyePACS will hit the same wall — **build the §2 V5 cache first** or
fold 0 won't finish.

---

## 1. Launch Config-D on Colab (the active manual step)

The Colab port lives in `experiments/colab/` (`train_config_d_colab.ipynb`,
`_build_colab_notebook.py`, `README.md`). It is **self-contained**: it clones
`github.com/yesmukhamedov/dr-classifier` and imports nothing from the repo at runtime.
Two modes via `DATASET` in cell 1:

| `DATASET`   | Source (Kaggle)                       | Size      | Use                                   |
|-------------|----------------------------------------|-----------|----------------------------------------|
| `"aptos"`   | competition `aptos2019-blindness-detection` | ~3.7k | **Quick functional test** — full Config-D pass in minutes to prove the Colab pipeline works. |
| `"eyepacs"` | dataset `dreamer07/eyepacs`            | ~35k      | **The real Config-D run.**             |

### ▶ Exact launch checklist (Kaggle token available — 2026-06-03)

A Kaggle **new-format `KGAT_…` access token** is now in hand, and cell 3 of the
notebook was updated to accept it (see auth step 1 below). Run order:

The notebook is now **two-mode** (cell 1 `MODE`) and uses the **V5 cache + Kaggle-Dataset
persistence** (no Google Drive) — see §2. Run order:

1. **Store the token as a Colab Secret** (never paste it into a cell):
   Colab → 🔑 (left sidebar) → *Add new secret* → Name **`KAGGLE_API_TOKEN`**,
   Value = the candidate's `KGAT_…` token, toggle **Notebook access** on.
   *(The literal token is intentionally not committed here — it is a live secret.
   It lives only in the candidate's Colab Secrets. Rotate it on Kaggle if leaked.)*
2. **Cell 1:** set `KAGGLE_USERNAME` (your Kaggle username — required for the
   persistence dataset slugs) and `DATASET = "eyepacs"`.
3. `Runtime → Change runtime type → T4 GPU`.
4. **Build the cache once:** set `MODE = "build_cache"` → `Run all`. Downloads
   EyePACS, runs Stages 0–4 + dataset-stats + PCA, pushes the bundle as the Kaggle
   dataset `<user>/eyepacs-v5-cache-eyepacs`. (~1–2 h; do the same with
   `DATASET="aptos"` first for a minutes-long end-to-end smoke test.)
5. **Train fold 0:** set `MODE = "train"`, `FOLD = 0` → `Run all`. Pulls the cache +
   any prior checkpoint, trains GPU-bound, versions the checkpoint dataset
   periodically + at the end. Repeat with `FOLD = 1..4` for the rest.
6. `dreamer07/eyepacs` needs **no** rule acceptance (the APTOS-only rule step does
   not apply to the real run).

> ✅ The §2 throughput blocker is now fixed in code (cache) and the §2 24 h-limit /
> persistence questions are resolved (Kaggle-Dataset persistence + `--resume`). The
> token unblocks the download; the cache unblocks the throughput; Kaggle Datasets
> unblock persistence without paid Drive.

### Why this needs the candidate (no browser/Colab access for Claude)

Claude cannot open a browser or run Colab. **Manual minimum:**

1. Open `train_config_d_colab.ipynb` in Colab.
2. Set `DATASET` and `FOLD` in **cell 1**.
3. `Runtime → Change runtime type → T4 GPU`.
4. `Run all`.
5. Pass the **3 authorization steps** below.

Everything else (Drive mount, Kaggle download, dataset-layout adapter, config merge,
dataset-stats + PCA caching, single-fold `--resume`) is automated in the cells.

### The 3 authorization steps (one-time, minimal, nothing secret leaves the session)

1. **Kaggle API token** — cell 3 now accepts **both** token formats:
   - **New (`KGAT_…`, recommended)** — Kaggle → *Settings* → *API* → *Create New Token*
     yields a `KGAT_…` access token. Add it as a **Colab Secret named
     `KAGGLE_API_TOKEN`** (🔑 left sidebar). The cell writes it to
     `~/.kaggle/access_token` + the `KAGGLE_API_TOKEN` env var.
   - **Legacy** — add `KAGGLE_USERNAME` + `KAGGLE_KEY` to Colab Secrets, or upload a
     `kaggle.json` of the form `{"username":"...","key":"..."}`.
   - The upload fallback auto-detects which kind of file you upload (a raw `KGAT_…`
     text token or a legacy `kaggle.json`).
2. **Google Drive** — click *Authorize* on the mount cell (OAuth). Checkpoints,
   dataset-stats and PCA eigvecs persist under `<DRIVE_DIR>` so per-fold `--resume`
   survives Colab disconnects.
3. **APTOS only** — accept the competition rules once at
   <https://www.kaggle.com/competitions/aptos2019-blindness-detection/rules>.
   (`dreamer07/eyepacs` needs no rule acceptance.)

### ⚠ Prerequisite — the cloned repo must be current (outstanding TODO)

The notebook clones `yesmukhamedov/dr-classifier`. That repo must already contain the
**up-to-date `experiments/`** — in particular:
- `scripts/compute_dataset_stats.py` (the **real** implementation, not the old stub),
- `scripts/precompute_v5_cache.py` (**new** — the V5 cache builder, §2),
- `src/preprocessing/pipeline_v5.py` with `precompute_deterministic` +
  `finish_from_cache` (**new** — the deterministic/stochastic split, §2),
- `src/data/datasets.py` with `CachedEyePACSDataset` + `load_cache_meta` (**new**),
- `src/experiments/exp1_factorial.py` with the `paths.v5_cache_dir` wiring (**new**),
- `kaggle/merge_config.py`,
- the EyePACS adapter **`is_file()` fix** (the CSV is wrapped in a same-named folder, so
  the probe must filter `if p.is_file()` or `read_csv` raises `IsADirectoryError`).

If `dr-classifier` is stale, **mirror the latest `experiments/` tree into it first.**
This is the same unclosed TODO carried over from the old Config-D task — now also
gating the cache code above.

### Order of actions

1. **Push the current `experiments/` to `dr-classifier`** (if not already current).
2. **Smoke test:** open the notebook, set `DATASET="aptos"`, `FOLD=0`, `Run all` →
   pipeline validated in minutes.
3. **Real run:** once APTOS passes → set `DATASET="eyepacs"`, **delete the cached
   `eyepacs_norm_stats.json` on Drive** (`<DRIVE_DIR>/processed/`) — otherwise the
   APTOS-computed Stage-7 stats get reused and the EyePACS checkpoint is **not
   thesis-faithful** — then launch the real **fold 0**.

### Persistence & Colab caveats

- **Outputs persist on Google Drive** (`output_dir` → Drive), so the next session
  resumes with zero setup. Trade-off: the **dataset re-downloads each session**
  (EyePACS won't fit the free 15 GB Drive tier) — ~10–20 min per EyePACS session.
- Free Colab disconnects on idle (~90 min), caps ~12 h/session → same
  **one-fold-per-session + `--resume`** strategy as Kaggle. **Colab Pro+ adds
  background execution.**
- EyePACS needs ~70 GB peak disk (zip + unzipped); GPU runtimes give ~78–112 GB; the zip
  is deleted right after extraction.
- EfficientNet runs **fp32** (mixed precision stays disabled — fp16 overflow). If T4
  OOMs at 512px, uncomment `training.batch_size=8` in the merge cell.
- **Outputs:** `<DRIVE_DIR>/outputs/exp1/checkpoints/D_fold{0..4}/best_model.pt`
  (monitored on `weighted_f1`) + `<DRIVE_DIR>/outputs/exp1/metrics.csv`.

---

## 2. ⚠ THE BLOCKER — V5 preprocessing throughput (read before paying for Colab)

**Diagnosis (confirmed by code, not a guess): the problem is NOT GPU speed.**

On Kaggle, 12 h elapsed with **zero epochs finished** — not because T4 is slow
(EfficientNet-B3 on T4 is ~15–60 min of *pure GPU* time per epoch), but because the GPU
**idles, starved for data**: the entire V5 pipeline runs **on CPU inside the DataLoader,
per image, every epoch.**

Evidence in code:
- `EyePACSDataset.__getitem__` (`src/data/datasets.py:133`) calls the full
  `PreprocessingPipelineV5.__call__` on every sample.
- The heaviest stages run on the **full-resolution** EyePACS image (~2500–4000px), not
  on 512px:
  - `detect_od_fovea` (`src/preprocessing/od_fovea_detect.py:190`) — classical CV + a
    large `GaussianBlur` at full resolution;
  - `crop_and_resize` — decode + resize from full resolution;
  - `apply_flat_field` — a large adaptive Gaussian.
- Workers = 2 on Kaggle → ~1.5–3 s CPU/image × 35k / 2 ≈ **7–14 h of preprocessing for
  ONE epoch.** Matches "no epoch in 12 h."

**Therefore:** an A100 on Colab will sit just as idle. More vCPU (Colab Pro ~8 vs Kaggle
2) gives ~4× but 20 epochs × 5 folds still won't fit a week while re-preprocessing every
epoch.

### The real fix — precompute V5 Stages 0–4 once and cache  ✅ IMPLEMENTED (branch `feat/v5-cache-colab`)

Stages 0→4 (flip, OD-fovea rotation, crop/resize, FOV-mask, flat-field) are **fully
deterministic** — no train-time randomness until Stage 5 (CLAHE p=0.8) and Stage 6
(augmentation). The cache stores each image as a **4-channel PNG** (RGB = Stage-4
flat-field output, alpha = binary FOV mask — **lossless**, the mask is strictly
{0,1}) plus a `cache_meta.csv` of the two OD/fovea scalars Stage 6 reads
(`confident`, `rotation_sigma_deg`). ~8 GB PNG-compressed for 35k.

**What landed (all on `feat/v5-cache-colab`, verified max|Δ| = 0.0 vs the live pipeline):**
- `src/preprocessing/pipeline_v5.py` — split the full path into deterministic
  `precompute_deterministic` (Stages 0–4) + stochastic `finish_from_cache`
  (Stages 5–7). `__call__` now routes through both, so the cached and live paths are
  **provably identical** (same `_finish`). The 4th-channel mask stays the un-warped
  FOV mask, exactly as before — zero drift.
- `scripts/precompute_v5_cache.py` — multiprocess cache builder (resumable; skips
  images already in `cache_meta.csv`). Writes `<name>.png` + `cache_meta.csv` +
  copies `trainLabels.csv` so the cache is a self-contained training input.
- `src/data/datasets.py` — `CachedEyePACSDataset` (+ `load_cache_meta`): reads the
  PNG cache and calls `finish_from_cache`; per-epoch CPU cost collapses to CLAHE +
  aug + normalize.
- `src/experiments/exp1_factorial.py` — opt-in via `paths.v5_cache_dir`. When set,
  the **full** configs (B/D) read the cache; baseline (A/C) errors clearly (no
  cacheable Stages 0–4). Drift-proof: same pipeline object finishes both paths.

**Verification (run locally, CPU):** synthetic-image round-trip and a tiny
end-to-end build→load test both give **max|Δ| = 0.0** between the cached tensor and
the live-pipeline tensor, in inference and seeded-training mode.

**Budget with the cache:** build ~1–2 h once → fold 0 (the one the demo needs) ~half a
day (GPU-bound) → all 5 folds fit a week with margin. **Without the cache: no.**

### Persistence — Kaggle Datasets fully replace Google Drive (no Drive, no paid tier)

The ~8 GB cache + the re-downloaded EyePACS don't both fit free Drive (15 GB). So
the Colab notebook (`experiments/colab/`) now persists **everything on Kaggle
Datasets**, pushed/pulled with the **same KGAT_ token** that downloads EyePACS — no
Drive, no OAuth, no paid storage:
- **Cache dataset** `<user>/eyepacs-v5-cache-<dataset>` — built once (MODE
  `build_cache`), pulled each training session (~8 GB tar, a few min vs re-downloading
  35 GB EyePACS every time). Bundles the Stage-7 norm-stats + PCA so they travel with it.
- **Checkpoints dataset** `<user>/dr-config-d-ckpts-<dataset>` — created on first
  push, **versioned** thereafter. A background thread versions it every
  `CKPT_UPLOAD_EVERY_MIN` (default 30) + a final push in a `finally`.

The notebook is now a **two-mode** flow (cell 1 `MODE`): `build_cache` (once) →
`train` (per fold). KGAT auth, push/pull/tar helpers, and the uploader thread are all
automated.

### Handling the 24 h cap / a fold that doesn't finish in one session

- **Free Colab** ≈ 12 h, **no** background execution; **Pro+** ≈ 24 h continuous in
  the background. With the cache, **fold 0 ≈ 12 h fits one session** (Pro+ comfortably).
- If a session is killed mid-fold: the background uploader has already versioned the
  checkpoint dataset (≤ `CKPT_UPLOAD_EVERY_MIN` old). Re-run MODE `train` with the
  **same `FOLD`** → the cell pulls the latest checkpoint and `--resume` continues; you
  lose at most one upload cadence. **One fold per session; cache built only once.**
- So even on **free** Colab the full run is feasible (more sessions, same resume
  loop). Pro+ just removes the babysitting (background 24 h) — it is **not** required.

### What to collect from the browser (Claude browser extension) before launching

1. **Your Kaggle username** — needed for the dataset slugs (`<user>/…`). It's the
   `kaggle.com/<username>` on your profile. Put it in cell 1 `KAGGLE_USERNAME`.
2. **Confirm `dreamer07/eyepacs` is still public + its layout** — open the dataset
   page; verify it exposes `trainLabels.csv` (cols `image`,`level`) + `train/*.jpeg`
   (the adapter expects this; the `is_file()` fix handles the same-named-folder wrap).
3. **Confirm your Colab tier** — Pro+ (for 24 h background) is *nice-to-have*, not
   required. Free works with the one-fold-per-session resume loop.
4. **(Repo currency — not browser)** the notebook clones `yesmukhamedov/dr-classifier`;
   it must contain this branch's `experiments/` (precompute script, the
   `paths.v5_cache_dir` wiring, `CachedEyePACSDataset`). Mirror `experiments/` into
   that repo before running — see §1 prerequisite.

### Colab tier findings (confirmed 2026-06-03 from official Colab subscription page + FAQ)

Google **does not publish** exact vCPU / RAM / GPU numbers — the FAQ states they
"vary over time." Below: official facts + commonly observed values. **Bottom line:
Colab gives no direct "N CPU cores" lever, so the §2 caching fix is mandatory.**

- **vCPU is tied to the machine, not the subscription.** A standard **T4 instance is
  ~2 vCPU — identical to Kaggle.** More vCPU only comes indirectly via a heavier
  machine (A100 ~12 vCPU historically) or a **High-RAM** runtime (paid tiers,
  `Runtime → Change runtime type → High-RAM`). There is **no** "more CPU" toggle.
- **GPU pool "varies over time."** Commonly T4 (also Free), L4, A100. Pro = "faster
  GPUs"; **Pro+ = priority access**, not an exclusive GPU set. No fixed tier→GPU map.
- **Background execution (tab closed / idle) is Pro+ only**, up to **24 h continuous**
  while code runs. Free/Pro/PAYG cap ~12 h, no background execution. All tiers stop
  once Compute Units are exhausted.

**Throughput math (≈2.25 s/img V5 on CPU × 35,126 imgs; EfficientNet-B3 GPU ≈30 min/epoch):**

| Path | vCPU | preproc/epoch | bound by | 1 fold (20 ep) | 5 folds (100 ep) |
|------|------|---------------|----------|----------------|------------------|
| Kaggle / Colab **T4** | 2 | ~11 h | **CPU (GPU idle)** | ~220 h | ~1100 h |
| Colab Pro High-RAM | ~8 | ~2.7 h | CPU | ~55 h | ~270 h |
| Colab **A100** | ~12 | ~1.8 h | CPU | ~36 h | ~180 h |
| **Cached (Stages 0–4)** | any | ~0 | **GPU ~30–40 min** | **~12 h** | ~58 h + ~2 h build |

**A100 is the wrong buy:** even at ~180 h for 5 folds it (a) still exceeds a week and
(b) burns the entire Pro+ ~500 CU/month in ~38 h (A100 ≈13 CU/h) — paying premium GPU
rates for a GPU that **sits idle waiting on CPU**. The cache flips the epoch to
GPU-bound **on a plain T4**, so **fold 0 (the only fold the demo needs) finishes in
~half a day** with no A100/Pro+ required. Pro+ stays *optional* (nice for 24 h
background execution so fold 0 survives a closed laptop), not a throughput fix.

**Open question for the cache:** the ~8 GB PNG cache + the re-downloaded EyePACS won't
both fit the free 15 GB Drive tier → the cache assumes **paid Google Drive** (or another
persistent location). Confirm storage before building.

---

## 3. Governance caveat — "Config D" pretrain axis (v6.0.0)

- The **shipped/demo "Config D"** is the original **ImageNet-pretrained** EfficientNet-B3
  + Full V5 artifact (the practical demo deliverable).
- Governance moved to **v6.0.0**: RETFound was dropped in favour of
  **ophthalmology-specific SSL** on the CNN backbones; **AOQ-1/3/4 resolved**, Configs
  **B/D reinstated**.
- **Divergence to track:** the shipped demo "Config D" is still the **retired ImageNet
  artifact**, not the v6.0.0 SSL formulation. Acceptable as the demo/practical artifact;
  reconciliation deferred. (Memory: `config-d-shipped-retfound-deferred`.) The Stage-7
  dataset-specific normalize work is governance-consistent regardless of the pretrain
  question.

---

## 4. State of the two parallel runs (fixed split, confirmed 2026-06-02)

- **Kaggle = APTOS — definitively.** Functional pipeline smoke test. EyePACS is **never**
  run on Kaggle. Earlier Kaggle logs mentioning EyePACS / `dreamer07/eyepacs` fold 0 are a
  superseded previous attempt; the current and all future Kaggle sessions are APTOS only.
- **Colab = EyePACS — definitively, and only here.** The real run, gated on §1 (launch)
  and §2 (caching fix).
- **Interim plumbing test:** the first APTOS epoch that finishes on Kaggle → its
  checkpoint goes on the server so the full service runs **now** for end-to-end demo
  validation. The EyePACS checkpoint from Colab replaces it later (only the weights +
  `*_norm_stats.json` swap). Only the EyePACS checkpoint is thesis-faithful.

---

## 5. Config-D training — done vs remaining

**Done (committed, on `main`):**
- `experiments/kaggle/` — `train_config_d.ipynb` (clone `dr-classifier`, EyePACS layout
  adapter incl. `is_file()` fix, deep-merged config, PCA, dataset-stats, single-fold
  `--resume`), `kaggle_paths.yaml`, `merge_config.py` (CLIs take one `--config`, so we
  pre-merge), `README.md`. Mirrored to the `dr-classifier` repo the notebook clones.
- `experiments/colab/` — the Colab port (§1).
- **Stage 7 (thesis-faithful)** — `scripts/compute_dataset_stats.py` implemented (was a
  stub): Stages 0–4, mask=1.0 only, `[0,1]` scale → `eyepacs_norm_stats.json`;
  `exp1_factorial.py` auto-loads it and injects dataset-specific normalize into the full
  configs (governance requires dataset-specific here, not ImageNet).

**Remaining — manual (the candidate):**
1. **Interim (Kaggle/APTOS):** take the first finished APTOS epoch's checkpoint → copy to
   `server/checkpoints/config_d_fold0.pt` **with its APTOS `*_norm_stats.json`** → bring
   the server + demo up now to validate the full service end-to-end (§6/§7 QA).
2. **Real (Colab/EyePACS):** run the notebook for `--fold 0..4`; retrieve `outputs/exp1/`.
   - **fold 0 alone unblocks the demo.** Folds 1–4 only feed `verify_exp1.py`'s
     dominance check (which also needs a Config C run, out of scope here).
   - **Swap-in:** replace the interim APTOS checkpoint with `D_fold0/best_model.pt` **and
     its EyePACS `eyepacs_norm_stats.json`** (both together — to avoid preprocessing
     drift). Only this checkpoint is thesis-faithful.
3. `pip install -r server/requirements.txt`; run uvicorn; run
   `server/tests/test_inference.py` and `scripts/verify_exp1.py`.
4. Deploy (§7).

**Risks:** session timeout mid-fold → `--resume` is wired. EfficientNet fp16 overflow →
`mixed_precision: false` stays (do not flip). EyePACS layout differs → the adapter
restructures before any code touches the data. Train/inference preprocessing drift → the
server imports the **same** `pipeline_v5`; `test_preprocessing_matches_training` locks it.

---

## 6. FastAPI backend + Demo frontend — done vs remaining

**Done (committed, on `main`):**
- **Backend `server/`** — bootable FastAPI app importing `experiments/src` (no
  duplication). Endpoints: `/api/predict` (per-eye + worst-eye patient-level, dataset
  stats injected at inference so no train/inference drift), `/api/gradcam`
  (self-contained Grad-CAM on `conv_head`; emits a CAM-geometry `rationale` +
  `cam_pixel_count`/`cam_area_frac`/`cam_region`, no LLM, neutral image-space wording per
  NC-14), `/api/visualize` (6-panel V5 strip via `pipeline_v5.stage_breakdown` + FOV mask
  + OD/fovea payload — **checkpoint-free**, works before training), `/api/selftest`,
  `/api/auth`, `/api/health` (provenance: version · git_sha · checkpoint ·
  `requires_password`). Password gate (`DEMO_PASSWORD`), in-memory image handling,
  safety limits (8 MB / MIME allowlist / 4096px). `Dockerfile` (HF port 7860),
  `requirements.txt`, README, tests.
- **Frontend `demo/`** — `Demo.js` calls `/api/predict` with graceful simulator
  fallback + status badge; `_apiPredict.js`; framing block (D.1); per-image vision
  widget `_VisionWidget.js` (OD/fovea overlay + chip + V5 strip + FOV mask toggle); live
  Grad-CAM `_LiveGradcam.js` with per-eye rationale; provenance footer; password access
  gate (revalidates a stored password on reload; offline/simulator never gated). EN+KZ
  i18n. ESLint clean; `CI=1 npm run build` OK.

**Verified as far as the local env allows** (no `fastapi`/`pytorch_grad_cam` installed):
`merge_config.py` deep-merge; preprocessing stage signatures; end-to-end
`V5 → (4,512,512) → efficientnet_b3(in_channels=4) → (1,5)`, softmax=1.0; Grad-CAM /
stage_breakdown / visualize logic on random-init weights; no hardcoded paths in `server/`
or `experiments/kaggle/`.

**Remaining — manual (the candidate):**
1. Train + drop the checkpoint (§5).
2. `pip install -r server/requirements.txt`; run `server/tests/test_inference.py`
   (`test_health`, `test_predict_left_only`, `test_predict_both_eyes`,
   `test_predict_rejects_non_image`, `test_preprocessing_matches_training`).
3. Curate the **5 walkthrough images** (one per DR grade 0–4): `od_fovea.confident=True`,
   unambiguous label, Grad-CAM on an interpretable region. Copy to
   `demo/public/pipeline/demo_cases/dr0N/` (rename to `dr0N_left/right.png`) + pre-computed
   Grad-CAMs as offline fallback. Replaces the current `WALKTHROUGH_POOL`.

---

## 7. Deployment & academic-beta launch — remaining (manual)

**Audience:** closed academic beta — supervisor, IITU department professors, committee
(~15 people). Single shared static password (`DEMO_PASSWORD`) is the access boundary; no
accounts. No image retention (in-memory only). One-line "research prototype, not a
medical device" banner; no regulatory/clinical-claims copy.

**The beta must demonstrate (all six must work on arbitrary uploads, else not ready):**
fundus → DR grade 0–4 (C-1); per-eye + worst-eye (Impl §8); live Grad-CAM overlay (C-3);
OD/fovea center viz (SC-F); FOV-mask preview / 4th channel (SC-E); baseline-vs-V5 6-panel
strip (C-1).

**Backend — HuggingFace Space:**
1. Create Space `<user>/dr-demo-config-d`, **Private** initially; SDK Docker; push the
   `Dockerfile`.
2. Env vars: `DEMO_PASSWORD`, `DEMO_VERSION` (semver), `MODEL_CHECKPOINT_ID`
   (e.g. `config-d-fold0-2026-06-15`). Checkpoint via Git LFS (~50 MB EfficientNet-B3,
   well under limits).
3. CPU Basic suffices (~10–15 s cold start, 0.5–2 s/predict, 1–3 s/gradcam); T4-small
   only if many committee members hit it at once during the defense.
4. Once healthy, **switch to Public** so the React frontend can call without HF auth —
   the password gate is the real restriction.

**Frontend — static hosting:**
1. `cd demo && npm run build`.
2. Deploy `demo/build/` to Vercel (recommended) or GitHub Pages.
3. Set `REACT_APP_API_URL=https://<user>-dr-demo-config-d.hf.space` in deployment env.
4. Tag releases `demo-v0.1.0`, etc. `/api/health` returns version · SHA · checkpoint.

**Distribution:** one email to the invited list — URL, password, one-paragraph context.

**Pre-launch QA gate (do ALL before sharing the URL):**
- `GET /api/health` → `status: ok`, reports checkpoint; `GET /api/selftest?password=…`
  → predict/gradcam/visualize all `pass`.
- Browser smoke (incognito): password → 5 walkthroughs each load 2 images + OD/fovea
  markers + grade ±1 + Grad-CAM + V5 strip; "Random EyePACS pair" ×5 no console errors;
  a selfie shows "not a fundus" chip but still runs; one custom fundus → full live
  pipeline; pause Space → `⚠ simulator (backend offline)` badge + walkthrough still works
  on pre-rendered assets; restart → `● real model` within 30 s.
- Provenance: `/api/health` checkpoint ID matches a fold in
  `experiments/outputs/exp1/checkpoints/` and a tagged release; footer shows the same
  triple.
- Sanity: 4/5–5/5 on curated walkthroughs (±1); 10 random pairs no crashes, probs sum
  1±0.01.
- Privacy: Space logs contain no image bytes / filenames / raw IPs (only `request_id`,
  `ip_hash`, sizes, grade, latency); no `/tmp` writes after 20 requests.
- **If any QA item fails, do not share the URL.**

**Beta-specific risks:** cold start ~10–15 s → footer note + spinner; Space idles
mid-defense → 30-min `/api/health` ping (UptimeRobot / GH Actions cron); pin
`grad-cam==1.5.0` to match Chapter-4 figures; rotate `DEMO_PASSWORD` if leaked.

---

## 8. Out of scope (explicit)

- Retraining all configs A/B/C — only **D** is required here.
- Browser-side ONNX inference — rejected for the FastAPI backend (keeps the
  thesis-defended pipeline).
- Accounts / OAuth / rate limiting / CAPTCHA / analytics / quotas / multi-tenancy.
- Legal/privacy docs beyond the one-line banner; clinical-decision-support claims.
- Persistent server-side feedback (relabel buffer stays client-side, JSONL export).
- Multi-model A/B in the demo (single Config D only). Folds 1–4 dominance check needs a
  Config C run — separate scope.

---

## 9. Confirmed split (resolved 2026-06-02)

**Kaggle = APTOS, Colab = EyePACS — final.** The candidate confirmed the current Kaggle
session is APTOS and that EyePACS will be run **only** on Colab. The first APTOS epoch to
finish goes on the server as an interim checkpoint to validate the full service; the
EyePACS/Colab checkpoint replaces it for the defense.

---

End of TASK.md.
