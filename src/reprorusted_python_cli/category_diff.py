"""Category Diff Tracking.

Compares two corpus snapshots and reports per-category changes
in compile rates, pattern counts, and quality metrics.

Usage:
    python -m reprorusted_python_cli.category_diff baseline.parquet current.parquet

Examples:
    >>> from reprorusted_python_cli.category_diff import compute_category_diff
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def compute_category_diff(
    baseline_path: str | Path,
    current_path: str | Path,
    output_path: str | Path | None = None,
) -> dict[str, dict[str, float]]:
    """Compute per-category diffs between two corpus snapshots.

    Args:
        baseline_path: Path to baseline corpus parquet file.
        current_path: Path to current corpus parquet file.
        output_path: Optional path to output JSON diff file.

    Returns:
        Dictionary mapping category names to their metric changes.
    """
    return {}


def main() -> None:
    """CLI entry point for category_diff."""
    import argparse

    parser = argparse.ArgumentParser(description="Category Diff Tracking")
    parser.add_argument("baseline", help="Baseline corpus parquet file")
    parser.add_argument("current", help="Current corpus parquet file")
    parser.add_argument("--output", "-o", help="Output JSON diff file")
    args = parser.parse_args()

    compute_category_diff(args.baseline, args.current, args.output)


if __name__ == "__main__":
    main()
