import pytest
from pathlib import Path
import tempfile
from unittest.mock import MagicMock
from typing import Generator, cast

from reifire.reification import ReifiedConcept
from reifire.visualization.metadata import IconMetadata
from reifire.visualization.registry import IconRegistry
from reifire.visualization.nounproject import NounProjectClient


@pytest.fixture
def mock_client() -> NounProjectClient:
    client = MagicMock(spec=NounProjectClient)
    client.get_icon.return_value = {"id": "123", "term": "test"}
    client.search_icons.return_value = {"icons": [{"id": "123", "term": "test"}]}
    return cast(NounProjectClient, client)


@pytest.fixture
def registry(mock_client: NounProjectClient) -> Generator[IconRegistry, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        registry_path = Path(tmpdir) / "registry.json"
        yield IconRegistry(mock_client, registry_path)


def test_set_icon_with_id(registry: IconRegistry) -> None:
    """Test setting an icon with a specific ID."""
    concept = ReifiedConcept({"type": "test"})
    concept.set_icon(registry, icon_id="123")

    assert concept.icon is not None
    assert concept.icon.icon_id == "123"
    assert concept.icon.term == "test"


def test_set_icon_with_suggestions(registry: IconRegistry) -> None:
    """Test setting an icon using suggestions."""
    concept = ReifiedConcept({"type": "test"})
    concept.set_icon(registry)

    assert concept.icon is not None
    assert concept.icon.icon_id == "123"  # First suggestion


def test_clear_icon() -> None:
    """Test clearing an icon."""
    concept = ReifiedConcept({"type": "test"})
    concept.icon = IconMetadata(icon_id="123", term="test")

    concept.clear_icon()
    assert concept.icon is None
