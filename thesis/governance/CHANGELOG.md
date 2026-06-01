# Governance Changelog

This file is the human-readable history of governance versions. Each entry corresponds to a git tag. To recover the exact state at any version, run `git checkout <tag>`.

The versioning scheme is defined in [VERSIONING_POLICY.md](VERSIONING_POLICY.md).

---

## v6.0.0 — 2026-06-01

**RETFound replaced by ophthalmology-specific self-supervised pretraining (MAJOR — reverses the v5.1–v5.2 RETFound binding).** The V5 arm of Experiment 1 no longer initializes from the RETFound ViT-Large foundation model. Instead, the existing CNN backbones (ResNet-50 / EfficientNet-B3) are initialized from a CNN-compatible domain-adaptive self-supervised learning protocol (DINO / BYOL / SimCLR / MoCo family, selected empirically) pretrained on an unlabeled retinal fundus corpus. Rationale: adopting RETFound changes both the architecture and the initialization, confounding the preprocessing contribution with an architecture change; a CNN-native SSL initialization changes only the initialization stage, preserving the CNN-centred research design and a defensible causal interpretation of the preprocessing contrast.

Because the SSL initialization is CNN-native, the 2×2 *(preprocessing × architecture)* factorial symmetry is **restored**: configurations **B and D are reinstated** (V5 + ophthalmology-SSL on ResNet-50 and EfficientNet-B3) and config **B′ is retired**. This resolves **AOQ-1** (→ option b), **AOQ-4** (symmetry), and **AOQ-3** (RETFound license moot), and simplifies **AOQ-2** (SSL pretrained directly on the 4-channel V5 tensor). The composite *(preprocessing × pretraining)* independent variable and **CFC-2.8 are retained** (baseline ⟹ ImageNet, V5 ⟹ ophthalmology-SSL), so the H-1 effect remains non-attributable to preprocessing alone; EH-4 cross-architecture replication is reinstated. A new supporting contribution **SC-H** records the SSL initialization, bounded by CFC-2.8. No preprocessing operational definitions (OD-3, Stages 0–7) and no other hypotheses are modified; the v5.3 paradigmatic framing is retained. Governance files updated: INVARIANTS, HYPOTHESIS, RESEARCH_ARCHITECTURE, CONTRIBUTIONS, CENTRAL_THESIS, ARGUMENT_MAP, VERSION_SYNC.

## v5.3.0 — 2026-05-28

Paradigmatic framing introduced. Two paradigms recognised: **P1** (end-to-end CNN; preprocessing as ancillary data preparation) and **P2** (integrated preprocessing-CNN; preprocessing as integral model component). Gulshan et al. (2016) designated canonical representative of P1 (per the methodological-practice criterion in SIR-9). New governance clauses: **SB-1.12** (Gulshan is not a numerical benchmark, baseline is operational construct per OD-3), **CFC-2.9** (forbids false attribution of "preprocessing is unimportant" claim to Gulshan or other P1 sources), **SIR-9** (paradigmatic-attribution rule). PC-0 (Paradigmatic Framing Claim) added to ARGUMENT_MAP as a non-empirical methodological claim feeding into IT-1. CENTRAL_THESIS gains an introductory paradigmatic-framing paragraph. CONTRIBUTIONS gains an introductory conceptual-framing block and a reframed C-1 novelty statement. No operational definitions, hypotheses, or experimental protocols are modified.

## v5.2.0 — 2026-05-28

Refinement of the RETFound pretraining-corpus description. The V5 arm of Experiment 1 is now described as initialized from RETFound, a foundation model **MAE-pretrained on a multi-modal retinal imaging corpus** comprising ≈904K color fundus photographs (CFP) + ≈736K optical coherence tomography (OCT) scans (~1.6M total) per Zhou et al. 2023, Nature. The dissertation's V5 arm loads the **CFP-pretrained checkpoint** specifically; the multi-modal description characterizes the foundation model at the publication level and does not extend the dissertation's input domain to OCT (SB-1.4 in INVARIANTS.md remains in force). The composite independent variable, CFC-2.8, and the AOQ-1 through AOQ-4 open questions from v5.1 are unchanged.

## v5.1.0 — 2026-05-14

Pretraining source amendment: V5 arm of Experiment 1 uses RETFound; baseline arm retains ImageNet. H-1 reformulated as Integrated Pipeline Dominance with composite independent variable. See INVARIANTS.md v5.1 Section X for open operational questions (AOQ-1 through AOQ-4).

## v5.0.0 — 2026-04-09

Monorepo consolidation and introduction of the V5 preprocessing pipeline. The three previously separate repositories — dissertation text, experiments, and demo dashboard — were unified into a single monorepo via subtree merges of `thesis/`, `experiments/`, and `demo/`. The V5 8-stage preprocessing pipeline was introduced, establishing the central thesis that `model = preprocessing + CNN`. Defense slide and dashboard scaffolding were added alongside the consolidated `.gitignore` and README.

## v4.0.0 — 2026-03-24

Governance synchronization pass. Residual stale references left by the V3 refactor were reconciled and the full governance set was brought to a consistent state across the V4 commit series (V4 → V4 fix → V4 edited → V4 final → V4 synchrone).

## v3.0.0 — 2026-03-14

Major restructuring. The experimental design was consolidated (APTOS dropped at this stage) and governance internal references were synchronized — INVARIANTS (OD-5, SB-1.1, SB-1.8, NC-16) and the ARGUMENT_MAP footer. The English and Kazakh tables of contents and the MASTER_OUTLINE were rewritten to V3.0. A meta-prompt writing pipeline was scaffolded (Section Brief, Writing/Revision/Translation/Verification templates, Continuity Note, context-assembly script) and the version synchronization register was introduced. The earlier v1 meta-prompt pipeline was deprecated.

## v2.0.0 — 2026-03-09

Second governance iteration. Methods were added and the document structure was reorganized following the V1 baseline.

## v1.0.0 — 2026-03-08 (inferred)

Pre-versioning baseline. The repository state captured by this tag predates the explicit governance versioning convention. See git tag `v1.0.0` for the complete state.
