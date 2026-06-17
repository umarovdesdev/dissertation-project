---
name: thesis-kz-translation
description: "Kazakh translation of all Phase-1 approved chapters + KZ assembly + GOST DOCX/PDF export (2026-06-17)"
metadata:
  type: project
---

Full Kazakh translation of the Phase-1 approved manuscript, built 2026-06-17 on candidate
request ("готовые главы хочу переводить и собрать как документ" → KZ, Phase-1 only, GOST DOCX/PDF).

**Translations:** all **53 approved sections** translated EN→KZ into
`chapters/**/translations/*-translation.md` (Ch1 11, Ch2 15 incl. pre-existing §2.1.1,
Ch3 13, §4.1 3, Ch6 9, App A+D). Follows `prompts/translation-directive.md` + `glossary/GLOSSARY_KZ.md`:
technical terms kept English (CNN, CLAHE, ResNet-50, Grad-CAM, pipeline, Loss/focal loss…),
governance codes (CFC/SIR/DGL/IT/SB/NC/EH/OD, H-1…H-7, P1/P2) unchanged, equations/tables/FIG-TAB
placeholders preserved verbatim, self-citations transliterated (Сапақова, Есмұхамедов және Сапақов).
Each file extracts **PART 1 only**; the EN PART-3 compliance checklist stays in the source draft
(noted in an "Аудармашы ескертуі"). `[UNSOURCED CLAIM]`/`[VERIFY]` markers translated & kept.
§2.C carries an internal note: its EN draft still calls §2.3.3 "unwritten" though §2.3.3 is now translated.

**Assembly:** `thesis/assembly/_assemble_kz.py` (mirror of `_assemble_en.py`) extracts the
`## 1-БӨЛІК` body per file in TABLE_OF_CONTENTS_KZ order → `DISSERTATION_KZ_partial_<date>.md`
(2026-06-17: **53 sections, ~41.2k PART-1 words**). Citations left author-year (GOST `[N]` is the
deferred final-assembly pass, same convention as EN — see [[citation-style-convention]], [[thesis-assembly]]).

**GOST export:** `.claude/skills/council-docs/scripts/md2gost.py` — **extended** to render Markdown
pipe-tables (→ Word "Table Grid", header bold), fenced ``` code blocks (→ Consolas), **and figure
placeholders** (2026-06-17). Backward-compatible (council docs have none).

**Figure embedding (2026-06-17):** drafts carry figures as inline text markers
`[FIG-3.1: caption — defense/.../img.png]`. md2gost now parses each, **embeds the actual image** (aspect-fit
to the text box via a PNG-IHDR size read) with a GOST caption below ("Figure N – Title" / KZ "Сурет N – Атауы"),
and replaces the marker with a cross-reference ("in Figure N"/"(Figure N)"; KZ "N-суретінде"/"(N-сурет)").
Dedup by figure number (FIG-3.7/3.8/3.13/3.14 referenced twice → placed once). Repo root auto-found (walks up
to the dir containing `defense/`); lang from `_KZ_`/`_EN_` in filename. The `…` path-ellipsis is normalized.
**All 25 figures embedded, 0 pending** (2026-06-17). Two figure-generation scripts in
`defense/figures/figures_mine/` (matplotlib, serif/print-friendly), kept in-repo, reproducible:
- `_make_ch2_figures.py` → the 4 conceptual diagrams formerly "ASSET TO BE CREATED": FIG-2.1 CLAHE lineage
  §2.1.1, FIG-2.3 Grad-CAM §2.5.1, FIG-2.4 laser thermal-optical §2.4.1, FIG-2.5 quality-metrics §2.6
  → `fig2_{1,3,4,5}_*.png`. (mathtext-safe: `\left/\right`, `\frac`, no `\Big/\dfrac/\text`.)
- `_make_dataset_montages.py` → the 2 sample-dir montages: FIG-1.1 EyePACS DR 0–4 row §1.1.1,
  FIG-4.2 6-dataset×5-grade matrix §4.1.1 (reads `demo/web/public/datasets/<ds>/samples/dr{0..4}/`,
  center-crops to square) → `fig1_1_dr_grades_eyepacs.png`, `fig4_2_dataset_grade_matrix.png`.
All six paths were wired into the source drafts + KZ translations (token replaced INSIDE the `[FIG-…]`
bracket only, never the PART-3 checklist text).

Latest deliverables (with GOST `[N]` citations AND embedded figures): `defense/docs/DISSERTATION_{EN,KZ}_GOST_2026-06-17.{docx,pdf}`
(docx ~4.6 MB, pdf ~6.4 MB). Installed `python-docx`+`docx2pdf`. Version-marker scrub runs by default (deliverable
outside thesis/). See [[thesis-assembly]] for the citation pass.

NOT translated (correctly): Ch0/Ch4 §4.2–4.8/Ch5/Ch7 — experiment-gated Phase 2. See [[thesis-writing-status]].
