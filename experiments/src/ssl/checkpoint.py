"""Versioned, trunk-only SSL checkpoint artifacts + manifest (brief §9.2/§9.3).

A checkpoint stores **only the trunk weights** (4-channel stem included, no
classifier head) plus a ``meta`` block, so it drops straight into a factory
model via :func:`~src.ssl.loader.load_ssl_backbone`. Naming:

    ssl_<method>_<backbone>_<in_channels>ch_<res>_ep<epochs>.pt
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

import torch


def checkpoint_filename(
    method: str, backbone: str, in_channels: int, image_size: int, epochs: int
) -> str:
    """Return the canonical checkpoint filename (brief §9.2).

    Args:
        method: SSL method name (e.g. ``"byol"``).
        backbone: Backbone name (e.g. ``"resnet50"``).
        in_channels: Input channel count (4).
        image_size: Pretraining resolution (256).
        epochs: Number of pretraining epochs.

    Returns:
        Filename string ``ssl_<method>_<backbone>_<ch>ch_<res>_ep<epochs>.pt``.
    """
    return f"ssl_{method}_{backbone}_{in_channels}ch_{image_size}_ep{epochs}.pt"


def _git_commit() -> str:
    """Return the current git commit hash, or ``"unknown"`` if unavailable."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def save_ssl_checkpoint(
    out_dir: str | Path,
    method: str,
    backbone: str,
    in_channels: int,
    image_size: int,
    epochs: int,
    seed: int,
    backbone_state_dict: dict[str, torch.Tensor],
    normalize_stats_used: str,
    gate_passed: bool,
    config_hash: str = "",
    extra_meta: dict[str, Any] | None = None,
) -> Path:
    """Write a versioned trunk-only SSL checkpoint (brief §9.2).

    Args:
        out_dir: Versioned output directory (e.g. ``outputs/ssl/v1.0``).
        method: SSL method name.
        backbone: Backbone name.
        in_channels: Input channel count (4).
        image_size: Pretraining resolution (256).
        epochs: Number of pretraining epochs.
        seed: Training seed.
        backbone_state_dict: Trunk-only weights (head excluded).
        normalize_stats_used: ``"imagenet"`` or ``"dataset_specific"`` — which
            Stage-7 stats produced the SSL base tensor.
        gate_passed: Whether the §8 linear-probe gate has passed (False until the
            gate runs; updated by the probe step).
        config_hash: Optional hash of the resolved config for auditability.
        extra_meta: Optional extra metadata merged into ``meta``.

    Returns:
        Path to the written ``.pt`` file.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = checkpoint_filename(method, backbone, in_channels, image_size, epochs)
    path = out_dir / fname

    meta: dict[str, Any] = {
        "method": method,
        "backbone": backbone,
        "in_channels": in_channels,
        "image_size": image_size,
        "epochs": epochs,
        "seed": seed,
        "normalize_stats_used": normalize_stats_used,
        "ssl_corpus": "EyePACS/test",
        "corpus_count": 53576,
        "git_commit": _git_commit(),
        "config_hash": config_hash,
        "gate_passed": bool(gate_passed),
    }
    if extra_meta:
        meta.update(extra_meta)

    torch.save({"backbone_state_dict": backbone_state_dict, "meta": meta}, path)
    return path


def set_gate_passed(ckpt_path: str | Path, gate_passed: bool) -> None:
    """Update the ``meta.gate_passed`` flag of an existing checkpoint in place.

    Args:
        ckpt_path: Path to the ``.pt`` checkpoint.
        gate_passed: New value of the gate flag.
    """
    ckpt_path = Path(ckpt_path)
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    ckpt["meta"]["gate_passed"] = bool(gate_passed)
    torch.save(ckpt, ckpt_path)


def train_state_filename(backbone: str) -> str:
    """Return the rolling resume-checkpoint filename for ``backbone``.

    One file per backbone (ResNet-50 and EfficientNet-B3 share a version dir),
    overwritten each cycle — this is the *resume* state, not a deliverable.

    Args:
        backbone: Backbone name (e.g. ``"resnet50"``).

    Returns:
        Filename string ``train_state_<backbone>.pt``.
    """
    return f"train_state_{backbone}.pt"


def save_train_state(
    out_dir: str | Path,
    backbone: str,
    epoch: int,
    global_step: int,
    trainer_state: dict[str, Any],
    rng_state: dict[str, Any] | None = None,
) -> Path:
    """Persist the full training state so a killed run can resume (brief §9.2).

    Writes a single rolling file per backbone holding the next epoch to run, the
    global step, the trainer state (method + optimizer + AMP scaler) and an
    optional RNG snapshot. The write is **atomic** (temp file + ``os.replace``)
    so a kill mid-write cannot corrupt the resume point — critical on a machine
    that has been observed to drop the job mid-run.

    Args:
        out_dir: Versioned output directory (e.g. ``outputs/ssl/v1.0``).
        backbone: Backbone name.
        epoch: Number of epochs completed (the epoch to resume *at*).
        global_step: Optimizer steps completed so far.
        trainer_state: ``SSLTrainer.state_dict()`` output.
        rng_state: Optional ``capture_rng_state()`` snapshot.

    Returns:
        Path to the written ``.pt`` file.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / train_state_filename(backbone)
    payload = {
        "epoch": int(epoch),
        "global_step": int(global_step),
        "backbone": backbone,
        "trainer": trainer_state,
        "rng": rng_state or {},
    }
    tmp = path.with_name(path.name + ".tmp")
    torch.save(payload, tmp)
    os.replace(tmp, path)
    return path


def load_train_state(out_dir: str | Path, backbone: str) -> dict[str, Any] | None:
    """Load the rolling resume checkpoint for ``backbone`` if it exists.

    Args:
        out_dir: Versioned output directory.
        backbone: Backbone name.

    Returns:
        The payload written by :func:`save_train_state`, or ``None`` if no
        resume state is present.
    """
    path = Path(out_dir) / train_state_filename(backbone)
    if not path.exists():
        return None
    return torch.load(path, map_location="cpu", weights_only=False)


def clear_train_state(out_dir: str | Path, backbone: str) -> None:
    """Remove the rolling resume checkpoint for ``backbone`` (run completed).

    Args:
        out_dir: Versioned output directory.
        backbone: Backbone name.
    """
    path = Path(out_dir) / train_state_filename(backbone)
    if path.exists():
        path.unlink()


def write_manifest(out_dir: str | Path, manifest: dict[str, Any]) -> Path:
    """Write the run manifest JSON (brief §9.3).

    Args:
        out_dir: Versioned output directory.
        manifest: Manifest dict (resolved config, corpus sizes, disjointness
            result, normalization stats, training-curve summary, gate pointers).

    Returns:
        Path to ``manifest.json``.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "manifest.json"
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
    return path


class SSLCheckpointManager:
    """Periodic versioned checkpointing with keep-last retention (brief §9.2).

    Mirrors :class:`~src.training.checkpoint.CheckpointManager` save/keep-last
    patterns, but persists the trunk-only artifact in the SSL format.

    Args:
        out_dir: Versioned output directory (e.g. ``outputs/ssl/v1.0``).
        method: SSL method name.
        backbone: Backbone name.
        in_channels: Input channel count.
        image_size: Pretraining resolution.
        seed: Training seed.
        normalize_stats_used: Stage-7 stats identifier.
        keep_last: Max number of periodic checkpoints to retain.
        config_hash: Optional config hash.
    """

    def __init__(
        self,
        out_dir: str | Path,
        method: str,
        backbone: str,
        in_channels: int,
        image_size: int,
        seed: int,
        normalize_stats_used: str,
        keep_last: int = 2,
        config_hash: str = "",
    ) -> None:
        self.out_dir = Path(out_dir)
        self.method = method
        self.backbone = backbone
        self.in_channels = in_channels
        self.image_size = image_size
        self.seed = seed
        self.normalize_stats_used = normalize_stats_used
        self.keep_last = keep_last
        self.config_hash = config_hash
        self._saved: list[Path] = []

    def save(
        self,
        epochs_done: int,
        backbone_state_dict: dict[str, torch.Tensor],
        gate_passed: bool = False,
        extra_meta: dict[str, Any] | None = None,
    ) -> Path:
        """Save a checkpoint tagged with the epochs completed; prune old ones.

        Args:
            epochs_done: Epoch count encoded in the filename.
            backbone_state_dict: Trunk-only weights.
            gate_passed: Gate flag (usually False until the probe runs).
            extra_meta: Optional extra metadata.

        Returns:
            Path to the written checkpoint.
        """
        path = save_ssl_checkpoint(
            self.out_dir, self.method, self.backbone, self.in_channels,
            self.image_size, epochs_done, self.seed, backbone_state_dict,
            self.normalize_stats_used, gate_passed, self.config_hash, extra_meta,
        )
        if path not in self._saved:
            self._saved.append(path)
        while len(self._saved) > self.keep_last:
            old = self._saved.pop(0)
            # Never delete the just-written checkpoint.
            if old != path and old.exists():
                old.unlink()
        return path
