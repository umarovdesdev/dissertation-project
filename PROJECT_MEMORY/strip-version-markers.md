---
name: strip-version-markers
description: "User-directed: ALL V5/V4/V3 version markers (V5 IS a version marker, not a preserved proper noun) banned outside thesis/; defense/experiments/demo/server done, council-export scrubber added md2gost.py 2026-06-12. 2026-06-16: V5-as-NAME also purged INSIDE thesis/ (arm='integrated arm'), VERSIONING_POLICY §2 + root CLAUDE.md reconciled; remaining root TODO = TASK.md, SUPERVISOR_HANDOFF.md, defense figure-script labels"
metadata:
  type: project
---

User wants every version marker (`V5`, `_V5`, `v5`, `V4`, `V3`, …) removed from all directories **outside `thesis/`**, preserving meaning. This **reverses** the old `thesis/governance/VERSIONING_POLICY.md` proper-noun exception (which said the `V5` proper noun was "preserved in all locations"). **UPDATED 2026-06-16:** §2 of that policy is rewritten to retire the exception (`V5` is a version token, never a name); §3 PRESERVE no longer preserves bare `Vn`; root `CLAUDE.md` versioning note reconciled.

Agreed replacement convention (confirmed by user):
- `V5 pipeline` / `Full V5` / `V5 препроцессинг` → **"pipeline"** / **"preprocessing pipeline"** / **"full pipeline"**; the only two comparison terms are **baseline** and **pipeline**.
- Formula subscripts `Δ_V5`, `ALO_V5` → `Δ_pipeline`, `ALO_pipeline`.

Deliberately KEPT (would break meaning / are real references):
- `CLAHE SV2` / `clahe_sv2` — a **method name**, NOT a version; leave everywhere.
- `Inception-v3` — third-party architecture name. `IMAGENET1K_V2` — torchvision `ResNet50_Weights` enum. `cv2` (OpenCV), `conv1/conv2`, `pipeline_val` — not version tags.

experiments/ rename map (DONE 2026-06-03):
- files: `pipeline_v5.py→pipeline.py`, `augmentation_v4.py→augmentation_unified.py`, `smoke_test_v4.py→smoke_test.py`, `precompute_v5_cache.py→precompute_cache.py`, `test_v5_cache.py→test_cache.py` (all `git mv`).
- symbols: `PreprocessingPipelineV5→PreprocessingPipeline`, `PreprocessingV5Config/PreprocessingV4Config→PreprocessingConfig`, `FundusAugmentationV4→UnifiedFundusAugmentation` (V3 `FundusAugmentation` KEPT — live separate class), `_V5PipelineAdapter→_PipelineAdapter`, `create_baseline_v5→create_baseline`.
- config: yaml key `preprocessing_v5→preprocessing`, value `full_v5→full`, removed dead `pipeline_version` line.
- Verified: all 78 .py compile; renamed modules import OK; tests/test_cache.py 3/3 pass.

EXTERNAL ACTION NEEDED: the Kaggle cache slug was renamed `eyepacs-v5-cache-*` → `eyepacs-cache-*` in code/notebooks. Already-pushed Kaggle datasets are now orphaned — either rebuild the cache (`MODE="build_cache"`, ~1–2 h EyePACS) or rename the Kaggle dataset to match. See [[colab-config-d-runner]].

demo/ + server/ (DONE 2026-06-03):
- server `app/preprocessing.py` imports experiments via sys.path; fixed broken `pipeline_v5`/`PreprocessingPipelineV5`/`PreprocessingV5Config` imports → `pipeline`/`PreprocessingPipeline`/`PreprocessingConfig`.
- API contract field renamed `v5_preview_png_b64` → `preview_png_b64` across BOTH server and demo — keep in sync.
- Renamed `v5_pipeline_specification.md`→`pipeline_specification.md`. KEPT: cv2, IMAGENET1K_V2, package-lock.json, demo/build/ (generated).

Council export leak fixed (2026-06-12): `thesis/output/*.md` (allowed to keep `V5`) was rendered verbatim into `defense/docs/*.docx`+`.pdf`, leaking `V5` outside `thesis/`. Fix = a scrubber **in the converter** so it can't regress: `strip_version_markers()` in `.claude/skills/council-docs/scripts/md2gost.py`, called by `convert(..., strip_versions=True)`. Removes `(V5)` parentheticals, bare tokens (`V5`/`v5.2`/`V4`/`V3`), and word forms (`version 5.x`/`версия 5`/`нұсқа 5`), each eating its adjacent space (signature spacing untouched). Source .md unchanged. Rebuilt all 5 deliverables; docx XML verified 0 `V[345]`. User restated the rule "раз и навсегда": **`V5` IS a version marker (5th version)** and must not appear in `defense/`, `demo/`, `experiments/`, or root. See [[council-docs-skill]].

Thesis-internal V5-as-NAME removal (2026-06-16): inside `thesis/`, `V5` was used overwhelmingly as a **name** (V5 pipeline / V5 arm / V5 Stage N / 4-channel V5 tensor / V5 configuration), not as a version. Per user, the name is removed and `V5` kept only as a bare version reference. Applied across ~120 thesis `.md` files (~615 edits, case-sensitive `V5` only, version markers `v5.x`/`V5.x`/`version 5` guarded):
- `V5 arm` / `V5 configuration` → **`integrated arm`** / **`integrated configuration`** (user-chosen name); shorthand `V5 ⟹` / `Performance(V5+SSL)` / `baseline vs V5` → `integrated …`.
- `V5 pipeline` / `8-stage V5 preprocessing` / `V5 Stage N` / `4-channel V5 tensor` → drop `V5` (descriptive form); `full V5` → `full pipeline`; CLAHE clip-limit subscript `CL_{V5}` → `CL_{DC}`.
- Verified: 0 `V5`-as-name left in `thesis/` (only `VERSIONING_POLICY.md` discusses it); no duplicate-word artifacts.
- NB terminology split: **inside thesis** the full-pipeline arm = "integrated arm"; **outside thesis** comparison terms stay "baseline" vs "pipeline" (root CLAUDE.md uses both: pipeline for the contrast, "integrated arm" as the named arm).

Status: `thesis/` (names) + `defense/` + `experiments/` + `demo/` + `server/` complete; council-export scrubber added 2026-06-12; `VERSIONING_POLICY.md`/root `CLAUDE.md` reconciled 2026-06-16. Still TODO: remaining **root-level docs** (`TASK.md`, `SUPERVISOR_HANDOFF.md`) and a few `defense/figures/scripts/*.py` panel labels still say "V5 Pipeline" — note some root files contain immutable identifiers (branch `feat/v5-cache-colab`, filenames) that must stay. See [[v5-cache-throughput]].
