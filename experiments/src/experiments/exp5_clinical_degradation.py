"""Experiment 5: Clinical Degradation Resistance (H-7).

Train on EyePACS. Evaluate on IDRiD and Messidor-2.
Compute delta = F1_EyePACS_val - F1_external for baseline vs full pipeline.
H-7: Degradation is statistically smaller with the pipeline vs baseline.
"""

from typing import Any


def run(config: dict[str, Any], *, fold: int | None = None,
        resume: bool = False, _configs_to_run: list[str] | None = None) -> None:
    """Run Experiment 5: Clinical Degradation Resistance."""
    raise NotImplementedError(
        "Experiment 5 (clinical degradation) not yet implemented. "
        "Train on EyePACS, test on IDRiD + Messidor-2, compute delta."
    )
