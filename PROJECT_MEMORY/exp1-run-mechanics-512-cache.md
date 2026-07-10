---
name: exp1-run-mechanics-512-cache
description: Running Exp-1 needs a 512² Stage 0-4 cache (SSL 256² cache NOT reusable) and a single merged config (run_experiment.py uses load_config, not the SSL multi-config chain); native-Windows ops gotchas
metadata:
  type: reference
---

**How to actually run Experiment 1 on the native-Windows RTX 5070 Ti box** (learned
2026-07-10 launching Config D). Non-obvious mechanics that cost investigation:

**1. `run_experiment.py` loads ONE config file** (`load_config`, not the `load_configs`
multi-`--config` chain the SSL scripts use). So you must pre-merge into a single file:
`load_configs("configs/default.yaml","configs/_win_local.yaml","<overlay>.yaml")` +
`yaml.safe_dump`. The merged run configs are `configs/_run_exp1D*.yaml` — **machine-specific
(contain C:/ D: paths), gitignored, uncommitted**. Regenerate per machine.

**2. Full-pipeline configs (B/D) need a 512² Stage 0-4 cache.** Live preprocessing runs the
8-stage pipeline incl. the U-Net OD/fovea detector per image (~0.39 img/s) → infeasible
(months for 35k×5 folds). The **SSL 256² cache is NOT reusable** (wrong resolution). Build the
512² cache once: `scripts/precompute_cache.py --images-root D:/datasets/EyePACS/train
--labels-csv .../trainLabels.csv --output-dir C:/ssl_data/cache_512 --preset efficientnet
--num-workers 14` (resumable). Then set `paths.cache_dir: C:/ssl_data/cache_512` in the merged
config → exp1 uses `CachedEyePACSDataset` (runs only Stages 5–7 live). Norm stats already exist
at `experiments/data/processed/eyepacs_norm_stats.json` (dataset-specific, thesis-faithful).

**3. Native-Windows ops gotchas:**
- **`PYTHONIOENCODING=utf-8` is mandatory** for scripts that print Unicode — `precompute_cache.py`
  crashes at the very end printing a box-drawing char under the cp1252 console (work is already
  done, but exit code is non-zero → breaks orchestrators). `run_ssl_pretrain.py` self-reconfigures;
  `precompute_cache.py` does not.
- **Run the precompute detector on CPU** via `CUDA_VISIBLE_DEVICES=''` so 14 spawn workers don't
  each grab GPU memory (contention/OOM). Training stages then get the GPU (unset the var).
- **Detached `Start-Process` (hidden, `-RedirectStandardOutput`) is the durable launch** — harness
  background jobs get killed. Long chains run as a detached PS orchestrator that writes a DONE/ABORT
  marker (pattern: `C:/ssl_out/orchestrate_*.ps1` → `*_DONE.txt`). PARSE-check with
  `[PSParser]::Tokenize` before launching (PS 5.1 chokes on nested-if + `*>>` + here-strings).
- Env python: `C:/mamba/envs/dr-classifier/python.exe` (torch 2.11+cu128, Blackwell sm_120).

**4. `_eval_utils._train_fresh` bug does NOT block Exp-1** — Config A–D go through
`Trainer.train_fold`, not the broken fresh-train path (that is an exp2/blending concern).
See [[continual-ssl-init-decision]], [[linear-probe-noise-fix]].
