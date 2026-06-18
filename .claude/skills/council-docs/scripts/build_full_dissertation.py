"""Assemble the COMPLETE dissertation (front matter + manuscript body) into one
new document (EN + KZ) as .docx (+ .pdf), with corrected page numbering.

Combines:
    defense/docs/FRONT_MATTER_{EN,KZ}_GOST_<date>  (title, contents, normative,
        designations & abbreviations, definitions)
    + the manuscript body  thesis/assembly/DISSERTATION_{EN,KZ}_GOST_<date>.md
      (the working title line + STAGE-G note at the top are stripped, so the body
       starts cleanly at chapter 1).

Numbering — one continuous Word section, title page unnumbered (p. 1), so the
physical page numbers run 1,2,3,… through the whole document. The CONTENTS is
rebuilt so every entry points at its TRUE page in the merged document:
    * front-matter sections (normative / designations / definitions) take their
      real pages, read from the FRONT_MATTER document;
    * manuscript sections take their page in the body + an offset F = the number
      of front-matter pages (the body begins on page F+1).
F and all section pages are measured with MS Word, so no page count is assumed.

Output: defense/docs/FULL_DISSERTATION_{EN,KZ}_GOST_<date>.docx (+ .pdf)

Usage:
    python build_full_dissertation.py [--date YYYY-MM-DD] [--no-pdf]
"""
from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path

from docx import Document

_HERE = Path(__file__).resolve().parent
ROOT = _HERE
while ROOT.parent != ROOT and not (ROOT / "defense").is_dir():
    ROOT = ROOT.parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


md2gost = _load("md2gost")
build_title = _load("build_title")
build_toc = _load("build_toc")
build_frontmatter = _load("build_frontmatter")
bundle = _load("build_frontmatter_bundle")

_CH1 = re.compile(r"^#\s+1\s")


def strip_body(md_text: str) -> str:
    """Drop the working title + STAGE-G note; keep from chapter 1 onward."""
    lines = md_text.splitlines()
    start = next((i for i, l in enumerate(lines) if _CH1.match(l)), 0)
    text = "\n".join(lines[start:])
    return md2gost.strip_version_markers(text)


def page_count(word, docx_path: Path) -> int:
    doc = word.Documents.Open(str(docx_path), ReadOnly=True)
    pages = int(doc.ComputeStatistics(2))  # wdStatisticPages
    doc.Close(False)
    return pages


def assemble(lang: str, body_text: str, merged_num, merged_front, out_docx: Path) -> None:
    src = ROOT / "thesis/output"
    doc = Document()
    md2gost._configure_styles(doc)
    md2gost._configure_page(doc)

    build_title.populate(doc, lang)                       # p.1 (unnumbered)
    doc.add_page_break()
    bundle.render_contents(doc, src / f"contents_{lang}.md", merged_num, merged_front)
    doc.add_page_break()
    bundle.render_simple_md(doc, (src / f"normative_references_{lang}.md").read_text(encoding="utf-8"))
    doc.add_page_break()
    build_frontmatter.render_abbrev_into(
        doc, md2gost.strip_version_markers((src / f"abbreviations_{lang}.md").read_text(encoding="utf-8"))
    )
    doc.add_page_break()
    bundle.render_simple_md(doc, (src / f"definitions_{lang}.md").read_text(encoding="utf-8"))
    doc.add_page_break()
    md2gost.render_into(doc, body_text, lang=lang, base_dir=ROOT)   # manuscript body

    md2gost._add_page_numbers(doc)
    out_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_docx))
    print("[docx]", out_docx.name)


def main() -> None:
    ap = argparse.ArgumentParser(description="Assemble full dissertation (EN+KZ)")
    ap.add_argument("--date", default="2026-06-17")
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()

    docs = ROOT / "defense/docs"
    asm = ROOT / "thesis/assembly"
    tmp = asm / "_tmp_body"
    tmp.mkdir(exist_ok=True)

    import win32com.client as wc
    word = wc.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False
    built = []
    try:
        for lang in ("en", "kz"):
            body_text = strip_body((asm / f"DISSERTATION_{lang.upper()}_GOST_{args.date}.md").read_text(encoding="utf-8"))

            # Measure: front-matter page count F + section pages, body section pages.
            front_docx = docs / f"FRONT_MATTER_{lang.upper()}_GOST_{args.date}.docx"
            F = page_count(word, front_docx)
            _, fm_front = build_toc.dump_pages(word, front_docx)

            # Stripped body alone → its internal page numbers (offset by F when merged).
            body_md = tmp / f"body_{lang}.md"
            body_md.write_text(body_text, encoding="utf-8")
            body_docx = tmp / f"body_{lang}.docx"
            md2gost.convert(body_md, body_docx, base_dir=ROOT)
            body_num, body_front = build_toc.dump_pages(word, body_docx)

            # Clean heading keys have no tab; contents-entry keys ("TEXT\tPAGE")
            # do — keep only the real section headings (language-agnostic).
            merged_num = {k: v + F for k, v in body_num.items() if "\t" not in k}
            merged_front = {k: v for k, v in fm_front.items() if "\t" not in k}
            for k, v in body_front.items():
                if "\t" not in k:
                    merged_front.setdefault(k, v + F)

            out = docs / f"FULL_DISSERTATION_{lang.upper()}_GOST_{args.date}.docx"
            assemble(lang, body_text, merged_num, merged_front, out)
            built.append(out)
            print(f"   [{lang}] front-matter pages F={F}; body starts on page {F + 1}")
    finally:
        try:
            word.Quit()
        except Exception:
            pass

    if not args.no_pdf:
        from docx2pdf import convert
        for out_docx in built:
            pdf = out_docx.with_suffix(".pdf")
            convert(str(out_docx), str(pdf))
            print("[pdf ]", pdf.name)


if __name__ == "__main__":
    main()
