# TRANSLATION REVIEW PROTOCOL

**Version:** 6.0.0 | **Date:** 2026-06-08 | **Binding Reference:** INVARIANTS.md v6.0.0
**Usage:** Use this checklist in a Claude Opus review session to verify a Kazakh translation against the approved English section and the translation control documents. Attach the approved English section, the Kazakh translation, GLOSSARY_KZ.md, and the Term Usage Report produced by `translation-directive.md` (PART 2).

This is **Stage F (Translation Review)** of the writing pipeline — the back-check that closes the loop opened by `translation-directive.md` (Stage E). It does not re-translate; it verifies.

---

# TRANSLATION REVIEW — §[X.Y.Z] [Section Title]

## A. SEMANTIC FIDELITY

For each paragraph of the section:
- [ ] The Kazakh text conveys the same propositional content as the approved English source — no claim added, dropped, strengthened, or weakened.
- [ ] Hedged claims remain hedged; the strength classification of every claim is preserved across languages.
- [ ] No content from a different section has leaked in; no paragraph is omitted.

## B. TERMINOLOGY CONTROL (GLOSSARY_KZ)

- [ ] Every term in GLOSSARY_KZ Section A (CNN, CLAHE, ResNet-50, EfficientNet-B3/B4, ROC-AUC, F1-Score, Grad-CAM, IoU, ALO, Transfer Learning, Fine-Tuning, etc.) **remains in English** and is not translated.
- [ ] Every conceptual term is translated per the GLOSSARY_KZ Part B table — no ad-hoc alternative renderings.
- [ ] First use of each translated term is bilingual: қазақша (English); subsequent uses are consistent.
- [ ] No Russian loan word is used where a Kazakh academic equivalent exists per GLOSSARY_KZ.
- [ ] The Term Usage Report (PART 2 from Stage E) matches the actual term usage in the translated text — spot-check at least the first use of each row.

## C. GOVERNANCE-CODE PRESERVATION

- [ ] All governance reference codes appear **verbatim and untranslated**: PC-0, PC-x, SC-x.y, SC-A…SC-H, H-x, CFC-1.x, CFC-2.x (incl. CFC-2.8, CFC-2.9), NC-x, SIR-x (incl. SIR-9), SB-x.x, DGL-x, EH-x, OD-x, IT-1, and the paradigm labels P1 / P2.
- [ ] All Literature Card IDs (e.g., LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-2025-Yesmukhamedov-01) are unchanged.
- [ ] Paradigm phrasings about Gulshan et al. (2016) / P1 sources remain within the permitted set after translation — the Kazakh rendering must not drift into a forbidden formulation (CFC-2.9): it may state that these works *treat preprocessing as ancillary data preparation* or *defer preprocessing details to the supplement*, but must NOT assert that they *claim preprocessing is unimportant* or that the dissertation *outperforms* them.

## D. STRUCTURAL PRESERVATION

- [ ] Section headings translated but numbering identical (§X.Y.Z).
- [ ] Table structures preserved — headers/text translated; data values, metrics, and numbers unchanged.
- [ ] Equation numbering and mathematical notation unchanged.
- [ ] Citation references ([Author, Year] or Literature Card IDs) unchanged.

## E. REGISTER

- [ ] Formal academic Kazakh appropriate for a doctoral defense at IITU — no colloquialisms.
- [ ] Third-person register and tense usage consistent with the English source (past tense for completed results, present for definitions).

## F. VERDICT

- [ ] **APPROVED** — translation passes all checks; Kazakh text is verified.
- [ ] **REVISION NEEDED** — list specific issues (paragraph/term/code location) for a Stage E re-translation pass.
