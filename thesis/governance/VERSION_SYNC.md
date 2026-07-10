# VERSION SYNCHRONIZATION REGISTER

**Version:** 6.3.0 | **Date:** 2026-07-09

## v6.3.0 Amendment Scope

**Supervised in-domain pretraining (SIP) added as a gate-selected integrated-arm initialization.** From-scratch label-free CNN-SSL (BYOL / MoCo-v2 / DINO) **failed** the linear-probe acceptance gate on the EyePACS-test corpus — best quadratic-κ ≈0.11 vs ImageNet ≈0.30, flat/declining ep50→ep100, a robust negative result (`experiments/outputs/ssl/COMPARISON.txt`). In response, **SIP** is admitted alongside fundus-SSL and the ImageNet→continual-SSL fallback: the same CNN backbone is supervised on the 53,576-image EyePACS-test corpus **using its DR grades** (started from ImageNet, adapted), then transferred to Experiment 1, with the final choice among the three inits made by the existing linear-probe acceptance gate on a **patient-level holdout**. This **(1) relaxes SB-2.4** to permit supervised use of the EyePACS-test grades for a distinct in-domain *pretraining* stage — the corpus stays disjoint from the Experiment-1 35,126 CV set by image + patient identity (INV-SSL-1/2) and is still not folded into Experiment-1 training; **(2) extends CFC-2.8** to list SIP as a gate-selected init while retaining its core confound caveat (the integrated arm still differs from baseline along both preprocessing and initialization); **(3) generalizes SC-H** from "self-supervised" to "in-domain initialization (self-supervised OR supervised), gate-selected," recording the SSL negative result as evidence. The label-free SSL objective is unchanged; SIP is a separate objective. **Adds an allowed initialization + relaxes one operational restriction; reverses no hypothesis, scope boundary, or forbidden-claim → MINOR bump** per VERSIONING_POLICY §4. Governance files updated: INVARIANTS (header, SB-2.4, CFC-2.8), CONTRIBUTIONS (SC-H), VERSION_SYNC. **Pending downstream sync** (does not gate this bump): HYPOTHESIS Premise-4/Conclusion wording, RESEARCH_ARCHITECTURE §4.2bis/§9.1, glossary EN/KZ. Implementation: `experiments/scripts/run_sip_pretrain.py`, spec `experiments/docs/supervised_indomain_pretraining_brief.md`, proposal `experiments/outputs/sip/v1.0/GOVERNANCE_AMENDMENT_PROPOSAL.md`.

## v6.2.0 Amendment Scope

**Fundus-SSL corpus + acceptance protocol locked for the integrated arm.** The v6.0.0 ophthalmology-SSL decision is unchanged; v6.2.0 fixes the operational specifics that were previously left open. (1) The integrated-arm SSL corpus is the **unlabeled EyePACS "test" split — 53,576 images**, **disjoint** from the Experiment-1 evaluation corpus (the ~35,126 labeled "train" split, 5-fold patient-level CV) by image identity *and* patient identity. This no-pretraining-leakage constraint is recorded as new clause **SB-2.4** (INVARIANTS) and operationalized in the experiments code as the disjointness assertions **INV-SSL-1 / INV-SSL-2**. (2) **BYOL** (Grill et al., 2020) is recorded as the **primary** CNN-compatible protocol (MoCo-v2 / SimSiam / DINO retained as alternatives), pretrained **from-scratch** on the 4-channel tensor. (3) A **linear-probe acceptance gate** is added: an SSL checkpoint enters Experiment 1 only after it beats random init and is competitive with ImageNet, for both backbones. **Adds new referenceable entities (SB-2.4, the linear-probe acceptance gate), reverses no binding → MINOR bump** per VERSIONING_POLICY §4. CFC-2.8 (baseline ⟹ ImageNet, integrated ⟹ fundus-SSL) and the composite IV are retained; no SSL performance is asserted (the integrated arm is specified, not yet trained). Governance files updated: INVARIANTS (SB-2.4, DGL-6, header), HYPOTHESIS (Premise 4 + Conclusion RETFound→SSL sync; specifics), RESEARCH_ARCHITECTURE (§4.2bis, §9.1), CONTRIBUTIONS (SC-H), VERSION_SYNC, CHANGELOG. Narrative sync: methodology §3.3.2 draft + KZ translation + continuity; glossary EN/KZ (linear-probe gate term + SSL-entry refinements). Literature: SSL cards #84–#92 already registered (no new card needed); LITERATURE_INDEX notes BYOL as the selected primary.

## v6.1.0 Amendment Scope

**OD-3 Stage-1 detector: classical CV → pre-trained, frozen learned detector.** The Stage-1 OD/fovea detector is replaced by a pre-trained, **frozen** heatmap-regression detector (U-Net encoder + DSNT head, trained on IDRiD localization ground-truth) that predicts OD/fovea probability heatmaps on the FOV-cropped frame with sub-pixel centers and a genuine per-landmark confidence. It meets the held-out IDRiD-test acceptance bar (OD median 0.066 R / 100 % within 1 R; fovea median 0.107 R / 99 % within 1 R; informative fovea confidence, Spearman ρ ≈ 0.44). The fallback rotation **σ is reconciled to 15.0°** (the code/eval value; the prior 13.0° text is corrected). The detector is **pre-trained and frozen — not co-trained with the DR classifier** — so preprocessing remains a fixed transform and `model = preprocessing + CNN` holds. **Adds a new substantive entity (the learned Stage-1 detector), reverses no binding → MINOR bump** per VERSIONING_POLICY §4. No hypothesis, scope boundary, factorial design, or other operational definition (Stages 0, 2–7) changes.

In-repo integration (Phase 2): the learned detector lives at `experiments/src/preprocessing/od_fovea_net/` behind the unchanged `detect_od_fovea(image_rgb) → ODFoveaResult` facade (additive confidence/heatmap fields); the live pipeline pivots Stage-5 polar CLAHE on the detected fovea when confident (else FOV centroid), with the pivot cached for the training path. `scripts/validate_od_fovea_idrid.py` reproduces the acceptance numbers on the IDRiD test split inside the monorepo. **Pending downstream (narrative) sync:** chapter drafts (3.1.1, 3.1.3, 1.1.1, 2.2.1), assembled dissertation bundles, abstracts, and glossary entries that still describe the classical Stage-1 detector are regenerated artifacts and remain a separate documentation pass (they do not gate this governance bump).

## v6.0.0 Amendment Scope

**RETFound replaced by ophthalmology-specific self-supervised pretraining.** The integrated arm of Experiment 1 no longer initializes from the RETFound ViT-Large foundation model; instead the existing CNN backbones (ResNet-50 / EfficientNet-B3) are initialized from a CNN-compatible domain-adaptive self-supervised learning protocol (DINO / BYOL / SimCLR / MoCo family, selected empirically) pretrained on an unlabeled retinal fundus corpus. Rationale: RETFound changes both architecture and initialization, confounding the preprocessing contribution; a CNN-native SSL initialization changes only the initialization stage. **This reverses the v5.1–v5.2 RETFound binding → MAJOR bump per VERSIONING_POLICY §4.**

Resolutions: **AOQ-1 → option (b)** (CNN-compatible SSL); **AOQ-4 resolved** (the 2×2 *(preprocessing × architecture)* factorial symmetry is restored — both backbones in both arms; configs **B and D reinstated**, config **B′ retired**); **AOQ-3 retired** (RETFound license moot); **AOQ-2 simplified** (SSL pretrained directly on the 4-channel tensor). The composite *(preprocessing × pretraining)* independent variable and **CFC-2.8 are retained** (baseline ⟹ ImageNet, integrated ⟹ ophthalmology-SSL), so the H-1 effect remains non-attributable to preprocessing alone. EH-4 cross-architecture replication is reinstated. A new supporting contribution **SC-H** records the SSL initialization (bounded by CFC-2.8). No preprocessing operational definitions (OD-3, Stages 0–7) are modified. The v5.3 paradigmatic framing (P1/P2, SB-1.12, CFC-2.9, SIR-9) is retained unchanged.

## v5.3 Amendment Scope

Paradigmatic framing introduced. Two paradigms recognised: **P1** (end-to-end CNN; preprocessing as ancillary data preparation) and **P2** (integrated preprocessing-CNN; preprocessing as integral model component). Gulshan et al. (2016) designated canonical representative of P1 (per the methodological-practice criterion in SIR-9). New governance clauses: **SB-1.12** (Gulshan is not a numerical benchmark, baseline is operational construct per OD-3), **CFC-2.9** (forbids false attribution of "preprocessing is unimportant" claim to Gulshan or other P1 sources), **SIR-9** (paradigmatic-attribution rule). PC-0 (Paradigmatic Framing Claim) added to ARGUMENT_MAP as a non-empirical methodological claim feeding into IT-1. CENTRAL_THESIS gains an introductory paradigmatic-framing paragraph. CONTRIBUTIONS gains an introductory conceptual-framing block and a reframed C-1 novelty statement. No operational definitions, hypotheses, or experimental protocols are modified. The integration tracker is `GULSHAN_PARADIGM_INTEGRATION_PLAN.md` at the repository root.

## v5.2 Amendment Scope

Refinement of the RETFound pretraining-corpus description. The integrated arm of Experiment 1 is now described as initialized from RETFound, a foundation model **MAE-pretrained on a multi-modal retinal imaging corpus** comprising ≈904K color fundus photographs (CFP) + ≈736K optical coherence tomography (OCT) scans (~1.6M total) per Zhou et al. 2023, Nature. The dissertation's integrated arm loads the **CFP-pretrained checkpoint** specifically; the multi-modal description characterizes the foundation model at the publication level and does not extend the dissertation's input domain to OCT (SB-1.4 in INVARIANTS.md remains in force). The composite independent variable, CFC-2.8, and the AOQ-1 through AOQ-4 open questions from v5.1 are unchanged.

## v5.1 Amendment Scope (historical)

Pretraining source amendment: integrated arm of Experiment 1 uses RETFound; baseline arm retains ImageNet. H-1 reformulated as Integrated Pipeline Dominance with composite independent variable. See INVARIANTS.md v5.1 Section X for open operational questions (AOQ-1 through AOQ-4).

## File Version Status

| File | Version | Synced |
|------|---------|--------|
| governance/INVARIANTS.md | 6.3.0 | ✅ — v6.3.0: SB-2.4 relaxed + CFC-2.8 extended to admit supervised in-domain pretraining (SIP) as a gate-selected integrated-arm init (SSL negative result); header summary added — completed 2026-07-09. v6.2.0: SB-2.4 added; DGL-6 extended (EyePACS-test 53,576, BYOL-primary, from-scratch, linear-probe gate) |
| governance/HYPOTHESIS.md | 6.2.0 | ✅ — v6.2.0: Premise 4 + Conclusion corrected RETFound→ophthalmology-SSL (v6.0.0 sync miss); SSL operational specifics recorded — completed 2026-06-26 |
| governance/RESEARCH_ARCHITECTURE.md | 6.2.0 | ✅ — v6.2.0: §4.2bis extended (corpus, BYOL-primary, from-scratch 4-channel, linear-probe gate); §9.1 pretraining-leakage bullet — completed 2026-06-26 |
| governance/VERSION_SYNC.md | 6.2.0 | ✅ |
| governance/ARGUMENT_MAP.md | 6.0.0 | ✅ — unaffected by v6.2.0 (no pretraining-source node in this file; binding-ref unchanged) |
| governance/CONTRIBUTIONS.md | 6.3.0 | ✅ — v6.3.0: SC-H generalized to "in-domain initialization (self-supervised OR supervised), gate-selected" — SIP admitted, SSL negative result recorded — completed 2026-07-09. v6.2.0: SC-H refined with locked SSL specifics; CFC-2.8 boundary unchanged |
| governance/CENTRAL_THESIS.md | 6.0.0 | ✅ — unaffected by v6.2.0 (no pretraining reference in body; binding-ref unchanged) |
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
| glossary/GLOSSARY_EN.md | 6.2.0 | ✅ — v6.0.0 SSL/paradigm terms present; v6.2.0: added Linear-Probe Acceptance Gate + Fundus-SSL Pretraining Corpus terms, refined SSL-Method-Family (BYOL primary) and Ophthalmology-SSL entries — completed 2026-06-26 |
| glossary/GLOSSARY_KZ.md | 6.2.0 | ✅ — v6.2.0: Kazakh equivalents mirrored for the new/refined SSL terms — completed 2026-06-26 |
| literature/LITERATURE_INDEX.md | 5.0 | ❌ — v6.0.0: SSL-family cards (DINO/BYOL/SimCLR/MoCo) for the integrated-arm pretraining; Zhou et al. 2023 (RETFound) demoted to historical/contrast; Paradigm column (v5.3) |
| literature/external/gulshan-2016.md | 5.0 | ❌ — Paradigmatic Role block required in §15 (v5.3) — see Task 1.1 |
| experiments/experimental-protocol.md | 5.0 | ❌ — v6.0.0: Exp 1 protocol must reflect the restored A/B/C/D factorial (integrated arm = ophthalmology-SSL); AOQ-1/3/4 resolved, AOQ-2 simplified |
| methods/preprocessing-pipeline.md | 6.1.0 (Stage 1) | ✅ — v6.1.0: Stage-1 description updated to the frozen learned heatmap detector (σ = 15.0°); other stages still pending the v6.0.0 pretrain-reference review |
| methods/implementation.md | 5.0 | ❌ — v6.0.0: model loading code paths must load an in-house ophthalmology-SSL CNN checkpoint (no RETFound/ViT-Large loader needed) |

## Downstream Code Status (not part of governance, listed for completeness)

| Path | Sync status |
|------|-------------|
| experiments/configs/default.yaml | Out of sync — integrated-arm config must point at an in-house ophthalmology-SSL CNN checkpoint (not ImageNet, not RETFound) |
| experiments/src/models/factory.py | Out of sync — needs an SSL-pretrained-CNN checkpoint loader for the integrated arm |
| experiments/src/models/resnet.py | In sync re: backbone (AOQ-1 resolved to option (b) — CNN unchanged); only the init-weights source changes |
| experiments/src/models/efficientnet.py | In sync re: backbone (AOQ-1 resolved to option (b) — CNN unchanged); only the init-weights source changes |
| demo/src/tabs/ModelArchitecture.js | ✅ Synced 2026-06-01 (v6.0.0) — integrated-arm row + note now ophthalmology-specific SSL on ResNet-50/EfficientNet-B3 (configs B/D); RETFound removed |
| defense/slides/08_CNN_ARCHITECTURE.md | ✅ Synced 2026-06-01 (v6.0.0) — bullet → ophthalmology-SSL; AOQ-1 note replaced with "symmetry restored" |
| defense/slides/09_ARCHITECTURE_COMPARISON.md | ✅ Synced 2026-06-01 (v6.0.0) — factorial table restored to A/B/C/D; B′ retired; Factor 2 + speech → SSL |
| defense/paradigmatic_speech.md | ✅ Synced 2026-06-01 (v6.0.0) — Gulshan caveat pretraining-source line → ImageNet / ophthalmology-SSL |
| thesis/chapters/01-problem-domain/README.md | ✅ Synced 2026-06-01 (v6.0.0) — §1.3.2 in-domain-pretraining contrast → ophthalmology-SSL (RETFound demoted to related work) |
| thesis/chapters/05-validation/README.md | ✅ Synced 2026-06-01 (v6.0.0) — Gulshan caveat-block pretraining-source item → ophthalmology-SSL |
| thesis/literature/external/gulshan-2016.md | ✅ Synced 2026-06-01 (v6.0.0) — § unsound-comparison pretraining-source line → ophthalmology-SSL (separate from the still-pending Paradigmatic Role block) |

Version history: v5.1 (2026-05-14) adopted RETFound for the integrated arm; v5.2 (2026-05-28) refined the RETFound corpus to multi-modal CFP + OCT; v5.3 (2026-05-28) introduced the paradigmatic framing (P1 / P2; Gulshan as canonical representative of P1). **v6.0.0 (2026-06-01) reverses the RETFound adoption** in favour of ophthalmology-specific self-supervised pretraining of the existing CNN backbones (MAJOR bump). The dependent governance and downstream files marked ❌/Out-of-sync above must be brought to v6.0.0 in subsequent passes; once governance is stable, the version-marker scan (VERSIONING_POLICY.md §6) enforces version containment outside `thesis/`.

**Note — Config-D naming divergence:** the *shipped* demo/training artifact "Config D" is the retired ImageNet pipeline (EfficientNet-B3 + ImageNet); governance **Config D** is now full pipeline + EfficientNet-B3 + ophthalmology-SSL. These must not be silently merged — the shipped demo predates this amendment.

## Sync Protocol

Before any chapter-writing session:
1. Verify all governance files marked ✅ are at version 6.0.0 (current authoritative version).
2. Files marked ❌ must not be cited as authoritative until brought to v6.0.0.
3. AOQ-1/AOQ-3/AOQ-4 are resolved and AOQ-2 simplified in v6.0.0 (INVARIANTS Section X); the integrated arm uses ophthalmology-specific SSL on the existing CNN backbones.
4. The v5.3 paradigmatic-framing constraints (SB-1.12, CFC-2.9, SIR-9) remain binding on every chapter, slide, and demo update.
5. After any governance update, re-verify dependent files.
