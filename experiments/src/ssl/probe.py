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

import os
import time
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
    encoder: nn.Module,
    loader: DataLoader,
    device: torch.device,
    desc: str = "",
    log_every: int = 50,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Extract frozen pooled features and labels for a probe loader.

    Args:
        encoder: Head-stripped trunk (frozen).
        loader: Yields ``(tensor, label)`` batches.
        device: Compute device.
        desc: Optional label printed with the progress lines (e.g. ``"ssl/test"``).
        log_every: Print a progress line every this many batches (0 disables). The
            probe otherwise prints nothing for minutes, so this restores an ETA.

    Returns:
        Tuple ``(features (N, d), labels (N,))`` on CPU.
    """
    encoder.eval()
    feats: list[torch.Tensor] = []
    labels: list[torch.Tensor] = []
    try:
        n_batches = len(loader)
    except TypeError:
        n_batches = 0
    t0 = time.time()
    for i, (x, y) in enumerate(loader):
        f = encoder(x.to(device))
        feats.append(f.detach().cpu())
        labels.append(y if isinstance(y, torch.Tensor) else torch.as_tensor(y))
        if log_every and desc and (i + 1) % log_every == 0:
            done = sum(t.shape[0] for t in feats)
            rate = done / max(time.time() - t0, 1e-6)
            eta = (n_batches - (i + 1)) / max(i + 1, 1) * (time.time() - t0)
            print(
                f"    [{desc}] batch {i + 1}/{n_batches or '?'} "
                f"({done} imgs, {rate:.1f} img/s, eta {eta / 60:.1f} min)",
                flush=True,
            )
    return torch.cat(feats), torch.cat(labels)


def _extract_or_load(
    encoder: nn.Module,
    loader: DataLoader,
    device: torch.device,
    cache_path: Path | None,
    desc: str = "",
) -> tuple[torch.Tensor, torch.Tensor]:
    """Extract features, or load them from a resumable on-disk cache if present.

    Feature extraction is the probe's cost. Caching the ``(features, labels)``
    blob per ``(backbone, init, split)`` makes the gate stop-and-resume safe: a
    killed run re-computes only the extractions it had not yet finished, and a
    re-run (e.g. on a faster machine after copying the blobs) is near-instant.
    Written atomically (temp + :func:`os.replace`) so a kill mid-write cannot
    leave a corrupt cache.

    Args:
        encoder: Frozen trunk.
        loader: Probe loader for the split.
        device: Compute device.
        cache_path: Destination ``.pt`` path, or ``None`` to disable caching.
        desc: Progress label forwarded to :func:`extract_features`.

    Returns:
        Tuple ``(features (N, d), labels (N,))`` on CPU.
    """
    try:
        expected_n = len(loader.dataset)  # type: ignore[arg-type]
    except (TypeError, AttributeError):
        expected_n = None

    if cache_path is not None and cache_path.exists():
        blob = torch.load(cache_path, map_location="cpu", weights_only=False)
        cached_n = int(blob["features"].shape[0])
        if expected_n is not None and cached_n != expected_n:
            # Stale/partial cache (e.g. from a --limit smoke, or an interrupted
            # write) — the row count no longer matches this run. Re-extract.
            print(f"    [{desc}] ignoring stale cache {cache_path.name} "
                  f"(has {cached_n} rows, expected {expected_n})", flush=True)
        else:
            print(f"    [{desc}] loaded cached features {tuple(blob['features'].shape)} "
                  f"from {cache_path.name}", flush=True)
            return blob["features"], blob["labels"]

    feats, labels = extract_features(encoder, loader, device, desc=desc)

    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = cache_path.with_suffix(cache_path.suffix + ".tmp")
        torch.save({"features": feats, "labels": labels}, tmp)
        os.replace(tmp, cache_path)
        print(f"    [{desc}] cached features -> {cache_path.name}", flush=True)
    return feats, labels


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
    feature_cache: tuple[Path | None, Path | None] = (None, None),
    desc: str = "",
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
        feature_cache: ``(train_cache_path, test_cache_path)`` for the resumable
            on-disk feature cache; ``(None, None)`` disables caching.
        desc: Progress label prefix (e.g. ``"resnet50/ssl"``).

    Returns:
        Dict with ``linear`` metrics, ``knn`` metrics, and ``feat_std``.
    """
    for p in encoder.parameters():
        p.requires_grad = False
    encoder.to(device)

    train_cache, test_cache = feature_cache
    tr_feats, tr_labels = _extract_or_load(
        encoder, train_loader, device, train_cache, desc=f"{desc}/train"
    )
    te_feats, te_labels = _extract_or_load(
        encoder, test_loader, device, test_cache, desc=f"{desc}/test"
    )

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
    feature_cache_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Run the full gate (random / ImageNet / SSL) for one backbone (§8.3/§8.4).

    Args:
        config: Full config dict (reads the ``ssl.probe`` block + ``in_channels``).
        backbone_name: Backbone to probe.
        ssl_ckpt_path: Path to the SSL trunk checkpoint to evaluate.
        train_loader: Probe-train loader.
        test_loader: Probe-test loader.
        device: Compute device.
        feature_cache_dir: Directory for the resumable per-init feature cache, or
            ``None`` to disable. Blobs are keyed ``{backbone}_{init}_{split}.pt``;
            random/ImageNet/SSL features are all deterministic under the fixed
            probe seed, so cached blobs stay consistent across resumed runs.

    Returns:
        Per-backbone report dict: metrics for each init condition + acceptance.
    """
    ssl_cfg = config["ssl"]
    probe_cfg = ssl_cfg.get("probe", {})
    in_channels = int(ssl_cfg.get("in_channels", 4))
    epochs = int(probe_cfg.get("epochs", 50))
    lr = float(probe_cfg.get("lr", 0.1))

    cache_root = Path(feature_cache_dir) if feature_cache_dir else None

    def _cache_pair(init_name: str) -> tuple[Path | None, Path | None]:
        if cache_root is None:
            return (None, None)
        return (
            cache_root / f"{backbone_name}_{init_name}_train.pt",
            cache_root / f"{backbone_name}_{init_name}_test.pt",
        )

    # Random init
    print(f"  [{backbone_name}] evaluating init: random", flush=True)
    rand_enc, feat_dim = build_ssl_encoder(backbone_name, in_channels, pretrained=False)
    random_metrics = evaluate_init(
        rand_enc, train_loader, test_loader, feat_dim, device, epochs=epochs, lr=lr,
        feature_cache=_cache_pair("random"), desc=f"{backbone_name}/random",
    )

    # ImageNet init
    print(f"  [{backbone_name}] evaluating init: imagenet", flush=True)
    imnet_enc, _ = build_ssl_encoder(backbone_name, in_channels, pretrained=True)
    imagenet_metrics = evaluate_init(
        imnet_enc, train_loader, test_loader, feat_dim, device, epochs=epochs, lr=lr,
        feature_cache=_cache_pair("imagenet"), desc=f"{backbone_name}/imagenet",
    )

    # SSL init
    print(f"  [{backbone_name}] evaluating init: ssl", flush=True)
    ssl_enc, _ = build_ssl_encoder(backbone_name, in_channels, pretrained=False)
    ckpt = torch.load(Path(ssl_ckpt_path), map_location="cpu", weights_only=False)
    load_result = ssl_enc.load_state_dict(ckpt["backbone_state_dict"], strict=False)
    if load_result.unexpected_keys:
        raise AssertionError(
            f"Unexpected keys loading SSL trunk into probe encoder: "
            f"{load_result.unexpected_keys[:10]}"
        )
    ssl_metrics = evaluate_init(
        ssl_enc, train_loader, test_loader, feat_dim, device, epochs=epochs, lr=lr,
        feature_cache=_cache_pair("ssl"), desc=f"{backbone_name}/ssl",
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
