"""Noun Project provider adapter."""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class NounProjectProviderAdapter:
    """Wraps NounProjectClient to conform to the IconProvider protocol."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
    ) -> None:
        self._client = None
        key = api_key or os.environ.get("NOUNPROJECT_API_KEY") or os.environ.get("NOUN_PROJECT_KEY")
        secret = api_secret or os.environ.get("NOUNPROJECT_API_SECRET") or os.environ.get("NOUN_PROJECT_SECRET")

        if key and secret:
            try:
                from reifire.visualization.nounproject import NounProjectClient

                self._client = NounProjectClient(key, secret)
            except Exception:
                logger.exception("Failed to initialize Noun Project client")

    @property
    def name(self) -> str:
        return "nounproject"

    @property
    def priority(self) -> int:
        return 50

    def is_available(self) -> bool:
        return self._client is not None

    def search(self, term: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search Noun Project for icons matching a term."""
        if self._client is None:
            return []

        try:
            results = self._client.search_icons(term, limit=limit)
            icons = results.get("icons", [])
            return [
                {
                    "id": str(icon.get("id", "")),
                    "name": icon.get("term", term),
                    "source": self.name,
                    "image": icon.get("thumbnail_url") or icon.get("preview_url", ""),
                    "attribution": f"Created by {icon.get('uploader', {}).get('name', 'Unknown')} from the Noun Project",
                    "tags": [t.get("slug", "") for t in icon.get("tags", []) if isinstance(t, dict)],
                }
                for icon in icons
                if icon.get("thumbnail_url") or icon.get("preview_url")
            ]
        except Exception:
            logger.exception("Noun Project search failed for '%s'", term)
            return []

    def get_icon(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get a Noun Project icon by ID."""
        if self._client is None:
            return None

        try:
            icon = self._client.get_icon(identifier)
            if not icon or "error" in icon:
                return None
            return {
                "id": str(icon.get("id", identifier)),
                "name": icon.get("term", ""),
                "source": self.name,
                "image": icon.get("thumbnail_url") or icon.get("preview_url", ""),
                "attribution": f"Created by {icon.get('uploader', {}).get('name', 'Unknown')} from the Noun Project",
            }
        except Exception:
            logger.exception("Noun Project get_icon failed for '%s'", identifier)
            return None
