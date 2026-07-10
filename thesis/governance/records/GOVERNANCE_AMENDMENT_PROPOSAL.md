# Governance amendment PROPOSAL — enable supervised in-domain pretraining (SIP)

**Status:** ✅ ADOPTED as governance **v6.3.0** (2026-07-10) — folded into INVARIANTS
(SB-2.4 + CFC-2.8 [v6.3.0]), CONTRIBUTIONS (SC-H), VERSION_SYNC. Retained here as the
decision-trail record; the text below is the pre-adoption proposal.

_Pre-adoption note:_ PROPOSAL ONLY — not binding until a maintainer folds it into
`thesis/governance/`. This file is drafted by the implementer to unblock the SIP arm
of the initialization head-to-head (see
`experiments/docs/supervised_indomain_pretraining_brief.md`). continual-SSL (v4.0)
does NOT depend on this proposal and may run meanwhile.

## Why an amendment is needed
SB-2.4 (v6.2.0) currently states the 53k EyePACS-"test" labels are "used only by the
linear-probe acceptance gate (DGL-6), **never by the SSL objective**." SIP feeds those
labels into a supervised pretraining objective, which the current wording forbids.
CFC-2.8 further slaves the integrated-arm init to *self-supervised* fundus pretraining.

## What triggered it
From-scratch in-domain CNN-SSL failed the acceptance gate across BYOL / MoCo-v2 / DINO
(best kappa 0.11 vs ImageNet 0.30) — a robust negative result. SIP is proposed as a
second candidate init to be selected against continual-SSL and ImageNet by the gate.

## Proposed changes (MINOR bump — adds entities, reverses no binding)
1. **SB-2.4** — add a clause permitting supervised use of the 53k DR labels for a
   distinct **in-domain PRETRAINING stage** whose corpus stays disjoint from the Exp-1
   35k CV set by image + patient identity (INV-SSL-1/2 unchanged). KEEP intact: the 53k
   "must not be folded into the Experiment-1 supervised training set" (pretrain-then-
   transfer is a separate stage, not folding).
2. **CFC-2.8** — list **supervised in-domain pretraining (SIP)** as an allowed
   integrated-arm initialization alongside fundus-SSL and the ImageNet->continual-SSL
   fallback; the final choice is made by the linear-probe acceptance gate. Baseline arm
   (A/C) remains ImageNet.
3. **SC-H** — reframe the supporting contribution from "self-supervised in-domain
   initialization" to "in-domain initialization (self-supervised OR supervised),
   selected by an acceptance gate," and record the SSL negative result as evidence.

## Explicit non-goals / caveats to record
- SIP does NOT resolve the central-thesis confound (H-1 still varies preprocessing AND
  init source together; FABLE5_REVIEW.md §5.1). If the committee-facing claim is
  "preprocessing matters," the confound-clean option remains ImageNet-in-both-arms.
- Leakage control: the SIP gate uses a patient-level holdout carved from the 53k; the
  gate never tests on a patient SIP trained on (brief §4).

## Maintainer sign-off
- [ ] SB-2.4 amended in thesis/governance/INVARIANTS.md
- [ ] CFC-2.8 amended
- [ ] SC-H reframed in thesis/governance/CONTRIBUTIONS.md
- [ ] VERSION_SYNC.md bumped (MINOR) with a pointer to this proposal
Until all four are checked, scripts/run_sip_pretrain.py must not be launched.
