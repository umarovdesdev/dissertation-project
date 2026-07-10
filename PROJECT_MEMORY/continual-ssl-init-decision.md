---
name: continual-ssl-init-decision
description: Integrated-arm (Config B/D) init = ImageNet→continual-SSL (MoCo-v2, ep50) for BOTH backbones; from-scratch SSL failed; EffNet continual gives NO benefit over ImageNet (honest caveat)
metadata:
  type: project
---

**Decision (2026-07-10, candidate):** The Experiment-1 integrated arm (Configs **B** and
**D**) is initialized from **ImageNet→continual-SSL** (MoCo-v2, ImageNet start via
`--pretrained-init`, 50 epochs, `run v4.0`) for **both** backbones — ResNet-50 (B) and
EfficientNet-B3 (D), the **ep50** checkpoints. Baseline arm (A/C) stays ImageNet.

**Path to here:** from-scratch in-domain CNN-SSL within INV-SSL-6 (BYOL/MoCo-v2/DINO)
**FAILED** the linear-probe gate (best κ≈0.11 vs ImageNet≈0.30, flat ep50→100 — robust
negative result). Pivoted to the governance-sanctioned **continual-SSL fallback** (CFC-2.8;
config `ssl_continual_v4_0.yaml`, EffNet overlay `ssl_continual_v4_0_eff.yaml` batch32/lr
0.000375/AMP-off). SIP (supervised in-domain pretraining) was built + governance-amended
(v6.3.0) as an alternative but NOT chosen — candidate picked continual for both for symmetry.

**Trustworthy gate results (robust probe on the seed-42 patient-level holdout, n_test=8036).**
The linear-probe gate was noisy (~±0.1 κ for EffNet — same frozen features gave ImageNet κ
0.338 vs 0.445 across runs); fixed `src/ssl/probe.py::_train_linear_head` (feature
standardization + seed-averaging + guaranteed convergence → deterministic). Re-gated:

| Backbone | continual κ | ImageNet κ | Δ | verdict |
|----------|-------------|------------|-----|---------|
| ResNet-50 (B)   | **0.605** | 0.357 | **+0.248** | continual is a large real win |
| EfficientNet-B3 (D) | **0.431** | 0.435 | **−0.004** | continual ≈ ImageNet, **no benefit** |

**⚠ CAVEAT to document in the thesis (do NOT overclaim):** continual-SSL helps ResNet-50
enormously but gives **EfficientNet-B3 no in-domain benefit** (0.431 ≈ ImageNet 0.435,
deterministic, not noise). Config D's integrated init is effectively ImageNet-equivalent;
using it is a symmetry/consistency choice, not an in-domain performance gain. (SIP-ResNet
scored 0.658 with the OLD noisy probe; re-gate with the robust probe before comparing.)

**Artifacts:** checkpoints `experiments/outputs/ssl/v4.0/ssl_mocov2_{resnet50,efficientnet_b3}_4ch_256_ep50.pt`
(both `gate_passed=True`); robust reports `C:/ssl_out/sip/v1.0/gate_report_{resnet50,efficientnet_b3}.json`;
Exp-1 wiring overlay `experiments/configs/exp1_continual_v4_0.yaml`. CFC-2.8 confound
(preprocessing × init) still applies — H-1 cannot isolate preprocessing (see [[config-d-pretraining]]).
