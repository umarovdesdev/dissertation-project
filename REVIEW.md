# Code Review — Dissertation Monorepo (`experiments/` + `demo/`)

**Reviewer:** Senior ML/software reviewer (Fable model)
**Date:** 2026-07-07
**Repo:** `E:\dissertation-project` (branch `feat/ssl-train-resume`)

## Scope reviewed

- **`experiments/`** — Python/PyTorch ML pipeline. Read in full or in depth: `run_experiment.py`, `configs/default.yaml`, `configs/ssl_pretrain.yaml` (config keys), and the live `src/` tree: preprocessing (`pipeline.py`, `config.py`, `od_fovea_detect.py`), models (`resnet.py`, `efficientnet.py`, `factory.py`), data (`splits.py`), training (`trainer.py`, `losses.py`), evaluation (`metrics.py`), experiments (`exp1_factorial.py`, `exp5_clinical_degradation.py`, `_eval_utils.py`), utils (`config.py`), and the SSL package (`ssl/dataset.py` + greps across `ssl/*`). Tree-walked ~200 source files including the two full repo snapshots under `experiments/outputs/kaggle_config_d*/repo/`.
- **`demo/`** — FastAPI backend (`server/app/*.py`: `main.py`, `inference.py`, `preprocessing.py`, `config.py`, `security.py`) and the React frontend (`web/src/*` via targeted greps: `data.js`, `tabs/ModelArchitecture.js`, `tabs/ResultsMain.js`, `tabs/Overview.js`, `web/public/RESULTS.md`, results JSON).
- **`thesis/governance/`** — cross-checked against `INVARIANTS.md` (v6.2.0), `HYPOTHESIS.md`, `RESEARCH_ARCHITECTURE.md`, plus the root and per-directory `CLAUDE.md` files.

**Note on `outputs/kaggle_config_d/` and `kaggle_config_d_v2/`:** these are full frozen copies of an *older* repo state (they contain `pipeline_v5.py`, `augmentation_v4.py`, `smoke_test_v4.py`, an `augmentation` section in config, etc.). Findings below target the **live** tree; the snapshots are flagged only where relevant (G-4).

---

## Section 1 — Executive summary (top risks)

1. **Demo presents un-run, pre-SSL "expected" results as *Confirmed*, with forbidden preprocessing-only attribution (CFC-2.8).** `web/public/RESULTS.md` and `web/src/data.js` state H-1–H-7 are "✓ Confirmed" with exact F1/AUC/κ/p-values, and explicitly attribute the effect to *preprocessing* ("significant main effect of preprocessing (p<0.001)", "EH-3 preprocessing dominance"). Governance (INVARIANTS v6.2.0) says the integrated arm is *specified, not yet trained*, and CFC-2.8 forbids attributing the H-1 effect to preprocessing alone. The presented numbers were generated under the superseded **ImageNet-init** design (RESULTS.md §3.1: "mask channel = mean of RGB weights"), not the current ophthalmology-SSL design the same demo claims elsewhere (`ModelArchitecture.js`). This is the single largest integrity/consistency risk for the defense. (C-1, C-2, D-1)
2. **`_eval_utils._train_fresh` is broken on its fresh-train path** — references a non-existent `config["augmentation"]` key (KeyError), double-augments, and never sets per-model mixed precision (EfficientNet fp16 overflow). Affects Exp 3/5/6 whenever an Exp-1 checkpoint is absent. (E-1, E-2)
3. **`fallback_rotation_sigma` code/governance contradiction:** code uses `13.0` (`config.py:171`, `default.yaml:32`), but INVARIANTS v6.1.0 states the code uses and is reconciled to **15.0°**. One of them is wrong. (C-3)
4. **`Trainer` defaults mixed precision from the deprecated global `training.mixed_precision: true`** and relies on each experiment to override per-model. Exp 1/2/4/7 override correctly; the shared eval helper does not. (E-2)
5. **Stale config + docstrings** for the Stage-1 detector: dead classical-CV params in `default.yaml`, and `pipeline.py` header still says "classical CV". Low risk but invites confusion about which detector is live. (E-6)

Overall the **live preprocessing/training/eval core is well-engineered** (clean stage split, cache path proven identical to live, strict patient-level CV with a leakage assert, correct EH-3 gate, correct 4-channel conv adaptation, SSL leakage assertions present). The serious problems are (a) demo↔governance drift and (b) the fresh-train fallback path.

---

## Section 2 — `experiments/` findings

- [ ] **E-1 — CONFIRMED — High — `src/experiments/_eval_utils.py:132`.**
  `_train_fresh` does `aug = FundusAugmentation(config["augmentation"])`, but `default.yaml` has **no `augmentation` section** (all augmentation params live under `preprocessing`). This raises `KeyError: 'augmentation'` the moment Exp 3/5/6 fall through to training a fresh model (no Exp-1 checkpoint present). Additionally, `build_full_pipeline(prep_cfg, is_training=True)` (line 131) already augments internally, so passing a *second* `FundusAugmentation` to `EyePACSDataset` would **double-augment** even if the key existed, and `FundusAugmentation` is the legacy `src/data/augmentation.py` class, not the live `UnifiedFundusAugmentation`.
  *Why it matters:* Exp 5/6 (H-6/H-7) silently depend on this path; it will crash the first time it is exercised without a cached Exp-1 model.
  *Fix:* Build the augmentation from the `preprocessing` section (or rely solely on the pipeline's internal Stage 6 and pass `augmentation=None`, matching `exp1_factorial.py`). Delete the separate `FundusAugmentation` wiring.

- [ ] **E-2 — CONFIRMED — High — `src/experiments/_eval_utils.py:133` + `src/training/trainer.py:48`.**
  `Trainer.__init__` sets `self.mixed_precision = tc.get("mixed_precision", True)` from `training.mixed_precision` (`default.yaml:123`, value `true`, explicitly marked *DEPRECATED*). `_train_fresh` constructs `Trainer(config, device="auto")` and **never overrides `trainer.mixed_precision` per model**, so a fresh EfficientNet-B3 full-pipeline model trains with AMP enabled — the exact fp16-overflow condition the project forbids for EfficientNet (CLAUDE.md, `default.yaml:110`).
  *Why it matters:* Violates the binding "mixed precision OFF for EfficientNet" hardware rule; risks NaN/overflow training in Exp 5/6 fresh-train fallback.
  *Fix:* In `_train_fresh`, set `trainer.mixed_precision = config["models"][model_name].get("mixed_precision", False)` before `train_fold` (mirror `exp1_factorial.py:449-451`). Better: make `Trainer` read the per-model flag itself and drop the deprecated global.

- [ ] **E-3 — CONFIRMED — Low — `src/experiments/_eval_utils.py:82,161`.**
  Fresh-train and checkpoint-load use `model_cfg = config["models"][model_name]` without injecting `in_channels` or an SSL init. `create_model` defaults `in_channels=4` (correct for full pipeline) and `pretrained=True` → **ImageNet init**, i.e. the pre-v6.0.0 design. For a degradation/transfer comparison this is defensible, but it is *not* the governance-current integrated arm (which is ophthalmology-SSL-initialised, configs B/D). If Exp 3/5 report "pipeline" numbers from this path, they conflate a different initialization than Exp 1's B/D.
  *Fix:* Prefer loading the gated SSL Exp-1 checkpoint; if training fresh, document that the fallback is ImageNet-init and flag it, per DGL-6's "must be explicitly flagged if used".

- [ ] **E-4 — CONFIRMED — Low — `src/training/trainer.py:70-119`.**
  `train_one_epoch` calls `scaler.unscale_(optimizer)` then `clip_grad_norm_` unconditionally. This is correct when AMP is enabled and a documented no-op when the `GradScaler` is disabled — but the signature type-hints `scaler: torch.cuda.amp.GradScaler` (deprecated import path) while the code constructs `torch.amp.GradScaler("cuda", ...)`. Cosmetic/deprecation only; no runtime bug.
  *Fix:* Update the type hint to `torch.amp.GradScaler`.

- [ ] **E-5 — PLAUSIBLE — Medium — `src/ssl/dataset.py:104-158` (`assert_ssl_corpus_disjoint`).**
  Patient-level disjointness is enforced by comparing filename-stem-derived patient ids (`stem.split("_")[0]`) between the EyePACS **train** and **test** label CSVs. The Kaggle EyePACS train/test splits use independent numeric sequences; depending on how the numbering was assigned, a numeric id (e.g. `"10"`) can appear in *both* CSVs as **different physical patients**. If so, this assert raises a **false-positive INV-SSL-2 violation** and blocks SSL pretraining; conversely, if numbering silently overlaps for genuinely distinct patients the "no patient overlap" guarantee is weaker than it reads.
  *Why it matters:* Either a spurious hard failure or an over-stated leakage guarantee for SB-2.4 / INV-SSL-2.
  *Fix:* Confirm empirically that EyePACS train/test stems and patient ids are globally disjoint; if they are not, namespace ids by split (e.g. `test:<id>` vs `train:<id>`) and rely on image-stem disjointness for the leakage guarantee, documenting the reasoning.

- [ ] **E-6 — CONFIRMED — Low — `configs/default.yaml:26-30` + `src/preprocessing/pipeline.py:11` + `src/preprocessing/config.py:164-169`.**
  Stage-1 is now the frozen learned U-Net+DSNT detector (`od_fovea_net`), but `default.yaml` still carries the **classical-CV** params `od_blur_sigma`, `od_percentile`, `fovea_blur_sigma`, `fovea_inner_factor`, `fovea_outer_factor` (dead on the live path — only `detect_od_fovea_classical` reads their equivalents, and it is off the live path). The `pipeline.py` module docstring (line 11) still labels Stage 1 "classical CV, fallback on low confidence".
  *Fix:* Remove/annotate the dead classical params in the config and update the docstring to the learned-detector description in `od_fovea_detect.py`.

- [ ] **E-7 — CONFIRMED — Low — `src/preprocessing/config.py:127` vs presets/YAML.**
  `PreprocessingConfig.clahe_mode` defaults to `"tiles"`, while every real pipeline (presets `resnet`/`efficientnet`, `default.yaml`) sets `"polar"`. A bare `PreprocessingConfig()` (used by some tests/tools) therefore silently runs a *different* Stage 5 than production. This is intentional (documented in the field comment) but is a foot-gun for anyone constructing a config directly.
  *Fix:* Consider defaulting to `"polar"` and letting tests opt into `"tiles"`, or add a loud warning when a `full` pipeline runs with `"tiles"`.

- [ ] **E-8 — CONFIRMED — Low — `src/experiments/exp1_factorial.py:1-11, 320`.**
  The module docstring frames Exp 1 as "whether the **preprocessing pipeline** produces statistically dominant improvement over resize-only baseline" — the pre-CFC-2.8 single-factor framing. The *run* itself is governance-correct (configs B/D load a gated SSL checkpoint via `_build_model_with_init`), so this is a documentation drift, not a logic error, but it reproduces the forbidden attribution in code comments.
  *Fix:* Reword to "integrated (preprocessing × ophthalmology-SSL) configuration vs baseline (stretch-resize + ImageNet)".

- [ ] **E-9 — CONFIRMED — Low — `src/evaluation/metrics.py:42-46`.**
  `roc_auc_score(..., multi_class="ovr")` raises `ValueError` (caught → NaN) whenever a validation fold is missing a class in `y_true`. With severe EyePACS imbalance and small folds, minority-class absence can intermittently NaN out ROC-AUC for a fold, which then drops from the mean in `_aggregate_cv_results`. Silent but affects the primary metric #2.
  *Fix:* Pass `labels=list(range(num_classes))` where supported, or aggregate probabilities to guarantee class presence; at minimum log when a fold's AUC is dropped.

- [ ] **E-10 — CONFIRMED — Info — doc drift in `experiments/CLAUDE.md`.**
  `experiments/CLAUDE.md` lists `src/models/two_stage.py` and `src/training/train.py`; neither exists in the live tree (only in the kaggle snapshots). Update the module map.

---

## Section 3 — `demo/` findings

- [ ] **D-1 — CONFIRMED — High — `web/public/RESULTS.md:72-90`, `web/src/data.js:649-656`, `web/src/tabs/ResultsMain.js:52`.**
  All six hypotheses are rendered "✓ Confirmed" with concrete metrics and p-values, and H-1 is captioned "EH-3 **preprocessing** dominance … H-1 confirmed for both". Governance (INVARIANTS v6.2.0 header) states "no SSL performance is asserted (the integrated arm is specified, not yet trained)", RESEARCH_ARCHITECTURE §8.5 lists hardware as "TBD", and CFC-2.8 forbids the preprocessing-only attribution. These are **expected/illustrative** numbers presented as measured results with no disclaimer.
  *Why it matters:* A defense audience will read fabricated-looking confirmed results; the preprocessing attribution is a governance violation.
  *Fix:* Add an explicit "projected / illustrative pending execution" banner, replace "Confirmed" status with "Design target / pending", and rename per C-2.

- [ ] **D-2 — CONFIRMED — Medium — internal inconsistency `web/src/tabs/ModelArchitecture.js:36-42` vs `web/public/RESULTS.md:74` & `web/src/data.js`.**
  `ModelArchitecture.js` correctly describes the pipeline arm as ophthalmology-SSL-initialised and cites CFC-2.8 ("attributable only to the integrated (preprocessing × pretrain) pair"). But the numeric results the demo shows were produced with **ImageNet copy-mean init** (RESULTS.md §3.1) and are labelled "Preprocessing Dominance" (`data.js:651`). The demo therefore simultaneously claims SSL init and shows ImageNet-init numbers.
  *Fix:* Regenerate results under the SSL-init design before publishing, or clearly mark the current numbers as ImageNet-init pilot values, and reconcile the H-1 name everywhere.

- [ ] **D-3 — CONFIRMED — Low — `server/app/inference.py:60`, `server/app/config.py`, `_eval_utils.py:83`.**
  Checkpoints are loaded with `torch.load(..., weights_only=False)` (full pickle). For a locally-provided checkpoint this is acceptable, but with a network-exposed server (`host` default `0.0.0.0`) and an optional/empty `DEMO_PASSWORD`, a swapped checkpoint path would execute arbitrary code at load.
  *Fix:* Use `weights_only=True` (checkpoints here are plain `state_dict` + metrics; load metrics separately) or restrict `CHECKPOINT_PATH` to a trusted dir.

- [ ] **D-4 — CONFIRMED — Low — `server/app/main.py:33-39`, `server/app/config.py:53`, `security.py`.**
  CORS allows credentials with `allow_methods=["*"]`/`allow_headers=["*"]`; `host` defaults to `0.0.0.0`; the password gate is fully open when `DEMO_PASSWORD` is unset (only a log warning). Fine for a controlled beta but worth hardening for any public exposure.
  *Fix:* Bind `127.0.0.1` by default, require a password unless an explicit `DEMO_OPEN=1` is set, and scope CORS methods/headers.

- [ ] **D-5 — CONFIRMED — Info — positive: demo reuses the training pipeline.**
  `server/app/preprocessing.py` + `inference.py` build the **same** `PreprocessingPipeline` (`from_preset("efficientnet")`, `create_for_inference`, dataset-specific Stage-7 stats from `eyepacs_norm_stats.json`) as Exp-1 Config D, avoiding train/inference preprocessing drift. This is correct and well-guarded (health endpoint warns when norm-stats are missing). No action; noted as a done-well item and a reference for D-2's fix.

- [ ] **D-6 — CONFIRMED — Low — `web/CLAUDE.md` TODO / stale pipeline images.**
  `demo/web/CLAUDE.md` records an open TODO that the pipeline demonstration images still show the old stretch-resize (not the isotropic-resize + padding + adaptive flat-field pipeline). Presentation assets do not match the current pipeline.
  *Fix:* Regenerate the `public/pipeline/**` stage images from the live pipeline.

---

## Section 4 — Thesis-vs-code consistency findings

- [ ] **C-1 — CONFIRMED — High — Results asserted ahead of execution.**
  Governance: integrated arm "specified, not yet trained"; hardware "TBD". Code/demo: `RESULTS.md` and `data.js` assert Confirmed H-1–H-7 with exact metrics and p-values. See D-1. This is a VCR-3-adjacent risk (results must be reported faithfully) and undermines the defense if challenged.

- [ ] **C-2 — CONFIRMED — High — CFC-2.8 violation in naming/attribution.**
  Governance renamed H-1 to **"Integrated Pipeline Dominance"** and forbids "preprocessing dominates" / "the preprocessing effect" framings. Code/demo still use **"Preprocessing Dominance"** and attribute the effect to preprocessing: `configs/default.yaml:235` (`"Experiment 1: Preprocessing Dominance (2x2 Factorial)"`), `exp1_factorial.py:1-5`, `web/src/data.js:651`, `web/public/RESULTS.md:72,90`, `web/src/tabs/ResultsMain.js:52`. (`ModelArchitecture.js:42` is the one place that gets it right.)
  *Fix:* Global rename to "Integrated Pipeline Dominance" and restate results as the integrated *(preprocessing × pretraining)* pair vs baseline.

- [ ] **C-3 — CONFIRMED — Medium — `fallback_rotation_sigma` value contradiction.**
  INVARIANTS v6.1.0 and RESEARCH_ARCHITECTURE §3.1 state the fallback augmentation rotation σ is **15.0°** and assert "the value the code and evaluation use". The code uses **13.0**: `configs/default.yaml:32` (`fallback_rotation_sigma: 13.0`), `default.yaml:59` (`rotation_sigma: 13.0`), `src/preprocessing/config.py:171,139` (defaults `13.0`). The classical detector's `_MAX_ROTATION_SIGMA = 15.0` cap (`od_fovea_detect.py:187`) is the only 15.0 present, and it is off the live path.
  *Why it matters:* A binding governance doc claims a code fact that is false; the augmentation actually applied at low-confidence fallback (`augmentation_unified.py:140`) is 13.0°, not 15.0°.
  *Fix:* Decide the intended value and reconcile — either bump the config/defaults to 15.0 or correct the governance text back to 13.0 (with a versioning note).

- [ ] **C-4 — CONFIRMED — Low — H-2 CLAHE sweep parameterisation mismatch.**
  Governance H-2 varies the **dual-constraint pair** `(clip_factor, global_threshold)`. `default.yaml:259-261` `clahe_sweep` only sweeps a 1-D `clip_limits` list; `global_threshold` is not swept, and `demo RESULTS.md`/`data.js:652` reports an optimum at "clip_factor=2.5/2.0, threshold=0.03" that the configured sweep grid cannot produce.
  *Fix:* Make the Exp-2 sweep 2-D over `(clip_factor, global_threshold)` to match H-2, or narrow the H-2 claim to the 1-D sweep actually run.

- [ ] **C-5 — CONFIRMED — Info — Stage-1 detector description consistent, params not.**
  The learned-detector implementation (`od_fovea_detect.detect_od_fovea` → `od_fovea_net`) matches OD-3/RESEARCH_ARCHITECTURE v6.1.0 (frozen, FOV-cropped, genuine confidence, polar-CLAHE fovea pivot gated on confidence). Only the dead classical config params (E-6) and the `pipeline.py` docstring lag. Good alignment overall.

- [ ] **C-6 — CONFIRMED — Info — 4-channel conv adaptation matches AOQ-2.**
  `resnet.py:38-53` / `efficientnet.py:50-64` implement exactly the "copy RGB weights to ch0-2, init ch3 from RGB mean" protocol referenced in INVARIANTS AOQ-2/§X, and for the SSL arm `_build_model_with_init` sets `pretrained=False` before loading SSL weights (so no ImageNet contamination). Correct.

---

## Section 5 — Versioning / governance policy violations

- [ ] **G-1 — CONFIRMED — Low — "Preprocessing Dominance" as a name.**
  Not a `v5.X` marker, but a governance-naming violation (see C-2). Enumerated here because VERSIONING_POLICY §2 also governs descriptive naming: the experimental arm must be the "integrated arm", H-1 the "Integrated Pipeline Dominance". Occurrences: `configs/default.yaml:235`, `exp1_factorial.py` docstring, `web/src/data.js:651`, `web/public/RESULTS.md`.

- [ ] **G-2 — CONFIRMED — Info — No `v5.X`/`V5` markers in live code.**
  Greps for `v5.`, `V5`, `version 5`, `pipeline_v5`, `RETFound` across the **live** `experiments/` and `demo/` source found only: (a) `experiments/docs/fundus_ssl_pretraining_brief.md` and `src/ssl/methods.py:17` mentioning RETFound *as explicitly out-of-scope/excluded* (legitimate context, not a version marker), and (b) `package-lock.json` hash false-positives. The live tree is clean of version markers outside `thesis/`. Good.

- [ ] **G-3 — CONFIRMED — Low — version-marker filenames in repo snapshots.**
  `experiments/outputs/kaggle_config_d/repo/` and `…_v2/repo/` contain `src/preprocessing/pipeline_v5.py`, `src/data/augmentation_v4.py`, `scripts/smoke_test_v4.py`, and `V5`-referencing `CLAUDE.md`. These are frozen output artifacts (copied older repo), but they physically place `v4`/`v5` markers outside `thesis/`. Per VERSIONING_POLICY §6 the containment scan may flag them.
  *Fix:* Gitignore/exclude `experiments/outputs/**/repo/` from the version-marker scan, or purge these snapshots from version control.

- [ ] **G-4 — CONFIRMED — Info — `experiments/kaggle/kaggle.json` present.**
  A `kaggle.json` (typically an API credential file) is tracked under `experiments/kaggle/`. If it contains a real token this is a secret leak.
  *Fix:* Verify it holds no credentials; gitignore it if it does.

---

## Section 6 — Positive notes / things done well

- [ ] **Deterministic/stochastic stage split is proven-identical.** `pipeline.py` factors Stages 0-4 (`_precompute_rgb`) from Stages 5-7 (`_finish`), and both the live `__call__` and the cache path (`precompute_deterministic`/`finish_from_cache`) funnel through the same `_finish`, including the cached fovea pivot — a clean way to guarantee the cache cannot drift from live inference.
- [ ] **Patient-level CV is correct and defended.** `PatientLevelKFold` groups by patient, stratifies on the patient's max grade, and `exp1_factorial` calls `verify_no_leakage` and **raises** on any overlap before training.
- [ ] **EH-3 dominance gate matches governance exactly** (`metrics.check_dominance`: ΔF1 ≥ 0.05, ΔAUC ≥ 0.02, Δκ ≥ 0, all-three), and H-1 support requires both B>A and D>C (EH-4 replication).
- [ ] **CFC-2.8 is enforced in the training path**, not just documented: configs B/D declare `init.source: ssl` with a checkpoint, and `_build_model_with_init` fails fast unless the SSL checkpoint carries `gate_passed=true` (`require_gate_passed=True`).
- [ ] **SSL leakage invariants are implemented** (`assert_ssl_corpus_disjoint`, INV-SSL-2) and raise (not warn) on overlap — modulo the id-namespacing concern in E-5.
- [ ] **Focal loss + inverse-frequency weights** are implemented correctly (alpha as a registered buffer, γ=2, weights normalised to sum=K) with a zero-count guard.
- [ ] **Demo backend hygiene:** no hardcoded absolute paths (all via env with sane relative defaults), upload MIME/size validation, single async lock to serialise GPU predictions, graceful degradation when checkpoint/norm-stats are missing, and — importantly — it reuses the exact training preprocessing pipeline (D-5).
- [ ] **Config-driven paths and reproducibility:** seeds/determinism set centrally (`set_seed`), per-model mixed-precision honoured in Exp 1/2/4/7, and dataset-specific Stage-7 stats wired through both training and inference.

---

### Suggested triage order

1. C-1 / C-2 / D-1 / D-2 (governance-facing integrity before the defense).
2. E-1 / E-2 (fresh-train path correctness + fp16 rule).
3. C-3 (rotation-σ reconciliation) and C-4 (H-2 sweep dimensionality).
4. E-5 (SSL id disjointness), E-3, D-3/D-4 (hardening).
5. E-6..E-10, D-6, G-1..G-4 (docs, dead config, snapshots, hygiene).
