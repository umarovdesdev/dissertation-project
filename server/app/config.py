"""Server settings, sourced from environment variables with sane defaults.

No hardcoded absolute paths: the checkpoint and norm-stats locations default to
``server/checkpoints/`` relative to this file and can be overridden via env.
"""

from __future__ import annotations

import os
from pathlib import Path

_SERVER_ROOT = Path(__file__).resolve().parents[1]  # .../server


class Settings:
    """Runtime configuration read once at import time.

    Attributes:
        checkpoint_path: Path to the Config D checkpoint (``best_model.pt``).
        norm_stats_path: Path to ``eyepacs_norm_stats.json`` (dataset-specific
            Stage 7 mean/std). Must match the stats used at training time.
        model_name: Backbone identifier for the model factory.
        in_channels: Input channel count (4 = RGB + FOV mask for full V5).
        num_classes: DR grade count (0–4).
        checkpoint_id: Human-readable provenance string for /api/health.
        device: ``"cuda"``, ``"cpu"``, or ``"auto"``.
        cors_origins: Allowed CORS origins (comma-separated env → list).
        host/port: uvicorn bind address.
    """

    def __init__(self) -> None:
        self.checkpoint_path: Path = Path(
            os.getenv("CHECKPOINT_PATH", str(_SERVER_ROOT / "checkpoints" / "config_d_fold0.pt"))
        )
        self.norm_stats_path: Path = Path(
            os.getenv("NORM_STATS_PATH", str(_SERVER_ROOT / "checkpoints" / "eyepacs_norm_stats.json"))
        )
        self.model_name: str = os.getenv("MODEL_NAME", "efficientnet_b3")
        self.in_channels: int = int(os.getenv("IN_CHANNELS", "4"))
        self.num_classes: int = int(os.getenv("NUM_CLASSES", "5"))
        self.checkpoint_id: str = os.getenv("MODEL_CHECKPOINT_ID", "config-d-fold0")
        self.device: str = os.getenv("DEVICE", "auto")
        self.preset: str = os.getenv("PREPROCESSING_PRESET", "efficientnet")

        # Access gate + provenance (TASK-Demo §C.2/§E.4).
        self.demo_password: str = os.getenv("DEMO_PASSWORD", "")
        self.demo_version: str = os.getenv("DEMO_VERSION", "")  # falls back to __version__
        self.git_sha: str = os.getenv("GIT_SHA", "")            # best-effort, see resolve_git_sha

        origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        self.cors_origins: list[str] = [o.strip() for o in origins.split(",") if o.strip()]

        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))

    def resolve_device(self) -> str:
        """Resolve ``"auto"`` to ``"cuda"`` when available, else ``"cpu"``."""
        if self.device != "auto":
            return self.device
        try:
            import torch
            return "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            return "cpu"

    def resolve_version(self) -> str:
        """Return the configured demo version, or the bundled ``__version__``."""
        if self.demo_version:
            return self.demo_version
        try:
            from server.__version__ import __version__
            return __version__
        except Exception:
            return "0.0.0"

    def resolve_git_sha(self) -> str:
        """Best-effort short git SHA: env override, else ``git rev-parse``, else ''."""
        if self.git_sha:
            return self.git_sha
        try:
            import subprocess
            sha = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=str(_SERVER_ROOT.parent), capture_output=True, text=True, timeout=2,
            )
            return sha.stdout.strip() if sha.returncode == 0 else ""
        except Exception:
            return ""


settings = Settings()
