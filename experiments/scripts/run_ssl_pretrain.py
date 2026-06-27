#!/usr/bin/env python3
"""CLI: SSL pretraining on the EyePACS test corpus (brief §3, §9, §14 Phase 2/4).

Pipeline:
    build corpus index → assert disjointness (INV-SSL-2) → two-view dataset
    → SSLTrainer (per-backbone AMP) → versioned trunk-only checkpoint + manifest.

Usage:
    python scripts/run_ssl_pretrain.py \
        --config configs/default.yaml --backbone resnet50
    python scripts/run_ssl_pretrain.py \
        --config configs/default.yaml --config configs/ssl_pretrain.yaml \
        --backbone efficientnet_b3 --screening
    # CPU smoke check (no real training):
    python scripts/run_ssl_pretrain.py --backbone resnet50 --limit 8 \
        --epochs 1 --max-steps 2 --device cpu --batch-size 2

Does NOT alter Experiment 1 — it only produces the SSL initialization.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

from torch.utils.data import DataLoader

# Allow running from repo root without installing the package.
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

# Force UTF-8 stdout/stderr so non-ASCII log glyphs do not crash on Windows
# consoles using a legacy code page (e.g. cp1251).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

from src.ssl.checkpoint import (  # noqa: E402
    SSLCheckpointManager,
    clear_train_state,
    load_train_state,
    save_train_state,
    write_manifest,
)
from src.ssl.dataset import EyePACSSSLDataset, assert_ssl_corpus_disjoint  # noqa: E402
from src.ssl.trainer import SSLTrainer  # noqa: E402
from src.ssl.transforms import build_two_view_transform, resolve_normalize_stats  # noqa: E402
from src.utils.config import load_configs  # noqa: E402
from src.utils.seed import capture_rng_state, restore_rng_state, set_seed  # noqa: E402


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SSL pretraining (brief §9).")
    parser.add_argument(
        "--config", action="append", default=None,
        help="YAML config path(s); repeatable (later overrides earlier). "
             "Default: configs/default.yaml.",
    )
    parser.add_argument("--backbone", required=True,
                        help="Backbone to pretrain (e.g. resnet50, efficientnet_b3).")
    parser.add_argument("--method", default=None, help="Override ssl.method.")
    parser.add_argument("--epochs", type=int, default=None, help="Override ssl.epochs.")
    parser.add_argument("--screening", action="store_true",
                        help="Use ssl.screening_epochs instead of ssl.epochs.")
    parser.add_argument("--batch-size", type=int, default=None, help="Override ssl.batch_size.")
    parser.add_argument("--limit", type=int, default=None,
                        help="Cap corpus rows (smoke tests).")
    parser.add_argument("--max-steps", type=int, default=None,
                        help="Hard cap on optimizer steps (smoke tests).")
    parser.add_argument("--device", default="auto", help="auto | cpu | cuda.")
    parser.add_argument("--pretrained-init", action="store_true",
                        help="Start from ImageNet (§11 continual-SSL fallback). "
                             "Flagged in the manifest. Default: from-scratch.")
    parser.add_argument("--resume", action="store_true",
                        help="Resume this backbone from its rolling train_state.pt "
                             "(method+optimizer+scaler+epoch) in the version dir, if "
                             "present. No-op when none exists. Use after a mid-run kill.")
    parser.add_argument("--skip-disjointness", action="store_true",
                        help="Skip the INV-SSL-2 assertion (e.g. when the train "
                             "labels CSV is absent on a smoke box). NOT for real runs.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    config_paths = args.config or ["configs/default.yaml"]
    config = load_configs(*config_paths)

    seed = int(config.get("seed", 42))
    set_seed(seed)

    ssl_cfg = config["ssl"]
    if args.method:
        ssl_cfg["method"] = args.method
    if args.batch_size:
        ssl_cfg["batch_size"] = args.batch_size

    epochs = args.epochs
    if epochs is None:
        epochs = int(ssl_cfg.get("screening_epochs", 100)) if args.screening \
            else int(ssl_cfg.get("epochs", 300))

    backbone = args.backbone
    method = str(ssl_cfg["method"]).lower()

    print(f"SSL pretraining | backbone={backbone} | method={method} | epochs={epochs}")
    print(f"Configs: {config_paths}")

    # ── Disjointness invariant (INV-SSL-2) ────────────────────────────────────
    corpus = ssl_cfg["corpus"]
    disjoint_audit = {"skipped": True}
    if not args.skip_disjointness:
        disjoint_audit = assert_ssl_corpus_disjoint(
            config["paths"]["eyepacs"],
            corpus["test_labels_csv"],
            corpus.get("train_labels_csv", "trainLabels.csv"),
        )
        print(f"  Disjointness OK — SSL={disjoint_audit['ssl_count']} "
              f"({disjoint_audit['ssl_patients']} patients) vs "
              f"train={disjoint_audit['train_count']} "
              f"({disjoint_audit['train_patients']} patients)")

    # ── Dataset / loader ──────────────────────────────────────────────────────
    transform = build_two_view_transform(config)
    dataset = EyePACSSSLDataset.from_config(config, transform, subset_size=args.limit)
    print(f"  Corpus images: {len(dataset)}")

    loader = DataLoader(
        dataset,
        batch_size=int(ssl_cfg.get("batch_size", 32)),
        shuffle=True,
        num_workers=int(ssl_cfg.get("num_workers", 4)),
        drop_last=True,
        pin_memory=False,
    )

    # ── Trainer ───────────────────────────────────────────────────────────────
    trainer = SSLTrainer(
        ssl_cfg, backbone, device=args.device, pretrained_init=args.pretrained_init,
    )
    print(f"  Device={trainer.device} | AMP={trainer.mixed_precision} "
          f"| feature_dim={trainer.feature_dim}")

    _mean, _std, norm_src = resolve_normalize_stats(config)
    version = ssl_cfg.get("checkpoint", {}).get("version", "v1.0")
    out_dir = pathlib.Path(ssl_cfg["checkpoint"]["out_dir"]) / version

    ckpt_mgr = SSLCheckpointManager(
        out_dir, method, backbone,
        in_channels=int(ssl_cfg.get("in_channels", 4)),
        image_size=int(ssl_cfg.get("image_size", 256)),
        seed=seed,
        normalize_stats_used=norm_src,
        keep_last=int(ssl_cfg.get("checkpoint", {}).get("keep_last", 2)),
    )
    save_every = int(ssl_cfg.get("checkpoint", {}).get("save_every", 50))
    resume_every = max(1, int(ssl_cfg.get("checkpoint", {}).get("resume_every", 1)))

    # ── Resume (optional) ─────────────────────────────────────────────────────
    # The rolling train_state.pt carries the full optimizer/EMA/method state so a
    # killed multi-day run continues from its last epoch instead of epoch 0.
    start_epoch = 0
    if args.resume:
        state = load_train_state(out_dir, backbone)
        if state is None:
            print(f"  --resume: no train_state for {backbone} in {out_dir}; starting fresh.")
        else:
            trainer.load_state_dict(state["trainer"])
            restore_rng_state(state.get("rng"))
            start_epoch = int(state["epoch"])
            print(f"  --resume: restored {backbone} at epoch {start_epoch}/{epochs} "
                  f"(global_step={state.get('global_step')}).")

    def _on_epoch_end(epoch: int, metrics: dict) -> None:
        # Resume state every `resume_every` epochs (atomic, single rolling file).
        if (epoch + 1) % resume_every == 0:
            save_train_state(
                out_dir, backbone, epoch + 1, int(metrics.get("global_step", 0)),
                trainer.state_dict(), capture_rng_state(),
            )
        # Periodic trunk-only deliverable checkpoint.
        if (epoch + 1) % save_every == 0:
            ckpt_mgr.save(epoch + 1, trainer.trunk_state_dict(), gate_passed=False)

    history = trainer.train(
        loader, epochs=epochs, on_epoch_end=_on_epoch_end, max_steps=args.max_steps,
        start_epoch=start_epoch,
    )

    # ── Final checkpoint + manifest ───────────────────────────────────────────
    final_path = ckpt_mgr.save(epochs, trainer.trunk_state_dict(), gate_passed=False)
    pretrained_init_source = "imagenet_continual" if args.pretrained_init else "from_scratch"
    manifest = {
        "backbone": backbone,
        "method": method,
        "epochs": epochs,
        "seed": seed,
        "in_channels": int(ssl_cfg.get("in_channels", 4)),
        "image_size": int(ssl_cfg.get("image_size", 256)),
        "downstream_image_size": 512,
        "normalize_stats_used": norm_src,
        "init_source": pretrained_init_source,
        "disjointness": disjoint_audit,
        "corpus_expected_count": corpus.get("expected_count"),
        "corpus_loaded_count": len(dataset),
        "checkpoint": str(final_path),
        "gate_report": str(out_dir / "gate_report.json"),
        "history_summary": {
            "first_loss": history[0]["loss"] if history else None,
            "last_loss": history[-1]["loss"] if history else None,
            "last_feat_std": history[-1]["feat_std"] if history else None,
        },
    }
    manifest_path = write_manifest(out_dir, manifest)

    # Run finished — drop the rolling resume state so a later --resume does not
    # pick up a completed run.
    clear_train_state(out_dir, backbone)

    print(f"\nDone. Checkpoint: {final_path}")
    print(f"Manifest: {manifest_path}")
    print("Next: run scripts/run_ssl_probe.py to evaluate the §8 gate.")


if __name__ == "__main__":
    # CUDA + DataLoader workers: the default 'fork' start method on Linux/WSL
    # re-initialises CUDA in the child, which crashes once the trainer has already
    # created a CUDA context. Force 'spawn' before any CUDA use; guard so it is a
    # no-op when the context is already configured. Datasets/transforms are
    # pickled to spawned workers, so they must stay picklable.
    import torch.multiprocessing as _mp

    try:
        _mp.set_start_method("spawn", force=True)
    except RuntimeError:
        pass
    main()
