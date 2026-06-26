"""Configuration loading utilities."""

from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file.

    Args:
        path: Path to the YAML config file.

    Returns:
        Parsed configuration as a nested dict.
    """
    with open(Path(path), "r") as f:
        return yaml.safe_load(f)


def deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge ``overlay`` onto a deep copy of ``base``.

    Nested dicts are merged key-by-key; non-dict values in ``overlay`` replace
    those in ``base``. Used to layer a dedicated overlay (e.g.
    ``configs/ssl_pretrain.yaml``) on top of ``configs/default.yaml``.

    Args:
        base: Base configuration dict.
        overlay: Overlay dict whose values take precedence.

    Returns:
        New merged dict (inputs are not mutated).
    """
    import copy

    result = copy.deepcopy(base)
    for key, val in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = copy.deepcopy(val)
    return result


def load_configs(*paths: str | Path) -> dict[str, Any]:
    """Load and deep-merge multiple YAML configs left-to-right.

    Later paths override earlier ones via :func:`deep_merge`. A single path
    behaves like :func:`load_config`.

    Args:
        *paths: One or more YAML config file paths.

    Returns:
        The merged configuration dict.

    Raises:
        ValueError: If no paths are given.
    """
    if not paths:
        raise ValueError("load_configs requires at least one path.")
    merged: dict[str, Any] = {}
    for p in paths:
        merged = deep_merge(merged, load_config(p))
    return merged


def get_experiment_config(config: dict[str, Any], exp_name: str) -> dict[str, Any]:
    """Merge global config with experiment-specific overrides.

    Args:
        config: Full config dict loaded from default.yaml.
        exp_name: Experiment key, e.g. "exp1".

    Returns:
        Merged dict: global config updated with experiment-specific values.
    """
    import copy

    merged = copy.deepcopy(config)
    exp_cfg = config.get("experiments", {}).get(exp_name)
    if exp_cfg is None:
        raise KeyError(f"Experiment '{exp_name}' not found in config['experiments'].")
    merged["experiment"] = exp_cfg
    return merged
