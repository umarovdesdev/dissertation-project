# TASK.md — Fundus-SSL pretraining: real GPU run + linear-probe gate

**Owner:** Yesmukhamedov N.S. (IITU)
**Driver this session:** Claude Code (Opus) — pre-flight, debugging, orchestration
**Updated:** 2026-06-27

> Prior content of this file (Config-D Kaggle/Colab demo launch, 2026-06-02) was a
> different, older effort. It was superseded here and remains recoverable from git
> history. Ask if you want it restored to a separate file.

---

## ⓪ TL;DR — what we are doing and the one thing in flight

- **Goal:** produce an in-domain **fundus self-supervised (SSL) initialization** for the
  **pipeline arm** of Experiment 1 (Configs **B** and **D**), then validate it with a
  **linear-probe acceptance gate**. Baseline arm (A/C) stays **ImageNet**. This realizes
  governance **CFC-2.8** (baseline⟹ImageNet, pipeline⟹SSL) and supporting contribution
  **SC-H**. RETFound was dropped in v6.0.0 in favour of CNN-native SSL.
- **Method:** **BYOL** (primary), from-scratch (random init), CNN-backbone-matched —
  pretrain **ResNet-50** and **EfficientNet-B3** separately. 4-channel input (RGB + FOV
  mask). Pretrain at 256², downstream at 512².
- **Corpus:** EyePACS original **"test" split = 53,576 images** (`EyePACS/test/*.jpeg`),
  label-free for SSL. **Disjoint** from Exp-1's 35,126 `train/` CV set (verified live:
  53,576 / 26,788 patients vs 35,126 / 17,563 patients) → **no pretraining leakage**
  (governance invariant **SB-2.4 / INV-SSL-1/2**).
- **▶ RESUMED 2026-06-27.** Cache re-launched (running) + training **`--resume` built &
  tested** (the prerequisite below). Decision made: **full run on THIS machine**.
- **Resume point:** the **Stage 0–4 cache** re-launch is **running** (skipped 51,205 already
  cached, processing the last 2,371) at `/home/yesmu/ssl_cache_256` (WSL-native ext4) →
  target 53,576. THEN proceed to training (§3).
- **Decision RESOLVED (candidate, 2026-06-27):** **full SSL run on this machine** (not cloud,
  not screening-only). This makes the training `--resume` feature a hard prerequisite —
  now **DONE** (see §4, last bullet). Free desktop apps before launch for batch 32.

---

## 1. Why a cache is mandatory (throughput)

Measured on this machine (RTX 3060, WSL2): the SSL dataset runs the full **Stage 0–5**
preprocessing live per image at **~0.39 img/s** single-thread. Full run ETA:

| Mode | per epoch | 300 ep × 2 backbones |
|------|-----------|----------------------|
| Live preproc, `num_workers=0` | ~38 h | **~2.6 years** ❌ |
| + spawn-fix, workers | ~5 h | ~120 days ❌ |
| **+ Stage 0–4 cache wired** | minutes | **~2–6 days** ✅ |

Stages 0–4 are deterministic (no train-time randomness until Stage 5 CLAHE + Stage 6
aug), so they are cached once at 256² as 4-channel PNG (RGB Stage-4 + binary FOV-mask
alpha) + `cache_meta.csv`. Mirrors the existing train-side `CachedEyePACSDataset`.

---

## 2. Done (this session)

- **Pre-flight verified:** WSL2 Ubuntu + conda `dr-classifier` + torch 2.5.1+cu121, CUDA
  visible (RTX 3060). Windows-side torch is **CPU-only** → GPU work must run in WSL. Data
  reachable in WSL at `/mnt/e/datasets/EyePACS`. Disjointness invariant confirmed live.
- **GPU compute validated:** BYOL ResNet-50, batch 16 @ 256², AMP — runs and **fits** in
  ~3.4 GB free VRAM (no OOM). Two-view 4-channel contract intact.
- **Two real blockers found & fixed** (committed? **NO — still in working tree**):
  1. **CUDA-fork crash** (`Cannot re-initialize CUDA in forked subprocess`): added a
     guarded `mp.set_start_method("spawn", force=True)` in `run_ssl_pretrain.py` and
     `run_ssl_probe.py`.
  2. **Cache not wired into SSL dataset:** added `CachedEyePACSSSLDataset` + `index_ssl_cache`
     in `src/ssl/dataset.py`, selected via `ssl.cache_dir` in `from_config`. Live path
     unchanged when `cache_dir` is null. Measured speedup **~20×** (21.6 vs 1.1 img/s
     single-thread for the base-tensor read). Added `ssl.cache_dir: null` to
     `configs/default.yaml`. Tests: **37 passed**.
- **Local WSL overlay** `experiments/configs/_wsl_local.yaml` created (**do NOT commit** —
  machine-specific): `paths.eyepacs=/mnt/e/...`, `ssl.batch_size=16`, `ssl.num_workers=4`,
  `ssl.cache_dir=/home/yesmu/ssl_cache_256`.

## 3. Remaining (in order)

1. **Finish the Stage 0–4 cache** for all 53,576 images → `/home/yesmu/ssl_cache_256`
   (native ext4). Verify `cache_meta.csv` has 53,576 data rows + matching PNG count.
2. **Run SSL pretraining** for both backbones (BYOL, from-scratch), GPU, in background:
   - **CONFIRMED order (2026-06-27):** **ResNet-50 first → run the gate on ResNet-50 only
     (`run_ssl_probe.py --backbone resnet50`) → only if it passes, train EfficientNet-B3.**
     This is a checkpoint before spending days on the second backbone.
   - Checkpoints versioned under `experiments/outputs/ssl/v1.0/` (`save_every` epochs).
3. **Linear-probe acceptance gate** (`scripts/run_ssl_probe.py`): probes random / ImageNet
   / SSL on the EyePACS-test `Usage` slice. Accept iff, **for both backbones**,
   κ(SSL) − κ(random) ≥ 0.05 **and** κ(SSL) ≥ κ(ImageNet) − 0.03. On pass it flips
   `meta.gate_passed=True` → **unblocks Exp-1 Configs B/D** (which currently fail-fast).
4. **Commit** the spawn-fix + cache-wiring code (NOT `_wsl_local.yaml`).
5. **Governance:** dataset-specific normalize stats are currently null → SSL falls back to
   ImageNet RGB stats (recorded in the manifest). Optional: run `compute_dataset_stats.py`
   for a cleaner run. Fallback documented if the gate fails: ImageNet→continual-SSL
   (`--pretrained-init`), NOT the default.

---

## 4. Known issues / gotchas on THIS machine (read before re-running)

- **WSL2 is fragile here.** Host RAM = **16 GB**, `.wslconfig` caps WSL at **memory=12GB,
  swap=4GB**. Repeated **`Wsl/Service/E_UNEXPECTED` catastrophic VM crashes** occurred:
  - Too many **spawn** workers (12–16) blow past 12 GB → VM dies. **Keep workers ≤ 4–6.**
  - **Mass writes to the 9p `/mnt/e` mount** (tens of thousands of PNGs) destabilize the
    VM → **write the cache to WSL-native ext4** (`/home/...`), read source JPEGs from
    `/mnt/e` (reads are fine). 941 GB free on native `/`.
  - Recover a wedged VM with **`wsl.exe --shutdown`** then re-launch.
- **Launch long jobs via the harness background runner, NOT `nohup ... &`** through a
  one-shot `wsl.exe bash -lc`: when that command returns, WSL tears down the session and
  kills the detached child. The background runner keeps `wsl.exe` alive across turns.
- **Never pipe the training/precompute command through `| tail`** when backgrounding — the
  pipeline's exit code becomes `tail`'s (0), masking real crashes. Redirect or let the
  runner capture stdout; use `python -u`.
- **VRAM contention:** ~8.6 GB of the 12 GB is held by **desktop apps** (Chrome/Edge/
  VS Code/Steam/**cs2.exe**), leaving ~3.4 GB. Batch 16 fits; **freeing apps allows
  batch 32** and a faster run.
- **Multi-line `wsl.exe bash -lc "..."` commands get mangled by CRLF** — prefer simple,
  single-line WSL commands.
- **The harness background runner can be KILLED mid-job** (observed: cache build stopped
  at ~31% with WSL still healthy — not a WSL crash, the runner itself was stopped).
  Mitigations: `precompute_ssl_cache.py` is now **resumable** (skips already-cached images
  by meta-row + PNG presence; opens meta in append mode) → just re-launch to continue.
- **✅ TRAINING RESUME — DONE (2026-06-27).** `run_ssl_pretrain.py --resume` now restores
  the full training state from a rolling `train_state_<backbone>.pt` (per backbone) in the
  version dir: SSL method (online trunk + projector + predictor + **EMA target**) +
  optimizer + AMP scaler + epoch + `global_step` (so the LR/momentum **schedule continues
  the same curve**) + RNG. Written **atomically** (temp + `os.replace`) every epoch
  (`ssl.checkpoint.resume_every`, default 1) so a kill mid-write can't corrupt it; cleared
  on successful completion. Trunk-only deliverable checkpoint format is **unchanged**.
  New: `SSLTrainer.state_dict()/load_state_dict()` (+ mismatch guard), `seed.capture/
  restore_rng_state`, `checkpoint.save/load/clear_train_state`. Tests: **15 passed**
  (incl. round-trip weight equality + `start_epoch` schedule continuity).
  **After a kill, just re-launch the SAME §5 training command with `--resume` appended.**

---

## 5. Commands (WSL, from `/mnt/e/dissertation-project/experiments`)

Prefix every WSL python call with:
`source ~/miniconda3/etc/profile.d/conda.sh; conda activate dr-classifier`

```bash
# Build the Stage 0–4 cache (one-time; native ext4; ≤4 workers; unbuffered; no pipe)
python -u scripts/precompute_ssl_cache.py \
  --config configs/default.yaml --config configs/_wsl_local.yaml \
  --output-dir /home/yesmu/ssl_cache_256 --num-workers 4

# SSL pretraining (per backbone) — cache picked up via ssl.cache_dir in _wsl_local.yaml
python -u scripts/run_ssl_pretrain.py \
  --config configs/default.yaml --config configs/ssl_pretrain.yaml --config configs/_wsl_local.yaml \
  --backbone resnet50            # then --backbone efficientnet_b3
# After a mid-run kill, re-launch the SAME command with --resume appended:
#   ... --backbone resnet50 --resume   (continues from the last epoch; no-op if none)

# Linear-probe acceptance gate (flips gate_passed on accept)
python -u scripts/run_ssl_probe.py \
  --config configs/default.yaml --config configs/ssl_pretrain.yaml --config configs/_wsl_local.yaml
```

Config keys live in `configs/default.yaml` (`ssl:` block, authoritative) + overlays
`configs/ssl_pretrain.yaml` (epochs/method) + `configs/_wsl_local.yaml` (machine paths;
uncommitted).

---

## 6. Pointers

- Decision & history: `PROJECT_MEMORY/config-d-pretraining.md`; throughput precedent:
  `PROJECT_MEMORY/v5-cache-throughput.md`.
- Build-spec: `experiments/docs/fundus_ssl_pretraining_brief.md`.
- Governance: `thesis/governance/INVARIANTS.md` (SB-2.4), `CONTRIBUTIONS.md` (SC-H),
  `HYPOTHESIS.md` — all at v6.2.0.
- Code: `experiments/src/ssl/` (+ `scripts/run_ssl_pretrain.py`, `run_ssl_probe.py`,
  `precompute_ssl_cache.py`); Exp-1 init routing in `src/experiments/exp1_factorial.py`.

End of TASK.md.
