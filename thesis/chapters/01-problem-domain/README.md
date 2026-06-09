# Chapter 1: Problem Domain Analysis

**Status:** Review prompt generated (v1.0, STALE — needs regeneration from V3.0 materials)
**Chapter function:** Literature review — landscape mapping, gap identification, research problem formulation
**Governance bindings:** CFC-2.2, CFC-2.4, NC-2, NC-3, SIR-1, SIR-3, SIR-4, SIR-5, SIR-8, **SB-1.12, CFC-2.9, SIR-9 (v5.3)**, **PC-0 (v5.3)**
**Key sources:** All 47 external literature cards + 6 self-citation cards

## Paradigmatic framing insertion (v5.3) — Tasks 2.1–2.4

This chapter is the **primary site** for the paradigmatic framing in the dissertation text. Binding content blocks per section:

### §1.3.1 (CNN Architectures for Medical Imaging) — Task 2.1
- Add a paragraph framing Gulshan et al. (2016) as the **archetype of the CNN approach in the DR domain** — the *methodological template* of the field: large training set + Inception-v3 backbone + multi-grader reference standard + dual external validation. Source wording: §16 *Citation-Ready Statements* of `thesis/literature/external/gulshan-2016.md`.
- Pratt 2016, Rakhlin 2017, Saxena 2020, Ting 2017, Voets 2019 are to be introduced as carriers of the same methodological template. The paradigm label (P1) is not yet introduced here — it is reserved for §1.4.

### §1.3.2 (Transfer Learning Strategies) — Task 2.2
- Mention Gulshan as an example of **ImageNet → fundus** transfer without explicit in-domain pretraining.
- Contrast with the dissertation's in-domain initialization (INVARIANTS v6.0.0 amendment): **ophthalmology-specific self-supervised pretraining** of the same CNN backbone on an unlabeled fundus corpus (CNN-compatible domain-adaptive SSL — DINO / BYOL / SimCLR / MoCo family). Retinal foundation models such as RETFound (Zhou et al. 2023, Nature) may be cited as related work, but are not adopted here — they change the backbone (ViT-Large) and would confound the preprocessing contrast.

### §1.4 (Critical Analysis of Existing Systems) — Task 2.3 — PRIMARY SITE FOR PARADIGMATIC FRAMING
- **2.3.1** Introduce the explicit **P1 vs P2** contrast (definitions from INVARIANTS v5.3 §I and CENTRAL_THESIS §Paradigmatic framing).
- **2.3.2** Enumerate Gulshan, Pratt, Rakhlin, Saxena, Ting, Voets as works in the P1 tradition. Each must be characterised by its *observable methodological practice* (preprocessing deferred to supplements; preprocessing treated as a tuning input; no preprocessing-vs-architecture decomposition). Per CFC-2.9 / SIR-1 / SIR-9, no theoretical "preprocessing is unimportant" statement may be attributed to these authors.
- **2.3.3** Formulate the **research gap**: the P1 methodological practice — leaving preprocessing unformalised or relegated to supplementary material — precludes isolating the contribution of preprocessing from the contribution of architecture and data scale.
- **2.3.4** Position the present dissertation as filling that gap through paradigm P2 (preprocessing as integral model component) and a controlled factorial design (Experiment 1, configs A/C vs. B/D).

### §1.5 (Formulation of the Research Problem) — Task 2.4
- Reformulate the problem statement in paradigmatic terms: "Existing end-to-end studies (P1) do not permit isolation of the contribution of preprocessing; the present work formalises preprocessing as an integral model component (P2) and empirically measures its contribution under controlled conditions on EyePACS."
- The P2 reformulation is non-empirical (PC-0 in ARGUMENT_MAP v5.3) but argues for the *productivity* of the paradigm shift, not its empirical superiority over P1 in all cases (forbidden by CFC-2.1).

### Cross-cutting forbidden phrasings (apply to every section of Chapter 1)
"Gulshan is our baseline" / "we outperform Gulshan" / "Gulshan claimed preprocessing is unimportant" / "the present work surpasses Gulshan numerically." See INVARIANTS v5.3 SB-1.12, CFC-2.9.

## Sections (per outline/TABLE_OF_CONTENTS_EN.md, v6.0.0)

# 1 PROBLEM DOMAIN ANALYSIS AND CURRENT STATE OF AUTOMATED DIABETIC RETINOPATHY DIAGNOSIS

## 1.1 Medical and Epidemiological Context of Diabetic Retinopathy
- 1.1.1 Pathophysiology and Clinical Grading Systems
- 1.1.2 Screening Requirements in Resource-Limited Healthcare Settings

## 1.2 Fundus Image Acquisition and Quality Variability
- 1.2.1 Sources of Image Degradation in Clinical Practice
- 1.2.2 Impact of Image Quality on Diagnostic Model Performance
- 1.2.3 Device-Specific Variability in Fundus Imaging

## 1.3 Deep Learning Approaches to Retinal Image Classification
- 1.3.1 Convolutional Neural Network Architectures for Medical Imaging
- 1.3.2 Transfer Learning and Self-Supervised Pretraining in Ophthalmic Diagnostics
- 1.3.3 Explainability Methods in Medical Image Classification

## 1.4 Critical Analysis of Existing Automated DR Screening Systems

## 1.5 Formulation of the Research Problem and Justification of Research Direction

- Conclusions to Chapter 1
