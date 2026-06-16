# VERIFICATION PROTOCOL

**Version:** 6.0.0 | **Date:** 2026-06-08 | **Binding Reference:** INVARIANTS.md v6.0.0
**Usage:** Use this checklist in Claude Opus review sessions to verify a drafted section against governance constraints. Attach the draft, the Section Brief, and INVARIANTS.md.

---

# VERIFICATION PROTOCOL — §[X.Y.Z] [Section Title]

## A. CLAIM COMPLIANCE

For each empirical claim in the draft:
- [ ] Evidence source cited (Literature Card filename + page/table)?
- [ ] Citation matches what the source's literature card actually states?
- [ ] Claim strength appropriate per ARGUMENT_MAP strength classification?
- [ ] Scope boundary stated at point of first introduction?
- [ ] **Claim coverage:** every Primary Claim (PC-0, PC-x) and Sub-claim (SC-x.y) listed in the Section Brief is actually advanced in the draft, and no claim outside the brief's bindings is introduced?

## B. FORBIDDEN CONTENT SCAN

- [ ] **CFC-2.1 scan:** No universal generalization ("all datasets," "universally," "always improves")
- [ ] **CFC-2.2 scan:** No superiority claims ("outperforms," "superior to," "better than [named system]")
- [ ] **CFC-2.3 scan:** No deployment outcomes as results ("reduces complications," "cost reduction")
- [ ] **CFC-2.4 scan:** No clinical validation claims ("clinical-grade," "clinically validated," "ready for deployment")
- [ ] **CFC-2.5 scan:** No perfect performance generalizations ("achieves 100% accuracy")
- [ ] **CFC-2.6 scan:** No amplified source claims — no conclusion attributed to a source stronger than its literature card explicitly states (cross-check §D / SIR-1)
- [ ] **CFC-2.7 scan:** No retroactive re-characterization of self-publications
- [ ] **CFC-2.8 scan:** No attribution of the H-1 effect to preprocessing alone — phrases "the preprocessing pipeline produces the observed improvement" or "preprocessing dominates" absent in the context of H-1 results; only integrated-pipeline framing used ("the integrated preprocessing + ophthalmology-SSL configuration outperforms the baseline + ImageNet configuration")
- [ ] **CFC-2.9 scan:** No false attribution of a "preprocessing is unimportant" theoretical claim to Gulshan et al. (2016) or any P1 source; no "Gulshan is our baseline" / "we outperform Gulshan" framing (permitted vs. forbidden phrasings checked in §F)
- [ ] **NC-x scan:** Each non-claim listed in Section Brief verified absent — including NC-14 (Grad-CAM ≠ clinical localization of pathology), NC-15 (dirty-data ingestion protocol bound to Kazakh medical-center data), NC-16 (device domain shift ≠ device certification/regulatory compliance), NC-17 (component ablation ≠ universally optimal preprocessing configuration)

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
- [ ] **SIR-2:** Inherited limitations from each cited source's literature card (§II.6) noted at first citation of the relevant result
- [ ] **SIR-7:** EfficientNetB0 results (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF) not generalized to the class of efficient CNN architectures without explicit comparative experiments
- [ ] **SIR-8:** Projected Kazakhstan deployment outcomes (LC-2025-Yesmukhamedov-01, p. 88) not attributed to the dissertation's own findings
- [ ] **SIR-9:** Any "canonical representative of paradigm X" designation grounded in observed methodological practice with a Methodological-Practice note in the source's literature card (§15/§18), not in an attributed theoretical statement

## E. STRUCTURAL INTEGRITY

- [ ] Section connects to preceding Continuity Note
- [ ] Forward/backward cross-references present as specified in Section Brief
- [ ] Continuity Note output is accurate and complete
- [ ] Word count within target range: [TARGET] — Actual: [COUNT]

## F. SCOPE & PARADIGM

- [ ] **SB-1.12:** Gulshan et al. (2016) not treated as an experimental control or numerical benchmark; the experimental baseline (configs A/C, OD-3) and the paradigmatic representative kept terminologically distinct
- [ ] **DGL-6:** Pretraining regimes correctly stated — baseline arm = ImageNet; integrated arm = ophthalmology-specific self-supervised pretraining of the same CNN backbone (ResNet-50 / EfficientNet-B3); no claim of guaranteed transfer
- [ ] **P1/P2 attribution:** Only permitted Gulshan/P1 phrasings used; forbidden phrasings absent (CFC-2.9, SIR-9):
  - Permitted: "treat preprocessing as ancillary data preparation," "defer preprocessing details to the supplement," "exemplify the methodological practice that this dissertation identifies as paradigm P1"
  - Forbidden: "Gulshan claims preprocessing is unimportant," "rejects preprocessing," "argued that preprocessing does not matter," "Gulshan is our baseline," "we outperform Gulshan"

## G. EVIDENCE THRESHOLDS (empirical sections only)

- [ ] **EH-3 (empirical dominance):** Any "dominance" claim satisfies ALL three simultaneously — weighted F1-score improvement ≥ 5 percentage points AND ROC-AUC improvement ≥ 0.02 AND no degradation in Cohen's Kappa, on the test partition. Improvement on a subset of metrics is not described as dominance
- [ ] **EH-4 (sufficient validation of H-1):** "Sufficiently validated" used only if EH-3 holds on the EyePACS test partition AND the same direction of effect is confirmed on ≥ 1 external dataset (APTOS 2019, IDRiD, or Messidor-2) AND results are replicated across both architectures (ResNet-50 and EfficientNet-B3)

## H. VERDICT

- [ ] **APPROVED** — section passes all checks
- [ ] **REVISION NEEDED** — list specific issues for Revision Session
