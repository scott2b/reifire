"""Factory for creating layout components from reified data structures."""

from typing import Dict, Any, Optional
from .layout import LayoutComponent, ComponentType, Size, Position


class ComponentFactory:
    """Creates layout components from reified data structures."""

    def __init__(self) -> None:
        """Initialize the factory."""
        self.default_icon_size = Size(50, 50)
        self.default_spacing = 20

    def create_from_reified(
        self, data: Dict[str, Any], parent_id: Optional[str] = None
    ) -> LayoutComponent:
        """Create a layout component from a reified data structure."""
        # Extract visualization properties
        visualization = data.get("visualization", {})
        properties = visualization.get("properties", {})

        # Get object data if present
        object_data = data.get("object", {})

        # Determine component type and size
        if object_data:
            component_type = ComponentType.OBJECT
            size = self._get_size_from_properties(properties)

            # Create the component
            component = LayoutComponent(
                id=f"obj_{object_data['name']}",
                type=component_type,
                position=Position(0, 0),
                size=size,
                properties=properties,
            )

            # Process modifiers if present
            if "modifiers" in object_data:
                for modifier in object_data["modifiers"]:
                    modifier_comp = self.create_modifier_component(
                        modifier, component.id
                    )
                    component.children.append(modifier_comp)

            return component

        elif "type" in data:
            component_type = ComponentType.GROUP
            size = self._get_size_from_properties(properties)
        elif "attributes" in data:
            component_type = ComponentType.ATTRIBUTE
            size = self._get_size_from_properties(properties)
        else:
            component_type = ComponentType.ICON
            size = self.default_icon_size

        # Create the component for non-object types
        component = LayoutComponent(
            id=self._generate_id(data),
            type=component_type,
            position=Position(0, 0),
            size=size,
            properties=properties,
        )

        # Process attributes if present
        if "attributes" in data:
            for attr in data["attributes"]:
                attr_comp = self.create_attribute_component(attr, component.id)
                component.children.append(attr_comp)

        # Process relationships if present
        if "relationships" in data:
            for rel in data["relationships"]:
                rel_comp = self.create_relationship_component(rel, component.id)
                component.children.append(rel_comp)

        return component

    def create_modifier_component(
        self, data: Dict[str, Any], parent_id: str
    ) -> LayoutComponent:
        """Create a component for a modifier."""
        visualization = data.get("visualization", {})
        return LayoutComponent(
            id=f"{parent_id}_mod_{data['name']}",
            type=ComponentType.MODIFIER,
            position=Position(0, 0),
            size=self._get_size_from_properties(visualization.get("properties", {})),
            properties={
                "name": data["name"],
                "value": data["value"],
                "visualization": visualization,
            },
        )

    def create_attribute_component(
        self, data: Dict[str, Any], parent_id: str
    ) -> LayoutComponent:
        """Create a component for an attribute."""
        visualization = data.get("visualization", {})
        return LayoutComponent(
            id=f"{parent_id}_attr_{data['name']}",
            type=ComponentType.ATTRIBUTE,
            position=Position(0, 0),
            size=self._get_size_from_properties(visualization.get("properties", {})),
            properties={
                "name": data["name"],
                "value": data["value"],
                "visualization": visualization,
            },
        )

    def create_relationship_component(
        self, data: Dict[str, Any], parent_id: str
    ) -> LayoutComponent:
        """Create a component for a relationship."""
        visualization = data.get("visualization", {})
        return LayoutComponent(
            id=f"{parent_id}_rel_{data['type']}_{data['source']}_{data['target']}",
            type=ComponentType.RELATIONSHIP,
            position=Position(0, 0),
            size=self._get_size_from_properties(visualization.get("properties", {})),
            properties={
                "type": data["type"],
                "source": data["source"],
                "target": data["target"],
                "visualization": visualization,
            },
        )

    def _generate_id(self, data: Dict[str, Any]) -> str:
        """Generate a unique ID for a component."""
        if "object" in data:
            return f"obj_{data['object']['name']}"
        elif "type" in data:
            return f"type_{data['type']['name']}"
        elif "attributes" in data:
            return "artifact"
        else:
            return f"comp_{id(data)}"

    def _get_size_from_properties(self, properties: Dict[str, Any]) -> Size:
        """Get component size from properties or use defaults."""
        width = float(properties.get("width", self.default_icon_size.width))
        height = float(properties.get("height", self.default_icon_size.height))
        return Size(width, height)
