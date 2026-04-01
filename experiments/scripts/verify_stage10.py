#!/usr/bin/env python3
"""Verify Stage 10: statistical tests + automated report generation.

Test 1 — McNemar test on hand-crafted predictions.
Test 2 — Bootstrap CI for all primary metrics.
Test 3 — Holm-Bonferroni multiple comparison correction.
Test 4 — DeLong test on synthetic data.
Test 5 — generate_report.py (most sections PENDING — pipeline check only).
"""

import subprocess
import sys
from pathlib import Path

# Ensure project root is on sys.path when running as a script
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np

from src.evaluation import (
    bootstrap_ci,
    bootstrap_ci_all_primary,
    delong_test,
    holm_bonferroni_correction,
    mcnemar_test,
    compute_mixed_effects_summary,
)

SEP = "=" * 65

# ── Test 1: McNemar test ──────────────────────────────────────────────────────
print(SEP)
print("Test 1: McNemar test")
print(SEP)

y_true  = np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 1])
y_pred_a = np.array([0, 0, 1, 0, 0, 1, 1, 1, 0, 1])  # model A
y_pred_b = np.array([0, 1, 1, 1, 0, 0, 1, 1, 0, 1])  # model B

result = mcnemar_test(y_true, y_pred_a, y_pred_b)
print(f"  b (A✓ B✗) = {result['b']}")
print(f"  c (A✗ B✓) = {result['c']}")
print(f"  statistic = {result['statistic']}")
print(f"  p_value   = {result['p_value']}")
print(f"  significant (α=0.05) = {result['significant']}")
print(f"  test_type = {result['test_type']}")

assert "p_value" in result
assert "significant" in result
assert 0.0 <= result["p_value"] <= 1.0
assert result["b"] >= 0 and result["c"] >= 0
print("  Assertions passed.")

# ── Test 2: Bootstrap CI ──────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 2: Bootstrap CI for all primary metrics")
print(SEP)

rng = np.random.default_rng(42)
N = 100
y_true_b  = rng.integers(0, 5, size=N)
y_pred_b_ = y_true_b.copy()
noise_idx = rng.choice(N, size=N // 5, replace=False)
y_pred_b_[noise_idx] = rng.integers(0, 5, size=len(noise_idx))
y_prob_b  = rng.dirichlet(np.ones(5), size=N).astype(np.float32)

ci_all = bootstrap_ci_all_primary(y_true_b, y_pred_b_, y_prob_b, n_iterations=200)
print(f"\n  {'Metric':<28} {'Mean':>8} {'CI lower':>10} {'CI upper':>10} {'Std':>8}")
print(f"  {'-'*65}")
for metric, ci in ci_all.items():
    print(f"  {metric:<28} {ci['mean']:>8.4f} {ci['ci_lower']:>10.4f} "
          f"{ci['ci_upper']:>10.4f} {ci['std']:>8.4f}")

# Structural assertions
for metric, ci in ci_all.items():
    assert "mean" in ci
    assert "ci_lower" in ci
    assert "ci_upper" in ci
    assert "std" in ci
    if not (ci["mean"] != ci["mean"]):  # not NaN
        assert ci["ci_lower"] <= ci["mean"] <= ci["ci_upper"], \
            f"{metric}: CI does not bracket mean"

# Single metric bootstrap CI
single = bootstrap_ci(
    y_true_b, y_pred_b_, y_prob_b,
    n_iterations=200,
)
assert 0.0 <= single["mean"] <= 1.0
print(f"\n  Default (weighted F1) single CI: "
      f"mean={single['mean']:.4f} [{single['ci_lower']:.4f}, {single['ci_upper']:.4f}]")
print("  Bootstrap assertions passed.")

# ── Test 3: Holm-Bonferroni ───────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 3: Holm-Bonferroni multiple comparison correction")
print(SEP)

p_values = [0.01, 0.04, 0.03, 0.005, 0.08]
corrected = holm_bonferroni_correction(p_values, alpha=0.05)
print(f"\n  {'Rank':>5} {'Original p':>12} {'Adjusted p':>12} {'Significant':>12}")
print(f"  {'-'*50}")
for r in corrected:
    print(f"  {r['rank']:>5} {r['original_p']:>12.6f} {r['adjusted_p']:>12.6f} "
          f"{'YES' if r['significant'] else 'no':>12}")

# Verify: corrected p-values are >= original p-values
for i, (orig, corr) in enumerate(zip(p_values, corrected)):
    assert corr["adjusted_p"] >= corr["original_p"] - 1e-9, \
        f"adjusted_p < original_p at index {i}"

# The smallest p (0.005) should still be significant after correction
smallest_orig = min(range(len(p_values)), key=lambda i: p_values[i])
assert corrected[smallest_orig]["significant"], \
    "Smallest p-value should remain significant after Holm-Bonferroni"
print("  Holm-Bonferroni assertions passed.")

# ── Mixed-effects summary ──────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 3b: Mixed-effects fold summary")
print(SEP)

fold_metrics = [
    {"val_weighted_f1": 0.72},
    {"val_weighted_f1": 0.75},
    {"val_weighted_f1": 0.70},
    {"val_weighted_f1": 0.73},
    {"val_weighted_f1": 0.71},
]
me_summ = compute_mixed_effects_summary(fold_metrics)
print(f"  Grand mean F1:       {me_summ['grand_mean']:.4f}")
print(f"  Between-fold std:    {me_summ['between_fold_std']:.4f}")
print(f"  n_folds:             {me_summ['n_folds']}")
assert abs(me_summ["grand_mean"] - 0.722) < 0.001
assert me_summ["n_folds"] == 5
print("  Mixed-effects assertions passed.")

# ── Test 4: DeLong test ───────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 4: DeLong ROC-AUC comparison test")
print(SEP)

rng2 = np.random.default_rng(99)
N2 = 200
y_true_d = rng2.integers(0, 5, size=N2)
# Model A: good separation for referable (grades 2-4)
y_prob_a = rng2.dirichlet(np.ones(5), size=N2).astype(np.float64)
y_prob_b2 = rng2.dirichlet(np.ones(5), size=N2).astype(np.float64)

dl = delong_test(y_true_d, y_prob_a, y_prob_b2)
print(f"  AUC_a = {dl['auc_a']:.4f}")
print(f"  AUC_b = {dl['auc_b']:.4f}")
print(f"  Δ AUC = {dl['auc_diff']:.4f}")
print(f"  z     = {dl['z_statistic']}")
print(f"  p     = {dl['p_value']}")
print(f"  significant (α=0.05) = {dl['significant']}")

assert 0.0 <= dl["auc_a"] <= 1.0
assert 0.0 <= dl["auc_b"] <= 1.0
assert 0.0 <= dl["p_value"] <= 1.0
# Test with identical predictions — should give p=1.0 (or NaN z)
dl_same = delong_test(y_true_d, y_prob_a, y_prob_a)
assert dl_same["auc_diff"] == 0.0 or abs(dl_same["auc_diff"]) < 1e-10
print("  DeLong assertions passed.")

# ── Test 5: Report generation ─────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 5: Report generation (most experiments PENDING)")
print(SEP)

report_path = Path("outputs/final_report.md")
result = subprocess.run(
    [sys.executable, "scripts/generate_report.py",
     "--output", str(report_path),
     "--outputs-root", "outputs"],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print(f"  STDERR: {result.stderr}")
    sys.exit(1)
print(f"  {result.stdout.strip()}")

assert report_path.exists(), f"Report not created at {report_path}"

content = report_path.read_text(encoding="utf-8")
lines   = content.splitlines()

# Check key sections present
required_phrases = [
    "DR-Classifier",
    "Hypothesis Outcome Summary",
    "Experiment 1",
    "Experiment 2",
    "Experiment 3",
    "Experiment 4",
    "Experiment 5",
    "Experiment 6",
    "Primary Claim Strength Assessment",
    "Statistical Validation Framework",
    "NC-14",
    "IT-1",
]
for phrase in required_phrases:
    assert phrase in content, f"Missing phrase in report: {phrase!r}"

print(f"\n  Report: {len(lines)} lines | {len(content)} chars")
print(f"\n  First 50 lines:")
print("  " + "\n  ".join(lines[:50]))

print(f"\n  All required sections verified.")
print(f"\n{SEP}")
print("All Stage 10 assertions passed.")
