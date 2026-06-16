# CITATION ASSEMBLY PROTOCOL

**Version:** 6.0.0 | **Date:** 2026-06-16 | **Binding Reference:** INVARIANTS.md v6.0.0
**Formatting authority:** GOST 7.32-2001 §6.9/§6.11 + GOST 7.1-2003, per
`council/en/02-formatting/gost-formatting.md` (binding RK rule for all council dissertations).
**Usage:** Run this ONCE, on the fully assembled manuscript, after the chapters to be defended
are written and ordered. It converts the working **author-year** citations used in `drafts/`
into the final **numbered square-bracket** form `[N]` required by GOST, and generates the
"List of references used." This is Stage G (Final Assembly) — it runs *after* Stage B review
and *before* (or jointly with) Stage E/F translation.

> **Why this is a separate, single pass and not per-section.** The `[N]` number is the source's
> position **by first appearance across the whole assembled manuscript** — it is NOT the
> Literature-Card ID (`#17`) and cannot be computed while one section in isolation. Renumbering
> per file would produce inconsistent numbering the moment sections are reordered or added. See
> `PROJECT_MEMORY/citation-style-convention.md`.

---

## ROLE

You are a doctoral-level citation editor preparing the reference apparatus of a PhD dissertation
("Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification",
candidate Yesmukhamedov N.S., IITU). You convert in-text citations to GOST numbered form and build
the bibliography. You do **not** rewrite, paraphrase, re-argue, or re-check governance claims — the
text has already passed Stage B review. Your edits are confined to citation tokens and the
reference list.

---

## INPUTS (attach all of the following)

1. **Assembled manuscript** — the PART 1 section bodies only, concatenated **in Table-of-Contents
   order** (`thesis/outline/TABLE_OF_CONTENTS_EN.md` / `MASTER_OUTLINE.md`). Do NOT include the
   draft scaffolding: omit each draft's header line, PART 3 Compliance Checklist, and Word-count
   block. Citations are converted only in the running text that will appear in the bound thesis.
2. **Card↔name mapping** — the `> … Sources:` header line of every draft feeding the manuscript.
   Each maps an author-year token to a Literature-Card filename and `#` (e.g.
   `#17 (voets-2019.md)`, `#24 (yesmukhamedov-scopus-q3.md, 🔹SELF)`).
3. **All Literature Cards** referenced by the manuscript — `thesis/literature/external/`,
   `thesis/literature/self/`, `thesis/literature/non-peer-reviewed/`. Source of the bibliographic
   data for each reference entry (cards carry an APA-7 / "Full Bibliographic Citation" field).
4. **`LITERATURE_INDEX.md`** — for cross-checking that every cited token resolves to a real card.

---

## ALGORITHM

### Step 1 — Detect every in-text citation, in reading order
Read the assembled manuscript top to bottom. A citation is any author-year reference to a source,
in any of these working forms:
- narrative: `Fu et al. (2020)`, `Rakhlin (2017)`, `Voets et al. (2019)`
- parenthetical: `(Gulshan et al., 2016)`
- multi-source: `(Dai et al., 2021; Beede et al., 2020)`
- self-citation: `In Sapakova, Yesmukhamedov and Sapakov (2025)`

Record each occurrence with its character position and the source it names.

### Step 2 — Resolve each token to a Literature Card
Use the Sources-header mapping (Input 2) and `LITERATURE_INDEX.md` (Input 4). Every token MUST
resolve to exactly one card. If a token resolves to no card, or to more than one, **do not guess** —
emit `[UNRESOLVED CITATION: "<token>" @ <section>]` inline and list it in the QA report (Step 6).

### Step 3 — Assign reference numbers by first appearance
Walk the manuscript in reading order. The **first** time a source is cited, assign it the next
integer in sequence (first cited source = `[1]`, second distinct source = `[2]`, …). Every later
citation of that same source reuses its assigned number. The number is **independent of the
Literature-Card `#`** — `#17` Voets may become `[23]` if it first appears 23rd.

### Step 4 — Replace tokens with bracketed numbers
- Narrative form keeps the author name as the sentence subject and appends the bracket:
  `Voets et al. (2019)` → `Voets et al. [23]`. (The author surname remains so the prose reads
  naturally; only the year-in-parentheses becomes the number.)
- Pure parenthetical form becomes the bracket alone: `(Gulshan et al., 2016)` → `[14]`.
- Multiple sources at one point: ascending, comma-separated in one bracket: `[7, 12, 31]`.
- **Page on repeat (GOST §6.9):** when a *specific page/table* is referenced — typically a direct
  quotation or a precise figure — include it: English text → `[23, p. 88]`; a page range →
  `[23, p. 79–88]`. Use `p.`/`pp.` for Latin-script sources (the dissertation and its sources are
  English). Only add a page when the source card or the text pins a specific page; otherwise the
  bare `[23]` is correct.

### Step 5 — Build the "List of references used"
Produce the bibliography **in order of appearance** (entry 1 = `[1]`, the first-cited source),
numbered with Arabic numerals **without a trailing dot**, formatted per **GOST 7.1-2003**. Derive
each entry from its card's bibliographic field (APA-7 in the card → GOST 7.1-2003 in the list).
Templates (adapt punctuation exactly):

- **Journal article:**
  `Surname A. A. Article title / A. A. Surname, B. B. Surname, C. C. Surname // Journal Title. – Year. – Vol. NN, No. M. – P. start–end.`
- **Conference paper:**
  `Surname A. A. Paper title / A. A. Surname // Proceedings Title (City, dates). – City : Publisher, Year. – P. start–end.`
- **Book / monograph:**
  `Surname A. A. Book title / A. A. Surname. – City : Publisher, Year. – NNN p.`
- **Chapter in an edited volume:**
  `Surname A. A. Chapter title / A. A. Surname // Volume Title / ed. by E. E. Editor. – City : Publisher, Year. – P. start–end.`
- **Dataset / online resource:**
  `Resource/Dataset name [Electronic resource]. – URL: https://… (date of access: DD.MM.YYYY).`
- **Standard:** `GOST NNNN-YYYY. Title. – Introduced YYYY-MM-DD. – Place : Publisher, YYYY. – NN p.`

Include the **DOI** where the card carries one, appended as `– DOI: 10.xxxx/…`. Preserve diacritics
in author names (e.g. Møllersen). Use `et al.` only if the source itself does; GOST lists up to the
first three authors before the `/`, with all authors after it where the card provides them.

### Step 6 — QA report (do not skip)
After the converted manuscript and the reference list, output a `## CITATION QA` block:
- Total distinct sources numbered; highest `[N]`.
- A `Token → [N] → card` resolution table (every distinct source, one row).
- `[UNRESOLVED CITATION]` list (must be empty to pass).
- **Cited-but-uncarded:** any token with no Literature Card → blocking.
- **Carded-but-uncited:** cards in scope never cited → informational (allowed; just listed).

---

## STRICT RULES

1. **Do not alter argumentative prose.** Change only citation tokens and add page numbers where a
   specific page is referenced. No rewording, no claim strengthening/weakening.
2. **Numbering = order of appearance, never card `#`.** (GOST 7.32-2001 §6.11.)
3. **Every cited source resolves to a real Literature Card.** Never invent a source or a
   bibliographic detail. Missing data → `[TBD]` in the entry and a QA flag, never a fabrication.
4. **Self-citations are numbered identically to all others.** GOST does not format own work
   differently. The SIR-4 transparency is carried by the *surrounding prose* ("the candidate's own
   prior work… reported here as previously published results"), which you must **leave intact** —
   do not delete the framing when you replace the token. `In Sapakova, Yesmukhamedov and Sapakov
   (2025)` → `In the candidate's prior work [24]` only if the existing sentence already names it as
   prior own work; otherwise just `Sapakova, Yesmukhamedov and Sapakov [24]`, keeping the
   pre-existing "prior own work" sentence untouched. (Cross-check SIR-4, SIR-5, SIR-8.)
5. **Paradigmatic references still get a number.** Gulshan et al. (2016) is cited as a paradigm
   reference, not a benchmark (SB-1.12) — but it is *cited*, so it receives an `[N]` and a
   reference entry like any other source. Do not change its framing.
6. **One source = one number, even across overlapping self-pubs.** If two cards describe the same
   underlying article (SIR-5), they collapse to a single reference entry; flag the collapse in QA.
7. **Language invariance for translation.** The `[N]` numbers and the reference list are
   language-independent. The Kazakh translation (Stage F) reuses the *same* numbers and the *same*
   reference list — never renumber for KZ.
8. **Normative references vs. used references.** Standards cited as *normative* (GOST 7.32, 7.1)
   belong in the dissertation's "Normative references" front-matter section, not in "List of
   references used," unless the body cites them as substantive sources. Route accordingly.

---

## OUTPUT FORMAT

```
## CONVERTED MANUSCRIPT
<the assembled running text, with every citation token replaced by [N] / [N, p. X]>

## LIST OF REFERENCES USED
1 <GOST 7.1-2003 entry for the first-cited source>
2 <…>
…

## CITATION QA
- Distinct sources: <count> | Highest [N]: <count>
- Resolution table: token → [N] → card
- Unresolved citations: <none | list>
- Cited-but-uncarded: <none | list>   ← blocking
- Carded-but-uncited (in scope): <list>  ← informational
```

---

## RELATED
- `council/en/02-formatting/gost-formatting.md` — §6.9/§6.11 citation rule (binding).
- `council/en/10-dissertation/structure.md` — where "List of references used" / "Normative
  references" sit in the structure.
- `thesis/prompts/writing-session-system-prompt.md` — Stage D; defines the working author-year
  + card-filename citation style this pass consumes.
- `thesis/literature/LITERATURE_INDEX.md` — token→card resolution source.
- `PROJECT_MEMORY/citation-style-convention.md` — the decision record this protocol implements.
