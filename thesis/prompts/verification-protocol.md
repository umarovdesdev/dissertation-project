# VERIFICATION PROTOCOL

**Version:** 1.0 | **Date:** 2026-03-14
**Usage:** Use this checklist in Claude Opus review sessions to verify a drafted section against governance constraints. Attach the draft, the Section Brief, and INVARIANTS.md.

---

# VERIFICATION PROTOCOL — §[X.Y.Z] [Section Title]

## A. CLAIM COMPLIANCE

For each empirical claim in the draft:
- [ ] Evidence source cited (Literature Card filename + page/table)?
- [ ] Citation matches what the source's literature card actually states?
- [ ] Claim strength appropriate per ARGUMENT_MAP strength classification?
- [ ] Scope boundary stated at point of first introduction?

## B. FORBIDDEN CONTENT SCAN

- [ ] **CFC-2.1 scan:** No universal generalization ("all datasets," "universally," "always improves")
- [ ] **CFC-2.2 scan:** No superiority claims ("outperforms," "superior to," "better than [named system]")
- [ ] **CFC-2.3 scan:** No deployment outcomes as results ("reduces complications," "cost reduction")
- [ ] **CFC-2.4 scan:** No clinical validation claims ("clinical-grade," "clinically validated," "ready for deployment")
- [ ] **CFC-2.5 scan:** No perfect performance generalizations ("achieves 100% accuracy")
- [ ] **CFC-2.7 scan:** No retroactive re-characterization of self-publications
- [ ] **NC-x scan:** Each non-claim listed in Section Brief verified absent

## C. TERMINOLOGICAL CONSISTENCY

- [ ] Every technical term matches GLOSSARY_EN canonical form
- [ ] Disambiguation rules applied (e.g., "feature extraction" vs. "frozen-base strategy")
- [ ] Operational definitions (OD-1 through OD-6) used verbatim where they appear
- [ ] No [TERM NOT IN GLOSSARY] flags unresolved

## D. SOURCE HANDLING

- [ ] **SIR-1:** No source attributed conclusions beyond what its literature card states
- [ ] **SIR-3:** Metric comparisons include dataset/partition/taxonomy context
- [ ] **SIR-4:** Self-publications identified as prior own work
- [ ] **SIR-5:** Overlapping self-publications not cited as independent confirmation
- [ ] **SIR-6:** Modeling study results (yesmukhamedov-kazutb.md) cited as theoretical only

## E. STRUCTURAL INTEGRITY

- [ ] Section connects to preceding Continuity Note
- [ ] Forward/backward cross-references present as specified in Section Brief
- [ ] Continuity Note output is accurate and complete
- [ ] Word count within target range: [TARGET] — Actual: [COUNT]

## F. VERDICT

- [ ] **APPROVED** — section passes all checks
- [ ] **REVISION NEEDED** — list specific issues for Revision Session
