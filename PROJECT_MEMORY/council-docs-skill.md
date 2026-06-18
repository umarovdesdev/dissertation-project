---
name: council-docs-skill
description: "Project skill that exports thesis/output council Markdown (abstracts, reviews) to GOST .docx + .pdf"
metadata:
  type: project
---

Project skill `council-docs` lives at `.claude/skills/council-docs/` (committed to repo, on drive E:). It converts the council Markdown sources in `thesis/output/` (abstract_en/ru/kz, supervisor_review_kz, foreign_consultant_review_en) into GOST-formatted `.docx` and `.pdf`, output to `defense/docs/`.

Toolchain (user chose 2026-06-12): `python-docx` builds the GOST docx (A4, Times New Roman 14, single spacing, margins L30/R10/T20/B20 mm, page numbers bottom-center, no number on page 1); PDF via `docx2pdf` driving installed MS Word (Windows-only step). pandoc/LibreOffice NOT installed.

Run: `python .claude/skills/council-docs/scripts/build_all.py` (flags: `--no-pdf`, `--only <stem>...`, `--out/--src`). Single file: `scripts/md2gost.py FILE.md --pdf`.

GOST rules come from `council/en/02-formatting/gost-formatting.md` + per-doc structure templates in `council/en/11/13/14-*`. The skill enforces formatting only, NOT content compliance — content must still be checked against the template structures. Related: [[people-and-identifiers]].

**Standalone GOST СОДЕРЖАНИЕ / CONTENTS** (added 2026-06-18): `scripts/build_toc.py` emits `defense/docs/TABLE_OF_CONTENTS_{EN,KZ}_GOST_<date>.{docx,pdf}` with right-aligned dotted leaders + real page numbers. Outline sources are `thesis/output/contents_{en,kz}.md` (flat list: only the title centered; chapters `##`, sections `###`, subsections `-`; internal version/binding line dropped). Page numbers are read from the assembled `DISSERTATION_{EN,KZ}_GOST_<date>.docx` via MS Word COM (`Range.Information(3)`), keyed by leading section number (parent section page = min child page; `N.C` = chapter-N conclusion). Sections not yet in the draft get an em-dash `—`, so numbers track the current manuscript (re-run after the manuscript grows). Run: `python .claude/skills/council-docs/scripts/build_toc.py --date 2026-06-17 [--no-pdf]`. NOTE: manuscript assembly currently orders Appendices BEFORE the reference list (App p125/p139 < refs p132/p146), so those two back-matter page numbers are out of natural TOC order until assembly order is fixed.
