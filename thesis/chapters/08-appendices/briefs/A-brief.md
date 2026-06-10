# SECTION BRIEF
## Appendix A — Source Code of the Preprocessing Pipeline

**Chapter:** Appendices (follows Ch 7)
**Section Function:** supporting material / reproducibility artifact (CODE CATALOGUE, not results)
**Word Count Target:** 700–1,000 words of explanatory prose framing the code listing (the code itself is reproduced/referenced by real path, not counted)
**Paragraph Count Target:** orientation prose + a stage→module map table + a representative verbatim excerpt

> **Pre-step gate check (PLAN §10 / §3.1):** PASSED. Required resource: **APP-A ✅ AVAILABLE** (`ASSET_INVENTORY.md §2`, row APP-A → `experiments/src/preprocessing/` (+ `experiments/src/`)). On-disk source verified present (11 stage modules + `__init__.py` in `experiments/src/preprocessing/`; full `src/` tree catalogued in `experiments/CLAUDE.md`). Nothing ❌ MISSING. No experiment outcome cited.

---

### GOVERNANCE BINDINGS

**Hypotheses tested/supported:** None — supporting artifact.
**Paradigm positioning:** None.
**Primary claims advanced:** None empirical. Supports the **reproducibility** commitment of §4.1.3 and the **CENTRAL_THESIS** (model = preprocessing + CNN; the preprocessing source is an integral model component, not ancillary tooling).
**Forbidden claims (must not appear):** CFC-2.1, CFC-2.2, CFC-2.4, CFC-2.5 — the appendix presents code, never a performance or deployment claim.
**Non-claims (must not assert):** None empirical at risk.
**Source interpretation rules:** **SIR-4** (the pipeline lineage descends from prior own work #19/#21/#23/#24 — the upgraded-CLAHE and preprocessing-integration line; identify as prior own work where the lineage is named); **SIR-1** (no amplification — list the code as it is on disk; do not describe capabilities the code does not implement).
**Scope boundaries:** **DGL-2** (carried from §4.1.3 — the code is reproducible, but its efficiency characteristics are hardware-bound). **No invention rule (binding for this appendix):** every file named must exist on disk at the stated path; no code may be fabricated, and any excerpt reproduced must be verbatim from the real file.
**Evidence thresholds:** None (non-experimental).

---

### CONTENT SPECIFICATION

**Section objective:** Provide the reproducibility artifact promised in §4.1.3 — a catalogue of the real, on-disk preprocessing source, mapping each of the eight pipeline stages (Ch 3) to its implementing module by real path, so an external party can locate and re-run the exact transformation applied to every image. Reference the code by path; reproduce at most one short representative module verbatim to ground the listing.

**Argumentative spine (required):**
- **Thesis:** The preprocessing pipeline is reproduced here as source because, under the central thesis, it is part of the model: the listing is what makes "model = preprocessing + CNN" auditable rather than asserted.
- **Reasoning chain:**
  1. Open from §4.1.3's promise: the preprocessing pipeline and training code are "versioned and reproduced in Appendix A."
  2. State the location and layout of the real source tree (`experiments/src/`), and the canonical preprocessing package (`experiments/src/preprocessing/`) that implements the eight stages.
  3. Render the **stage → module** map (Stage 0–7 → real file path), drawn from the on-disk package and `experiments/CLAUDE.md`.
  4. Reproduce one short, representative module **verbatim** (Stage 4 flat-field, `flat_field.py`) to show the listing is real source, not paraphrase.
  5. Note the orchestrator (`pipeline.py`) chains the stages, the configuration surface (`config.py` / `PIPELINE_PRESETS`) selects baseline vs full-pipeline mode, and the wider `src/` tree (data, models, training, evaluation, explainability, experiments, utils) holds the rest of the reproducible apparatus.
  6. Bound it: DGL-2 (efficiency hardware-bound); no-invention rule (everything listed is on disk); no performance claim.
- **Conclusion / hand-off:** The appendix closes the reproducibility loop opened in §4.1.3; together with the fixed configuration (Table 4.2) and the documented hardware, the versioned source makes the experimental pipeline recoverable.

**Required content elements:**
1. Pointer back to §4.1.3 (reproducibility promise) and to the central thesis (preprocessing = model component).
2. Real source-tree layout: `experiments/src/preprocessing/` package contents + the broader `experiments/src/` subpackages.
3. **Stage → module** map table (Stage 0–7 → real file path), each entry verifiable on disk.
4. One verbatim excerpt (Stage 4 `flat_field.py`) reproduced exactly.
5. Configuration/orchestration note (`pipeline.py`, `config.py`, `PIPELINE_PRESETS`; baseline vs full-pipeline mode).
6. Bounds: DGL-2; no-invention rule; no performance/deployment claim.

**Required tables/figures:**
- **Stage→module map** rendered inline as Markdown (from the on-disk package + `experiments/CLAUDE.md`).
- **One verbatim code block** (`flat_field.py`), reproduced exactly from disk.

**Required equations:** None (the flat-field relation `corrected = image − GaussianBlur(image, σ) + 128` appears only as reproduced from the real module docstring).

---

### SOURCE MAPPING

| Source | Role | Specific Content |
|--------|------|------------------|
| `experiments/src/preprocessing/` (on disk) | primary artifact | `__init__.py`, `pipeline.py`, `config.py`, `canonical_flip.py`, `canonical_orientation.py`, `crop_resize.py`, `flat_field.py`, `clahe.py`, `upgraded_clahe.py`, `polar_clahe.py`, `imagenet_normalize.py`, `od_fovea_detect.py` — the eight-stage implementation |
| `experiments/CLAUDE.md` | source-tree map | authoritative stage→file mapping and `src/` subpackage layout |
| #19/#21/#23/#24 🔹SELF | lineage (SIR-4) | the upgraded-CLAHE + preprocessing-integration line from which the pipeline descends — named as prior own work, not re-claimed |

**⚠️ Coverage gaps:** None requiring `[UNSOURCED CLAIM]`. The appendix asserts only facts about files that exist on disk (verified) and carries no empirical claim. (Note: Stage 5 ships with the polar-CLAHE variant as default — `polar_clahe.py` alongside `upgraded_clahe.py` — per the current on-disk state; reference both, do not assert a result about either.)

---

### CROSS-REFERENCES

**Backward:** §4.1.3 (reproducibility promise + versioned code); §3.1.1 (8-stage specification); §3.1.2 (dual-constraint CLAHE); CENTRAL_THESIS (preprocessing = model component).
**Forward:** Appendix B (training curves — Phase-2 blocked), Phase 3 §11.2 (resolution of asset paths).

---

### BOUNDARY WARNINGS

1. **No-invention rule is the spine.** Every path/file named must exist on disk; reproduce only verbatim, never paraphrased-as-code.
2. No performance, accuracy, or deployment claim (CFC-2.2/2.4/2.5) — this is a code catalogue.
3. DGL-2 carried: the code is reproducible; its efficiency is hardware-bound.
4. SIR-4: where the pipeline lineage is named, identify #19/#21/#23/#24 as prior own work; SIR-1: do not amplify the code beyond what it implements.

---

### ACCEPTANCE CRITERIA

A draft is **strong** when:
- [ ] Stage→module map is complete (Stages 0–7), every path real and on-disk-verifiable.
- [ ] At least one verbatim excerpt reproduced exactly from a real file.
- [ ] Reproducibility loop from §4.1.3 explicitly closed; central-thesis framing (preprocessing = model) stated.
- [ ] No-invention rule honored; no performance/deployment claim; DGL-2 carried; SIR-4 lineage identified.

A **passable** draft merely lists files. Aim above passable: each entry tied to its pipeline stage and the listing framed as the auditability of the central thesis.

---

### WRITING DIRECTIVES (section-specific)

- **Tense:** present (the code *is* / *implements*).
- **Self-citation handling:** SIR-4 for the #19/#21/#23/#24 lineage.
- **Terminology watch:** pipeline stage; orchestrator; configuration preset; FOV mask; flat-field correction; CLAHE; deterministic execution. Flag any non-glossary term.
- **No fabrication:** paths and excerpts must match disk exactly.
