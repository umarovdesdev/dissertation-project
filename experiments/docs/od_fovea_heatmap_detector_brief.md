# OD / Fovea Heatmap Detector — Build Brief (standalone project)

**Audience:** an autonomous coding agent (ChatGPT Codex) that will build this as a
**separate, self-contained repository**. It will later be reviewed and integrated into the
dissertation monorepo (`experiments/src/preprocessing/`) by the maintainer.

**Goal.** Replace the current brittle classical OD/fovea detector with a **learned
heatmap-regression detector** that, for any color fundus image, outputs a **probability
heatmap** for the optic-disc (OD) center and a probability heatmap for the fovea center,
plus sub-pixel coordinates and a *real* per-landmark confidence derived from the heatmap.

This brief is binding on the public API (§6) and the acceptance criteria (§9). Everything
else is a strong recommendation — deviate only with a documented reason.

---

## 1. Why we are doing this (context, do not skip)

The monorepo's preprocessing pipeline has a Stage 1 "OD–fovea rotation normalization" that
currently uses a **classical CV** detector (`od_fovea_detect.py`): OD = centroid of the
brightest blurred region; fovea = darkest point in an annulus around the OD.

Validation against IDRiD localization ground-truth (516 images) showed:

- **OD:** median ~0.67 OD-radii error, ~65 % within 1 OD-radius — mediocre but usable.
- **Fovea: fails.** Median ~5 OD-radii, ~0 % within 2 OD-radii. The "darkest-in-annulus"
  search **latches onto the dark vignette** at native resolution.
- The old `confident` flag is **useless**: it is `True` for 100 % of images, including
  every fovea failure. It cannot gate a fallback.

**Two lessons that must shape the new design:**

1. **Do not detect on the raw native-resolution image.** Detect on a FOV-cropped, resized,
   illumination-normalized frame so the dark vignette is gone (see §5 coordinate frame).
2. **Confidence must be a genuine quantity** derived from the predicted heatmap (peak
   sharpness / spatial spread), not a boolean that is always true (see §7).

---

## 2. Reference methods and repositories (reproduce, don't reinvent)

Use these as the proven blueprint. The first is the primary reference.

| Ref | What | Use for |
|-----|------|---------|
| **FundusPosNet** (IEEE Access 2021, Manipal) — `github.com/bhargav-jb/FundusPosNet` | Encoder–decoder **heatmap regression**, joint OD+fovea, ~12.9M params, dilated convs, trained on **413 IDRiD** images, 2D-Gaussian targets, BCE loss, Adam lr=1e-3, 800 epochs. SOTA on IDRiD/Messidor/G1020. (Keras.) | **Primary architecture & target-encoding reference.** Reimplement the idea in PyTorch. |
| **anibali/dsntnn** (PyTorch; also in Kornia ≥0.1.4) | DSNT layer: differentiable soft-argmax from a heatmap → sub-pixel coordinates, with no extra parameters, works at low heatmap resolution. | **Coordinate decoding + uncertainty head** (recommended over plain argmax). |
| **berenslab/fundus_image_toolbox** (MIT, `pip install fundus_image_toolbox`) | Multi-task EfficientNet trained on **ADAM+REFUGE+IDRiD**, returns `[fovea_x, fovea_y, od_x, od_y]`. | **Sanity baseline / fallback.** Run it first to get a known-good reference number and as an optional ensemble teacher. MIT license = safe to vendor. |
| **minesmeyer/od-fovea-regression** | Pixel-wise distance-to-landmark regression (FCN). | Alternative robust formulation if heatmap peaks prove unstable. |
| **JOINED** (PMLR 2022, `arxiv.org/abs/2203.00461`) | Prior-guided multi-task OD/cup segmentation + fovea detection. | Inspiration for using OD segmentation as an auxiliary task to stabilize OD. |
| Multiresolution cascaded attention U-Net (Sci. Rep. 2024, `nature.com/articles/s41598-024-73493-7`) | Localization + segmentation of OD/fovea via heatmaps. | Architecture variant if a plain U-Net underperforms. |

**Recommended concrete stack for us:** PyTorch (the monorepo is PyTorch 2.5 + timm), a
**U-Net with a `timm` encoder (ResNet-18 or EfficientNet-B0)**, **2 output channels**
(OD, fovea), and a **DSNT head** for decoding + uncertainty. This matches our toolchain and
runs comfortably on an RTX 3060 12 GB. (FundusPosNet's custom dilated encoder–decoder is an
acceptable alternative, but the timm-U-Net is simpler to maintain.)

---

## 3. Data

### 3.1 Primary training/eval source — IDRiD localization

Layout (on the maintainer's machine `E:/datasets/IDRiD/C. Localization/`):

```
1. Original Images/a. Training Set/IDRiD_XXX.jpg      (413 images)
1. Original Images/b. Testing Set/IDRiD_XXX.jpg       (103 images)
2. Groundtruths/1. Optic Disc Center Location/{a.train, b.test}_..._Markups.csv
2. Groundtruths/2. Fovea Center Location/{train,test}_..._Markups.csv
```

CSV columns of interest: `Image No`, `X- Coordinate`, `Y - Coordinate` (in **original-image
pixels**; ignore trailing empty columns). Parse only rows whose first cell starts with
`IDRiD_`.

- **Train the detector on the 413-image Training Set only.**
- **The 103-image Testing Set is a held-out honest test set. Never train or tune on it.**
  (The monorepo's `validate_od_fovea_idrid.py` currently reports train+test together; our
  acceptance numbers in §9 are **test-split only**.)

### 3.2 Optional auxiliary data (to improve cross-camera generalization)

IDRiD is a single camera (Kowa). The detector must run on EyePACS, APTOS, Messidor-2, DDR,
ODIR-5K, RFMiD (many cameras). To generalize:

- **OD auxiliary:** add OD-segmentation sets — IDRiD segmentation subset (81 OD masks),
  REFUGE, ADAM, RIGA — converting masks to OD-center heatmaps. Optional second task.
- Keep **fovea** supervised from IDRiD (scarce GT) plus any Messidor release with fovea
  coordinates if available.
- If extra labeled data is unavailable, rely on **aggressive augmentation** (§4). Landmark
  heatmap nets are data-efficient; 413 images + augmentation is a viable baseline.

### 3.3 Coordinate frame for training (critical — fixes the vignette bug)

Train and infer on a **FOV-cropped, isotropically-resized 512×512 frame**, not the raw
image. In the monorepo this transform already exists
(`src/preprocessing/crop_resize.py::crop_and_resize(image, target_size=512,
return_transform=True)`), returning a `CropResizeTransform` with `.apply(x,y)` (pre-crop →
canvas). For this standalone project, **reimplement an equivalent FOV crop** (detect fundus
bounding box, isotropic resize, center pad) and **transform the GT coordinates through the
same affine** so targets live in the 512×512 frame. Keep the forward+inverse affine params
so coordinates can be mapped back to original-image pixels for evaluation.

---

## 4. Targets and augmentation

- **Target heatmaps:** for each landmark, a 2D-Gaussian centered on the (transformed) GT
  coordinate, rendered on the decoder output grid (e.g. 128×128). Start with
  **σ ≈ 0.02 × output_side** (≈ OD-radius scale); expose σ as a config knob and sweep it.
- **Augmentation (apply identically to image and to GT heatmap/coordinate):**
  random rotation (±25°), scale (0.85–1.15), translation, horizontal flip
  (swaps eye laterality — fine, heatmaps flip with the image), brightness/contrast, gamma,
  mild color jitter, mild Gaussian blur, and **simulated illumination/vignette** to harden
  against the exact failure mode of the old detector. Keep an augmentation-off validation
  pass.

---

## 5. Model + decoding

- **Backbone:** U-Net, encoder = `timm` ResNet-18 or EfficientNet-B0 (ImageNet-pretrained).
- **Head:** 2-channel heatmap → **DSNT** (`dsntnn`/Kornia) → 2 sub-pixel coordinates.
- **Input:** 3-channel RGB, 512×512 (the FOV-cropped frame). Heatmap output 128×128.
- **Loss:** DSNT recipe = **Euclidean** (predicted coord vs GT coord) + **Jensen–Shannon
  divergence** regularization keeping the heatmap a compact Gaussian. (FundusPosNet's
  per-pixel BCE/MSE on the Gaussian target is an acceptable alternative baseline — implement
  both behind a flag and compare.)
- **Joint vs separate:** predict both landmarks jointly (shared encoder) — the fixed
  OD↔fovea geometry is a useful implicit prior, as in FundusPosNet/JOINED.

---

## 6. PUBLIC API — binding integration contract

The standalone project must ship an inference entry point that the maintainer can wrap to
**exactly reproduce** the monorepo's existing function signature, so it drops in with no
downstream changes (`pipeline.py`, the demo server, and `validate_od_fovea_idrid.py` all
call this):

```python
@dataclass
class ODFoveaResult:
    od_center: tuple[int, int]      # (x, y) in INPUT-image pixels
    od_radius: float                # pixels (estimate; may be fixed prior or from OD seg)
    fovea_center: tuple[int, int]   # (x, y) in INPUT-image pixels
    fovea_radius: float             # pixels
    distance: float                 # euclidean OD<->fovea, pixels
    angle_rad: float                # atan2(dy, dx) of OD->fovea vector
    angle_deg: float
    rotation_sigma_deg: float       # adaptive rotation sigma for augmentation
    confident: bool                 # derived from confidence threshold (see §7)
    # NEW fields (additive — keep the above intact):
    od_confidence: float            # [0,1], from OD heatmap
    fovea_confidence: float         # [0,1], from fovea heatmap
    od_heatmap: np.ndarray | None   # float32 prob map, resized to input frame (optional return)
    fovea_heatmap: np.ndarray | None

def detect_od_fovea(image_rgb: np.ndarray) -> ODFoveaResult: ...
```

**Hard requirements:**

- Input is an **RGB uint8** array `(H, W, 3)` at arbitrary resolution. The function must
  internally FOV-crop+resize to 512, run the net, and **map coordinates back to input-image
  pixels** before returning. (Callers pass the full image and expect input-frame coords —
  this is how the existing validation compares against IDRiD original-pixel GT.)
- Weights load **once** (lazy singleton), CPU and CUDA both supported.
- Pure function, deterministic, no global state beyond the cached model.
- No hardcoded paths; weights path from config/argument; use `pathlib.Path`.
- Type hints on every signature; Args/Returns docstrings. All code/comments in English.

---

## 7. Confidence (this is the whole point — must be real)

From the **softmax-normalized** predicted heatmap `H` (sums to 1 over pixels):

- **peak** `p_max = max(H)`,
- **spread** `σ_eff = sqrt(Var_x + Var_y)` from DSNT second moments.

Define `confidence ∈ [0,1]` as a monotone function of high peak + low spread (e.g.
`exp(-σ_eff / σ_ref)`, or a calibrated logistic). **Calibrate the threshold on the IDRiD
test split** by correlating `σ_eff` with actual Euclidean error, and report that
correlation. A diffuse or multi-modal map ⇒ low confidence.

Downstream contract: when `od_confidence`/`fovea_confidence` is below threshold, the caller
will **skip rotation normalization** and **pivot polar-CLAHE on the FOV centroid** instead
of the detected fovea. So the confidence must actually track error — demonstrate it.

`rotation_sigma_deg`: derive from positional uncertainty as the existing code does —
`σ_θ = degrees(atan(σ_pos / distance))`, capped at 15°, where `σ_pos` now comes from the
**heatmap spreads** (real uncertainty) rather than fixed radii.

---

## 8. Deliverables (standalone repo)

```
od-fovea-detector/
  README.md                  # what it is, install, train, infer, results table
  requirements.txt           # pinned; torch, timm, dsntnn or kornia, opencv, numpy, pandas
  configs/default.yaml       # all knobs: paths, sigma, lr, epochs, backbone, heatmap size
  src/
    data.py                  # IDRiD loader + FOV-crop affine + GT->heatmap targets
    model.py                 # U-Net(timm encoder) + DSNT head
    losses.py                # DSNT (euclidean + JS) and BCE/MSE baseline behind a flag
    train.py                 # training loop, early stopping on IDRiD-test EMD, seed=42
    infer.py                 # detect_od_fovea(image_rgb) -> ODFoveaResult  (the §6 API)
    confidence.py            # heatmap -> (coord, p_max, sigma_eff, confidence)
    eval.py                  # reproduce the metrics JSON format below + montage PNG
  weights/od_fovea_unet.pt   # trained weights (+ link if too large for git)
  outputs/eval_report.json   # metrics on IDRiD test (and any extra sets)
  outputs/montage.png        # predicted (solid) vs GT (cross) markers
```

`eval.py` must emit a metrics JSON with the **same shape** as the monorepo's
`outputs/validation/od_fovea_idrid_metrics.json` (per-split `od`/`fovea` blocks with
`error_px` {median,mean,p90,max,n}, `error_od_radii`, `success_within_1_od_radius`,
`success_within_2_od_radii`) plus a `confidence_vs_error` correlation block, so results are
directly comparable to the old classical detector.

Reproducibility: fixed seed (42), deterministic flags, document exact train/test image IDs
used.

---

## 9. Acceptance criteria (test split only, must beat the classical baseline)

On the **IDRiD 103-image Testing Set** (never seen in training):

- **Fovea:** median error **< 1.0 OD-radius**, and **≥ 90 % within 1 OD-radius**.
  (Baseline classical detector: ~5 OD-radii, ~0 % within 2R — any competent heatmap model
  beats this by a wide margin.)
- **OD:** median error **≤ 0.5 OD-radius**, **≥ 95 % within 1 OD-radius**.
- **Confidence is informative:** Spearman correlation between `σ_eff` and actual error is
  positive and significant; low-confidence flagging captures the worst-error cases.
- **Cross-camera sanity:** qualitative montage on a sample of EyePACS/APTOS images shows
  visually correct OD and fovea (no GT there, so eyeball it).
- **Runtime:** ≤ ~50 ms/image on the RTX 3060 (GPU), ≤ ~300 ms on CPU. (Coords are
  deterministic once weights are frozen, so the monorepo will cache them — but keep it fast.)

If fovea cannot clear the bar with IDRiD alone, add the §3.2 auxiliary OD data and/or revisit
σ and augmentation before changing the architecture.

---

## 10. Pitfalls — read before coding

1. **Never run the net on the raw native image.** Always FOV-crop + resize first; the dark
   border/vignette is what broke the old fovea search.
2. **No test-set leakage.** Train on 413, evaluate on 103. Do not tune σ/threshold on test —
   use a held-out slice of train for that, then report test once.
3. **Coordinate frames.** GT is original-image pixels; you train in the 512 frame; the API
   returns input-image pixels. Keep the affine and its inverse exact — off-by-frame bugs
   look like "the model is bad" but are just mapping errors.
4. **Horizontal flip** swaps left/right eye AND OD↔fovea laterality; that is fine for a
   landmark task as long as the target heatmaps flip with the image. Do not "fix" the eye
   side.
5. **Confidence must move with error**; if it doesn't, the fallback gate is worthless (that
   was the old bug). Prove the correlation in the eval report.
6. **License hygiene:** if you vendor any weights/code from FundusPosNet or berenslab, record
   the license; the monorepo prefers MIT/permissive.

---

## 11. After delivery — integration plan (maintainer, for awareness)

The maintainer will: (a) port `infer.py` into
`experiments/src/preprocessing/od_fovea_net/`, wrap it behind the existing
`detect_od_fovea(image_rgb) -> ODFoveaResult` facade (adding the new confidence fields),
drop weights into `weights/`; (b) **reorder early pipeline stages** so detection runs on the
FOV-cropped frame (`flip → FOV crop+resize → detect → rotate → mask → flat-field → CLAHE`);
(c) re-run `validate_od_fovea_idrid.py` to confirm the §9 numbers in-repo; (d) let
polar-CLAHE pivot on the detected fovea when confidence is high (the `fovea_xy` override
already exists), else FOV centroid; (e) cache OD/fovea coords + confidence into the Stage 0–4
cache; (f) amend governance: INVARIANTS.md **OD-3 / Stage 1** definition changes from
"classical CV (brightest/darkest)" to "frozen, pre-trained heatmap detector" — note the
detector is **pre-trained and frozen**, not co-trained with the DR-CNN, so the central thesis
"model = preprocessing + CNN" is preserved (preprocessing stays fixed).
