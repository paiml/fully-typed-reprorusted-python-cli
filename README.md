# fully-typed-reprorusted-python-cli

[![CI](https://github.com/paiml/fully-typed-reprorusted-python-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/paiml/fully-typed-reprorusted-python-cli/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/paiml/fully-typed-reprorusted-python-cli)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/linter-ruff-purple.svg)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/badge/package-uv-orange.svg)](https://github.com/astral-sh/uv)

**Fully-typed Python-to-Rust transpilation corpus and CITL (Compiler-in-the-Loop)
training framework** for the [depyler](https://github.com/paiml/depyler) transpiler.

This is a strict-typing retrofit of
[reprorusted-python-cli](https://github.com/paiml/reprorusted-python-cli),
with every Python file passing `ty` with zero errors.

## Installation

```bash
# Clone the repository
git clone https://github.com/paiml/fully-typed-reprorusted-python-cli.git
cd fully-typed-reprorusted-python-cli

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
make setup
```

## Usage

```bash
# Run all quality gates (5-gate Jidoka pipeline)
make check

# Run tests with coverage
make test

# Run full corpus pipeline
make corpus-pipeline

# Use weak supervision labeler programmatically
python -c "from reprorusted_python_cli.weak_supervision import WeakSupervisionLabeler; print(WeakSupervisionLabeler())"
```

## Demo

```bash
# Clone and setup
git clone https://github.com/paiml/fully-typed-reprorusted-python-cli.git
cd fully-typed-reprorusted-python-cli
make setup

# Run all 5-gate Jidoka quality pipeline
make check

# Use weak supervision labeler
python -c "
from reprorusted_python_cli.weak_supervision import WeakSupervisionLabeler
labeler = WeakSupervisionLabeler()
result = labeler.label('def greet(name: str) -> str: return f\"Hello, {name}\"')
print(f'Label: {result.final_label}, Confidence: {result.confidence:.2f}')
"
# Output: Label: Label.COMPILABLE, Confidence: 0.85

# Run corpus pipeline
make corpus-pipeline

# View corpus dashboard
make corpus-dashboard
```

## Architecture

```
fully-typed-reprorusted-python-cli/
├── src/reprorusted_python_cli/
│   ├── weak_supervision.py       # Tarantula-weighted labeling functions
│   ├── synthetic_augmenter.py    # Mutation-based data augmentation
│   ├── label_corpus.py           # Apply weak supervision labels
│   ├── augment_corpus.py         # Synthetic data generation
│   ├── corpus_quality_report.py  # Quality metrics and recommendations
│   ├── category_diff.py          # Track category-level changes
│   ├── zero_success_analyzer.py  # Identify blocking patterns
│   ├── golden_traces_analyzer.py # Oracle training pattern extraction
│   ├── clippy_gate.py            # Rust idiomaticity quality gate
│   ├── hitl_sampler.py           # Human-in-the-loop QA sampling
│   ├── measure_compile_rate.py   # Single-shot compile rate tracking
│   ├── export_hf_corpus.py       # HuggingFace dataset export
│   ├── check_test_lib_crates.py  # Validate test file crate types
│   ├── generate_insights.py      # Tarantula fault localization insights
│   └── verify_qa_checklist.py    # Dataset QA verification
└── tests/
    └── unit/                     # 152 tests, 100% coverage
```

## Quality Standards

| Gate | Tool | Requirement |
|------|------|-------------|
| 1 | ruff check | Zero lint violations |
| 2 | ruff format | Consistent formatting |
| 3 | ty | Zero type errors |
| 4 | bandit | Zero security findings |
| 5 | pytest | 95%+ branch coverage |

Additional standards:
- Google-style docstrings with 3+ doctests per function
- All pipeline scripts fully typed and importable as modules
- PEP 561 compliant (`py.typed` marker)

## Pipeline Modules

| Module | Purpose |
|--------|---------|
| `weak_supervision` | Tarantula-weighted labeling functions |
| `synthetic_augmenter` | Mutation-based data augmentation |
| `label_corpus` | Apply weak supervision labels to corpus |
| `augment_corpus` | Synthetic data generation |
| `corpus_quality_report` | Quality metrics and recommendations |
| `category_diff` | Track category-level changes |
| `zero_success_analyzer` | Identify blocking patterns |
| `golden_traces_analyzer` | Oracle training pattern extraction |
| `clippy_gate` | Rust idiomaticity quality gate |
| `hitl_sampler` | Human-in-the-loop QA sampling |
| `measure_compile_rate` | Single-shot compile rate tracking |
| `export_hf_corpus` | HuggingFace dataset export |
| `check_test_lib_crates` | Validate test file crate types |
| `generate_insights` | Tarantula fault localization insights |
| `verify_qa_checklist` | Dataset QA verification |

## Quick Start

```bash
# Install dependencies (requires uv)
make setup

# Run all quality gates
make check

# Run tests only
make test

# Run full corpus pipeline
make corpus-pipeline

# View corpus status dashboard
make corpus-dashboard

# Export to HuggingFace format
make corpus-export
```

## Corpus Pipeline

```bash
# Individual pipeline stages
make corpus-label          # Apply weak supervision labels
make corpus-augment        # Generate synthetic examples
make corpus-report         # Quality report
make corpus-analyze        # Zero-success analysis
make corpus-golden-analyze # Golden trace extraction
make corpus-clippy-check   # Clippy quality gate
make corpus-hitl-sample    # HITL QA sampling
make corpus-e2e-rate       # Compile rate measurement
make corpus-category-diff  # Category diff tracking
```

## CI Pipeline

The 5-gate Jidoka pipeline runs on every push:

1. **Gate 1**: Lint (ruff check)
2. **Gate 2**: Format (ruff format --check)
3. **Gate 3**: Type check (ty)
4. **Gate 4**: Security (bandit)
5. **Gate 5**: Tests + Coverage (pytest, 95% threshold)

Matrix: Ubuntu + macOS × Python 3.11 + 3.12

## CITL Framework

The Compiler-in-the-Loop (CITL) training framework uses:

- **Weak Supervision**: Tarantula fault localization weights for labeling
- **Synthetic Augmentation**: Mutation strategies (async, generator, lambda, walrus)
- **Quality Gates**: Clippy idiomaticity checks
- **Human-in-the-Loop**: Stratified sampling for expert review

## Contributing

1. Fork the repository
2. Create a feature branch
3. Ensure all quality gates pass: `make check`
4. Submit a pull request

## License

Apache-2.0
