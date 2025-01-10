"""Tests for the Noun Project client."""

import pytest
from reifire.visualization.nounproject import NounProjectClient
from unittest.mock import patch, MagicMock
from pathlib import Path


@pytest.fixture
def mock_client() -> NounProjectClient:
    """Create a mock Noun Project client for testing."""
    with patch("requests.request") as mock_request:
        # Mock the initial authentication call
        mock_response = MagicMock()
        mock_response.json.return_value = {"icons": [{"id": "123"}]}
        mock_request.return_value = mock_response

        return NounProjectClient(
            "test_key", "test_secret", cache_dir=Path("/tmp/test_cache")
        )


def test_rate_limiting(mock_client: NounProjectClient) -> None:
    """Test rate limiting functionality."""
    with patch("time.sleep") as mock_sleep:
        mock_client._rate_limit_wait()
        mock_client._rate_limit_wait()
        assert mock_sleep.called


def test_get_icon(mock_client: NounProjectClient) -> None:
    """Test getting an icon by ID."""
    with patch("requests.request") as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "icon": {"id": "123", "preview_url": "http://example.com"}
        }
        mock_request.return_value = mock_response

        result = mock_client.get_icon("123")
        assert "icon" in result
        assert result["icon"]["id"] == "123"


def test_search_icons(mock_client: NounProjectClient) -> None:
    """Test searching for icons."""
    with patch("requests.request") as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = {"icons": [{"id": "123"}]}
        mock_request.return_value = mock_response

        result = mock_client.search_icons("test")
        assert "icons" in result
