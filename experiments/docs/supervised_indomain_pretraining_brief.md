# Supervised in-domain pretraining (SIP) — build brief + head-to-head protocol

**Purpose.** Provide a SECOND candidate initialization for the Exp-1 pipeline arm
(Config B/D) and compare it head-to-head with continual-SSL (v4.0), picking the
winner on equal footing. Baseline arm (A/C) stays ImageNet regardless.

## 1. Relationship to the other arms
- **continual-SSL v4.0** (configs/ssl_continual_v4_0.yaml): label-free, sanctioned
  fallback, zero new code, risk = catastrophic forgetting below kappa 0.29.
- **SIP sip/v1.0** (configs/sip_pretrain.yaml, THIS brief): supervised on the 53k DR
  labels, needs new code + a governance amendment, but is DR-discriminative by
  construction and should clear the gate comfortably.
Run both; choose by §8.

## 2. Governance (BLOCKER — maintainer)
SIP violates SB-2.4 as written (labels are pretraining-only for the gate). Required
amendment (proposal: outputs/sip/v1.0/GOVERNANCE_AMENDMENT_PROPOSAL.md):
- **SB-2.4** — permit supervised use of the 53k labels for a distinct in-domain
  PRETRAINING stage; keep the "must not be folded into the Exp-1 35k training set"
  clause intact (pretrain-then-transfer is not folding).
- **CFC-2.8** — add "supervised in-domain pretraining (SIP)" as an allowed
  integrated-arm init alongside the SSL fallback.
- **SC-H** — reframe the supporting contribution from "self-supervised" to
  "in-domain initialization (self-supervised OR supervised), selected by gate".
Do not launch SIP before sign-off. continual-SSL needs none of this and can proceed.

## 3. Data (reuse, no new download)
- Images: existing 256 Stage-0-4 cache (ssl.cache_dir). 4-ch PNG + cache_meta.csv.
- Labels: testLabels15.csv (verified 1:1 with the 53,576 images, 2026-06-26).

## 4. Shared comparison holdout (the fairness mechanism — used by BOTH arms)
Carve the 53k ONCE, patient-level, seed=42, holdout_frac=0.15 -> `pretrain` (~45.5k)
and `holdout` (~8k), no patient in both. Reuse src/data/splits.py PatientLevelKFold
logic. Persist the two id-lists + an intersection==empty assertion (mirror INV-SSL-1/2).
- BOTH SIP and continual-SSL train ONLY on `pretrain`.
- The gate fits its linear head on a slice of `pretrain` and TESTS on `holdout`,
  identically for random / ImageNet / continual-SSL / SIP.
This replaces the probe's current Usage=Private split for the head-to-head so the
comparison is patient-clean and identical across arms. (For a standalone continual-SSL
fallback run that is NOT part of the comparison, the default Usage gate is acceptable.)

## 5. SIP training (NEW code: scripts/run_sip_pretrain.py + a thin dataset)
- Dataset: SupervisedPretrainDataset over the cache, returns (4ch tensor, grade);
  train-side Stage-5/6 stochastic aug (reuse existing transforms), holdout eval clean.
- Model: create_model(name, {in_channels:4, pretrained:True, num_classes:5}) — start
  from ImageNet, adapt the 4th channel as the factory already does.
- Loop: REUSE src/training/trainer.py (Focal gamma=2 + inverse-freq weights, AMP per
  models.mixed_precision, grad-clip, early-stop). Params from the `sip:` block.
- Resumable via the existing atomic train_state pattern (--resume).

## 6. Checkpoint + manifest (compat with the Exp-1 loader)
Write a trunk-only checkpoint + manifest.json that load_ssl_backbone accepts:
method="supervised_indomain", corpus="eyepacs_test_53k", init_source="imagenet",
split_holdout_ids ref, and gate_passed (set by §7). Same filename convention:
sip_{backbone}_4ch_256_ep{N}.pt under outputs/sip/v1.0/.

## 7. Gate (REUSE run_ssl_probe.py)
Run the existing frozen-linear-probe on the shared `holdout` for every init. For SIP,
pick the epoch with the best holdout kappa (guards against supervised overfitting).
Acceptance unchanged: kappa >= kappa_imagenet - 0.03 AND >= random + 0.05. SIP is
expected to pass with margin; the informative number is HOW FAR above ImageNet.

## 8. Head-to-head decision rule
Level 1 (cheap, do first): compare frozen-probe kappa on the shared holdout —
  random | ImageNet | continual-SSL v4.0 | SIP sip/v1.0.
  - If neither in-domain arm beats ImageNet -> USE IMAGENET in the pipeline arm
    (this is the honest outcome the whole gate exists to detect).
  - Else the higher-kappa in-domain arm is the candidate.
Level 2 (expensive): run Exp-1 B/D (35k, 5-fold CV) with the Level-1 winner's
  checkpoint; report EH-3 (dF1>=5pp, dAUC>=0.02, no kappa loss) vs the A/C ImageNet
  baseline. Run Level 2 for both arms only if compute allows; otherwise winner only.

## 9. Files & namespaces
- outputs/sip/v1.0/  — SIP checkpoints, gate reports, split id-lists, amendment proposal.
- outputs/ssl/v4.0/  — continual-SSL checkpoints + FALLBACK_ACTIVATION.md.
- Keep the two run families in separate dirs; never overwrite the v1.0-v3.0 SSL records.

## 10. Open decisions (for the candidate / maintainer)
- SIP lr (3e-4) and epochs (40) are engineering estimates, not measured — the ep5/10
  holdout curve calibrates them.
- Whether to run Level 2 (downstream Exp-1) for BOTH arms or the winner only, given
  the RTX-3060/5070-Ti compute budget.
- Whether SIP, if it wins, is framed as the integrated-arm init OR kept as a labeled
  appendix while the pipeline arm uses ImageNet (this affects the central-thesis
  confound discussed in FABLE5_REVIEW.md §5.1 — SIP does NOT resolve it).
