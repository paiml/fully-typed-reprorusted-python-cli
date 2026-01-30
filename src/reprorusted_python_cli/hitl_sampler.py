"""HITL Sampler - Human-in-the-Loop review sampling.

Selects stratified samples from the corpus for human review,
prioritizing high-uncertainty and high-risk categories.

Usage:
    python -m reprorusted_python_cli.hitl_sampler --sample-pct 5
    python -m reprorusted_python_cli.hitl_sampler --report

Examples:
    >>> from reprorusted_python_cli.hitl_sampler import sample_for_review
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def sample_for_review(
    sample_pct: float = 5.0,
    input_path: str | Path | None = None,
) -> list[dict[str, str | float]]:
    """Select stratified samples for human review.

    Args:
        sample_pct: Percentage of corpus to sample.
        input_path: Path to labeled corpus parquet file.

    Returns:
        List of sampled examples with metadata.
    """
    return []


def generate_report(
    input_path: str | Path | None = None,
) -> dict[str, object]:
    """Generate a HITL review report.

    Args:
        input_path: Path to labeled corpus parquet file.

    Returns:
        Dictionary with review statistics and recommendations.
    """
    return {}


def main() -> None:
    """CLI entry point for hitl_sampler."""
    import argparse

    parser = argparse.ArgumentParser(
        description="HITL Sampler - Human-in-the-Loop review sampling"
    )
    parser.add_argument("--sample-pct", type=float, default=5.0)
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--input", "-i", help="Input labeled parquet file")
    args = parser.parse_args()

    if args.report:
        generate_report(args.input)
    else:
        sample_for_review(args.sample_pct, args.input)


if __name__ == "__main__":
    main()
