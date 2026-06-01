# TASK.md — Config D on Kaggle + Real Demo.js Inference

**Owner:** Yesmukhamedov N.S.
**Executor:** Claude Code
**Goal:** (1) Train Config D (Full V5 + EfficientNet-B3) on Kaggle and (2) replace the simulated `Demo.js` inference with real predictions from the trained model.

---

## 0. Decisions already made

| Question | Answer |
|---|---|
| Kaggle goal | Train Config D from scratch, full 5-fold CV |
| Real Demo.js approach | FastAPI backend + PyTorch (full V5 pipeline server-side) |
| Existing checkpoints | None — train from scratch |

---

## ✅ Progress status (updated 2026-06-01)

**Completion verdict: code-complete, manually pending.** Every code item in this
task is implemented and on `main`. The task is *not* fully closed: it still
depends on off-machine manual steps (the Kaggle training run, dropping the
checkpoint, running the test suite in a `fastapi`/`torch` env, and deployment).
There is no remaining code work Claude can do here — the blockers are all manual.

**Done (committed):**
- **Part A — repo + notebook.** `experiments/kaggle/` has `train_config_d.ipynb`
  (clone `dr-classifier`, EyePACS layout adapter, deep-merged config, PCA,
  dataset-stats, single-fold `--resume`), `kaggle_paths.yaml`,
  `merge_config.py` (the CLIs take one `--config`, so we pre-merge), `README.md`.
  The same files + code changes were pushed to the **`dr-classifier`** repo the
  notebook clones.
- **Part A — Stage 7 (thesis-faithful).** `scripts/compute_dataset_stats.py`
  implemented (was a stub): Stages 0–4, mask=1.0 only, `[0,1]` scale →
  `data/processed/eyepacs_norm_stats.json`. `exp1_factorial.py` auto-loads it and
  injects dataset-specific normalize into the full configs (the preset path left
  `dataset_mean/std=None` → ImageNet). Governance requires dataset-specific here.
- **Part B — backend.** `server/` is a bootable FastAPI app importing
  `experiments/src` (no duplication). `create_for_inference` already existed;
  worst-eye aggregation; dataset-stats injected at inference (no train/inference
  drift). `Dockerfile` (HF port 7860), `requirements.txt`, README, tests.
- **Part C — frontend wiring.** `Demo.js` calls `/api/predict` with graceful
  simulator fallback; `_apiPredict.js`; status badge; EN+KZ i18n.
  (TASK-Demo Parts C/D add Grad-CAM, /api/visualize, the vision widget, etc.)

**Verified (as far as the local env allows — no `fastapi`/`pytorch_grad_cam`):**
- `merge_config.py` deep-merge; preprocessing stage signatures; end-to-end
  `V5 → (4,512,512) → efficientnet_b3(in_channels=4) → (1,5)`, softmax=1.0;
  Grad-CAM / stage_breakdown / visualize logic on random-init weights.
- No hardcoded paths in `server/` or `experiments/kaggle/` (all from config/env).

**Remaining — manual (the candidate):**
1. Run the Kaggle notebook for `--fold 0..4`; download `outputs/exp1/`.
2. Copy `D_fold0/best_model.pt` → `server/checkpoints/config_d_fold0.pt` and
   `eyepacs_norm_stats.json` alongside it. (Both — to avoid preprocessing drift.)
3. `pip install -r server/requirements.txt`, run uvicorn; run
   `server/tests/test_inference.py` and `scripts/verify_exp1.py`.
4. Deploy (Part D) — HF Space + Vercel.

**Governance caveat:** "Config D" here is the **v5.0** design
(V5 + EfficientNet-B3 + **ImageNet** pretrain). Governance **v5.1 retired** it for
**Config B' (V5 + RETFound)**; AOQ-1 is unresolved. Shipped as the practical/demo
artifact; the RETFound/B' reconciliation is deferred. The Stage 7 normalize work
above is governance-consistent regardless of the pretrain question.

### Kaggle run log

**2026-06-01 — fold 0 launched.**
- **EyePACS source chosen: Kaggle dataset `dreamer07/eyepacs`** — 35,126 `*.jpeg`
  with original `<id>_<side>` filenames + `trainLabels.csv` (`image,level`),
  ~35 GB, pre-extracted. Verified via the browser: CSV path
  `.../eyepacs/trainLabels.csv/trainLabels.csv`, images flat under
  `.../eyepacs/data/data/`, extension `.jpeg`.
  - Rejected `tantai31124/eyepacs-original` (98 GB, ImageFolder
    `{train,val,test}/{0..4}`, **no `trainLabels.csv`**, already re-split →
    patient-leak + relabel-provenance risk).
  - Competition `diabetic-retinopathy-detection` (rules accepted) kept only as a
    canonical fallback — its multi-part `train.zip.00x` extraction can exceed the
    `/kaggle/working` quota (the notebook's heavy fallback path).
  - Local `E:/datasets/EyePACS` is the same canonical layout but unused on Kaggle
    (would need a ~35 GB upload).
- **Adapter bug fixed (Cell 6 / `experiments/kaggle/_build_notebook.py`).**
  `dreamer07/eyepacs` wraps the CSV in a *folder* also named `trainLabels.csv`,
  so `INPUT.rglob("trainLabels.csv")` matched the directory first and `first()`
  resolved `labels` to a dir → `read_csv` would raise `IsADirectoryError`. Fix:
  both probes now filter `if p.is_file()`. `_build_notebook.py` patched and
  `train_config_d.ipynb` regenerated; the same cell was hand-replaced in the
  running Kaggle notebook. **TODO:** mirror this fix into the `dr-classifier`
  GitHub repo (the notebook imports from there) so future imports are correct.
- **Status:** *Config-D Version #1* training on Kaggle (GPU **T4 x2**), fold 0,
  `Save & Run All (Commit)`. Awaiting `D_fold0/best_model.pt` +
  `eyepacs_norm_stats.json`. Folds 1–4 deferred (mind the ~30 h/week GPU quota);
  **fold 0 alone unblocks the demo** — folds 1–4 only feed `verify_exp1.py`'s
  dominance check (which also needs a Config C run, out of scope here).

---

## Part A — Train Config D on Kaggle

### A.1 Repository preparation (local, before Kaggle)

1. Create `experiments/kaggle/` folder. Add these files:
   - `experiments/kaggle/train_config_d.ipynb` — main notebook (template below).
   - `experiments/kaggle/kaggle_paths.yaml` — config override with Kaggle paths.
   - `experiments/kaggle/README.md` — short usage instructions.
2. Ensure the `experiments/src/` tree is import-clean (no hardcoded `E:/` paths). Verify by grepping:
   ```bash
   grep -rn "E:/" experiments/src/ experiments/configs/ experiments/run_experiment.py
   ```
   If anything outside `configs/default.yaml` matches, refactor it to read from config.
3. Push the `experiments/` tree to a public GitHub repo OR upload it as a Kaggle Dataset (Code dataset). Recommend GitHub — easier to iterate. Repo URL goes into the notebook's first cell.

### A.2 `kaggle_paths.yaml` (config override)

Create at `experiments/kaggle/kaggle_paths.yaml`:

```yaml
# Overrides paths in configs/default.yaml for Kaggle environment.
# Load order: default.yaml → kaggle_paths.yaml (deep merge).
paths:
  eyepacs:    "/kaggle/input/diabetic-retinopathy-detection"
  output_dir: "/kaggle/working/outputs"
training:
  num_workers: 2     # Kaggle CPU is weaker than local; safer at 2
  batch_size:  16    # T4 has 16 GB — keep batch_size 16, image_size 512
```

Verify `src/utils/config.py` supports passing multiple `--config` files for deep merge. If not, extend it:
- CLI: `python run_experiment.py exp1 --config configs/default.yaml --config kaggle/kaggle_paths.yaml --configs D`
- Implementation: merge dicts recursively, later configs win.

### A.3 Kaggle Dataset setup

EyePACS on Kaggle:
- Source: `kaggle competitions download -c diabetic-retinopathy-detection` (the 2015 Diabetic Retinopathy Detection competition by EyePACS).
- The notebook must **attach this competition's data as input**. After attach, the path is `/kaggle/input/diabetic-retinopathy-detection/`.
- Verify the directory layout matches what `EyePACSDataset` expects (see `experiments/src/data/datasets.py`). If structure differs (e.g., trainLabels.csv location, image folder names), add a tiny adapter at the top of the notebook that symlinks/restructures into `/kaggle/working/eyepacs/` before training.

### A.4 Notebook template (`train_config_d.ipynb`)

Cell structure:

```python
# Cell 1 — Clone repo and install deps
!git clone https://github.com/<USER>/<REPO>.git /kaggle/working/repo
%cd /kaggle/working/repo/experiments
!pip install -q -r requirements.txt
!pip install -q timm   # required by efficientnet.py but missing from requirements

# Cell 2 — Sanity checks
!nvidia-smi
!ls /kaggle/input/diabetic-retinopathy-detection | head
import torch; print(torch.__version__, torch.cuda.is_available())

# Cell 3 — Compute dataset stats (only fold 0 needs this; subsequent folds reuse)
# Skip if dataset_mean / dataset_std already populated in default.yaml.
!python scripts/compute_dataset_stats.py --config configs/default.yaml \
    --config kaggle/kaggle_paths.yaml

# Cell 4 — Compute PCA eigvecs for color augmentation (one-shot)
!python scripts/compute_pca_eigvecs.py --config configs/default.yaml \
    --config kaggle/kaggle_paths.yaml

# Cell 5 — Train ONE fold (Kaggle 12h limit → one fold per session/commit)
# Change --fold for each subsequent session: 0 → 1 → 2 → 3 → 4
!python run_experiment.py exp1 \
    --config configs/default.yaml \
    --config kaggle/kaggle_paths.yaml \
    --configs D \
    --fold 0 \
    --resume

# Cell 6 — Persist results to /kaggle/working/outputs so "Save Version" keeps them
!cp -r /kaggle/working/repo/experiments/outputs /kaggle/working/outputs_final
!ls -la /kaggle/working/outputs_final/exp1/checkpoints/fold_0/
```

### A.5 Multi-fold strategy (working around the 12h limit)

Option 1 — **Five committed versions** (recommended, simplest):
- Run notebook with `--fold 0`, Save Version (Quick Save, "Save & Run All").
- After it completes, in the next version add the previous output as a Kaggle Dataset input, then run `--fold 1 --resume`. Repeat through fold 4.

Option 2 — **Checkpoint relay**:
- After fold N completes, download `outputs/exp1/checkpoints/fold_N/best.pt` from notebook output.
- Upload to a private Kaggle Dataset `<user>/dr-config-d-checkpoints`.
- New notebook session: attach the dataset, copy checkpoints back into `outputs/exp1/checkpoints/`, run `--fold N+1`.

Option 3 — **Single long session** (only viable if total training fits in 12h):
- Skip Cell 5's `--fold` and run all 5 folds. EfficientNet-B3 on 35k images × 20 epochs × 5 folds is typically >12h on T4, so this usually fails partway. Use only if you've confirmed timings on a 1-fold dry run.

### A.6 Outputs to retrieve

After all folds complete, the notebook output should contain:
- `outputs/exp1/metrics.csv` — per-epoch metrics for all 5 folds, config D.
- `outputs/exp1/checkpoints/fold_{0..4}/best.pt` — best checkpoint per fold (monitor: `val_weighted_f1`).
- `outputs/exp1/logs/` — training logs.

Download all of `outputs/exp1/` and place it locally at `experiments/outputs/exp1/`.

### A.7 Verification

Run locally after download:
```bash
cd experiments
python scripts/verify_exp1.py
```
Expect: 5 folds present, each with `best.pt`, dominance check vs Config C reported.

---

## Part B — Real Demo.js inference (FastAPI backend)

### B.1 Server folder layout

Create a new top-level folder `E:/dissertation-project/server/`:

```
server/
├── README.md
├── requirements.txt
├── Dockerfile
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app + endpoints
│   ├── inference.py       # Model loading + predict()
│   ├── preprocessing.py   # Wraps experiments/src/preprocessing/pipeline_v5
│   ├── gradcam.py         # Optional: Grad-CAM on demand
│   ├── schemas.py         # Pydantic request/response models
│   └── config.py          # Settings (checkpoint path, host, port)
├── checkpoints/
│   └── config_d_fold0.pt  # Symlink or copy from experiments/outputs/exp1/...
└── tests/
    └── test_inference.py
```

### B.2 Reuse experiments code (do NOT duplicate)

The server imports preprocessing + model code directly from `experiments/`:

```python
# server/app/preprocessing.py
import sys
from pathlib import Path
EXPERIMENTS_ROOT = Path(__file__).resolve().parents[2] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_ROOT))

from src.preprocessing.pipeline_v5 import PreprocessingPipelineV5
from src.preprocessing.config import PreprocessingV5Config

def build_inference_pipeline() -> PreprocessingPipelineV5:
    config = PreprocessingV5Config.from_preset("efficientnet")
    # is_training=False → no augmentation, deterministic CLAHE
    return PreprocessingPipelineV5.create_for_inference(config)
```

If `create_for_inference` does not exist in `pipeline_v5.py`, add it — mirror `create_for_training` but with `is_training=False` and CLAHE deterministic (no stochastic application).

### B.3 `inference.py`

Responsibilities:
- Load `models/efficientnet_b3` via `experiments/src/models/factory.create_model(name="efficientnet_b3", in_channels=4, num_classes=5)`.
- Load checkpoint state dict from `checkpoints/config_d_fold0.pt`.
- Run preprocessing pipeline on raw image bytes (RGB), convert to tensor `[1, 4, 512, 512]`.
- For bilateral input: run both eyes, return per-eye + patient-level (worst-eye) result.

Per-eye response shape (must match what the current `Demo.js` already renders):
```json
{
  "pred": 2,
  "probs": [0.05, 0.10, 0.55, 0.20, 0.10],
  "confidence": 0.55,
  "latency_ms": 412
}
```

Patient-level response:
```json
{
  "pred": 2,
  "probs": [...],
  "confidence": 0.55,
  "latency_ms": 480,
  "per_eye": [
    {"eye": "left",  "pred": 1, "probs": [...], "confidence": 0.62, "latency_ms": 240},
    {"eye": "right", "pred": 2, "probs": [...], "confidence": 0.55, "latency_ms": 240}
  ]
}
```

This shape is intentionally identical to what `patientPrediction()` in `Demo.js` currently produces, so the frontend changes stay minimal.

### B.4 `main.py` — endpoints

```
POST /api/predict
  body: multipart/form-data { left?: File, right?: File }
  returns: PatientPredictionResponse (see B.3)

POST /api/gradcam
  body: multipart/form-data { eye: "left"|"right", image: File }
  returns: { gradcam_png_b64, attention_overlay_png_b64 }

GET /api/health
  returns: { status: "ok", model: "config-D", checkpoint: "fold0", device: "cuda"|"cpu" }
```

CORS: allow the demo origin (dev `http://localhost:3000`, prod whatever).

Model is loaded once at startup (`@app.on_event("startup")`), kept on GPU if available, CPU fallback. Add a global `asyncio.Lock` if multiple requests would otherwise race on a single CUDA stream.

### B.5 `requirements.txt`

```
fastapi>=0.115
uvicorn[standard]>=0.32
python-multipart>=0.0.9
torch>=2.1
torchvision>=0.16
timm>=1.0
opencv-python-headless>=4.8
numpy>=1.24
Pillow>=10.0
pydantic>=2.0
```

### B.6 Dockerfile (for HuggingFace Spaces / Render deployment)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY experiments/src /app/experiments/src
COPY experiments/configs /app/experiments/configs
COPY server /app/server
COPY checkpoints /app/checkpoints
ENV PYTHONPATH=/app/experiments:/app/server
EXPOSE 7860
CMD ["uvicorn", "server.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

Note: HuggingFace Spaces requires port `7860`. For Render or self-hosting, change accordingly.

### B.7 Local dev

```bash
cd E:/dissertation-project
# Copy a trained checkpoint into place:
cp experiments/outputs/exp1/checkpoints/fold_0/best.pt server/checkpoints/config_d_fold0.pt

# Install + run
pip install -r server/requirements.txt
uvicorn server.app.main:app --reload --host 0.0.0.0 --port 8000
# → server now serving at http://localhost:8000
```

Smoke test:
```bash
curl -F "left=@experiments/data/sample_left.jpg" \
     -F "right=@experiments/data/sample_right.jpg" \
     http://localhost:8000/api/predict
```

### B.8 Tests (`server/tests/test_inference.py`)

Minimum coverage:
- `test_health` — 200 OK and reports loaded checkpoint.
- `test_predict_left_only` — single-eye request, returns valid shape, probs sum to ~1.
- `test_predict_both_eyes` — bilateral, `per_eye` length is 2, patient `pred == max(per_eye[*].pred)`.
- `test_predict_rejects_non_image` — 400 on a text upload.
- `test_preprocessing_matches_training` — run pipeline on one EyePACS image twice, assert outputs are identical and shape `[4, 512, 512]`.

---

## Part C — Wire `Demo.js` to the backend

### C.1 New env-driven API URL

Add to `E:/dissertation-project/demo/.env.development`:
```
REACT_APP_API_URL=http://localhost:8000
```
Add to `E:/dissertation-project/demo/.env.production` (set after deployment):
```
REACT_APP_API_URL=https://<your-space>.hf.space
```

### C.2 New file: `demo/src/tabs/_apiPredict.js`

Encapsulates the network call so `Demo.js` stays readable:

```js
// demo/src/tabs/_apiPredict.js
const API = process.env.REACT_APP_API_URL || '';

async function dataUrlToBlob(dataUrl) {
  const r = await fetch(dataUrl);
  return await r.blob();
}

export async function predictPatient(eyes) {
  // eyes: [{ eye: 'left'|'right', src: dataURL|publicPath, name }]
  const fd = new FormData();
  for (const e of eyes) {
    let blob;
    if (e.src.startsWith('data:')) {
      blob = await dataUrlToBlob(e.src);
    } else {
      // sample image from /public — fetch through CRA so dev proxy/cors works
      const r = await fetch(e.src);
      blob = await r.blob();
    }
    fd.append(e.eye, blob, e.name || `${e.eye}.png`);
  }
  const t0 = performance.now();
  const res = await fetch(`${API}/api/predict`, { method: 'POST', body: fd });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  const json = await res.json();
  json.client_latency_ms = Math.round(performance.now() - t0);
  return json;
}

export async function isApiHealthy() {
  try {
    const r = await fetch(`${API}/api/health`, { method: 'GET' });
    return r.ok;
  } catch {
    return false;
  }
}
```

### C.3 Modify `demo/src/tabs/Demo.js`

Concrete edits — keep simulation as fallback (controlled by a `useRealModel` toggle so the demo still works offline):

1. **Add imports near the top:**
   ```js
   import { predictPatient, isApiHealthy } from './_apiPredict';
   ```
2. **Add health check state** (top of `Demo()`):
   ```js
   const [apiHealthy, setApiHealthy] = useState(null); // null=unknown, bool=resolved
   const [useRealModel, setUseRealModel] = useState(true);
   useEffect(() => { isApiHealthy().then(setApiHealthy); }, []);
   ```
3. **Rewrite `handleRun`** to call the API when `useRealModel && apiHealthy`:
   ```js
   const handleRun = async () => {
     if (eyes.length === 0) return;
     setRunning(true);
     setResult(null);
     setFeedbackMode(null);
     try {
       if (useRealModel && apiHealthy) {
         const r = await predictPatient(eyes);
         // Normalize: API returns per_eye (snake_case), simulator uses perEye.
         setResult({
           pred: r.pred,
           probs: r.probs,
           confidence: r.confidence,
           latencyMs: r.latency_ms,
           perEye: r.per_eye.map(p => ({
             eye: p.eye,
             src: eyes.find(e => e.eye === p.eye)?.src,
             result: {
               pred: p.pred, probs: p.probs,
               confidence: p.confidence, latencyMs: p.latency_ms,
             },
           })),
         });
       } else {
         // Fallback to simulator (unchanged code path).
         const r = patientPrediction(eyes);
         setResult(r);
       }
     } catch (e) {
       console.error(e);
       setToast(`Inference failed: ${e.message}. Falling back to simulator.`);
       setTimeout(() => setToast(''), 4000);
       setResult(patientPrediction(eyes));
     } finally {
       setRunning(false);
     }
   };
   ```
4. **Status badge in the Run section** (near the existing model-version span):
   ```jsx
   {apiHealthy === null && <span style={{fontSize:10,color:C.gray}}>checking model…</span>}
   {apiHealthy === true  && <span style={{fontSize:10,color:C.greenT}}>● real model</span>}
   {apiHealthy === false && <span style={{fontSize:10,color:C.amberT}}>● simulator (API offline)</span>}
   ```
5. **Update the footer Note** to reflect actual mode:
   ```jsx
   <Note>
     {apiHealthy
       ? <>Predictions from Config D checkpoint (EfficientNet-B3, fold 0). F1={D.f1.toFixed(3)}, AUC={D.auc.toFixed(3)}, κ={D.k.toFixed(3)}.</>
       : <>Simulated Config D output (backend unavailable). Reported reference metrics: F1={D.f1.toFixed(3)}, AUC={D.auc.toFixed(3)}, κ={D.k.toFixed(3)}.</>}
   </Note>
   ```

### C.4 Translation keys

Add to `demo/src/i18n/` (in both EN and RU dictionaries):
- `demo.modelStatus.checking`
- `demo.modelStatus.real`
- `demo.modelStatus.simulator`
- `demo.modelStatus.fallbackToast`

Replace the inline literals from step C.3 step 4 with `t('demo.modelStatus.*')`.

### C.5 (Optional) Real Grad-CAM

Currently `VisualizationBlock` shows pre-rendered Grad-CAMs only for walkthrough images. When the backend is healthy and the user uploads custom images, call `/api/gradcam` after `/api/predict` and render returned base64 PNGs in the same layout. Gate this behind `caseRef === null && apiHealthy` so walkthrough images keep using their pre-rendered assets (faster, deterministic).

---

## Part D — Deployment

### D.1 Local-only (development)
1. Train Config D on Kaggle (Part A).
2. Download checkpoint into `server/checkpoints/`.
3. Start FastAPI locally (Part B.7).
4. `cd demo && npm start` — Demo.js auto-picks up `REACT_APP_API_URL=http://localhost:8000`.

### D.2 Public demo (HuggingFace Spaces, recommended)
1. Create a new Space, SDK: Docker.
2. Push `Dockerfile`, `server/`, `experiments/src/`, `experiments/configs/`, and a `.gitattributes` with `*.pt filter=lfs diff=lfs merge=lfs -text`.
3. Add the checkpoint via Git LFS (or as a Hub Model repo linked at runtime).
4. After Space builds, set `REACT_APP_API_URL` in `demo/.env.production` to `https://<user>-<space>.hf.space`.
5. `cd demo && npm run build`. Deploy `demo/build/` to GitHub Pages / Vercel / Netlify.

### D.3 Spending caps
- HF Spaces free CPU tier is enough for demo-level traffic (slow first request: ~5–10 s on CPU per eye). If demo latency matters, upgrade to a T4 small ($0.60/h, only while requests come in).

---

## Part E — Acceptance checklist

Tick each item before marking the task complete.

- [ ] `experiments/kaggle/train_config_d.ipynb` runs end-to-end on a fresh Kaggle session (verified with `--fold 0`). — notebook ready; **manual Kaggle run**.
- [ ] All 5 folds produce `best_model.pt` (under `D_fold{N}/`) and `metrics.csv` rows. — **manual training**.
- [ ] `experiments/scripts/verify_exp1.py` reports dominance check vs Config C without errors. — needs trained folds.
- [x] `server/` implemented; `GET /api/health` returns `model: "config-D"`. (To boot: `pip install -r server/requirements.txt`.)
- [x] `POST /api/predict` returns valid JSON matching the B.3 schema (predict logic verified on random-init weights).
- [ ] `server/tests/test_inference.py` passes. — tests written; run in an env with `fastapi`/`torch`.
- [x] `Demo.js` shows green "● real model" badge when the backend is up (and a checkpoint is loaded).
- [ ] Predictions are model-derived, not the simulator's hash-based RNG. — true once a real checkpoint is loaded (manual, post-training).
- [x] When the backend is stopped, Demo.js shows amber "● simulator" badge and still works (graceful fallback).
- [x] No hardcoded paths in `server/` or `experiments/kaggle/` (`grep "E:/"` clean; all paths from config/env).
- [x] README present in `server/README.md` and `experiments/kaggle/README.md`.

---

## Out of scope (explicitly)

- Retraining all 5 configs (A/B/C/D) on Kaggle — only D is required.
- Browser-side ONNX inference — was rejected in favor of FastAPI backend.
- User authentication / rate limiting on the API — add later if the demo gets exposed publicly.
- Persisting relabel history server-side — the existing localStorage + JSONL export flow stays.

---

## Risks & mitigations

| Risk | Mitigation |
|---|---|
| Kaggle session times out mid-fold | `--resume` is already wired; each fold should fit in 12h. If not, reduce `max_epochs` to 15 (early stopping rarely lets it run all 20 anyway). |
| EfficientNet-B3 fp16 overflow on T4 | Already handled: `models.efficientnet_b3.mixed_precision: false` in `default.yaml`. Do not flip this. |
| EyePACS folder layout on Kaggle differs from local | Add restructuring shell snippet at top of notebook (symlinks into expected layout) before any code path touches the dataset. |
| Checkpoint too large for HF Spaces free tier | EfficientNet-B3 weights are ~50 MB — well under limits. |
| Preprocessing drift between training and inference | Server imports the *same* `pipeline_v5` module as training. Add `test_preprocessing_matches_training` (B.8) to lock this in. |

---

End of TASK.md.
