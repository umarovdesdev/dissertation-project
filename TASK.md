# TASK.md — Fundus-SSL pretraining: real GPU run + linear-probe gate

**Owner:** Yesmukhamedov N.S. (IITU)
**Driver this session:** Claude Code (Opus) — pre-flight, debugging, orchestration
**Updated:** 2026-07-06

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
- **✅ ResNet-50 SSL training COMPLETE — epoch 300/300 (2026-07-07).** Final trunk checkpoint
  `outputs/ssl/v1.0/ssl_byol_resnet50_4ch_256_ep300.pt` + `manifest.json` written;
  `train_state_resnet50.pt` cleared on clean completion. Reached 300 across several
  `--resume` restarts (last: died mid-ep280 → resumed ep280 → ran to 300).
- **▶ NEXT (run on the faster PC): the linear-probe gate** `run_ssl_probe.py --backbone resnet50`.
  The probe was **rewritten this session** to (a) read the 256² Stage 0–4 **cache** (was live
  preproc 3× over 53,576 imgs → hours; now minutes) and (b) checkpoint extracted features to a
  **resumable on-disk cache** so it can be stopped/resumed. See §3 step 3 + §6.
- **⚠ WATCH — likely BYOL collapse:** by epoch 278 `feat_std` fell to **~0.001–0.003** (was
  ~0.0065 at ep 25), loss near-zero (~0.0005–0.18). Stable/not crashing, but this is the
  collapse signature. The §3.3 linear-probe gate is the real test of whether the features are
  usable; run it before spending days on EfficientNet-B3.
- **Stage 0–4 cache COMPLETE & VERIFIED (2026-06-27):** 53,576 PNGs == 53,576
  `cache_meta.csv` data rows (1:1, no dups, 0 errors) at `/home/yesmu/ssl_cache_256`
  (WSL-native ext4). The resumed run processed the final 2,371 (incl. 223 orphan PNGs)
  cleanly. **Ready for training (§3 step 2).**
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
- **Two real blockers found & fixed** (✅ **COMMITTED** in `c1e3320` "SSL pretraining: add
  training --resume + cache wiring + spawn-fix" — supersedes the old "NOT committed" note):
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

1. ✅ **DONE (2026-06-27).** Stage 0–4 cache built for all 53,576 images →
   `/home/yesmu/ssl_cache_256`: verified 53,576 data rows == 53,576 PNGs, 0 errors, no dups.
2. **Run SSL pretraining** for both backbones (BYOL, from-scratch), GPU, in background:
   - **CONFIRMED order (2026-06-27):** **ResNet-50 first → run the gate on ResNet-50 only
     (`run_ssl_probe.py --backbone resnet50`) → only if it passes, train EfficientNet-B3.**
     This is a checkpoint before spending days on the second backbone.
   - Checkpoints versioned under `experiments/outputs/ssl/v1.0/` (`save_every` epochs).
   - **▶ ResNet-50 IN PROGRESS — resumed epoch 279/300 as of 2026-07-05** (300 epochs, AMP,
     cuda, **batch_size=16** per `_wsl_local.yaml`; the early 2026-06-27 "batch 32" note was a
     first attempt — the durable run is batch 16). Disjointness re-verified live each launch
     (SSL 53,576/26,788pt vs train 35,126/17,563pt). ~0.24 h/epoch → ~22 epochs / ~5–6 h left.
     - **Progress log:** reached ep 278 by ~2026-07-05 08:51; the python trainer then died
       (verified: 0 live trainers, 0 GPU compute apps — a genuine death, not a harness "kill").
       Re-launched with `--resume` at 2026-07-05 12:57 → cleanly restored at epoch 278/300
       (global_step=930744) and continued. Deliverable trunk checkpoints saved so far:
       ep50 / ep100 / ep200 / ep250 under `experiments/outputs/ssl/v1.0/`.
     - **⚠ feat_std collapse watch:** dropped to ~0.001–0.003 by ep 278 (was ~0.0065 at ep 25),
       loss near-zero. Stable but a BYOL-collapse signature — the §3.3 probe gate is the real
       check. See TL;DR WATCH bullet.
     - **Log:** `/home/yesmu/ssl_resnet50.log` (WSL-native; grows via `>>` append).
     - **Resume state:** `experiments/outputs/ssl/v1.0/train_state_resnet50.pt` (413 MB,
       rolling, atomic per-epoch). **NOTE the path:** state is in the **version dir**, NOT
       in `/home/yesmu/` (that dir holds only the log + the Stage-0–4 cache).
     - **Recovery:** if the python process *genuinely* dies, re-launch the SAME §5 command
       with `--resume` → restores from the last saved epoch boundary (loses ≤1 partial
       epoch). Verified working repeatedly (epochs 4→5→6→7→8→…→25 across launches).
     - **⚠ Liveness ≠ harness task status — see §4.** The python survives harness
       "killed/stopped" notifications; check the real PID, do NOT reflexively relaunch.
     EfficientNet-B3 NOT started (gated on ResNet-50 passing the §3.3 / §8 probe).
3. **Linear-probe acceptance gate** (`scripts/run_ssl_probe.py`): probes random / ImageNet
   / SSL on the EyePACS-test `Usage` slice. Accept iff, **for both backbones**,
   κ(SSL) − κ(random) ≥ 0.05 **and** κ(SSL) ≥ κ(ImageNet) − 0.03. On pass it flips
   `meta.gate_passed=True` → **unblocks Exp-1 Configs B/D** (which currently fail-fast).
   - **▶ NOT yet run for real** (a 300-row `--limit` smoke passed end-to-end; the full
     53,576-row gate is queued for the faster PC).
   - **256² cache now TRAVELS on E: as a tarball (2026-07-07):**
     `experiments/outputs/ssl/ssl_cache_256.tar` (4.02 GB, gitignored; verified 53,577
     files = 53,576 PNG + `cache_meta.csv`). Built via a single sequential tar write (safe
     vs the §4 "53k small-file writes crash the VM" pattern). **On the faster PC**, extract
     it to that machine's **WSL-native ext4** (NOT /mnt/e — same §4 write-storm risk), then
     point `ssl.cache_dir` there via that PC's own `_wsl_local.yaml`:
     `mkdir -p ~/ssl && tar xf /mnt/e/dissertation-project/experiments/outputs/ssl/ssl_cache_256.tar -C ~/ssl`
     → cache at `~/ssl/ssl_cache_256`. Without the cache the probe still works but silently
     falls back to the slow live-preprocessing path.
   - **Rewired this session (see §6):** now uses `CachedEyePACSProbeDataset` (reads the
     256² Stage 0–4 cache — the same fix training already had) → gate drops from hours to
     minutes; and a **resumable feature cache** at `outputs/ssl/v1.0/probe_features/`
     (`{backbone}_{init}_{split}.pt`, atomic write, stale-count-guarded) so a killed run
     re-extracts only what's missing. `--no-feature-cache` disables it; `--limit` smokes
     never write it. Verified: cached probe tensor == live path (bit-identical bar ≤1 uint8
     level at a few px); `tests/test_ssl.py` 15 passed.
4. ✅ **DONE.** The spawn-fix + cache-wiring + `--resume` code is committed (`c1e3320`).
   `_wsl_local.yaml` remains intentionally uncommitted (machine-specific). Still dirty in
   the working tree: `TASK.md` (this file, status notes) + `.claude/settings.local.json`.
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
- **★ KEY FINDING (2026-06-29) — a harness "killed/stopped" notification does NOT kill the
  training.** The notification refers only to the **Windows-side `wsl.exe` relay** the
  harness tracks. When that relay is stopped, the **Linux-side python is reparented to init
  (PID 1) inside the WSL VM and keeps running.** Verified: a single python process ran
  **continuously ~6 h to epoch 25** while the harness reported FIVE "killed" events for its
  successive wrapper tasks. **Implications for any future session:**
  - **Judge liveness by the real process, NOT the harness task status.** Check:
    `wsl.exe -d Ubuntu -e sh -c "ps -eo pid,etime,cmd | grep '[p]ython -u scripts/run_ssl_pretrain'"`
    and `nvidia-smi --query-compute-apps=pid,used_memory --format=csv`.
  - **Do NOT reflexively re-launch on a "killed" notification.** A second `--resume` while
    the first is alive risks **two trainers writing the same `train_state_resnet50.pt`** →
    checkpoint corruption (and there is ~8.5 GB free VRAM, enough for a 2nd batch-16 process
    to actually start). Only re-launch after confirming **zero** live python trainers.
  - The default WSL distro on this machine is **`docker-desktop`** (empty); the project
    distro is **`Ubuntu`** — always target it explicitly: `wsl.exe -d Ubuntu ...`.
- **`setsid nohup` does NOT survive here** (tested 2026-06-29) — confirms the bullet above:
  a one-shot `wsl.exe bash -lc` that returns still loses the detached child. The only launch
  method that yields a durable trainer is the **harness background runner** (its python then
  outlives the runner via init-reparenting, per the KEY FINDING).
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

## 4½. Storage & working model — the optimal-run playbook (READ FIRST for any run)

**Two storage zones, with different rules. Confusing them either crashes the WSL VM
(§4) or loses work when the drive moves to another PC.**

| Zone | Where | Role | Travels? |
|------|-------|------|----------|
| **E: (durable, source-of-truth)** | `/mnt/e/dissertation-project/...` (9p mount) | Final deliverables + anything that must survive/travel | ✅ on the external drive |
| **Native ext4 (fast scratch)** | `~/...` inside WSL Ubuntu (e.g. `~/ssl_cache_256`) | Fast working copies of bulk data + logs | ❌ machine-local only |

**Why two zones (measured, §1/§4):** the 9p `/mnt/e` mount is *slow to read* and — critically —
**mass small-file writes to it (tens of thousands of PNGs) crash the WSL VM** (`E_UNEXPECTED`).
Native ext4 is fast and safe. So we stage bulk data on native ext4, but keep the authoritative
copy on E:.

**The three write rules (memorise these):**
1. **Reads from `/mnt/e` are fine** (source JPEGs, configs, the cache tarball). Slow but safe.
2. **Big *single-file* sequential writes to `/mnt/e` are fine** — this is how the trainer
   already writes `train_state_*.pt` (413 MB) and trunk `.pt` (90 MB) to `outputs/ssl/v1.0/`
   every epoch across 300 epochs with no crash. The probe `gate_report.json` + the ~6
   `probe_features/*.pt` blobs are also fine (few files).
3. **NEVER mass-write many small files to `/mnt/e`.** 53k PNGs → write to native ext4, then
   **`tar`** the directory as ONE sequential file onto E: (rule 2). Extract on the other side.

**The optimal per-run loop (applies to precompute, training, probe, and every future Exp):**
1. **Stage bulk inputs on native ext4.** If a working cache is missing on this machine,
   either extract the E: tarball (below) or rebuild it there — never point a hot loop at 53k
   files on `/mnt/e`.
2. **Run with resumability ON, deliverables written to E: directly** (single-file writes, rule 2):
   - Training: `--resume` restores from `train_state_<backbone>.pt` (atomic, per-epoch) → survives
     any kill, continues the exact LR/momentum curve. Cleared on clean finish.
   - Probe: resumable feature cache `outputs/ssl/v1.0/probe_features/{backbone}_{init}_{split}.pt`
     (atomic, stale-count-guarded) → a killed probe re-extracts only what's missing.
   - **Judge liveness by the real PID, not harness task status** (§4 KEY FINDING).
3. **At the END, guarantee everything is on E:.** Deliverables already are (they were written
   there). Any bulk cache that only lives on native ext4 and is worth keeping → `tar` it to E:
   (as done for the 256² cache, below). **Nothing important may be left only on native ext4
   when the session ends** — that disk does not travel.

**Answer to "can I copy to the computer's memory, work there, then copy back to E:?" → YES —
that is exactly the intended model.** Bulk working data lives on native ext4 for speed/VM-safety;
the *result* must end up on E:. Round-trip via `tar` (single-file writes both ways).

**Portability of the 256² cache (done 2026-07-07):** it is on E: as
`experiments/outputs/ssl/ssl_cache_256.tar` (4.02 GB, gitignored; verified 53,577 files).
On each machine:
```bash
# extract the traveling tarball to THIS machine's native ext4 (NOT /mnt/e):
mkdir -p ~/ssl && tar xf /mnt/e/dissertation-project/experiments/outputs/ssl/ssl_cache_256.tar -C ~/ssl
#   → cache at ~/ssl/ssl_cache_256   (note: differs from this machine's ~/ssl_cache_256)
# then set ssl.cache_dir to that path in THIS machine's own configs/_wsl_local.yaml
```

**No code change is needed for portability.** The SSL/probe code reads the cache location only
from `ssl.cache_dir` (project rule: no hardcoded paths). The machine-specific value lives solely
in `configs/_wsl_local.yaml` — which is **uncommitted but DOES ride the E: drive**, so on another
PC it arrives with THIS machine's paths; edit its 3 keys (`paths.eyepacs`, `ssl.cache_dir`,
`ssl.batch_size`) to match that PC. If the cache is absent the probe/training silently fall back
to the slow live-preprocessing path — the probe log shows `dataset=EyePACSProbeDataset` (live) vs
`CachedEyePACSProbeDataset` (cached), so that line is your fast-path check.

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
- **Probe cache + resumable-features rewrite (2026-07-07, this session):**
  `src/ssl/dataset.py` (new `CachedEyePACSProbeDataset` + `resolve_normalize_stats` +
  cache branch in `EyePACSProbeDataset.build_probe_splits`), `src/ssl/probe.py`
  (`_extract_or_load` on-disk feature cache + progress logging in `extract_features`),
  `scripts/run_ssl_probe.py` (`feature_cache_dir` wiring + `--no-feature-cache`). Not yet
  committed — the 3 files are dirty in the working tree alongside `TASK.md`.

End of TASK.md.
