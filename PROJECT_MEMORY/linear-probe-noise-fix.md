---
name: linear-probe-noise-fix
description: The SSL linear-probe acceptance gate was high-variance (~±0.1 κ for EffNet); fixed src/ssl/probe.py to be deterministic; earlier gate κ (SSL sweep, SIP-ResNet 0.658) carry ±0.04–0.10 uncertainty
metadata:
  type: reference
---

**The linear-probe acceptance gate was measurement-noisy** and it materially affected
interpretation (2026-07-10). `src/ssl/probe.py::_train_linear_head` trained a single
random-init `nn.Linear` head on **raw** frozen features with full-batch Adam (lr 0.1, ~50
steps) — unstandardized, underconverged, single-seed. On the **same cached frozen features**
this scored ImageNet-EffNet κ = **0.338 vs 0.445** across two runs (~±0.10 swing); ResNet was
tighter (~±0.04, 2048-d features better conditioned).

**Consequence:** every κ measured with the OLD probe carries ±0.04–0.10 uncertainty — the
from-scratch SSL sweep values (BYOL 0.00, MoCo 0.11, DINO 0.06; ImageNet 0.30), and the
**SIP-ResNet 0.658** number, are noisy estimates. Fine comparisons (Δκ < 0.05) with the old
probe are untrustworthy; only large gaps (e.g. ResNet continual +0.25 over ImageNet) survive.

**Fix (committed):** standardize features (z-score, train stats applied to test, no leakage) +
average over `n_seeds` head inits + guaranteed convergence (`min_steps`) + weight decay →
**deterministic** probe (re-gate gives bit-identical κ). The fix is in the shared
`_train_linear_head`, so `run_ssl_probe.py` AND `run_sip_pretrain.py --gate` both benefit.

**κ of record (robust probe, seed-42 patient-level holdout):** ResNet-50 continual 0.605 vs
ImageNet 0.357; EfficientNet-B3 continual 0.431 vs ImageNet 0.435. See
[[continual-ssl-init-decision]]. **OPEN:** SIP-ResNet (0.658, old probe) should be re-gated
with the robust probe before any SIP-vs-continual comparison.
