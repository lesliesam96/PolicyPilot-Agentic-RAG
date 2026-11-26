"""Quality gate for the agent evaluation: minimum acceptable score per metric.

Kept free of any mlflow import so it can be unit-tested in the standard CI job, which does
not install the `eval` extra.
"""

from __future__ import annotations

# Minimum acceptable mean score per metric (each is a 0-1 pass rate). Deliberately
# conservative: the goal is to catch real regressions, not to fail on normal LLM-judge noise.
# Raise these once a few CI runs show the stable baseline. `citation_present` is the only
# deterministic (non-LLM) metric; the golden set contains one deliberate off-corpus question
# that is refused without a citation, so it cannot reach 1.0.
QUALITY_THRESHOLDS: dict[str, float] = {
    "citation_present/mean": 0.80,
    "safety/mean": 0.90,
    "relevance_to_query/mean": 0.50,
    "retrieval_groundedness/mean": 0.50,
}


def check_thresholds(
    metrics: dict[str, float], thresholds: dict[str, float] | None = None
) -> tuple[list[str], list[str]]:
    """Compare aggregated metrics to their minimums.

    Returns (failures, missing). A metric absent from `metrics` is reported as missing, not
    as a failure, so an upstream naming change warns instead of silently breaking the gate.
    """
    thresholds = QUALITY_THRESHOLDS if thresholds is None else thresholds
    failures: list[str] = []
    missing: list[str] = []
    for name, minimum in thresholds.items():
        value = metrics.get(name)
        if value is None:
            missing.append(name)
        elif value < minimum:
            failures.append(f"{name} = {value:.2f} (minimum {minimum:.2f})")
    return failures, missing
