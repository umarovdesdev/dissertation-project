# VERIFICATION PROTOCOL — Appendix A: Source Code of the Preprocessing Pipeline

**Protocol version:** 6.0.0 · **Inputs:** `drafts/A-draft.md` + `briefs/A-brief.md` + INVARIANTS.md v6.0.0 · **Reviewer pass:** Opus self-verification.

---

## A. CLAIM COMPLIANCE

- [x] Evidence source cited — every module to its real path in `experiments/src/preprocessing/`; source-tree layout to `experiments/CLAUDE.md`; lineage to #19/#21/#23/#24.
- [x] Citation matches the source — Table A.1 stage→module map matches the on-disk package (verified: `flat_field.py`, `crop_resize.py`, `upgraded_clahe.py`, `polar_clahe.py`, `imagenet_normalize.py`, `od_fovea_detect.py`, `canonical_flip.py`, `canonical_orientation.py`, `clahe.py`, `config.py`, `pipeline.py` all present; `data/augmentation_unified.py` present per `experiments/CLAUDE.md`). Reproduced `flat_field.py` block is byte-for-byte.
- [x] Claim strength appropriate — no empirical claim; only file existence + stage mapping + verbatim excerpt.
- [x] Scope boundary stated — DGL-2 carried at final ¶; no-invention rule honored throughout.
- [x] Claim coverage — brief specifies no PC/SC; none introduced.

**A verdict:** PASS.

## B. FORBIDDEN CONTENT SCAN

- [x] CFC-2.1 — no universal generalization.
- [x] CFC-2.2 — no superiority/ranking; catalogue only.
- [x] CFC-2.3 — N/A (no deployment outcome).
- [x] CFC-2.4 — no clinical-grade / real-time / deployment claim; explicitly disclaimed.
- [x] CFC-2.5 — no performance figure cited.
- [x] CFC-2.6 — no amplification; code listed as-is, #19/#21/#23/#24 not over-read.
- [x] CFC-2.7 — sources cited as-is.
- [x] CFC-2.8 — N/A (no H-1 result/attribution).
- [x] CFC-2.9 — N/A (no Gulshan/P1 source).
- [x] NC scan — no empirical NC at risk in a code-catalogue appendix.

**B verdict:** PASS.

## C. TERMINOLOGICAL CONSISTENCY

- [x] pipeline stage, orchestrator, configuration preset, FOV mask, flat-field correction, dual-constraint CLAHE, deterministic execution, baseline vs full-pipeline mode — all in standard form.
- [x] Disambiguation — "reproducible source" distinguished from "reproducible efficiency" (the latter hardware-bound, DGL-2).
- [x] No unresolved `[TERM NOT IN GLOSSARY]` flags.

**C verdict:** PASS.

## D. SOURCE HANDLING

- [x] SIR-1 — code listed as it is on disk; no capability beyond implementation described.
- [x] SIR-2 — DGL-2 hardware bound carried from §4.1.3.
- [x] SIR-3 — N/A (no cross-source metric).
- [x] SIR-4 — #19/#21/#23/#24 identified as prior own work; pipeline framed as consolidating that lineage, not re-claiming its results.
- [x] SIR-5 — #23/#24 duplicate-card pair not double-counted (referenced together as the EEJET line; full reconciliation deferred to App D where the publication itself is catalogued).
- [x] SIR-6/7/8/9 — N/A.

**D verdict:** PASS.

## E. STRUCTURAL INTEGRITY

- [x] Connects to §4.1.3 — opens from the reproducibility promise; closes the loop.
- [x] Cross-references present — backward to §4.1.3, §3.1.1, §3.1.2, CENTRAL_THESIS; forward to App B (blocked) and Phase 3 §11.2.
- [x] Continuity Note accurate and complete (`continuity/A-continuity.md`), incl. App D setup and STOP marker.
- [x] Word count: framing prose target 700–1,000 — Actual: **~840**. PASS. (Reproduced code block excluded from count, as specified.)

**E verdict:** PASS.

## F. SCOPE & PARADIGM

- [x] SB-1.12 / DGL-6 — N/A.
- [x] P1/P2 attribution — no Gulshan/P1 phrasing present.

**F verdict:** PASS.

## G. EVIDENCE THRESHOLDS

- [x] EH-3 / EH-4 — N/A. Non-experimental supporting artifact; no metric.

**G verdict:** PASS (not applicable).

## H. VERDICT

- [x] **APPROVED** — appendix passes all applicable checks (A–G). No revision needed. **Appendix A COMPLETE.**

**Notes for downstream:** (1) Phase 3 §11.2 reproduces the remaining preprocessing modules in full from the package and resolves App A paths in the assembled `.docx`. (2) No-invention rule was the binding spine and is satisfied — every path verified on disk, the one excerpt byte-for-byte from `flat_field.py`. (3) Stage 5 polar-default (`polar_clahe.py`) noted as the current on-disk default; this is a code fact, not an experimental claim. (4) Proceed to App D (the second and final Phase-1 appendix); STOP after App D per task instruction.
