"""Linear-probe + kNN acceptance gate for SSL checkpoints (brief §8).

No SSL checkpoint enters Experiment 1 until it passes this gate. For each
backbone the gate compares three frozen-backbone initializations on the EyePACS
*test* probe slice — random init, ImageNet init, and the SSL checkpoint — and
accepts the SSL init iff it beats random by a margin and is within (or better
than) ``accept_vs_imagenet_kappa_margin`` of ImageNet, without collapse.

The probe trains only a single ``Linear(feature_dim, 5)`` head on frozen pooled
features; features are extracted once (backbone frozen) and reused for both the
linear head and the kNN second opinion.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

from src.evaluation.metrics import compute_primary_metrics
from src.ssl.encoder import build_ssl_encoder
from src.ssl.methods import feature_std


@torch.no_grad()
def extract_features(
    encoder: nn.Module, loader: DataLoader, device: torch.device
) -> tuple[torch.Tensor, torch.Tensor]:
    """Extract frozen pooled features and labels for a probe loader.

    Args:
        encoder: Head-stripped trunk (frozen).
        loader: Yields ``(tensor, label)`` batches.
        device: Compute device.

    Returns:
        Tuple ``(features (N, d), labels (N,))`` on CPU.
    """
    encoder.eval()
    feats: list[torch.Tensor] = []
    labels: list[torch.Tensor] = []
    for x, y in loader:
        f = encoder(x.to(device))
        feats.append(f.detach().cpu())
        labels.append(y if isinstance(y, torch.Tensor) else torch.as_tensor(y))
    return torch.cat(feats), torch.cat(labels)


def _train_linear_head(
    train_feats: torch.Tensor,
    train_labels: torch.Tensor,
    test_feats: torch.Tensor,
    feature_dim: int,
    num_classes: int,
    epochs: int,
    lr: float,
    device: torch.device,
) -> np.ndarray:
    """Train a linear head on cached frozen features; return test probabilities.

    Args:
        train_feats: Probe-train features ``(Ntr, d)``.
        train_labels: Probe-train labels ``(Ntr,)``.
        test_feats: Probe-test features ``(Nte, d)``.
        feature_dim: Feature dimension ``d``.
        num_classes: Number of DR grades (5).
        epochs: Linear-head training epochs.
        lr: Learning rate.
        device: Compute device.

    Returns:
        Test-set class probabilities ``(Nte, num_classes)`` as a NumPy array.
    """
    head = nn.Linear(feature_dim, num_classes).to(device)
    optimizer = torch.optim.Adam(head.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    x_tr = train_feats.to(device)
    y_tr = train_labels.long().to(device)
    head.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = criterion(head(x_tr), y_tr)
        loss.backward()
        optimizer.step()

    head.eval()
    with torch.no_grad():
        probs = F.softmax(head(test_feats.to(device)), dim=1)
    return probs.cpu().numpy()


@torch.no_grad()
def _knn_predict(
    train_feats: torch.Tensor,
    train_labels: torch.Tensor,
    test_feats: torch.Tensor,
    k: int = 20,
) -> np.ndarray:
    """Cosine k-NN prediction on frozen features (second opinion, §8.2).

    Args:
        train_feats: Probe-train features ``(Ntr, d)``.
        train_labels: Probe-train labels ``(Ntr,)``.
        test_feats: Probe-test features ``(Nte, d)``.
        k: Number of neighbours.

    Returns:
        Predicted labels ``(Nte,)`` as a NumPy array.
    """
    tr = F.normalize(train_feats, dim=1)
    te = F.normalize(test_feats, dim=1)
    sims = te @ tr.t()                                  # (Nte, Ntr)
    k = min(k, tr.shape[0])
    idx = sims.topk(k, dim=1).indices                   # (Nte, k)
    neigh = train_labels[idx]                           # (Nte, k)
    num_classes = int(train_labels.max().item()) + 1
    onehot = F.one_hot(neigh, num_classes).sum(dim=1)   # (Nte, C)
    return onehot.argmax(dim=1).numpy()


def evaluate_init(
    encoder: nn.Module,
    train_loader: DataLoader,
    test_loader: DataLoader,
    feature_dim: int,
    device: torch.device,
    num_classes: int = 5,
    epochs: int = 50,
    lr: float = 0.1,
    knn_k: int = 20,
) -> dict[str, Any]:
    """Run the frozen-backbone linear probe + kNN for one initialization.

    Args:
        encoder: Frozen trunk.
        train_loader: Probe-train loader.
        test_loader: Probe-test loader.
        feature_dim: Trunk feature dimension.
        device: Compute device.
        num_classes: Number of DR grades.
        epochs: Linear-head epochs.
        lr: Linear-head learning rate.
        knn_k: kNN neighbour count.

    Returns:
        Dict with ``linear`` metrics, ``knn`` metrics, and ``feat_std``.
    """
    for p in encoder.parameters():
        p.requires_grad = False
    encoder.to(device)

    tr_feats, tr_labels = extract_features(encoder, train_loader, device)
    te_feats, te_labels = extract_features(encoder, test_loader, device)

    probs = _train_linear_head(
        tr_feats, tr_labels, te_feats, feature_dim, num_classes, epochs, lr, device
    )
    y_true = te_labels.numpy()
    y_pred = probs.argmax(axis=1)
    linear_metrics = compute_primary_metrics(y_true, y_pred, probs, num_classes=num_classes)

    knn_pred = _knn_predict(tr_feats, tr_labels, te_feats, k=knn_k)
    knn_metrics = compute_primary_metrics(y_true, knn_pred, None, num_classes=num_classes)

    return {
        "linear": linear_metrics,
        "knn": knn_metrics,
        "feat_std": feature_std(te_feats),
        "n_train": int(tr_feats.shape[0]),
        "n_test": int(te_feats.shape[0]),
    }


def decide_acceptance(
    ssl_metrics: dict[str, Any],
    random_metrics: dict[str, Any],
    imagenet_metrics: dict[str, Any],
    accept_vs_random_kappa_delta: float,
    accept_vs_imagenet_kappa_margin: float,
    min_feat_std: float = 1e-3,
) -> dict[str, Any]:
    """Apply the §8.4 acceptance criterion for one backbone.

    Args:
        ssl_metrics: ``evaluate_init`` output for the SSL init.
        random_metrics: ``evaluate_init`` output for random init.
        imagenet_metrics: ``evaluate_init`` output for ImageNet init.
        accept_vs_random_kappa_delta: Required κ margin over random.
        accept_vs_imagenet_kappa_margin: Allowed κ deficit vs ImageNet (negative,
            e.g. -0.03 ⇒ SSL within 0.03 κ of ImageNet).
        min_feat_std: Collapse floor on SSL feature std.

    Returns:
        Dict with the three sub-criteria and ``passed``.
    """
    k_ssl = ssl_metrics["linear"]["cohen_kappa_quadratic"]
    k_rand = random_metrics["linear"]["cohen_kappa_quadratic"]
    k_imnet = imagenet_metrics["linear"]["cohen_kappa_quadratic"]
    f1_ssl = ssl_metrics["linear"]["weighted_f1"]
    f1_rand = random_metrics["linear"]["weighted_f1"]

    beats_random = (k_ssl - k_rand >= accept_vs_random_kappa_delta) and (f1_ssl > f1_rand)
    competitive_imagenet = k_ssl >= k_imnet + accept_vs_imagenet_kappa_margin
    not_collapsed = ssl_metrics["feat_std"] > min_feat_std

    return {
        "kappa_ssl": k_ssl,
        "kappa_random": k_rand,
        "kappa_imagenet": k_imnet,
        "beats_random": bool(beats_random),
        "competitive_with_imagenet": bool(competitive_imagenet),
        "not_collapsed": bool(not_collapsed),
        "passed": bool(beats_random and competitive_imagenet and not_collapsed),
    }


def run_probe_for_backbone(
    config: dict[str, Any],
    backbone_name: str,
    ssl_ckpt_path: str | Path,
    train_loader: DataLoader,
    test_loader: DataLoader,
    device: torch.device,
) -> dict[str, Any]:
    """Run the full gate (random / ImageNet / SSL) for one backbone (§8.3/§8.4).

    Args:
        config: Full config dict (reads the ``ssl.probe`` block + ``in_channels``).
        backbone_name: Backbone to probe.
        ssl_ckpt_path: Path to the SSL trunk checkpoint to evaluate.
        train_loader: Probe-train loader.
        test_loader: Probe-test loader.
        device: Compute device.

    Returns:
        Per-backbone report dict: metrics for each init condition + acceptance.
    """
    ssl_cfg = config["ssl"]
    probe_cfg = ssl_cfg.get("probe", {})
    in_channels = int(ssl_cfg.get("in_channels", 4))
    epochs = int(probe_cfg.get("epochs", 50))
    lr = float(probe_cfg.get("lr", 0.1))

    # Random init
    rand_enc, feat_dim = build_ssl_encoder(backbone_name, in_channels, pretrained=False)
    random_metrics = evaluate_init(
        rand_enc, train_loader, test_loader, feat_dim, device, epochs=epochs, lr=lr
    )

    # ImageNet init
    imnet_enc, _ = build_ssl_encoder(backbone_name, in_channels, pretrained=True)
    imagenet_metrics = evaluate_init(
        imnet_enc, train_loader, test_loader, feat_dim, device, epochs=epochs, lr=lr
    )

    # SSL init
    ssl_enc, _ = build_ssl_encoder(backbone_name, in_channels, pretrained=False)
    ckpt = torch.load(Path(ssl_ckpt_path), map_location="cpu", weights_only=False)
    load_result = ssl_enc.load_state_dict(ckpt["backbone_state_dict"], strict=False)
    if load_result.unexpected_keys:
        raise AssertionError(
            f"Unexpected keys loading SSL trunk into probe encoder: "
            f"{load_result.unexpected_keys[:10]}"
        )
    ssl_metrics = evaluate_init(
        ssl_enc, train_loader, test_loader, feat_dim, device, epochs=epochs, lr=lr
    )

    acceptance = decide_acceptance(
        ssl_metrics, random_metrics, imagenet_metrics,
        accept_vs_random_kappa_delta=float(probe_cfg.get("accept_vs_random_kappa_delta", 0.05)),
        accept_vs_imagenet_kappa_margin=float(probe_cfg.get("accept_vs_imagenet_kappa_margin", -0.03)),
    )

    return {
        "backbone": backbone_name,
        "ssl_checkpoint": str(ssl_ckpt_path),
        "random": random_metrics,
        "imagenet": imagenet_metrics,
        "ssl": ssl_metrics,
        "acceptance": acceptance,
    }
