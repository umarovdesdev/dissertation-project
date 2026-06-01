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
| GET  | `/api/health`  | — | `{status, model, checkpoint, checkpoint_loaded, device}` |
| POST | `/api/predict` | multipart `left?`, `right?` | patient-level + `per_eye` (see `schemas.py`) |
| POST | `/api/gradcam` | multipart `eye`, `image` | **501** (scaffold) |

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
cd E:/dissertation-project
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

## Status / next

- [x] Bootable API, real V5 preprocessing + model wiring, worst-eye aggregation.
- [x] Dataset-specific normalize injection (no preprocessing drift).
- [ ] Grad-CAM (`gradcam.py`) — TASK-Demo §C.5.
- [ ] Password gate, `/api/visualize`, `/api/selftest`, OD/fovea payload — TASK-Demo Part C.
- [ ] Bundle real checkpoint after Kaggle training (Part A).
