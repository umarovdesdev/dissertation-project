# server/ — DR-Classifier inference backend

FastAPI + PyTorch backend that serves **real** Config D (Full V5 +
EfficientNet-B3) predictions to the React demo. It imports preprocessing and
model code directly from `../experiments/src` — no duplication, so inference
runs the *same* V5 pipeline that was defended in the thesis.

## Layout

```
server/
├── app/
│   ├── __init__.py        puts experiments/ on sys.path
│   ├── config.py          env-driven settings (paths, device, CORS)
│   ├── schemas.py         Pydantic request/response models
│   ├── preprocessing.py   builds the V5 inference pipeline (+ dataset stats)
│   ├── inference.py       model load + predict (per-eye, worst-eye patient)
│   ├── gradcam.py         scaffold stub (→ 501) — see TASK-Demo §C.5
│   └── main.py            FastAPI app + endpoints
├── checkpoints/           drop config_d_fold0.pt + eyepacs_norm_stats.json here
├── tests/test_inference.py
├── requirements.txt
└── Dockerfile             HuggingFace Spaces (port 7860)
```

## Endpoints

| Method | Path | Body | Returns |
|---|---|---|---|
| GET  | `/api/health`   | — | `{status, model, checkpoint, checkpoint_loaded, device, version, git_sha}` |
| POST | `/api/predict`  | multipart `left?`, `right?`, `password?` | patient-level + `per_eye` |
| POST | `/api/gradcam`  | multipart `image`, `eye`, `password?`, `target_class?` | `{gradcam_png_b64, attention_overlay_png_b64, target_class}` |
| POST | `/api/visualize`| multipart `image`, `eye`, `password?` | `{fov_mask_png_b64, v5_preview_png_b64, od_fovea}` |
| GET  | `/api/selftest` | query `password?` | per-op pass/fail report |

- **Grad-CAM** is a self-contained torch implementation on EfficientNet's
  `conv_head` (no `pytorch-grad-cam` dependency); JET overlay over the original
  image. **/api/visualize** returns the 6-panel V5 stage strip (via
  `pipeline_v5.stage_breakdown`), the FOV mask, and the classical-CV OD/fovea
  payload (`od_fovea`).
- **Password gate (§C.2):** set `DEMO_PASSWORD` to require a `password` field on
  every endpoint except `/api/health`. Unset → gate **open** (local dev).
- **Safety limits (§C.4):** ≤ 8 MB/image, MIME ∈ {jpeg,png,webp} (else 415),
  decoded ≤ 4096×4096; all decoding in-memory (no disk writes).

## Why two files in `checkpoints/`

Config D trained with **dataset-specific** Stage 7 normalize (D-2), not ImageNet.
To avoid train/inference preprocessing drift, the server injects the *same*
EyePACS mean/std the checkpoint trained with:

- `config_d_fold0.pt`  ← `experiments/outputs/exp1/checkpoints/D_fold{N}/best_model.pt`
- `eyepacs_norm_stats.json` ← `experiments/data/processed/eyepacs_norm_stats.json`
  (produced by `scripts/compute_dataset_stats.py`)

If `eyepacs_norm_stats.json` is missing, the server still boots but logs a
warning and falls back to ImageNet — **don't** demo Config D that way.

## Local dev

```bash
cd <repo-root>   # the dissertation-project checkout
# 1. Put the trained artifacts in place:
cp experiments/outputs/exp1/checkpoints/D_fold0/best_model.pt server/checkpoints/config_d_fold0.pt
cp experiments/data/processed/eyepacs_norm_stats.json        server/checkpoints/

# 2. Install + run (use the dr-classifier env, or a fresh venv):
pip install -r server/requirements.txt
uvicorn server.app.main:app --reload --port 8000
# → http://localhost:8000/api/health
```

Smoke test:
```bash
curl -F "left=@<some_fundus>.jpg" -F "right=@<some_fundus>.jpg" \
     http://localhost:8000/api/predict
```

## Configuration (env vars)

| Var | Default | Purpose |
|---|---|---|
| `CHECKPOINT_PATH` | `server/checkpoints/config_d_fold0.pt` | Model weights. |
| `NORM_STATS_PATH` | `server/checkpoints/eyepacs_norm_stats.json` | Stage 7 stats. |
| `MODEL_CHECKPOINT_ID` | `config-d-fold0` | Provenance shown in `/api/health`. |
| `DEVICE` | `auto` | `cuda` / `cpu` / `auto`. |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed origins. |
| `PORT` | `8000` (Docker: `7860`) | Bind port. |

## Tests

```bash
pytest server/tests/test_inference.py
```
They boot the app and assert response *shape/behaviour*; they pass even without
a checkpoint (random-init weights still give a valid softmax).

## Configuration (added env vars)

| Var | Default | Purpose |
|---|---|---|
| `DEMO_PASSWORD` | (unset) | Shared access password; unset = gate open. |
| `DEMO_VERSION` | `__version__` | Version string in `/api/health`. |
| `GIT_SHA` | `git rev-parse` | Provenance SHA (best-effort). |

## Status / next

- [x] Bootable API, real V5 preprocessing + model wiring, worst-eye aggregation.
- [x] Dataset-specific normalize injection (no preprocessing drift).
- [x] Grad-CAM (live, self-contained), `/api/visualize` (V5 strip + FOV mask +
      OD/fovea), `/api/selftest`, password gate, safety limits, health provenance.
- [ ] Frontend wiring of the new endpoints (per-image widget, live Grad-CAM,
      provenance footer, password screen) — TASK-Demo Part D.
- [ ] Bundle real checkpoint after Kaggle training (Part A).
