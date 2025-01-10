import pytest
from pathlib import Path
import tempfile
from reifire.visualization.suggestions import IconSuggester
from typing import Generator


@pytest.fixture
def suggester() -> Generator[IconSuggester, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        usage_path = Path(tmpdir) / "usage.json"
        yield IconSuggester(usage_path)


def test_related_terms(suggester: IconSuggester) -> None:
    """Test getting related terms."""
    related = suggester.get_related_terms("computer")
    assert len(related) > 0
    assert "machine" in related


def test_icon_scoring(suggester: IconSuggester) -> None:
    """Test icon relevance scoring."""
    icon = {"id": "123", "term": "computer", "tags": ["technology", "device"]}
    score = suggester.score_icon(icon, "computer")
    assert 0 <= score <= 1
    assert score >= 0.5  # High score for exact match


def test_usage_recording(suggester: IconSuggester) -> None:
    """Test recording and using selection history."""
    suggester.record_selection("computer", "123")
    suggester.record_selection("computer", "123")

    icon = {"id": "123", "term": "computer"}
    score1 = suggester.score_icon(icon, "computer")

    icon2 = {"id": "456", "term": "computer"}
    score2 = suggester.score_icon(icon2, "computer")

    assert score1 > score2  # Previously selected icon scores higher


def test_suggestion_sorting(suggester: IconSuggester) -> None:
    """Test sorting suggestions by relevance."""
    icons = [
        {"id": "1", "term": "computer", "tags": ["technology"]},
        {"id": "2", "term": "laptop", "tags": ["computer"]},
        {"id": "3", "term": "desk", "tags": ["furniture"]},
    ]

    sorted_icons = suggester.sort_suggestions(icons, "computer")
    assert len(sorted_icons) == 3
    assert sorted_icons[0]["id"] == "1"  # Most relevant first
