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
