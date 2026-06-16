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
