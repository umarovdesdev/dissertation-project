# EfficientNet-B3 SSL retrain (v1.1) — HANDOFF for the RTX 3060 / WSL machine

**Goal.** Run EfficientNet-B3 BYOL pretraining with the **same collapse fix** applied to ResNet-50,
**in parallel** with the ResNet-50 v1.1 run on the other PC. Both write to version **v1.1**; the
per-backbone filenames and resume-state files don't clash.

> **Why a retrain at all?** The v1.0 BYOL runs collapsed (probe gate: κ_ssl≈0 vs κ_imagenet≈0.30).
> Root cause = two small-batch bugs: (1) `SSLTrainer` uses `base_lr` **without batch-size scaling**,
> so v1.0 ran LR 0.45 at batch 16 (~36× too high); (2) batch 16 is too small for BYOL's `BatchNorm1d`
> projector. Fix = **bigger batch + LR scaled to it** (`base_lr = 0.2 × batch / 256`). Full context: `TASK.md`.

---

## 0. What already exists on this machine (no setup needed)
- conda env **`dr-classifier`** (torch 2.5.1+cu121 — fine for EfficientNet on the 3060; `timm` installed).
- WSL2 Ubuntu; the drive mounts at **`/mnt/e`**.
- Stage 0–4 **cache at `/home/yesmu/ssl_cache_256`** (WSL-native ext4).
- Dataset at `/mnt/e/datasets/EyePACS` (test split + `testLabels15.csv` + `trainLabels.csv`).
- Configs (they travel on the drive): `configs/_wsl_local.yaml` (this machine's paths) +
  **`configs/ssl_retrain_eff_v1_1.yaml`** (the fix; batch 32, base_lr 0.025, out_dir `/home/yesmu/ssl_out`).

## 1. Pre-flight (30 seconds — confirm the machine is ready)
```bash
source ~/miniconda3/etc/profile.d/conda.sh; conda activate dr-classifier
cd /mnt/e/dissertation-project/experiments
# GPU visible?
python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
# cache present? (expect a cache_meta.csv + ~53,576 PNGs)
ls /home/yesmu/ssl_cache_256/cache_meta.csv && wc -l /home/yesmu/ssl_cache_256/cache_meta.csv
```
If the cache is missing, rebuild it (one-time) or extract the tarball that travels on the drive:
```bash
mkdir -p /home/yesmu && tar xf /mnt/e/dissertation-project/experiments/outputs/ssl/ssl_cache_256.tar -C /home/yesmu
#   -> /home/yesmu/ssl_cache_256   (matches cache_dir in _wsl_local.yaml)
```

## 2. Launch (background; unbuffered; NO `| tail` — it masks crash exit codes)
```bash
source ~/miniconda3/etc/profile.d/conda.sh; conda activate dr-classifier
cd /mnt/e/dissertation-project/experiments
nohup python -u scripts/run_ssl_pretrain.py \
  --config configs/default.yaml --config configs/ssl_pretrain.yaml \
  --config configs/_wsl_local.yaml --config configs/ssl_retrain_eff_v1_1.yaml \
  --backbone efficientnet_b3 --device cuda \
  >> /home/yesmu/ssl_eff_b3.log 2>&1 &
```
> **Launch caveat on this box (from TASK.md §4):** a one-shot `wsl.exe bash -lc "…"` that returns can
> kill the detached child. Launch from a WSL shell you keep open, or via the harness background runner.
> The python survives harness "killed" notifications via init-reparenting — judge liveness by the real
> PID (`ps -eo pid,etime,cmd | grep '[r]un_ssl_pretrain'`), not the task status.

## 3. Resume after any kill / reboot (loses ≤1 epoch)
```bash
# same command with --resume appended:
python -u scripts/run_ssl_pretrain.py \
  --config configs/default.yaml --config configs/ssl_pretrain.yaml \
  --config configs/_wsl_local.yaml --config configs/ssl_retrain_eff_v1_1.yaml \
  --backbone efficientnet_b3 --device cuda --resume
```
Rolling state: `/home/yesmu/ssl_out/v1.1/train_state_efficientnet_b3.pt` (atomic, per-epoch).

## 4. What HEALTHY looks like (watch the log)
- `AMP=False | feature_dim=1536` at start (fp32 — correct for EfficientNet).
- **loss** starts ~3.9 and **decreases**; **feat_std** starts ~0.016 and **stays/ rises** (≳0.01).
- **COLLAPSE signature (bad):** loss → ~0 and feat_std → ~0.002. If you see that, stop and ping —
  don't run 300 epochs into a wall. (The v1.0 collapse showed loss≈0.08 from the very first epoch.)
- Checkpoints land at ep50/100/… in `/home/yesmu/ssl_out/v1.1/` (`save_every=50`).

## 5. Gate the fix EARLY (don't wait for ep300)
When ep50 (or ep100) lands, run the probe on that checkpoint (minutes; features cache to disk):
```bash
python -u scripts/run_ssl_probe.py \
  --config configs/default.yaml --config configs/ssl_pretrain.yaml \
  --config configs/_wsl_local.yaml --config configs/ssl_retrain_eff_v1_1.yaml \
  --backbone efficientnet_b3 --device cuda \
  --ckpt /home/yesmu/ssl_out/v1.1/ssl_byol_efficientnet_b3_4ch_256_ep100.pt
```
PASS iff `κ(ssl) − κ(random) ≥ 0.05` AND `κ(ssl) ≥ κ(imagenet) − 0.03`. A rising κ toward ImageNet by
ep50/100 means the fix worked; continue to ep300. If ep50 still shows κ≈0, switch to the fallback
(`--pretrained-init`, continual-SSL from ImageNet — starts at κ≈0.30, near-impossible to fail).

## 6. When done — MOVE THE DELIVERABLE TO THE DRIVE (durability/travel)
`/home/yesmu/ssl_out` is machine-local and does NOT travel. Copy the final checkpoint + manifest to E:
```bash
cp /home/yesmu/ssl_out/v1.1/ssl_byol_efficientnet_b3_4ch_256_ep300.pt \
   /home/yesmu/ssl_out/v1.1/manifest.json \
   /mnt/e/dissertation-project/experiments/outputs/ssl/v1.1/
```

## 7. Notes
- **fp32 is slow on the 3060** — expect this run to be long (likely multiple days for 300 ep). It's
  resumable, so reboots are fine. Gating ep50/100 (step 5) tells you if it's worth continuing.
- EfficientNet-B3 SSL is **gated the same way** as ResNet: it must pass its probe gate before its
  checkpoint unblocks Exp-1 Config D. Both backbones must pass for contribution SC-H.
- If you want a bigger batch (faster, better BN stats) and have the VRAM headroom, edit
  `ssl_retrain_eff_v1_1.yaml` per the table at its top and rescale `base_lr = 0.2 × batch / 256`.
