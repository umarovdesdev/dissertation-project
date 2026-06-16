---
name: citation-style-convention
description: Drafts intentionally use author-year citations; GOST [N] numbering is deferred to final assembly
metadata:
  type: project
---

In-text citations in `thesis/chapters/**/drafts/` intentionally use **author-year**
(e.g. "Voets et al. (2019)", "In Sapakova, Yesmukhamedov and Sapakov (2025)"). This is a
**working/intermediate** style, NOT the final form — it is deliberately tied to literature
cards so reviewers can trace each claim to its source (writing-prompt: "cite by Literature
Card filename"). The draft header lists the card↔name mapping (e.g. #17 = voets-2019.md).

The **final dissertation** must cite by **numbered square brackets `[11]`** in order of first
appearance, with the reference list numbered in order of appearance, per GOST 7.32-2001 §6.9/§6.11
and GOST 7.1-2003 (binding RK rule, see `council/en/02-formatting/gost-formatting.md`). Page on
repeat: `[11, с. 88]`.

**Decision (2026-06-16):** leave author-year in drafts; do NOT convert per-file. Convert to
`[N]` in a single **citation-assembly pass at final assembly**, because:
- `[N]` ≠ literature-card ID (#17). It is the source's position by first appearance across the
  whole assembled document, so it cannot be computed per-section while chapters are still in flux.
- Self-citations use the same numbered `[N]` form; SIR-4 transparency is carried by the
  surrounding prose ("the candidate's own prior work … previously published results"), not by the
  citation format.

No chapter currently uses `[N]` form (verified: no `[\d+]` matches in `chapters/`). See
[[thesis-writing-status]], [[literature-corpus-120]].

The citation-assembly pass is specified in `thesis/prompts/citation-assembly.md` (Stage G,
written 2026-06-16): consumes the assembled PART 1 bodies in TOC order + the draft Sources-header
card↔name mappings + the cards' bibliographic fields; assigns `[N]` by first appearance, builds the
GOST 7.1-2003 "List of references used," emits a QA resolution report. KZ translation reuses the
same numbers/list.
