from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from .nounproject import NounProjectClient
from .suggestions import IconSuggester


class IconRegistry:
    """Manages icon associations and metadata for reified concepts."""

    def __init__(
        self,
        noun_project_client: NounProjectClient,
        registry_path: Optional[Path] = None,
        suggester: Optional[IconSuggester] = None,
    ) -> None:
        """Initialize the registry.

        Args:
            noun_project_client: Client for fetching icons
            registry_path: Path to store registry data (defaults to ~/.reifire/icon_registry.json)
            suggester: Suggestion engine for intelligent suggestions
        """
        self.client = noun_project_client
        self.registry_path = (
            registry_path or Path.home() / ".reifire" / "icon_registry.json"
        )
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.suggester = suggester or IconSuggester()
        self._load_registry()

    def _load_registry(self) -> None:
        """Load the registry from disk."""
        self.associations: Dict[str, Dict[str, Any]] = {}
        if self.registry_path.exists():
            self.associations = json.loads(self.registry_path.read_text())

    def _save_registry(self) -> None:
        """Save the registry to disk."""
        self.registry_path.write_text(json.dumps(self.associations, indent=2))

    def associate_icon(
        self, term: str, icon_id: str, metadata: Optional[Dict] = None
    ) -> None:
        """Associate an icon with a term.

        Args:
            term: The term to associate with
            icon_id: The Noun Project icon ID
            metadata: Optional metadata about the association
        """
        self.associations[term] = {
            "icon_id": icon_id,
            "metadata": metadata or {},
            "version": 1,  # Basic versioning
        }
        self._save_registry()
        # Record selection for future suggestions
        self.suggester.record_selection(term, icon_id)

    def get_icon(self, term: str) -> Optional[Dict[str, Any]]:
        """Get the icon associated with a term.

        Args:
            term: The term to look up

        Returns:
            Icon data if found, None otherwise
        """
        if term in self.associations:
            icon_id = self.associations[term]["icon_id"]
            return self.client.get_icon(icon_id)
        return None

    def suggest_icons(
        self, term: str, limit: int = 5, context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Suggest icons for a term."""
        # Get related terms
        related_terms = self.suggester.get_related_terms(term)

        # Search for icons using both original and related terms
        all_icons = []
        all_icons.extend(self.client.search_icons(term, limit=limit)["icons"])
        for related_term in related_terms[:2]:  # Limit related term searches
            all_icons.extend(
                self.client.search_icons(related_term, limit=limit)["icons"]
            )

        # Score and sort suggestions
        sorted_icons = self.suggester.sort_suggestions(all_icons, term, context)

        # Return top suggestions
        return sorted_icons[:limit]

    def get_custom_mapping(self, term: str) -> Optional[str]:
        """Get any custom mapping for a term."""
        if term in self.associations:
            metadata = self.associations[term].get("metadata", {})
            mapping: Optional[str] = metadata.get("custom_mapping")
            return mapping
        return None

    def set_custom_mapping(self, term: str, mapping: str) -> None:
        """Set a custom mapping for a term."""
        if term not in self.associations:
            self.associations[term] = {"metadata": {}, "version": 1}
        self.associations[term]["metadata"]["custom_mapping"] = mapping
        self._save_registry()
