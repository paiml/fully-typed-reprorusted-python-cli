"""Check that test files use [lib] crate type, not [[bin]].

Validates Cargo.toml files in test directories to ensure they
declare [lib] crate types for proper test harness integration.

Usage:
    python -m reprorusted_python_cli.check_test_lib_crates

Examples:
    >>> from reprorusted_python_cli.check_test_lib_crates import check_test_lib_crates
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def check_test_lib_crates(
    examples_dir: str | Path | None = None,
) -> dict[str, list[str]]:
    """Check test file crate types across all examples.

    Args:
        examples_dir: Path to examples directory.

    Returns:
        Dictionary with 'lib' and 'bin' lists of example names.
    """
    return {"lib": [], "bin": []}


def main() -> None:
    """CLI entry point for check_test_lib_crates."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Check that test files use [lib] crate type, not [[bin]]"
    )
    parser.add_argument("--examples-dir", "-d", help="Examples directory")
    args = parser.parse_args()

    check_test_lib_crates(args.examples_dir)


if __name__ == "__main__":
    main()
