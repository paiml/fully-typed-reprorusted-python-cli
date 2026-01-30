"""Comprehensive tests for synthetic_augmenter module."""

from __future__ import annotations

from reprorusted_python_cli.synthetic_augmenter import (
    TARANTULA_SCORES,
    AugmentedExample,
    MutationStrategy,
    SyntheticAugmenter,
)


class TestMutationStrategy:
    """Tests for the MutationStrategy enum."""

    def test_strategy_members(self) -> None:
        """All three strategy values exist."""
        assert MutationStrategy.TARANTULA is not None
        assert MutationStrategy.RANDOM is not None
        assert MutationStrategy.TARGETED is not None

    def test_strategy_count(self) -> None:
        """There are exactly 3 strategies."""
        assert len(list(MutationStrategy)) == 3

    def test_strategy_names(self) -> None:
        """Strategy names match expected strings."""
        assert MutationStrategy.TARANTULA.name == "TARANTULA"
        assert MutationStrategy.RANDOM.name == "RANDOM"
        assert MutationStrategy.TARGETED.name == "TARGETED"


class TestTarantulaScores:
    """Tests for the TARANTULA_SCORES constant."""

    def test_scores_exist(self) -> None:
        """Expected score keys are present."""
        expected_keys = {
            "async_await",
            "generator",
            "generator_expression",
            "walrus_operator",
            "lambda",
            "context_manager",
            "class_definition",
            "exception_handling",
            "stdin_usage",
            "list_comprehension",
            "import_statement",
            "function_definition",
        }
        assert set(TARANTULA_SCORES.keys()) == expected_keys

    def test_scores_in_range(self) -> None:
        """All scores are between 0 and 1."""
        for score in TARANTULA_SCORES.values():
            assert 0.0 <= score <= 1.0

    def test_async_highest(self) -> None:
        """Async/await has the highest score."""
        assert TARANTULA_SCORES["async_await"] == max(TARANTULA_SCORES.values())


class TestAugmentedExample:
    """Tests for the AugmentedExample dataclass."""

    def test_creation(self) -> None:
        """AugmentedExample can be created with required fields."""
        ex = AugmentedExample(
            original_code="def f(): pass",
            mutated_code="async def f(): pass",
            mutation_type="async_await",
        )
        assert ex.original_code == "def f(): pass"
        assert ex.mutated_code == "async def f(): pass"
        assert ex.mutation_type == "async_await"

    def test_default_is_synthetic(self) -> None:
        """Default is_synthetic is True."""
        ex = AugmentedExample("a", "b", "test")
        assert ex.is_synthetic is True

    def test_default_metadata(self) -> None:
        """Default metadata is an empty dict."""
        ex = AugmentedExample("a", "b", "test")
        assert ex.metadata == {}

    def test_custom_metadata(self) -> None:
        """Custom metadata is stored."""
        meta = {"tarantula_score": 0.9}
        ex = AugmentedExample("a", "b", "test", metadata=meta)
        assert ex.metadata["tarantula_score"] == 0.9

    def test_distinct_default_metadata(self) -> None:
        """Each instance gets its own default metadata dict."""
        ex1 = AugmentedExample("a", "b", "t1")
        ex2 = AugmentedExample("c", "d", "t2")
        ex1.metadata["key"] = 1.0
        assert "key" not in ex2.metadata


class TestSyntheticAugmenter:
    """Tests for the SyntheticAugmenter class."""

    def test_default_strategy(self) -> None:
        """Default strategy is TARANTULA."""
        aug = SyntheticAugmenter()
        assert aug.strategy == MutationStrategy.TARANTULA

    def test_custom_strategy(self) -> None:
        """Custom strategy is stored correctly."""
        aug = SyntheticAugmenter(strategy=MutationStrategy.RANDOM)
        assert aug.strategy == MutationStrategy.RANDOM

    def test_mutation_methods_exist(self) -> None:
        """All 4 mutation methods are registered."""
        aug = SyntheticAugmenter()
        assert len(aug._mutation_methods) == 4

    def test_mutation_method_keys(self) -> None:
        """Expected mutation type keys are present."""
        aug = SyntheticAugmenter()
        expected = {
            "async_await",
            "generator",
            "lambda",
            "walrus_operator",
        }
        assert set(aug._mutation_methods.keys()) == expected

    def test_mutate_async(self) -> None:
        """Async mutation injects async/await pattern."""
        aug = SyntheticAugmenter()
        result = aug.mutate("def hello(): return 1", mutation_type="async_await")
        assert isinstance(result, AugmentedExample)
        assert "async def" in result.mutated_code
        assert result.mutation_type == "async_await"
        assert result.original_code == "def hello(): return 1"

    def test_mutate_generator(self) -> None:
        """Generator mutation injects yield pattern."""
        aug = SyntheticAugmenter()
        result = aug.mutate("def gen(): return 1", mutation_type="generator")
        assert "yield" in result.mutated_code
        assert result.mutation_type == "generator"

    def test_mutate_lambda(self) -> None:
        """Lambda mutation appends lambda expression."""
        aug = SyntheticAugmenter()
        result = aug.mutate("x = 1", mutation_type="lambda")
        assert "lambda" in result.mutated_code
        assert result.mutation_type == "lambda"

    def test_mutate_walrus(self) -> None:
        """Walrus mutation injects walrus operator."""
        aug = SyntheticAugmenter()
        result = aug.mutate("x = 42", mutation_type="walrus_operator")
        assert ":=" in result.mutated_code
        assert result.mutation_type == "walrus_operator"

    def test_mutate_has_metadata(self) -> None:
        """Mutation results include tarantula_score metadata."""
        aug = SyntheticAugmenter()
        result = aug.mutate("def f(): return 1", mutation_type="async_await")
        assert "tarantula_score" in result.metadata

    def test_mutate_is_synthetic(self) -> None:
        """All mutations are marked as synthetic."""
        aug = SyntheticAugmenter()
        result = aug.mutate("x = 1", mutation_type="lambda")
        assert result.is_synthetic is True

    def test_mutate_tarantula_strategy(self) -> None:
        """Tarantula strategy selects a valid mutation type."""
        aug = SyntheticAugmenter(strategy=MutationStrategy.TARANTULA)
        result = aug.mutate("def f(): return 1")
        assert result.mutation_type in aug._mutation_methods

    def test_mutate_random_strategy(self) -> None:
        """Random strategy selects a valid mutation type."""
        aug = SyntheticAugmenter(strategy=MutationStrategy.RANDOM)
        result = aug.mutate("def f(): return 1")
        assert result.mutation_type in aug._mutation_methods

    def test_mutate_targeted_strategy(self) -> None:
        """Targeted strategy uses the first mutation method."""
        aug = SyntheticAugmenter(strategy=MutationStrategy.TARGETED)
        result = aug.mutate("def f(): return 1")
        first_key = next(iter(aug._mutation_methods.keys()))
        assert result.mutation_type == first_key

    def test_generate_batch_default_count(self) -> None:
        """Generate batch creates 3 examples by default."""
        aug = SyntheticAugmenter()
        results = aug.generate_batch("def f(): return 1")
        assert len(results) == 3

    def test_generate_batch_custom_count(self) -> None:
        """Generate batch creates requested number of examples."""
        aug = SyntheticAugmenter()
        results = aug.generate_batch("def f(): return 1", count=5)
        assert len(results) == 5

    def test_generate_batch_types(self) -> None:
        """Generate batch returns AugmentedExample instances."""
        aug = SyntheticAugmenter()
        results = aug.generate_batch("def f(): return 1", count=2)
        for result in results:
            assert isinstance(result, AugmentedExample)

    def test_generate_batch_cycles_mutation_types(self) -> None:
        """Generate batch cycles through mutation types."""
        aug = SyntheticAugmenter()
        results = aug.generate_batch("def f(): return 1", count=8)
        types = [r.mutation_type for r in results]
        # 8 items cycling through 4 methods = each appears twice
        assert len(types) == 8

    def test_select_by_tarantula(self) -> None:
        """Tarantula selection returns a valid mutation type."""
        aug = SyntheticAugmenter()
        selected = aug._select_by_tarantula()
        assert selected in aug._mutation_methods

    def test_inject_async_no_return(self) -> None:
        """Async injection works on code without return."""
        aug = SyntheticAugmenter()
        result = aug._inject_async_pattern("def f(): pass")
        assert "async def" in result.mutated_code
        assert "await" not in result.mutated_code

    def test_inject_async_with_return(self) -> None:
        """Async injection adds await when return is present."""
        aug = SyntheticAugmenter()
        result = aug._inject_async_pattern("def f(): return 42")
        assert "async def" in result.mutated_code
        assert "await" in result.mutated_code

    def test_inject_generator_no_return(self) -> None:
        """Generator injection on code without return."""
        aug = SyntheticAugmenter()
        result = aug._inject_generator_pattern("def f(): pass")
        assert result.mutated_code == "def f(): pass"

    def test_inject_generator_with_return(self) -> None:
        """Generator injection replaces return with yield."""
        aug = SyntheticAugmenter()
        result = aug._inject_generator_pattern("def f(): return 42")
        assert "yield" in result.mutated_code

    def test_inject_lambda(self) -> None:
        """Lambda injection appends lambda expression."""
        aug = SyntheticAugmenter()
        result = aug._inject_lambda_pattern("x = 1")
        assert result.mutated_code.endswith("lambda x: x * 2")

    def test_inject_walrus(self) -> None:
        """Walrus injection replaces assignment."""
        aug = SyntheticAugmenter()
        result = aug._inject_walrus_pattern("x = 42")
        assert ":=" in result.mutated_code

    def test_inject_walrus_no_assignment(self) -> None:
        """Walrus injection on code without assignment."""
        aug = SyntheticAugmenter()
        result = aug._inject_walrus_pattern("print('hello')")
        assert result.mutated_code == "print('hello')"
