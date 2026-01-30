"""Pytest configuration and shared fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def tmp_corpus_dir(tmp_path: Path) -> Path:
    """Create a temporary corpus directory structure."""
    examples = tmp_path / "examples"
    examples.mkdir()
    return tmp_path


@pytest.fixture
def sample_python_code() -> str:
    """Return sample Python code for testing."""
    return '''def hello(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"
'''


@pytest.fixture
def sample_async_code() -> str:
    """Return sample async Python code for testing."""
    return '''async def fetch_data(url: str) -> str:
    """Fetch data from URL."""
    return await get(url)
'''
