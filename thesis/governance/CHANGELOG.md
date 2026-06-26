# Governance Changelog

This file is the human-readable history of governance versions. Each entry corresponds to a git tag. To recover the exact state at any version, run `git checkout <tag>`.

The versioning scheme is defined in [VERSIONING_POLICY.md](VERSIONING_POLICY.md).

---

## v6.2.0 — 2026-06-26

**Fundus-SSL corpus and acceptance protocol locked for the integrated arm (MINOR — new referenceable entities, no binding reversed).** The v6.0.0 ophthalmology-SSL decision is unchanged; this amendment fixes the operational specifics that were previously left open. The integrated-arm self-supervised pretraining corpus is fixed to the **unlabeled EyePACS original "test" split — 53,576 images** — which is **disjoint** from the Experiment-1 evaluation corpus (the ~35,126 labeled "train" split, 5-fold patient-level CV) by image identity and patient identity. This no-pretraining-leakage constraint is recorded as new clause **SB-2.4** (INVARIANTS) and is operationalized in the experiments code as the disjointness assertions **INV-SSL-1 / INV-SSL-2**. **BYOL** (Grill et al., 2020) is recorded as the primary CNN-compatible protocol (MoCo-v2 / SimSiam / DINO retained as alternatives), pretrained **from-scratch (random initialization)** directly on the 4-channel tensor (RGB + FOV mask). A **linear-probe acceptance gate** is added as the precondition for any SSL checkpoint to enter Experiment 1: with the backbone frozen, a linear head must beat random init and be competitive with ImageNet on a label-bearing EyePACS-test slice, for both backbones; an ImageNet→continual-SSL initialization is a documented (non-default) fallback.

Because this adds new referenceable entities (SB-2.4, the acceptance gate) and reverses no binding constraint, hypothesis, or scope boundary, it is a MINOR bump. CFC-2.8 (baseline ⟹ ImageNet, integrated ⟹ fundus-SSL) and the composite *(preprocessing × pretraining)* independent variable are retained; no SSL performance is asserted (the integrated arm is specified, not yet trained). This amendment also corrects a v6.0.0 sync miss: HYPOTHESIS.md Premise 4 and the Conclusion, which still named RETFound, are brought to the ophthalmology-SSL framing. Governance files updated: INVARIANTS, HYPOTHESIS, RESEARCH_ARCHITECTURE, CONTRIBUTIONS, VERSION_SYNC. Narrative sync: methodology §3.3.2 (draft + KZ translation + continuity), glossary EN/KZ. SSL literature cards (#84–#92) were already registered; no new card was required.

## v6.1.0 — 2026-06-23

**OD-3 Stage-1 detector: classical CV → pre-trained, frozen learned heatmap detector (MINOR — new substantive entity, no binding reversed).** The Stage-1 OD/fovea detector — previously classical computer vision (brightest-region OD, darkest-region-with-distance-prior fovea) — is replaced by a pre-trained, **frozen** heatmap-regression detector (U-Net encoder + DSNT head) trained on IDRiD localization ground-truth. It predicts OD/fovea probability heatmaps on the FOV-cropped frame, yielding sub-pixel centers and a **genuine** per-landmark confidence (from heatmap peak sharpness and spatial spread) that gates the rotation fallback and the Stage-5 polar-CLAHE fovea pivot.

Motivation: the classical detector localized the fovea unreliably (~5 OD-radii median error, ~0 % within 2 R at native resolution) and its confidence flag was non-informative. The learned detector meets the held-out IDRiD-test acceptance bar — OD median 0.066 R (100 % within 1 R); fovea median 0.107 R (99 % within 1 R); informative fovea confidence (Spearman ρ ≈ 0.44) — reproduced in-repo by `scripts/validate_od_fovea_idrid.py`. The fallback rotation **σ is reconciled to 15.0°** (the value the code and evaluation actually use; the prior 13.0° text is corrected). The detector is **pre-trained and frozen — not co-trained with the DR classifier** — so the preprocessing pipeline remains a fixed transform and the central thesis `model = preprocessing + CNN` is preserved. No hypothesis, scope boundary, factorial design, or other operational definition (Stages 0, 2–7) is modified. Governance files updated: INVARIANTS, RESEARCH_ARCHITECTURE, VERSION_SYNC, methods/preprocessing-pipeline. Narrative chapter drafts, assembled dissertation bundles, abstracts, and glossary entries describing the classical Stage-1 detector remain a separate downstream documentation pass.

## v6.0.0 — 2026-06-01

**RETFound replaced by ophthalmology-specific self-supervised pretraining (MAJOR — reverses the v5.1–v5.2 RETFound binding).** The integrated arm of Experiment 1 no longer initializes from the RETFound ViT-Large foundation model. Instead, the existing CNN backbones (ResNet-50 / EfficientNet-B3) are initialized from a CNN-compatible domain-adaptive self-supervised learning protocol (DINO / BYOL / SimCLR / MoCo family, selected empirically) pretrained on an unlabeled retinal fundus corpus. Rationale: adopting RETFound changes both the architecture and the initialization, confounding the preprocessing contribution with an architecture change; a CNN-native SSL initialization changes only the initialization stage, preserving the CNN-centred research design and a defensible causal interpretation of the preprocessing contrast.

Because the SSL initialization is CNN-native, the 2×2 *(preprocessing × architecture)* factorial symmetry is **restored**: configurations **B and D are reinstated** (integrated preprocessing + ophthalmology-SSL on ResNet-50 and EfficientNet-B3) and config **B′ is retired**. This resolves **AOQ-1** (→ option b), **AOQ-4** (symmetry), and **AOQ-3** (RETFound license moot), and simplifies **AOQ-2** (SSL pretrained directly on the 4-channel tensor). The composite *(preprocessing × pretraining)* independent variable and **CFC-2.8 are retained** (baseline ⟹ ImageNet, integrated ⟹ ophthalmology-SSL), so the H-1 effect remains non-attributable to preprocessing alone; EH-4 cross-architecture replication is reinstated. A new supporting contribution **SC-H** records the SSL initialization, bounded by CFC-2.8. No preprocessing operational definitions (OD-3, Stages 0–7) and no other hypotheses are modified; the v5.3 paradigmatic framing is retained. Governance files updated: INVARIANTS, HYPOTHESIS, RESEARCH_ARCHITECTURE, CONTRIBUTIONS, CENTRAL_THESIS, ARGUMENT_MAP, VERSION_SYNC.

## v5.3.0 — 2026-05-28

Paradigmatic framing introduced. Two paradigms recognised: **P1** (end-to-end CNN; preprocessing as ancillary data preparation) and **P2** (integrated preprocessing-CNN; preprocessing as integral model component). Gulshan et al. (2016) designated canonical representative of P1 (per the methodological-practice criterion in SIR-9). New governance clauses: **SB-1.12** (Gulshan is not a numerical benchmark, baseline is operational construct per OD-3), **CFC-2.9** (forbids false attribution of "preprocessing is unimportant" claim to Gulshan or other P1 sources), **SIR-9** (paradigmatic-attribution rule). PC-0 (Paradigmatic Framing Claim) added to ARGUMENT_MAP as a non-empirical methodological claim feeding into IT-1. CENTRAL_THESIS gains an introductory paradigmatic-framing paragraph. CONTRIBUTIONS gains an introductory conceptual-framing block and a reframed C-1 novelty statement. No operational definitions, hypotheses, or experimental protocols are modified.

## v5.2.0 — 2026-05-28

Refinement of the RETFound pretraining-corpus description. The integrated arm of Experiment 1 is now described as initialized from RETFound, a foundation model **MAE-pretrained on a multi-modal retinal imaging corpus** comprising ≈904K color fundus photographs (CFP) + ≈736K optical coherence tomography (OCT) scans (~1.6M total) per Zhou et al. 2023, Nature. The dissertation's integrated arm loads the **CFP-pretrained checkpoint** specifically; the multi-modal description characterizes the foundation model at the publication level and does not extend the dissertation's input domain to OCT (SB-1.4 in INVARIANTS.md remains in force). The composite independent variable, CFC-2.8, and the AOQ-1 through AOQ-4 open questions from v5.1 are unchanged.

## v5.1.0 — 2026-05-14

Pretraining source amendment: integrated arm of Experiment 1 uses RETFound; baseline arm retains ImageNet. H-1 reformulated as Integrated Pipeline Dominance with composite independent variable. See INVARIANTS.md v5.1 Section X for open operational questions (AOQ-1 through AOQ-4).

## v5.0.0 — 2026-04-09

Monorepo consolidation and introduction of the preprocessing pipeline. The three previously separate repositories — dissertation text, experiments, and demo dashboard — were unified into a single monorepo via subtree merges of `thesis/`, `experiments/`, and `demo/`. The 8-stage preprocessing pipeline was introduced, establishing the central thesis that `model = preprocessing + CNN`. Defense slide and dashboard scaffolding were added alongside the consolidated `.gitignore` and README.

## v4.0.0 — 2026-03-24

Governance synchronization pass. Residual stale references left by the V3 refactor were reconciled and the full governance set was brought to a consistent state across the V4 commit series (V4 → V4 fix → V4 edited → V4 final → V4 synchrone).

## v3.0.0 — 2026-03-14

Major restructuring. The experimental design was consolidated (APTOS dropped at this stage) and governance internal references were synchronized — INVARIANTS (OD-5, SB-1.1, SB-1.8, NC-16) and the ARGUMENT_MAP footer. The English and Kazakh tables of contents and the MASTER_OUTLINE were rewritten to V3.0. A meta-prompt writing pipeline was scaffolded (Section Brief, Writing/Revision/Translation/Verification templates, Continuity Note, context-assembly script) and the version synchronization register was introduced. The earlier v1 meta-prompt pipeline was deprecated.

## v2.0.0 — 2026-03-09

Second governance iteration. Methods were added and the document structure was reorganized following the V1 baseline.

## v1.0.0 — 2026-03-08 (inferred)

Pre-versioning baseline. The repository state captured by this tag predates the explicit governance versioning convention. See git tag `v1.0.0` for the complete state.
