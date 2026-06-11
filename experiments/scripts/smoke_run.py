"""Smoke runner: launch every experiment on a tiny subset / 1 epoch.

Goal is NOT to produce valid results — it is to confirm each experiment's
execution path runs without code errors. Each experiment is isolated in its own
try/except so one failure does not stop the rest. A concise traceback tail is
printed for any failure.

Run: python scripts/smoke_run.py
"""

from __future__ import annotations

import sys
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.utils.config import load_config, get_experiment_config  # noqa: E402
from src.utils.seed import set_seed  # noqa: E402


def smoke_config() -> dict:
    """Load default config and shrink it for a fast smoke run."""
    cfg = load_config(str(REPO / "configs" / "default.yaml"))
    cfg["training"]["max_epochs"] = 1
    cfg["training"]["batch_size"] = 8
    cfg["training"]["num_workers"] = 0
    cfg.setdefault("cross_validation", {})
    cfg["cross_validation"]["stratified"] = False  # tiny subset → skip per-class min
    # point output at a throwaway dir so we don't clobber real artifacts
    cfg["paths"]["output_dir"] = "outputs/_smoke"
    # disable any precomputed cache so the raw path is exercised
    cfg["paths"].pop("cache_dir", None)
    cfg.setdefault("subset", {})["enabled"] = False
    # Config ships Windows paths (E:/datasets/...). Under WSL the same drive is
    # mounted at /mnt/e — translate so the smoke run finds the data.
    for k, v in list(cfg["paths"].items()):
        if isinstance(v, str) and v[:3].lower() == "e:/":
            cfg["paths"][k] = "/mnt/e/" + v[3:]
    return cfg


def main() -> int:
    base = smoke_config()
    set_seed(42)

    def merged(exp: str) -> dict:
        return get_experiment_config(base, exp)

    # (label, thunk). Ordered so exp1 produces checkpoints for downstream exps.
    import importlib
    e1 = importlib.import_module("src.experiments.exp1_factorial")
    e2 = importlib.import_module("src.experiments.exp2_ablation")
    e3 = importlib.import_module("src.experiments.exp3_transferability")
    e4 = importlib.import_module("src.experiments.exp4_explainability")
    e5 = importlib.import_module("src.experiments.exp5_clinical_degradation")
    e6 = importlib.import_module("src.experiments.exp6_device_shift")
    e7 = importlib.import_module("src.experiments.exp7_clinical")

    jobs: list[tuple[str, callable]] = [
        ("exp1 (A,B,C,D fold0)", lambda: e1.run(
            merged("exp1"), fold=0, _subset_size=200,
            _configs_to_run=["A", "B", "C", "D"])),
        ("exp2 (baseline+full)", lambda: e2.run(
            merged("exp2"), fold=0, _subset_size=120,
            _levels_to_run=["baseline", "full"],
            _clahe_values=[2.0], _quality_n_samples=6)),
        ("exp3 (EyePACS→APTOS)", lambda: e3.run(
            merged("exp3"), fold=0, _subset_size=80)),
        ("exp4 (Grad-CAM IDRiD)", lambda: e4.run(
            merged("exp4"), fold=0, _subset_size=40)),
        ("exp5 (degradation)", lambda: e5.run(
            merged("exp5"), fold=0, _subset_size=80)),
        ("exp6 (device shift)", lambda: e6.run(
            merged("exp6"), fold=0, _subset_size=80)),
        ("exp7 (IDRiD→Clinical)", lambda: e7.run(
            merged("exp7"), fold=0, _subset_size=80)),
    ]

    results: list[tuple[str, str, float, str]] = []
    for label, thunk in jobs:
        print("\n" + "#" * 75)
        print(f"#  SMOKE: {label}")
        print("#" * 75)
        t0 = time.time()
        try:
            thunk()
            dt = time.time() - t0
            results.append((label, "PASS", dt, ""))
            print(f"\n>>> {label}: PASS ({dt:.0f}s)")
        except Exception as exc:  # noqa: BLE001
            dt = time.time() - t0
            tb = traceback.format_exc()
            # keep last frames — most relevant to the failure point
            tail = "\n".join(tb.strip().splitlines()[-12:])
            results.append((label, "FAIL", dt, f"{type(exc).__name__}: {exc}"))
            print(f"\n>>> {label}: FAIL ({dt:.0f}s)\n{tail}")

    print("\n" + "=" * 75)
    print("SMOKE SUMMARY")
    print("=" * 75)
    for label, status, dt, err in results:
        line = f"  {status:4s}  {label:24s}  {dt:5.0f}s"
        if err:
            line += f"   {err}"
        print(line)
    n_fail = sum(1 for _, s, _, _ in results if s == "FAIL")
    print(f"\n{len(results) - n_fail}/{len(results)} experiments launched cleanly.")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
