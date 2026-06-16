#!/usr/bin/env python3
"""Assemble the intermediate EN manuscript from approved PART 1 draft bodies.

Per thesis/prompts/citation-assembly.md INPUTS#1: concatenate PART 1 section
bodies only, in Table-of-Contents order; omit the draft header blockquote, the
PART 3 Compliance Checklist, and the Word-count block. Citations are LEFT in
their working author-year form (Stage G conversion is deferred until the full
manuscript is assembled). This is a reversible, read-only-source operation.
"""
from __future__ import annotations
import re
from pathlib import Path
from datetime import date

CH_ROOT = Path(__file__).resolve().parent.parent / "chapters"
OUT = Path(__file__).resolve().parent / f"DISSERTATION_EN_partial_{date.today()}.md"

# Chapter dir -> TOC chapter heading. Only chapters with approved drafts.
CHAPTERS = [
    ("01-problem-domain",
     "1 PROBLEM DOMAIN ANALYSIS AND CURRENT STATE OF AUTOMATED DIABETIC RETINOPATHY DIAGNOSIS"),
    ("02-theoretical-foundations",
     "2 THEORETICAL FOUNDATIONS OF IMAGE PREPROCESSING AND DEEP LEARNING FOR FUNDUS IMAGE ANALYSIS"),
    ("03-methodology",
     "3 METHODOLOGY OF INTEGRATED PREPROCESSING-CNN PIPELINE DESIGN"),
    ("04-experiments",
     "4 EXPERIMENTAL RESEARCH — PREPROCESSING IMPACT ON CNN DIAGNOSTIC PERFORMANCE"),
    ("06-system-architecture",
     "6 ARCHITECTURE OF AN AUTOMATED DR SCREENING SYSTEM FOR RESOURCE-LIMITED ENVIRONMENTS"),
    ("08-appendices", "APPENDICES"),
]

BODY_END = re.compile(r"^(## PART [23]\b|### Word count\b|## PART 2\b)", re.I)
PART1_HDR = re.compile(r"^## PART 1\b", re.I)


def section_key(p: Path):
    stem = p.name.replace("-draft.md", "")
    toks = []
    for t in stem.split("."):
        if t.isdigit():
            toks.append((0, int(t), ""))
        else:  # 'C' (conclusion) and appendix letters sort after numerics
            toks.append((1, 0, t))
    return toks


def extract(p: Path):
    lines = p.read_text(encoding="utf-8").splitlines()
    title = next((l for l in lines if l.startswith("# ")), p.stem)
    # locate PART 1
    try:
        i = next(idx for idx, l in enumerate(lines) if PART1_HDR.match(l))
    except StopIteration:
        return title, "", 0
    body = []
    for l in lines[i + 1:]:
        if BODY_END.match(l):
            break
        body.append(l)
    # trim leading/trailing blanks and stray '---' separators
    while body and (body[0].strip() == "" or body[0].strip() == "---"):
        body.pop(0)
    while body and (body[-1].strip() == "" or body[-1].strip() == "---"):
        body.pop()
    text = "\n".join(body)
    words = len(re.findall(r"\S+", text))
    return title, text, words


def main():
    out = []
    manifest = []
    out.append("# Automated Diabetic Retinopathy Diagnosis via Fundus Image "
               "Enhancement and CNN Classification")
    out.append("")
    out.append(f"> **Intermediate EN assembly — {date.today()}.** Concatenation of "
               "approved PART 1 draft bodies in Table-of-Contents order. Working "
               "author-year citations are unconverted (GOST `[N]` is a deferred "
               "single Stage-G pass). Compliance checklists, draft headers, and "
               "word-count blocks are excluded. NOT the final bound thesis: "
               "experiment-gated chapters (most of Ch 4, Ch 5) and front/back "
               "matter (Ch 0, Ch 7) are absent. Chapters 1, 2, 3, 6 + §4.1 are "
               "content-complete (§2.4.2 consolidated into §2.4.1; §2.3.3 drafted "
               "2026-06-16).")
    out.append("")
    total_words = 0
    for cdir, heading in CHAPTERS:
        d = CH_ROOT / cdir / "drafts"
        files = sorted(d.glob("*-draft.md"), key=section_key)
        if not files:
            continue
        out.append("\n---\n")
        out.append(f"# {heading}")
        out.append("")
        for f in files:
            title, text, words = extract(f)
            total_words += words
            manifest.append((f.name, words))
            out.append(text if title in text else f"{title}\n\n{text}")
            out.append("")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"WROTE {OUT}")
    print(f"Sections: {len(manifest)} | Total PART-1 words: {total_words:,}")
    print("\n# file -> words")
    for name, w in manifest:
        print(f"  {name:28s} {w:6,d}")


if __name__ == "__main__":
    main()
