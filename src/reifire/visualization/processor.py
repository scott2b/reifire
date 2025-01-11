"""Processor for converting JSON data into visualization components."""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from .icon_manager import IconManager


@dataclass
class VisualizationComponent:
    """Component in the visualization."""

    id: str
    type: str
    label: str
    x: float
    y: float
    width: float
    height: float
    properties: Dict[str, Any]


@dataclass
class VisualizationConnection:
    """Connection between components in the visualization."""

    source: str
    target: str
    type: str
    properties: Dict[str, Any]


class VisualizationProcessor:
    """Processes JSON data into visualization components."""

    def __init__(self, icon_manager: Optional[IconManager] = None) -> None:
        """Initialize the visualization processor.

        Args:
            icon_manager: Optional IconManager instance for handling icons
        """
        self.components: List[VisualizationComponent] = []
        self.connections: List[VisualizationConnection] = []
        self.current_y = 0  # Start at 0 for test compatibility
        self.spacing = 100
        self.x_offset = 250  # Increased horizontal spacing for better readability
        self.level_offset = 50  # Additional offset for nested components
        self.base_x = 50  # Base x position for the leftmost components
        self.icon_manager = icon_manager

    def process_json(
        self, data: Dict[str, Any]
    ) -> Tuple[List[VisualizationComponent], List[VisualizationConnection]]:
        """Process JSON data into visualization components and connections."""
        self.components = []
        self.connections = []
        self.current_y = 0  # Reset to 0 for test compatibility

        # Process main object
        main_id = self._add_object_component(
            data.get("object", {}), "object", x_offset=self.base_x
        )

        # Process modifiers if present
        if "object" in data and "modifiers" in data["object"]:
            for modifier in data["object"]["modifiers"]:
                mod_id = self._add_modifier_component(
                    modifier, x_offset=self.base_x + self.x_offset
                )
                self._add_connection(
                    main_id, mod_id, "modifier", modifier.get("properties", {})
                )

        # Process type
        if "type" in data:
            type_id = self._add_object_component(
                data["type"], "type", x_offset=self.base_x + self.x_offset
            )
            self._add_connection(
                main_id, type_id, "type", data["type"].get("properties", {})
            )

        # Process artifact
        if "artifact" in data:
            artifact_id = self._add_object_component(
                data["artifact"], "artifact", x_offset=self.base_x + self.x_offset * 2
            )
            self._add_connection(
                main_id, artifact_id, "artifact", data["artifact"].get("properties", {})
            )

            # Process attributes
            if "attributes" in data["artifact"]:
                for attr in data["artifact"]["attributes"]:
                    attr_id = self._add_attribute_component(
                        attr, x_offset=self.base_x + self.x_offset * 2
                    )
                    self._add_connection(
                        artifact_id, attr_id, "attribute", attr.get("properties", {})
                    )

                    # Process alternatives
                    if "alternatives" in attr:
                        for alt in attr["alternatives"]:
                            alt_id = self._add_attribute_component(
                                alt,
                                is_alternative=True,
                                x_offset=self.base_x + self.x_offset * 3,
                            )
                            self._add_connection(
                                attr_id,
                                alt_id,
                                "alternative",
                                alt.get("properties", {}),
                            )

            # Process relationships
            if "relationships" in data["artifact"]:
                for rel in data["artifact"]["relationships"]:
                    rel_id = self._add_relationship_component(rel)
                    # Add connections to source and target
                    if "source" in rel and "target" in rel:
                        self._add_connection(rel["source"], rel_id, "source", {})
                        self._add_connection(rel_id, rel["target"], "target", {})

        return self.components, self.connections

    def _add_object_component(
        self, obj: Dict[str, Any], type_name: str, x_offset: float = 0
    ) -> str:
        """Add a component for an object."""
        component_id = f"{type_name}_{len(self.components)}"

        # Get visualization properties using IconManager if available
        vis_props = {}
        if self.icon_manager:
            vis_props = self.icon_manager.get_visualization_properties(obj)
        elif "visualization" in obj:
            vis_props = obj.get("visualization", {})
        elif "icon" in obj:
            vis_props = {"image": obj["icon"], "name": obj.get("name", type_name)}

        # Create component with proper properties
        component = VisualizationComponent(
            id=component_id,
            type=type_name,
            label=obj.get("name", type_name),
            x=x_offset,
            y=self.current_y,
            width=200,  # Increased width for better readability
            height=60,  # Increased height for better spacing
            properties={
                "visualization": vis_props,
                **{
                    k: v
                    for k, v in obj.items()
                    if k
                    not in [
                        "name",
                        "visualization",
                        "icon",
                        "modifiers",
                        "attributes",
                        "relationships",
                    ]
                },
            },
        )

        self.components.append(component)
        self.current_y += self.spacing
        return component_id

    def _add_modifier_component(
        self, modifier: Dict[str, Any], x_offset: float = 0
    ) -> str:
        """Add a component for a modifier."""
        component_id = f"mod_{len(self.components)}"

        # Get visualization properties using IconManager if available
        vis_props = {}
        if self.icon_manager:
            vis_props = self.icon_manager.get_visualization_properties(modifier)
        elif "visualization" in modifier:
            vis_props = modifier.get("visualization", {})
        elif "icon" in modifier:
            vis_props = {
                "image": modifier["icon"],
                "name": modifier.get("name", "Modifier"),
            }

        # Create label with name and value
        label = f"{modifier.get('name', 'Modifier')}"
        if "value" in modifier and modifier["value"] is not None:
            label += f": {modifier['value']}"

        # Create component
        component = VisualizationComponent(
            id=component_id,
            type="modifier",
            label=label,
            x=x_offset,
            y=self.current_y,
            width=180,
            height=50,
            properties={
                "visualization": vis_props,
                **{
                    k: v
                    for k, v in modifier.items()
                    if k
                    not in ["name", "value", "visualization", "icon", "alternatives"]
                },
            },
        )

        self.components.append(component)
        self.current_y += self.spacing
        return component_id

    def _add_attribute_component(
        self, attr: Dict[str, Any], is_alternative: bool = False, x_offset: float = 0
    ) -> str:
        """Add a component for an attribute."""
        component_id = f"attr_{len(self.components)}"

        # Get visualization properties using IconManager if available
        vis_props = {}
        if self.icon_manager:
            vis_props = self.icon_manager.get_visualization_properties(attr)
        elif "visualization" in attr:
            vis_props = attr.get("visualization", {})
        elif "icon" in attr:
            vis_props = {
                "image": attr["icon"],
                "name": attr.get("name", "Attribute"),
            }

        # Create label with name and value
        label = f"{attr.get('name', 'Attribute')}"
        if "value" in attr and attr["value"] is not None:
            label += f": {attr['value']}"

        # Create component
        component = VisualizationComponent(
            id=component_id,
            type="alternative" if is_alternative else "attribute",
            label=label,
            x=x_offset,
            y=self.current_y,
            width=180,
            height=50,
            properties={
                "visualization": vis_props,
                **{
                    k: v
                    for k, v in attr.items()
                    if k
                    not in ["name", "value", "visualization", "icon", "alternatives"]
                },
            },
        )

        self.components.append(component)
        self.current_y += self.spacing

        # Special handling for color scheme attributes
        if attr.get("name") == "color scheme" and "visualization" in attr:
            vis = attr["visualization"]
            if vis.get("source") == "colors" and vis.get("name"):
                colors = vis["name"].split("-")
                # Create individual color nodes
                for color in colors:
                    color_id = f"color_{len(self.components)}"
                    color_component = VisualizationComponent(
                        id=color_id,
                        type="color",
                        label=color,
                        x=x_offset + self.x_offset,
                        y=self.current_y,
                        width=120,
                        height=50,
                        properties={
                            "visualization": {
                                "source": "colors",
                                "name": color,
                                "images": (
                                    [vis_props.get("images", [])[colors.index(color)]]
                                    if vis_props.get("images")
                                    else None
                                ),
                            }
                        },
                    )
                    self.components.append(color_component)
                    # Add composition connection
                    self._add_connection(component_id, color_id, "composition", {})
                    self.current_y += self.spacing

        return component_id

    def _add_relationship_component(self, rel: Dict[str, Any]) -> str:
        """Add a component for a relationship."""
        component_id = f"rel_{len(self.components)}"

        # Get visualization properties using IconManager if available
        vis_props = {}
        if self.icon_manager:
            vis_props = self.icon_manager.get_visualization_properties(rel)
        elif "visualization" in rel:
            vis_props = rel.get("visualization", {})
        elif "icon" in rel:
            vis_props = {"image": rel["icon"], "name": rel.get("name", "Relationship")}

        # Create label with source and target
        label = f"{rel.get('type', 'Relationship')}"
        if "source" in rel and "target" in rel:
            label = f"{label}: {rel['source']} -> {rel['target']}"

        # Create component
        component = VisualizationComponent(
            id=component_id,
            type="relationship",
            label=label,
            x=self.base_x
            + self.x_offset * 2,  # Position relationships at same level as artifacts
            y=self.current_y,
            width=180,
            height=50,
            properties={
                "visualization": vis_props,
                **{
                    k: v
                    for k, v in rel.items()
                    if k not in ["type", "visualization", "icon", "source", "target"]
                },
            },
        )

        self.components.append(component)
        self.current_y += self.spacing
        return component_id

    def _add_connection(
        self,
        source_id: str,
        target_id: str,
        connection_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a connection between components."""
        if properties is None:
            properties = {}

        connection = VisualizationConnection(
            source=source_id,
            target=target_id,
            type=connection_type,
            properties=properties,
        )
        self.connections.append(connection)
