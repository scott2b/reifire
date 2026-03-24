"""Base protocol for icon providers."""

from typing import Dict, Any, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class IconProvider(Protocol):
    """Protocol that all icon providers must implement."""

    @property
    def name(self) -> str:
        """Provider identifier used in source fields (e.g. 'bundled', 'material')."""
        ...

    @property
    def priority(self) -> int:
        """Lower numbers are tried first. Bundled=10, Material=20, NounProject=50, LLM=80."""
        ...

    def is_available(self) -> bool:
        """Whether this provider is currently configured and usable."""
        ...

    def search(self, term: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for icons matching a term.

        Returns list of dicts, each with at minimum:
          - 'name': str
          - 'source': str (matches self.name)
          - 'image': str (URL, data URI, or file path)
        Optional keys: 'id', 'attribution', 'tags', 'metadata'
        """
        ...

    def get_icon(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get a specific icon by its provider-specific identifier.

        Returns same dict shape as search results, or None.
        """
        ...
