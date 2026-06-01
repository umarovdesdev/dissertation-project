# VERSION SYNCHRONIZATION REGISTER

**Version:** 6.0.0 | **Date:** 2026-06-01

## v6.0.0 Amendment Scope

**RETFound replaced by ophthalmology-specific self-supervised pretraining.** The V5 arm of Experiment 1 no longer initializes from the RETFound ViT-Large foundation model; instead the existing CNN backbones (ResNet-50 / EfficientNet-B3) are initialized from a CNN-compatible domain-adaptive self-supervised learning protocol (DINO / BYOL / SimCLR / MoCo family, selected empirically) pretrained on an unlabeled retinal fundus corpus. Rationale: RETFound changes both architecture and initialization, confounding the preprocessing contribution; a CNN-native SSL initialization changes only the initialization stage. **This reverses the v5.1–v5.2 RETFound binding → MAJOR bump per VERSIONING_POLICY §4.**

Resolutions: **AOQ-1 → option (b)** (CNN-compatible SSL); **AOQ-4 resolved** (the 2×2 *(preprocessing × architecture)* factorial symmetry is restored — both backbones in both arms; configs **B and D reinstated**, config **B′ retired**); **AOQ-3 retired** (RETFound license moot); **AOQ-2 simplified** (SSL pretrained directly on the 4-channel V5 tensor). The composite *(preprocessing × pretraining)* independent variable and **CFC-2.8 are retained** (baseline ⟹ ImageNet, V5 ⟹ ophthalmology-SSL), so the H-1 effect remains non-attributable to preprocessing alone. EH-4 cross-architecture replication is reinstated. A new supporting contribution **SC-H** records the SSL initialization (bounded by CFC-2.8). No preprocessing operational definitions (OD-3, Stages 0–7) are modified. The v5.3 paradigmatic framing (P1/P2, SB-1.12, CFC-2.9, SIR-9) is retained unchanged.

## v5.3 Amendment Scope

Paradigmatic framing introduced. Two paradigms recognised: **P1** (end-to-end CNN; preprocessing as ancillary data preparation) and **P2** (integrated preprocessing-CNN; preprocessing as integral model component). Gulshan et al. (2016) designated canonical representative of P1 (per the methodological-practice criterion in SIR-9). New governance clauses: **SB-1.12** (Gulshan is not a numerical benchmark, baseline is operational construct per OD-3), **CFC-2.9** (forbids false attribution of "preprocessing is unimportant" claim to Gulshan or other P1 sources), **SIR-9** (paradigmatic-attribution rule). PC-0 (Paradigmatic Framing Claim) added to ARGUMENT_MAP as a non-empirical methodological claim feeding into IT-1. CENTRAL_THESIS gains an introductory paradigmatic-framing paragraph. CONTRIBUTIONS gains an introductory conceptual-framing block and a reframed C-1 novelty statement. No operational definitions, hypotheses, or experimental protocols are modified. The integration tracker is `GULSHAN_PARADIGM_INTEGRATION_PLAN.md` at the repository root.

## v5.2 Amendment Scope

Refinement of the RETFound pretraining-corpus description. The V5 arm of Experiment 1 is now described as initialized from RETFound, a foundation model **MAE-pretrained on a multi-modal retinal imaging corpus** comprising ≈904K color fundus photographs (CFP) + ≈736K optical coherence tomography (OCT) scans (~1.6M total) per Zhou et al. 2023, Nature. The dissertation's V5 arm loads the **CFP-pretrained checkpoint** specifically; the multi-modal description characterizes the foundation model at the publication level and does not extend the dissertation's input domain to OCT (SB-1.4 in INVARIANTS.md remains in force). The composite independent variable, CFC-2.8, and the AOQ-1 through AOQ-4 open questions from v5.1 are unchanged.

## v5.1 Amendment Scope (historical)

Pretraining source amendment: V5 arm of Experiment 1 uses RETFound; baseline arm retains ImageNet. H-1 reformulated as Integrated Pipeline Dominance with composite independent variable. See INVARIANTS.md v5.1 Section X for open operational questions (AOQ-1 through AOQ-4).

## File Version Status

| File | Version | Synced |
|------|---------|--------|
| governance/INVARIANTS.md | 6.0.0 | ✅ — v6.0.0: RETFound→ophthalmology-SSL in H-1/DGL-6/CFC-2.8; Section X AOQ-1/3/4 resolved, AOQ-2 simplified — completed 2026-06-01 |
| governance/HYPOTHESIS.md | 6.0.0 | ✅ — v6.0.0: H-1 RETFound clause replaced with ophthalmology-SSL; AOQ references marked resolved — completed 2026-06-01 |
| governance/RESEARCH_ARCHITECTURE.md | 6.0.0 | ✅ — v6.0.0: §4.1/4.2/4.2bis rewritten; Exp-1 A/B/C/D factorial restored, B′ retired; §7 ablation table updated; EH-4 reinstated — completed 2026-06-01 |
| governance/VERSION_SYNC.md | 6.0.0 | ✅ |
| governance/ARGUMENT_MAP.md | 6.0.0 | ✅ — v6.0.0: binding-ref bump only (no RETFound/pretraining node in this file) — completed 2026-06-01 |
| governance/CONTRIBUTIONS.md | 6.0.0 | ✅ — v6.0.0: SC-H (ophthalmology-SSL initialization, CFC-2.8-bounded) added; header amendment note — completed 2026-06-01 |
| governance/CENTRAL_THESIS.md | 6.0.0 | ✅ — v6.0.0: binding-ref bump only (no pretraining reference in body) — completed 2026-06-01 |
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
| glossary/GLOSSARY_EN.md | 5.0 | ❌ — v6.0.0: add ophthalmology-specific SSL, DINO, BYOL, SimCLR, MoCo terms (RETFound now historical); plus paradigm P1/P2, canonical representative (v5.3) |
| glossary/GLOSSARY_KZ.md | 5.0 | ❌ — Kazakh equivalents for new glossary terms |
| literature/LITERATURE_INDEX.md | 5.0 | ❌ — v6.0.0: SSL-family cards (DINO/BYOL/SimCLR/MoCo) for the V5-arm pretraining; Zhou et al. 2023 (RETFound) demoted to historical/contrast; Paradigm column (v5.3) |
| literature/external/gulshan-2016.md | 5.0 | ❌ — Paradigmatic Role block required in §15 (v5.3) — see Task 1.1 |
| experiments/experimental-protocol.md | 5.0 | ❌ — v6.0.0: Exp 1 protocol must reflect the restored A/B/C/D factorial (V5 arm = ophthalmology-SSL); AOQ-1/3/4 resolved, AOQ-2 simplified |
| methods/preprocessing-pipeline.md | 5.0 | ⚠️ — preprocessing stages unchanged; review for pretrain references |
| methods/implementation.md | 5.0 | ❌ — v6.0.0: model loading code paths must load an in-house ophthalmology-SSL CNN checkpoint (no RETFound/ViT-Large loader needed) |

## Downstream Code Status (not part of governance, listed for completeness)

| Path | Sync status |
|------|-------------|
| experiments/configs/default.yaml | Out of sync — V5-arm config must point at an in-house ophthalmology-SSL CNN checkpoint (not ImageNet, not RETFound) |
| experiments/src/models/factory.py | Out of sync — needs an SSL-pretrained-CNN checkpoint loader for the V5 arm |
| experiments/src/models/resnet.py | In sync re: backbone (AOQ-1 resolved to option (b) — CNN unchanged); only the init-weights source changes |
| experiments/src/models/efficientnet.py | In sync re: backbone (AOQ-1 resolved to option (b) — CNN unchanged); only the init-weights source changes |
| demo/src/tabs/ModelArchitecture.js | ✅ Synced 2026-06-01 (v6.0.0) — V5-arm row + note now ophthalmology-specific SSL on ResNet-50/EfficientNet-B3 (configs B/D); RETFound removed |
| defense/slides/08_CNN_ARCHITECTURE.md | ✅ Synced 2026-06-01 (v6.0.0) — V5 bullet → ophthalmology-SSL; AOQ-1 note replaced with "symmetry restored" |
| defense/slides/09_ARCHITECTURE_COMPARISON.md | ✅ Synced 2026-06-01 (v6.0.0) — factorial table restored to A/B/C/D; B′ retired; Factor 2 + speech → SSL |
| defense/paradigmatic_speech.md | ✅ Synced 2026-06-01 (v6.0.0) — Gulshan caveat pretraining-source line → ImageNet / ophthalmology-SSL |
| thesis/chapters/01-problem-domain/README.md | ✅ Synced 2026-06-01 (v6.0.0) — §1.3.2 in-domain-pretraining contrast → ophthalmology-SSL (RETFound demoted to related work) |
| thesis/chapters/05-validation/README.md | ✅ Synced 2026-06-01 (v6.0.0) — Gulshan caveat-block pretraining-source item → ophthalmology-SSL |
| thesis/literature/external/gulshan-2016.md | ✅ Synced 2026-06-01 (v6.0.0) — § unsound-comparison pretraining-source line → ophthalmology-SSL (separate from the still-pending Paradigmatic Role block) |

Version history: v5.1 (2026-05-14) adopted RETFound for the V5 arm; v5.2 (2026-05-28) refined the RETFound corpus to multi-modal CFP + OCT; v5.3 (2026-05-28) introduced the paradigmatic framing (P1 / P2; Gulshan as canonical representative of P1). **v6.0.0 (2026-06-01) reverses the RETFound adoption** in favour of ophthalmology-specific self-supervised pretraining of the existing CNN backbones (MAJOR bump). The dependent governance and downstream files marked ❌/Out-of-sync above must be brought to v6.0.0 in subsequent passes; once governance is stable, `STRIP_VERSIONS_PLAN.md` enforces version containment outside `thesis/`.

**Note — Config-D naming divergence:** the *shipped* demo/training artifact "Config D" is the retired ImageNet pipeline (EfficientNet-B3 + ImageNet); governance **Config D** is now V5 + EfficientNet-B3 + ophthalmology-SSL. These must not be silently merged — the shipped demo predates this amendment.

## Sync Protocol

Before any chapter-writing session:
1. Verify all governance files marked ✅ are at version 6.0.0 (current authoritative version).
2. Files marked ❌ must not be cited as authoritative until brought to v6.0.0.
3. AOQ-1/AOQ-3/AOQ-4 are resolved and AOQ-2 simplified in v6.0.0 (INVARIANTS Section X); the V5 arm uses ophthalmology-specific SSL on the existing CNN backbones.
4. The v5.3 paradigmatic-framing constraints (SB-1.12, CFC-2.9, SIR-9) remain binding on every chapter, slide, and demo update.
5. After any governance update, re-verify dependent files.
