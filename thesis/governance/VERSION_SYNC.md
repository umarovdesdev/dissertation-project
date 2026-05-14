# VERSION SYNCHRONIZATION REGISTER

**Version:** 5.1 | **Date:** 2026-05-13

## v5.1 Amendment Scope

Pretraining source amendment: V5 arm of Experiment 1 uses RETFound; baseline arm retains ImageNet. H-1 reformulated as Integrated Pipeline Dominance with composite independent variable. See INVARIANTS.md v5.1 Section X for open operational questions (AOQ-1 through AOQ-4).

## File Version Status

| File | Version | Synced |
|------|---------|--------|
| governance/INVARIANTS.md | 5.1 | ✅ |
| governance/HYPOTHESIS.md | 5.1 | ✅ |
| governance/RESEARCH_ARCHITECTURE.md | 5.1 | ✅ |
| governance/ARGUMENT_MAP.md | 5.0 | ❌ — references "Preprocessing Dominance" H-1; must be re-derived to reflect Integrated Pipeline Dominance and CFC-2.8 |
| governance/CONTRIBUTIONS.md | 5.0 | ❌ — contribution claims tied to preprocessing-only attribution must be reframed under CFC-2.8 |
| governance/CENTRAL_THESIS.md | 5.0 | ❌ — IT-1 wording references baseline pretrain symmetry; review against H-1 v5.1 |
| governance/CORE_OBJECTIVE.md | 5.0 | ⚠️ — review for pretrain references |
| outline/MASTER_OUTLINE.md | 5.0 | ❌ — chapter outlines that frame H-1 must be updated |
| outline/TABLE_OF_CONTENTS_EN.md | 5.0 | ⚠️ — likely unchanged but verify |
| outline/TABLE_OF_CONTENTS_KZ.md | 5.0 | ⚠️ — likely unchanged but verify |
| glossary/GLOSSARY_EN.md | 5.0 | ❌ — add RETFound, MAE, in-domain pretraining, foundation model |
| glossary/GLOSSARY_KZ.md | 5.0 | ❌ — Kazakh equivalents for new glossary terms |
| literature/LITERATURE_INDEX.md | 5.0 | ❌ — Zhou et al. 2023 (RETFound) literature card must be authored and indexed |
| experiments/experimental-protocol.md | 5.0 | ❌ — Exp 1 protocol must reflect v5.1 configurations and AOQ-1/2 resolutions |
| methods/preprocessing-pipeline.md | 5.0 | ⚠️ — preprocessing stages unchanged; review for pretrain references |
| methods/implementation.md | 5.0 | ❌ — model loading code paths must accommodate RETFound weights |

## Downstream Code Status (not part of governance, listed for completeness)

| Path | Sync status |
|------|-------------|
| experiments/configs/default.yaml | Out of sync — `pretrained: true` lines and `imagenet_*` keys must accommodate the V5 arm |
| experiments/src/models/factory.py | Out of sync — no RETFound loader |
| experiments/src/models/resnet.py | Out of sync if AOQ-1 resolves to option (a) ViT-Large |
| experiments/src/models/efficientnet.py | Out of sync if AOQ-1 resolves to option (a) |

Per the user's 2026-05-13 directive: governance v5.1 is the authoritative reference; downstream code and dependent governance files will be brought into sync in a subsequent pass.

## Sync Protocol

Before any chapter-writing session:
1. Verify all governance files marked ✅ are at version 5.1.
2. Files marked ❌ must not be cited as authoritative until brought to v5.1.
3. AOQ-1 through AOQ-4 (INVARIANTS v5.1 Section X) must be resolved before Experiment 1 execution.
4. After any governance update, re-verify dependent files.
