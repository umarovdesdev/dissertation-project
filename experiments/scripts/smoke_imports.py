"""Smoke test: compile + import every module to catch syntax/import errors.

Run: python scripts/smoke_imports.py
Exits non-zero if any module fails to compile or import.
"""

from __future__ import annotations

import importlib
import sys
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "src"
sys.path.insert(0, str(REPO))

EXP_MODULES = [
    "src.experiments.exp1_factorial",
    "src.experiments.exp2_ablation",
    "src.experiments.exp3_transferability",
    "src.experiments.exp4_explainability",
    "src.experiments.exp5_clinical_degradation",
    "src.experiments.exp6_device_shift",
    "src.experiments.exp7_clinical",
]


def main() -> int:
    # 1) Import every src.* module by walking the package tree.
    all_mods: list[str] = []
    for p in sorted(SRC.rglob("*.py")):
        if p.name == "__init__.py":
            rel = p.parent.relative_to(REPO)
        else:
            rel = p.relative_to(REPO).with_suffix("")
        mod = ".".join(rel.parts)
        all_mods.append(mod)

    failures: list[tuple[str, str]] = []
    ok = 0
    for mod in all_mods:
        try:
            importlib.import_module(mod)
            ok += 1
        except Exception:  # noqa: BLE001
            failures.append((mod, traceback.format_exc()))

    print(f"[imports] {ok}/{len(all_mods)} src modules imported OK")

    # 2) Confirm each experiment exposes a callable run().
    for mod in EXP_MODULES:
        try:
            m = importlib.import_module(mod)
            assert callable(getattr(m, "run")), "missing run()"
            print(f"[run-entry] {mod:48s} OK (run() present)")
        except Exception:  # noqa: BLE001
            failures.append((mod + ".run", traceback.format_exc()))

    if failures:
        print(f"\n===== {len(failures)} FAILURES =====")
        for name, tb in failures:
            print(f"\n----- {name} -----")
            print(tb)
        return 1
    print("\nALL IMPORTS + RUN ENTRYPOINTS OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
