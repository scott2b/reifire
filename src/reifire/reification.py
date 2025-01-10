"""Module for converting natural language prompts into reified data structures."""

from typing import Dict, Any, Optional
from .visualization.metadata import IconMetadata
from .visualization.registry import IconRegistry


class ReifiedConcept:
    """Base class for reified concepts."""

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
        self.icon: Optional[IconMetadata] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        data = self.data.copy()
        if self.icon:
            data["_icon"] = self.icon.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReifiedConcept":
        """Create from dictionary representation."""
        icon_data = data.pop("_icon", None)
        concept = cls(data)
        if icon_data:
            concept.icon = IconMetadata.from_dict(icon_data)
        return concept

    def set_icon(
        self,
        registry: IconRegistry,
        term: Optional[str] = None,
        icon_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Set an icon for this concept."""
        term = term or self.data.get("type", "")
        if icon_id:
            # Use specific icon
            self.icon = IconMetadata(
                icon_id=icon_id, term=term, metadata=metadata or {}
            )
            registry.associate_icon(term, icon_id, metadata)
        else:
            # Get suggestions and use the best match
            suggestions = registry.suggest_icons(term)
            if suggestions:
                best_match = suggestions[0]
                self.icon = IconMetadata(
                    icon_id=best_match["id"], term=term, metadata=metadata or {}
                )
                registry.associate_icon(term, best_match["id"], metadata)

    def clear_icon(self) -> None:
        """Remove the icon from this concept."""
        self.icon = None
