---
name: config-d-pretraining
description: "Pretraining-axis decision history — shipped Config D (ImageNet) vs governance Config D (SSL); AOQ-1 resolved in v6.0.0"
metadata:
  type: project
---

**RESOLVED 2026-06-01 (governance v6.0.0).** The V5-arm pretraining axis is settled: **RETFound is dropped** in favour of **ophthalmology-specific self-supervised pretraining** (CNN-compatible domain-adaptive SSL — DINO/BYOL/SimCLR/MoCo family, kept open, selected empirically) of the *existing* CNN backbones (ResNet-50 / EfficientNet-B3). This resolves **AOQ-1 → option (b)**, **AOQ-4** (2×2 *(preprocessing × architecture)* symmetry restored: configs **B and D reinstated**, **B′ retired**), **AOQ-3** (RETFound license moot); **AOQ-2** simplified (SSL pretrains on the 4-channel V5 tensor). The composite *(preprocessing × pretraining)* IV and **CFC-2.8 are retained** (baseline⟹ImageNet, V5⟹SSL). MAJOR bump per VERSIONING_POLICY §4. Committed `c1fa0b0` (governance) + `55576d1` (dependent sync), tag `v6.0.0`, pushed to origin/main. New supporting contribution **SC-H** records the SSL init (CFC-2.8-bounded).

**Config-D naming divergence (still live):** the *shipped* demo/training "Config D" is the retired **v5.0 artifact = V5 + EfficientNet-B3 + ImageNet** (the `dreamer07/eyepacs` Kaggle run, fold 0 — see [[config-d-kaggle-source]]). Governance **Config D is now V5 + EfficientNet-B3 + ophthalmology-SSL**. These must **not** be silently merged — the shipped demo predates v6.0.0. The Stage-7 dataset-specific input normalization was never the open issue; the pretraining/backbone axis was, and is now closed.

**Genuine remaining work (net-new):** glossary SSL terms (EN/KZ), new SSL-family literature cards + LITERATURE_INDEX, and the experiments/ SSL **pretraining implementation** (training code + checkpoint loader). The implementation is outside Claude's role per CLAUDE.md (ChatGPT implements; Claude plans/reviews).

**Why:** the candidate chose a CNN-native in-domain initialization so architecture is not confounded with preprocessing — a defensible causal interpretation of the H-1 contrast, unlike RETFound (ViT-L) which changes the backbone.

**How to apply:** Treat v6.0.0 as authoritative; don't reintroduce RETFound as the V5-arm source. When touching demo/experiments Config D, check whether the context means the *shipped ImageNet artifact* or the *governance SSL design*.
