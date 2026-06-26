# Fundus SSL Pretraining — Build Brief (in-repo component)

**Audience:** the engineer/agent (ChatGPT Codex per the role split) who will implement the
self-supervised pretraining stage *inside the dissertation monorepo* under
`experiments/`. Claude plans/reviews; the implementer writes the training code and the
checkpoint loader.

**Goal.** Produce **in-domain, CNN-backbone-matched, label-free self-supervised
initializations** for **ResNet-50** and **EfficientNet-B3**, pretrained on EyePACS fundus
images that pass through the project's existing 4-channel preprocessing pipeline. These
checkpoints become the initialization for the **pipeline arm** of Experiment 1 (Configs **B**
and **D**). The **baseline arm** (Configs **A** and **C**) stays on ImageNet weights. This
realizes governance **CFC-2.8** (baseline ⟹ ImageNet, pipeline ⟹ SSL) and records the new
supporting contribution **SC-H**.

This brief is **binding** on: the SSL corpus and the disjointness invariant (§2), the
4-channel two-view augmentation contract (§4), the checkpoint artifact format and loader
contract (§9–§10), and the linear-probe acceptance gate (§8). Everything else is a strong
recommendation — deviate only with a documented reason.

> **Authority.** The pretraining-axis decision is **already made and locked** (governance
> v6.0.0; SSL corpus locked 2026-06-26 — see
> `PROJECT_MEMORY/config-d-pretraining.md`). This brief *restates and operationalizes* that
> decision; it does not re-open it. RETFound / ViT / MAE are **out of scope** and must not be
> reintroduced (rationale in §3).

---

## 1. Why we are doing this (context, do not skip)

The H-1 contrast in Experiment 1 is a 2×2 factorial of *(preprocessing × architecture)*. If
the pipeline arm were initialized from a **different backbone** (e.g. RETFound's ViT-L), then
"preprocessing" and "architecture/initialization" would be **confounded** and the causal
reading of H-1 would collapse. The candidate therefore chose an **architecture-matched,
in-domain initialization**: the *same* ResNet-50 and EfficientNet-B3 backbones used in the
baseline arm, but initialized from self-supervised pretraining **on fundus images** instead
of ImageNet.

Two consequences shape this design:

1. **The backbone must be identical** to the supervised one (same `conv1`/`conv_stem`, same
   trunk), so the SSL checkpoint drops into `create_resnet50(...)` /
   `create_efficientnet("b3", ...)` with **no architectural change** — only the weights
   differ. The only non-standard detail is the **4-channel stem** (RGB + FOV mask), which
   both the SSL encoder and the downstream classifier already use.
2. **The SSL init must be earned, not assumed.** Before any SSL checkpoint is allowed into
   Experiment 1, it must pass a **frozen-backbone linear-probe gate** (§8) showing it beats
   random init and is competitive with ImageNet on DR grading. From-scratch SSL on ~53k
   images is the *default*; if the gate fails, the **documented fallback** (§11) is
   ImageNet→continual-SSL — but that is a fallback, not the plan.

---

## 2. Governance & leakage invariants (binding)

These are hard constraints. A reviewer must be able to verify each one mechanically.

**INV-SSL-1 — SSL corpus is the EyePACS original "test" split.**
Pretraining uses the **53,576** images at `paths.eyepacs/test/*.jpeg`. Labels exist
(`paths.eyepacs/testLabels15.csv`, columns `image,level,Usage`) but are **UNUSED** for the
SSL objective — pretraining is **label-free**.

**INV-SSL-2 — Disjointness from Experiment 1 (no pretraining leakage).**
The SSL corpus (`test/`, 53,576) is **disjoint** from Experiment 1's evaluation corpus (the
**~35,126** images in `train/` governed by `trainLabels.csv`, 5-fold patient-level CV). The
two splits are separate EyePACS releases and share **no images and no patient IDs**. This is
analogous to ImageNet being a separate corpus for the baseline arm. The implementation MUST
include an explicit **disjointness assertion** (§3.3) that fails loudly if any overlap is
detected. The Exp 1 loader already reads only `train/`
(`src/data/datasets.py::EyePACSDataset.from_directory`, ~lines 209–248), so no Exp-1 code
changes are required — but the SSL job must still assert disjointness on its own inputs.

**INV-SSL-3 — Do NOT fold the 53k into Experiment 1 supervised training.**
Experiment 1's dataset (~35,126) is **governance-fixed**. The 53k corpus is
**pretraining-only**. It must never be concatenated into the supervised train/val folds.

**INV-SSL-4 — Baseline arm stays ImageNet.**
SSL weights initialize **only** Configs B and D (pipeline, 4-channel). Configs A and C
(baseline, 3-channel) keep `pretrained: true` = ImageNet. The clean contrast is
**ImageNet (baseline) vs fundus-only-SSL (pipeline)**.

**INV-SSL-5 — Frozen, pre-trained, not co-trained.**
SSL pretraining is a **separate, prior** stage. The resulting weights are an *initialization*
for Exp 1 fine-tuning; the SSL encoder is **not** co-trained with the DR classifier. The
central thesis "model = preprocessing + CNN" is preserved (preprocessing stays fixed; the
backbone is merely better-initialized).

**INV-SSL-6 — Method family restricted to CNN-compatible SSL.**
Allowed families: **BYOL / MoCo-v2 / SimSiam / DINO** (CNN-compatible). **MAE is excluded**
(ViT-only). **RETFound is excluded** (changes the backbone). **SimCLR-style large-batch
contrastive is disfavored** (negatives require batches our 12 GB GPU cannot reach at 256²;
see §5).

**Linkage:** records **SC-H**; bounded by **CFC-2.8**; resolves **AOQ-1(b)/AOQ-2/AOQ-4** per
governance v6.0.0. Any change to this brief that touches CFC-2.8 must be mirrored in
`thesis/governance/` (INVARIANTS.md, CONTRIBUTIONS.md) — out of scope for the implementer,
flag it to the maintainer.

---

## 3. Data specification

### 3.1 Corpus & paths (all from config, never hardcoded)

| Item | Value | Source |
|------|-------|--------|
| SSL image dir | `<paths.eyepacs>/test/` | new config key, see §3.4 |
| SSL image glob | `*.jpeg` | 53,576 files |
| Optional labels (probe only) | `<paths.eyepacs>/testLabels15.csv` | columns `image,level,Usage` |
| Exp-1 corpus (must stay disjoint) | `<paths.eyepacs>/train/` + `trainLabels.csv` | ~35,126 |

`paths.eyepacs` is already `"E:/datasets/EyePACS"` in `configs/default.yaml`. **No path may be
hardcoded** in code — read everything from the YAML (project rule, see §13). Use
`pathlib.Path` throughout.

### 3.2 Reading the 53k (match existing conventions)

Mirror `EyePACSDataset.from_directory` (datasets.py:209–248):

- Enumerate images from `testLabels15.csv` `image` column → `image_path = test_dir / f"{name}.jpeg"`;
  skip rows whose file is missing (`if not img_path.exists(): continue`) so a partial download
  does not crash the run.
- `patient_id = name.split("_")[0]`; `eye_side = "left" if "_left" in name else "right"`.
- For the **SSL objective, ignore the `level` column entirely.** Labels are read **only** by
  the linear-probe gate (§8), never by the pretext task.
- Images are loaded with `cv2.imread` (returns **BGR**); the preprocessing pipeline converts
  **BGR→RGB on entry** (project rule: all internal processing is RGB). Do not double-convert.

Implement a dedicated `EyePACSSSLDataset` (a label-free sibling of `EyePACSDataset`) rather
than overloading the supervised class — its `__getitem__` returns **two augmented views**
(§4), not `(tensor, label)`.

### 3.3 Disjointness assertion (INV-SSL-2 enforcement, must be code)

At job start, the SSL entry point MUST:

1. Build the set of SSL image stems from `test/` and the set of Exp-1 stems from `train/`
   (or from `trainLabels.csv`).
2. Assert `ssl_stems.isdisjoint(train_stems)` AND
   `ssl_patient_ids.isdisjoint(train_patient_ids)`.
3. On any overlap, **raise** with the offending IDs listed (do not warn-and-continue).
4. Log corpus sizes (expect 53,576 SSL / ~35,126 Exp-1) and write them into the run manifest
   (§9) so the gate report is auditable.

### 3.4 New config block

Add an `ssl:` top-level block to `configs/default.yaml` (or a dedicated
`configs/ssl_pretrain.yaml` that inherits via the existing `src/utils/config.py` merge). All
knobs live here — see §6 for the full table. Minimal path keys:

```yaml
ssl:
  corpus:
    eyepacs_test_dir:   "test"                # joined onto paths.eyepacs
    test_labels_csv:    "testLabels15.csv"    # probe only; joined onto paths.eyepacs
    image_glob:         "*.jpeg"
    expected_count:     53576
  # ... method / optimizer / schedule / probe blocks (see §6, §8)
```

---

## 4. Preprocessing & augmentation specification (binding 4-channel contract)

### 4.1 Base tensor = deterministic part of the existing pipeline

SSL views are built **on top of the project's 8-stage pipeline**, reusing the deterministic
Stages 0–5 so the SSL feature space matches the downstream pipeline-arm feature space:

```
Stage 0 Canonical flip (left→right)            — deterministic
Stage 1 OD–fovea rotation normalization        — deterministic
Stage 2 FOV crop + isotropic resize            — deterministic, but to 256² here (see §4.4)
Stage 3 FOV mask → 4th channel                 — deterministic
Stage 4 Flat-field correction (σ=0.07·D)       — deterministic
Stage 5 CLAHE                                   — set to deterministic for the SSL BASE tensor
                                                  (disable the train-time stochastic p=0.8;
                                                  SSL view stochasticity comes from §4.3)
```

The base sample is therefore a **4-channel float tensor**: channels `[R, G, B, M]` where `M`
is the binary FOV mask (1.0 inside FOV, 0.0 outside). **Stage 7 dataset-specific normalize**
is applied to the RGB channels (use the EyePACS dataset_mean/std once computed; until then,
ImageNet stats are an acceptable stopgap — record which was used). The mask channel is **not**
normalized (it stays {0,1}).

> Reuse `PreprocessingPipeline` (or a thin SSL preset of `PreprocessingConfig`) to produce the
> Stage 0–5 base tensor. Do **not** reimplement the stages. Caching the deterministic Stage
> 0–4 output (as `CachedEyePACSDataset`/`scripts/precompute_cache.py` already do for Exp 1)
> is strongly recommended for throughput — 53k × many epochs is the bottleneck (§12).

### 4.2 Two-view generation

Each `__getitem__` returns **two independently-augmented views** `(v1, v2)` of the same base
4-channel tensor (the standard SSL positive pair). For DINO, additionally emit the
multi-crop set (2 global + N local crops) — keep the count configurable (§6) and small
(e.g. 2 global @ 224–256², 4–6 local @ 96²) to fit 12 GB.

### 4.3 Augmentation channel rule (CRITICAL — binding)

This is the single most important correctness rule of the brief:

- **GEOMETRIC augmentations apply to ALL 4 channels together** (RGB **and** mask), so the
  mask stays spatially consistent with the image. Includes: random resized crop, horizontal
  flip, rotation, affine/scale/translation.
- **PHOTOMETRIC augmentations apply to the RGB channels ONLY, NEVER the mask channel.**
  Includes: ColorJitter (brightness/contrast/saturation/hue), Gaussian blur, grayscale,
  solarize, Gaussian noise. The mask channel is a geometry indicator, not an image —
  perturbing its intensity is meaningless and would corrupt the signal.

Implementation contract: split the 4-channel tensor into `rgb = x[:3]` and `mask = x[3:4]`;
apply geometric ops to the full stack with a **shared sampled transform** (same random
params for rgb and mask); apply photometric ops to `rgb` only; re-concatenate
`[rgb_aug, mask_geom]`. After photometric ops, **re-clamp/re-binarize the mask is not needed**
(it never saw photometric ops); after geometric ops the mask may interpolate — **threshold it
back to {0,1}** (e.g. `mask = (mask > 0.5).float()`) to keep it binary.

Recommended view recipe (BYOL/MoCo/SimSiam asymmetric-friendly; tune in §6):
RandomResizedCrop(scale 0.2–1.0) → HorizontalFlip(p=0.5) → [RGB-only] ColorJitter(0.4/0.4/0.2/0.1, p=0.8) →
[RGB-only] RandomGrayscale(p=0.2) → [RGB-only] GaussianBlur(p: view1=1.0, view2=0.1) →
[RGB-only] Solarize(p: view2 only) → normalize RGB → threshold mask.

Reuse the existing affine/ColorJitter machinery in `src/data/augmentation_unified.py` where
possible, but the **two-view SSL transform is a new module** (§7) — the Stage-6 supervised
augmentation is single-view and not directly reusable.

### 4.4 Resolution

Pretrain at **256×256** (set Stage 2 `target_size: 256` for the SSL base tensor) to cut
compute and fit larger batches. **Downstream Exp 1 uses 512×512.** CNNs (fully convolutional
trunks + adaptive global pooling) tolerate the resolution change; the loaded weights are
resolution-agnostic except the final pooling, which is adaptive. State this in the run
manifest. (If DINO local crops are used, keep globals at 224–256², locals at 96².)

---

## 5. SSL method specification

### 5.1 Primary recommendation: **BYOL** (4-channel, asymmetric, no negatives)

**Use BYOL as the primary method.** Rationale under our constraints (RTX 3060 12 GB,
`batch_size` ≈ 16–48 at 256²):

- **No negative pairs / no memory queue / no large-batch requirement.** BYOL learns from
  positive pairs only via an online/target asymmetric predictor + EMA target network. This
  is the best fit for a small-batch single-GPU budget — it avoids SimCLR's large-batch
  negative requirement entirely (INV-SSL-6).
- **Robust to batch size**, which matters because 4-channel 256² limits us to modest batches.
- Architecture-agnostic: wraps any CNN trunk (ResNet-50 and EfficientNet-B3 alike) with no
  ViT assumptions.

**Components:** online encoder `f_θ` (backbone, 4-ch stem) → projector MLP (2-layer,
hidden 4096 → output 256, BN+ReLU) → predictor MLP (same shape, online only); target
encoder+projector are the EMA of the online ones (no predictor). Loss = normalized MSE
(2 − 2·cos) between online prediction and target projection, symmetrized over the two views.
EMA momentum `τ` ramps `0.996 → 1.0` on a cosine schedule.

### 5.2 Alternatives (implement behind a `ssl.method` flag)

| Method | When to prefer | Key cost |
|--------|----------------|----------|
| **MoCo-v2** | If BYOL training is unstable / collapses; queue gives stable negatives at small batch. | Maintains a momentum queue (e.g. 4096–16384 keys) — modest memory. |
| **SimSiam** | Simplest (no EMA, no queue); good sanity baseline. | Collapse risk; needs stop-grad + predictor exactly right. |
| **DINO** | If self-distillation + multi-crop yields the best linear-probe number. | Multi-crop raises memory; centering+sharpening temperature tuning. |

All four share the same `EyePACSSSLDataset` + two-view transform; they differ only in the
loss/head/momentum module. Build a common `SSLTrainer` with a pluggable `method` strategy.

### 5.3 Selection criterion (empirical, gate-driven)

Run a **short screening** of each candidate (e.g. 100 epochs, both backbones optional —
screen on ResNet-50 first) and **select the method that maximizes the §8 linear-probe metric
(EyePACS-test held-out quadratic-weighted κ / weighted-F1)** on the probe slice, subject to
stable (non-collapsing) training. Tie-break toward the cheaper/simpler method (BYOL > MoCo-v2 >
SimSiam > DINO by training cost). **Record the screening table in the gate report.** Promote
the winner to a full run (§6 epochs) for **both** backbones.

### 5.4 Hyperparameters (defaults — expose all in `ssl:` YAML)

| Knob | Default | Notes |
|------|---------|-------|
| `method` | `byol` | one of byol / mocov2 / simsiam / dino |
| `image_size` | 256 | Stage-2 target for SSL base tensor |
| `in_channels` | 4 | RGB + FOV mask |
| `batch_size` | 32 | start 32 @ 256²; reduce to 16 if OOM, raise to 48 if headroom (§12) |
| `optimizer` | `lars` (BYOL/DINO) / `sgd` (MoCo/SimSiam) | LARS for large-batch-style BYOL; AdamW acceptable if LARS unavailable |
| `base_lr` | `0.2 × batch_size / 256` (BYOL/LARS) | linear scaling rule; for SGD/MoCo use 0.03 base |
| `weight_decay` | 1e-6 (BYOL) / 1e-4 (MoCo/SimSiam) | per-method conventions |
| `warmup_epochs` | 10 | linear warmup |
| `schedule` | cosine decay to 0 | over `epochs` |
| `epochs` | 300 (full run); 100 (screening) | 53k is small → more epochs help; watch the gate, not a fixed number |
| `ema_momentum` | 0.996 → 1.0 cosine | BYOL/MoCo/DINO target update |
| `projector` | 2-layer MLP, hidden 4096, out 256, BN | |
| `predictor` | 2-layer MLP, hidden 4096, out 256, BN | online only (BYOL/SimSiam) |
| `mixed_precision` | **ResNet-50: on; EfficientNet-B3: OFF** | matches known fp16-overflow rule for EfficientNet (CLAUDE.md) |
| `grad_clip` | 1.0 | gradient explosion guard (known early-training issue) |
| `num_workers` | 4 | matches training config |
| `seed` | 42, `deterministic: true` | project reproducibility rule |

> **mixed_precision is per-backbone**: EfficientNet-B3 must run **fp32** (the same fp16
> overflow that disables AMP in supervised EfficientNet applies here). ResNet-50 may use AMP.

---

## 6. Config block (authoritative knob list)

The implementer adds this under `ssl:` (paths from §3.4 not repeated). Every value above is a
key here; nothing is hardcoded in Python. Example skeleton:

```yaml
ssl:
  method:            byol            # byol | mocov2 | simsiam | dino
  image_size:        256
  in_channels:       4
  epochs:            300
  screening_epochs:  100
  batch_size:        32
  num_workers:       4
  seed:              42
  deterministic:     true
  grad_clip:         1.0

  optimizer:
    name:            lars            # lars | sgd | adamw
    base_lr:         0.45            # = 0.2 * batch_size/256 for bs=576-equiv; recompute per bs
    weight_decay:    1.0e-6
    warmup_epochs:   10
    schedule:        cosine

  byol:
    proj_hidden:     4096
    proj_out:        256
    pred_hidden:     4096
    ema_base:        0.996

  mocov2:  { queue_size: 8192, moco_dim: 128, temperature: 0.2, ema: 0.999 }
  simsiam: { proj_hidden: 2048, proj_out: 2048, pred_hidden: 512 }
  dino:    { out_dim: 65536, n_local_crops: 6, warmup_teacher_temp: 0.04, teacher_temp: 0.07 }

  augment:
    global_crop_scale: [0.2, 1.0]
    local_crop_scale:  [0.05, 0.2]   # dino only
    color_jitter:      [0.4, 0.4, 0.2, 0.1]
    color_jitter_prob: 0.8
    grayscale_prob:    0.2
    blur_prob_view1:   1.0
    blur_prob_view2:   0.1
    solarize_prob_view2: 0.2
    # NOTE: all photometric entries above apply to RGB channels ONLY (§4.3)

  backbones:          [resnet50, efficientnet_b3]   # pretrain each separately

  mixed_precision:
    resnet50:         true
    efficientnet_b3:  false

  checkpoint:
    out_dir:          "outputs/ssl"        # joined onto repo, versioned subdirs (§9)
    save_every:       50
    keep_last:        2

  probe:                                    # see §8
    enabled:          true
    epochs:           50
    batch_size:       64
    lr:               0.1
    label_csv:        "testLabels15.csv"
    holdout_usage:    "Private"             # carve probe test slice by Usage column
    accept_vs_random_kappa_delta: 0.05
    accept_vs_imagenet_kappa_margin: -0.03  # SSL within 0.03 κ of ImageNet (or better)
```

---

## 7. Backbone / stem details

Both backbones are taken **unchanged** from the existing factory so SSL and supervised share
identical trunks:

- **ResNet-50:** `create_resnet50(in_channels=4, pretrained=False, ...)` (random init for
  from-scratch SSL). The 4-channel `conv1` replacement logic already exists
  (`src/models/resnet.py`:38–53). For from-scratch SSL set `pretrained=False` so the stem is
  randomly initialized (no ImageNet copy); the classification `fc` head is irrelevant during
  SSL — **strip it** and attach the SSL projector/predictor to the 2048-d pooled features.
- **EfficientNet-B3:** `create_efficientnet("b3", in_channels=4, pretrained=False, ...)`. The
  4-channel `conv_stem` replacement already exists (`src/models/efficientnet.py`:50–64).
  Strip `classifier`; attach SSL heads to the `feat_dim`-d pooled features.

**Feature extraction for SSL:** use the backbone trunk up to and including global average
pooling (drop the classification head). For ResNet-50 that is the 2048-d vector; for
EfficientNet-B3 it is `model.classifier.in_features`-d. Provide a small
`build_ssl_encoder(backbone_name, in_channels=4)` helper that returns `(trunk, feature_dim)`.

**From-scratch means random init** (INV-SSL-6 / locked decision): `pretrained=False`. Do not
silently start from ImageNet — that is the §11 fallback only, and must be explicitly flagged
in the manifest if ever used.

---

## 8. Linear-probe validation gate (binding acceptance criterion)

**No SSL checkpoint enters Experiment 1 until it passes this gate.**

### 8.1 Probe dataset slice (uses the now-available test labels, leak-free)

The probe uses `testLabels15.csv` — the labels that are *forbidden* for the pretext task are
*permitted* here, because the probe is a **separate evaluation**, not part of the SSL
objective. To avoid the probe training on what it tests, **carve the slice by the `Usage`
column**:

- **Probe-train** = rows with `Usage == "Public"`.
- **Probe-test** = rows with `Usage == "Private"`.

(If the `Usage` split is too imbalanced for the 5 DR grades, fall back to a fixed
seed-42 patient-level stratified 80/20 split of the 53k — document which was used.) The probe
never touches the Exp-1 `train/` corpus, so INV-SSL-2 holds.

### 8.2 Protocol (frozen backbone)

1. Load the SSL-pretrained backbone; **freeze all backbone weights** (`requires_grad=False`).
2. Attach a single fresh `Linear(feature_dim, 5)` head (no hidden layer, no dropout) on the
   frozen pooled features.
3. Train **only the linear head** on probe-train (Configs use the **same 4-channel pipeline
   input**, 256² to match pretraining; or 512² — keep consistent and record it). Use the
   project's class-weighted/focal setup or plain cross-entropy — record which.
4. Evaluate on probe-test with the project's primary metrics
   (`src/evaluation/metrics.py`): weighted-F1, ROC-AUC, **quadratic-weighted Cohen κ**,
   accuracy.
5. (Optional, cheap) also report a **k-NN** evaluation on the frozen features (e.g. k=20,
   cosine) as a second opinion.

### 8.3 Baselines to compare against (same probe protocol)

- **Random-init** backbone (same architecture, `pretrained=False`, untrained) — the floor.
- **ImageNet-init** backbone (`pretrained=True`) — the incumbent the pipeline arm must rival.

### 8.4 Acceptance criterion (must hold for BOTH backbones)

A checkpoint **passes** iff, on probe-test:

1. **Beats random init** by a clear margin: `κ(SSL) − κ(random) ≥ 0.05`
   (`probe.accept_vs_random_kappa_delta`), and similarly improves weighted-F1.
2. **Competitive with ImageNet:** `κ(SSL) ≥ κ(ImageNet) − 0.03`
   (`probe.accept_vs_imagenet_kappa_margin`) — i.e. within 0.03 κ of, or better than,
   ImageNet. Being *better* than ImageNet is welcome but not required (the contribution SC-H
   is "in-domain init is at least competitive", not "SSL wins").
3. Training did **not collapse** (loss/feature-variance sane; representation not constant).

If either backbone fails, **do not promote** — go to §11 (fallback / diagnosis). The gate
report (JSON) records all three init conditions × both backbones × all metrics + the §5.3
method-screening table, so the decision is auditable.

---

## 9. Training loop, checkpointing & artifacts

### 9.1 Loop

Standard SSL loop using the common `SSLTrainer`:

- per step: load batch → build two views (§4) → forward online+target (or method-specific) →
  loss → backward (AMP per §5.4) → grad-clip → optimizer step → EMA target update (if
  applicable) → LR/momentum schedulers.
- Reuse `src/utils/seed.py` for determinism; reuse `src/utils/config.py` for YAML loading.
- Log: loss, LR, EMA momentum, feature std (collapse monitor), throughput. Write a periodic
  **representation-collapse check** (std of L2-normalized features should stay well above 0).

### 9.2 Checkpoint artifact format (binding)

Save **versioned** checkpoints per backbone under `ssl.checkpoint.out_dir`:

```
outputs/ssl/
  v1.0/
    ssl_byol_resnet50_4ch_256_ep300.pt
    ssl_byol_efficientnet_b3_4ch_256_ep300.pt
    manifest.json
    gate_report.json
```

Naming: `ssl_<method>_<backbone>_<in_channels>ch_<res>_ep<epochs>.pt`. Each `.pt` MUST store:

- `backbone_state_dict` — the **trunk weights only**, keyed so they load directly into the
  factory model's trunk (i.e. matching `create_resnet50(in_channels=4)` /
  `create_efficientnet("b3", in_channels=4)` state-dict keys, **excluding** the classifier
  head). The 4-channel stem weights are included.
- `meta`: `{method, backbone, in_channels:4, image_size:256, epochs, seed,
  normalize_stats_used, ssl_corpus:"EyePACS/test", corpus_count:53576, git_commit,
  config_hash, gate_passed:bool}`.

Reuse `src/training/checkpoint.py::CheckpointManager` patterns (save/keep-last). Keep weights
**4-channel-stem compatible** with Configs B/D.

### 9.3 Run manifest

`manifest.json` records: resolved config, corpus sizes + disjointness-assertion result
(§3.3), normalization stats used, per-backbone training curves summary, and pointers to the
gate report. This is the audit trail for SC-H.

---

## 10. Integration with Experiment 1 (Configs B & D)

The pipeline arm must initialize from the SSL checkpoint **instead of** ImageNet, with the
baseline arm untouched. Minimal, additive integration:

1. **Loader function** (new): `load_ssl_backbone(model, ckpt_path)` that loads
   `backbone_state_dict` into a factory model built with `in_channels=4`, asserts the stem is
   4-channel, and returns the model with a **fresh** 5-class head (the SSL `.pt` carries no
   classifier). Strict-load the trunk; report any missing/unexpected keys.
2. **Config wiring:** extend the Exp-1 config so Configs **B** and **D** carry an
   `init: {source: ssl, ckpt: "outputs/ssl/v1.0/ssl_byol_<backbone>_4ch_256_ep300.pt"}`
   while Configs **A** and **C** carry `init: {source: imagenet}`. The model factory /
   `exp1_factorial.py` selects: `imagenet` → `pretrained=True`; `ssl` → build
   `pretrained=False` then `load_ssl_backbone(...)`.
3. **Gate enforcement:** Exp-1 must refuse to start a B/D run whose checkpoint
   `meta.gate_passed != true` (fail fast — no ungated init enters the experiment).
4. **No change to A/C** and no change to the Exp-1 dataset/CV. This keeps the H-1 contrast
   exactly *(preprocessing × architecture)* with initialization aligned to CFC-2.8.

Downstream fine-tuning then proceeds at **512²** with the existing trainer; the SSL weights
are resolution-agnostic except adaptive pooling (§4.4).

---

## 11. Risks & fallbacks

| Risk | Mitigation / fallback |
|------|-----------------------|
| **53k is small for from-scratch SSL** → init underperforms ImageNet on the probe. | **Documented fallback (NOT default): ImageNet→continual-SSL** — initialize the SSL encoder from ImageNet (`pretrained=True`) and continue SSL on the 53k. Only invoke if the §8 gate fails for from-scratch; must be explicitly flagged in the manifest (`init_source: imagenet_continual`). Note this slightly softens the "fundus-only" contrast — record the caveat for the thesis. |
| **Method collapse** (SimSiam/BYOL constant features). | Feature-std monitor (§9.1); switch to MoCo-v2 (queue stabilizes); verify stop-grad/predictor wiring; lower LR. |
| **OOM at 256² / batch too small for stable SSL.** | Reduce `batch_size` to 16 and rely on BYOL's batch-robustness; enable grad accumulation for an effective larger batch; ResNet-50 AMP on. **Do not** switch to SimCLR-style negatives (INV-SSL-6). |
| **EfficientNet fp16 overflow.** | EfficientNet SSL runs **fp32** (`mixed_precision.efficientnet_b3: false`). |
| **Probe `Usage` split too imbalanced.** | Fall back to seed-42 patient-level stratified 80/20 of the 53k (§8.1); document. |
| **Throughput bottleneck (53k × hundreds of epochs).** | Precompute & cache the deterministic Stage 0–4 base tensor (reuse `scripts/precompute_cache.py` pattern); SSL view augmentation runs per-epoch on cached 4-ch tensors. |
| **Accidental leakage** (someone points SSL at `train/`). | Hard disjointness assertion (§3.3) raises before training. |

---

## 12. Compute budget (RTX 3060 12 GB)

- Pretrain at **256²**, 4-channel, `batch_size≈32` (BYOL). Expect single-GPU runs of order
  days for 300 epochs × 2 backbones × method screening — **screen at 100 epochs first**
  (§5.3) to pick the method before committing full runs.
- ResNet-50: AMP on. EfficientNet-B3: fp32 (slower, smaller feasible batch — drop to 16–24 if
  needed).
- Cache Stage 0–4 to keep the DataLoader from starving the GPU.

---

## 13. File / module layout (follow existing structure)

New code lives under `experiments/`, mirroring the existing `src/` taxonomy. **No governance
copies here** (single source of truth is `thesis/governance/`).

```
experiments/
  configs/
    ssl_pretrain.yaml              # ssl: block (or merge into default.yaml) — §6
  src/
    ssl/                           # NEW package
      __init__.py
      dataset.py                   # EyePACSSSLDataset (label-free, two-view) — §3.2
      transforms.py                # TwoViewTransform + 4ch geometric/photometric split — §4.3
      methods.py                   # BYOL (primary) + MoCoV2/SimSiam/DINO strategies — §5
      heads.py                     # projector/predictor MLPs — §5.1
      encoder.py                   # build_ssl_encoder(backbone, in_channels) -> (trunk, dim) — §7
      trainer.py                   # SSLTrainer loop, EMA, schedulers, collapse monitor — §9
      probe.py                     # linear-probe + kNN gate, baselines, accept logic — §8
      checkpoint.py                # versioned save/load + manifest (or reuse training/checkpoint) — §9.2
      loader.py                    # load_ssl_backbone(model, ckpt) for Exp-1 — §10
    data/datasets.py               # (unchanged; SSL uses src/ssl/dataset.py)
    models/{resnet,efficientnet}.py# (unchanged; reused via factory with in_channels=4)
  scripts/
    run_ssl_pretrain.py            # CLI: build corpus → assert disjointness → train → save
    run_ssl_probe.py               # CLI: run §8 gate, emit gate_report.json
    precompute_ssl_cache.py        # optional Stage 0–4 cache for the 53k (reuse existing pattern)
  outputs/ssl/v1.0/...             # checkpoints + manifest + gate_report — §9.2
  docs/
    fundus_ssl_pretraining_brief.md  # this file
```

**Code rules (project-binding, restate):** type hints on every signature; Args/Returns
docstrings on every public function; **no hardcoded paths — all from YAML** (`pathlib.Path`);
all internal image processing in **RGB** (`cv2.imread` is BGR → convert on entry); English
only; every module independently testable; seed=42, deterministic.

---

## 14. Phased implementation plan

**Phase 0 — Scaffolding & data (no training).**
Add `ssl:` config; implement `EyePACSSSLDataset` reading `test/*.jpeg`; implement the §3.3
disjointness assertion and prove 53,576 / ~35,126 with zero overlap; wire the deterministic
Stage 0–5 base tensor at 256². *Exit:* a DataLoader yields 4-channel base tensors; disjointness
assertion passes.

**Phase 1 — Two-view 4-channel transform.**
Implement `TwoViewTransform` with the §4.3 channel rule (geometric→all 4, photometric→RGB
only, mask re-thresholded). Unit-test that the mask channel is identical under photometric
ops and co-transformed under geometric ops, and stays binary. *Exit:* visual + assertion
tests pass.

**Phase 2 — BYOL on ResNet-50 (primary).**
Implement `build_ssl_encoder`, projector/predictor, BYOL strategy, `SSLTrainer` (EMA,
schedules, collapse monitor, AMP). Short smoke-train (few epochs) to confirm loss decreases
and features don't collapse. *Exit:* stable loss curve, feature-std healthy, checkpoint saved
in the §9.2 format.

**Phase 3 — Method screening + gate harness.**
Implement MoCo-v2/SimSiam/DINO strategies behind `ssl.method`; implement the §8 linear-probe
+ kNN gate with random/ImageNet baselines and the `Usage`-based slice. Run the 100-epoch
screening on ResNet-50; pick the winner by probe κ (§5.3). *Exit:* `gate_report.json` with the
screening table; a method selected.

**Phase 4 — Full pretraining, both backbones.**
Full-epoch runs (winning method) for ResNet-50 (AMP) and EfficientNet-B3 (fp32). Cache Stage
0–4 first (Phase-0 script) for throughput. *Exit:* two versioned checkpoints + manifest.

**Phase 5 — Gate decision.**
Run the §8 gate on both full checkpoints vs random and ImageNet. If both pass → mark
`gate_passed:true`. If not → invoke §11 fallback (ImageNet→continual-SSL) and re-gate; if
still failing, escalate to maintainer (do not ship an ungated init). *Exit:* gate verdict
recorded.

**Phase 6 — Exp-1 integration.**
Implement `load_ssl_backbone` + the `init:` config wiring so Configs B/D load the gated SSL
checkpoint and A/C stay ImageNet; add the fail-fast `gate_passed` check. Do **not** alter the
Exp-1 dataset or CV. *Exit:* a dry-run B/D build loads SSL weights (strict trunk load, fresh
head); A/C unchanged.

**Phase 7 — Handoff to maintainer.**
Maintainer amends `thesis/governance/` (SC-H wording under CFC-2.8) and runs Exp 1. (Out of
the implementer's scope — flag it.)

---

## 15. Acceptance summary (what "done" means)

1. `EyePACSSSLDataset` loads the 53,576-image `test/` corpus label-free; disjointness
   assertion vs the ~35,126 `train/` corpus passes (§2, §3.3).
2. Two-view transform honors the 4-channel rule: photometric on RGB only, geometric on all 4,
   mask stays binary (§4.3) — proven by unit tests.
3. BYOL (or the gate-selected method) pretrains **both** ResNet-50 and EfficientNet-B3 at
   256², 4-channel, producing versioned `.pt` checkpoints in the §9.2 format with a manifest.
4. The §8 linear-probe gate shows, for **both** backbones, SSL **beats random** and is
   **within 0.03 κ of (or better than) ImageNet** on the EyePACS-test probe slice — recorded
   in `gate_report.json`.
5. `load_ssl_backbone` lets Configs **B/D** initialize from the gated checkpoint while
   **A/C** stay ImageNet, with a fail-fast `gate_passed` guard (§10).
6. No hardcoded paths; all knobs in YAML; type hints + docstrings; RGB-internal; seed 42 /
   deterministic (§13).
