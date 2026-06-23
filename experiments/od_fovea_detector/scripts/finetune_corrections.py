"""Offline fine-tune of the OD/fovea detector from clinician corrections (Phase 4).

Human-in-the-loop / active-learning loop. Starting from the frozen base weights
(``io.weights_path``), this mixes the 413-image IDRiD TRAIN split with the
exported clinician corrections (oversampled by ``finetune.correction_repeat``),
fine-tunes a few epochs at a small learning rate, and early-stops on the
held-out IDRiD-train slice — exactly the slice ``src.train`` uses, so the
IDRiD TEST split stays an honest hold-out.

The detector is **pre-trained and frozen relative to the DR classifier**:
fine-tuning happens only here, offline, and never co-trains with the DR-CNN, so
the central thesis "model = preprocessing + CNN" is preserved.

After fine-tuning, the candidate weights are evaluated on the IDRiD TEST split
and checked against the Phase-1 acceptance bar (``finetune.acceptance``). The
candidate is saved as a versioned ``od_fovea_unet_vN.pt`` with a sidecar JSON
logging which corrections went in, the base weights, and the acceptance result.
A candidate that regresses below the bar is saved but flagged ``promote=False``
— it must never replace the frozen weights.

Usage::

    conda activate dr-classifier
    cd experiments/od_fovea_detector
    python scripts/finetune_corrections.py --config configs/default.yaml

Requires torch + timm + the IDRiD dataset + a non-empty correction store.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from export_corrections import idrid_test_hashes, load_correction_samples  # noqa: E402


def _resolve(path_str: str, config_path: pathlib.Path) -> pathlib.Path:
    """Resolve a config path string relative to the config file if not absolute."""
    p = pathlib.Path(path_str)
    return p if p.is_absolute() else (config_path.resolve().parent.parent / p).resolve()


def _next_version_path(weights_dir: pathlib.Path) -> tuple[pathlib.Path, int]:
    """Pick the next ``od_fovea_unet_vN.pt`` path (base = v1, fine-tunes ≥ v2)."""
    existing = sorted(weights_dir.glob("od_fovea_unet_v*.pt"))
    max_n = 1
    for p in existing:
        try:
            n = int(p.stem.rsplit("_v", 1)[1])
        except (IndexError, ValueError):
            continue
        max_n = max(max_n, n)
    version = max_n + 1
    return weights_dir / f"od_fovea_unet_v{version}.pt", version


def _check_acceptance(test_summary: dict, bar: dict) -> tuple[bool, dict]:
    """Compare an eval summary against the Phase-1 acceptance bar.

    Args:
        test_summary: ``evaluate_split`` summary for the IDRiD test split.
        bar: ``finetune.acceptance`` thresholds.

    Returns:
        ``(passed, details)`` where ``details`` holds the measured values and
        per-criterion pass flags.
    """
    od_med = test_summary["od"]["error_od_radii"]["median"]
    od_1r = test_summary["od"]["success_within_1_od_radius"]
    fv_med = test_summary["fovea"]["error_od_radii"]["median"]
    fv_1r = test_summary["fovea"]["success_within_1_od_radius"]

    checks = {
        "od_median_radii": (od_med, od_med <= bar["od_median_radii_max"]),
        "od_within_1r": (od_1r, od_1r >= bar["od_within_1r_min"]),
        "fovea_median_radii": (fv_med, fv_med <= bar["fovea_median_radii_max"]),
        "fovea_within_1r": (fv_1r, fv_1r >= bar["fovea_within_1r_min"]),
    }
    passed = all(ok for _, ok in checks.values())
    details = {k: {"value": float(v), "passed": bool(ok)} for k, (v, ok) in checks.items()}
    return passed, details


def finetune(config_path: pathlib.Path, corrections_dir: pathlib.Path | None,
             epochs_override: int | None = None) -> int:
    """Run one fine-tune-from-corrections round and gate it on acceptance.

    Args:
        config_path: Path to the YAML config.
        corrections_dir: Override for the correction store directory.
        epochs_override: Optional override for ``finetune.epochs``.

    Returns:
        Process exit code: ``0`` if a promotable candidate was produced, ``2``
        if a candidate was produced but regressed (rejected), ``1`` if there was
        nothing to do (no corrections).
    """
    import numpy as np
    import torch
    from torch.utils.data import DataLoader

    from src.data import IDRiDLocalizationDataset, load_split
    from src.eval import evaluate_split
    from src.infer import reset_cache
    from src.losses import build_loss
    from src.model import build_model
    from src.train import _loss_target, _split_train_val, set_seed
    from src.utils import load_config, resolve_device

    cfg = load_config(config_path)
    ft = cfg["finetune"]
    set_seed(cfg["seed"])
    device = resolve_device(cfg["io"]["device"])

    root = pathlib.Path(cfg["data"]["idrid_root"])
    if not root.exists():
        raise FileNotFoundError(
            f"IDRiD localization root not found: {root}. Set data.idrid_root.")

    corr_dir = (corrections_dir if corrections_dir is not None
                else _resolve(ft["corrections_dir"], config_path))
    exclude = idrid_test_hashes(root)  # never fine-tune on test images
    corr_samples = load_correction_samples(corr_dir, exclude)
    if not corr_samples:
        print(f"No usable corrections in {corr_dir} (after excluding "
              f"{len(exclude)} IDRiD-test hashes). Nothing to fine-tune.")
        return 1

    # IDRiD TRAIN, split into the same train/val slices src.train uses.
    samples = load_split(root, "train")
    tr_samples, va_samples = _split_train_val(
        samples, cfg["data"]["val_fraction"], cfg["seed"])

    repeat = int(ft["correction_repeat"])
    combined = list(tr_samples) + corr_samples * repeat
    print(f"fine-tune set: {len(tr_samples)} IDRiD-train + "
          f"{len(corr_samples)}×{repeat} corrections = {len(combined)} samples")

    input_size = cfg["data"]["input_size"]
    heatmap_size = cfg["data"]["heatmap_size"]
    sigma = cfg["data"]["sigma_frac"] * heatmap_size

    tr_ds = IDRiDLocalizationDataset(
        combined, input_size, heatmap_size, sigma,
        augment_cfg=cfg["train"]["augmentation"], seed=cfg["seed"])
    va_ds = IDRiDLocalizationDataset(
        va_samples, input_size, heatmap_size, sigma,
        augment_cfg=None, seed=cfg["seed"])

    tr_loader = DataLoader(tr_ds, batch_size=cfg["train"]["batch_size"],
                           shuffle=True, num_workers=cfg["train"]["num_workers"],
                           drop_last=False)
    va_loader = DataLoader(va_ds, batch_size=cfg["train"]["batch_size"],
                           shuffle=False, num_workers=cfg["train"]["num_workers"])

    model = build_model(cfg["model"], heatmap_size).to(device)

    base_weights = _resolve(cfg["io"]["weights_path"], config_path)
    if not base_weights.exists():
        raise FileNotFoundError(
            f"Base weights not found: {base_weights}. Train Phase 1 first.")
    ckpt = torch.load(base_weights, map_location=device, weights_only=False)
    state = ckpt.get("state_dict", ckpt) if isinstance(ckpt, dict) else ckpt
    model.load_state_dict(state)
    print(f"loaded base weights: {base_weights}")

    sigma_norm = 2.0 * sigma / heatmap_size
    criterion = build_loss(cfg["loss"], sigma_norm)
    loss_type = cfg["loss"].get("type", "dsnt")
    opt = torch.optim.Adam(model.parameters(), lr=ft["lr"],
                           weight_decay=ft["weight_decay"])

    epochs = epochs_override or int(ft["epochs"])
    patience = int(ft["early_stopping_patience"])
    weights_dir = base_weights.parent
    cand_path, version = _next_version_path(weights_dir)

    best_val = float("inf")
    bad_epochs = 0
    best_state: dict | None = None
    for epoch in range(epochs):
        model.train()
        tr_loss = 0.0
        for img, heatmaps, coords in tr_loader:
            img = img.to(device)
            target = _loss_target(loss_type, heatmaps, coords).to(device)
            loss, _ = criterion(model(img), target)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tr_loss += float(loss.detach()) * img.size(0)
        tr_loss /= max(len(tr_ds), 1)

        model.eval()
        va_loss = 0.0
        with torch.no_grad():
            for img, heatmaps, coords in va_loader:
                img = img.to(device)
                target = _loss_target(loss_type, heatmaps, coords).to(device)
                loss, _ = criterion(model(img), target)
                va_loss += float(loss.detach()) * img.size(0)
        va_loss /= max(len(va_ds), 1)
        print(f"epoch {epoch + 1}/{epochs}  train {tr_loss:.4f}  val {va_loss:.4f}",
              flush=True)

        if va_loss < best_val - 1e-6:
            best_val = va_loss
            bad_epochs = 0
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        else:
            bad_epochs += 1
            if bad_epochs >= patience:
                print(f"early stopping at epoch {epoch + 1}", flush=True)
                break

    if best_state is not None:
        model.load_state_dict(best_state)
    torch.save({
        "state_dict": model.state_dict(),
        "config": cfg,
        "val_loss": best_val,
        "base_weights": str(base_weights),
        "version": version,
    }, cand_path)
    print(f"saved candidate weights -> {cand_path} (best val {best_val:.4f})")

    # --- Acceptance gate on the honest IDRiD test hold-out ---
    reset_cache()
    print("evaluating candidate on IDRiD test split...")
    test_summary, _ = evaluate_split(root, "test", config_path, cand_path, limit=0)
    passed, details = _check_acceptance(test_summary, ft["acceptance"])

    sidecar = cand_path.with_suffix(".json")
    sidecar.write_text(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": version,
        "weights": cand_path.name,
        "base_weights": str(base_weights),
        "corrections_dir": str(corr_dir),
        "n_corrections": len(corr_samples),
        "correction_image_hashes": [s.image_id for s in corr_samples],
        "correction_repeat": repeat,
        "idrid_test_excluded": len(exclude),
        "lr": ft["lr"],
        "epochs_run": epoch + 1,
        "best_val_loss": best_val,
        "acceptance": {"passed": passed, "bar": ft["acceptance"], "measured": details},
        "test_summary": test_summary,
        "promote": passed,
    }, indent=2), encoding="utf-8")

    print("\n=== IDRiD-test acceptance ===")
    for name, d in details.items():
        print(f"  {'PASS' if d['passed'] else 'FAIL'}  {name} = {d['value']:.4f}")
    print(f"log -> {sidecar}")
    if passed:
        print(f"\nPROMOTABLE: v{version} meets the Phase-1 bar. To freeze it, "
              f"point io.weights_path / OD_FOVEA_WEIGHTS at {cand_path.name}.")
        return 0
    print(f"\nREJECTED: v{version} regressed below the Phase-1 bar — do NOT promote.")
    return 2


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Fine-tune the OD/fovea detector from clinician corrections.")
    p.add_argument("--config", type=pathlib.Path,
                   default=pathlib.Path("configs/default.yaml"))
    p.add_argument("--corrections-dir", type=pathlib.Path, default=None,
                   help="Override the correction store directory.")
    p.add_argument("--epochs", type=int, default=None,
                   help="Override finetune.epochs (e.g. for a quick run).")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    return finetune(args.config, args.corrections_dir, args.epochs)


if __name__ == "__main__":
    raise SystemExit(main())
