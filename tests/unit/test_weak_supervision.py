"""Comprehensive tests for weak_supervision module."""

from __future__ import annotations

from reprorusted_python_cli.weak_supervision import (
    TARANTULA_WEIGHTS,
    Label,
    LabeledExample,
    LabelingFunction,
    WeakSupervisionLabeler,
)


class TestLabel:
    """Tests for the Label enum."""

    def test_label_members(self) -> None:
        """All four label values exist."""
        assert Label.HIGH_RISK is not None
        assert Label.MEDIUM_RISK is not None
        assert Label.LOW_RISK is not None
        assert Label.ABSTAIN is not None

    def test_label_count(self) -> None:
        """There are exactly 4 labels."""
        assert len(list(Label)) == 4

    def test_label_names(self) -> None:
        """Label names match expected strings."""
        assert Label.HIGH_RISK.name == "HIGH_RISK"
        assert Label.MEDIUM_RISK.name == "MEDIUM_RISK"
        assert Label.LOW_RISK.name == "LOW_RISK"
        assert Label.ABSTAIN.name == "ABSTAIN"

    def test_label_uniqueness(self) -> None:
        """All label values are distinct."""
        values = [label.value for label in Label]
        assert len(values) == len(set(values))


class TestTarantulaWeights:
    """Tests for the TARANTULA_WEIGHTS constant."""

    def test_weights_exist(self) -> None:
        """All expected weight keys are present."""
        expected_keys = {
            "async_pattern",
            "generator_pattern",
            "walrus_pattern",
            "lambda_pattern",
            "context_manager_pattern",
            "class_pattern",
            "exception_pattern",
        }
        assert set(TARANTULA_WEIGHTS.keys()) == expected_keys

    def test_weights_in_range(self) -> None:
        """All weights are between 0 and 1."""
        for weight in TARANTULA_WEIGHTS.values():
            assert 0.0 <= weight <= 1.0

    def test_async_highest(self) -> None:
        """Async pattern has the highest weight."""
        assert TARANTULA_WEIGHTS["async_pattern"] == max(TARANTULA_WEIGHTS.values())


class TestLabelingFunction:
    """Tests for the LabelingFunction dataclass."""

    def test_creation(self) -> None:
        """LabelingFunction can be created with all fields."""
        lf = LabelingFunction("test", 0.5, r"async def", Label.HIGH_RISK)
        assert lf.name == "test"
        assert lf.weight == 0.5
        assert lf.pattern == r"async def"
        assert lf.label == Label.HIGH_RISK

    def test_default_label(self) -> None:
        """Default label is HIGH_RISK."""
        lf = LabelingFunction("test", 0.5, r"foo")
        assert lf.label == Label.HIGH_RISK

    def test_apply_match(self) -> None:
        """Apply returns the label when pattern matches."""
        lf = LabelingFunction("async", 0.9, r"async def", Label.HIGH_RISK)
        result = lf.apply("async def foo(): pass")
        assert result == Label.HIGH_RISK

    def test_apply_no_match(self) -> None:
        """Apply returns ABSTAIN when pattern does not match."""
        lf = LabelingFunction("async", 0.9, r"async def", Label.HIGH_RISK)
        result = lf.apply("def foo(): pass")
        assert result == Label.ABSTAIN

    def test_apply_empty_code(self) -> None:
        """Apply returns ABSTAIN on empty string."""
        lf = LabelingFunction("test", 0.5, r"yield", Label.HIGH_RISK)
        assert lf.apply("") == Label.ABSTAIN

    def test_apply_regex_pattern(self) -> None:
        """Apply works with complex regex patterns."""
        lf = LabelingFunction("ctx", 0.6, r"with .+:", Label.MEDIUM_RISK)
        assert lf.apply("with open('f') as fp:") == Label.MEDIUM_RISK
        assert lf.apply("without context") == Label.ABSTAIN

    def test_apply_yield_pattern(self) -> None:
        """Apply detects yield in generator functions."""
        lf = LabelingFunction("gen", 0.9, r"yield ", Label.HIGH_RISK)
        assert lf.apply("def gen(): yield 1") == Label.HIGH_RISK
        assert lf.apply("def normal(): return 1") == Label.ABSTAIN

    def test_apply_multiline(self) -> None:
        """Apply works with multiline code."""
        lf = LabelingFunction("lambda", 0.7, r"lambda ", Label.MEDIUM_RISK)
        code = "x = 1\nf = lambda x: x + 1\ny = 2"
        assert lf.apply(code) == Label.MEDIUM_RISK


class TestLabeledExample:
    """Tests for the LabeledExample dataclass."""

    def test_creation(self) -> None:
        """LabeledExample can be created with required fields."""
        ex = LabeledExample("code", Label.LOW_RISK, 1.0)
        assert ex.code == "code"
        assert ex.label == Label.LOW_RISK
        assert ex.confidence == 1.0

    def test_default_lf_votes(self) -> None:
        """Default lf_votes is an empty dict."""
        ex = LabeledExample("code", Label.LOW_RISK, 1.0)
        assert ex.lf_votes == {}

    def test_custom_lf_votes(self) -> None:
        """LabeledExample accepts custom lf_votes."""
        votes = {"async": Label.HIGH_RISK, "lambda": Label.ABSTAIN}
        ex = LabeledExample("code", Label.HIGH_RISK, 0.9, lf_votes=votes)
        assert ex.lf_votes == votes
        assert len(ex.lf_votes) == 2

    def test_distinct_default_dicts(self) -> None:
        """Each instance gets its own default dict."""
        ex1 = LabeledExample("a", Label.LOW_RISK, 1.0)
        ex2 = LabeledExample("b", Label.LOW_RISK, 1.0)
        ex1.lf_votes["test"] = Label.HIGH_RISK
        assert "test" not in ex2.lf_votes


class TestWeakSupervisionLabeler:
    """Tests for the WeakSupervisionLabeler class."""

    def test_default_threshold(self) -> None:
        """Default threshold is 0.5."""
        labeler = WeakSupervisionLabeler()
        assert labeler.threshold == 0.5

    def test_custom_threshold(self) -> None:
        """Custom threshold is stored correctly."""
        labeler = WeakSupervisionLabeler(threshold=0.7)
        assert labeler.threshold == 0.7

    def test_default_labeling_functions(self) -> None:
        """Has 4 built-in labeling functions."""
        labeler = WeakSupervisionLabeler()
        assert len(labeler.labeling_functions) == 4

    def test_lf_names(self) -> None:
        """Built-in LFs have expected names."""
        labeler = WeakSupervisionLabeler()
        names = {lf.name for lf in labeler.labeling_functions}
        expected = {
            "async_pattern",
            "generator_pattern",
            "lambda_pattern",
            "context_manager_pattern",
        }
        assert names == expected

    def test_label_simple_code(self) -> None:
        """Simple code without patterns returns LOW_RISK."""
        labeler = WeakSupervisionLabeler()
        result = labeler.label("def f(): return 1")
        assert result.label == Label.LOW_RISK
        assert result.confidence == 1.0

    def test_label_async_code(self) -> None:
        """Async code returns HIGH_RISK."""
        labeler = WeakSupervisionLabeler()
        result = labeler.label("async def f(): await g()")
        assert result.label == Label.HIGH_RISK

    def test_label_generator_code(self) -> None:
        """Generator code returns HIGH_RISK."""
        labeler = WeakSupervisionLabeler()
        result = labeler.label("def gen(): yield 1")
        assert result.label == Label.HIGH_RISK

    def test_label_lambda_code(self) -> None:
        """Lambda code returns MEDIUM_RISK."""
        labeler = WeakSupervisionLabeler()
        result = labeler.label("f = lambda x: x + 1")
        assert result.label == Label.MEDIUM_RISK

    def test_label_context_manager_code(self) -> None:
        """Context manager code returns MEDIUM_RISK."""
        labeler = WeakSupervisionLabeler()
        result = labeler.label("with open('f') as fp: pass")
        assert result.label == Label.MEDIUM_RISK

    def test_label_empty_code(self) -> None:
        """Empty string returns LOW_RISK."""
        labeler = WeakSupervisionLabeler()
        result = labeler.label("")
        assert result.label == Label.LOW_RISK

    def test_label_has_votes(self) -> None:
        """Labeled result includes votes from all LFs."""
        labeler = WeakSupervisionLabeler()
        result = labeler.label("async def f(): pass")
        assert len(result.lf_votes) == 4

    def test_label_confidence_range(self) -> None:
        """Confidence is always between 0 and 1."""
        labeler = WeakSupervisionLabeler()
        for code in [
            "async def f(): pass",
            "yield 1",
            "lambda x: x",
            "def f(): return 1",
            "",
        ]:
            result = labeler.label(code)
            assert 0.0 <= result.confidence <= 1.0

    def test_stats_initial(self) -> None:
        """Initial stats are all zeros."""
        labeler = WeakSupervisionLabeler()
        stats = labeler.get_stats()
        assert stats["total_labeled"] == 0
        assert stats["abstentions"] == 0

    def test_stats_after_labeling(self) -> None:
        """Stats update after labeling."""
        labeler = WeakSupervisionLabeler()
        labeler.label("def f(): return 1")
        stats = labeler.get_stats()
        assert stats["total_labeled"] == 1

    def test_stats_coverage(self) -> None:
        """Coverage is correct after labeling."""
        labeler = WeakSupervisionLabeler()
        labeler.label("async def f(): pass")
        labeler.label("def f(): return 1")
        stats = labeler.get_stats()
        assert stats["total_labeled"] == 2
        # First has non-abstain vote, second is all abstain
        assert stats["abstentions"] == 1
        assert stats["coverage"] == 0.5

    def test_stats_conflicts(self) -> None:
        """Conflicts counted for mixed votes."""
        labeler = WeakSupervisionLabeler()
        # Code matching both HIGH_RISK and MEDIUM_RISK patterns
        code = "async def f(): lambda x: x"
        labeler.label(code)
        stats = labeler.get_stats()
        assert stats["conflicts"] > 0

    def test_multiple_labels(self) -> None:
        """Labeling many examples works correctly."""
        labeler = WeakSupervisionLabeler()
        codes = [
            "x = 1",
            "async def f(): pass",
            "def g(): yield 1",
            "f = lambda x: x",
            "with open('f') as fp: pass",
        ]
        for code in codes:
            result = labeler.label(code)
            assert isinstance(result, LabeledExample)
        stats = labeler.get_stats()
        assert stats["total_labeled"] == 5

    def test_label_combined_high_medium(self) -> None:
        """Code with async + lambda gets HIGH_RISK (higher weight)."""
        labeler = WeakSupervisionLabeler()
        result = labeler.label("async def f(): return lambda x: x")
        assert result.label == Label.HIGH_RISK

    def test_label_returns_labeled_example_type(self) -> None:
        """Label method returns a LabeledExample instance."""
        labeler = WeakSupervisionLabeler()
        result = labeler.label("x = 1")
        assert isinstance(result, LabeledExample)
        assert isinstance(result.label, Label)
        assert isinstance(result.confidence, float)
        assert isinstance(result.lf_votes, dict)
