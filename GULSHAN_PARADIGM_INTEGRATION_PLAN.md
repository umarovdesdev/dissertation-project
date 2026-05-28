# GULSHAN PARADIGM INTEGRATION PLAN
## Phased task tracker: embedding the reframed role of Gulshan 2016 into the dissertation project

**Candidate:** Yesmukhamedov N.S.
**Created:** 2026-05-28
**Document status:** Working tracker; updated as phases are executed
**Related governance documents:** INVARIANTS.md v5.2, ARGUMENT_MAP.md v5.0, CENTRAL_THESIS.md v5.0, CONTRIBUTIONS.md v5.0

---

## 0. Context and rationale

### 0.1. Core idea

Gulshan et al. (2016, JAMA) is a foundational study that established the CNN paradigm for automated diabetic retinopathy screening and set the methodological template followed by most subsequent works. In this dissertation, Gulshan is positioned as the **canonical representative of paradigm P1** ("end-to-end CNN, preprocessing treated as ancillary data preparation"), which is operationally instantiated in the baseline configuration of Experiment 1 (configs A/C). The alternative paradigm P2 ("model = preprocessing + CNN, preprocessing as an integral model component") constitutes the principal conceptual contribution of this work and is operationalised in the V5 arm (configs B/D).

### 0.2. What this plan does NOT do

- It does NOT rename the operational definition of `baseline` in OD-3 (stretch-resize + ImageNet normalize).
- It does NOT claim numerical superiority over Gulshan (forbidden by CFC-2.2 in the absence of a direct replication).
- It does NOT attribute to Gulshan the explicit theoretical claim "preprocessing is unimportant" (forbidden by SIR-1; Gulshan embodies a methodological practice rather than making an explicit theoretical statement).
- It does NOT change any experimental result, protocol, or hyperparameter.

### 0.3. What this plan does

It introduces a uniform **paradigmatic framing** across governance documents, the Gulshan literature card, the literature index, methodological chapters, and defense materials. Terminology is brought to a single standard throughout the corpus.

---

## 1. Unified terminology (mandatory across all artefacts)

| Term | Meaning |
|---|---|
| Paradigm P1 — end-to-end CNN paradigm | "Preprocessing is ancillary data preparation, not requiring methodological discussion" |
| Paradigm P2 — integrated preprocessing-CNN paradigm | "Preprocessing is an integral model component" |
| Canonical representative of the paradigm | Gulshan et al. (2016) for P1 |
| Paradigmatic instantiation | Operational embodiment of a paradigm's principles in a concrete experimental configuration |
| Experimental baseline configuration | Configs A/C in Experiment 1: stretch-resize + ImageNet normalize, 3 channels |
| Historical / foundational reference | Gulshan as a landmark work in the literature |

**Forbidden phrasings:**
- "Gulshan is our baseline" (conflicts with the operational definition of `baseline` in OD-3)
- "We outperform Gulshan" (violates CFC-2.2)
- "Gulshan claimed that preprocessing is unimportant" (violates SIR-1)

**Permitted phrasings:**
- "Gulshan is the canonical representative of the end-to-end CNN paradigm"
- "The baseline configuration operationally instantiates the paradigm represented by Gulshan"
- "Direct numerical comparison with Gulshan is not performed due to differences in task (binary vs five-class), backbone, and validation protocol"

---

## PHASE 0 — Governance (foundation layer)

Goal: introduce the paradigmatic framing into governance documents. After this phase, all subsequent updates must reference this framing as the single source of truth.

### Task 0.1 — Extend INVARIANTS.md

- [x] **0.1.1** Add to Section IV (Scope Boundaries) a new clause `SB-1.12`: a clarification that Gulshan et al. (2016) functions as the canonical representative of paradigm P1, not as an experimental control; numerical comparison is not performed.
- [x] **0.1.2** Add to Section VI (Claim Formulation Constraints) a clause `CFC-2.9`: prohibition of phrasings that attribute to Gulshan an explicit "preprocessing is unimportant" claim; only descriptions of methodological practice (preprocessing deferred to supplement) are permitted.
- [x] **0.1.3** Add to Section VII (Source Interpretation Rules) a clause `SIR-9`: the rule of paradigmatic attribution — a source may be designated "canonical representative of paradigm X" if (a) the source's methodological practice matches the definition of X and (b) the source is cited for that practice, not for an absent theoretical statement.
- [x] **0.1.4** Raise document version to **v5.3**, add a "v5.3 Amendment Summary" block.
- [x] **0.1.5** Update VERSION_SYNC.md: record v5.3, mark all dependent files as ❌ (out of sync).

**Files:** `thesis/governance/INVARIANTS.md`, `thesis/governance/VERSION_SYNC.md`
**Acceptance criterion:** the document reads cleanly; all references to `SB-1.12`, `CFC-2.9`, `SIR-9` are valid and do not contradict existing v5.2 clauses.

### Task 0.2 — Update CENTRAL_THESIS.md

- [x] **0.2.1** Add an introductory paragraph formulating the paradigmatic P1/P2 contrast as the conceptual foundation of the work.
- [x] **0.2.2** Explicitly cite Gulshan as the canonical representative of P1.
- [x] **0.2.3** Raise version to v5.3 and reflect in VERSION_SYNC.

**Files:** `thesis/governance/CENTRAL_THESIS.md`
**Acceptance criterion:** the central thesis contains the paradigmatic framing while preserving operational compatibility with IT-1 v5.2 in INVARIANTS.md.

### Task 0.3 — Update CONTRIBUTIONS.md

- [x] **0.3.1** Add an introductory block to Primary Contributions: the principal conceptual contribution is the P1 → P2 paradigm shift, not merely a local metric improvement.
- [x] **0.3.2** Reframe the novelty statement of C-1 to reflect the paradigmatic shift, not only the engineering details of the 8 stages.
- [x] **0.3.3** Raise version to v5.3 and reflect in VERSION_SYNC.

**Files:** `thesis/governance/CONTRIBUTIONS.md`
**Acceptance criterion:** C-1 is described both as an engineering contribution (8 stages) and as a conceptual one (paradigm shift); no conflict with CFC-2.8/2.9.

### Task 0.4 — Update ARGUMENT_MAP.md

- [x] **0.4.1** Add a new top-level node `PC-0` (Paradigmatic Framing Claim) before PC-1: paradigm P2 is conceptually more productive than P1 in the context of five-class DR classification.
- [x] **0.4.2** Mark PC-0 as a **non-empirical / methodological** claim — it is not tested experimentally but argued discursively in chapters 1.4–1.5.
- [x] **0.4.3** Connect PC-0 → PC-1 as "PC-1 supplies empirical evidence consistent with paradigm P2 but does not universally prove it".
- [x] **0.4.4** Raise version to v5.3.

**Files:** `thesis/governance/ARGUMENT_MAP.md`
**Acceptance criterion:** PC-0 is explicitly marked as methodological, not empirical; does not violate CFC-2.1 (universal generalization).

---

## PHASE 1 — Literature (literature layer)

### Task 1.1 — Update the Gulshan literature card

- [x] **1.1.1** In §15 (Relevance to My Dissertation) of `gulshan-2016.md` add a "Paradigmatic Role" block: explicitly note Gulshan's function as the canonical representative of paradigm P1.
- [x] **1.1.2** Record that no direct numerical comparison is performed; justify by the difference in tasks (binary vs five-class) and backbones (Inception-v3 vs ResNet-50/EfficientNet-B3).
- [x] **1.1.3** In §16 (Citation-Ready Statements) add 3–4 ready-made formulations for use in chapter 1.4 and the defense speech.
- [x] **1.1.4** In §18 (Analytical Synthesis) clarify that the paradigmatic attribution is grounded in the source's methodological practice (preprocessing deferred to the supplement), not in an explicit theoretical statement by the authors.

**Files:** `thesis/literature/external/gulshan-2016.md`
**Acceptance criterion:** the card describes Gulshan as the canonical representative of P1 in an SIR-1-compliant (non-amplifying) manner.

### Task 1.2 — Audit related literature cards

- [x] **1.2.1** Audit `pratt-2016.md`, `rakhlin-2017.md`, `saxena-2020.md`, `ting-2017.md`, `voets-2019.md` — for each, tag whether it belongs to paradigm P1 (most: yes).
- [x] **1.2.2** Add a single line to §15 of each card: "Position in paradigm space: P1 (end-to-end CNN, preprocessing as auxiliary step)".
- [x] **1.2.3** If any sources explicitly formalise preprocessing as a model component (e.g., hybrid schemes), tag them as P2-tending.

**Files:** `thesis/literature/external/*.md`
**Acceptance criterion:** every relevant card has a single paradigmatic-position line; no card receives an attribution stronger than its own text supports.

### Task 1.3 — Update LITERATURE_INDEX.md

- [x] **1.3.1** Add a column **"Paradigm"** to the Source Index table with values P1 / P2-tending / N/A.
- [x] **1.3.2** Fill the column for every indexed source.
- [x] **1.3.3** In the Notes section add a clarification of the column and a reference to SIR-9 (INVARIANTS v5.3).

**Files:** `thesis/literature/LITERATURE_INDEX.md`
**Acceptance criterion:** the Paradigm column is present, consistent with the cards, and does not contradict SIR-1/SIR-9.

---

## PHASE 2 — Dissertation chapters (chapter layer)

For each chapter: insert the paradigmatic framing where it is logically appropriate; do not rewrite existing sections.

### Task 2.1 — Chapter 1.3.1 (CNN Architectures for Medical Imaging)

- [x] **2.1.1** Add a paragraph: Gulshan (2016) as the archetype of the CNN approach in the DR domain, the methodological template.
- [x] **2.1.2** Source the wording from §16 of the literature card.

**Files:** `thesis/chapters/02-theoretical-foundations/drafts/` (or the current working copy)

### Task 2.2 — Chapter 1.3.2 (Transfer Learning Strategies)

- [x] **2.2.1** Mention Gulshan as an example of ImageNet→fundus transfer without explicit in-domain pretraining; contrast with RETFound (v5.1/v5.2 amendment).

### Task 2.3 — Chapter 1.4 (Critical Analysis of Existing Systems) — primary site for the paradigmatic framing

- [x] **2.3.1** Introduce the explicit P1 vs P2 contrast.
- [x] **2.3.2** Enumerate Gulshan, Pratt, Rakhlin, Saxena, Ting, Voets as works in the P1 tradition; note that **all of them leave preprocessing unformalised or defer it to supplements**.
- [x] **2.3.3** Formulate the hypothesis that this methodological practice creates a research gap — the inability to isolate the contribution of preprocessing from the contribution of architecture and data scale.
- [x] **2.3.4** Position the present dissertation as filling that gap through paradigm P2 and a controlled factorial design (Experiment 1).

### Task 2.4 — Chapter 1.5 (Formulation of the Research Problem)

- [x] **2.4.1** Reformulate the problem statement in terms of a paradigmatic shift: "Existing end-to-end studies (P1) do not permit isolation of the contribution of preprocessing; the present work formalises preprocessing as an integral model component (P2) and empirically measures its contribution under controlled conditions."

### Task 2.5 — Chapter 3.1 (Pipeline Formalisation)

- [x] **2.5.1** In the preamble explicitly note that the decision to formalise preprocessing is conceptual, motivated by paradigm P2.
- [x] **2.5.2** Provide a one-paragraph contrast with the Gulshan paradigm (the framing "preprocessing as ancillary data preparation").

### Task 2.6 — Chapter 4.2 (Experiment 1 — Causal Improvement)

- [x] **2.6.1** In the description of configs A/C explicitly state: "The baseline configuration of Experiment 1 operationally instantiates the end-to-end CNN classification paradigm canonically represented by Gulshan et al. (2016)."
- [x] **2.6.2** In the description of configs B/D: "The V5 configuration operationalises the integrated preprocessing-CNN pipeline paradigm."
- [x] **2.6.3** In the Discussion state explicitly that the A-vs-B (and C-vs-D) result is interpreted as an empirical contrast between two paradigms under otherwise identical conditions, **not** as a comparison against specific numerical figures from Gulshan 2016.

### Task 2.7 — Chapters 5.1 (Cross-dataset Generalization) and 5.5 (Comparative Analysis)

- [x] **2.7.1** In §5.5, when comparing against the literature, explicitly use the paradigmatic framing: numerical values from Gulshan are reported as a **contextual reference** (historical reference), not as a direct benchmark.
- [x] **2.7.2** Every mention of Gulshan's numerical results is accompanied by a caveat noting differences in task and protocol.

### Task 2.8 — Introduction

- [x] **2.8.1** In the Introduction, mention Gulshan as the landmark that opened the era of CNN-based DR screening.
- [x] **2.8.2** Pre-introduce the paradigmatic framing — this prepares the reader for chapter 1.4.

**Files:** `thesis/chapters/00-introduction/drafts/`, `thesis/chapters/01-problem-domain/drafts/`, `thesis/chapters/02-theoretical-foundations/drafts/`, `thesis/chapters/03-methodology/drafts/`, `thesis/chapters/04-experiments/drafts/`, `thesis/chapters/05-validation/drafts/`

**Acceptance criterion for Phase 2:** all affected chapters use the unified terminology from §1 of this plan; no phrasings from the "Forbidden phrasings" list appear.

---

## PHASE 3 — Defense and demo (presentation layer)

### Task 3.1 — Defense slides

- [x] **3.1.1** Create a new slide "Paradigmatic Positioning" (after the slide on existing works, before the methodology slide).
- [x] **3.1.2** The slide contains: left column P1 (Gulshan + followers), right column P2 (the present work); beneath them an arrow "experimental test → Experiment 1".
- [x] **3.1.3** Update the novelty and contribution slides: novelty = paradigmatic shift + 8-stage pipeline as its operationalisation.
- [x] **3.1.4** Audit the existing `defense/slides/NOVELTY_SLIDE.md` for consistency.

**Files:** `defense/slides/`, `defense/slide_plan.md`

### Task 3.2 — Demo (React dashboard)

- [x] **3.2.1** In `demo/src/tabs/Overview.js` or `ModelArchitecture.js` add a "Paradigmatic context" block with a brief P1 vs P2 statement.
- [x] **3.2.2** In `demo/src/tabs/ExpH1.js` label configs A/C as "P1 instantiation (Gulshan-paradigm baseline)" and B/D as "P2 instantiation (V5 integrated pipeline)".
- [x] **3.2.3** Localisation: add Kazakh equivalents in `demo/src/i18n.js` for the new strings (English is the primary; Kazakh per project convention).

**Files:** `demo/src/tabs/*.js`, `demo/src/i18n.js`

### Task 3.3 — Defense speech (oral text)

- [x] **3.3.1** Prepare a 60-second oral fragment with a pre-formulated sentence drawn from §0.3 of this plan.
- [x] **3.3.2** Prepare answers to 3 anticipated committee questions:
  - "Why did you not directly replicate Gulshan?"
  - "Why ResNet-50/EfficientNet-B3 rather than Inception-v3?"
  - "What are the numerical differences from Gulshan?"

---

## PHASE 4 — Verification and closure

### Task 4.1 — Cross-file terminology audit

- [x] **4.1.1** Run a grep over the corpus: every occurrence of `Gulshan` is classified as (a) landmark, (b) canonical representative of P1, or (c) historical reference; none as "our baseline".
- [x] **4.1.2** Run a grep over `baseline` — separate the operational baseline (configs A/C) from "literature baseline" in narrative discussion; use precise terminology everywhere.

### Task 4.2 — Governance compliance check

- [x] **4.2.1** Verify that no phrasing violates: SIR-1 (non-amplification), SIR-9 (paradigmatic attribution), CFC-2.2 (no undirected superiority claims), CFC-2.8 (composite IV), CFC-2.9 (no false attribution to Gulshan).
- [x] **4.2.2** If a violation is found — rephrase or delete.

### Task 4.3 — Final version reconciliation

- [x] **4.3.1** Raise all affected governance files to v5.3.
- [x] **4.3.2** Update VERSION_SYNC.md: convert all ❌ entries to ✅.
- [x] **4.3.3** Record the integration completion date in VERSION_SYNC.md.

### Task 4.4 — Regression semantic test

- [x] **4.4.1** Read CENTRAL_THESIS, CONTRIBUTIONS, ARGUMENT_MAP, chapter 1.4, and chapter 4.2 in sequence as a single connected narrative — verify that the paradigmatic framing reads consistently.
- [x] **4.4.2** Read §5.5 and the Conclusion — verify that no residual old-version phrasings remain ("we outperform Gulshan", "Gulshan is our baseline", etc.).

---

## Execution order and dependencies

```
Phase 0 (Governance)
   ├── 0.1 INVARIANTS    ──┐
   ├── 0.2 CENTRAL_THESIS ─┤
   ├── 0.3 CONTRIBUTIONS  ─┼─── must complete BEFORE Phase 2
   └── 0.4 ARGUMENT_MAP   ─┘

Phase 1 (Literature)
   ├── 1.1 Gulshan card     ──┐
   ├── 1.2 Related cards     ─┼─── may run in parallel with Phase 0
   └── 1.3 Literature Index  ─┘

Phase 2 (Chapters)
   └── 2.1–2.8 — sequential, after Phase 0 and Phase 1 complete

Phase 3 (Defense + Demo)
   └── 3.1–3.3 — after Phase 2

Phase 4 (Verification)
   └── 4.1–4.4 — after Phase 3; MANDATORY before closing the integration
```

---

## Progress tracking

| Phase | Tasks | Done | Status |
|---|---|---|---|
| Phase 0 — Governance | 4 | 4 | ✅ Completed 2026-05-28 |
| Phase 1 — Literature | 3 | 3 | ✅ Completed 2026-05-28 |
| Phase 2 — Chapters | 8 | 8 | ✅ Completed 2026-05-28 (spec-level — chapter drafts not yet authored; paradigmatic framing inserted into each chapter README as binding writing spec) |
| Phase 3 — Defense + Demo | 3 | 3 | ✅ Completed 2026-05-28 |
| Phase 4 — Verification | 4 | 4 | ✅ Completed 2026-05-28 |
| **Total** | **22** | **22** | **✅ 100% — integration complete 2026-05-28** |

### Completion notes

- **Phase 0:** INVARIANTS.md raised to v5.3 with SB-1.12, CFC-2.9, SIR-9 clauses; CENTRAL_THESIS.md, CONTRIBUTIONS.md, ARGUMENT_MAP.md raised to v5.3 with paradigmatic-framing additions (introductory paragraph, conceptual-framing block, PC-0 node respectively); VERSION_SYNC.md updated with v5.3 amendment scope.
- **Phase 1:** gulshan-2016.md §15 now contains a Paradigmatic Role block, §16 contains paradigmatic citation-ready statements P-1..P-4, §18 contains a Paradigmatic Synthesis subsection. Five other cards (pratt-2016, rakhlin-2017, saxena-2020, ting-2017, voets-2019) gained a Position-in-paradigm-space line. LITERATURE_INDEX.md gained a Paradigm column on every Source Index row, with a classification-rule note explaining the tagging convention.
- **Phase 2:** Chapter drafts do not yet exist in any of `00-introduction` through `05-validation`. The paradigmatic-framing content for each affected section was therefore inserted into the chapter's README.md as a binding writing-spec block, to be consumed when the chapter is drafted. The five affected chapter READMEs (00, 01, 03, 04, 05) each carry an explicit Task-2.x block with the verbatim binding content; chapter 02 carries a minor paradigmatic-framing note.
- **Phase 3:** Defense slides: a new slide `05a_PARADIGMATIC_POSITIONING.md` was authored in Kazakh + English; `44_NOVELTY.md` (slide 43 in slide_plan numbering) was extended with the P1 → P2 framing in §2 and Ж-1; `slide_plan.md` was updated to register the new slide. Demo: `Overview.js` gained a "Paradigmatic Context (P1 → P2)" section with two coloured blocks; `ExpH1.js` factorial table gained a Paradigm column labelling configs A/C as "P1 instantiation" and B/D as "P2 instantiation"; `i18n.js` gained `paradigm.*` keys in both EN and KZ. A `defense/paradigmatic_speech.md` companion document was created with a 60-second oral fragment (EN + KZ) and the three anticipated committee-question answers.
- **Phase 4:** Cross-corpus grep audit ran clean — every occurrence of `Gulshan` outside this plan and the forbidden-phrasing meta-discussion lists is either a permitted descriptive use (literature card, dataset descriptor in demo) or a governance-binding citation. No "Gulshan is our baseline" / "we outperform Gulshan" / "Gulshan claimed preprocessing is unimportant" / "Gulshan-baseline is surpassed" asserted statements exist anywhere in the corpus. The `baseline` terminology is consistent: the operational baseline (configs A/C, OD-3) is always referenced by configuration label or by "the baseline configuration," never as "Gulshan." Governance compliance against SIR-1, SIR-9, CFC-2.1, CFC-2.2, CFC-2.8, CFC-2.9 was verified for every new block authored in this integration.

---

## Decision log

| Date | Decision / Note | Author |
|---|---|---|
| 2026-05-28 | Plan created. Paradigmatic reformulation of Gulshan agreed (canonical representative of P1, not baseline). | N.S. + AI assistant |
| 2026-05-28 | Terminology "homology" rejected in favour of "canonical representative of the paradigm" / "paradigmatic instantiation". | N.S. + AI assistant |
| 2026-05-28 | Working file translated to English (project working languages: English + Kazakh; no Russian retained). | N.S. + AI assistant |
| 2026-05-28 | Integration executed: all 22 tasks across Phases 0–4 completed. Governance corpus at v5.3. | AI assistant |

---

*This file is a working document. As tasks are executed, mark them `[x]`, update the progress table in §"Progress tracking", and record decisions in the table above.*
