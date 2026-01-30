# fully-typed-reprorusted-python-cli

Fully-typed Python-to-Rust transpilation corpus and CITL (Compiler-in-the-Loop)
training framework for the [depyler](https://github.com/paiml/depyler) transpiler.

This is a strict-typing retrofit of
[reprorusted-python-cli](https://github.com/paiml/reprorusted-python-cli),
with every Python file passing `ty` with zero errors.

## Quality Standards

- 95%+ test coverage (branch)
- Zero `ty` type errors
- Zero `ruff` lint violations (including docstring rules)
- Zero `bandit` security findings
- Google-style docstrings with 3+ doctests per function
- All pipeline scripts fully typed and importable

## Pipeline Modules

| Module | Purpose |
|---|---|
| `weak_supervision` | Tarantula-weighted labeling functions |
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
| `synthetic_augmenter` | Mutation-based data augmentation |
| `generate_insights` | Tarantula fault localization insights |
| `verify_qa_checklist` | Dataset QA verification |

## Quick Start

```bash
make setup            # Install dependencies
make check            # Run all quality gates
make corpus-pipeline  # Run full corpus pipeline
make corpus-dashboard # View corpus status
```

## License

Apache-2.0
