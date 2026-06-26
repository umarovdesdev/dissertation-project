"""Exp-1 integration loader: drop an SSL trunk into a factory model (brief §10).

``load_ssl_backbone`` loads the trunk-only ``backbone_state_dict`` from an SSL
checkpoint into a factory model built with ``in_channels=4``, leaving a **fresh**
5-class head (the SSL ``.pt`` carries no classifier). It strict-loads the trunk,
asserts the 4-channel stem, optionally enforces the ``gate_passed`` flag, and
reports any missing / unexpected keys.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import torch
import torch.nn as nn


def _stem_in_channels(model: nn.Module) -> int | None:
    """Return the input channel count of the model's first conv, if found."""
    if hasattr(model, "conv1") and isinstance(model.conv1, nn.Conv2d):
        return model.conv1.in_channels
    if hasattr(model, "conv_stem") and isinstance(model.conv_stem, nn.Conv2d):
        return model.conv_stem.in_channels
    for module in model.modules():
        if isinstance(module, nn.Conv2d):
            return module.in_channels
    return None


def _head_key_prefixes(model: nn.Module) -> tuple[str, ...]:
    """Return the state-dict key prefixes of the classification head."""
    prefixes: list[str] = []
    if hasattr(model, "fc"):
        prefixes.append("fc.")
    if hasattr(model, "classifier"):
        prefixes.append("classifier.")
    return tuple(prefixes)


def load_ssl_backbone(
    model: nn.Module,
    ckpt_path: str | Path,
    require_gate_passed: bool = True,
    strict_trunk: bool = True,
) -> dict[str, Any]:
    """Load an SSL trunk checkpoint into a factory model (fresh head retained).

    Args:
        model: A factory model built with ``in_channels=4`` (e.g. via
            ``create_model(name, {"pretrained": False, "in_channels": 4, ...})``)
            carrying a fresh, randomly-initialized classifier head.
        ckpt_path: Path to the SSL ``.pt`` (``backbone_state_dict`` + ``meta``).
        require_gate_passed: If ``True``, refuse to load a checkpoint whose
            ``meta.gate_passed`` is not ``True`` (fail-fast gate, brief §10.3).
        strict_trunk: If ``True``, assert that the only missing keys are the head
            keys and that there are no unexpected keys.

    Returns:
        The checkpoint ``meta`` dict.

    Raises:
        FileNotFoundError: If ``ckpt_path`` does not exist.
        RuntimeError: If ``require_gate_passed`` and the gate has not passed.
        AssertionError: If the model stem is not 4-channel, or (under
            ``strict_trunk``) trunk keys do not match cleanly.
    """
    ckpt_path = Path(ckpt_path)
    if not ckpt_path.exists():
        raise FileNotFoundError(
            f"SSL checkpoint not found: {ckpt_path}. Pretrain + gate it first "
            f"(scripts/run_ssl_pretrain.py, scripts/run_ssl_probe.py)."
        )

    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    if "backbone_state_dict" not in ckpt or "meta" not in ckpt:
        raise AssertionError(
            f"Malformed SSL checkpoint {ckpt_path}: expected keys "
            f"'backbone_state_dict' and 'meta'."
        )
    meta: dict[str, Any] = ckpt["meta"]

    if require_gate_passed and not bool(meta.get("gate_passed", False)):
        raise RuntimeError(
            f"SSL checkpoint {ckpt_path} has gate_passed != True. The linear-probe "
            f"gate (brief §8) must pass before this init enters Experiment 1. "
            f"Run scripts/run_ssl_probe.py and confirm acceptance, or pass "
            f"require_gate_passed=False for a dry run."
        )

    stem_ch = _stem_in_channels(model)
    assert stem_ch == 4, (
        f"Target model stem has in_channels={stem_ch}, expected 4 (RGB + FOV "
        f"mask). SSL weights are 4-channel-stem (Configs B/D) only."
    )

    result = model.load_state_dict(ckpt["backbone_state_dict"], strict=False)

    if strict_trunk:
        head_prefixes = _head_key_prefixes(model)
        unexpected = list(result.unexpected_keys)
        non_head_missing = [
            k for k in result.missing_keys
            if not any(k.startswith(p) for p in head_prefixes)
        ]
        assert not unexpected, (
            f"Unexpected keys when loading SSL trunk into {type(model).__name__}: "
            f"{unexpected[:10]}"
        )
        assert not non_head_missing, (
            f"Missing non-head keys when loading SSL trunk (trunk mismatch): "
            f"{non_head_missing[:10]}"
        )

    return meta
