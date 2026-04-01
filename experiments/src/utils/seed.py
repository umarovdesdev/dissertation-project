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
