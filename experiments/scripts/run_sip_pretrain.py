#!/usr/bin/env python3
"""CLI: supervised in-domain pretraining (SIP) on the 53k labeled EyePACS-test.

The SECOND candidate initialization for the Exp-1 pipeline arm (Config B/D), a
head-to-head against continual-SSL (configs/ssl_continual_v4_0.yaml). SIP supervises
the same CNN backbone on the EyePACS-test DR grades (started from ImageNet, adapted),
then transfers to Experiment 1. Governance: INVARIANTS SB-2.4 [v6.3.0] permits the
labeled use for this distinct pretraining stage; CFC-2.8 [v6.3.0] lists SIP as a
gate-selected integrated-arm init. Spec: docs/supervised_indomain_pretraining_brief.md.

Pipeline:
    testLabels15.csv -> PATIENT-LEVEL split (pretrain / holdout, seed-fixed, disjoint)
    -> supervised train on pretrain (ImageNet init, Focal + inverse-freq, early-stop on
       holdout) -> trunk-only checkpoint(s) compatible with load_ssl_backbone
    -> (--gate) frozen linear-probe on the SHARED holdout: random / ImageNet / SIP.

The trunk is built via build_ssl_encoder (identical keys to the SSL checkpoints), so
the SIP checkpoint drops into Exp-1 through the unchanged load_ssl_backbone path and is
probed by the unchanged evaluate_init. Two 4-channel views are NOT used — SIP is
single-view supervised; labels replace the SSL positive pair.

Usage:
    # train (per backbone):
    python scripts/run_sip_pretrain.py \
        --config configs/default.yaml --config configs/_win_local.yaml \
        --config configs/sip_pretrain.yaml --backbone resnet50 --device cuda
    # gate a trained checkpoint on the shared holdout:
    python scripts/run_sip_pretrain.py <same configs> --backbone resnet50 --device cuda \
        --gate --ckpt C:/ssl_out/sip/v1.0/ssl_sip_resnet50_4ch_256_ep40.pt
    # CPU smoke:
    python scripts/run_sip_pretrain.py --backbone resnet50 --limit 64 --epochs 1 \
        --max-steps 2 --device cpu --batch-size 8 --skip-disjointness
"""

from __future__ import annotations

import argparse
import json
import math
import os
import pathlib
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# Allow running from repo root without installing the package.
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

from src.data.datasets import load_cache_meta  # noqa: E402
from src.evaluation.metrics import compute_primary_metrics  # noqa: E402
from src.ssl.checkpoint import save_ssl_checkpoint, set_gate_passed, write_manifest  # noqa: E402
from src.ssl.dataset import (  # noqa: E402
    CachedEyePACSProbeDataset,
    _eye_side_from_name,
    assert_ssl_corpus_disjoint,
    build_ssl_base_pipeline,
)
from src.ssl.encoder import build_ssl_encoder  # noqa: E402
from src.ssl.probe import decide_acceptance, evaluate_init  # noqa: E402
from src.ssl.transforms import resolve_normalize_stats  # noqa: E402
from src.training.losses import compute_class_weights, create_loss  # noqa: E402
from src.utils.config import load_configs  # noqa: E402
from src.utils.seed import set_seed  # noqa: E402


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Supervised in-domain pretraining (SIP).")
    parser.add_argument("--config", action="append", default=None,
                        help="YAML config path(s); repeatable (later overrides earlier).")
    parser.add_argument("--backbone", required=True,
                        help="Backbone to pretrain (resnet50 | efficientnet_b3).")
    parser.add_argument("--epochs", type=int, default=None, help="Override sip.epochs.")
    parser.add_argument("--batch-size", type=int, default=None, help="Override sip.batch_size.")
    parser.add_argument("--limit", type=int, default=None,
                        help="Cap corpus rows AFTER the split (smoke tests).")
    parser.add_argument("--max-steps", type=int, default=None,
                        help="Hard cap on optimizer steps per epoch (smoke tests).")
    parser.add_argument("--device", default="auto", help="auto | cpu | cuda.")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from the rolling sip_train_state_<backbone>.pt.")
    parser.add_argument("--gate", action="store_true",
                        help="Gate-only mode: frozen linear-probe on the shared holdout "
                             "for random / ImageNet / SIP (no training).")
    parser.add_argument("--ckpt", default=None,
                        help="Checkpoint to gate (--gate mode). Default: the ep<epochs> file.")
    parser.add_argument("--skip-disjointness", action="store_true",
                        help="Skip the INV-SSL-2 assertion (smoke boxes only).")
    return parser.parse_args()


def _resolve_device(name: str) -> torch.device:
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(name)


# ---------------------------------------------------------------------------
# Data: patient-level split + cached labeled datasets
# ---------------------------------------------------------------------------

def _cache_dir(config: dict[str, Any], sip_cfg: dict[str, Any]) -> Path | None:
    """Resolve the Stage 0-4 cache dir (sip.cache_dir, else ssl.cache_dir)."""
    cd = sip_cfg.get("cache_dir") or config.get("ssl", {}).get("cache_dir")
    if cd and (Path(cd) / "cache_meta.csv").exists():
        return Path(cd)
    return None


def build_patient_split(
    config: dict[str, Any],
    sip_cfg: dict[str, Any],
    cached_names: set[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carve the 53k into pretrain / holdout at PATIENT level (SB-2.4 [v6.3.0] (c)).

    Reads testLabels15.csv, keeps only rows present in the cache, groups by patient
    id (numeric stem prefix), and assigns a seed-fixed ``holdout_frac`` of *patients*
    to the holdout — so no patient appears in both, and the acceptance gate never
    tests on a patient the backbone trained on.

    Args:
        config: Full config dict (``paths.eyepacs``, ``ssl.corpus``).
        sip_cfg: The ``sip`` config block (reads ``split`` sub-block).
        cached_names: Image stems present in the Stage 0-4 cache.

    Returns:
        Tuple ``(pretrain_df, holdout_df)`` with columns ``image``, ``level``.
    """
    corpus = config["ssl"]["corpus"]
    split_cfg = sip_cfg.get("split", {})
    labels_csv = Path(config["paths"]["eyepacs"]) / split_cfg.get(
        "labels_csv", corpus["test_labels_csv"]
    )
    holdout_frac = float(split_cfg.get("holdout_frac", 0.15))
    seed = int(split_cfg.get("seed", 42))

    df = pd.read_csv(labels_csv)
    df = df[df["image"].astype(str).isin(cached_names)].reset_index(drop=True)
    df["patient"] = df["image"].astype(str).str.split("_").str[0]

    patients = np.array(sorted(df["patient"].unique()))
    rng = np.random.default_rng(seed)
    rng.shuffle(patients)
    n_hold = max(1, int(round(holdout_frac * len(patients))))
    holdout_patients = set(patients[:n_hold].tolist())

    hold_mask = df["patient"].isin(holdout_patients)
    holdout_df = df[hold_mask].reset_index(drop=True)
    pretrain_df = df[~hold_mask].reset_index(drop=True)

    # Hard leakage assertion (mirrors INV-SSL-1/2 style).
    overlap = set(pretrain_df["patient"]) & set(holdout_df["patient"])
    assert not overlap, f"SIP split leak: {len(overlap)} patients in both slices."
    return pretrain_df, holdout_df


def make_cached_dataset(
    df: pd.DataFrame,
    cache_dir: Path,
    cache_meta: dict[str, Any],
    preprocessing: Any,
) -> CachedEyePACSProbeDataset:
    """Build a labeled cached dataset yielding ``(4ch tensor, DR grade)`` from a split df."""
    paths, labels, sides = [], [], []
    for _, row in df.iterrows():
        name = str(row["image"])
        png = cache_dir / f"{name}.png"
        if not png.exists():
            continue
        paths.append(str(png))
        labels.append(int(row["level"]))
        sides.append(_eye_side_from_name(name))
    return CachedEyePACSProbeDataset(paths, labels, sides, preprocessing, cache_meta)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class SIPModel(nn.Module):
    """ImageNet-initialized trunk (build_ssl_encoder) + a fresh linear DR head.

    The trunk is the exact head-stripped backbone the SSL checkpoints use, so
    ``self.trunk.state_dict()`` is a drop-in ``backbone_state_dict`` for
    :func:`~src.ssl.loader.load_ssl_backbone` and the probe encoder.
    """

    def __init__(self, backbone: str, in_channels: int, num_classes: int) -> None:
        super().__init__()
        self.trunk, self.feature_dim = build_ssl_encoder(
            backbone, in_channels=in_channels, pretrained=True
        )
        self.head = nn.Linear(self.feature_dim, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.trunk(x))


# ---------------------------------------------------------------------------
# Train / eval
# ---------------------------------------------------------------------------

def _cosine_warmup_lr(epoch: int, warmup: int, total: int) -> float:
    """Per-epoch LR multiplier: linear warmup then cosine decay to ~0."""
    if warmup > 0 and epoch < warmup:
        return (epoch + 1) / warmup
    if total <= warmup:
        return 1.0
    progress = (epoch - warmup) / max(1, total - warmup)
    return 0.5 * (1.0 + math.cos(math.pi * min(1.0, progress)))


@torch.no_grad()
def evaluate_holdout(model: nn.Module, loader: DataLoader, device: torch.device) -> dict:
    """Weighted-F1 (+ primary metrics) of the SIP head on the holdout split."""
    model.eval()
    ys, ps = [], []
    for x, y in loader:
        logits = model(x.to(device))
        ps.append(logits.argmax(1).cpu())
        ys.append(y if isinstance(y, torch.Tensor) else torch.as_tensor(y))
    y_true = torch.cat(ys).numpy()
    y_pred = torch.cat(ps).numpy()
    return compute_primary_metrics(y_true, y_pred, None, num_classes=5)


def _train_state_path(out_dir: Path, backbone: str) -> Path:
    return out_dir / f"sip_train_state_{backbone}.pt"


def train(args: argparse.Namespace, config: dict[str, Any]) -> None:
    sip_cfg = config["sip"]
    backbone = args.backbone
    device = _resolve_device(args.device)
    seed = int(sip_cfg.get("seed", config.get("seed", 42)))
    set_seed(seed)

    epochs = int(args.epochs if args.epochs is not None else sip_cfg.get("epochs", 40))
    batch_size = int(args.batch_size if args.batch_size is not None
                     else sip_cfg.get("batch_size", 96))
    image_size = int(sip_cfg.get("image_size", 256))
    in_channels = int(sip_cfg.get("in_channels", 4))
    num_workers = int(sip_cfg.get("num_workers", config.get("ssl", {}).get("num_workers", 4)))
    amp = bool(sip_cfg.get("mixed_precision", {}).get(backbone, backbone == "resnet50")) \
        and device.type == "cuda"

    print(f"SIP pretraining | backbone={backbone} | epochs={epochs} | batch={batch_size} "
          f"| device={device} | AMP={amp}")
    print(f"Configs: {args.config}")

    # ── Disjointness (INV-SSL-2) ──────────────────────────────────────────────
    corpus = config["ssl"]["corpus"]
    disjoint_audit: dict[str, Any] = {"skipped": True}
    if not args.skip_disjointness:
        disjoint_audit = assert_ssl_corpus_disjoint(
            config["paths"]["eyepacs"], corpus["test_labels_csv"],
            corpus.get("train_labels_csv", "trainLabels.csv"),
        )
        print(f"  Disjointness OK — SSL={disjoint_audit['ssl_count']} "
              f"({disjoint_audit['ssl_patients']} patients)")

    # ── Data ──────────────────────────────────────────────────────────────────
    cache_dir = _cache_dir(config, sip_cfg)
    if cache_dir is None:
        raise FileNotFoundError(
            "SIP requires the Stage 0-4 cache (sip.cache_dir / ssl.cache_dir). "
            "Build it with scripts/precompute_ssl_cache.py."
        )
    cache_meta = load_cache_meta(cache_dir)
    cached_names = set(cache_meta.keys())
    preprocessing = build_ssl_base_pipeline(config.get("preprocessing"), image_size)

    pretrain_df, holdout_df = build_patient_split(config, sip_cfg, cached_names)
    if args.limit is not None:
        pretrain_df = pretrain_df.iloc[: args.limit].reset_index(drop=True)
        holdout_df = holdout_df.iloc[: max(8, args.limit // 4)].reset_index(drop=True)

    train_ds = make_cached_dataset(pretrain_df, cache_dir, cache_meta, preprocessing)
    holdout_ds = make_cached_dataset(holdout_df, cache_dir, cache_meta, preprocessing)
    print(f"  Split (patient-level): pretrain={len(train_ds)} imgs / "
          f"{pretrain_df['patient'].nunique()} patients | "
          f"holdout={len(holdout_ds)} imgs / {holdout_df['patient'].nunique()} patients")

    train_loader = DataLoader(
        train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers,
        drop_last=True, pin_memory=False,
    )
    holdout_loader = DataLoader(
        holdout_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers,
        pin_memory=False,
    )

    # ── Model / loss / optim ──────────────────────────────────────────────────
    model = SIPModel(backbone, in_channels, num_classes=5).to(device)
    class_weights = compute_class_weights(
        [int(v) for v in pretrain_df["level"].tolist()], num_classes=5,
        method=str(sip_cfg.get("loss", {}).get("class_weights", "inverse_frequency")),
    )
    criterion = create_loss(
        class_weights=class_weights, device=str(device),
        loss_type=str(sip_cfg.get("loss", {}).get("type", "focal")),
        gamma=float(sip_cfg.get("loss", {}).get("gamma", 2.0)),
    )
    opt_cfg = sip_cfg.get("optimizer", {})
    base_lr = float(opt_cfg.get("lr", 3.0e-4))
    warmup = int(opt_cfg.get("warmup_epochs", 2))
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=base_lr,
        weight_decay=float(opt_cfg.get("weight_decay", 1.0e-4)),
    )
    scaler = torch.amp.GradScaler("cuda", enabled=amp)
    grad_clip = float(sip_cfg.get("grad_clip", 1.0))

    _mean, _std, norm_src = resolve_normalize_stats(config)
    ckpt_cfg = sip_cfg.get("checkpoint", {})
    version = str(ckpt_cfg.get("version", "v1.0"))
    out_dir = Path(ckpt_cfg.get("out_dir", "outputs/sip")) / "sip" / version
    out_dir.mkdir(parents=True, exist_ok=True)
    save_every = int(ckpt_cfg.get("save_every", 5))

    # ── Resume ────────────────────────────────────────────────────────────────
    start_epoch, best_f1, best_epoch = 0, -1.0, 0
    ts_path = _train_state_path(out_dir, backbone)
    if args.resume and ts_path.exists():
        st = torch.load(ts_path, map_location="cpu", weights_only=False)
        model.load_state_dict(st["model"])
        optimizer.load_state_dict(st["optimizer"])
        scaler.load_state_dict(st["scaler"])
        start_epoch, best_f1, best_epoch = st["epoch"], st["best_f1"], st["best_epoch"]
        print(f"  --resume: restored at epoch {start_epoch}/{epochs} (best F1={best_f1:.4f}).")

    def _save_trunk(ep: int, gate_passed: bool = False) -> Path:
        return save_ssl_checkpoint(
            out_dir, method="sip", backbone=backbone, in_channels=in_channels,
            image_size=image_size, epochs=ep, seed=seed,
            backbone_state_dict=model.trunk.state_dict(),
            normalize_stats_used=norm_src, gate_passed=gate_passed,
            extra_meta={
                "init_source": "imagenet_supervised",
                "sip": True,
                "holdout_frac": float(sip_cfg.get("split", {}).get("holdout_frac", 0.15)),
                "split_seed": int(sip_cfg.get("split", {}).get("seed", 42)),
            },
        )

    # ── Train loop ────────────────────────────────────────────────────────────
    history: list[dict] = []
    for epoch in range(start_epoch, epochs):
        for g in optimizer.param_groups:
            g["lr"] = base_lr * _cosine_warmup_lr(epoch, warmup, epochs)
        model.train()
        running, nseen = 0.0, 0
        for step, (x, y) in enumerate(train_loader):
            if args.max_steps is not None and step >= args.max_steps:
                break
            x, y = x.to(device), y.long().to(device)
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", enabled=amp):
                loss = criterion(model(x), y)
            scaler.scale(loss).backward()
            if grad_clip > 0:
                scaler.unscale_(optimizer)
                nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            scaler.step(optimizer)
            scaler.update()
            running += float(loss.item()) * x.size(0)
            nseen += x.size(0)

        train_loss = running / max(1, nseen)
        hold = evaluate_holdout(model, holdout_loader, device)
        f1 = float(hold["weighted_f1"])
        lr_now = optimizer.param_groups[0]["lr"]
        print(f"  ep{epoch + 1}/{epochs} | loss={train_loss:.4f} | lr={lr_now:.2e} | "
              f"holdout_f1={f1:.4f} | holdout_kappa={hold.get('cohen_kappa_quadratic', 0):.4f}",
              flush=True)
        history.append({"epoch": epoch + 1, "loss": train_loss, "holdout_f1": f1,
                        "holdout_kappa": float(hold.get("cohen_kappa_quadratic", 0.0))})

        if (epoch + 1) % save_every == 0 or (epoch + 1) == epochs:
            _save_trunk(epoch + 1, gate_passed=False)
        if f1 > best_f1:
            best_f1, best_epoch = f1, epoch + 1
            best_path = _save_trunk(epoch + 1, gate_passed=False)
            # Stable pointer to the best epoch for the gate step.
            (out_dir / f"BEST_{backbone}.txt").write_text(
                f"{best_path.name}\nepoch={best_epoch}\nholdout_f1={best_f1:.4f}\n"
            )

        # Rolling resume state (atomic).
        tmp = ts_path.with_suffix(".pt.tmp")
        torch.save({"epoch": epoch + 1, "model": model.state_dict(),
                    "optimizer": optimizer.state_dict(), "scaler": scaler.state_dict(),
                    "best_f1": best_f1, "best_epoch": best_epoch}, tmp)
        os.replace(tmp, ts_path)

    # ── Manifest + split id-lists ─────────────────────────────────────────────
    (out_dir / f"pretrain_ids_{backbone}.txt").write_text(
        "\n".join(pretrain_df["image"].astype(str).tolist())
    )
    (out_dir / f"holdout_ids_{backbone}.txt").write_text(
        "\n".join(holdout_df["image"].astype(str).tolist())
    )
    write_manifest(out_dir, {
        "run": "sip", "backbone": backbone, "epochs": epochs, "seed": seed,
        "init_source": "imagenet_supervised", "in_channels": in_channels,
        "image_size": image_size, "downstream_image_size": 512,
        "normalize_stats_used": norm_src, "disjointness": disjoint_audit,
        "n_pretrain": len(train_ds), "n_holdout": len(holdout_ds),
        "n_pretrain_patients": int(pretrain_df["patient"].nunique()),
        "n_holdout_patients": int(holdout_df["patient"].nunique()),
        "best_epoch": best_epoch, "best_holdout_f1": best_f1,
        "history": history,
        "gate_report": str(out_dir / f"gate_report_{backbone}.json"),
    })
    if ts_path.exists() and (start_epoch < epochs):
        ts_path.unlink()  # clean finish
    print(f"\nDone. Best holdout F1={best_f1:.4f} at epoch {best_epoch}. Dir: {out_dir}")
    print(f"Next: --gate --ckpt {out_dir}/ (see BEST_{backbone}.txt) to run the acceptance gate.")


# ---------------------------------------------------------------------------
# Gate (shared holdout; reuses evaluate_init / decide_acceptance)
# ---------------------------------------------------------------------------

def gate(args: argparse.Namespace, config: dict[str, Any]) -> None:
    sip_cfg = config["sip"]
    backbone = args.backbone
    device = _resolve_device(args.device)
    seed = int(sip_cfg.get("seed", config.get("seed", 42)))
    set_seed(seed)

    image_size = int(sip_cfg.get("image_size", 256))
    in_channels = int(sip_cfg.get("in_channels", 4))
    num_workers = int(sip_cfg.get("num_workers", config.get("ssl", {}).get("num_workers", 4)))
    probe_cfg = config["ssl"].get("probe", {})
    gate_cfg = sip_cfg.get("gate", {})
    probe_train_cap = int(gate_cfg.get("probe_train_cap", 12000))
    probe_bs = int(probe_cfg.get("batch_size", 128))

    cache_dir = _cache_dir(config, sip_cfg)
    if cache_dir is None:
        raise FileNotFoundError("SIP gate requires the Stage 0-4 cache.")
    cache_meta = load_cache_meta(cache_dir)
    cached_names = set(cache_meta.keys())
    preprocessing = build_ssl_base_pipeline(config.get("preprocessing"), image_size)

    # SAME patient-level split as training (seed-fixed) -> holdout unseen by SIP.
    pretrain_df, holdout_df = build_patient_split(config, sip_cfg, cached_names)
    if probe_train_cap and len(pretrain_df) > probe_train_cap:
        pretrain_df = pretrain_df.sample(
            n=probe_train_cap, random_state=seed
        ).reset_index(drop=True)

    probe_train_ds = make_cached_dataset(pretrain_df, cache_dir, cache_meta, preprocessing)
    probe_test_ds = make_cached_dataset(holdout_df, cache_dir, cache_meta, preprocessing)
    train_loader = DataLoader(probe_train_ds, batch_size=probe_bs, shuffle=False,
                              num_workers=num_workers, pin_memory=False)
    test_loader = DataLoader(probe_test_ds, batch_size=probe_bs, shuffle=False,
                             num_workers=num_workers, pin_memory=False)
    print(f"SIP gate | backbone={backbone} | probe_train={len(probe_train_ds)} "
          f"| holdout={len(probe_test_ds)} | device={device}")

    ckpt_cfg = sip_cfg.get("checkpoint", {})
    out_dir = Path(ckpt_cfg.get("out_dir", "outputs/sip")) / "sip" / str(ckpt_cfg.get("version", "v1.0"))
    ckpt_path = Path(args.ckpt) if args.ckpt else None
    if ckpt_path is None:
        best_ptr = out_dir / f"BEST_{backbone}.txt"
        if best_ptr.exists():
            ckpt_path = out_dir / best_ptr.read_text().splitlines()[0].strip()
        else:
            raise FileNotFoundError(f"No --ckpt and no BEST_{backbone}.txt in {out_dir}.")

    epochs = int(probe_cfg.get("epochs", 50))
    lr = float(probe_cfg.get("lr", 0.1))
    fc_dir = out_dir / f"probe_features_{backbone}"

    def _cache_pair(init: str) -> tuple[Path, Path]:
        return (fc_dir / f"{backbone}_{init}_train.pt", fc_dir / f"{backbone}_{init}_test.pt")

    print(f"  [{backbone}] random", flush=True)
    rand_enc, feat_dim = build_ssl_encoder(backbone, in_channels, pretrained=False)
    random_m = evaluate_init(rand_enc, train_loader, test_loader, feat_dim, device,
                             epochs=epochs, lr=lr, feature_cache=_cache_pair("random"),
                             desc=f"{backbone}/random")
    print(f"  [{backbone}] imagenet", flush=True)
    imnet_enc, _ = build_ssl_encoder(backbone, in_channels, pretrained=True)
    imagenet_m = evaluate_init(imnet_enc, train_loader, test_loader, feat_dim, device,
                               epochs=epochs, lr=lr, feature_cache=_cache_pair("imagenet"),
                               desc=f"{backbone}/imagenet")
    print(f"  [{backbone}] sip ({ckpt_path.name})", flush=True)
    sip_enc, _ = build_ssl_encoder(backbone, in_channels, pretrained=False)
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    res = sip_enc.load_state_dict(ckpt["backbone_state_dict"], strict=False)
    if res.unexpected_keys:
        raise AssertionError(f"Unexpected keys loading SIP trunk: {res.unexpected_keys[:10]}")
    sip_m = evaluate_init(sip_enc, train_loader, test_loader, feat_dim, device,
                          epochs=epochs, lr=lr, feature_cache=_cache_pair("sip"),
                          desc=f"{backbone}/sip")

    acceptance = decide_acceptance(
        sip_m, random_m, imagenet_m,
        accept_vs_random_kappa_delta=float(probe_cfg.get("accept_vs_random_kappa_delta", 0.05)),
        accept_vs_imagenet_kappa_margin=float(probe_cfg.get("accept_vs_imagenet_kappa_margin", -0.03)),
    )
    report = {"backbone": backbone, "sip_checkpoint": str(ckpt_path), "holdout": "patient_level",
              "random": random_m, "imagenet": imagenet_m, "sip": sip_m, "acceptance": acceptance}
    report_path = out_dir / f"gate_report_{backbone}.json"
    report_path.write_text(json.dumps(report, indent=2, default=float))

    print(f"\n  kappa: SIP={acceptance['kappa_ssl']:.4f} "
          f"random={acceptance['kappa_random']:.4f} imagenet={acceptance['kappa_imagenet']:.4f} "
          f"-> passed={acceptance['passed']}")
    if acceptance["passed"]:
        set_gate_passed(ckpt_path, True)
        print(f"  gate PASSED — flipped meta.gate_passed=True on {ckpt_path.name}")
    else:
        print("  gate FAILED — meta.gate_passed left False; SIP does not enter Exp-1.")
    print(f"  Report: {report_path}")


def main() -> None:
    args = _parse_args()
    config = load_configs(*(args.config or ["configs/default.yaml"]))
    if "sip" not in config:
        raise KeyError("Config has no `sip:` block — load configs/sip_pretrain.yaml.")
    if args.gate:
        gate(args, config)
    else:
        train(args, config)


if __name__ == "__main__":
    import torch.multiprocessing as _mp
    try:
        _mp.set_start_method("spawn", force=True)
    except RuntimeError:
        pass
    main()
