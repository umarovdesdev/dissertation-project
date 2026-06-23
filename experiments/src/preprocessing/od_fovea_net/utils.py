"""Shared helpers: YAML config loading and device resolution."""

from __future__ import annotations

import pathlib

import yaml


def load_config(path: pathlib.Path | str) -> dict:
    """Load a YAML config file into a dict.

    Args:
        path: Path to the YAML config.

    Returns:
        Parsed config dictionary.
    """
    path = pathlib.Path(path)
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def resolve_device(device: str = "auto") -> str:
    """Resolve a device string to ``"cpu"`` or ``"cuda"``.

    Args:
        device: ``"auto"``, ``"cpu"``, or ``"cuda"``.

    Returns:
        ``"cuda"`` if requested/available, else ``"cpu"``.
    """
    if device == "cpu":
        return "cpu"
    try:
        import torch
        if device == "cuda":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"
