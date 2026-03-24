from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from .suggestions import IconSuggester


class IconRegistry:
    """Manages icon associations and metadata for reified concepts."""

    def __init__(
        self,
        provider_chain: Optional[Any] = None,
        registry_path: Optional[Path] = None,
        suggester: Optional[IconSuggester] = None,
    ) -> None:
        """Initialize the registry.

        Args:
            provider_chain: ProviderChain for fetching icons. If None, creates a default chain.
            registry_path: Path to store registry data (defaults to ~/.reifire/icon_registry.json)
            suggester: Suggestion engine for intelligent suggestions
        """
        if provider_chain is None:
            from .providers.chain import ProviderChain

            provider_chain = ProviderChain()
        self.provider_chain = provider_chain
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
            icon_id: The icon identifier (provider-specific)
            metadata: Optional metadata about the association
        """
        self.associations[term] = {
            "icon_id": icon_id,
            "metadata": metadata or {},
            "version": 1,
        }
        self._save_registry()
        self.suggester.record_selection(term, icon_id)

    def get_icon(self, term: str) -> Optional[Dict[str, Any]]:
        """Get the icon associated with a term.

        Args:
            term: The term to look up

        Returns:
            Icon data if found, None otherwise
        """
        if term in self.associations:
            assoc = self.associations[term]
            icon_id = assoc["icon_id"]
            source = assoc.get("metadata", {}).get("source", "")
            if source:
                return self.provider_chain.get_icon(source, icon_id)
            # If no source stored, search by term as fallback
            results = self.provider_chain.search(term, limit=1)
            return results[0] if results else None
        return None

    def suggest_icons(
        self, term: str, limit: int = 5, context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Suggest icons for a term."""
        related_terms = self.suggester.get_related_terms(term)

        # Search all providers for original and related terms
        all_icons = self.provider_chain.search_all(term, limit=limit)
        for related_term in related_terms[:2]:
            all_icons.extend(self.provider_chain.search_all(related_term, limit=limit))

        # Score and sort suggestions
        sorted_icons = self.suggester.sort_suggestions(all_icons, term, context)
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
