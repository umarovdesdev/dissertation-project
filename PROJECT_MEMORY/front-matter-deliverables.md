---
name: front-matter-deliverables
description: GOST front-matter pages (title page, normative references, designations & abbreviations, definitions) — sources + how to rebuild EN/KZ docx+pdf; aligned to real IITU sample dissertations
metadata:
  type: project
---

The GOST front-matter pages that precede the INTRODUCTION — **TITLE PAGE**,
**NORMATIVE REFERENCES**, **DESIGNATIONS AND ABBREVIATIONS**, **DEFINITIONS** — were
authored 2026-06-18 as standalone source Markdown in `thesis/output/`:
`titlepage_{en,kz}.md`, `normative_references_{en,kz}.md`, `abbreviations_{en,kz}.md`
(= the "Designations and Abbreviations" section), `definitions_{en,kz}.md`.

**Verified 2026-06-18 against real IITU council samples** in
`D:/dissertation_council/Образцы документов/авторы/` (esp. the English theses of
Daurenbayeva & Tokhtakhunov) and corrected to match the house style — DON'T diverge:

- **Order** (per samples): TITLE PAGE → NORMATIVE REFERENCES → DESIGNATIONS AND
  ABBREVIATIONS → DEFINITIONS. (NB: this differs from `council/en/10-dissertation/structure.md`,
  which lists Definitions before Designations — the actual dissertations do Designations first.)
  `contents_{en,kz}.md` were reordered to match.
- **Normative references = the EXACT shared IITU list** every doctorant uses (not a guessed
  set): HAC Instruction on preparing a thesis/abstract dated 28 Sep 2004 No. 377-3y;
  GOST 7.32-2001; GOST 7.1-2003; ST RK 34.005-2002; ST RK 34.015-2002; ST RK 34.027-2006;
  ST RK 34.014-2002. Intro line "This thesis uses references to the following standards:".
- **Title page** matches the IITU samples: single org line "International Information
  Technology University" (NO ministry line); `UDC: 004.93:617.735` left / `On manuscript
  right` right; author CAPS; title; `8D06104 – Computer systems and software engineering`;
  "Thesis for the degree of doctor of Philosophy (PhD)"; consultant block as
  credentials-then-NAME-last (Scientific consultant → Candidate of Phys.-Math. Sciences,
  Associate Professor, International Information Technology University → Sapakova S.Z.;
  Foreign consultant → Professor, Universiti Putra Malaysia → Al-Haddad S.A.R.);
  "Republic of Kazakhstan / Almaty, 2026". (2026-06-18: consultant affiliation spelled out
  full — samples use the full university name, not "IITU"/"ХАТУ".)
- **CONTENTS/TOC** (`contents_{en,kz}.md`, rendered by `build_toc.py`): EN heading is
  **"CONTENT" (singular)** — both samples use singular, not "CONTENTS". **INTRODUCTION is a
  SINGLE TOC line** — samples do NOT subdivide the introduction (the 16-item intro breakdown
  was removed 2026-06-18). KZ heading "МАЗМҰНЫ". Kept (samples differ but defensible/manuscript-tied):
  "LIST OF REFERENCES USED" (samples say "REFERENCES"); "APPENDICES" + descriptive titles
  (samples list bare "APPENDIX A/B/C").
- **Abbreviations** = borderless two-column list (abbrev | decoding), no header row, symbols
  appended; **Definitions** = flowing "**Term** — definition" paragraphs. Both formats per samples.
- Definitions/abbreviations content derived from `thesis/glossary/GLOSSARY_EN.md` (v6.0.0).

**Build scripts** in `.claude/skills/council-docs/scripts/`:
- `build_title.py` — title page (positional, direct python-docx; field values embedded; EN+KZ).
  Exposes `populate(doc, lang)` so the bundle can compose the title page into one document.
- `build_frontmatter.py` — the 3 sections as separate files (normative & definitions via
  `md2gost.convert`; abbreviations via a custom borderless-table renderer because md2gost only
  emits bordered tables with a bold header). Exposes `render_abbrev_into(doc, text)`.
- `build_frontmatter_bundle.py` — **combines everything into ONE ordered file** per language:
  `FRONT_MATTER_{EN,KZ}_GOST_<date>.docx`(+pdf). Order TITLE → CONTENTS → NORMATIVE REFERENCES
  → DESIGNATIONS AND ABBREVIATIONS → DEFINITIONS, single Word section so page numbering is
  continuous with the title page unnumbered (title=p.1, contents=p.2, …) — matches the IITU
  samples. CONTENTS page numbers are read from `DISSERTATION_{EN,KZ}_GOST_<date>.docx` via Word
  (same as the standalone TOC); front-matter entries not yet in the manuscript show "—".
- `build_full_dissertation.py` — **assembles the COMPLETE dissertation** (front matter +
  manuscript body) into `FULL_DISSERTATION_{EN,KZ}_GOST_<date>.docx`(+pdf). Strips the body's
  working-title line + STAGE-G note (keeps from chapter 1), one continuous Word section so
  physical numbering runs 1,2,3,… with the title page unnumbered, and rebuilds the CONTENTS so
  every entry points at its TRUE merged page: front-matter sections take their real pages; body
  sections take body-page + F where F = front-matter page count (EN F=10 → body p.11; KZ F=11 →
  body p.12). F and section pages are MEASURED with Word (no assumptions). 2026-06-18: EN 150 pp,
  KZ 165 pp. NB: it needs the body markdown `thesis/assembly/DISSERTATION_{EN,KZ}_GOST_<date>.md`.
  Bugfix kept: section pages are taken from clean heading keys (no tab); contents-entry keys
  ("TEXT\tPAGE") are skipped — earlier an English-only key filter blanked the KZ front sections.
- Rebuild: `python build_title.py --date 2026-06-17`,
  `python build_frontmatter.py --date 2026-06-17`,
  `python build_frontmatter_bundle.py --date 2026-06-17`,
  `python build_full_dissertation.py --date 2026-06-17`.

`md2gost.py` now exposes `render_into(doc, text, …)` (the Markdown loop, no page setup/save) so
the body can be composed into the combined document; `convert()` wraps it.

`titlepage_*.md` are an editable reference copy only — `build_title.py` is the source of truth.
PDF rendering avoids a stuck Word: extract sample-PDF text with `pypdf` (installed), not Word COM
(opening a PDF in Word hangs on a modal). To be assembled into one dissertation later; date stamp
matches the assembled manuscript + TOC. See [[thesis-assembly]], [[council-docs-skill]],
[[people-and-identifiers]].
