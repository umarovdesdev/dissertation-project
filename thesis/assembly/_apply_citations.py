#!/usr/bin/env python3
"""Stage-G PREVIEW: convert working author-year citations in the assembled
manuscript to GOST numbered [N] form (by first appearance), build the
List of references used, and emit a resolution + QA report.

PREVIEW ONLY — numbers are provisional (more chapters will shift them); rendered
to separate files; working drafts keep author-year. External sources are
converted; self-citations (#19-#24), uncarded (#52/#53), and Appendix-D
publication records are LEFT as author-year and flagged for the final pass.
"""
from __future__ import annotations
import re
from pathlib import Path
from datetime import date

HERE = Path(__file__).resolve().parent
SRC = HERE / "DISSERTATION_EN_partial_2026-06-16.md"
BIB = HERE / "_card_bib.tsv"
OUT_MS = HERE / f"DISSERTATION_EN_preview_GOST_{date.today()}.md"
OUT_QA = HERE / "_citation_resolution.md"

YEAR = r"(?:19|20)\d{2}[a-z]?"
STOP = {"and", "the", "in", "of", "by", "et", "al"}

def key(author, year):
    a = author.lower().replace("&", "and")
    a = re.sub(r"\bet al\.?\b", "", a)
    a = re.sub(r"[^a-z\s]", " ", a)
    a = re.sub(r"\s+", " ", a).strip()
    surnames = [w for w in a.split() if len(w) > 1 and w not in STOP]
    joined = "-".join(surnames) if surnames else a
    return f"{joined}|{year[:4]}"

# --- token key -> card filename (external, resolvable). Co-author/variant keys
#     collapse to the same card; MULTI splits a combined "(…, 2015, 2016)" cite.
K2C = {
 "kusuhara|2018":"kusuhara-2018.md","morya|2024":"morya-2024.md",
 "wang-lo|2018":"wang-lo-2018.md","gettinger|2025":"gettinger-2025.md",
 "kesharwani|2021":"kesharwani-2021.md","porwal|2018":"porwal-2018-idrid-dataset.md",
 "shen|2020":"shen-2020-cofe-net.md","fu|2020":"fu-2020-eyeq-riqa.md",
 "zago|2018":"zago-2018-riqa.md","dai|2021":"dai-2021-deepdr.md",
 "rakhlin|2017":"rakhlin-2017.md","voets|2019":"voets-2019.md",
 "gulshan|2016":"gulshan-2016.md","beede|2020":"beede-2020-human-centered-dr.md",
 "liu|2022":"liu-2022.md","zhou|2022":"zhou-2022-domain-generalization-survey.md",
 "wang-deng|2018":"wang-2018-deep-visual-domain-adaptation-survey.md",
 "litjens|2017":"litjens-2017-medical-dl-survey.md","krizhevsky|2012":"krizhevsky-2012-alexnet.md",
 "simonyan-zisserman|2015":"simonyan-2015-vgg.md",
 "szegedy|2015":"MULTI:szegedy-2015-googlenet.md,szegedy-2016-inception-v3.md",
 "he|2016":"he-2016-deep-residual-learning.md","huang|2017":"huang-2017-densenet.md",
 "tan-le|2019":"tan-2019-efficientnet.md","tan-le|2021":"tan-2021-efficientnetv2.md",
 "pratt|2016":"pratt-2016.md","xu|2024":"xu-2024-hybrid.md",
 "gargeya-leng|2017":"gargeya-2017-automated-dr.md","quellec|2017":"quellec-2017-deep-image-mining.md",
 "arora|2024":"arora-2024-efficientnet.md","sharma|2025":"sharma-2025-vit-capsule.md",
 "wan|2021":"wan-2021-ead-net.md","zhou|2020":"zhou-2020-fgadr-benchmark.md",
 "khosravi|2025":"khosravi-2025.md","ryu|2021":"ryu-2021-octa.md",
 "esteva|2017":"esteva-2017-skin-cancer.md","burlina|2017":"burlina-2017-amd-dcnn.md",
 "dosovitskiy|2021":"dosovitskiy-2021-vision-transformer.md","goh|2024":"goh-2024-vit-vs-cnn.md",
 "liu|2021":"liu-2021-swin-transformer.md","geetha-hema|2026":"geetha-hema-2026.md",
 "saxena|2020":"saxena-2020.md","cheplygina|2018":"cheplygina-2018-not-so-supervised-survey.md",
 "zhou|2023":"zhou-2023-retfound.md","azizi|2021":"azizi-2021-micle.md",
 "tjoa-guan|2020":"tjoa-2020-xai-survey.md","samek|2017":"samek-2017-explainable-ai.md",
 "zhou|2016":"zhou-2016-cam.md","selvaraju|2017":"selvaraju-2017-grad-cam.md",
 "chattopadhyay|2018":"chattopadhyay-2018-grad-cam-plus-plus.md",
 "lundberg-lee|2017":"lundberg-2017-shap.md","ribeiro|2016":"ribeiro-2016-lime.md",
 "abr-moff|2018":"abramoff-2018-clinical-ai-validation.md","ting|2017":"ting-2017.md",
 "bellemo|2019":"bellemo-2019-ai-dr-africa.md","zhang|2022":"zhang-2022-multicentre.md",
 "ruamviboonsuk|2022":"ruamviboonsuk-2022.md","nchez-guti-rrez|2022":"sanchez-gutierrez-2022.md",
 "baget-bernaldiz|2021":"baget-bernaldiz-2021.md","wewetzer|2021":"wewetzer-2021.md",
 "senapati|2024":"senapati-2024.md","ting|2019":"ting-2019-dl-ophthalmology-review.md",
 "de-fauw|2018":"defauw-2018-retinal-oct.md","pizer|1987":"pizer-1987-adaptive-histogram-equalization.md",
 "zuiderveld|1994":"zuiderveld-1994-clahe.md","hayati|2023":"hayati-2023.md",
 "shaout-han|2025":"shaout-han-2025.md","chakka|2023":"chakka-2023.md",
 "tomasi-manduchi|1998":"tomasi-1998-bilateral-filtering.md","morel|2011":"buades-2011-non-local-means.md",
 "sun|2016":"he-2016-deep-residual-learning.md","weinberger|2017":"huang-2017-densenet.md",
 "cui|2019":"cui-2019-class-balanced-loss.md","chairi|2024":"araf-2024.md",
 "lin|2017":"lin-2017-focal-loss.md","srivastava|2014":"srivastava-2014-dropout.md",
 "ioffe-szegedy|2015":"ioffe-2015-batch-normalization.md",
 "shorten-khoshgoftaar|2019":"shorten-2019-augmentation-survey.md",
 "zhang|2018":"zhang-2018-mixup.md","cubuk|2020":"cubuk-2020-randaugment.md",
 "buda|2018":"buda-2018-class-imbalance.md","pan-yang|2010":"pan-2010-transfer-learning-survey.md",
 "lipson|2014":"yosinski-2014-transferability-features.md","le|2019":"tan-2019-efficientnet.md",
 "pluim|2018":"cheplygina-2018-not-so-supervised-survey.md","arrieta|2022":"arrieta-2022.md",
 "yosinski|2014":"yosinski-2014-transferability-features.md","kornblith|2019":"kornblith-2019-transferability.md",
 "ganin|2016":"ganin-2016-dann.md","shurrab-duwairi|2022":"shurrab-2022-ssl-medical-survey.md",
 "chen|2020":"chen-2020-simclr.md","he|2020":"he-2020-moco.md","grill|2020":"grill-2020-byol.md",
 "chen-he|2021":"chen-2021-simsiam.md","caron|2021":"caron-2021-dino.md","he|2022":"he-2022-mae.md",
 "everingham|2010":"everingham-2010-pascal-voc.md","rezatofighi|2019":"rezatofighi-2019-giou.md",
 "szegedy|2016":"szegedy-2016-inception-v3.md","araf|2024":"araf-2024.md",
 "buda-maki-mazurowski|2018":"buda-2018-class-imbalance.md","krause|2018":"krause-2018-grader-variability.md",
 "kingma-ba|2015":"kingma-2015-adam.md","cuadros-bresnick|2009":"cuadros-2009-eyepacs.md",
 "cuadros|2009":"cuadros-2009-eyepacs.md","decenci-re|2014":"decenciere-2014-messidor.md",
 "nandal|2024":"nandal-2024.md",
 # #52/#53 cards written 2026-06-16 — now resolvable (incl. prose-artifact forms)
 "guo|2017":"guo-2017-calibration.md","after-guo|2017":"guo-2017-calibration.md",
 "wang|2004":"wang-2004-ssim.md","after-wang|2004":"wang-2004-ssim.md",
 "property-image-quality-analysis-measures-via-ssim-after-wang|2004":"wang-2004-ssim.md",
 # "Hinton (2012)" = extractor truncation of "Krizhevsky, Sutskever, and Hinton (2012)" = AlexNet
 "hinton|2012":"krizhevsky-2012-alexnet.md",
}
SELF = {"yesmukhamedov|2025","yesmukhamedov-sapakov|2025",
        "sapakova-yesmukhamedov-sapakov|2025","sapakova|2025",
        "modeling-study-reported-herald-kazutb|2024"}
UNCARDED = {}  # (none) — #52/#53 carded; "Hinton (2012)" resolved to AlexNet [Krizhevsky 2012]
APPD = {"yemberdiyeva-kozhamkulova|2025","ds|2025","daniyarova-armankyzy|2025",
        "emberdieva-kaldybaeva|2024","haddad-daniyarova|2025","lc-altimemy|2021","procedia-ds|2025"}

text = SRC.read_text(encoding="utf-8")
ci = text.find("# 1 PROBLEM DOMAIN")
head, body = text[:ci], text[ci:]

# ---------- PASS 1: assign [N] to cards by first appearance ----------
order_events = []
narr = re.compile(r"([A-Z][A-Za-z'’\-]+(?:\s+(?:and|&|et\s+al\.?|[A-Z][A-Za-z'’\-]+|[A-Z]\.))*?)\s\((" + YEAR + r")\)")
paren = re.compile(r"\(([^()]*?[A-Za-z][^()]*?(?:19|20)\d{2}[a-z]?[^()]*?)\)")
for m in narr.finditer(body):
    order_events.append((m.start(), key(re.sub(r"\s+"," ",m.group(1)).strip().strip(","), m.group(2))))
for m in paren.finditer(body):
    inner = m.group(1)
    if not re.search(r"[A-Za-z]", re.sub(YEAR, "", inner)):
        continue
    for part in inner.split(";"):
        ym = re.search(r"("+YEAR+r")", part)
        if ym and part[:ym.start()].strip().strip(",").strip():
            order_events.append((m.start(), key(part[:ym.start()].strip().strip(","), ym.group(1))))
order_events.sort(key=lambda e: e[0])

cardN, N = {}, 0
def assign(card):
    global N
    if card not in cardN:
        N += 1
        cardN[card] = N
for pos, k in order_events:
    v = K2C.get(k)
    if not v:
        continue
    if v.startswith("MULTI:"):
        for c in v[6:].split(","):
            assign(c)
    else:
        assign(v)

def num_for(k):
    v = K2C.get(k)
    if not v:
        return None
    if v.startswith("MULTI:"):
        return ", ".join(str(cardN[c]) for c in v[6:].split(","))
    return str(cardN[v])

# ---------- PASS 2: replace in text ----------
PAGE = re.compile(r",?\s*(p{1,2}\.\s*[\dIVxiv–\-]+)\s*$", re.I)
def repl_paren(m):
    inner = m.group(1)
    if not re.search(r"[A-Za-z]", re.sub(YEAR, "", inner)):
        return m.group(0)
    nums, leftovers = [], []
    for part in inner.split(";"):
        ym = re.search(r"("+YEAR+r")", part)
        author = part[:ym.start()].strip().strip(",").strip() if ym else ""
        if not ym or not author:
            leftovers.append(part.strip()); continue
        tail = part[ym.end():]
        pg = PAGE.search(part)
        k = key(author, ym.group(1))
        nn = num_for(k)
        if nn is None:
            leftovers.append(part.strip())
        else:
            nums.append(nn + (", " + pg.group(1) if pg else ""))
    if not nums:
        return m.group(0)
    out = "[" + ", ".join(nums) + "]"
    if leftovers:
        out += " (" + "; ".join(leftovers) + ")"
    return out
def repl_narr(m):
    nm, yr = m.group(1), m.group(2)
    nn = num_for(key(re.sub(r"\s+"," ",nm).strip().strip(","), yr))
    return f"{nm} [{nn}]" if nn is not None else m.group(0)

conv = paren.sub(repl_paren, body)
conv = narr.sub(repl_narr, conv)

# ---------- reference list (cards in [N] order, APA from bib) ----------
bib = {}
for ln in BIB.read_text(encoding="utf-8").splitlines():
    p = ln.split("\t")
    if len(p) >= 2:
        bib[p[0]] = re.sub(r"\[https?://[^\]]+\]\([^)]+\)", lambda x: x.group(0).split("]")[0][1:], p[1])
inv = {v: k for k, v in cardN.items()}
refs = []
for n in range(1, N + 1):
    card = inv[n]
    cite = bib.get(card, "[card not found]")
    cite = re.sub(r"\*", "", cite)  # drop md emphasis
    refs.append(f"{n}. {cite}")

# ---------- write converted manuscript ----------
hdr = (f"# Automated Diabetic Retinopathy Diagnosis — EN preview with GOST [N] citations\n\n"
       f"> **STAGE-G PREVIEW — {date.today()}.** Author-year → numbered [N] (by first "
       f"appearance) on the intermediate assembly. **Provisional:** numbers WILL change "
       f"when experiment-gated chapters are added; the working drafts keep author-year. "
       f"External sources converted ({N} numbered). LEFT as author-year & flagged: "
       f"self-citations (#19–#24, per-section disambiguation), uncarded #52/#53, and "
       f"Appendix-D publication records. See `_citation_resolution.md` for the table + QA.\n")
OUT_MS.write_text(hdr + "\n" + conv +
                  "\n\n---\n\n# LIST OF REFERENCES USED (preview, in order of appearance)\n\n"
                  "> APA-derived; final GOST 7.1-2003 punctuation applied at final assembly.\n\n"
                  + "\n".join(refs) + "\n", encoding="utf-8")
print(f"WROTE {OUT_MS.name} | external sources numbered: {N}")
print(f"   replacements: paren+narr applied; refs listed 1..{N}")

# ---------- resolution + QA report ----------
# distinct keys in first-appearance order, with counts
kcount, korder = {}, []
for _, k in order_events:
    if k not in kcount:
        korder.append(k); kcount[k] = 0
    kcount[k] += 1

rows, collapses, selfs, uncarded, appd, unresolved = [], [], [], [], [], []
card_first_key = {}
for k in korder:
    v = K2C.get(k)
    if v and v.startswith("MULTI:"):
        cards = v[6:].split(",")
        nn = ", ".join(str(cardN[c]) for c in cards)
        rows.append((k, nn, "+".join(cards), kcount[k]))
        continue
    if v:
        n = cardN[v]
        first = card_first_key.setdefault(v, k)
        rows.append((k, str(n), v + ("  ⟲collapse→"+first if first != k else ""), kcount[k]))
        if first != k:
            collapses.append((k, first, n, v))
        continue
    if k in SELF:
        selfs.append((k, kcount[k])); rows.append((k, "SELF", "#19–#24 (author-year kept)", kcount[k])); continue
    if k in UNCARDED:
        uncarded.append((k, UNCARDED[k], kcount[k])); rows.append((k, "UNCARDED", UNCARDED[k], kcount[k])); continue
    if k in APPD:
        appd.append((k, kcount[k])); rows.append((k, "APP-D", "publication record (not in ref list)", kcount[k])); continue
    unresolved.append((k, kcount[k])); rows.append((k, "??", "UNRESOLVED", kcount[k]))

cited_cards = set(cardN)
all_ext = {c for c in bib if c not in {  # exclude self + non-citable
    "yesmukhamedov-conf.md","yesmukhamedov-kazutb.md","yesmukhamedov-kbtu.md",
    "yesmukhamedov-nan-rk.md","yesmukhamedov-scopus-q2.md","yesmukhamedov-scopus-q3.md",
    "wikipedia-clahe.md"}}
uncited = sorted(all_ext - cited_cards)

q = [f"# Stage-G citation conversion — resolution & QA (PREVIEW {date.today()})\n",
     f"Source: `{SRC.name}` (intermediate assembly, Ch 1/2/3/6 + §4.1 + App A/D).",
     f"Converted manuscript + reference list: `{OUT_MS.name}`.\n",
     "**PREVIEW caveat:** numbers are by first appearance in this *partial* manuscript and",
     "will change when experiment-gated chapters are added. Run once, for real, at final assembly.\n",
     "## Summary",
     f"- Distinct external sources numbered: **{N}**  |  Highest [N]: **{N}**",
     f"- Distinct in-text citation tokens detected: **{len(korder)}**",
     f"- Self-citation tokens (left author-year): **{len(selfs)}**  |  Appendix-D records: **{len(appd)}**",
     f"- Cited-but-UNCARDED / ambiguous (blocking): **{len(uncarded)}** ({', '.join(k for k,_,_ in uncarded) or 'none'})",
     f"- Carded-but-uncited in this partial set (informational): **{len(uncited)}**",
     f"- Unresolved: **{len(unresolved)}**\n",
     "## ⚠ Cited-but-uncarded (BLOCKING at final assembly)"]
for k, why, c in uncarded:
    q.append(f"- `{k}` ×{c} → {why}")
q += ["\n## Self-citations (#19–#24) — left as author-year, disambiguate per section at final assembly",
      "Same surface form maps to different self-papers by section (Sources headers): "
      "#19 conf / #21 kbtu (one experiment), #20 kazutb (thermal), #22 nan-rk (architecture), "
      "#23 scopus-q2 ≡ #24 scopus-q3 (one EEJET article — SIR-5 collapse). GOST numbers self "
      "identically to others; SIR-4 framing in prose is preserved."]
for k, c in selfs:
    q.append(f"- `{k}` ×{c}")
q += ["\n## Appendix-D publication records — excluded from 'List of references used'",
      "These are the candidate's own publication-table entries / co-authors in App D "
      "(approbation record, not running-text literature citations); `LC-AlTimemy-2021` is the "
      "known scopus-q2 ID anomaly."]
for k, c in appd:
    q.append(f"- `{k}` ×{c}")
q.append("\n## Collapses (variant / co-author surnames → one source)")
for k, first, n, v in collapses:
    q.append(f"- `{k}` → [{n}] (same source as `{first}` → {v})")
q.append("\n## Carded-but-uncited in this partial manuscript (informational — expected; cited in undrafted Ch 4/5/0/7)")
q.append(", ".join(uncited))
q.append("\n## Full resolution table (token → [N]/status → card, ×count, first-appearance order)")
for i, (k, nn, card, c) in enumerate(rows, 1):
    q.append(f"{i:3d}. `{k}`  →  {nn}  ←  {card}  ×{c}")
OUT_QA.write_text("\n".join(q), encoding="utf-8")
print(f"WROTE {OUT_QA.name} | tokens={len(korder)} uncited={len(uncited)} unresolved={len(unresolved)}")
