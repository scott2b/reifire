import pytest
from pathlib import Path
import tempfile
from unittest.mock import MagicMock, Mock
from reifire.visualization.registry import IconRegistry
from reifire.visualization.nounproject import NounProjectClient
from typing import Generator, cast
from unittest.mock import call


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


def test_associate_icon(registry: IconRegistry) -> None:
    """Test associating an icon with a term."""
    registry.associate_icon("test", "123", {"tags": ["example"]})
    assert "test" in registry.associations
    assert registry.associations["test"]["icon_id"] == "123"
    assert registry.associations["test"]["metadata"]["tags"] == ["example"]


def test_get_icon(registry: IconRegistry, mock_client: NounProjectClient) -> None:
    """Test retrieving an associated icon."""
    registry.associate_icon("test", "123")
    icon = registry.get_icon("test")
    assert icon is not None and icon["id"] == "123"
    cast(Mock, mock_client.get_icon).assert_called_once_with("123")


def test_suggest_icons(registry: IconRegistry, mock_client: NounProjectClient) -> None:
    """Test icon suggestions."""
    suggestions = registry.suggest_icons("test")
    assert len(suggestions) <= 5  # We're limiting to 5 suggestions
    assert suggestions[0]["id"] == "123"
    # First call is for the original term
    assert cast(Mock, mock_client.search_icons).call_args_list[0] == call(
        "test", limit=5
    )


def test_custom_mappings(registry: IconRegistry) -> None:
    """Test custom mapping functionality."""
    registry.set_custom_mapping("test", "custom_value")
    assert registry.get_custom_mapping("test") == "custom_value"
