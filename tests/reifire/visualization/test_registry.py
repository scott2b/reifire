import pytest
from pathlib import Path
import tempfile
from unittest.mock import MagicMock
from reifire.visualization.registry import IconRegistry
from reifire.visualization.providers.base import IconProvider
from typing import Generator


@pytest.fixture
def mock_provider() -> IconProvider:
    provider = MagicMock(spec=IconProvider)
    provider.name = "mock"
    provider.priority = 10
    provider.is_available.return_value = True
    provider.search.return_value = [{"id": "123", "name": "test", "source": "mock", "image": "test.svg"}]
    provider.get_icon.return_value = {"id": "123", "name": "test", "source": "mock", "image": "test.svg"}
    return provider


@pytest.fixture
def mock_chain(mock_provider: IconProvider) -> MagicMock:
    from reifire.visualization.providers.chain import ProviderChain

    chain = MagicMock(spec=ProviderChain)
    chain.search.return_value = [{"id": "123", "name": "test", "source": "mock", "image": "test.svg"}]
    chain.search_all.return_value = [{"id": "123", "name": "test", "source": "mock", "image": "test.svg"}]
    chain.get_icon.return_value = {"id": "123", "name": "test", "source": "mock", "image": "test.svg"}
    return chain


@pytest.fixture
def registry(mock_chain: MagicMock) -> Generator[IconRegistry, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        registry_path = Path(tmpdir) / "registry.json"
        yield IconRegistry(mock_chain, registry_path)


def test_associate_icon(registry: IconRegistry) -> None:
    """Test associating an icon with a term."""
    registry.associate_icon("test", "123", {"tags": ["example"]})
    assert "test" in registry.associations
    assert registry.associations["test"]["icon_id"] == "123"
    assert registry.associations["test"]["metadata"]["tags"] == ["example"]


def test_get_icon(registry: IconRegistry, mock_chain: MagicMock) -> None:
    """Test retrieving an associated icon."""
    registry.associate_icon("test", "123", {"source": "mock"})
    icon = registry.get_icon("test")
    assert icon is not None and icon["id"] == "123"
    mock_chain.get_icon.assert_called_once_with("mock", "123")


def test_suggest_icons(registry: IconRegistry, mock_chain: MagicMock) -> None:
    """Test icon suggestions."""
    suggestions = registry.suggest_icons("test")
    assert len(suggestions) <= 5
    assert suggestions[0]["id"] == "123"
    mock_chain.search_all.assert_called()


def test_custom_mappings(registry: IconRegistry) -> None:
    """Test custom mapping functionality."""
    registry.set_custom_mapping("test", "custom_value")
    assert registry.get_custom_mapping("test") == "custom_value"
