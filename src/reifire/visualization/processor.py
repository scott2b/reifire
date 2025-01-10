"""Processor for converting JSON data into visualization components."""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import json

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

    def __init__(self):
        self.components: List[VisualizationComponent] = []
        self.connections: List[VisualizationConnection] = []
        self.current_y = 50  # Start with some padding
        self.spacing = 100
        self.x_offset = 250  # Increased horizontal spacing for better readability
        self.level_offset = 50  # Additional offset for nested components

    def process_json(self, data: Dict[str, Any]) -> Tuple[List[VisualizationComponent], List[VisualizationConnection]]:
        """Process JSON data into visualization components and connections."""
        self.components = []
        self.connections = []
        self.current_y = 50

        # Process main object
        main_id = self._add_object_component(data.get("object", {}), "object")

        # Process modifiers if present
        if "object" in data and "modifiers" in data["object"]:
            for modifier in data["object"]["modifiers"]:
                mod_id = self._add_modifier_component(modifier, x_offset=self.x_offset)
                self._add_connection(main_id, mod_id, "modifier", modifier.get("properties", {}))

        # Process type
        if "type" in data:
            type_id = self._add_object_component(data["type"], "type", x_offset=self.x_offset)
            self._add_connection(main_id, type_id, "type", data["type"].get("properties", {}))

        # Process artifact
        if "artifact" in data:
            artifact_id = self._add_object_component(data["artifact"], "artifact", x_offset=self.x_offset * 2)
            self._add_connection(main_id, artifact_id, "artifact", data["artifact"].get("properties", {}))

            # Process attributes
            if "attributes" in data["artifact"]:
                for attr in data["artifact"]["attributes"]:
                    attr_id = self._add_attribute_component(attr, x_offset=self.x_offset * 2)
                    self._add_connection(artifact_id, attr_id, "attribute", attr.get("properties", {}))

                    # Process alternatives
                    if "alternatives" in attr:
                        for alt in attr["alternatives"]:
                            alt_id = self._add_attribute_component(alt, is_alternative=True, x_offset=self.x_offset * 3)
                            self._add_connection(attr_id, alt_id, "alternative", alt.get("properties", {}))

            # Process relationships
            if "relationships" in data["artifact"]:
                for rel in data["artifact"]["relationships"]:
                    rel_id = self._add_relationship_component(rel, x_offset=self.x_offset * 2)
                    self._add_connection(artifact_id, rel_id, "relationship", rel.get("properties", {}))

                    # Add actual relationship connection if source/target specified
                    if "source" in rel and "target" in rel:
                        self._add_connection(rel_id, f"rel_{rel['source']}_{rel['target']}", rel["type"], rel.get("properties", {}))

        return self.components, self.connections

    def _add_object_component(self, obj: Dict[str, Any], type_name: str, x_offset: float = 0) -> str:
        """Add a component for an object."""
        component_id = f"{type_name}_{len(self.components)}"
        
        # Extract visualization properties
        vis_props = obj.get("visualization", {})
        if not vis_props and "icon" in obj:
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
                **{k: v for k, v in obj.items() if k not in ["name", "visualization", "icon", "modifiers", "attributes", "relationships"]}
            }
        )
        
        self.components.append(component)
        self.current_y += self.spacing
        return component_id

    def _add_modifier_component(self, modifier: Dict[str, Any], x_offset: float = 0) -> str:
        """Add a component for a modifier."""
        component_id = f"mod_{len(self.components)}"
        
        # Extract visualization properties
        vis_props = modifier.get("visualization", {})
        if not vis_props and "icon" in modifier:
            vis_props = {"image": modifier["icon"], "name": modifier.get("name", "Modifier")}
        
        # Create label with name and value
        label = f"{modifier.get('name', 'Modifier')}"
        if "value" in modifier and modifier["value"] is not None:
            label += f": {modifier['value']}"
        
        # Create component
        component = VisualizationComponent(
            id=component_id,
            type="modifier",
            label=label,
            x=x_offset + self.x_offset,
            y=self.current_y,
            width=180,
            height=50,
            properties={
                "visualization": vis_props,
                **{k: v for k, v in modifier.items() if k not in ["name", "value", "visualization", "icon", "alternatives"]}
            }
        )
        
        self.components.append(component)
        self.current_y += self.spacing
        
        # Process alternatives if present
        if "alternatives" in modifier:
            for alt in modifier["alternatives"]:
                alt_id = self._add_modifier_component(alt, x_offset + self.level_offset)
                self._add_connection(component_id, alt_id, "alternative", alt.get("properties", {}))
        
        return component_id

    def _add_attribute_component(self, attr: Dict[str, Any], is_alternative: bool = False, x_offset: float = 0) -> str:
        """Add a component for an attribute."""
        component_id = f"attr_{len(self.components)}"
        
        # Extract visualization properties
        vis_props = attr.get("visualization", {})
        if not vis_props and "icon" in attr:
            vis_props = {"image": attr["icon"], "name": attr.get("name", "Attribute")}
        
        # Create label with name and value
        label = f"{attr.get('name', 'Attribute')}"
        if "value" in attr and attr["value"] is not None:
            label += f": {attr['value']}"
        
        # Create component
        component = VisualizationComponent(
            id=component_id,
            type="attribute" if not is_alternative else "alternative",
            label=label,
            x=x_offset + (self.level_offset if is_alternative else 0),
            y=self.current_y,
            width=180,
            height=50,
            properties={
                "visualization": vis_props,
                **{k: v for k, v in attr.items() if k not in ["name", "value", "visualization", "icon", "alternatives"]}
            }
        )
        
        self.components.append(component)
        if not is_alternative:
            self.current_y += self.spacing
        
        return component_id

    def _add_relationship_component(self, rel: Dict[str, Any], x_offset: float = 0) -> str:
        """Add a component for a relationship."""
        component_id = f"rel_{len(self.components)}"
        
        # Extract visualization properties
        vis_props = rel.get("visualization", {})
        if not vis_props and "icon" in rel:
            vis_props = {"image": rel["icon"], "name": rel.get("type", "Relationship")}
        
        # Create component
        component = VisualizationComponent(
            id=component_id,
            type="relationship",
            label=f"{rel.get('type', 'Relationship')}: {rel.get('source', '')} -> {rel.get('target', '')}",
            x=x_offset,
            y=self.current_y,
            width=250,  # Increased width for relationship labels
            height=50,
            properties={
                "visualization": vis_props,
                **{k: v for k, v in rel.items() if k not in ["type", "source", "target", "visualization", "icon"]}
            }
        )
        
        self.components.append(component)
        self.current_y += self.spacing
        return component_id

    def _add_connection(self, source_id: str, target_id: str, connection_type: str, properties: Dict[str, Any] = None) -> None:
        """Add a connection between components."""
        connection = VisualizationConnection(
            source=source_id,
            target=target_id,
            type=connection_type,
            properties=properties or {}
        )
        self.connections.append(connection) 