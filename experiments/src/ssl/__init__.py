"""Self-supervised pretraining (SSL) package for fundus CNN backbones.

Implements in-domain, CNN-backbone-matched, label-free self-supervised
pretraining (BYOL primary, with MoCo-v2 / SimSiam / DINO selectable) on the
EyePACS original "test" split (53,576 images), producing 4-channel
(RGB + FOV mask) ResNet-50 and EfficientNet-B3 initializations for the pipeline
arm of Experiment 1 (Configs B and D).

See ``experiments/docs/fundus_ssl_pretraining_brief.md`` for the binding spec.

Public surface:
    build_ssl_encoder         — factory-matched trunk + feature dim (encoder.py)
    EyePACSSSLDataset         — label-free two-view dataset (dataset.py)
    EyePACSProbeDataset       — labelled single-view probe dataset (dataset.py)
    assert_ssl_corpus_disjoint— leakage invariant INV-SSL-2 (dataset.py)
    TwoViewTransform          — 4-channel two-view augmentation (transforms.py)
    build_method / SSLMethod  — pluggable SSL strategies (methods.py)
    SSLTrainer                — training loop, EMA, schedulers, collapse (trainer.py)
    save_ssl_checkpoint / SSLCheckpointManager — versioned trunk-only ckpt (checkpoint.py)
    load_ssl_backbone         — Exp-1 integration loader (loader.py)
"""

from __future__ import annotations

# Submodules are imported directly by callers
# (e.g. ``from src.ssl.trainer import SSLTrainer``), mirroring the rest of the
# codebase (``from src.training.trainer import Trainer``). The package __init__
# is intentionally side-effect-free so importing it pulls in no heavy deps.
