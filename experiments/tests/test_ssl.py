"""Smoke + invariant tests for the SSL pretraining package (CPU, synthetic).

Covers the binding contracts that a reviewer must verify mechanically:
- the 4-channel two-view augmentation rule (§4.3): photometric never touches the
  mask, geometric is shared, the mask stays binary;
- the leakage / disjointness invariant (INV-SSL-2, §3.3);
- BYOL + alternatives forward/backward + a 1-step optimizer update;
- the trunk-only checkpoint format and the Exp-1 loader gate (§9.2/§10).

No GPU and no dataset images are required.
"""

from __future__ import annotations

import random as pyrandom

import numpy as np
import pytest
import torch
from torch.utils.data import DataLoader, Dataset

from src.ssl.checkpoint import save_ssl_checkpoint, set_gate_passed
from src.ssl.dataset import assert_ssl_corpus_disjoint
from src.ssl.encoder import build_ssl_encoder
from src.ssl.loader import load_ssl_backbone
from src.ssl.methods import build_method
from src.ssl.probe import decide_acceptance, evaluate_init
from src.ssl.trainer import SSLTrainer
from src.ssl.transforms import TwoViewTransform
from src.models.factory import create_model


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _seeded(view, base: torch.Tensor, seed: int) -> torch.Tensor:
    """Call a single-view transform under a fixed Python+torch RNG seed."""
    pyrandom.seed(seed)
    torch.manual_seed(seed)
    return view(base)


def _make_base(seed: int) -> torch.Tensor:
    """A 4-channel base tensor: random RGB in [0,1] + a circular binary mask."""
    rng = np.random.default_rng(seed)
    rgb = torch.from_numpy(rng.random((3, 96, 96)).astype(np.float32))
    yy, xx = np.mgrid[0:96, 0:96]
    mask = ((xx - 48) ** 2 + (yy - 48) ** 2 <= 38 ** 2).astype(np.float32)
    mask_t = torch.from_numpy(mask).unsqueeze(0)
    return torch.cat([rgb, mask_t], dim=0)


def _minimal_ssl_config(method: str = "byol") -> dict:
    """A minimal resolved ``ssl`` config block sufficient for the trainer."""
    return {
        "method": method,
        "in_channels": 4,
        "image_size": 64,
        "grad_clip": 1.0,
        "mixed_precision": {"resnet50": True, "efficientnet_b3": False},
        "optimizer": {"name": "lars", "base_lr": 0.1, "weight_decay": 1e-6, "warmup_epochs": 0},
        "byol": {"proj_hidden": 256, "proj_out": 64, "pred_hidden": 256, "ema_base": 0.99},
        "mocov2": {"queue_size": 32, "moco_dim": 32, "temperature": 0.2, "ema": 0.99},
        "simsiam": {"proj_hidden": 256, "proj_out": 256, "pred_hidden": 64},
        "dino": {"out_dim": 512, "student_temp": 0.1, "teacher_temp": 0.07, "center_momentum": 0.9},
    }


# ---------------------------------------------------------------------------
# §4.3 — 4-channel augmentation channel contract
# ---------------------------------------------------------------------------

def test_mask_is_binary_and_geometry_only():
    """Photometric ops never touch the mask; geometric is shared; mask stays {0,1}."""
    transform = TwoViewTransform(out_size=64, color_jitter_prob=1.0, grayscale_prob=1.0,
                                 blur_prob_view1=1.0, solarize_prob_view2=1.0)
    view = transform.view1

    base_a = _make_base(0)
    base_b = _make_base(0).clone()
    base_b[:3] = torch.rand_like(base_b[:3])  # different RGB, identical mask

    out_a = _seeded(view, base_a, seed=123)
    out_b = _seeded(view, base_b, seed=123)

    # Mask channel identical despite different RGB → photometric/RGB never leaks
    # into the mask, and the geometric transform was shared.
    assert torch.equal(out_a[3], out_b[3])
    # Mask stays strictly binary after interpolation + re-threshold.
    assert set(torch.unique(out_a[3]).tolist()).issubset({0.0, 1.0})
    # RGB channels differ (they carried different content through photometrics).
    assert not torch.equal(out_a[:3], out_b[:3])


def test_two_view_returns_pair_with_correct_shape():
    """TwoViewTransform yields two 4-channel views at the requested size."""
    transform = TwoViewTransform(out_size=64)
    v1, v2 = transform(_make_base(1))
    assert v1.shape == (4, 64, 64)
    assert v2.shape == (4, 64, 64)


# ---------------------------------------------------------------------------
# INV-SSL-2 — disjointness
# ---------------------------------------------------------------------------

def test_disjointness_passes_and_raises(tmp_path):
    """assert_ssl_corpus_disjoint passes on disjoint corpora, raises on overlap."""
    import pandas as pd

    root = tmp_path
    pd.DataFrame({"image": ["1_left", "1_right", "2_left"], "level": [0, 1, 0]}).to_csv(
        root / "trainLabels.csv", index=False
    )
    # Disjoint test corpus (different patient ids).
    pd.DataFrame({"image": ["90_left", "91_right"], "level": [0, 2], "Usage": ["Public", "Private"]}).to_csv(
        root / "testLabels15.csv", index=False
    )
    audit = assert_ssl_corpus_disjoint(root, "testLabels15.csv", "trainLabels.csv")
    assert audit["disjoint"] is True
    assert audit["ssl_count"] == 2 and audit["train_count"] == 3

    # Overlapping patient id → must raise.
    pd.DataFrame({"image": ["1_left", "92_right"], "level": [0, 2]}).to_csv(
        root / "testLabels_bad.csv", index=False
    )
    with pytest.raises(AssertionError):
        assert_ssl_corpus_disjoint(root, "testLabels_bad.csv", "trainLabels.csv")


# ---------------------------------------------------------------------------
# §7 — encoder construction
# ---------------------------------------------------------------------------

def test_build_ssl_encoder_feature_dims():
    """Factory-matched trunks expose the expected pooled feature dims."""
    _, dim_r = build_ssl_encoder("resnet50", in_channels=4, pretrained=False)
    assert dim_r == 2048
    _, dim_e = build_ssl_encoder("efficientnet_b3", in_channels=4, pretrained=False)
    assert dim_e == 1536
    trunk, _ = build_ssl_encoder("resnet50", in_channels=4, pretrained=False)
    out = trunk(torch.randn(2, 4, 64, 64))
    assert out.shape == (2, 2048)


# ---------------------------------------------------------------------------
# §5 — methods forward/backward + 1-step optimizer update
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("method", ["byol", "mocov2", "simsiam", "dino"])
def test_method_forward_backward_step(method):
    """Each SSL method runs a forward + backward + optimizer step on CPU (bs=2)."""
    torch.manual_seed(0)
    trunk, feat_dim = build_ssl_encoder("resnet50", in_channels=4, pretrained=False)
    model = build_method(method, trunk, feat_dim, _minimal_ssl_config(method))
    opt = torch.optim.SGD([p for p in model.parameters() if p.requires_grad], lr=0.01)

    v1 = torch.randn(2, 4, 64, 64)
    v2 = torch.randn(2, 4, 64, 64)
    loss = model(v1, v2)
    assert loss.ndim == 0 and torch.isfinite(loss)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if model.uses_ema:
        model.momentum_update(0.99)
    # Features must not be collapsed to a constant.
    feats = model.extract_features(v1)
    assert feats.std().item() > 0


# ---------------------------------------------------------------------------
# §9 — trainer loop + trunk-only checkpoint + §10 loader gate
# ---------------------------------------------------------------------------

class _SyntheticTwoView(Dataset):
    """Tiny synthetic two-view dataset (random 4-channel tensors)."""

    def __init__(self, n: int = 4, size: int = 64) -> None:
        self.n = n
        self.size = size

    def __len__(self) -> int:
        return self.n

    def __getitem__(self, idx: int):
        g = torch.Generator().manual_seed(idx)
        v1 = torch.rand(4, self.size, self.size, generator=g)
        v2 = torch.rand(4, self.size, self.size, generator=g)
        return v1, v2


def test_trainer_step_checkpoint_and_loader(tmp_path):
    """SSLTrainer trains a step, saves a trunk-only ckpt, loader gates + loads it."""
    cfg = _minimal_ssl_config("byol")
    trainer = SSLTrainer(cfg, "resnet50", device="cpu")
    loader = DataLoader(_SyntheticTwoView(n=4), batch_size=2)
    history = trainer.train(loader, epochs=1, log_every=1, max_steps=2)
    assert history and np.isfinite(history[-1]["loss"])

    out_dir = tmp_path / "v1.0"
    ckpt = save_ssl_checkpoint(
        out_dir, "byol", "resnet50", in_channels=4, image_size=64, epochs=1, seed=42,
        backbone_state_dict=trainer.trunk_state_dict(),
        normalize_stats_used="imagenet", gate_passed=False,
    )
    assert ckpt.exists()

    # Fresh-headed factory model; gate not yet passed → loader must refuse.
    model = create_model("resnet50", {"pretrained": False, "in_channels": 4, "num_classes": 5})
    with pytest.raises(RuntimeError):
        load_ssl_backbone(model, ckpt, require_gate_passed=True)

    # Dry run (gate bypass) must load the trunk cleanly (only head keys missing).
    meta = load_ssl_backbone(model, ckpt, require_gate_passed=False)
    assert meta["backbone"] == "resnet50" and meta["in_channels"] == 4

    # Flip the gate → strict gated load succeeds.
    set_gate_passed(ckpt, True)
    model2 = create_model("resnet50", {"pretrained": False, "in_channels": 4, "num_classes": 5})
    meta2 = load_ssl_backbone(model2, ckpt, require_gate_passed=True)
    assert meta2["gate_passed"] is True


def test_loader_rejects_3channel_model(tmp_path):
    """The loader asserts the target stem is 4-channel (Configs B/D only)."""
    trunk, _ = build_ssl_encoder("resnet50", in_channels=4, pretrained=False)
    out_dir = tmp_path / "v1.0"
    ckpt = save_ssl_checkpoint(
        out_dir, "byol", "resnet50", 4, 64, 1, 42,
        {k: v.detach().cpu() for k, v in trunk.state_dict().items()},
        "imagenet", gate_passed=True,
    )
    model_3ch = create_model("resnet50", {"pretrained": False, "in_channels": 3, "num_classes": 5})
    with pytest.raises(AssertionError):
        load_ssl_backbone(model_3ch, ckpt, require_gate_passed=True)


# ---------------------------------------------------------------------------
# §8 — probe evaluation + acceptance logic
# ---------------------------------------------------------------------------

class _SyntheticLabeled(Dataset):
    """Tiny synthetic labelled dataset (random 4-channel tensors + DR grades)."""

    def __init__(self, n: int = 16) -> None:
        self.n = n

    def __len__(self) -> int:
        return self.n

    def __getitem__(self, idx: int):
        g = torch.Generator().manual_seed(idx)
        x = torch.rand(4, 64, 64, generator=g)
        y = int(idx % 5)
        return x, y


def test_probe_evaluate_and_acceptance():
    """evaluate_init returns metrics; decide_acceptance applies the §8.4 rule."""
    encoder, feat_dim = build_ssl_encoder("resnet50", in_channels=4, pretrained=False)
    loader = DataLoader(_SyntheticLabeled(16), batch_size=8)
    metrics = evaluate_init(encoder, loader, loader, feat_dim, torch.device("cpu"), epochs=2)
    assert "linear" in metrics and "knn" in metrics and "feat_std" in metrics
    assert "cohen_kappa_quadratic" in metrics["linear"]

    ssl_m = {"linear": {"cohen_kappa_quadratic": 0.50, "weighted_f1": 0.6}, "feat_std": 0.2}
    rand_m = {"linear": {"cohen_kappa_quadratic": 0.40, "weighted_f1": 0.5}, "feat_std": 0.2}
    imnet_m = {"linear": {"cohen_kappa_quadratic": 0.52, "weighted_f1": 0.62}, "feat_std": 0.2}
    decision = decide_acceptance(ssl_m, rand_m, imnet_m, 0.05, -0.03)
    assert decision["passed"] is True  # +0.10 vs random, within 0.03 of imagenet
