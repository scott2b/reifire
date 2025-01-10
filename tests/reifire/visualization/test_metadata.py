from pathlib import Path
from reifire.visualization.metadata import IconMetadata


def test_icon_metadata_serialization() -> None:
    """Test serialization of icon metadata."""
    icon = IconMetadata(
        icon_id="123",
        term="computer",
        metadata={"tags": ["technology"]},
        local_path=Path("/tmp/icons/123.svg"),
    )

    # Test to_dict
    data = icon.to_dict()
    assert data["icon_id"] == "123"
    assert data["term"] == "computer"
    assert data["metadata"]["tags"] == ["technology"]
    assert data["local_path"] == "/tmp/icons/123.svg"

    # Test from_dict
    restored = IconMetadata.from_dict(data)
    assert restored.icon_id == icon.icon_id
    assert restored.term == icon.term
    assert restored.metadata == icon.metadata
    assert restored.local_path == icon.local_path


def test_icon_metadata_defaults() -> None:
    """Test default values for icon metadata."""
    icon = IconMetadata(icon_id="123", term="computer")
    assert icon.source == "noun_project"
    assert icon.metadata == {}
    assert icon.local_path is None
