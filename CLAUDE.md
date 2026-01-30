# fully-typed-reprorusted-python-cli - Development Guidelines

## Project Overview

Fully-typed Python-to-Rust transpilation corpus and CITL (Compiler-in-the-Loop)
training framework for the depyler transpiler. This is the strict-typing retrofit
of reprorusted-python-cli.

## Critical Rules

### Package Management
- **ONLY use `uv`** - No pip, conda, or poetry
- All commands use `uv run` prefix
- Dependencies managed in `pyproject.toml`

### Quality Standards
- **95% minimum test coverage** (branch) - Enforced via pytest
- **Zero ruff violations** - `make lint` must pass (including D rules)
- **Zero ty type errors** - `make typecheck` must pass
- **100% docstring coverage** for public APIs
- **Property-based testing** via Hypothesis for all pure functions

### Typing Rules
- `from __future__ import annotations` in every `.py` file
- Full type annotations on all function parameters and return types
- Zero `# type: ignore` comments (fix the code instead)
- Use `TYPE_CHECKING` guard for import-only types
- Prefer `X | None` over `Optional[X]`
- Use `TypeAlias` for complex types

### Docstring Rules
- Google style convention
- Every public function has a docstring
- Minimum 3 doctests per function: happy path, edge case, error case
- Use `+IGNORE_EXCEPTION_DETAIL` for error doctests

### TDD Workflow
1. Write failing test (RED)
2. Implement minimum code (GREEN)
3. Refactor while green (REFACTOR)

### Commit Format
```
feat|fix|docs|refactor|test: message (Refs GH-XXX)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Commands

```bash
make setup              # Install dependencies
make check              # All 5 gates (lint + format + ty + security + coverage)
make lint               # Ruff linter
make format             # Format check
make typecheck          # ty type checker
make test               # Full test suite with coverage
make test-fast          # Quick unit tests, no coverage
make security           # Bandit security scan
make mutation           # Mutation testing

# Corpus pipeline
make corpus-pipeline    # Full pipeline (label -> augment -> report -> analyze)
make corpus-e2e-rate    # Measure single-shot compile rate
make corpus-dashboard   # Unified status view
make corpus-export      # Export corpus to Parquet
```

## Module Structure

All pipeline scripts live in `src/reprorusted_python_cli/` as importable
modules with `if __name__ == "__main__":` blocks for CLI invocation.

```python
"""Module docstring with overview.

Usage:
    python -m reprorusted_python_cli.module_name [OPTIONS]

Examples:
    >>> from reprorusted_python_cli.module_name import func
    >>> func(...)
    ...
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def func(param: str) -> ReturnType:
    """One-line summary.

    Args:
        param: Description.

    Returns:
        Description.

    Raises:
        ValueError: When param is invalid.

    Examples:
        >>> func("test")
        'expected'
    """
    ...
```
