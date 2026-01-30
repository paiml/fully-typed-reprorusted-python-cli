#!/usr/bin/env python3
"""Weak Supervision Labeling for Training Data.

Uses Tarantula fault localization scores as labeling function weights.

Usage:
    python -m reprorusted_python_cli.weak_supervision data/corpus.parquet

Examples:
    >>> labeler = WeakSupervisionLabeler()
    >>> result = labeler.label("def hello(): return 42")
    >>> result.label.name
    'LOW_RISK'

    >>> result = labeler.label("async def fetch(): await get()")
    >>> result.label.name
    'HIGH_RISK'

    >>> labeler.get_stats()["total_labeled"]
    2
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

# Tarantula-derived weights for labeling functions
TARANTULA_WEIGHTS: dict[str, float] = {
    "async_pattern": 0.946,
    "generator_pattern": 0.927,
    "walrus_pattern": 0.850,
    "lambda_pattern": 0.783,
    "context_manager_pattern": 0.652,
    "class_pattern": 0.612,
    "exception_pattern": 0.577,
}


class Label(Enum):
    """Risk labels for code transpilation.

    Examples:
        >>> Label.HIGH_RISK.name
        'HIGH_RISK'

        >>> Label.ABSTAIN.name
        'ABSTAIN'

        >>> len(list(Label))
        4
    """

    HIGH_RISK = auto()
    MEDIUM_RISK = auto()
    LOW_RISK = auto()
    ABSTAIN = auto()


@dataclass
class LabelingFunction:
    """A programmatic labeling function with Tarantula weight.

    Attributes:
        name: Identifier for this labeling function.
        weight: Tarantula-derived weight (0.0 to 1.0).
        pattern: Regex pattern to match against code.
        label: Label to assign when pattern matches.

    Examples:
        >>> lf = LabelingFunction("test", 0.5, r"async def", Label.HIGH_RISK)
        >>> lf.apply("async def foo(): pass").name
        'HIGH_RISK'

        >>> lf.apply("def foo(): pass").name
        'ABSTAIN'

        >>> lf.weight
        0.5
    """

    name: str
    weight: float
    pattern: str
    label: Label = Label.HIGH_RISK

    def apply(self, code: str) -> Label:
        """Apply LF to code, return label or ABSTAIN.

        Args:
            code: Python source code to check.

        Returns:
            Matching label or ABSTAIN if pattern not found.

        Examples:
            >>> lf = LabelingFunction("test", 0.5, r"yield", Label.HIGH_RISK)
            >>> lf.apply("def gen(): yield 1").name
            'HIGH_RISK'

            >>> lf.apply("def normal(): return 1").name
            'ABSTAIN'

            >>> lf.apply("").name
            'ABSTAIN'
        """
        if re.search(self.pattern, code):
            return self.label
        return Label.ABSTAIN


@dataclass
class LabeledExample:
    """Result of weak supervision labeling.

    Attributes:
        code: The labeled source code.
        label: Assigned risk label.
        confidence: Confidence score (0.0 to 1.0).
        lf_votes: Per-LF vote mapping.

    Examples:
        >>> ex = LabeledExample("code", Label.LOW_RISK, 1.0)
        >>> ex.label.name
        'LOW_RISK'

        >>> ex.confidence
        1.0

        >>> ex.lf_votes
        {}
    """

    code: str
    label: Label
    confidence: float
    lf_votes: dict[str, Label] = field(default_factory=dict)


class WeakSupervisionLabeler:
    """Label code using programmatic labeling functions.

    Examples:
        >>> labeler = WeakSupervisionLabeler()
        >>> len(labeler.labeling_functions)
        4

        >>> result = labeler.label("def simple(): return 1")
        >>> result.label.name
        'LOW_RISK'

        >>> result = labeler.label("async def f(): await g()")
        >>> result.label.name
        'HIGH_RISK'
    """

    def __init__(self, threshold: float = 0.5) -> None:
        """Initialize with built-in Tarantula-weighted LFs.

        Args:
            threshold: Confidence threshold for labeling.

        Examples:
            >>> labeler = WeakSupervisionLabeler(threshold=0.7)
            >>> labeler.threshold
            0.7
        """
        self.threshold = threshold
        self._stats: dict[str, int] = {"labeled": 0, "conflicts": 0, "abstentions": 0}
        self.labeling_functions: list[LabelingFunction] = [
            LabelingFunction(
                name="async_pattern",
                weight=TARANTULA_WEIGHTS["async_pattern"],
                pattern=r"async def|await ",
                label=Label.HIGH_RISK,
            ),
            LabelingFunction(
                name="generator_pattern",
                weight=TARANTULA_WEIGHTS["generator_pattern"],
                pattern=r"yield ",
                label=Label.HIGH_RISK,
            ),
            LabelingFunction(
                name="lambda_pattern",
                weight=TARANTULA_WEIGHTS["lambda_pattern"],
                pattern=r"lambda ",
                label=Label.MEDIUM_RISK,
            ),
            LabelingFunction(
                name="context_manager_pattern",
                weight=TARANTULA_WEIGHTS["context_manager_pattern"],
                pattern=r"with .+:",
                label=Label.MEDIUM_RISK,
            ),
        ]

    def label(self, code: str) -> LabeledExample:
        """Apply all LFs and aggregate labels.

        Args:
            code: Python source code to label.

        Returns:
            LabeledExample with aggregated label and confidence.

        Examples:
            >>> labeler = WeakSupervisionLabeler()
            >>> result = labeler.label("def f(): return 1")
            >>> result.confidence
            1.0

            >>> result = labeler.label("lambda x: x + 1")
            >>> result.label.name
            'MEDIUM_RISK'

            >>> result = labeler.label("")
            >>> result.label.name
            'LOW_RISK'
        """
        votes: dict[str, Label] = {}
        weighted_scores: dict[Label, float] = {
            Label.HIGH_RISK: 0.0,
            Label.MEDIUM_RISK: 0.0,
            Label.LOW_RISK: 0.0,
        }

        for lf in self.labeling_functions:
            vote = lf.apply(code)
            votes[lf.name] = vote
            if vote != Label.ABSTAIN:
                weighted_scores[vote] += lf.weight

        non_abstain = [v for v in votes.values() if v != Label.ABSTAIN]
        if not non_abstain:
            final_label = Label.LOW_RISK
            confidence = 1.0
            self._stats["abstentions"] += 1
        else:
            final_label = max(weighted_scores, key=lambda k: weighted_scores[k])
            total_weight = sum(weighted_scores.values())
            confidence = (
                weighted_scores[final_label] / total_weight if total_weight else 0.5
            )
            if len(set(non_abstain)) > 1:
                self._stats["conflicts"] += 1

        self._stats["labeled"] += 1
        return LabeledExample(
            code=code, label=final_label, confidence=confidence, lf_votes=votes
        )

    def get_stats(self) -> dict[str, int | float]:
        """Return labeling statistics.

        Returns:
            Dict with total_labeled, coverage, conflicts, abstentions.

        Examples:
            >>> labeler = WeakSupervisionLabeler()
            >>> _ = labeler.label("x = 1")
            >>> stats = labeler.get_stats()
            >>> stats["total_labeled"]
            1
        """
        total = self._stats["labeled"] or 1
        return {
            "total_labeled": self._stats["labeled"],
            "coverage": (total - self._stats["abstentions"]) / total,
            "conflicts": self._stats["conflicts"] / total,
            "abstentions": self._stats["abstentions"],
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Weak Supervision Labeling")
    parser.add_argument("input", help="Input parquet file")
    parser.add_argument("--output", "-o", help="Output parquet file")
    parser.add_argument("--stats", action="store_true", help="Show LF statistics")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    labeler = WeakSupervisionLabeler(threshold=args.threshold)
    print(f"Labeler initialized with {len(labeler.labeling_functions)} LFs")
