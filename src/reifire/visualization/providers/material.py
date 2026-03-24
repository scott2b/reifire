"""Material Design Icons provider adapter."""

import base64
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from reifire.visualization.material_icons import MaterialIconProvider

logger = logging.getLogger(__name__)


class MaterialIconProviderAdapter:
    """Wraps MaterialIconProvider to conform to the IconProvider protocol."""

    def __init__(self) -> None:
        self._provider = MaterialIconProvider()

    @property
    def name(self) -> str:
        return "material"

    @property
    def priority(self) -> int:
        return 20

    def is_available(self) -> bool:
        return self._provider.is_available()

    def _path_to_data_uri(self, icon_path: str) -> str:
        """Convert a local file path to a data URI."""
        path = Path(icon_path)
        if not path.exists():
            return icon_path
        content = path.read_bytes()
        b64 = base64.b64encode(content).decode()
        suffix = path.suffix.lstrip(".")
        mime = f"image/{suffix}" if suffix != "svg" else "image/svg+xml"
        return f"data:{mime};base64,{b64}"

    def search(self, term: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search Material Design Icons for a term."""
        if not self.is_available():
            return []

        icon_path = self._provider.get_icon_path(term)
        if not icon_path:
            return []

        return [{
            "id": term,
            "name": term,
            "source": self.name,
            "image": self._path_to_data_uri(icon_path),
        }]

    def get_icon(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get a Material Design icon by name."""
        if not self.is_available():
            return None

        try:
            data = self._provider.get_icon_data(identifier)
            return {
                "id": identifier,
                "name": data["name"],
                "source": self.name,
                "image": self._path_to_data_uri(data["path"]),
            }
        except ValueError:
            return None
