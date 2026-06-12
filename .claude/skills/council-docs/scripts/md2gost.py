"""Convert a council Markdown document into a GOST-formatted .docx (and optionally .pdf).

GOST parameters (per council/en/02-formatting/gost-formatting.md):
    A4, single line spacing, Times New Roman 14 pt,
    margins: left 30 mm, right 10 mm, top 20 mm, bottom 20 mm,
    page numbers centered at the bottom (not printed on the first page).

Markdown supported: # / ## / ### / #### headings, **bold**, *italic*, `code`,
numbered lists (1.), bullet lists (- / *), --- rule, blank-line paragraphs.

Usage:
    python md2gost.py INPUT.md [-o OUTPUT.docx] [--pdf]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt

FONT_NAME = "Times New Roman"
FONT_SIZE = 14  # pt
FIRST_LINE_INDENT_CM = 1.25

_INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*].*?\*|`.+?`)")

# --- Version-marker scrubbing -------------------------------------------------
# Council deliverables are rendered OUTSIDE thesis/ (into defense/docs/). Per the
# project versioning policy, version markers — including the "V5" proper noun for
# the preprocessing pipeline — must never leak outside thesis/. The source .md in
# thesis/output/ is allowed to keep them; this converter strips them on the way
# out so the .docx/.pdf never carry a version. See REFACTORING.md §"V5 leak".

# Each pattern eats one adjacent space (leading where present) so removal leaves
# no double space and no space before punctuation — without touching whitespace
# elsewhere on the line (e.g. signature underscores spaced for layout).
# Parenthetical version tag, e.g. " (V5)", "(v5.1)", "(version 5.0)", "(нұсқа 5)".
_VER_PAREN = re.compile(
    r"[ \t]*\((?:[Vv][345](?:\.\d+)*|(?:version|версия|версии|нұсқа)[ \t]*[345](?:\.\d+)*)\)",
    re.IGNORECASE,
)
# Bare token, e.g. " V5", " v5.2", " V4.1", " V3" (leading space consumed).
_VER_TOKEN = re.compile(r"[ \t]*\b[Vv][345](?:\.\d+)*\b")
# Word form, e.g. " version 5.0", " версия 5", " нұсқа 5.1" (leading space consumed).
_VER_WORD = re.compile(
    r"[ \t]*\b(?:version|версия|версии|нұсқа)[ \t]*[345](?:\.\d+)*\b", re.IGNORECASE
)


def strip_version_markers(text: str) -> str:
    """Remove version markers (V3/V4/V5, decimals, word forms) from `text`.

    Council deliverables render outside thesis/, where no version marker —
    including the "V5" pipeline proper noun — may appear. Each pattern consumes
    the space preceding the marker so the surrounding text stays clean without
    rewriting unrelated whitespace.

    Args:
        text: Source Markdown that may legitimately contain version markers
            (it lives under thesis/).

    Returns:
        The text with version markers removed.
    """
    text = _VER_PAREN.sub("", text)
    text = _VER_TOKEN.sub("", text)
    text = _VER_WORD.sub("", text)
    return text


def _set_cell_font(run, *, bold=False, italic=False) -> None:
    run.font.name = FONT_NAME
    run.font.size = Pt(FONT_SIZE)
    # Ensure the font also applies to complex-script / Cyrillic ranges.
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), FONT_NAME)
    run.bold = bold
    run.italic = italic


def _add_runs(paragraph, text: str, *, bold=False, italic=False) -> None:
    """Add inline-formatted runs (**bold**, *italic*, `code`) to a paragraph."""
    for token in _INLINE.split(text):
        if not token:
            continue
        if token.startswith("**") and token.endswith("**"):
            _set_cell_font(paragraph.add_run(token[2:-2]), bold=True, italic=italic)
        elif token.startswith("`") and token.endswith("`"):
            r = paragraph.add_run(token[1:-1])
            _set_cell_font(r, bold=bold, italic=italic)
            r.font.name = "Consolas"
            r._element.get_or_add_rPr().find(qn("w:rFonts")).set(qn("w:ascii"), "Consolas")
            r._element.get_or_add_rPr().find(qn("w:rFonts")).set(qn("w:hAnsi"), "Consolas")
        elif token.startswith("*") and token.endswith("*"):
            _set_cell_font(paragraph.add_run(token[1:-1]), bold=bold, italic=True)
        else:
            _set_cell_font(paragraph.add_run(token), bold=bold, italic=italic)


def _configure_styles(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = FONT_NAME
    normal.font.size = Pt(FONT_SIZE)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT_NAME)
    pf = normal.paragraph_format
    pf.line_spacing = 1.0
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)


def _configure_page(doc: Document) -> None:
    for section in doc.sections:
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.left_margin = Mm(30)
        section.right_margin = Mm(10)
        section.top_margin = Mm(20)
        section.bottom_margin = Mm(20)
        section.different_first_page_header_footer = True  # no number on page 1


def _add_page_numbers(doc: Document) -> None:
    """Centered PAGE field in the footer; first-page footer left blank."""
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run = p.add_run()
    _set_cell_font(run)
    run._element.append(fld_begin)
    run._element.append(instr)
    run._element.append(fld_end)
    # Leave the first-page footer empty.
    section.first_page_footer.is_linked_to_previous = False


def _add_hrule(doc: Document) -> None:
    p = doc.add_paragraph()
    p_pr = p._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "auto")
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def _heading(doc: Document, text: str, level: int):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12 if level <= 2 else 6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _add_runs(p, text, bold=True)
        for r in p.runs:
            r.font.size = Pt(16)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        _add_runs(p, text, bold=True, italic=(level >= 4))
    return p


def _body(doc: Document, text: str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Mm(FIRST_LINE_INDENT_CM * 10)
    _add_runs(p, text)
    return p


def _list_item(doc: Document, marker: str, text: str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Mm(12.5)
    p.paragraph_format.first_line_indent = Mm(-7.0)  # hanging
    _add_runs(p, f"{marker}\t{text}")
    return p


_NUM = re.compile(r"^(\d+)\.\s+(.*)$")
_BUL = re.compile(r"^[-*]\s+(.*)$")
_HDR = re.compile(r"^(#{1,6})\s+(.*)$")


def convert(md_path: Path, docx_path: Path, *, strip_versions: bool = True) -> None:
    text = md_path.read_text(encoding="utf-8")
    if strip_versions:
        text = strip_version_markers(text)
    lines = text.splitlines()
    doc = Document()
    _configure_styles(doc)
    _configure_page(doc)

    buf: list[str] = []

    def flush_paragraph() -> None:
        if buf:
            _body(doc, " ".join(buf).strip())
            buf.clear()

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            continue
        if stripped == "---" or set(stripped) == {"-"} and len(stripped) >= 3:
            flush_paragraph()
            _add_hrule(doc)
            continue

        m = _HDR.match(stripped)
        if m:
            flush_paragraph()
            _heading(doc, m.group(2).strip(), len(m.group(1)))
            continue

        m = _NUM.match(stripped)
        if m:
            flush_paragraph()
            _list_item(doc, f"{m.group(1)}.", m.group(2).strip())
            continue

        m = _BUL.match(stripped)
        if m:
            flush_paragraph()
            _list_item(doc, "•", m.group(1).strip())
            continue

        buf.append(stripped)

    flush_paragraph()
    _add_page_numbers(doc)
    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_path))


def main() -> None:
    ap = argparse.ArgumentParser(description="Markdown -> GOST .docx (+ optional .pdf)")
    ap.add_argument("input", type=Path, help="input .md file")
    ap.add_argument("-o", "--output", type=Path, help="output .docx (default: alongside input)")
    ap.add_argument("--pdf", action="store_true", help="also render a .pdf via MS Word")
    args = ap.parse_args()

    md_path: Path = args.input
    docx_path: Path = args.output or md_path.with_suffix(".docx")
    convert(md_path, docx_path)
    print(f"[docx] {docx_path}")

    if args.pdf:
        from docx2pdf import convert as to_pdf

        pdf_path = docx_path.with_suffix(".pdf")
        to_pdf(str(docx_path), str(pdf_path))
        print(f"[pdf ] {pdf_path}")


if __name__ == "__main__":
    main()
