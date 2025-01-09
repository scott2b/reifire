"""Test configuration for reifire package."""

from pathlib import Path

import pytest


@pytest.fixture
def examples_dir() -> Path:
    """Return the path to the examples directory."""
    return Path(__file__).parent.parent / "examples"
