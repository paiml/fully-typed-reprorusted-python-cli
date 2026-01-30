# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Fully-typed retrofit of reprorusted-python-cli
- All pipeline scripts moved to `src/reprorusted_python_cli/` as importable modules
- `py.typed` PEP 561 marker
- `from __future__ import annotations` in every file
- Google-style docstrings with doctests on all public APIs
- 5-gate Jidoka CI pipeline (lint + format + ty + security + test)
- Docker reproducible build environment
- Dev container configuration

### Changed
- Line length from 100 to 88 (matches hf-ground-truth-corpus)
- Ruff rules expanded: added N, SIM, RUF, D
- Coverage enforced at 95% with branch coverage
- All sibling imports replaced with package-relative imports
