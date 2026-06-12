"""Build all council deliverables from thesis/output/*.md into GOST .docx + .pdf.

Discovers the known council source documents (abstracts + reviews) under
thesis/output/ and renders each to <out_dir>/<name>.docx and .pdf.

Usage:
    python build_all.py [--src DIR] [--out DIR] [--no-pdf] [--only NAME ...]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import md2gost

# Council source documents living in thesis/output/ (stem -> human label).
DOCS = {
    "abstract_en": "Abstract (English)",
    "abstract_ru": "Abstract (Russian)",
    "abstract_kz": "Abstract (Kazakh)",
    "supervisor_review_kz": "Supervisor review (Kazakh)",
    "foreign_consultant_review_en": "Foreign consultant review (English)",
}


def main() -> None:
    repo = Path(__file__).resolve().parents[4]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=repo / "thesis" / "output")
    ap.add_argument("--out", type=Path, default=repo / "defense" / "docs")
    ap.add_argument("--no-pdf", action="store_true", help="skip PDF rendering")
    ap.add_argument("--only", nargs="*", default=None, help="build only these stems")
    args = ap.parse_args()

    stems = args.only or list(DOCS)
    built: list[Path] = []
    missing: list[str] = []

    for stem in stems:
        md = args.src / f"{stem}.md"
        if not md.exists():
            missing.append(stem)
            continue
        docx = args.out / f"{stem}.docx"
        md2gost.convert(md, docx)
        print(f"[docx] {DOCS.get(stem, stem):40s} -> {docx}")
        built.append(docx)

    if not args.no_pdf and built:
        from docx2pdf import convert as to_pdf

        # Convert the whole output folder in one Word session (faster, one COM init).
        to_pdf(str(args.out))
        for docx in built:
            print(f"[pdf ] {docx.with_suffix('.pdf')}")

    if missing:
        print(f"\nWARNING: missing sources: {', '.join(missing)}", file=sys.stderr)

    print(f"\nDone. {len(built)} document(s) -> {args.out}")


if __name__ == "__main__":
    main()
