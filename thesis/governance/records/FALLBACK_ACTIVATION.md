# Continual-SSL fallback — ACTIVATION RECORD (run v4.0)

**Status:** activated 2026-07-09. **Governance basis:** INVARIANTS / CFC-2.8 —
"An ImageNet→continual-SSL initialization is a documented fallback should the gate
fail; it is not the default and **must be explicitly flagged if used**." This file
is that explicit flag. The checkpoint manifest independently records
`init_source=imagenet_continual` (run_ssl_pretrain.py:194).

## Why the fallback was triggered
From-scratch in-domain CNN-SSL within the INV-SSL-6 family FAILED the linear-probe
acceptance gate across three method families — a robust negative result, not a
tuning accident (source: outputs/ssl/COMPARISON.txt + per-run gate_report_ep*.json):

| Method | Epoch | kappa(SSL) | kappa(ImageNet) | passed |
|--------|-------|-----------|-----------------|--------|
| BYOL v1.0/v1.1/v1.2 | ep50–300 | 0.000 | 0.30 | no |
| MoCo-v2 v2.0 | ep50 / ep100 | 0.112 / 0.109 | 0.32 / 0.30 | no |
| DINO v3.0 | ep50 / ep100 | 0.075 / 0.061 | 0.32 / 0.30 | no |

Acceptance needs kappa(SSL) >= kappa(ImageNet) - 0.03. Best from-scratch SSL (0.11)
is ~1/3 of ImageNet (0.30). ep50->ep100 flat/declining rules out undertraining.

## What v4.0 does
Start the trunk from ImageNet (already passes the gate frozen, kappa 0.30) and run
MoCo-v2 (best in-family) ONLY to adapt to fundus statistics — SSL must merely NOT
DESTROY a competitive start. Config: configs/ssl_continual_v4_0.yaml. Objective
stays LABEL-FREE, so SB-2.4 is untouched and the frozen-probe gate remains valid
as-is. Deltas vs from-scratch: base_lr 10x lower (0.001125), epochs 50, warmup 3.

## Failure mode to watch (inverted vs from-scratch)
ImageNet arm passes trivially, so the only failure mode is DEGRADATION below ~0.29
(catastrophic forgetting). Gate at ep10/25/50; if kappa monotonically declines from
~0.32, STOP — more epochs is the risk, not the cure.

## Head-to-head with SIP
This continual-SSL arm is being compared against supervised in-domain pretraining
(SIP, outputs/sip/v1.0). For that comparison BOTH arms are re-gated on the SAME
patient-level holdout — see experiments/docs/supervised_indomain_pretraining_brief.md
§4/§8 for the shared-holdout protocol and the decision rule.

## Maintainer action (governance fold-in)
This run activates a fallback that INVARIANTS classifies as non-default. A maintainer
should mirror a one-line note into thesis/governance (VERSION_SYNC.md and/or the
CFC-2.8 discussion) that the fallback is IN USE for the integrated arm, with a pointer
to this record. No binding constraint is reversed by activating a documented fallback.
