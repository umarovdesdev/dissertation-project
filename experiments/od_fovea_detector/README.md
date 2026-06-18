# OD / Fovea Heatmap-Regression Detector

A standalone, learned optic-disc (OD) and fovea localizer for color fundus
images. It replaces the brittle classical detector
(`experiments/src/preprocessing/od_fovea_detect.py`, which fails on the fovea by
latching onto the dark vignette) with an **encoder–decoder heatmap-regression**
model that outputs, per landmark, a probability heatmap, a sub-pixel
coordinate, and a **genuine confidence** derived from the heatmap spread.

This is a self-contained project intended to be reviewed and then integrated
into the monorepo by the maintainer (see *Integration* below). It is **not**
wired into the live preprocessing pipeline.

## What it does

* **Coordinate frame.** Detects on a FOV-cropped, isotropically-resized 512×512
  frame (vignette removed), then maps coordinates back to input-image pixels.
* **Architecture.** U-Net with a `timm` encoder (ResNet-18 default,
  EfficientNet-B0 option), 2 output channels (OD, fovea), shared encoder so the
  fixed OD↔fovea geometry is an implicit prior.
* **Decoding.** DSNT (differentiable soft-argmax) → sub-pixel coordinate +
  second-moment spread. A compact DSNT implementation is vendored in
  `src/dsnt.py`, so neither `kornia` nor `dsntnn` is required to run (either can
  be swapped in).
* **Confidence.** `confidence = exp(-sigma_eff / sigma_ref)` from the heatmap
  spread — a real quantity that tracks error, unlike the old always-true flag.
* **Losses.** DSNT (Euclidean + Jensen–Shannon regularization) by default;
  per-pixel MSE/BCE on Gaussian targets behind a config flag.

## Layout

```
od_fovea_detector/
  README.md
  requirements.txt
  configs/default.yaml        all knobs (paths, sigma, lr, epochs, backbone, sizes, seed)
  src/
    geometry.py               FOV-crop + forward/inverse affine + Gaussian targets (torch-free)
    dsnt.py                   vendored DSNT (torch path + numpy mirror)
    confidence.py             heatmap -> (coord, p_max, sigma_eff, confidence)  (torch-free)
    data.py                   IDRiD loader + targets + augmentation Dataset
    model.py                  U-Net(timm encoder) + heatmap head + DSNT decode
    losses.py                 DSNT loss + heatmap MSE/BCE baseline
    train.py                  deterministic training loop, early stop on held-out TRAIN slice
    infer.py                  detect_od_fovea(image_rgb) -> ODFoveaResult  (the §6 API)
    eval.py                   metrics JSON (monorepo shape) + Spearman + montage
    utils.py                  config load + device resolution
  scripts/smoke_test.py       synthetic train->infer->eval (no dataset)
  tests/                      pytest/unittest; torch-free tests + torch-gated contract test
  weights/                    trained weights land here (od_fovea_unet.pt)
  outputs/                    eval_report.json + montage.png
```

## Install

Use the monorepo conda env (PyTorch 2.5 + timm):

```bash
conda activate dr-classifier
pip install -r requirements.txt   # only if any pin is missing in the env
```

The torch-free tests need only `numpy`, `opencv-python`, `Pillow`. `kornia` and
`dsntnn` are optional (vendored DSNT is used by default).

## Train (real, on IDRiD)

Trains on the **413-image IDRiD Training Set only**; a `val_fraction` slice of
TRAIN is held out for early stopping and threshold calibration. The 103-image
Testing Set is never touched during training.

```bash
conda activate dr-classifier
cd experiments/od_fovea_detector
# Edit configs/default.yaml -> data.idrid_root if needed.
python -m src.train --config configs/default.yaml
# Quick sanity run:
python -m src.train --config configs/default.yaml --epochs 2
```

Weights are written to `weights/od_fovea_unet.pt` (path from `io.weights_path`).

## Evaluate (real, on IDRiD test split — the acceptance numbers)

```bash
conda activate dr-classifier
python -m src.eval --config configs/default.yaml --weights weights/od_fovea_unet.pt --split test
```

Outputs `outputs/eval_report.json` (same shape as the monorepo's
`outputs/validation/od_fovea_idrid_metrics.json`: per-split `od`/`fovea` blocks
with `error_px` {median,mean,p90,max,n}, `error_od_radii`,
`success_within_1_od_radius`, `success_within_2_od_radii`) plus a
`confidence_vs_error` Spearman block, and `outputs/montage.png`.

**Acceptance (test split only):** fovea median < 1.0 OD-radius and ≥ 90% within
1 OD-radius; OD median ≤ 0.5 OD-radius and ≥ 95% within 1 OD-radius; positive,
significant Spearman between `sigma_eff` and error.

## Inference API (binding contract — §6)

```python
from src.infer import detect_od_fovea
import cv2
img = cv2.cvtColor(cv2.imread("fundus.jpg"), cv2.COLOR_BGR2RGB)
res = detect_od_fovea(img)            # weights load once (lazy singleton)
res.od_center, res.fovea_center       # (x, y) in INPUT-image pixels
res.od_confidence, res.fovea_confidence
res.od_heatmap, res.fovea_heatmap     # prob maps resized to the input frame
```

`ODFoveaResult` reproduces the monorepo dataclass exactly and **adds**
`od_confidence`, `fovea_confidence`, `od_heatmap`, `fovea_heatmap`. CPU and
CUDA are both supported (`device="cpu"|"cuda"|"auto"`).

## Tests

```bash
# Torch-free (pass with only numpy/opencv/Pillow):
python -m unittest discover -s tests -v
# or, with pytest:
pytest tests -v

# Synthetic end-to-end smoke test (requires torch + timm):
python scripts/smoke_test.py
```

Torch-free tests cover: target-heatmap rendering, the FOV-crop affine
round-trip (forward∘inverse ≈ identity), DSNT peak recovery, and confidence
monotonicity (sharp > diffuse). The contract test and smoke test require the
`dr-classifier` env (torch/timm) and skip cleanly otherwise.

## Reproducibility

Fixed seed (42), deterministic cuDNN flags. The exact train/test image IDs are
the IDRiD `IDRiD_*` ids present in both the OD and fovea markup CSVs of each
split (413 train / 103 test).

## Integration (maintainer)

1. Port `src/infer.py` into `experiments/src/preprocessing/od_fovea_net/`, wrap
   it behind the existing `detect_od_fovea(image_rgb) -> ODFoveaResult` facade
   (adding the new confidence fields), drop `weights/od_fovea_unet.pt` in.
2. **Reorder early pipeline stages** so detection runs on the FOV-cropped frame:
   `flip → FOV crop+resize → detect → rotate → mask → flat-field → CLAHE`.
3. Re-run `scripts/validate_od_fovea_idrid.py` to confirm the §9 numbers in-repo.
4. Let polar-CLAHE pivot on the detected fovea when confidence is high, else the
   FOV centroid.
5. Cache OD/fovea coords + confidence into the Stage 0–4 cache.
6. Amend governance: `INVARIANTS.md` OD-3 / Stage 1 changes from "classical CV"
   to "frozen, pre-trained heatmap detector" — pre-trained and **frozen**, not
   co-trained with the DR-CNN, so "model = preprocessing + CNN" is preserved.

## Licenses

The DSNT algorithm is from Nibali et al. (2018), reimplemented from the public
paper (no code vendored from `dsntnn`/`kornia`). `timm` encoders are
Apache-2.0. No FundusPosNet or berenslab weights/code are vendored.
```
