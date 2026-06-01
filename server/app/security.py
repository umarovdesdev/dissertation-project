"""Single shared-password gate (TASK-Demo §C.2).

Adequate for a ~15-person academic beta. If ``DEMO_PASSWORD`` is unset/empty the
gate is disabled (open) — convenient for local dev; a warning is logged once.
"""

from __future__ import annotations

from .config import settings

_warned = False


def gate_disabled() -> bool:
    """Return True when no password is configured (gate open)."""
    global _warned
    if not settings.demo_password:
        if not _warned:
            print("[WARN] DEMO_PASSWORD unset — endpoints are OPEN (no password gate).")
            _warned = True
        return True
    return False


def check_password(password: str | None) -> bool:
    """Validate a supplied password against ``DEMO_PASSWORD``.

    Args:
        password: Password from the request (form field or query param).

    Returns:
        True if access is allowed (gate disabled, or password matches).
    """
    if gate_disabled():
        return True
    return bool(password) and password == settings.demo_password
