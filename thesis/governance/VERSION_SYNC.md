# VERSION SYNCHRONIZATION REGISTER

**Version:** 5.3 | **Date:** 2026-05-28

## v5.3 Amendment Scope

Paradigmatic framing introduced. Two paradigms recognised: **P1** (end-to-end CNN; preprocessing as ancillary data preparation) and **P2** (integrated preprocessing-CNN; preprocessing as integral model component). Gulshan et al. (2016) designated canonical representative of P1 (per the methodological-practice criterion in SIR-9). New governance clauses: **SB-1.12** (Gulshan is not a numerical benchmark, baseline is operational construct per OD-3), **CFC-2.9** (forbids false attribution of "preprocessing is unimportant" claim to Gulshan or other P1 sources), **SIR-9** (paradigmatic-attribution rule). PC-0 (Paradigmatic Framing Claim) added to ARGUMENT_MAP as a non-empirical methodological claim feeding into IT-1. CENTRAL_THESIS gains an introductory paradigmatic-framing paragraph. CONTRIBUTIONS gains an introductory conceptual-framing block and a reframed C-1 novelty statement. No operational definitions, hypotheses, or experimental protocols are modified. The integration tracker is `GULSHAN_PARADIGM_INTEGRATION_PLAN.md` at the repository root.

## v5.2 Amendment Scope

Refinement of the RETFound pretraining-corpus description. The V5 arm of Experiment 1 is now described as initialized from RETFound, a foundation model **MAE-pretrained on a multi-modal retinal imaging corpus** comprising ≈904K color fundus photographs (CFP) + ≈736K optical coherence tomography (OCT) scans (~1.6M total) per Zhou et al. 2023, Nature. The dissertation's V5 arm loads the **CFP-pretrained checkpoint** specifically; the multi-modal description characterizes the foundation model at the publication level and does not extend the dissertation's input domain to OCT (SB-1.4 in INVARIANTS.md remains in force). The composite independent variable, CFC-2.8, and the AOQ-1 through AOQ-4 open questions from v5.1 are unchanged.

## v5.1 Amendment Scope (historical)

Pretraining source amendment: V5 arm of Experiment 1 uses RETFound; baseline arm retains ImageNet. H-1 reformulated as Integrated Pipeline Dominance with composite independent variable. See INVARIANTS.md v5.1 Section X for open operational questions (AOQ-1 through AOQ-4).

## File Version Status

| File | Version | Synced |
|------|---------|--------|
| governance/INVARIANTS.md | 5.3 | ✅ — v5.3 amendment: paradigmatic framing (SB-1.12, CFC-2.9, SIR-9) — completed 2026-05-28 |
| governance/HYPOTHESIS.md | 5.2 | ⚠️ — no v5.3 hypothesis changes; review only for any phrasings touching Gulshan/baseline conflation |
| governance/RESEARCH_ARCHITECTURE.md | 5.2 | ⚠️ — no v5.3 experimental-design changes; review only for paradigmatic phrasings if any |
| governance/VERSION_SYNC.md | 5.3 | ✅ |
| governance/ARGUMENT_MAP.md | 5.3 | ✅ — v5.3 amendment: PC-0 (Paradigmatic Framing Claim, methodological) added as top-level node — completed 2026-05-28; v5.1/v5.2 H-1 reframing not yet propagated (separate work item, see note) |
| governance/CONTRIBUTIONS.md | 5.3 | ✅ — v5.3 amendment: conceptual-framing block + reframed C-1 novelty (paradigm shift + 8-stage engineering) — completed 2026-05-28; v5.1/v5.2 CFC-2.8 reframing not yet propagated (separate work item) |
| governance/CENTRAL_THESIS.md | 5.3 | ✅ — v5.3 amendment: introductory paradigmatic-framing paragraph — completed 2026-05-28; v5.1/v5.2 pretrain-symmetry phrasing not yet propagated (separate work item) |
| literature/external/gulshan-2016.md | v5.3 sync ✅ | ✅ — v5.3: §15 Paradigmatic Role block + §16 Paradigmatic citation-ready statements + §18 Paradigmatic Synthesis — completed 2026-05-28 |
| literature/external/pratt-2016.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/external/rakhlin-2017.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/external/saxena-2020.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/external/ting-2017.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/external/voets-2019.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/LITERATURE_INDEX.md | v5.3 sync (Paradigm column) ✅ | ✅ — v5.3: Paradigm column added to Source Index; classification rule documented in Notes — completed 2026-05-28. v5.1/v5.2 RETFound card creation remains a separate work item (not part of v5.3 paradigmatic scope). |
| chapters/00-introduction/README.md | v5.3 spec ✅ | ✅ — Task 2.8 paradigmatic-framing block added |
| chapters/01-problem-domain/README.md | v5.3 spec ✅ | ✅ — Tasks 2.1–2.4 paradigmatic-framing block added (primary site for paradigmatic discussion) |
| chapters/02-theoretical-foundations/README.md | v5.3 spec ✅ | ✅ — v5.3 paradigmatic-framing note added |
| chapters/03-methodology/README.md | v5.3 spec ✅ | ✅ — Task 2.5 paradigmatic-framing block added |
| chapters/04-experiments/README.md | v5.3 spec ✅ | ✅ — Task 2.6 paradigmatic-framing block added (Experiment 1 A/C and B/D paradigmatic labelling) |
| chapters/05-validation/README.md | v5.3 spec ✅ | ✅ — Task 2.7 paradigmatic-framing block added (§5.5 caveat block for Gulshan numerical figures) |
| defense/slides/05a_PARADIGMATIC_POSITIONING.md | v5.3 ✅ NEW | ✅ — Task 3.1 new paradigmatic positioning slide created |
| defense/slides/44_NOVELTY.md | v5.3 ✅ | ✅ — Task 3.1.3 novelty slide updated with P1 → P2 framing |
| defense/slide_plan.md | v5.3 ✅ | ✅ — paradigmatic positioning slide registered in plan |
| defense/paradigmatic_speech.md | v5.3 ✅ NEW | ✅ — Task 3.3 defense speech + anticipated Q&A created |
| demo/src/tabs/Overview.js | v5.3 ✅ | ✅ — Task 3.2.1 paradigmatic context block added |
| demo/src/tabs/ExpH1.js | v5.3 ✅ | ✅ — Task 3.2.2 P1/P2 paradigm column added to factorial table |
| demo/src/i18n.js | v5.3 ✅ | ✅ — Task 3.2.3 paradigm.* keys added in EN and KZ |
| governance/CORE_OBJECTIVE.md | 5.0 | ⚠️ — review for pretrain references AND paradigmatic phrasings |
| outline/MASTER_OUTLINE.md | 5.0 | ❌ — chapter outlines that frame H-1 must be updated AND paradigmatic framing inserted in ch 1.4 / 1.5 |
| outline/TABLE_OF_CONTENTS_EN.md | 5.0 | ⚠️ — likely unchanged but verify |
| outline/TABLE_OF_CONTENTS_KZ.md | 5.0 | ⚠️ — likely unchanged but verify |
| glossary/GLOSSARY_EN.md | 5.0 | ❌ — add RETFound terms (v5.1/v5.2) AND paradigm P1, paradigm P2, canonical representative, paradigmatic instantiation (v5.3) |
| glossary/GLOSSARY_KZ.md | 5.0 | ❌ — Kazakh equivalents for new glossary terms |
| literature/LITERATURE_INDEX.md | 5.0 | ❌ — Zhou et al. 2023 (RETFound) card AND Paradigm column (v5.3) — see GULSHAN_PARADIGM_INTEGRATION_PLAN.md Task 1.3 |
| literature/external/gulshan-2016.md | 5.0 | ❌ — Paradigmatic Role block required in §15 (v5.3) — see Task 1.1 |
| experiments/experimental-protocol.md | 5.0 | ❌ — Exp 1 protocol must reflect v5.1 configurations and AOQ-1/2 resolutions |
| methods/preprocessing-pipeline.md | 5.0 | ⚠️ — preprocessing stages unchanged; review for pretrain references |
| methods/implementation.md | 5.0 | ❌ — model loading code paths must accommodate RETFound CFP-checkpoint weights |

## Downstream Code Status (not part of governance, listed for completeness)

| Path | Sync status |
|------|-------------|
| experiments/configs/default.yaml | Out of sync — `pretrained: true` lines and `imagenet_*` keys must accommodate the V5 arm (RETFound CFP checkpoint per v5.2) |
| experiments/src/models/factory.py | Out of sync — no RETFound loader |
| experiments/src/models/resnet.py | Out of sync if AOQ-1 resolves to option (a) ViT-Large |
| experiments/src/models/efficientnet.py | Out of sync if AOQ-1 resolves to option (a) |
| demo/src/tabs/ModelArchitecture.js | Updated 2026-05-28 — V5 arm row (RETFound CFP-pretrained, multi-modal corpus) added to architecture table |
| defense/slides/08_CNN_ARCHITECTURE.md | Updated 2026-05-28 — disambiguated baseline/V5 pretrain sources |
| defense/slides/09_ARCHITECTURE_COMPARISON.md | Updated 2026-05-28 — pretrain source clarified in factorial table |

Per the user's 2026-05-13 directive: governance v5.1 was the authoritative reference; v5.2 (2026-05-28) refines RETFound corpus to multi-modal CFP + OCT. v5.3 (2026-05-28) introduces the paradigmatic framing (P1 / P2; Gulshan as canonical representative of P1). v5.3 is a *purely additive* governance amendment: no v5.2 binding is reversed, and no hypothesis or operational definition is modified. Downstream code and dependent governance files will be brought into sync in subsequent passes; the v5.3 integration tracker is `GULSHAN_PARADIGM_INTEGRATION_PLAN.md` at the repository root.

## Sync Protocol

Before any chapter-writing session:
1. Verify all governance files marked ✅ are at version 5.3 (current authoritative version).
2. Files marked ❌ must not be cited as authoritative until brought to v5.3.
3. AOQ-1 through AOQ-4 (INVARIANTS v5.1/v5.2 Section X) must be resolved before Experiment 1 execution.
4. The v5.3 paradigmatic-framing constraints (SB-1.12, CFC-2.9, SIR-9) bind every chapter, slide, and demo update from 2026-05-28 onward.
5. After any governance update, re-verify dependent files.
