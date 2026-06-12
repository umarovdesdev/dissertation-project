---
name: colab-config-d-runner
description: "Colab port of the Config-D training notebook — APTOS quick-test then EyePACS real run; persistence on Kaggle Datasets"
metadata:
  type: project
---

`experiments/colab/` is the Google Colab port of [[config-d-kaggle-source]]'s Config-D run, added 2026-06-02. Split of work: **Kaggle ran APTOS** (quick functional test); **Colab is for the real EyePACS Config-D run** (Colab Pro/Pro+ for faster runtime). Same exp1 / Config-D (Full V5 + EfficientNet-B3); one fold per session + `--resume`.

**Critical perf blocker — see [[v5-cache-throughput]]:** on Kaggle (T4, 12 h) **not a single epoch finished** because V5 runs per-image on CPU in the DataLoader. A faster Colab GPU alone will NOT fix this — the GPU starves on CPU preprocessing. The real fix is precompute-and-cache Stages 0–4.

Key design vs Kaggle:
- **`DATASET` switch (cell 1):** `"aptos"` (competition `aptos2019-blindness-detection`, ~3.7k imgs — quick functional test) vs `"eyepacs"` (dataset `dreamer07/eyepacs`, real run). Reuses the same EyePACS-vs-APTOS layout adapter.
- **Persistence = Kaggle Datasets** (updated; supersedes the earlier Google-Drive plan — see [[v5-cache-throughput]]): cache + checkpoints persist as private Kaggle Datasets via the KGAT_ token; no Drive/OAuth/paid tier.
- **Self-contained:** notebook passes Colab paths as dotted overrides to the repo's `kaggle/merge_config.py`. Credentials via Colab Secrets (`KAGGLE_USERNAME`/`KAGGLE_KEY` or `KAGGLE_API_TOKEN`).

**Kaggle account/auth (verified 2026-06-03):** username = `yesmukhamedov` (set in cell 1's `KAGGLE_USERNAME`; slugs become `yesmukhamedov/eyepacs-cache-{DATASET}` + `yesmukhamedov/dr-config-d-ckpts-{DATASET}`). Auth uses the **new `KGAT_…` token** saved locally in `~/.kaggle/access_token` (or env `KAGGLE_API_TOKEN`) — NOT in `kaggle.json` (legacy `{username,key}` only). kaggle CLI 2.2.0 — `-u/--user` flag unsupported.

Gotcha: switching APTOS→EyePACS must delete cached `eyepacs_norm_stats.json` first (else Stage-7 stats are APTOS-derived → not thesis-faithful). Prereq: the cloned `yesmukhamedov/dr-classifier` repo must be current — see [[config-d-cache-handoff]].
