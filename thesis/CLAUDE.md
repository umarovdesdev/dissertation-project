# thesis/ — Dissertation Text and Governance

Doctoral dissertation: "Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification"
Candidate: Yesmukhamedov N.S., IITU, Almaty, Kazakhstan.

## Structure

```
governance/          — SINGLE SOURCE OF TRUTH for all project claims
  INVARIANTS.md        v4.1 — scope, forbidden claims, binding constraints
  HYPOTHESIS.md        v4.1 — H-1 through H-6 formal definitions
  ARGUMENT_MAP.md      v4.1 — claim-evidence dependency DAG
  CENTRAL_THESIS.md    v4.0 — one-paragraph thesis statement
  CORE_OBJECTIVE.md    v4.0 — research goal
  CONTRIBUTIONS.md     v4.1 — 4 primary + supporting contributions
  RESEARCH_ARCHITECTURE.md  v4.1 — full experimental design
  VERSION_SYNC.md      v4.1 — cross-file version register

chapters/            — 8 chapters (00–07), each with:
  briefs/              section briefs (writing specs)
  drafts/              generated text
  reviews/             review feedback
  sessions/            session transcripts
  continuity/          continuity notes between sections
  translations/        Kazakh translations

literature/
  external/            36 literature cards (structured 18-section format)
  self/                6 self-citations (yesmukhamedov-*.md)
  non-peer-reviewed/   1 card (wikipedia-clahe.md)
  LITERATURE_INDEX.md  master index of all sources

glossary/
  GLOSSARY_EN.md       canonical English terms
  GLOSSARY_KZ.md       Kazakh translations

outline/
  MASTER_OUTLINE.md    chapter-by-chapter content specification
  TABLE_OF_CONTENTS_EN.md
  TABLE_OF_CONTENTS_KZ.md

methods/
  preprocessing-pipeline.md   V4 pipeline full specification
  implementation.md           implementation details

prompts/              AI writing session templates
  writing-session-system-prompt.md  — fixed system prompt for all writing sessions
  section-brief-template.md
  continuity-note-template.md
  revision-session-template.md
  literature-card-generation.md
  literature-card-review.md
  and others...

experiments/
  experimental-protocol.md    detailed scientific protocol (426 lines)

scripts/
  assemble-session-input.py   helper for preparing writing session inputs
```

## Governance Hierarchy

INVARIANTS.md is the supreme authority. If any document conflicts with INVARIANTS, INVARIANTS wins. The hierarchy:

1. INVARIANTS.md — defines what can and cannot be claimed
2. HYPOTHESIS.md — formal hypothesis definitions (must match INVARIANTS)
3. ARGUMENT_MAP.md — claim-evidence structure (must match INVARIANTS)
4. CENTRAL_THESIS.md / CORE_OBJECTIVE.md — thesis statement and goal
5. CONTRIBUTIONS.md — what the dissertation contributes
6. RESEARCH_ARCHITECTURE.md — experimental design details

## Writing Workflow

1. Prepare a Section Brief (from `prompts/section-brief-template.md`)
2. Load the system prompt (`prompts/writing-session-system-prompt.md`)
3. Load INVARIANTS.md + relevant governance docs
4. Load relevant literature cards
5. Load continuity note from preceding section (if any)
6. Generate section text
7. Review against governance constraints
8. Produce continuity note for next section

## Key Governance Rules

- Every empirical claim must cite its evidence source by Literature Card filename
- Forbidden claims (CFC-2.x) must not appear in any form
- Non-claims (NC-x) must not be asserted
- Scope boundaries (SB/DGL) must be stated where relevant claims first appear
- Self-citations must be identified as prior own work (SIR-4)
- No source amplification — only attribute conclusions explicitly in the literature card (SIR-1)
- Terminology must match GLOSSARY_EN canonical forms

## Chapter Status

- 00-introduction: Not started (depends on all other chapters)
- 01-problem-domain: In progress
- 02-theoretical-foundations: In progress
- 03-methodology: In progress
- 04-experiments: In progress
- 05-validation: Not started
- 06-system-architecture: Not started
- 07-conclusion: Not started (depends on all chapters)

## Hypotheses

- H-1: Preprocessing Dominance (Exp 1, EyePACS)
- H-2: CLAHE Threshold Sensitivity (Exp 2, IDRiD)
- H-3: DROPPED in V3
- H-4: Cross-Dataset Generalization (Exp 5, Messidor/IDRiD, G ≥ 0.85)
- H-5: Explainability — Grad-CAM ALO/IoU (Exp 4, IDRiD)
- H-6: Device Domain Shift (Exp 6, RFMiD/DDR/ODIR-5K)

## Language

- Dissertation text: formal academic English
- Translations: Kazakh (in translations/ subdirectories)
- All governance docs: English
- Register: third person, past tense for results, present tense for definitions
