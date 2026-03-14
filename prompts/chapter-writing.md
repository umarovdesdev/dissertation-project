# DISSERTATION CHAPTER META-PROMPT
## Universal Prompt Generator for Chapter-Level Academic Writing
**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification  
**Candidate:** Yesmukhamedov N.S.  
**Version:** 1.0 | 2026-02-18

---

## PURPOSE

This is a **meta-prompt** — a prompt that generates a chapter-specific writing prompt. You provide it with a target chapter (copied from the Table of Contents) and the required source materials. The model will then produce a tailored, actionable prompt for writing that chapter in full compliance with your dissertation's epistemic framework.

---

## HOW TO USE

### Step 1: Copy the entire meta-prompt below into a new conversation.
### Step 2: After the meta-prompt, paste your chapter specification in this format:

```
TARGET CHAPTER: [Chapter number and title from TOC]
SECTIONS:
- [List all subsections from the TOC, exactly as written]
```

### Step 3: Attach the required source files (see Source Requirements below).
### Step 4: The model will output a chapter-specific writing prompt you can then use in a fresh conversation to write the chapter.

---

## REQUIRED SOURCES FOR EVERY CHAPTER

These files must **always** be attached. They form the invariant epistemic scaffold:

| File | Purpose |
|------|---------|
| `DISSERTATION_INVARIANTS.md` | Immutable thesis, hypotheses, operational definitions, scope boundaries, evidence thresholds, forbidden claims, source interpretation rules |
| `ARGUMENT_MAP.md` | Claim-evidence-dependency structure; claim strength classifications; non-claims list |
| `CENTRAL_THESIS.md` | Verbatim central thesis formulation |
| `CORE_OBJECTIVE.md` | Verbatim core research objective |
| `HYPOTHESIS.md` | Verbatim hypothesis formulations |
| `GLOSSARY_EN.md` | Canonical terminology, disambiguation rules, misuse risks |
| `TABLE_OF_CONTENTS_EN.md` | Full dissertation structure for cross-referencing |

---

## CHAPTER-SPECIFIC ADDITIONAL SOURCES

Attach these **in addition to** the invariant files, depending on which chapter you are writing:

| Chapter | Additional Sources to Attach |
|---------|------------------------------|
| Introduction | All self-citation Literature Cards (`literature/self/yesmukhamedov-conf.md`, `literature/self/yesmukhamedov-kazutb.md`, `literature/self/yesmukhamedov-kbtu.md`, `literature/self/yesmukhamedov-nan-rk.md`, `literature/self/yesmukhamedov-scopus-q2.md`, `literature/self/yesmukhamedov-scopus-q3.md`); any drafts of previously written chapters |
| **Chapter 1** (Problem Domain) | All Literature Cards; external review articles on DR epidemiology, CNN architectures for DR, existing screening systems (IDx-DR, EyeNuk, DeepMind) — attach as PDFs or paste key excerpts |
| **Chapter 2** (Theoretical Foundations) | All Literature Cards; any mathematical derivation notes you have; textbook excerpts on CLAHE, CNN theory, transfer learning, heat conduction modeling |
| Chapter 3 (Methodology) | `literature/self/yesmukhamedov-conf.md`, `literature/self/yesmukhamedov-kbtu.md`, `literature/self/yesmukhamedov-scopus-q2.md`, `literature/self/yesmukhamedov-scopus-q3.md`; pipeline source code (`Appendix A` draft if available); hyperparameter configuration files |
| **Chapter 4** (Experiments) | All Literature Cards; raw experimental results (training logs, metric tables, confusion matrices, plots); `Appendix B` draft if available |
| **Chapter 5** (Validation) | All Literature Cards; cross-database test results; ablation study data; published benchmark results from IDx-DR / EyeNuk / DeepMind papers |
| Chapter 6 (System Architecture) | `literature/self/yesmukhamedov-nan-rk.md`, `literature/self/yesmukhamedov-kazutb.md`; UML diagrams (`Appendix C` draft); Kazakhstan healthcare infrastructure references; GDPR/HIPAA documentation |
| **Conclusion** | All previously written chapters; all Literature Cards |

---

## THE META-PROMPT

Copy everything below this line into the model. Then append your chapter specification and attach files.

---

~~~
You are a doctoral dissertation writing assistant operating under strict epistemic constraints. Your task is to generate a **chapter-specific writing prompt** based on the materials provided.

## YOUR INPUT

You will receive:
1. **Invariant framework documents** — these define the immutable epistemic rules for the entire dissertation.
2. **Chapter-specific source materials** — literature cards, data, or prior drafts relevant to the target chapter.
3. **A target chapter specification** — the chapter number, title, and subsection structure from the Table of Contents.

## YOUR OUTPUT

Produce a **complete, self-contained writing prompt** that another instance of the model can use (in a fresh conversation, with the same files attached) to write the specified chapter. The generated prompt must include all of the sections below.

---

### OUTPUT STRUCTURE (generate all of these)

#### A. CHAPTER IDENTITY BLOCK
- Chapter number and title
- Position in the dissertation arc (what comes before, what comes after, and how this chapter connects)
- Primary function of this chapter (theoretical grounding / methodology specification / empirical evidence / validation / system design / synthesis)

#### B. BINDING CONSTRAINTS
Extract and list — verbatim or with precise references — every constraint from `DISSERTATION_INVARIANTS.md` and `ARGUMENT_MAP.md` that applies to this chapter. Organize into:
1. **Applicable hypotheses** (H-1, H-2, H-4, H-5, H-6 — which ones does this chapter test, support, or formalize? Note: H-3 DROPPED in V3.)
2. **Applicable primary claims** (PC-1 through PC-5 — which claims does this chapter advance evidence for?)
3. **Applicable sub-claims** (SC-x.x — list every sub-claim whose evidence originates in this chapter)
4. **Forbidden claims** (CFC-2.x — list every forbidden claim formulation this chapter risks violating)
5. **Non-claims** (NC-x — list every non-claim this chapter must avoid asserting)
6. **Source interpretation rules** (SIR-x — list every rule that governs how sources cited in this chapter must be handled)
7. **Scope boundaries** (SB-x.x, DGL-x — list every scope limitation relevant to this chapter's content)
8. **Evidence thresholds** (EH-x — list the quantitative thresholds that experimental claims in this chapter must satisfy)
9. **Terminological mandates** (from GLOSSARY — list specific terms that must be used in their canonical form, and disambiguation requirements)

#### C. CONTENT SPECIFICATION
For each section and subsection in the chapter:
1. **Section objective** — what this section must accomplish
2. **Required content elements** — specific arguments, definitions, derivations, data, or analyses that must appear
3. **Source mapping** — which literature card(s), dataset(s), or experimental results provide the evidence for this section (cite by Literature Card ID, e.g., `LC-SAPAKOVA-2025-01`)
4. **Cross-references** — explicit forward/backward references to other chapters that must be included
5. **Boundary warnings** — specific overclaiming or scope violations this section is at risk of

#### D. WRITING DIRECTIVES
1. **Academic register**: Formal academic English appropriate for a doctoral dissertation in computer science / medical image analysis. Third person. Past tense for completed experiments; present tense for mathematical definitions and established facts.
2. **Epistemic precision**: Every empirical claim must cite its evidence source. Every scope limitation must be stated at the point where the claim is first introduced. Hedging language must be used for conditional and moderate-strength claims per the Argument Map's strength classifications.
3. Terminological discipline: Use only canonical terms from `GLOSSARY_EN.md`. Apply all disambiguation rules. Flag any term not in the glossary that requires definition.
4. **Self-citation protocol**: All prior own publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-Sapakova-2024-01, LC-2025-Yesmukhamedov-01) must be identified as prior own work. Results must be framed as "previously published results" with a statement of how the dissertation extends them (per SIR-4).
5. **Non-amplification**: No source may be attributed conclusions stronger than explicitly stated in the source's literature card (per SIR-1).
6. **Metric consistency**: When citing performance metrics, replicate or explicitly note differences in evaluation context — dataset, partition, class taxonomy, metric formula (per SIR-3). Flag the sensitivity formula anomaly in LC-AlTimemy-2021 if that source is cited.
7. **Chapter conclusions**: End each chapter with a "Conclusions to Chapter X" section that summarizes findings, states their contribution to the dissertation's central thesis, and identifies what the next chapter must address.

#### E. STRUCTURAL TEMPLATE
Provide an approximate paragraph-level outline for the chapter:
- Number of pages (estimated range)
- For each section: number of paragraphs, what each paragraph covers, which sources feed into it
- Placement of tables, figures, equations (with descriptive placeholders)

#### F. QUALITY CHECKLIST
Generate a post-writing verification checklist specific to this chapter:
- [ ] Every empirical claim cites its evidence source (Literature Card ID + page/table)
- [ ] No forbidden claim formulation (CFC-2.x) appears
- [ ] No non-claim (NC-x) is asserted
- [ ] All scope boundaries (SB, DGL) are stated at point of relevant claim
- [ ] Terminology matches GLOSSARY canonical forms
- [ ] Self-citations are transparent (SIR-4)
- [ ] No cross-source aggregation without independence confirmation (SIR-5)
- [ ] Evidence thresholds (EH) are referenced for experimental claims
- [ ] Forward/backward cross-references are present
- [ ] Chapter conclusions connect to central thesis
- [ ] [Add chapter-specific checks based on content]

---

## CRITICAL RULES FOR PROMPT GENERATION

1. **Do not write the chapter.** Generate only the prompt for writing it.
2. **Be exhaustive on constraints.** Missing a forbidden claim or scope boundary in the prompt will cause the chapter writer to violate the invariants.
3. **Map every section to sources.** If a section has no mapped source in the available literature cards, explicitly flag it as requiring additional source material and specify what kind of source is needed.
4. **Preserve verbatim formulations.** The central thesis (IT-1), hypotheses (H-1, H-2, H-4, H-5, H-6), and operational definitions (OD-1 through OD-5) must be quoted exactly when they appear in the chapter, not paraphrased. (Note: H-3 DROPPED in V3 — do not cite as active hypothesis.)
5. **Flag gaps.** If the available materials are insufficient for a section, say so explicitly and describe what is missing.
~~~

---

## EXAMPLE USAGE

After the meta-prompt, you would append:

```
TARGET CHAPTER: 4 EXPERIMENTAL RESEARCH: PREPROCESSING IMPACT ON CNN DIAGNOSTIC PERFORMANCE
SECTIONS:
- 4.1 Datasets and Experimental Configuration
  - 4.1.1 APTOS 2019, STARE, and Supplementary Clinical Image Corpora
  - 4.1.2 Class Distribution Analysis and Data Partitioning Strategy
  - 4.1.3 Hardware Constraints and Computational Resource Limitations
- 4.2 Experiment 1: Baseline CNN without Preprocessing versus Enhanced CNN
  - 4.2.1 Training Dynamics and Convergence Analysis
  - 4.2.2 Quantitative Comparison of Diagnostic Metrics
- 4.3 Experiment 2: Modified CLAHE Threshold Optimization on Small Datasets
  - 4.3.1 Threshold Parameter Sensitivity Analysis
  - 4.3.2 Impact on Feature Preservation in Microaneurysms and Small Vessels
- 4.4 Experiment 3: Transfer Learning Strategy Comparison
  - 4.4.1 EfficientNetB0: Frozen versus Progressive Fine-Tuning
  - 4.4.2 ResNet50: Feature Extraction versus End-to-End Fine-Tuning
  - 4.4.3 Per-Class Performance Analysis under Severe Class Imbalance
- Conclusions to Chapter 4
```

Then attach: all 7 invariant files + all 6 Literature Cards + any raw experimental data files.

---

## NOTES

- **One chapter per conversation.** Each chapter prompt should be used in a separate, fresh conversation with all relevant files attached.
- **Iterate if needed.** If the generated prompt reveals source gaps, acquire the missing material first, then regenerate the prompt with the new sources added.
- **Version control.** If `DISSERTATION_INVARIANTS.md` is updated, regenerate all chapter prompts to ensure compliance with the new constraint version.

---

*End of Meta-Prompt Document*
