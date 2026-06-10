# SECTION BRIEF
## Appendix D — Certificates and Publication Confirmations

**Chapter:** Appendices (follows Ch 7)
**Section Function:** supporting material / approbation evidence (PUBLICATION CATALOGUE, not results)
**Word Count Target:** 500–800 words of framing prose around the publication table and the asset list
**Paragraph Count Target:** orientation prose + a publications table + a certificate-asset list

> **Pre-step gate check (PLAN §10 / §3.1):** PASSED. Required resource: **APP-D ✅ AVAILABLE** (`ASSET_INVENTORY.md §2`, row APP-D → six PNGs in `defense/presentation/assets/publications/`: `SCOPUS.png`, `SCOPUS_CONF.png`, `KBTU.png`, `KAZTBU.png`, `AKADEMY.png`, `PUBLICATIONS.png`). On-disk assets verified present. Source publications catalogued in `thesis/literature/self/` (cards #19–#24). Nothing ❌ MISSING. No experiment outcome cited.

---

### GOVERNANCE BINDINGS

**Hypotheses tested/supported:** None — approbation/supporting evidence.
**Paradigm positioning:** None.
**Primary claims advanced:** None empirical. Supports **§0.11 (Approbation)** and **§0.12 (Publications)** (Ch 0, Phase-2) by cataloguing the prior-publication record.
**Forbidden claims (must not appear):** CFC-2.1, CFC-2.2, CFC-2.4, CFC-2.5 — list publications and confirmation assets; assert no result, ranking, or deployment claim. In particular, the EEJET self-publication reports a "100% accuracy/sensitivity/specificity" figure in its own abstract; **that figure must NOT be repeated or endorsed here** (CFC-2.5 / SIR-1) — the appendix catalogues the *existence and provenance* of the publication, not its claims.
**Non-claims (must not assert):** None empirical at risk.
**Source interpretation rules:** **SIR-4** (every catalogued publication is co-authored by the candidate → identify as prior own work, the binding spine of this appendix); **SIR-5** (cards #23 `scopus-q2` and #24 `scopus-q3` are duplicate cards of the **same** EEJET article — catalogue the article once, do not double-count it as two publications); **SIR-1** (no amplification — list venue/DOI/year as recorded; do not restate the publications' internal performance claims as findings of this dissertation).
**Scope boundaries:** **No-fabrication rule (binding):** every catalogued entry must correspond to a real card in `thesis/literature/self/` and/or a real asset on disk; no publication, certificate, or DOI may be invented.
**Evidence thresholds:** None (non-experimental).

---

### CONTENT SPECIFICATION

**Section objective:** Catalogue the candidate's prior publications relevant to the dissertation and the corresponding publication/indexing-confirmation assets, identifying every entry as prior own work (SIR-4) and providing the approbation record that §0.11/§0.12 draw upon — with no fabricated entry and without repeating any publication's internal performance claim.

**Argumentative spine (required):**
- **Thesis:** The dissertation's contributions were progressively published in peer-reviewed venues; this appendix records that publication trail and its confirmation assets as the approbation of the work, while marking every entry as the candidate's own prior work so the main text's reuse of it is transparent (SIR-4).
- **Reasoning chain:**
  1. State the appendix's purpose: provide the approbation/publication record underpinning §0.11 and §0.12.
  2. Render the **publications table** — five distinct peer-reviewed outputs (the EEJET article appears once, though two analytical cards describe it; SIR-5), each with authors, title, venue, year, DOI, indexing, and the literature-card ID (#19–#24).
  3. Identify all as co-authored by the candidate (prior own work, SIR-4); note that the EEJET entry is documented by two cards (`scopus-q2`/`scopus-q3`) prepared from different perspectives (SIR-5), and flag the known card-ID anomaly on `scopus-q2.md` (`LC-AlTimemy-2021`) without inferring anything from it.
  4. List the **confirmation assets** by real path (the six PNGs), mapping each to its publication; note `PUBLICATIONS.png` as the aggregate record.
  5. Bound it: no-fabrication rule; do not repeat the EEJET "100%" figure or any internal performance claim (SIR-1/CFC-2.5).
- **Conclusion / hand-off:** The publication record and its confirmation assets constitute the approbation evidence for §0.11/§0.12; the assets are resolved to image insertions in Phase 3 (§11.2).

**Required content elements:**
1. Purpose statement linking App D to §0.11 (Approbation) and §0.12 (Publications).
2. **Publications table:** 5 distinct outputs — EEJET (Scopus Q3 journal, #23/#24); Procedia CS / DS 2025 (Scopus conference, #19); KBTU Herald (#21); KazUTB Vestnik (#20); NAS RK News, Phys.-Math. Series (#22) — authors/venue/year/DOI/indexing/card-ID.
3. SIR-4 identification of all as prior own work; SIR-5 note on the #23/#24 duplicate EEJET cards; card-ID anomaly flag.
4. **Confirmation-asset list:** the six real PNGs by path, mapped to publications.
5. Bounds: no-fabrication; no repetition of internal performance claims (SIR-1/CFC-2.5).

**Required tables/figures:**
- **Publications table** rendered inline as Markdown.
- **Confirmation-asset list** as placeholders by real path (resolved to image insertions in Phase 3 §11.2; e.g. `[APP-D/SCOPUS.png: … — defense/presentation/assets/publications/SCOPUS.png]`).

**Required equations:** None.

---

### SOURCE MAPPING

| Source | Role | Specific Content |
|--------|------|------------------|
| #19 `yesmukhamedov-conf.md` 🔹SELF | publication entry (SIR-4) | Sapakova, Yesmukhamedov et al. (2025), *Procedia Computer Science* 272, 496–501, DOI 10.1016/j.procs.2025.10.237 (DS 2025, Istanbul) → `SCOPUS_CONF.png` |
| #20 `yesmukhamedov-kazutb.md` 🔹SELF | publication entry (SIR-4) | Sapakova et al. (2024), *Vestnik KazUTB* 2(27-740), DOI 10.58805/kazutb.v.2.27-740 → `KAZTBU.png` |
| #21 `yesmukhamedov-kbtu.md` 🔹SELF | publication entry (SIR-4) | Yesmukhamedov et al. (2025), *Herald of KBTU* 4(75), DOI 10.55452/1998-6688-2025-22-4-119-130 → `KBTU.png` |
| #22 `yesmukhamedov-nan-rk.md` 🔹SELF | publication entry (SIR-4) | Yesmukhamedov, Sapakova, Al-Haddad, Daniyarova (2025), *News of NAS RK, Phys.-Math. Series* 2(354), 74–91, DOI 10.32014/2025.2518-1726.345 → `AKADEMY.png` |
| #23 `yesmukhamedov-scopus-q2.md` 🔹SELF | publication entry (SIR-4/SIR-5) | duplicate card of the EEJET article; ID anomaly `LC-AlTimemy-2021` flagged |
| #24 `yesmukhamedov-scopus-q3.md` 🔹SELF | publication entry (SIR-4/SIR-5) | Sapakova, Yesmukhamedov & Sapakov (2025), *Eastern-European J. of Enterprise Technologies* 4(9(136)), 79–88, DOI 10.15587/1729-4061.2025.335570 → `SCOPUS.png` |
| `defense/presentation/assets/publications/*.png` (on disk) | confirmation assets | `SCOPUS.png`, `SCOPUS_CONF.png`, `KBTU.png`, `KAZTBU.png`, `AKADEMY.png`, `PUBLICATIONS.png` |
| `LITERATURE_INDEX.md` note #5 | reconciliation | #23 and #24 are duplicate entries for the same EEJET article |

**⚠️ Coverage gaps:** None requiring `[UNSOURCED CLAIM]`. Every entry corresponds to a real card and/or asset. Card-ID anomaly on `scopus-q2.md` is flagged, not resolved here (it does not affect the bibliographic catalogue, which keys on the recorded citation).

---

### CROSS-REFERENCES

**Backward:** §2.4.1 (#20 laser model), §3.x/§4.x (#19/#21/#23/#24 preprocessing lineage), §6.1–§6.3 (#22 architecture) — the sections that reuse each prior work.
**Forward:** §0.11 (Approbation), §0.12 (Publications) — Phase-2 (Ch 0), which draw on this catalogue; Phase 3 §11.2 (asset resolution).

---

### BOUNDARY WARNINGS

1. **No-fabrication rule is the spine.** Every publication, DOI, and asset must be real (card-backed and/or on disk); invent nothing.
2. **Do not repeat internal performance claims** — especially the EEJET "100% accuracy/sensitivity/specificity" figure (SIR-1/CFC-2.5). Catalogue existence and provenance, not claims.
3. **SIR-4 on every entry** — all are co-authored prior own work.
4. **SIR-5** — the EEJET article is one publication, two cards; count it once.
5. No result, ranking, or deployment claim (CFC-2.2/2.4).

---

### COUNTER-ARGUMENT & INHERITED LIMITATIONS

- **Counter-position:** A publication list can read as a performance endorsement of its contents. Pre-empt by stating explicitly that the catalogue records provenance and approbation, not the validity of the publications' internal claims, which are re-examined under the dissertation's own governance.
- **Inherited limitations (SIR-2):** the self-publications carry self-plagiarism risk (LITERATURE_INDEX note #4) — the SIR-4 identification here is what keeps the main text's reuse transparent.

---

### ACCEPTANCE CRITERIA

A draft is **strong** when:
- [ ] Publications table complete: 5 distinct outputs, each with authors/venue/year/DOI/indexing/card-ID; EEJET counted once (SIR-5).
- [ ] Every entry identified as prior own work (SIR-4); #23/#24 duplication and the card-ID anomaly noted.
- [ ] Six confirmation assets listed by real path and mapped to publications.
- [ ] No internal performance claim repeated (esp. EEJET "100%"); no fabricated entry; bounds stated.

A **passable** draft merely lists references. Aim above passable: the catalogue is framed as approbation evidence with transparent SIR-4 provenance.

---

### WRITING DIRECTIVES (section-specific)

- **Tense:** present for the catalogue ("the work was published" — past for the act of publication; present for "this appendix records").
- **Self-citation handling:** SIR-4 on every entry; SIR-5 for the EEJET duplicate cards.
- **Terminology watch:** peer-reviewed publication; Scopus-indexed; conference proceedings; approbation. Flag any non-glossary term.
- **No amplification:** venue/DOI/year as recorded; no restatement of publications' performance figures.
