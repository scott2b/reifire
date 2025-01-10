"""Icon management for visualizations."""

from typing import Dict, Any, Optional
from .nounproject import NounProjectClient
from reifire.icon_registry import IconRegistry


class IconManager:
    """Manages icon fetching and registration for visualizations."""

    # Generic fallback icons for different types
    FALLBACK_ICONS = {
        "default": "https://raw.githubusercontent.com/primer/octicons/main/icons/dot-24.svg",
        "object": "https://raw.githubusercontent.com/primer/octicons/main/icons/package-24.svg",
        "modifier": "https://raw.githubusercontent.com/primer/octicons/main/icons/gear-24.svg",
        "type": "https://raw.githubusercontent.com/primer/octicons/main/icons/file-code-24.svg",
        "artifact": "https://raw.githubusercontent.com/primer/octicons/main/icons/file-24.svg",
        "attribute": "https://raw.githubusercontent.com/primer/octicons/main/icons/list-unordered-24.svg",
        "alternative": "https://raw.githubusercontent.com/primer/octicons/main/icons/git-branch-24.svg",
        "relationship": "https://raw.githubusercontent.com/primer/octicons/main/icons/link-24.svg",
    }

    def __init__(
        self, icon_registry: IconRegistry, noun_project_client: NounProjectClient
    ):
        """Initialize the icon manager.

        Args:
            icon_registry: The icon registry to use for storing and retrieving icons
            noun_project_client: The Noun Project client for fetching icons
        """
        self.icon_registry = icon_registry
        self.noun_project_client = noun_project_client

    def get_visualization_properties(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Get visualization properties for an object, including fetching icons if needed.

        Args:
            obj: The object to get visualization properties for

        Returns:
            A dictionary of visualization properties including icon information
        """
        print(
            f"\nProcessing visualization for: {obj.get('name', obj.get('type', 'unnamed'))}"
        )

        # If visualization properties are already set, try to fetch a real icon
        if "visualization" in obj and obj["visualization"]:
            vis_props = dict(
                obj["visualization"]
            )  # Create a copy to avoid modifying original
            print(f"  Found existing visualization properties: {vis_props}")

            if vis_props.get("source") == "nounproject":
                # Try to get a real icon for the name
                icon_name = vis_props.get("name", "")
                print(f"  Noun Project icon specified with name: {icon_name}")
                if icon_name:
                    icon_url = self._get_or_fetch_icon(icon_name)
                    if icon_url:
                        print(f"  Updated placeholder with real icon URL: {icon_url}")
                        vis_props["image"] = icon_url
                    else:
                        # Use fallback icon based on component type
                        component_type = obj.get("type", "default").lower()
                        fallback_url = self.FALLBACK_ICONS.get(component_type, self.FALLBACK_ICONS["default"])
                        print(f"  Using fallback icon: {fallback_url}")
                        vis_props["image"] = fallback_url
            return vis_props

        # If an icon is specified directly, use that
        if "icon" in obj:
            print(f"  Using directly specified icon: {obj['icon']}")
            return {
                "image": obj["icon"],
                "name": obj.get("name", ""),
                "source": "direct",
            }

        # Try to fetch an icon based on the object's name or type
        icon_name = obj.get("name", "") or obj.get("type", "")
        if not icon_name:
            print("  No name or type found to fetch icon for")
            # Use default fallback icon
            return {"image": self.FALLBACK_ICONS["default"], "source": "fallback"}

        print(f"  Attempting to fetch icon for: {icon_name}")
        # Try to get or fetch an icon
        icon_url = self._get_or_fetch_icon(icon_name)
        if icon_url:
            print(f"  Successfully got icon URL: {icon_url}")
            return {"image": icon_url, "name": icon_name, "source": "nounproject"}

        print("  No icon found or fetched, using fallback")
        # Use fallback icon based on component type
        component_type = obj.get("type", "default").lower()
        fallback_url = self.FALLBACK_ICONS.get(component_type, self.FALLBACK_ICONS["default"])
        return {"image": fallback_url, "name": icon_name, "source": "fallback"}

    def _get_or_fetch_icon(self, term: str) -> Optional[str]:
        """Get an icon from the registry or fetch it from the Noun Project.

        Args:
            term: The term to get or fetch an icon for

        Returns:
            The URL of the icon if found or fetched, None otherwise
        """
        print(f"  Looking up icon for term: {term}")

        # Check registry first
        icon_url = self.icon_registry.get_icon(term)
        if icon_url:
            print(f"  Found icon in registry: {icon_url}")
            return icon_url

        print("  Icon not in registry, attempting to fetch from Noun Project...")
        # Try to fetch from Noun Project
        try:
            # Search for icons matching the term
            print(f"  Searching Noun Project for: {term}")
            search_results = self.noun_project_client.search_icons(term, limit=1)

            if not search_results.get("icons"):
                print("  No icons found in search results")
                return None

            # Get the first icon's details
            icon_data = search_results["icons"][0]
            icon_id = str(icon_data["id"])  # Ensure icon_id is a string
            print(f"  Found icon with ID: {icon_id}")

            # Use thumbnail_url directly from search results
            preview_url = icon_data.get("thumbnail_url")
            if not isinstance(preview_url, str):
                print("  Icon data missing thumbnail URL")
                return None

            print(f"  Got icon URL: {preview_url}")
            print("  Registering icon for future use")
            self.icon_registry.register_icon(term, preview_url)
            return preview_url

        except Exception as e:
            print(f"  Error fetching icon: {str(e)}")
            return None
