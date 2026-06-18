---
name: abstract-annotation-alignment
description: thesis/output abstracts (EN/RU/KZ) restructured to match REAL IITU peer authorefarat samples (not just the council template)
metadata:
  type: project
---

The trilingual аннотация/abstract (`thesis/output/abstract_{en,ru,kz}.md`) was aligned on
2026-06-18 to the **real authorefarat samples** of IITU doctoral candidates in
`D:/dissertation_council/Образцы документов/авторы/` (Tokhtakhunov, Daurenbayeva, et al.),
**not just** the council template `council/en/11-abstract-annotation/structure.md`. The template
diverged from what candidates actually submit — trust the real samples for the section set/order.

Canonical structure now (all 3 languages, kept fully parallel — 20 `##` sections, identical order):
title (`# ABSTRACT` / `# АННОТАЦИЯ` / `# АҢДАТПА` — **no "(АВТОРЕФЕРАТ)"**) + bold descriptor →
General characteristics of the research → Relevance → Aim → Objectives → Object → Subject →
Methodology and methods → Empirical (experimental) basis → Scientific novelty → Main results →
Statements for defense → Theoretical significance → Practical significance → Reliability →
Approbation + connection with scientific programmes → **Publications (with the numbered works list
folded inline)** → Main content of the work (chapter overview) → Author's personal contribution →
**ends on Structure and length of the dissertation**.

Removed as отсебятина / template-isms that real samples don't have (flagged by the candidate):
- `(АВТОРЕФЕРАТ)` subtitle (was pre-existing in RU/KZ, not from samples).
- Umbrella `# GENERAL CHARACTERISTICS OF THE WORK` heading.
- Separate `# CONCLUSION` / `ЗАКЛЮЧЕНИЕ` / `ҚОРЫТЫНДЫ` section.
- Trailing standalone `LIST OF PUBLISHED WORKS` section (list moved into Publications, in the body).

Content added per samples + real RK normative docs: state-programmes (AI Concept 2024–2029,
President's Address «Kazakhstan in the Era of AI» 8 Sep 2025, Law «On AI» No. 230-VIII 17 Nov 2025,
Law «On Science» art. 20); "Author's personal contribution" section; "General characteristics" lead
para. KZ terminology fixed: Latin "pipeline" → "конвейер" (correct case forms; sentence-start caps).

Metrics stay qualitative (experiments Phase-2 gated — no fabricated numbers; see [[thesis-writing-status]]).
OUTSTANDING: Scopus **percentile** (have Q3 only). Build via [[council-docs-skill]] → `defense/docs/`.
NOTE: `defense/docs/*.docx` lock if open in Word — close before rebuild.
