from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class IconMetadata:
    """Metadata for icons associated with reified concepts."""

    icon_id: str
    term: str
    source: str = "noun_project"  # Future-proof for other icon sources
    metadata: Dict[str, Any] = field(default_factory=dict)
    local_path: Optional[Path] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = {
            "icon_id": self.icon_id,
            "term": self.term,
            "source": self.source,
            "metadata": self.metadata,
        }
        if self.local_path:
            data["local_path"] = str(self.local_path)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IconMetadata":
        """Create from dictionary."""
        local_path = data.get("local_path")
        if local_path:
            local_path = Path(local_path)
        return cls(
            icon_id=data["icon_id"],
            term=data["term"],
            source=data.get("source", "noun_project"),
            metadata=data.get("metadata", {}),
            local_path=local_path,
        )
