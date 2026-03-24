"""Icon management for visualizations."""

import logging
from typing import Dict, Any, Optional
from reifire.icon_registry import IconRegistry
from .color_swatch import ColorSwatchGenerator
import base64

logger = logging.getLogger(__name__)


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
        self,
        icon_registry: IconRegistry,
        provider_chain: Optional[Any] = None,
    ) -> None:
        """Initialize the icon manager.

        Args:
            icon_registry: The icon registry to use for storing and retrieving icons
            provider_chain: ProviderChain for fetching icons. If None, creates a default chain.
        """
        self.icon_registry = icon_registry
        if provider_chain is None:
            from .providers.chain import ProviderChain

            provider_chain = ProviderChain()
        self.provider_chain = provider_chain

    def _get_component_category(self, term: str) -> str:
        """Determine the category of a component based on its name."""
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
                logger.debug("Generating color swatches for: %s", vis_props.get("name", ""))
                colors = vis_props["name"].split("-")
                swatches = ColorSwatchGenerator.generate_swatches(colors)

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

                # For any provider-backed source, try to resolve the icon
                if vis_props["source"] not in ["openai", "custom", "colors"]:
                    icon_image = self._resolve_icon(vis_props["name"])
                    if icon_image:
                        result["image"] = icon_image
                    else:
                        category = self._get_component_category(vis_props["name"])
                        result["image"] = self.FALLBACK_ICONS.get(
                            category, self.FALLBACK_ICONS["default"]
                        )
                elif vis_props["source"] in ["openai", "custom"]:
                    result["image"] = self.FALLBACK_ICONS["default"]
                return result
            return dict(vis_props)

        # If an icon is specified directly, use that
        if "icon" in obj:
            return {
                "image": obj["icon"],
                "name": obj.get("name", ""),
                "source": "direct",
            }

        # Try to fetch an icon based on the object's name or type
        icon_name = obj.get("name", "") or obj.get("type", "")
        if not icon_name:
            return {"image": self.FALLBACK_ICONS["default"], "source": "fallback"}

        icon_image = self._resolve_icon(icon_name)
        if icon_image:
            return {"image": icon_image, "name": icon_name, "source": "provider"}

        category = self._get_component_category(icon_name)
        component_type = obj.get("type", "default").lower()
        fallback_url = self.FALLBACK_ICONS.get(
            category,
            self.FALLBACK_ICONS.get(component_type, self.FALLBACK_ICONS["default"]),
        )
        return {"image": fallback_url, "name": icon_name, "source": "fallback"}

    def _resolve_icon(self, term: str) -> Optional[str]:
        """Resolve an icon for a term using the registry cache then provider chain.

        Args:
            term: The term to resolve an icon for

        Returns:
            The image URL/data URI if found, None otherwise
        """
        # Check registry cache first
        icon_url = self.icon_registry.get_icon(term)
        if icon_url:
            return icon_url

        # Search provider chain
        results = self.provider_chain.search(term, limit=1)
        if results:
            image = results[0].get("image", "")
            if image:
                self.icon_registry.register_icon(term, image)
                return image

        return None

    def get_icon_data(
        self, icon_name: str, icon_type: Optional[str] = None
    ) -> dict[str, Any]:
        """Get icon data for a given icon name and optional provider type.

        Args:
            icon_name: The name of the icon to retrieve
            icon_type: Optional provider name to search (e.g. 'material', 'bundled')

        Returns:
            A dictionary containing the icon data
        """
        if icon_type is not None:
            result = self.provider_chain.get_icon(icon_type, icon_name)
            if result:
                return result
            # Try searching if get_icon didn't find it
            results = self.provider_chain.search(icon_name, limit=1)
            provider_results = [r for r in results if r.get("source") == icon_type]
            if provider_results:
                return provider_results[0]
            raise ValueError(f"Icon {icon_name} not found in {icon_type}")

        # Search all providers
        results = self.provider_chain.search(icon_name, limit=1)
        if results:
            return results[0]

        raise ValueError(f"Icon {icon_name} not found in any available provider")
