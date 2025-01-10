"""Common test fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def test_icons_dir() -> Path:
    """Get the base directory for test icons."""
    base_dir = Path(__file__).parent.parent.parent / "assets" / "icons"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


@pytest.fixture
def nounproject_icons_dir(test_icons_dir: Path) -> Path:
    """Get the directory for Noun Project test icons."""
    icons_dir = test_icons_dir / "nounproject"
    icons_dir.mkdir(exist_ok=True)
    return icons_dir


@pytest.fixture
def material_icons_dir(test_icons_dir: Path) -> Path:
    """Get the directory for Material Design test icons."""
    icons_dir = test_icons_dir / "material_design"
    icons_dir.mkdir(exist_ok=True)
    return icons_dir 