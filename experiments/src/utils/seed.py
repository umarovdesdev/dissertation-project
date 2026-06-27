"""Reproducibility seed utilities."""

import os
import random

import numpy as np
import torch


def set_seed(seed: int = 42) -> None:
    """Set all relevant random seeds for full reproducibility.

    Configures Python random, NumPy, PyTorch (CPU + CUDA), and
    cuDNN determinism flags. Also sets PYTHONHASHSEED.

    Args:
        seed: Integer seed value. Defaults to 42.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def capture_rng_state() -> dict:
    """Snapshot the global RNG state for a resumable run.

    Captures Python ``random``, NumPy, and PyTorch CPU (plus per-device CUDA)
    generator states so a checkpointed run can continue with the same random
    stream. Intended to be persisted alongside the SSL resume checkpoint.

    Returns:
        A dict consumable by :func:`restore_rng_state`. The ``cuda`` key is
        present only when CUDA is available.
    """
    state: dict = {
        "python": random.getstate(),
        "numpy": np.random.get_state(),
        "torch": torch.get_rng_state(),
    }
    if torch.cuda.is_available():
        state["cuda"] = torch.cuda.get_rng_state_all()
    return state


def restore_rng_state(state: dict | None) -> None:
    """Restore a global RNG snapshot produced by :func:`capture_rng_state`.

    Args:
        state: A dict from :func:`capture_rng_state`, or ``None`` (no-op). CUDA
            state is restored only when CUDA is available; a snapshot taken on a
            different device count is skipped rather than raising.
    """
    if not state:
        return
    if "python" in state:
        random.setstate(state["python"])
    if "numpy" in state:
        np.random.set_state(state["numpy"])
    if "torch" in state:
        torch.set_rng_state(state["torch"])
    cuda = state.get("cuda")
    if cuda and torch.cuda.is_available() and len(cuda) == torch.cuda.device_count():
        torch.cuda.set_rng_state_all(cuda)
