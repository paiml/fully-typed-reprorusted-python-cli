.PHONY: setup lint format format-fix typecheck test test-fast test-unit test-doctest coverage coverage-check security check mutation docs export clean

# === Setup ===
setup:
	uv sync

# === Quality Gates ===
lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format --check src/ tests/

format-fix:
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

typecheck:
	uv run ty check src/

security:
	uv run bandit -r src/ -ll

check: lint format typecheck security coverage-check
	@echo "All quality gates passed."

# === Testing ===
test:
	uv run pytest

test-fast:
	uv run pytest tests/unit/ -x -q --no-cov

test-unit:
	uv run pytest tests/unit/ -v

test-doctest:
	uv run pytest --doctest-modules src/

coverage:
	uv run pytest --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

coverage-check:
	uv run pytest --cov-fail-under=95

# === Mutation Testing ===
mutation:
	uv run mutmut run --paths-to-mutate=src/reprorusted_python_cli/

# === Documentation ===
docs:
	uv run pdoc -o docs/api src/reprorusted_python_cli
	@echo "API documentation generated in docs/api/"

# === Corpus Pipeline ===
corpus-label:
	uv run python -m reprorusted_python_cli.label_corpus data/depyler_citl_corpus_v2.parquet \
		--output data/labeled_corpus.parquet

corpus-augment:
	uv run python -m reprorusted_python_cli.augment_corpus data/labeled_corpus.parquet \
		--output data/augmented_corpus.parquet --multiplier 2

corpus-report:
	uv run python -m reprorusted_python_cli.corpus_quality_report data/labeled_corpus.parquet \
		--output reports/quality_report.json

corpus-analyze:
	uv run python -m reprorusted_python_cli.zero_success_analyzer data/labeled_corpus.parquet \
		--output reports/zero_success_analysis.json

corpus-pipeline: corpus-label corpus-augment corpus-report corpus-analyze
	@echo "Full corpus pipeline complete."

corpus-golden-analyze:
	uv run python -m reprorusted_python_cli.golden_traces_analyzer --json

corpus-golden-export:
	uv run python -m reprorusted_python_cli.golden_traces_analyzer \
		--output data/golden_traces.json

corpus-clippy-check:
	uv run python -m reprorusted_python_cli.clippy_gate --soft -v

corpus-clippy-strict:
	uv run python -m reprorusted_python_cli.clippy_gate --strict

corpus-hitl-sample:
	uv run python -m reprorusted_python_cli.hitl_sampler --sample-pct 5

corpus-hitl-report:
	uv run python -m reprorusted_python_cli.hitl_sampler --report

corpus-e2e-rate:
	uv run python -m reprorusted_python_cli.measure_compile_rate -v

corpus-category-diff:
	uv run python -m reprorusted_python_cli.category_diff data/baseline_corpus.parquet data/labeled_corpus.parquet

corpus-export:
	uv run python -m reprorusted_python_cli.export_hf_corpus

corpus-dashboard:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "CORPUS DASHBOARD"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	uv run python -m reprorusted_python_cli.measure_compile_rate
	@echo ""
	uv run python -m reprorusted_python_cli.check_test_lib_crates

# === Clean ===
clean:
	rm -rf .pytest_cache .ruff_cache .hypothesis htmlcov .coverage
	rm -rf __pycache__ src/**/__pycache__ tests/**/__pycache__
	rm -rf dist/ build/ *.egg-info
