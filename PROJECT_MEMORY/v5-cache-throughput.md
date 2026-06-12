---
name: v5-cache-throughput
description: "Why Config-D training is GPU-starved (full V5 per-image on CPU every epoch); fix = precompute-and-cache Stages 0–4, IMPLEMENTED on feat/v5-cache-colab"
metadata:
  type: project
---

**Symptom (2026-06-02):** Config-D on Kaggle T4 ran 12 h without finishing a single epoch. Root cause is NOT GPU speed — it's CPU preprocessing throughput, so a faster GPU (A100) won't help; the GPU starves waiting for data.

**Why:** `EyePACSDataset.__getitem__` (`src/data/datasets.py:133-154`) calls the full pipeline `__call__` on every sample, every epoch, on CPU. The expensive parts run on the **full-resolution** EyePACS image (~2500–4000 px): Stage 0/1 `detect_od_fovea` (large GaussianBlur on full-res green channel), Stage 2 `crop_and_resize` (full-res decode + isotropic resize), Stage 4 `apply_flat_field` (large adaptive Gaussian σ=0.07·D). DataLoader `num_workers`=2 (Kaggle) → throughput-bound. Trainer wires `persistent_workers` + `prefetch_factor=2`, so the only lever there is more workers.

**Fix (IMPLEMENTED 2026-06-03, branch `feat/v5-cache-colab`, pushed; verified max|Δ|=0.0 vs live pipeline):** precompute Stages 0–4 ONCE (deterministic — no randomness until Stage 5 CLAHE p=0.8 / Stage 6 aug) → cache each image as a **4-channel PNG** (RGB=Stage-4 flat-field, alpha=binary FOV mask — lossless; ~8 GB for 35k) + `cache_meta.csv` of the two OD/fovea scalars Stage 6 reads (`confident`, `rotation_sigma_deg`). Code: pipeline split into `precompute_deterministic`+`finish_from_cache` (both finish via shared `_finish`, so cached==live, zero drift); `scripts/precompute_cache.py` (multiprocess, resumable); `CachedEyePACSDataset`+`load_cache_meta` in datasets.py; opt-in via `paths.v5_cache_dir` in exp1_factorial (full configs B/D only); `tests/test_cache.py`. Train-time epochs become GPU-bound (~30–40 min T4).

**Persistence decision (supersedes "paid Google Drive"):** Colab notebook now uses **Kaggle Datasets, NOT Drive** — cache + checkpoints persist as private Kaggle Datasets pushed/pulled with the same KGAT_ token; no Drive/OAuth/paid tier. Notebook is two-mode (`build_cache` once, `train` per fold) with a background checkpoint-uploader (every 30 min) + `--resume` so a session killed at the 12h/24h cap loses ≤30 min. Cell 1 needs `KAGGLE_USERNAME`. See [[colab-config-d-runner]], [[config-d-kaggle-source]], [[config-d-cache-handoff]].

NOTE (post version-marker strip): file/symbol names lost the `v5` tag — `precompute_v5_cache.py`→`precompute_cache.py`, `test_v5_cache.py`→`test_cache.py`, `pipeline_v5.py`→`pipeline.py`. See [[strip-version-markers]].
