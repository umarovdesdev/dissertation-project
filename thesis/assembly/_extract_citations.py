#!/usr/bin/env python3
"""Stage-G helper #1: extract every in-text author-year citation from the
assembled manuscript, in reading order, and list the DISTINCT (author-phrase,
year) tokens by first appearance. Output drives the manual token->card->[N]
mapping (see _apply_citations.py)."""
from __future__ import annotations
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent / "DISSERTATION_EN_partial_2026-06-16.md"
OUT = Path(__file__).resolve().parent / "_citations_extracted.txt"
text = SRC.read_text(encoding="utf-8")

# Scan running text only: start at the first chapter heading (drops the leading
# metadata blockquote, which else yields a false '(... 2026-...)' token).
ci = text.find("# 1 PROBLEM DOMAIN")
if ci > 0:
    text = text[ci:]

YEAR = r"(?:19|20)\d{2}[a-z]?"

# --- Narrative: "Name ... (YYYY)" — author phrase immediately before (YYYY) ---
# author phrase = run of Capitalized words / connectors / 'et al.' ending right before '('
narr = re.compile(
    r"([A-Z][A-Za-z'’\-]+(?:\s+(?:and|&|et\s+al\.?|[A-Z][A-Za-z'’\-]+|[A-Z]\.))*?)\s\((" + YEAR + r")\)"
)
# --- Parenthetical: "(... Author ..., YYYY[; ...])" — group has letters + year ---
paren = re.compile(r"\(([^()]*?[A-Za-z][^()]*?(?:19|20)\d{2}[a-z]?[^()]*?)\)")

events = []  # (pos, raw, author_phrase, year)

for m in narr.finditer(text):
    author = re.sub(r"\s+", " ", m.group(1)).strip().strip(",")
    events.append((m.start(), m.group(0), author, m.group(2)))

for m in paren.finditer(text):
    inner = m.group(1)
    # skip pure-year groups (those are the year-part of a narrative cite)
    if not re.search(r"[A-Za-z]", re.sub(YEAR, "", inner)):
        continue
    # split multi-source on ';'
    for part in inner.split(";"):
        part = part.strip()
        ym = re.search(r"(" + YEAR + r")", part)
        if not ym:
            continue
        author = part[:ym.start()].strip().strip(",").strip()
        if not author:
            continue
        events.append((m.start(), "(" + part + ")", author, ym.group(1)))

events.sort(key=lambda e: e[0])

STOP = {"and", "the", "in", "of", "by", "et", "al"}

def key(author, year):
    a = author.lower().replace("&", "and")
    a = re.sub(r"\bet al\.?\b", "", a)
    a = re.sub(r"[^a-z\s]", " ", a)
    a = re.sub(r"\s+", " ", a).strip()
    surnames = [w for w in a.split() if len(w) > 1 and w not in STOP]
    joined = "-".join(surnames) if surnames else a
    return f"{joined}|{year[:4]}"

seen = {}
order = []
for pos, raw, author, year in events:
    k = key(author, year)
    if k not in seen:
        line = text[:pos].count("\n") + 1
        seen[k] = {"key": k, "first_line": line, "first_raw": raw,
                   "author": author, "year": year, "count": 0, "variants": set()}
        order.append(k)
    seen[k]["count"] += 1
    seen[k]["variants"].add(author)

lines = [f"DISTINCT citation tokens: {len(order)}\n"]
for i, k in enumerate(order, 1):
    e = seen[k]
    lines.append(f"{i:3d}. [{k:34s}] L{e['first_line']:<5d} x{e['count']:<3d} "
                 f"first={e['first_raw'][:48]!r}")
    if len(e["variants"]) > 1:
        lines.append(f"       variants: {' | '.join(sorted(e['variants']))}")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"WROTE {OUT}  ({len(order)} distinct tokens)")
