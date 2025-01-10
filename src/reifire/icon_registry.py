"""Registry for managing icons."""

from typing import Dict, Optional
import json
from pathlib import Path


class IconRegistry:
    """Registry for managing icons."""

    def __init__(self, storage_file: Optional[Path] = None) -> None:
        """Initialize the icon registry.

        Args:
            storage_file: Optional path to a JSON file for persistent storage
        """
        self._icons: Dict[str, str] = {}
        self.storage_file = (
            storage_file or Path.home() / ".reifire" / "icon_registry.json"
        )
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_icons()

    def _load_icons(self) -> None:
        """Load icons from storage file if it exists."""
        if self.storage_file.exists():
            try:
                self._icons = json.loads(self.storage_file.read_text())
                print(f"Loaded {len(self._icons)} icons from registry")
            except json.JSONDecodeError:
                print("Invalid icon registry file, starting fresh")
                self._icons = {}
        else:
            print("No existing icon registry found, starting fresh")

    def _save_icons(self) -> None:
        """Save icons to storage file."""
        try:
            self.storage_file.write_text(json.dumps(self._icons, indent=2))
            print(f"Saved {len(self._icons)} icons to registry")
        except Exception as e:
            print(f"Failed to save icon registry: {e}")

    def register_icon(self, name: str, icon_url: str) -> None:
        """Register an icon in the registry.

        Args:
            name: The name to register the icon under
            icon_url: The URL of the icon
        """
        print(f"Registering icon '{name}' with URL: {icon_url}")
        self._icons[name] = icon_url
        self._save_icons()

    def get_icon(self, name: str) -> Optional[str]:
        """Get an icon from the registry.

        Args:
            name: The name of the icon to get

        Returns:
            The URL of the icon if found, None otherwise
        """
        icon_url = self._icons.get(name)
        if icon_url:
            print(f"Found icon '{name}' in registry: {icon_url}")
        else:
            print(f"Icon '{name}' not found in registry")
        return icon_url

    def clear(self) -> None:
        """Clear all icons from the registry."""
        self._icons = {}
        if self.storage_file.exists():
            self.storage_file.unlink()
        print("Cleared icon registry")
