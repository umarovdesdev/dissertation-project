#!/usr/bin/env python3
"""Stage-G FINAL pass: convert working author-year citations to GOST numbered
[N] form on BOTH the EN and KZ assembled manuscripts (2026-06-17), with ONE
shared numbering, and build the "List of references used" in each language.

Per thesis/prompts/citation-assembly.md:
  * Numbering is assigned ONCE, by first appearance in the EN manuscript
    (GOST 7.32-2001 §6.11) -> authoritative card -> [N] map.
  * The SAME map is applied to KZ (rule #7, language invariance). KZ keeps Latin
    author surnames but uses Kazakh connectors ("X және әріптестері(нің/не/нен)"
    = et al., "X пен/мен Y" = "X and Y") and the Kazakh page form "699-б.".
  * Resolution is surname-based and language-agnostic: surnames_of() strips every
    non-[a-z] char (so accents AND all Cyrillic connectors fall away), then
    resolve() tries candidate keys full-join -> first-author -> pairs -> singles,
    matching the literature-card map. This handles comma lists, "et al.", accented
    names (González-Díaz), and Kazakh declensions uniformly.
  * Self-citations (#19-24, Cyrillic in KZ / SELF-set in EN) and Appendix-D
    publication records resolve to no external card and are LEFT author-year
    (SIR-4 prose framing preserved); flagged for manual per-section disambiguation.

Outputs (thesis/assembly/): DISSERTATION_EN_GOST_<date>.md,
DISSERTATION_KZ_GOST_<date>.md, _citation_resolution_final_<date>.md
"""
from __future__ import annotations
import re, sys, unicodedata
from pathlib import Path
from datetime import date

HERE = Path(__file__).resolve().parent
SRC_EN = HERE / "DISSERTATION_EN_partial_2026-06-17.md"
SRC_KZ = HERE / "DISSERTATION_KZ_partial_2026-06-17.md"
BIB = HERE / "_card_bib.tsv"
OUT_EN = HERE / f"DISSERTATION_EN_GOST_{date.today()}.md"
OUT_KZ = HERE / f"DISSERTATION_KZ_GOST_{date.today()}.md"
OUT_QA = HERE / f"_citation_resolution_final_{date.today()}.md"

YEAR = r"(?:19|20)\d{2}[a-z]?"
STOP = {"and", "the", "in", "of", "by", "et", "al"}

# token key -> card filename (external). MULTI splits a combined "(…, 2015, 2016)".
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
 "sanchez-gutierrez|2022":"sanchez-gutierrez-2022.md",
 "baget-bernaldiz|2021":"baget-bernaldiz-2021.md","wewetzer|2021":"wewetzer-2021.md",
 "senapati|2024":"senapati-2024.md","ting|2019":"ting-2019-dl-ophthalmology-review.md",
 "de-fauw|2018":"defauw-2018-retinal-oct.md","fauw|2018":"defauw-2018-retinal-oct.md",
 "pizer|1987":"pizer-1987-adaptive-histogram-equalization.md",
 "zuiderveld|1994":"zuiderveld-1994-clahe.md","hayati|2023":"hayati-2023.md",
 "shaout-han|2025":"shaout-han-2025.md","shaout|2025":"shaout-han-2025.md","chakka|2023":"chakka-2023.md",
 "tomasi-manduchi|1998":"tomasi-1998-bilateral-filtering.md","tomasi|1998":"tomasi-1998-bilateral-filtering.md",
 "morel|2011":"buades-2011-non-local-means.md","buades|2011":"buades-2011-non-local-means.md",
 "sun|2016":"he-2016-deep-residual-learning.md","weinberger|2017":"huang-2017-densenet.md",
 "cui|2019":"cui-2019-class-balanced-loss.md","chairi|2024":"araf-2024.md","araf|2024":"araf-2024.md",
 "lin|2017":"lin-2017-focal-loss.md","srivastava|2014":"srivastava-2014-dropout.md",
 "ioffe-szegedy|2015":"ioffe-2015-batch-normalization.md","ioffe|2015":"ioffe-2015-batch-normalization.md",
 "shorten-khoshgoftaar|2019":"shorten-2019-augmentation-survey.md",
 "shorten|2019":"shorten-2019-augmentation-survey.md",
 "zhang|2018":"zhang-2018-mixup.md","cubuk|2020":"cubuk-2020-randaugment.md",
 "buda|2018":"buda-2018-class-imbalance.md","pan-yang|2010":"pan-2010-transfer-learning-survey.md",
 "pan|2010":"pan-2010-transfer-learning-survey.md",
 "lipson|2014":"yosinski-2014-transferability-features.md","yosinski|2014":"yosinski-2014-transferability-features.md",
 "le|2019":"tan-2019-efficientnet.md",
 "pluim|2018":"cheplygina-2018-not-so-supervised-survey.md","arrieta|2022":"arrieta-2022.md",
 "kornblith|2019":"kornblith-2019-transferability.md",
 "ganin|2016":"ganin-2016-dann.md","shurrab-duwairi|2022":"shurrab-2022-ssl-medical-survey.md",
 "shurrab|2022":"shurrab-2022-ssl-medical-survey.md",
 "chen|2020":"chen-2020-simclr.md","he|2020":"he-2020-moco.md","grill|2020":"grill-2020-byol.md",
 "chen-he|2021":"chen-2021-simsiam.md","caron|2021":"caron-2021-dino.md","he|2022":"he-2022-mae.md",
 "everingham|2010":"everingham-2010-pascal-voc.md","rezatofighi|2019":"rezatofighi-2019-giou.md",
 "szegedy|2016":"szegedy-2016-inception-v3.md",
 "buda-maki-mazurowski|2018":"buda-2018-class-imbalance.md","krause|2018":"krause-2018-grader-variability.md",
 "kingma-ba|2015":"kingma-2015-adam.md","kingma|2015":"kingma-2015-adam.md",
 "cuadros-bresnick|2009":"cuadros-2009-eyepacs.md","cuadros|2009":"cuadros-2009-eyepacs.md",
 "decenci-re|2014":"decenciere-2014-messidor.md","decenciere|2014":"decenciere-2014-messidor.md",
 "nandal|2024":"nandal-2024.md","guo|2017":"guo-2017-calibration.md","wang|2004":"wang-2004-ssim.md",
 "hinton|2012":"krizhevsky-2012-alexnet.md","gonzalez-diaz|2024":"gonzalez-diaz-2024.md",
 "abramoff|2018":"abramoff-2018-clinical-ai-validation.md",
}
SELF_SUR = {"yesmukhamedov", "sapakova", "sapakov", "kazutb"}  # candidate's own work -> keep author-year
APPD_SUR = {"yemberdiyeva", "kozhamkulova", "daniyarova", "armankyzy", "emberdieva",
            "kaldybaeva", "haddad", "altimemy", "procedia", "ds", "istanbul"}

# ---- surname extraction (language-agnostic: folds accents to ASCII, drops Cyrillic) ----
def surnames_of(author: str):
    a = unicodedata.normalize("NFKD", author)  # González -> Gonzalez, Abràmoff -> Abramoff
    a = "".join(c for c in a if not unicodedata.combining(c)).lower().replace("&", " and ")
    a = re.sub(r"\bet al\.?\b", " ", a)
    a = re.sub(r"[^a-z\s]", " ", a)
    a = re.sub(r"\s+", " ", a).strip()
    return [w for w in a.split() if len(w) > 1 and w not in STOP]


def resolve(author: str, year: str):
    """Return K2C value (card or 'MULTI:...') or None, by candidate-key priority."""
    sl = surnames_of(author)
    if not sl:
        return None
    y = year[:4]
    cands = ["-".join(sl), sl[0]]
    cands += [f"{sl[i]}-{sl[i+1]}" for i in range(len(sl) - 1)]
    cands += sl
    for c in cands:
        v = K2C.get(f"{c}|{y}")
        if v:
            return v
    return None


def classify(author: str):
    sl = set(surnames_of(author))
    if sl & SELF_SUR:
        return "self"
    if sl & APPD_SUR:
        return "appd"
    return "unknown"


# ---- regexes -------------------------------------------------------------
SUR = r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÿ'’\-]+"
INIT = r"[A-Z]\."
KZC = r"(?:және\s+әріптестер[Ѐ-ӿ]*|әріптестер[Ѐ-ӿ]*|және|пен|мен|бен|т\.б\.)"
SEP = r"(?:\s*,\s*|\s+&\s+|\s+and\s+|\s+et\s+al\.?\s*|\s+" + KZC + r"\s*)"
TAIL = r"(?:\s+et\s+al\.?|\s+" + KZC + r")?"
AUTHORS = SUR + r"(?:" + SEP + r"(?:" + SUR + r"|" + INIT + r"))*" + TAIL
# narrative: author block + "(year[, page])"
NARR = re.compile(r"(" + AUTHORS + r")\s*\((" + YEAR + r")((?:,\s*[^)]*)?)\)")
# parenthetical: requires a Latin letter + a 4-digit year inside
PAREN = re.compile(r"\(([^()]*?[A-Za-z][^()]*?(?:19|20)\d{2}[a-z]?[^()]*?)\)")
# page tail inside a citation: "p. 370" / "pp. 79-88" (EN) or "699-б." / "699 б." (KZ)
PAGE = re.compile(r"((?:p{1,2}\.\s*[\dIVxiv–\-]+)|(?:\d+\s*-?\s*б\.))\s*$", re.I)


def split_body(path: Path):
    text = path.read_text(encoding="utf-8")
    i = re.search(r"(?m)^# 1 ", text).start()
    return text[:i], text[i:]


# ---------- PASS 1: assign [N] from EN, by first appearance ----------
head_en, body_en = split_body(SRC_EN)
events = []  # (pos, K2C-value)
for m in NARR.finditer(body_en):
    v = resolve(m.group(1), m.group(2))
    if v:
        events.append((m.start(), v))
for m in PAREN.finditer(body_en):
    inner = m.group(1)
    if not re.search(r"[A-Za-z]", re.sub(YEAR, "", inner)):
        continue
    for part in inner.split(";"):
        ym = re.search(r"(" + YEAR + r")", part)
        author = part[:ym.start()].strip().strip(",").strip() if ym else ""
        if ym and author:
            v = resolve(author, ym.group(1))
            if v:
                events.append((m.start(), v))
events.sort(key=lambda e: e[0])

cardN, N = {}, 0
def assign(card):
    global N
    if card not in cardN:
        N += 1
        cardN[card] = N
for _, v in events:
    if v.startswith("MULTI:"):
        for c in v[6:].split(","):
            assign(c)
    else:
        assign(v)


def value_to_nums(v):
    if v.startswith("MULTI:"):
        return ", ".join(str(cardN[c]) for c in v[6:].split(","))
    return str(cardN[v])


# ---------- replacement (shared by EN and KZ) ----------
def repl_narr(m):
    author, year, rest = m.group(1), m.group(2), m.group(3)
    v = resolve(author, year)
    if not v:
        return m.group(0)
    nn = value_to_nums(v)
    pg = PAGE.search(rest)
    return f"{author} [{nn}, {pg.group(1).strip()}]" if pg else f"{author} [{nn}]"


def repl_paren(m):
    inner = m.group(1)
    if not re.search(r"[A-Za-z]", re.sub(YEAR, "", inner)):
        return m.group(0)
    nums, leftovers = [], []
    for part in inner.split(";"):
        ym = re.search(r"(" + YEAR + r")", part)
        author = part[:ym.start()].strip().strip(",").strip() if ym else ""
        if not ym or not author:
            leftovers.append(part.strip()); continue
        v = resolve(author, ym.group(1))
        if not v:
            leftovers.append(part.strip()); continue
        pg = PAGE.search(part)
        nums.append(value_to_nums(v) + (", " + pg.group(1).strip() if pg else ""))
    if not nums:
        return m.group(0)
    out = "[" + ", ".join(nums) + "]"
    if leftovers:
        out += " (" + "; ".join(leftovers) + ")"
    return out


def convert(body):
    return NARR.sub(repl_narr, PAREN.sub(repl_paren, body))


conv_en = convert(body_en)
head_kz, body_kz = split_body(SRC_KZ)
conv_kz = convert(body_kz)

# ---------- reference list (cards in [N] order) ----------
bib = {}
for ln in BIB.read_text(encoding="utf-8").splitlines():
    p = ln.split("\t")
    if len(p) >= 2:
        bib[p[0]] = re.sub(r"\[https?://[^\]]+\]\([^)]+\)", lambda x: x.group(0).split("]")[0][1:], p[1])
inv = {v: k for k, v in cardN.items()}
refs = [f"{n}. {re.sub(r'[*]', '', bib.get(inv[n], '[card not found]'))}" for n in range(1, N + 1)]

# ---------- exhaustive QA: every remaining author-year token ----------
def residual(conv):
    blocking, selfk, appdk, unknown = [], [], [], []
    for m in NARR.finditer(conv):
        cls = ("blocking" if resolve(m.group(1), m.group(2)) else classify(m.group(1)))
        {"blocking": blocking, "self": selfk, "appd": appdk, "unknown": unknown}[cls].append(("narr", m.group(0)[:70]))
    for m in PAREN.finditer(conv):
        inner = m.group(1)
        if not re.search(r"[A-Za-z]", re.sub(YEAR, "", inner)):
            continue
        for part in inner.split(";"):
            ym = re.search(r"(" + YEAR + r")", part)
            a = part[:ym.start()].strip().strip(",").strip() if ym else ""
            if not ym or not a:
                continue
            cls = ("blocking" if resolve(a, ym.group(1)) else classify(a))
            {"blocking": blocking, "self": selfk, "appd": appdk, "unknown": unknown}[cls].append(("paren", m.group(0)[:70]))
    return blocking, selfk, appdk, unknown


SELF_NOTE_EN = (
    "\n\n> **Note — pending entries.** Self-citations of the candidate (Yesmukhamedov; Sapakova, "
    "Yesmukhamedov & Sapakov, 2024–2025) and the Appendix-D publication records are intentionally "
    "left in author-year form: the same surface form maps to different self-papers by section, so "
    "their `[N]` numbers require manual per-section disambiguation before the final bound "
    "submission. Their SIR-4 'prior own work' prose framing is preserved in the running text.\n")
SELF_NOTE_KZ = (
    "\n\n> **Ескерту — кейінге қалдырылған жазбалар.** Кандидаттың өзіне сілтемелері (Есмұхамедов; "
    "Сапақова, Есмұхамедов және Сапақов, 2024–2025) мен Қосымша Д жариялым жазбалары әдейі автор-жыл "
    "түрінде қалдырылды: бірдей жазылым әртүрлі бөлімдерде әртүрлі өз мақалаға сәйкес келеді, "
    "сондықтан олардың `[N]` нөмірлері түпкі түптеуге дейін қолмен бөлім-бойынша ажыратуды талап "
    "етеді. Мәтіндегі SIR-4 'кандидаттың алдыңғы жеке жұмысы' тұжырымдамасы сақталған.\n")

hdr_en = (f"# Automated Diabetic Retinopathy Diagnosis — EN manuscript with GOST [N] citations\n\n"
          f"> **STAGE-G (final pass) — {date.today()}.** Working author-year citations converted to "
          f"numbered `[N]` (GOST 7.32-2001 §6.11, by first appearance). {N} external sources numbered "
          f"[1]–[{N}]. Numbers are shared with the Kazakh manuscript (language invariance). Provisional "
          f"until the experiment-gated chapters (most of Ch 4, Ch 5, Ch 0, Ch 7) join the assembly.\n")
hdr_kz = (f"# Диабеттік ретинопатияны автоматтандырылған диагностикалау — GOST [N] дәйексөздері бар "
          f"қазақ тіліндегі мәтін\n\n"
          f"> **STAGE-G (түпкі өту) — {date.today()}.** Жұмыстық автор-жыл дәйексөздері нөмірленген "
          f"`[N]` түріне түрлендірілді (GOST 7.32-2001 §6.11, алғаш кездесу ретімен). {N} сыртқы "
          f"дереккөз [1]–[{N}] болып нөмірленді. Нөмірлер ағылшын тіліндегі мәтінмен ортақ "
          f"(тіл-инварианттылық).\n")

OUT_EN.write_text(
    hdr_en + "\n" + conv_en +
    "\n\n---\n\n# LIST OF REFERENCES USED\n\n"
    "> In order of first appearance (GOST 7.32-2001 §6.11). Entries derived from the literature "
    "cards; GOST 7.1-2003 punctuation refinement is the final typesetting step.\n\n"
    + "\n".join(refs) + SELF_NOTE_EN, encoding="utf-8")
OUT_KZ.write_text(
    hdr_kz + "\n" + conv_kz +
    "\n\n---\n\n# ПАЙДАЛАНЫЛҒАН ӘДЕБИЕТТЕР ТІЗІМІ\n\n"
    "> Алғаш кездесу ретімен (GOST 7.32-2001 §6.11). Дереккөздер тізімі ағылшын тіліндегі мәтінмен "
    "бірдей нөмірленген (тіл-инварианттылық).\n\n"
    + "\n".join(refs) + SELF_NOTE_KZ, encoding="utf-8")

# ---------- QA report ----------
b_en, s_en, a_en, u_en = residual(conv_en)
b_kz, s_kz, a_kz, u_kz = residual(conv_kz)
n_en = len(re.findall(r"\[\d+(?:,[^\]]*)?\]", conv_en))
n_kz = len(re.findall(r"\[\d+(?:,[^\]]*)?\]", conv_kz))

q = [f"# Stage-G citation conversion — FINAL resolution & QA ({date.today()})\n",
     f"Sources: `{SRC_EN.name}` + `{SRC_KZ.name}`.  Outputs: `{OUT_EN.name}`, `{OUT_KZ.name}`.",
     "Numbering assigned ONCE by first appearance in EN, reused verbatim in KZ (rule #7).\n",
     "## Summary",
     f"- External sources numbered: **{N}**  |  Highest [N]: **{N}**",
     f"- Bracketed citations placed — EN: **{n_en}** | KZ: **{n_kz}**",
     f"- Residual *resolvable* author-year (BLOCKING) — EN: **{len(b_en)}** | KZ: **{len(b_kz)}**",
     f"- Left as author-year by policy — self EN/KZ: **{len(s_en)}/{len(s_kz)}** ; App-D EN/KZ: **{len(a_en)}/{len(a_kz)}**",
     f"- UNKNOWN author-year (needs a card or is non-citation prose) — EN: **{len(u_en)}** | KZ: **{len(u_kz)}**\n",
     "## BLOCKING — resolvable but still author-year (must be 0)",
     "### EN"] + ([f"- {t}: `{s}`" for t, s in b_en] or ["- none"]) + ["### KZ"] + ([f"- {t}: `{s}`" for t, s in b_kz] or ["- none"])
q += ["\n## UNKNOWN author-year (review — uncarded source or false positive)", "### EN"]
q += ([f"- {t}: `{s}`" for t, s in sorted(set(u_en))] or ["- none"])
q += ["### KZ"] + ([f"- {t}: `{s}`" for t, s in sorted(set(u_kz))] or ["- none"])
q += ["\n## Self-citations left author-year (policy) — distinct surface forms",
      "### EN"] + sorted({s for _, s in s_en}) + ["### KZ"] + sorted({s for _, s in s_kz})
q.append("\n## Reference list (in order of appearance)")
q += refs
OUT_QA.write_text("\n".join(q), encoding="utf-8")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
print(f"WROTE {OUT_EN.name}  (brackets: {n_en})")
print(f"WROTE {OUT_KZ.name}  (brackets: {n_kz})")
print(f"WROTE {OUT_QA.name}")
print(f"External sources numbered: {N}")
print(f"BLOCKING  EN={len(b_en)}  KZ={len(b_kz)}   UNKNOWN  EN={len(u_en)}  KZ={len(u_kz)}")
