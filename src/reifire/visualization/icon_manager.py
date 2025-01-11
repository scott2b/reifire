"""Icon management for visualizations."""

from typing import Dict, Any, Optional
from .nounproject import NounProjectClient
from reifire.icon_registry import IconRegistry
from .material_icons import MaterialIconProvider
from .color_swatch import ColorSwatchGenerator
import base64


class IconManager:
    """Manages icon fetching and registration for visualizations."""

    # Generic fallback icons for different types
    FALLBACK_ICONS = {
        "default": "https://raw.githubusercontent.com/primer/octicons/main/icons/dot-24.svg",
        "object": "https://raw.githubusercontent.com/primer/octicons/main/icons/package-24.svg",
        "modifier": "https://raw.githubusercontent.com/primer/octicons/main/icons/gear-24.svg",
        "type": "https://raw.githubusercontent.com/primer/octicons/main/icons/file-code-24.svg",
        "artifact": "https://raw.githubusercontent.com/primer/octicons/main/icons/file-24.svg",
        "attribute": (
            "https://raw.githubusercontent.com/primer/octicons/main/icons/list-unordered-24.svg"
        ),
        "alternative": (
            "https://raw.githubusercontent.com/primer/octicons/main/icons/git-branch-24.svg"
        ),
        # Add more specific fallbacks for UI components
        "ui_component": (
            "https://raw.githubusercontent.com/primer/octicons/main/icons/browser-24.svg"
        ),
        "form_element": "https://raw.githubusercontent.com/primer/octicons/main/icons/form-24.svg",
        "navigation": (
            "https://raw.githubusercontent.com/primer/octicons/main/icons/navigation-24.svg"
        ),
        "data_display": "https://raw.githubusercontent.com/primer/octicons/main/icons/graph-24.svg",
        "feedback": "https://raw.githubusercontent.com/primer/octicons/main/icons/comment-24.svg",
        "layout": "https://raw.githubusercontent.com/primer/octicons/main/icons/layout-24.svg",
        # Add more specific fallbacks for technical components
        "api": "https://raw.githubusercontent.com/primer/octicons/main/icons/api-24.svg",
        "database": "https://raw.githubusercontent.com/primer/octicons/main/icons/database-24.svg",
        "security": (
            "https://raw.githubusercontent.com/primer/octicons/main/icons/shield-lock-24.svg"
        ),
        "analytics": "https://raw.githubusercontent.com/primer/octicons/main/icons/graph-24.svg",
        "deployment": "https://raw.githubusercontent.com/primer/octicons/main/icons/rocket-24.svg",
    }

    # Component type categorization
    COMPONENT_CATEGORIES = {
        "ui_component": [
            "button",
            "input",
            "select",
            "checkbox",
            "radio",
            "slider",
            "switch",
            "date",
            "time",
            "color",
        ],
        "form_element": ["form", "field", "label", "textarea", "validation", "submit"],
        "navigation": ["menu", "nav", "sidebar", "breadcrumb", "pagination", "tabs"],
        "data_display": ["table", "list", "grid", "chart", "graph", "tree", "timeline"],
        "feedback": [
            "alert",
            "toast",
            "notification",
            "progress",
            "spinner",
            "loading",
        ],
        "layout": [
            "container",
            "row",
            "column",
            "card",
            "panel",
            "section",
            "header",
            "footer",
        ],
        "api": ["endpoint", "route", "request", "response", "client", "server"],
        "database": ["query", "schema", "model", "migration", "index"],
        "security": ["auth", "permission", "role", "token", "encryption"],
        "analytics": ["metric", "report", "dashboard", "tracking", "monitor"],
        "deployment": ["build", "release", "version", "environment", "config"],
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
        self.material_provider = MaterialIconProvider()

    def _get_component_category(self, term: str) -> str:
        """Determine the category of a component based on its name.

        Args:
            term: The term to categorize

        Returns:
            The category name for the term
        """
        normalized = term.lower()
        for category, terms in self.COMPONENT_CATEGORIES.items():
            if any(t in normalized for t in terms):
                return category
        return "default"

    def get_visualization_properties(self, obj: Dict[str, Any]) -> dict[str, Any]:
        """Get visualization properties for an object."""
        # If visualization properties are already specified, use those
        if "visualization" in obj:
            vis_props = obj["visualization"]
            if not isinstance(vis_props, dict):
                raise ValueError("Visualization properties must be a dictionary")

            # Handle color swatches
            if vis_props.get("source") == "colors":
                print(f"  Generating color swatches for: {vis_props.get('name', '')}")
                colors = vis_props["name"].split("-")
                swatches = ColorSwatchGenerator.generate_swatches(colors)

                # Convert SVG strings to data URLs
                data_urls = []
                for swatch in swatches:
                    b64 = base64.b64encode(swatch.encode()).decode()
                    data_urls.append(f"data:image/svg+xml;base64,{b64}")

                return {
                    "images": data_urls,
                    "source": "colors",
                    "name": vis_props.get("name", ""),
                }

            # Handle existing icon sources
            if "name" in vis_props and "source" in vis_props:
                result: dict[str, Any] = {
                    "name": vis_props["name"],
                    "source": vis_props["source"],
                }

                if vis_props["source"] == "nounproject":
                    print(
                        f"  Noun Project icon specified with name: {vis_props['name']}"
                    )
                    icon_url = self._get_or_fetch_icon(vis_props["name"])
                    if icon_url:
                        print(f"  Updated placeholder with real icon URL: {icon_url}")
                        result["image"] = icon_url
                    else:
                        print("  Using fallback icon for failed Noun Project fetch")
                        category = self._get_component_category(vis_props["name"])
                        result["image"] = self.FALLBACK_ICONS.get(
                            category, self.FALLBACK_ICONS["default"]
                        )
                elif vis_props["source"] in ["openai", "custom"]:
                    print(
                        "  Using fallback icon for {source} source: "
                        "{fallback}".format(
                            source=vis_props["source"],
                            fallback=self.FALLBACK_ICONS["default"],
                        )
                    )
                    result["image"] = self.FALLBACK_ICONS["default"]
                return result
            return dict(vis_props)

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
            return {"image": self.FALLBACK_ICONS["default"], "source": "fallback"}

        print(f"  Attempting to fetch icon for: {icon_name}")
        icon_url = self._get_or_fetch_icon(icon_name)
        if icon_url:
            print(f"  Successfully got icon URL: {icon_url}")
            source = "material" if icon_url.startswith("/") else "nounproject"
            return {"image": icon_url, "name": icon_name, "source": source}

        print("  No icon found or fetched, using fallback")
        category = self._get_component_category(icon_name)
        component_type = obj.get("type", "default").lower()
        fallback_url = self.FALLBACK_ICONS.get(
            category,
            self.FALLBACK_ICONS.get(component_type, self.FALLBACK_ICONS["default"]),
        )
        return {"image": fallback_url, "name": icon_name, "source": "fallback"}

    def _get_or_fetch_icon(self, term: str) -> Optional[str]:
        """Get an icon from the registry or fetch it from available sources.

        Args:
            term: The term to get or fetch an icon for

        Returns:
            The URL or path of the icon if found or fetched, None otherwise
        """
        print(f"  Looking up icon for term: {term}")

        # Check registry first
        icon_url = self.icon_registry.get_icon(term)
        if icon_url:
            print(f"  Found icon in registry: {icon_url}")
            return icon_url

        # Try Material Design Icons if available
        if self.material_provider.is_available():
            print("  Checking Material Design Icons...")
            if icon_path := self.material_provider.get_icon_path(term):
                print(f"  Found Material Design icon: {icon_path}")
                self.icon_registry.register_icon(term, icon_path)
                return icon_path

        print(
            "  Icon not found in Material Design Icons, "
            "attempting to fetch from Noun Project..."
        )
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

    def get_icon_data(
        self, icon_name: str, icon_type: Optional[str] = None
    ) -> dict[str, Any]:
        """Get icon data for a given icon name and type.

        Args:
            icon_name: The name of the icon to retrieve
            icon_type: The type of icon to retrieve. If not specified, will search all
                registered icon types.

        Returns:
            A dictionary containing the icon data
        """
        if icon_type is not None:
            if icon_type not in ["material", "nounproject"]:
                raise ValueError(
                    f"Icon type {icon_type} not found. Available types: material, nounproject"
                )
            if icon_type == "material" and self.material_provider.is_available():
                return self.material_provider.get_icon_data(icon_name)
            elif icon_type == "nounproject":
                icon_url = self._get_or_fetch_icon(icon_name)
                if icon_url:
                    return {
                        "image": icon_url,
                        "name": icon_name,
                        "source": "nounproject",
                    }
            raise ValueError(f"Icon {icon_name} not found in {icon_type}")

        # Try material icons first if available
        if self.material_provider.is_available():
            try:
                return self.material_provider.get_icon_data(icon_name)
            except ValueError:
                pass

        # Try noun project
        icon_url = self._get_or_fetch_icon(icon_name)
        if icon_url:
            return {"image": icon_url, "name": icon_name, "source": "nounproject"}

        raise ValueError(f"Icon {icon_name} not found in any available icon types")
