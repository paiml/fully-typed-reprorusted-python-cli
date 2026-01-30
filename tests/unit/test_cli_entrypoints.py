"""Tests for CLI entry point main() functions.

Each module has a main() function that uses argparse.
We test these by mocking sys.argv.
"""

from __future__ import annotations

from unittest.mock import patch

from reprorusted_python_cli import augment_corpus as augment_mod
from reprorusted_python_cli import category_diff as category_mod
from reprorusted_python_cli import check_test_lib_crates as check_mod
from reprorusted_python_cli import clippy_gate as clippy_mod
from reprorusted_python_cli import corpus_quality_report as report_mod
from reprorusted_python_cli import export_hf_corpus as export_mod
from reprorusted_python_cli import generate_insights as insights_mod
from reprorusted_python_cli import golden_traces_analyzer as golden_mod
from reprorusted_python_cli import hitl_sampler as hitl_mod
from reprorusted_python_cli import label_corpus as label_mod
from reprorusted_python_cli import measure_compile_rate as compile_mod
from reprorusted_python_cli import verify_qa_checklist as qa_mod
from reprorusted_python_cli import zero_success_analyzer as zero_mod


class TestAugmentCorpusMain:
    """Tests for augment_corpus main()."""

    def test_main_runs(self) -> None:
        """Main function runs with required args."""
        with patch("sys.argv", ["prog", "input.parquet"]):
            augment_mod.main()

    def test_main_with_options(self) -> None:
        """Main function runs with all options."""
        with patch(
            "sys.argv",
            ["prog", "input.parquet", "-o", "out.parquet", "--multiplier", "3"],
        ):
            augment_mod.main()


class TestCategoryDiffMain:
    """Tests for category_diff main()."""

    def test_main_runs(self) -> None:
        """Main function runs with required args."""
        with patch("sys.argv", ["prog", "base.parquet", "current.parquet"]):
            category_mod.main()

    def test_main_with_output(self) -> None:
        """Main function runs with output option."""
        with patch(
            "sys.argv",
            ["prog", "base.parquet", "current.parquet", "-o", "diff.json"],
        ):
            category_mod.main()


class TestCheckTestLibCratesMain:
    """Tests for check_test_lib_crates main()."""

    def test_main_runs(self) -> None:
        """Main function runs with no args."""
        with patch("sys.argv", ["prog"]):
            check_mod.main()

    def test_main_with_dir(self) -> None:
        """Main function runs with examples dir."""
        with patch("sys.argv", ["prog", "-d", "/tmp/examples"]):
            check_mod.main()


class TestClippyGateMain:
    """Tests for clippy_gate main()."""

    def test_main_runs(self) -> None:
        """Main function runs with no args."""
        with patch("sys.argv", ["prog"]):
            clippy_mod.main()

    def test_main_strict(self) -> None:
        """Main function runs with strict flag."""
        with patch("sys.argv", ["prog", "--strict"]):
            clippy_mod.main()

    def test_main_verbose(self) -> None:
        """Main function runs with verbose flag."""
        with patch("sys.argv", ["prog", "-v"]):
            clippy_mod.main()


class TestCorpusQualityReportMain:
    """Tests for corpus_quality_report main()."""

    def test_main_runs(self) -> None:
        """Main function runs with required args."""
        with patch("sys.argv", ["prog", "input.parquet"]):
            report_mod.main()

    def test_main_with_output(self) -> None:
        """Main function runs with output option."""
        with patch("sys.argv", ["prog", "input.parquet", "-o", "report.json"]):
            report_mod.main()


class TestExportHfCorpusMain:
    """Tests for export_hf_corpus main()."""

    def test_main_runs(self) -> None:
        """Main function runs with no args."""
        with patch("sys.argv", ["prog"]):
            export_mod.main()

    def test_main_with_paths(self) -> None:
        """Main function runs with input and output."""
        with patch("sys.argv", ["prog", "-i", "in.parquet", "-o", "out.parquet"]):
            export_mod.main()


class TestGenerateInsightsMain:
    """Tests for generate_insights main()."""

    def test_main_runs(self) -> None:
        """Main function runs with no args."""
        with patch("sys.argv", ["prog"]):
            insights_mod.main()

    def test_main_with_paths(self) -> None:
        """Main function runs with input and output."""
        with patch(
            "sys.argv",
            ["prog", "-i", "in.parquet", "-o", "insights.json"],
        ):
            insights_mod.main()


class TestGoldenTracesMain:
    """Tests for golden_traces_analyzer main()."""

    def test_main_runs(self) -> None:
        """Main function runs with no args."""
        with patch("sys.argv", ["prog"]):
            golden_mod.main()

    def test_main_with_output(self) -> None:
        """Main function runs with output option."""
        with patch("sys.argv", ["prog", "-o", "golden.json"]):
            golden_mod.main()

    def test_main_json(self) -> None:
        """Main function runs with json flag."""
        with patch("sys.argv", ["prog", "--json"]):
            golden_mod.main()


class TestHitlSamplerMain:
    """Tests for hitl_sampler main()."""

    def test_main_sample(self) -> None:
        """Main function runs in sample mode."""
        with patch("sys.argv", ["prog"]):
            hitl_mod.main()

    def test_main_report(self) -> None:
        """Main function runs in report mode."""
        with patch("sys.argv", ["prog", "--report"]):
            hitl_mod.main()

    def test_main_with_input(self) -> None:
        """Main function runs with input path."""
        with patch("sys.argv", ["prog", "-i", "corpus.parquet"]):
            hitl_mod.main()

    def test_main_custom_pct(self) -> None:
        """Main function runs with custom sample pct."""
        with patch("sys.argv", ["prog", "--sample-pct", "10.0"]):
            hitl_mod.main()


class TestLabelCorpusMain:
    """Tests for label_corpus main()."""

    def test_main_runs(self) -> None:
        """Main function runs with required args."""
        with patch("sys.argv", ["prog", "input.parquet"]):
            label_mod.main()

    def test_main_with_options(self) -> None:
        """Main function runs with all options."""
        with patch(
            "sys.argv",
            ["prog", "input.parquet", "-o", "out.parquet", "--threshold", "0.7"],
        ):
            label_mod.main()


class TestMeasureCompileRateMain:
    """Tests for measure_compile_rate main()."""

    def test_main_runs(self) -> None:
        """Main function runs with no args."""
        with patch("sys.argv", ["prog"]):
            compile_mod.main()

    def test_main_verbose(self) -> None:
        """Main function runs with verbose flag."""
        with patch("sys.argv", ["prog", "-v"]):
            compile_mod.main()

    def test_main_with_dir(self) -> None:
        """Main function runs with examples dir."""
        with patch("sys.argv", ["prog", "-d", "/tmp/examples"]):
            compile_mod.main()


class TestVerifyQaChecklistMain:
    """Tests for verify_qa_checklist main()."""

    def test_main_runs(self) -> None:
        """Main function runs with no args."""
        with patch("sys.argv", ["prog"]):
            qa_mod.main()

    def test_main_strict(self) -> None:
        """Main function runs with strict flag."""
        with patch("sys.argv", ["prog", "--strict"]):
            qa_mod.main()

    def test_main_with_input(self) -> None:
        """Main function runs with input path."""
        with patch("sys.argv", ["prog", "-i", "corpus.parquet"]):
            qa_mod.main()


class TestZeroSuccessMain:
    """Tests for zero_success_analyzer main()."""

    def test_main_runs(self) -> None:
        """Main function runs with required args."""
        with patch("sys.argv", ["prog", "input.parquet"]):
            zero_mod.main()

    def test_main_with_output(self) -> None:
        """Main function runs with output option."""
        with patch("sys.argv", ["prog", "input.parquet", "-o", "analysis.json"]):
            zero_mod.main()
