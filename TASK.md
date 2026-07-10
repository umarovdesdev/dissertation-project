# TASK.md — Fundus-SSL pretraining: real GPU run + linear-probe gate

**Owner:** Yesmukhamedov N.S. (IITU)
**Driver this session:** Claude Code (Opus) — pre-flight, debugging, orchestration
**Updated:** 2026-07-06

> Prior content of this file (Config-D Kaggle/Colab demo launch, 2026-06-02) was a
> different, older effort. It was superseded here and remains recoverable from git
> history. Ask if you want it restored to a separate file.

---

## ⓪ TL;DR — what we are doing and the one thing in flight

> ### ✅✅ RESOLUTION 2026-07-10 — SSL solved via ImageNet→continual-SSL; Config B/D initialized; Config D run in flight
>
> **Bottom line: the SSL blocker is RESOLVED.** After from-scratch in-domain SSL failed (below),
> pivoted to the governance-sanctioned **ImageNet→continual-SSL** fallback (MoCo-v2, `--pretrained-init`,
> 50 ep, `run v4.0`). Chosen for **BOTH** backbones; both ep50 checkpoints pass the linear-probe gate
> and unblock Exp-1 Configs **B** and **D**. Checkpoints (gate_passed=True) at
> `experiments/outputs/ssl/v4.0/ssl_mocov2_{resnet50,efficientnet_b3}_4ch_256_ep50.pt`.
>
> **Head-to-head on the seed-42 patient-level holdout (robust deterministic probe — the numbers of record):**
>
> | Backbone (Config) | continual κ | ImageNet κ | Δ | verdict |
> |-------------------|-------------|-----------|-----|---------|
> | ResNet-50 (B)     | **0.605**   | 0.357     | **+0.248** | continual = large real in-domain win |
> | EfficientNet-B3 (D) | **0.431** | 0.435     | **−0.004** | continual ≈ ImageNet, **no benefit** |
>
> **⚠ Thesis caveat (do NOT overclaim):** continual helps ResNet-50 enormously but gives EfficientNet-B3
> **no in-domain benefit** (deterministic, not noise). Config D's init is effectively ImageNet-equivalent;
> using it is a symmetry choice. Any integrated-arm effect on D is from preprocessing, not the init.
>
> **Probe noise FIXED.** The linear-probe gate was high-variance (~±0.1 κ for EffNet — same frozen features
> scored ImageNet κ 0.338 vs 0.445 across runs). Fixed `src/ssl/probe.py::_train_linear_head` (feature
> standardization + seed-averaging + guaranteed convergence → **deterministic**). All κ of record are re-gated.
>
> **SIP (supervised in-domain pretraining) built + governance-amended, but NOT chosen.** Implemented
> `scripts/run_sip_pretrain.py` (supervised on the 53k DR grades, patient-level holdout, reuses the SSL
> checkpoint/probe infra) as a stronger alternative; SIP-ResNet scored 0.658 (old noisy probe). Landed the
> **v6.3.0 governance amendment** (INVARIANTS SB-2.4 relaxed + CFC-2.8 extended; CONTRIBUTIONS SC-H
> generalized to "in-domain init, self-supervised OR supervised, gate-selected"; VERSION_SYNC). Candidate
> chose **continual for both** for symmetry; SIP stays a sanctioned option. Spec:
> `experiments/docs/supervised_indomain_pretraining_brief.md`.
>
> **▶ IN FLIGHT — Config D full run, autonomous.** No 512² Exp-1 cache existed (only the SSL 256² cache),
> so a detached orchestrator (`C:/ssl_out/orchestrate_expD.ps1`) runs the whole chain unattended:
> **build 512² Stage 0–4 cache (35k train) → smoke Config D → full 5-fold Config D** (EfficientNet-B3, fp32,
> continual init, dataset-specific norm stats). Multi-day (cache ~hours + EffNet fp32 @512² ~1–2 days).
> Progress `C:/ssl_out/orchestrate_expD.log`; done marker `C:/ssl_out/EXPD_DONE.txt`; metrics
> `experiments/outputs/exp1/metrics.csv`. **NEXT after D:** Config **C** (ImageNet baseline, same backbone —
> the H-1 pair for D), then **A/B**. CFC-2.8 confound stands (H-1 cannot isolate preprocessing).
> Wiring overlays: `configs/exp1_continual_v4_0.yaml` (B/D → continual), `configs/exp1_sip.yaml` (SIP variant);
> machine-merged run configs `configs/_run_exp1D*.yaml` are uncommitted (machine paths). Decision recorded in
> `PROJECT_MEMORY/continual-ssl-init-decision.md`.

> ### ■■ RESULTS 2026-07-09 — SSL METHOD SWEEP COMPLETE: all 4 gates FAILED, in-family SSL exhausted
>
> **Bottom line: from-scratch in-domain CNN-SSL within the INV-SSL-6 family (BYOL / MoCo-v2 / DINO)
> does NOT clear the linear-probe gate on this fundus corpus (256², 53k). No run is in flight; GPU idle.**
> This is now a robust negative result (4 failed gates across 3 method families, flat/declining
> trajectories), not a tuning accident. Candidate decision (2026-07-09): record and pause here.
>
> **Linear-probe gate (kappa quadratic), corrected re-gate — the numbers of record:**
>
> | Method | Epoch | kappa(SSL) | kappa(random) | kappa(ImageNet) | passed |
> |--------|-------|-----------|--------------|----------------|--------|
> | BYOL v1.1 / v1.2 | ep50 | **0.000** | 0.00 | 0.32 | ❌ |
> | MoCo-v2 (v2.0) | ep50 | **0.112** | 0.00 | 0.320 | ❌ |
> | MoCo-v2 (v2.0) | ep100 | **0.109** | 0.00 | 0.303 | ❌ |
> | DINO (v3.0) | ep50 | 0.075 | 0.00 | 0.320 | ❌ |
> | DINO (v3.0) | ep100 | 0.061 | 0.00 | 0.303 | ❌ |
>
> Acceptance needs kappa(SSL) ≥ kappa(ImageNet) − 0.03 (≈0.29) AND ≥ random+0.05. All fail the
> ImageNet-competitiveness arm badly (best SSL 0.11 vs ImageNet 0.30). Source: `C:/ssl_out/COMPARISON.txt`,
> per-run `gate_report_ep{50,100}.json` + `regate_ep{50,100}.log` under `outputs/ssl/v2.0/` and `v3.0/` (copied to D:).
>
> **Interpretation (four findings):**
> 1. **Method change WORKED, partially.** MoCo/DINO beat random for the first time (kappa 0.06–0.11 vs
>    BYOL's exact 0.00) — the no-negatives diagnosis was right; the negative queue / centering recovered
>    *some* DR signal. But it is only ~1/3 of ImageNet.
> 2. **Undertraining is RULED OUT.** ep50→ep100 is flat/declining (MoCo 0.112→0.109; DINO 0.075→0.061).
>    More epochs do not help — this kills the "gate ep50 too early" alternative.
> 3. **MoCo-v2 is the best in-family method** (kappa ≈0.11); DINO is worse (≈0.06–0.075) *despite* the
>    highest training feat_std (0.013) — another confirmation that training-time feat_std is a misleading
>    proxy and only the probe kappa is trustworthy.
> 4. **The corrected gate machinery is proven** (ImageNet scores 0.30–0.32 every run; the earlier
>    "gates crashed in 4s" was a bug — `run_ssl_probe.py` has NO `--method` flag; the orchestrator wrongly
>    passed it. Fixed in the re-gate; probe reads the backbone from the checkpoint, method is irrelevant).
>
> **RECOMMENDED NEXT PATH (not started — awaiting candidate/maintainer):** stop tuning in-family methods.
> Highest-probability unblock for Configs B/D = **ImageNet→continual-SSL** (`--pretrained-init`, MoCo-v2):
> start from ImageNet (kappa 0.32, already passes) and SSL-adapt on fundus — SSL only has to *not destroy*
> a competitive start. Documented fallback (§5). Alternatives to escalate to the maintainer: an INV-SSL-6
> amendment for Barlow Twins / VICReg (redundancy-reduction, out-of-family today), and/or revisiting the
> frozen-linear-probe acceptance criterion, which may be too harsh for from-scratch in-domain SSL on a
> 53k corpus (Fable-5 review, `FABLE5_REVIEW.md`; note the exact-0.000 BYOL kappa partly reflected probe
> majority-collapse under 73% class-0 imbalance — a class-balanced probe control was never run).
>
> **Artifacts preserved (nothing deleted):** `outputs/ssl/v1.0` (BYOL collapse), `v1.1`/`v1.2` (BYOL fail),
> `v2.0` (MoCo-v2 ep50/ep100 + gates), `v3.0` (DINO ep50/ep100 + gates). DINO stopped at ep100 (reached);
> `train_state` on C: is `--resume`-able. Orchestrator scripts live in `C:/ssl_out/*.ps1` (machine-local).

> ### ▶▶ SESSION 2026-07-08 (native Windows / RTX 5070 Ti / drive D:) — METHOD PIVOT BYOL → MoCo-v2
>
> **The BYOL approach is abandoned after 3 failed probe gates; MoCo-v2 (v2.0) is now the run in flight.**
> Read this block first — it supersedes the older v1.1 "healthy ep18" optimism below.
>
> - **v1.1 ResNet-50 BYOL — GATED @ ep50 & FAILED.** The batch-96/lr-0.075 fix reached ep58/300 then
>   stopped. ep50 probe gate: **κ(SSL)=0.0000, AUC 0.508 ≈ random** (κ_imagenet=0.320, AUC 0.711).
>   Same failure as v1.0. Probe machinery proven sound (ImageNet scores normally).
> - **v1.2 = domain-tuned AUGMENTATION fix — BUILT, TRAINED to ep50, GATED & FAILED.** New config
>   `configs/ssl_retrain_v1_2.yaml`: crop [0.2→0.5], color_jitter [0.4→0.2], grayscale 0.2→**0**,
>   solarize 0.2→**0**, blur_view1 1.0→0.5 (the SSL block had copied the raw ImageNet SimCLR recipe;
>   the project's own supervised aug is 4× milder). ep50 gate: **κ(SSL)=0.0000, AUC 0.524** — moved
>   only +0.016 vs v1.1. **CONCLUSION: augmentation is NOT the dominant lever.**
> - **🔎 ROOT CAUSE (confirmed across 3 runs):** BYOL has **no negatives**, so its loss is dominated by
>   the largest un-augmented variation (global illumination / camera / vignetting / FOV) and the
>   **sparse DR lesion signal (<1% of pixels) contributes negligibly** → features are rich (feat_std
>   healthy, 0 dead dims, `not_collapsed=true`) but **orthogonal to DR grade** (even kNN κ≈0.006).
>   feat_std is a false-negative collapse monitor; the linear-probe κ is the only trustworthy test.
> - **⚖ GOVERNANCE GATE on the fix:** the intended pivot was Barlow Twins / VICReg, but those are a
>   **redundancy-reduction family NOT in INV-SSL-6** (allowed: BYOL / MoCo-v2 / SimSiam / DINO; brief
>   §88-92). Using them needs a maintainer amendment to INVARIANTS.md + CONTRIBUTIONS.md — out of scope
>   for the implementer. **Chosen instead: MoCo-v2** — already in the allowed family, **already coded**
>   (`src/ssl/methods.py` MoCoV2), and it targets the exact root cause: an **8192-entry InfoNCE negative
>   queue** forces every image to be distinguishable from thousands of others → representation must
>   encode discriminative content, cannot collapse onto global nuisance. Zero new code — config only.
> - **▶ v2.0 MoCo-v2 — LAUNCHED & HEALTHY (2026-07-08 18:02).** New config `configs/ssl_moco_v2_0.yaml`:
>   `method=mocov2`, optimizer **sgd base_lr 0.01125** (=0.03×96/256) **wd 1e-4**, batch 96, queue 8192,
>   moco_dim 128, temp 0.2, ema 0.999; **keeps the v1.2 domain-tuned augment so METHOD is the only
>   changed variable vs the last BYOL run** (clean attribution). From-scratch, NEW dir `C:/ssl_out/v2.0/`.
>   Healthy start: loss plateaus ~8.7 (near InfoNCE equilibrium ln(8193)≈9.0 — EXPECTED as the queue
>   fills; declines only after the 10-ep warmup), feat_std steady ~0.005, no NaN, GPU 85%/9.3 GB.
>   **ep50 gate pending** via a detached orchestrator (below). Filename: `ssl_mocov2_resnet50_4ch_256_ep50.pt`.
> - **PRIOR RUNS PRESERVED on D: (per candidate request, nothing deleted):** `outputs/ssl/v1.0/`
>   (collapse record, ep50-300 + gate_report), `v1.1/` (ep50 ckpt + gate_report + probe_features +
>   train_state, copied from C: this session), `v1.2/` (ep50 ckpt + gate_report + logs). v2.0
>   deliverables copy to `outputs/ssl/v2.0/` at the ep50 gate.
> - **★ PROCESS RULE for THIS machine (native Windows):** harness-tracked background jobs (Bash/PS
>   `run_in_background`) **get KILLED on long waits**; a detached **`Start-Process`** survives the
>   harness (like the trainer). Long orchestration (wait-for-ep50 → stop trainer → gate → copy → DONE)
>   must run as a detached `Start-Process powershell -File …ps1` writing a `GATE_DONE.txt` marker.
>   GPU can't do training+probe together (14+3.5 > 16 GB) → the orchestrator STOPS the trainer at ep50
>   before gating; `train_state` is atomic per-epoch so `--resume` to ep300 stays possible.
> - **v2.0 run command** (from `D:/dissertation-project/experiments`):
>   ```bash
>   PY="C:/mamba/envs/dr-classifier/python.exe"
>   "$PY" -u scripts/run_ssl_pretrain.py \
>     --config configs/default.yaml --config configs/ssl_pretrain.yaml \
>     --config configs/_win_local.yaml --config configs/ssl_moco_v2_0.yaml \
>     --backbone resnet50 --method mocov2 --device cuda        # add --resume after any kill
>   # gate: same 4 configs + run_ssl_probe.py --backbone resnet50 --method mocov2 \
>   #       --ckpt C:/ssl_out/v2.0/ssl_mocov2_resnet50_4ch_256_ep50.pt
>   ```
> - **NEXT if MoCo-v2 ALSO fails the gate:** escalate to the maintainer for the INV-SSL-6 amendment
>   (Barlow Twins / VICReg), or try the documented **ImageNet→continual-SSL fallback** (`--pretrained-init`,
>   starts at κ=0.32). Do NOT keep tuning BYOL augmentation — that lever is exhausted.

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
- **❌ LINEAR-PROBE GATE RUN & FAILED (2026-07-07, faster PC / RTX 5070 Ti).** Full 53,576-row
  gate on ResNet-50: **κ(SSL)=0.0025, κ(random)=0.0000, κ(imagenet)=0.3025** (ROC-AUC: ssl
  0.514 ≈ random 0.500 vs imagenet 0.715). Both criteria fail (`beats_random=false`,
  `competitive_with_imagenet=false`). `meta.gate_passed` **NOT** flipped → **Exp-1 Configs B/D
  stay blocked**, and **EfficientNet-B3 SSL must NOT be started** (it was gated on this pass).
  Report: `outputs/ssl/v1.0/gate_report.json`. The probe machinery is proven sound — ImageNet
  scores normally (κ=0.30), so a broken probe is ruled out; **the checkpoint is the problem.**
- **⚠ CONFIRMED — BYOL representational collapse (v1.0).** The §3.6 WATCH came true: ep300 features
  are functionally random (probe AUC 0.514). `not_collapsed=true` in the report is a
  false-negative from a lenient feat_std threshold — functionally it IS collapsed.
- **🔎 ROOT CAUSE (2026-07-07):** two compounding bugs, both in the small-batch regime:
  1. **LR ~36× too high.** `SSLTrainer` (src/ssl/trainer.py:192,202) reads `optimizer.base_lr`
     **verbatim, with NO batch-size scaling**. v1.0 used `base_lr=0.45` at **batch 16**; the
     standard BYOL/LARS rule is `lr = 0.2 × batch/256 = 0.0125` at batch 16.
  2. **Batch 16 too small** for BYOL — the projector/predictor use `BatchNorm1d`
     (src/ssl/heads.py:41), whose stats are far too noisy at batch 16 (a classic collapse driver).
- **▶ RESOLUTION — v1.1 retrain LAUNCHED (2026-07-07, RTX 5070 Ti), decision: "retrain large batch".**
  From-scratch BYOL at **batch 96** (13.9 GB VRAM, AMP) + **base_lr 0.075** (= 0.2×96/256), 300 ep,
  written to a **NEW `outputs/ssl/v1.1/`** dir (v1.0 collapsed ckpt + gate_report preserved as the
  record). Config: new `configs/ssl_retrain_v1_1.yaml`. **Healthy start:** loss 3.99→3.47 over ep0,
  feat_std steady ~0.0057 (NOT decaying). **ETA ~28 h** (~5.6 min/ep, ~160 img/s, GPU-bound at 99%).
  Resumable via `--resume` (rolling `train_state_resnet50.pt` in v1.1 dir, per-epoch). **Plan:** gate
  the intermediate ep50 (~4.7 h) / ep100 (~9.3 h) checkpoints early to confirm the fix before ep300;
  only start EfficientNet-B3 after ResNet-50 v1.1 passes the §3.3 gate. Command: §5 (v1.1 variant below).
  - **⚠ CRASH + RECOVERY (2026-07-07 18:36):** the per-epoch `torch.save` of the 413 MB
    `train_state` **crashed writing to the external drive D:** (`RuntimeError: [enforce fail at
    inline_container.cc] unexpected pos …` — a truncated write ~150 MB in; D: had 395 GB free, so
    NOT disk-full → external-USB write flakiness). Atomic-save saved us: the prior **ep6** state was
    intact + verified-loadable. **FIX:** redirected `checkpoint.out_dir` → **`C:/ssl_out`** (fast
    internal disk) in `ssl_retrain_v1_1.yaml`; copied the good ep6 state to C:; relaunched with
    `--resume` (restored ep6). **Verified the epoch save now succeeds on C:** (18:47:40, clean).
    → **All v1.1 artifacts now live on `C:/ssl_out/v1.1/` (NOT D:)**; copy the final deliverable
    ckpt to `D:/…/outputs/ssl/v1.1/` at the end for durability/travel.
  - **LIVE STATUS (last checked 2026-07-07 ~20:26):** ALIVE, paused once by candidate then resumed to
    **ep18/300** (writing to C:), VRAM 14.3 GB, GPU-bound. **loss ~0.47** (warmup done, LR at peak 0.075),
    **feat_std ~0.0075** — healthy (~4× above the collapsed 0.0018; not trending to 0). Pace ~6 min/ep →
    **ep50 ≈ +3 h, ep300 ≈ +28 h.** Real test = the ep50 probe gate.
  - **★ DISK RULE for THIS machine (native Windows):** the external drive **D: is NOT safe for the
    hot checkpoint loop** — a 413 MB file written every epoch crashed torch.save mid-write. Write
    all training/probe outputs to **internal C:**, copy only final deliverables to D:. (Mirrors the
    WSL "native ext4 scratch vs E: durable" rule in §4½, but here the flaky zone is D: itself.)
- **❓ WHY RETRAIN ResNet-50 AGAIN (not move to EfficientNet-B3)?** Because ResNet-50 **v1.0 FAILED the
  gate** — training it to ep300 on 53k imgs "completed" but produced *useless* (collapsed) features
  (κ≈random). The governance order is **ResNet-50 must PASS the gate BEFORE EfficientNet-B3 starts**
  (§3 step 2) — the ResNet gate is the cheap canary: if BYOL is broken, EfficientNet would collapse the
  same way and waste more GPU-days. Also **Config B (ResNet+pipeline) itself requires a working ResNet
  SSL init**, so it stays blocked regardless of EfficientNet. v1.1 is a **redo of a failed run with the
  bug fixed**, not redundant work.
- **▶ EfficientNet-B3 v1.1 — PREPARED for a PARALLEL run on the RTX 3060 / WSL box (2026-07-07).**
  Candidate decided to run EfficientNet-B3 SSL **in parallel** (not strictly after ResNet passes the
  gate). Justified: the ResNet v1.1 fix is **already showing healthy anti-collapse** (feat_std rising
  through ep18), so the "cheap canary" has effectively given its positive signal — applying the SAME
  fix to EfficientNet now is low-risk. **Same two-pronged fix**, EfficientNet-tuned:
  - Config: **`configs/ssl_retrain_eff_v1_1.yaml`** — batch **32**, `base_lr` **0.025** (=0.2×32/256),
    v1.1, `out_dir=/home/yesmu/ssl_out`. **AMP stays OFF** (fp16 overflow); fp32 is VRAM-heavy —
    MEASURED on the 5070 Ti: EfficientNet-B3 fp32 @256² is **batch 64 → 15.9 GB**, so batch 32 (~8.5 GB)
    fits the 3060's 12 GB. Path smoke-tested here: runs, `feature_dim=1536`, healthy start (loss 3.98,
    feat_std 0.016).
  - **Handoff doc (on D:):** `EFFICIENTNET_B3_SSL_HANDOFF.md` (repo root) — pre-flight, launch/resume
    commands (WSL), disk rule (write to `/home/yesmu/ssl_out`, copy final to `/mnt/e/…/outputs/ssl/v1.1`),
    healthy-vs-collapse signatures, and early ep50/100 gating.
  - Both backbones still must pass their probe gate before their checkpoints unblock Exp-1 (B/D).
- **▶ ENV NOTE — the "faster PC" is native Windows, NO WSL, drive = D:.** TASK.md's WSL/`/mnt/e`/
  conda commands do NOT apply here. This session rebuilt the env from scratch: Miniforge GUI
  installer fails (exit 2, non-interactive) → used **micromamba** to create the `dr-classifier`
  conda env (py3.11) at `C:/mamba/envs/dr-classifier`; **torch 2.11.0+cu128** (Blackwell sm_120,
  the 3060's torch 2.5.1 won't run this GPU); `timm` also required (missing from requirements.txt).
  Cache extracted from the E:/D: tarball to `C:/ssl_data/ssl_cache_256`. Machine paths live in a
  NEW `configs/_win_local.yaml` (native Windows) — the committed `_wsl_local.yaml` (RTX 3060/WSL)
  was left untouched so the drive round-trips. Run command: see §5 (Windows variant).
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

### 5-bis. Commands — NATIVE WINDOWS / RTX 5070 Ti (the "faster PC", NO WSL)

Env is **micromamba**, not the failed Miniforge installer. Env python:
`C:/mamba/envs/dr-classifier/python.exe` (torch 2.11.0+cu128, Blackwell). Machine paths +
cache live in `configs/_win_local.yaml` (native, uncommitted); the v1.1 retrain science
(batch/lr/version) lives in `configs/ssl_retrain_v1_1.yaml`. Run from `D:/dissertation-project/experiments`:

```bash
PY="C:/mamba/envs/dr-classifier/python.exe"
# SSL retrain v1.1 (fixes the batch-16 collapse) — writes outputs/ssl/v1.1/
"$PY" -u scripts/run_ssl_pretrain.py \
  --config configs/default.yaml --config configs/ssl_pretrain.yaml \
  --config configs/_win_local.yaml --config configs/ssl_retrain_v1_1.yaml \
  --backbone resnet50 --device cuda            # add --resume after any kill/reboot

# Linear-probe gate on a v1.1 checkpoint (uses the C:/ssl_data cache via _win_local)
"$PY" -u scripts/run_ssl_probe.py \
  --config configs/default.yaml --config configs/ssl_pretrain.yaml \
  --config configs/_win_local.yaml --config configs/ssl_retrain_v1_1.yaml \
  --backbone resnet50 --device cuda
#   (to gate an intermediate ep50/ep100 ckpt instead of the derived ep300 name, add
#    --ckpt outputs/ssl/v1.1/ssl_byol_resnet50_4ch_256_ep100.pt)
```


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
