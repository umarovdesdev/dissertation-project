---
name: thesis-assembly
description: "Intermediate EN manuscript assembly — script, convention, output, and known TOC gaps (2026-06-16)"
metadata:
  type: project
---

Reusable assembly of the dissertation manuscript from approved drafts. Built 2026-06-16 on
candidate request ("собрать готовые части в документ").

**Script:** `thesis/assembly/_assemble_en.py` — re-runnable as more chapters get approved.
**Output:** `thesis/assembly/DISSERTATION_EN_partial_<date>.md`.

**Extraction convention** (matches `thesis/prompts/citation-assembly.md` INPUTS#1): for each
`chapters/**/drafts/*-draft.md` it keeps the `# §x Title` line + the **PART 1: SECTION TEXT**
body only, and drops the `> Draft generated…` blockquote, the **PART 3 Compliance Checklist**,
and the **Word count** block. Files are ordered by parsed section number (`X.C` conclusions and
appendix letters sort last); chapters concatenated in TOC order
(`outline/TABLE_OF_CONTENTS_EN.md`).

**This intermediate build (2026-06-16):** 53 sections, ~51.5k PART-1 words (after §2.3.3 added).
Includes the Phase-1 approved set only — Ch 1, Ch 2, Ch 3, §4.1, Ch 6, App A, App D. Working **author-year citations
are left unconverted**: GOST `[N]` is a single deferred Stage-G pass on the *final* assembled
manuscript (see [[citation-style-convention]]), and KZ translation (Stage E/F) is best done on the
final text — so the candidate chose the plain EN concatenation first.

**Assembled-set gaps: NONE remaining in Ch 1/2/3/6/§4.1.**
- **§2.3.3** In-Domain SSL for Retinal Imaging — **DRAFTED & APPROVED 2026-06-16** (deferral lifted;
  brief/draft/continuity/review saved). Now included in the assembly between §2.3.2 and §2.4.1.
  Ch 2 is content-complete (14/14 numbered + §2.C).

**§2.4.2 RESOLVED (2026-06-16): consolidation legalized, not a gap.** §2.4.2 "Implications for
Diagnostic Image Feature Interpretation" was never written as a standalone subsection; its content
(the laser model is epistemically independent of the diagnostic system + the SB-1.5/SIR-6/CFC-2.4
boundary) was folded into the closing of §2.4.1 during drafting, which transitions straight to
§2.5.1. PLAN.md already excluded §2.4.2 (its checklist/table/count never listed it; "Ch 2 (15)" =
14 numbered subsections incl. deferred §2.3.3 + §2.C). On candidate approval the phantom entry was
removed from `TABLE_OF_CONTENTS_EN.md`, `TABLE_OF_CONTENTS_KZ.md`, and `MASTER_OUTLINE.md`
(content folded into §2.4.1's outline entry; §2.5 not renumbered). Ch 2 = **14 numbered
subsections**, 13 written + §2.3.3 deferred.

**Not in this build (correctly):** Ch 0 (intro), Ch 5, Ch 7, most of Ch 4 (§4.2–§4.8) — all
experiment-gated Phase-2/front-back-matter. Full bound thesis is Phase 3 (assemble → Stage-G
citations → resolve FIG/TAB placeholders → single .docx), after experiments land.

Minor cosmetic: section titles and chapter titles are both `#` (h1) in the Markdown; re-level at
the .docx stage (council-docs / md2gost path).

## Stage-G citation conversion — PREVIEW run (2026-06-16)

Ran the `citation-assembly.md` Stage-G pass as a **preview** on the intermediate assembly (candidate
request). Scripts in `thesis/assembly/`: `_extract_citations.py` (ordered token extraction),
`_apply_citations.py` (author-year → `[N]` by first appearance + reference list + QA). Outputs:
`DISSERTATION_EN_preview_GOST_2026-06-16.md` (converted manuscript + "List of references used")
and `_citation_resolution.md` (token→[N]→card table + QA). `_card_bib.tsv` / `_draft_sources.tsv`
are regenerable intermediates.

**Result (after #52/#53 cards written 2026-06-16):** 125 distinct in-text tokens → **101 external
sources numbered [1]–[101]**, **0 unresolved**.
Self-citations (5 surface forms, 32 occurrences) **left as author-year** — same form maps to
different self-papers by section, so per-section disambiguation (#19 conf/#21 kbtu = one experiment;
#20 kazutb; #22 nan-rk; #23≡#24 EEJET, SIR-5 collapse) is deferred to the real pass. Appendix-D
publication records (7) excluded from the numbered list. 8 co-author/variant collapses handled
(e.g., Le→Tan2019, Sun→He2016, Pluim→Cheplygina, Chairi→Araf).

**Blocking findings — all cleared 2026-06-16:** #52 Guo 2017 + #53 Wang 2004 SSIM were cited but
uncarded → cards written (`guo-2017-calibration.md`, `wang-2004-ssim.md`). "Hinton (2012)" was a
Stage-G extractor artifact, not a gap — it is "Krizhevsky, Sutskever, and Hinton (2012)" = AlexNet
(#65, [19]); map collapses it. **Stage-G preview is now fully clean: 0 uncarded, 0 unresolved.**
See [[literature-integrity-flags]]. **Preview only** — numbers are
provisional (shift when Ch 4/5/0/7 are added); the convention stays: working drafts keep author-year,
the real `[N]` pass runs ONCE at final assembly (see [[citation-style-convention]]).

## Stage-G citation conversion — APPLIED to EN+KZ partial assemblies (2026-06-17)

Candidate flagged that the assembled Phase-1 docs still carried author-year citations (KZ DOCX/PDF
in `defense/docs/`). Ran the real Stage-G pass with a new self-contained script
`thesis/assembly/_finalize_citations.py` (supersedes the preview `_apply_citations.py`):
- One **shared numbering** assigned by first appearance in the **EN** body; the SAME card→[N] map
  applied to **KZ** (citation-assembly.md rule #7, language invariance). Reference list reused, KZ
  heading "ПАЙДАЛАНЫЛҒАН ӘДЕБИЕТТЕР ТІЗІМІ".
- Resolution is **surname-based + language-agnostic**: `surnames_of()` folds accents via NFKD
  (González-Díaz→gonzalez-diaz) and drops all Cyrillic (so KZ connectors "X және әріптестері(нің/не)",
  "X пен/мен Y" fall away), then `resolve()` tries candidate keys full-join→first-author→pairs→singles.
  This fixed the KZ-only gaps the preview's EN-tuned regex missed (KZ declensions, Latin "et al." kept
  in some KZ sections, accented names, comma-separated author lists like "Krizhevsky, Sutskever және Hinton").
- **Result: 102 external sources [1]–[102]** (preview's 101 + **González-Díaz 2024**, previously
  carded-but-uncited, now cited in §2.4.1 → numbers shifted +1 vs the preview). **0 BLOCKING, 0 UNKNOWN.**
  Brackets placed: EN ~219, KZ ~223. Self-citations + App-D records still **author-year by policy**
  (per-section disambiguation pending; SIR-4 prose preserved) — noted in a pending-entries blockquote in each doc.

**Outputs:** `thesis/assembly/DISSERTATION_{EN,KZ}_GOST_2026-06-17.md` (+ `_citation_resolution_final_2026-06-17.md`
QA, exhaustive: flags every remaining `(YYYY)` regardless of card map). Re-rendered **GOST deliverables**
via `md2gost.py`: `defense/docs/DISSERTATION_{EN,KZ}_GOST_2026-06-17.{docx,pdf}`.

**Pipeline:** chapters → `_assemble_{en,kz}.py` → `DISSERTATION_*_partial_*.md` (author-year intermediate)
→ `_finalize_citations.py` (reads those partials as `SRC_EN`/`SRC_KZ`) → `*_GOST_*.md` → `md2gost.py` → docx/pdf.
**The superseded author-year `partial` .md intermediates + the 06-16 preview + the old KZ-partial docx/pdf were
DELETED on candidate request (2026-06-17)** — they are regenerable by re-running `_assemble_*.py`. So to re-run
the citation pass (e.g. for self-citation numbering), **re-assemble the partials first**; `_finalize_citations.py`
still points at the `DISSERTATION_*_partial_2026-06-17.md` paths.

Known minor: a citation page given in a *separate* trailing paren ("… (p. 370)" / "(370-б.)") is left
as-is, not merged into `[N, p. 370]` (only "(year, page)" same-paren forms merge) — final-typesetting refinement.
Numbers remain provisional until experiment-gated Ch 4/5/0/7 join the assembly.
