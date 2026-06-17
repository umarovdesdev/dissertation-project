#!/usr/bin/env python3
"""Assemble the intermediate KZ manuscript from approved translation bodies.

Mirror of `_assemble_en.py` for the Kazakh translations under
`chapters/**/translations/*-translation.md`. For each file it keeps the
`# §x Title` line plus the **1-БӨЛІК: БӨЛІМ МӘТІНІ** body only, dropping the
`> Қазақ тіліндегі аударма…` blockquote and the trailing `### Аудармашы ескертуі`
note. Files are ordered by parsed section number (`X.C` conclusions and appendix
letters sort last); chapters concatenated in Table-of-Contents order
(outline/TABLE_OF_CONTENTS_KZ.md). Working author-year citations are left
unconverted (GOST `[N]` is a deferred single pass on the final manuscript).
This is a reversible, read-only-source operation.
"""
from __future__ import annotations
import re
from pathlib import Path
from datetime import date

CH_ROOT = Path(__file__).resolve().parent.parent / "chapters"
OUT = Path(__file__).resolve().parent / f"DISSERTATION_KZ_partial_{date.today()}.md"

# Chapter dir -> TOC chapter heading (KZ). Only chapters with approved translations.
CHAPTERS = [
    ("01-problem-domain",
     "1 ДИАБЕТТІК РЕТИНОПАТИЯНЫ АВТОМАТТАНДЫРЫЛҒАН ДИАГНОСТИКАЛАУДЫҢ "
     "ПРОБЛЕМАЛЫҚ САЛАСЫН ТАЛДАУ ЖӘНЕ ҚАЗІРГІ ЖАЙ-КҮЙІ"),
    ("02-theoretical-foundations",
     "2 FUNDUS IMAGE ТАЛДАУЫ ҮШІН IMAGE PREPROCESSING ЖӘНЕ DEEP LEARNING "
     "ТЕОРИЯЛЫҚ НЕГІЗДЕРІ"),
    ("03-methodology",
     "3 ИНТЕГРАЦИЯЛАНҒАН PREPROCESSING-CNN PIPELINE ЖОБАЛАУ ӘДІСТЕМЕСІ"),
    ("04-experiments",
     "4 ЭКСПЕРИМЕНТТІК ЗЕРТТЕУ — PREPROCESSING-ТІҢ CNN ДИАГНОСТИКАЛЫҚ "
     "ӨНІМДІЛІГІНЕ ӘСЕРІ"),
    ("06-system-architecture",
     "6 РЕСУРСТАРЫ ШЕКТЕУЛІ ОРТАҒА АРНАЛҒАН DR АВТОМАТТАНДЫРЫЛҒАН СКРИНИНГ "
     "ЖҮЙЕСІНІҢ АРХИТЕКТУРАСЫ"),
    ("08-appendices", "ҚОСЫМШАЛАР"),
]

# body ends at the translator note or a PART-2/PART-3 style block
BODY_END = re.compile(r"^(### Аудармашы ескертуі|## 2-БӨЛІК|## PART [23]\b|## 3-БӨЛІК)", re.I)
PART1_HDR = re.compile(r"^## 1-БӨЛІК\b", re.I)


def section_key(p: Path):
    stem = p.name.replace("-translation.md", "")
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
    try:
        i = next(idx for idx, l in enumerate(lines) if PART1_HDR.match(l))
    except StopIteration:
        return title, "", 0
    body = []
    for l in lines[i + 1:]:
        if BODY_END.match(l):
            break
        body.append(l)
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
    out.append("# Көз түбі кескінін жақсарту және CNN жіктеуі арқылы диабеттік "
               "ретинопатияны автоматтандырылған диагностикалау")
    out.append("")
    out.append(f"> **Аралық қазақ тіліндегі жинақ — {date.today()}.** Бекітілген "
               "аудармалардың 1-БӨЛІК мәтіндерін Мазмұн ретімен біріктіру. Жұмыстық "
               "автор-жыл дәйексөздері түрлендірілмеген (GOST `[N]` — түпкі жинақтаудағы "
               "жалғыз шегерілген өту). Аудармашы ескертулері, аударма тақырыпшалары мен "
               "тексеру тізімдері қосылмаған. Бұл — түпкі түптелген диссертация ЕМЕС: "
               "эксперимент-шартты тараулар (4-тараудың көп бөлігі, 5-тарау) мен "
               "алғы/соңғы материал (0-тарау, 7-тарау) жоқ. 1, 2, 3, 6-тараулар + §4.1 "
               "мазмұны толық.")
    out.append("")
    total_words = 0
    for cdir, heading in CHAPTERS:
        d = CH_ROOT / cdir / "translations"
        files = sorted(d.glob("*-translation.md"), key=section_key)
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
    # ASCII-safe stdout (Windows console may be cp1251 and cannot encode Cyrillic)
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(f"WROTE {OUT}")
    print(f"Sections: {len(manifest)} | Total PART-1 (1-BOLIK) words: {total_words:,}")
    print("\n# file -> words")
    for name, w in manifest:
        print(f"  {name:28s} {w:6,d}")


if __name__ == "__main__":
    main()
