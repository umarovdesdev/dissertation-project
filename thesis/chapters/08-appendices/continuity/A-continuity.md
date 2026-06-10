# CONTINUITY NOTE — Appendix A: Source Code of the Preprocessing Pipeline

**Version:** 6.0.0 · PART 2 of the App A session · **First of the two writable-now appendices (App A, App D). Phase-1 appendix item.**

---

**Key concepts established:**
- **App A is a reproducibility artifact**, not narrative prose: it discharges the §4.1.3 promise that the preprocessing + training code is "versioned and reproduced in Appendix A."
- **Central-thesis framing:** under "model = preprocessing + CNN," the preprocessing source *is* part of the model specification; reproducing it makes the thesis auditable.
- **Real on-disk source only.** Catalogue confined to `experiments/src/preprocessing/` (11 stage modules + `__init__.py`); wider apparatus in sibling `experiments/src/` subpackages (`data/`, `models/`, `training/`, `evaluation/`, `explainability/`, `experiments/`, `utils/`) named for locatability.
- **Stage→module map (Table A.1)** rendered inline: Stage 0–7 → real file paths (Stage 5 = both `upgraded_clahe.py` + `polar_clahe.py`, polar default; Stage 6 = `data/augmentation_unified.py`; config via `config.py`/`PIPELINE_PRESETS`; orchestration via `pipeline.py`).
- **One verbatim excerpt** reproduced byte-for-byte from `flat_field.py` (Stage 4) to ground the listing as real source.
- **Bounds:** DGL-2 (efficiency hardware-bound, carried from §4.1.3); no-invention rule (every path on disk, excerpts verbatim); SIR-4 (#19/#21/#23/#24 lineage = prior own work); no performance/deployment claim (CFC-2.4).

**Terms carried:** pipeline stage; orchestrator (`PreprocessingPipeline`); configuration preset (`PIPELINE_PRESETS`); FOV mask; flat-field correction; dual-constraint CLAHE; deterministic execution; baseline vs full-pipeline mode.

**Argument thread:** App A closes the reproducibility loop opened in §4.1.3. The fixed configuration (Table 4.2) + documented hardware + versioned source = recoverable experimental pipeline.

**Final topic:** The closing paragraph states the loop is closed and reiterates DGL-2 / no-deployment-claim bounds.

**Setup for next item (App D — Certificates & Publication Confirmations, Phase-1 writable):** App D is the second and final Phase-1 appendix. It catalogues the real publication-confirmation assets (6 PNGs in `defense/presentation/assets/publications/`) and the 5 distinct self-publications (#19–#24, with #23/#24 a duplicate-card pair for the one EEJET article), all co-authored by the candidate → **SIR-4**. No fabricated entries; identify all as prior own work.

**Unresolved threads / flags (carry forward):**
- **STOP after App D.** Per task instruction, work stops once App D is saved + tracker updated. Do NOT start any Phase-2 section (§4.2–§4.8, Ch 5, Ch 0, Ch 7, App B/C/E/F) — all remain experiment-result blocked.
- **Phase 3 §11.2:** remaining preprocessing modules reproduced in full from the package into the assembled `.docx`; App A paths resolved there.
- **App B/C/E/F remain ⛔ blocked** (App B = Exp 1–7 curves/matrices; App C = DIA-6.3 UML asset; App E = Exp 4; App F = Exp 6).
- **Stage 5 polar-default divergence** (project memory: existing Config-D checkpoints predate the polar default) — relevant only to experiment execution, not to this code catalogue; noted, not acted on.
