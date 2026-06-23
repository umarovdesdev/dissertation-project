# PROJECT MEMORY — index (on drive E:)

Persistent project facts for the dissertation, stored **on the external drive** so they
travel across the candidate's work PC / home laptop / university machine. This replaces
the machine-local `~/.claude/.../memory/` store (which does NOT travel). Read this index
at session start; write new durable facts into `PROJECT_MEMORY/` and add a line here.

Format: one file per fact in `PROJECT_MEMORY/`, with YAML frontmatter (`name`, `description`,
`metadata.type`). Link facts with `[[name]]`. See `REFACTORING.md` for the migration plan.

## People & documents
- [People & identifiers](PROJECT_MEMORY/people-and-identifiers.md) — canonical EN/KZ/RU names (candidate Yesmukhamedov N.S., supervisor Sapakova S.Z. = к.ф.-м.н./associate prof., foreign consultant Al-Haddad), programme **8D06104 Computer systems and software engineering**; human copy `council/PEOPLE.md`
- [council-docs skill](PROJECT_MEMORY/council-docs-skill.md) — `.claude/skills/council-docs/` exports thesis/output abstracts+reviews → GOST .docx/.pdf in `defense/docs/`
- [Abstract/annotation alignment](PROJECT_MEMORY/abstract-annotation-alignment.md) — trilingual аннотация restructured to REAL IITU peer samples (2026-06-18): no "(АВТОРЕФЕРАТ)"/umbrella/separate CONCLUSION; publications folded into body; ends on Structure; +state-programmes, +author-contribution; KZ "pipeline"→"конвейер"

## Thesis writing
- [Thesis writing status](PROJECT_MEMORY/thesis-writing-status.md) — Phase 1 (all writable-now: Ch1/2/3/6 + §4.1 + App A/D) APPROVED 2026-06-10; §2.3.3 deferred; rest Phase-2 experiment-gated; Ch3 detail + carry-forwards
- [Literature integrity flags](PROJECT_MEMORY/literature-integrity-flags.md) — kusuhara rename done; #46/#47/#48 cards (2026-06-12) + #49/#50/#51 cards (2026-06-16) now written; OPEN: DDR full-PDF upgrade, scopus-q2 ID mismatch
- [Thesis assembly](PROJECT_MEMORY/thesis-assembly.md) — `thesis/assembly/_assemble_en.py` concatenates approved PART-1 bodies in TOC order → intermediate EN manuscript (2026-06-16: 53 sections, ~51.5k words); citations unconverted; Ch 1/2/3/6/§4.1 content-complete (§2.3.3 drafted, §2.4.2 consolidated)
- [Thesis KZ translation](PROJECT_MEMORY/thesis-kz-translation.md) — all 53 Phase-1 sections translated EN→KZ → `chapters/**/translations/`; `_assemble_kz.py` → KZ manuscript (53 secs, ~41.2k words); md2gost extended for tables/code → GOST `.docx`+`.pdf` in `defense/docs/` (2026-06-17)
- [Literature corpus → 120](PROJECT_MEMORY/literature-corpus-120.md) — LITERATURE_INDEX v6.1.0 (2026-06-12): 81→120 sources; litres PDFs carded (#46/#47/#48 + FGADR #83) + 38 web sources #84–#121; resolves §1.2.1, §2.3.3, §3.3.2 gaps
- [Citation style convention](PROJECT_MEMORY/citation-style-convention.md) — drafts use author-year (working, card-tied); GOST `[N]` numbering deferred to a single citation-assembly pass at final assembly (decided 2026-06-16)
- [Front-matter deliverables](PROJECT_MEMORY/front-matter-deliverables.md) — TITLE PAGE + NORMATIVE REFERENCES → DESIGNATIONS & ABBREVIATIONS → DEFINITIONS, EN/KZ GOST docx+pdf in `defense/docs/`; **verified & aligned to real IITU samples** (`D:/dissertation_council/Образцы документов/авторы`): house order, exact shared normative-refs list, sample title-page format; built by `build_title.py` + `build_frontmatter.py`

## Experiments / Config-D
- [Config-D pretraining axis](PROJECT_MEMORY/config-d-pretraining.md) — v6.0.0 drops RETFound for ophthalmology SSL; shipped demo Config-D = retired ImageNet artifact (divergence)
- [Config-D Kaggle source](PROJECT_MEMORY/config-d-kaggle-source.md) — trains on `dreamer07/eyepacs`; adapter `is_file()` fix; Run#1 EyePACS failed (12h), Run#2 APTOS ok (interim ckpt f1=0.82)
- [Colab Config-D runner](PROJECT_MEMORY/colab-config-d-runner.md) — `experiments/colab/` two-mode; Kaggle=APTOS test, Colab=real EyePACS; persistence on Kaggle Datasets
- [V5 cache / throughput](PROJECT_MEMORY/v5-cache-throughput.md) — GPU-starved by per-image CPU preprocessing; fix = precompute+cache Stages 0–4 (IMPLEMENTED feat/v5-cache-colab)
- [Config-D cache handoff](PROJECT_MEMORY/config-d-cache-handoff.md) — 2026-06-03 handoff; experiments/ mirrored to dr-classifier repo; next = the Colab run
- [Preprocessing: OD/fovea + polar CLAHE](PROJECT_MEMORY/preprocessing-od-fovea-polar.md) — classical detector unreliable (fovea fails); polar CLAHE now Stage-5 default pivoting on FOV centroid → checkpoints must be retrained; **2026-06-18 decided to replace with learned heatmap detector**
- [OD/fovea heatmap detector plan](PROJECT_MEMORY/od-fovea-heatmap-detector-plan.md) — learned U-Net+DSNT heatmap detector (FundusPosNet ref); build spec in `experiments/docs/od_fovea_heatmap_detector_brief.md`; holds the **PENDING INVARIANTS OD-3 edit** — apply only after the detector is implemented & validated
- [OD/fovea detector — 4-phase task brief](TASK_OD_FOVEA_DETECTOR.md) — root task file (2026-06-23): code-complete standalone detector is **UNTRAINED** (empty weights/); remaining work = Phase1 train+validate on IDRiD → Phase2 integrate into live pipeline (FOV-crop-first reorder + facade + OD-3 governance) → Phase3 demo heatmap discs + drag-correct UI → Phase4 persist corrections + offline fine-tune (detector stays frozen vs DR-CNN)

## Cross-cutting
- [Strip version markers](PROJECT_MEMORY/strip-version-markers.md) — V5 IS a version marker; remove V5/V4/V3 outside thesis/; defense/experiments/demo/server done, council export now auto-scrubbed in md2gost.py (2026-06-12), root TODO
- [Demo stack](PROJECT_MEMORY/demo-stack.md) — launch backend (WSL) + frontend (npm) + Cloudflare tunnels for the real model; human copy `demo/RUNBOOK.md`
