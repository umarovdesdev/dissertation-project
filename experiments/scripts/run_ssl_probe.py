#!/usr/bin/env python3
"""CLI: linear-probe acceptance gate for SSL checkpoints (brief §8, §14 Phase 5).

For each backbone, compares random / ImageNet / SSL initializations on the
EyePACS-test probe slice (carved by the ``Usage`` column), applies the §8.4
acceptance criterion, writes ``gate_report.json``, and — when accepted — flips
``meta.gate_passed`` on the SSL checkpoint so Exp-1 will accept it.

Usage:
    python scripts/run_ssl_probe.py --config configs/default.yaml
    # CPU smoke check:
    python scripts/run_ssl_probe.py --backbone resnet50 --limit 16 \
        --device cpu --epochs 2 --ckpt <path-to-ssl.pt>
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import torch
from torch.utils.data import DataLoader

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

# Force UTF-8 stdout/stderr so non-ASCII log glyphs do not crash on Windows
# consoles using a legacy code page (e.g. cp1251).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

from src.ssl.checkpoint import checkpoint_filename, set_gate_passed  # noqa: E402
from src.ssl.dataset import EyePACSProbeDataset  # noqa: E402
from src.ssl.probe import run_probe_for_backbone  # noqa: E402
from src.utils.config import load_configs  # noqa: E402
from src.utils.seed import set_seed  # noqa: E402


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SSL linear-probe gate (brief §8).")
    parser.add_argument("--config", action="append", default=None,
                        help="YAML config path(s); repeatable. Default: configs/default.yaml.")
    parser.add_argument("--backbone", default=None,
                        help="Probe a single backbone; default: all ssl.backbones.")
    parser.add_argument("--ckpt", default=None,
                        help="Explicit SSL checkpoint path (overrides the derived name).")
    parser.add_argument("--epochs", type=int, default=None, help="Override probe.epochs.")
    parser.add_argument("--limit", type=int, default=None, help="Cap probe rows (smoke).")
    parser.add_argument("--device", default="auto", help="auto | cpu | cuda.")
    parser.add_argument("--no-feature-cache", action="store_true",
                        help="Disable the resumable on-disk feature cache "
                             "(default: cache under <out_dir>/<version>/probe_features).")
    return parser.parse_args()


def _derive_ckpt_path(config: dict, backbone: str) -> pathlib.Path:
    """Derive the canonical SSL checkpoint path for a backbone from config."""
    ssl_cfg = config["ssl"]
    ckpt_cfg = ssl_cfg.get("checkpoint", {})
    version = ckpt_cfg.get("version", "v1.0")
    fname = checkpoint_filename(
        str(ssl_cfg["method"]).lower(), backbone,
        int(ssl_cfg.get("in_channels", 4)), int(ssl_cfg.get("image_size", 256)),
        int(ssl_cfg.get("epochs", 300)),
    )
    return pathlib.Path(ckpt_cfg["out_dir"]) / version / fname


def main() -> None:
    args = _parse_args()
    config = load_configs(*(args.config or ["configs/default.yaml"]))
    set_seed(int(config.get("seed", 42)))

    ssl_cfg = config["ssl"]
    if args.epochs is not None:
        ssl_cfg.setdefault("probe", {})["epochs"] = args.epochs

    device = args.device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)

    backbones = [args.backbone] if args.backbone else list(ssl_cfg.get("backbones", ["resnet50"]))

    version = ssl_cfg.get("checkpoint", {}).get("version", "v1.0")
    out_dir = pathlib.Path(ssl_cfg["checkpoint"]["out_dir"]) / version
    # Disable the resumable feature cache for --limit smoke runs so a truncated
    # slice never poisons the cache a later full run would read.
    feature_cache_dir = (
        None if (args.no_feature_cache or args.limit is not None)
        else out_dir / "probe_features"
    )

    print("Building probe slices (Usage-based) …")
    train_ds, test_ds = EyePACSProbeDataset.build_probe_splits(config, subset_size=args.limit)
    batch = int(ssl_cfg.get("probe", {}).get("batch_size", 64))
    train_loader = DataLoader(train_ds, batch_size=batch, shuffle=False,
                              num_workers=int(ssl_cfg.get("num_workers", 0)))
    test_loader = DataLoader(test_ds, batch_size=batch, shuffle=False,
                             num_workers=int(ssl_cfg.get("num_workers", 0)))
    print(f"  probe-train={len(train_ds)} | probe-test={len(test_ds)} "
          f"| dataset={type(train_ds).__name__}")
    if feature_cache_dir is not None:
        print(f"  feature cache (resumable): {feature_cache_dir}")

    reports: dict[str, dict] = {}
    all_passed = True
    for backbone in backbones:
        ckpt_path = pathlib.Path(args.ckpt) if args.ckpt else _derive_ckpt_path(config, backbone)
        print(f"\nProbing {backbone} | ckpt={ckpt_path}")
        report = run_probe_for_backbone(
            config, backbone, ckpt_path, train_loader, test_loader, device,
            feature_cache_dir=feature_cache_dir,
        )
        reports[backbone] = report
        passed = report["acceptance"]["passed"]
        all_passed = all_passed and passed
        acc = report["acceptance"]
        print(f"  kappa: SSL={acc['kappa_ssl']:.4f} random={acc['kappa_random']:.4f} "
              f"imagenet={acc['kappa_imagenet']:.4f} -> passed={passed}")

        if passed and ckpt_path.exists():
            set_gate_passed(ckpt_path, True)
            print(f"  meta.gate_passed set to True on {ckpt_path.name}")

    out_dir.mkdir(parents=True, exist_ok=True)
    gate_report = {"backbones": reports, "all_passed": all_passed}
    report_path = out_dir / "gate_report.json"
    with open(report_path, "w") as f:
        json.dump(gate_report, f, indent=2)

    print(f"\nGate report: {report_path}")
    print(f"All backbones passed: {all_passed}")


if __name__ == "__main__":
    # CUDA + DataLoader workers: the default 'fork' start method on Linux/WSL
    # re-initialises CUDA in the child, which crashes once a CUDA context exists.
    # Force 'spawn' before any CUDA use; guard so it is a no-op when already set.
    # Datasets/transforms are pickled to spawned workers, so they must stay
    # picklable.
    import torch.multiprocessing as _mp

    try:
        _mp.set_start_method("spawn", force=True)
    except RuntimeError:
        pass
    main()
