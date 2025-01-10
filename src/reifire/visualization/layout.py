"""Layout engine for visual components."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple


class ConnectionType(Enum):
    """Types of connections between components."""

    PARENT_CHILD = "parent-child"  # Basic hierarchical relationship
    INHERITANCE = "inheritance"  # Class/type inheritance
    COMPOSITION = "composition"  # Strong ownership/containment
    AGGREGATION = "aggregation"  # Weak ownership/containment
    DEPENDENCY = "dependency"  # Uses/depends on
    ASSOCIATION = "association"  # General relationship
    REFERENCE = "reference"  # References/points to


@dataclass
class Connection:
    """Represents a connection between two components."""

    source_id: str
    target_id: str
    type: ConnectionType
    properties: Dict[str, Any] = field(default_factory=dict)


class LayoutType(Enum):
    """Types of layouts supported by the engine."""

    HIERARCHICAL = "hierarchical"  # Tree-like structure
    VERTICAL = "vertical"  # Top to bottom
    HORIZONTAL = "horizontal"  # Left to right
    GRID = "grid"  # Matrix layout
    FLOW = "flow"  # Natural flow layout
    CENTERED = "centered"  # Centered layout


class ComponentType(Enum):
    """Types of components that can be laid out."""

    OBJECT = "object"  # Base objects
    MODIFIER = "modifier"  # Object modifiers
    ATTRIBUTE = "attribute"  # Component attributes
    RELATIONSHIP = "relationship"  # Component relationships
    ICON = "icon"  # Icon/image components
    COLOR = "color"  # Color components
    GROUP = "group"  # Grouped components


@dataclass
class Position:
    """2D position with optional depth for hierarchical layouts."""

    x: float
    y: float
    z: Optional[float] = None


@dataclass
class Size:
    """Component size."""

    width: float
    height: float


@dataclass
class LayoutComponent:
    """A component to be laid out."""

    id: str
    type: ComponentType
    position: Position
    size: Size
    children: List["LayoutComponent"] = field(default_factory=list)
    parent: Optional["LayoutComponent"] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    connections: List[Connection] = field(default_factory=list)

    def add_connection(
        self,
        target_id: str,
        conn_type: ConnectionType,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a connection to another component."""
        self.connections.append(
            Connection(
                source_id=self.id,
                target_id=target_id,
                type=conn_type,
                properties=properties or {},
            )
        )


class LayoutEngine:
    """Engine for laying out visual components."""

    def __init__(self, layout_type: LayoutType = LayoutType.HIERARCHICAL) -> None:
        """Initialize the layout engine."""
        self.layout_type = layout_type
        self.components: Dict[str, LayoutComponent] = {}
        self.root: Optional[LayoutComponent] = None

    def add_component(
        self,
        id: str,
        type: ComponentType,
        size: Size,
        parent_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> LayoutComponent:
        """Add a component to be laid out."""
        # Create component with temporary position
        component = LayoutComponent(
            id=id,
            type=type,
            position=Position(0, 0),
            size=size,
            properties=properties or {},
        )

        # Set up parent-child relationship
        if parent_id:
            parent = self.components.get(parent_id)
            if parent:
                component.parent = parent
                parent.children.append(component)
                # Add implicit parent-child connection
                component.add_connection(parent_id, ConnectionType.PARENT_CHILD)
            else:
                raise ValueError(f"Parent component {parent_id} not found")
        elif not self.root:
            self.root = component

        self.components[id] = component
        return component

    def add_connection(
        self,
        source_id: str,
        target_id: str,
        conn_type: ConnectionType,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a connection between components."""
        source = self.components.get(source_id)
        target = self.components.get(target_id)

        if not source or not target:
            raise ValueError("Source or target component not found")

        source.add_connection(target_id, conn_type, properties)

    def get_all_connections(self) -> List[Connection]:
        """Get all connections in the layout."""
        connections = []
        for component in self.components.values():
            connections.extend(component.connections)
        return connections

    def layout(self) -> Dict[str, Tuple[Position, Size]]:
        """Calculate positions for all components based on layout type."""
        if not self.root:
            return {}

        if self.layout_type == LayoutType.HIERARCHICAL:
            self._layout_hierarchical(self.root, Position(0, 0))
        elif self.layout_type == LayoutType.VERTICAL:
            self._layout_vertical(self.root, Position(0, 0))
        elif self.layout_type == LayoutType.HORIZONTAL:
            self._layout_horizontal(self.root, Position(0, 0))
        elif self.layout_type == LayoutType.GRID:
            self._layout_grid(self.root, Position(0, 0))
        elif self.layout_type == LayoutType.FLOW:
            self._layout_flow(self.root, Position(0, 0))
        elif self.layout_type == LayoutType.CENTERED:
            self._layout_centered(self.root, Position(0, 0))

        return {id: (c.position, c.size) for id, c in self.components.items()}

    def _layout_hierarchical(
        self, component: LayoutComponent, start_pos: Position
    ) -> Size:
        """Layout components in a tree structure."""
        component.position = start_pos
        if not component.children:
            return component.size

        # Calculate positions for children
        total_width = 0.0
        max_height = 0.0
        x = start_pos.x
        y = start_pos.y + component.size.height + 50  # Vertical spacing

        for child in component.children:
            child_size = self._layout_hierarchical(child, Position(x, y))
            total_width += child_size.width
            max_height = max(max_height, child_size.height)
            x += child_size.width + 20  # Horizontal spacing

        # Center children under parent
        offset = (total_width - component.size.width) / 2
        for child in component.children:
            child.position.x -= offset

        return Size(
            max(total_width, component.size.width),
            component.size.height + max_height + 50,
        )

    def _layout_vertical(self, component: LayoutComponent, start_pos: Position) -> Size:
        """Layout components vertically."""
        component.position = start_pos
        if not component.children:
            return component.size

        total_height = component.size.height
        max_width = component.size.width
        y = start_pos.y + component.size.height + 20  # Vertical spacing

        for child in component.children:
            child.position = Position(start_pos.x, y)
            total_height += child.size.height + 20  # Include spacing
            max_width = max(max_width, child.size.width)
            y += child.size.height + 20

        return Size(max_width, total_height)

    def _layout_horizontal(
        self, component: LayoutComponent, start_pos: Position
    ) -> Size:
        """Layout components horizontally."""
        component.position = start_pos
        if not component.children:
            return component.size

        total_width = component.size.width
        max_height = component.size.height
        x = start_pos.x + component.size.width + 20  # Horizontal spacing

        for child in component.children:
            child.position = Position(x, start_pos.y)
            total_width += child.size.width + 20  # Include spacing
            max_height = max(max_height, child.size.height)
            x += child.size.width + 20

        return Size(total_width, max_height)

    def _layout_grid(self, component: LayoutComponent, start_pos: Position) -> Size:
        """Layout components in a grid."""
        component.position = start_pos
        if not component.children:
            return component.size

        # Calculate grid dimensions
        n = len(component.children)
        cols = int(n**0.5)  # Square root for roughly square grid
        rows = (n + cols - 1) // cols

        max_cell_width = max(child.size.width for child in component.children)
        max_cell_height = max(child.size.height for child in component.children)

        # Position children in grid
        for i, child in enumerate(component.children):
            row = i // cols
            col = i % cols
            x = start_pos.x + col * (max_cell_width + 20)
            y = start_pos.y + row * (max_cell_height + 20)
            child.position = Position(x, y)

        total_width = cols * max_cell_width + (cols - 1) * 20
        total_height = rows * max_cell_height + (rows - 1) * 20

        return Size(total_width, total_height)

    def _layout_flow(self, component: LayoutComponent, start_pos: Position) -> Size:
        """Layout components in a natural flow."""
        component.position = start_pos
        if not component.children:
            return component.size

        x = start_pos.x
        y = start_pos.y + component.size.height + 20
        row_height = 0.0
        max_width = 0.0
        row_start_x = x

        for child in component.children:
            if x + child.size.width > 1000:  # Max width threshold
                x = row_start_x
                y += row_height + 20
                row_height = 0

            child.position = Position(x, y)
            x += child.size.width + 20
            row_height = max(row_height, child.size.height)
            max_width = max(max_width, x - row_start_x)

        return Size(max_width, y + row_height - start_pos.y)

    def _layout_centered(self, component: LayoutComponent, start_pos: Position) -> Size:
        """Layout components with center alignment."""
        component.position = start_pos
        if not component.children:
            return component.size

        # First layout children vertically
        total_height = component.size.height
        max_width = component.size.width
        y = start_pos.y + component.size.height + 20

        for child in component.children:
            child_width = child.size.width
            max_width = max(max_width, child_width)
            child.position = Position(
                start_pos.x + (max_width - child_width) / 2, y  # Center horizontally
            )
            total_height += child.size.height + 20
            y += child.size.height + 20

        return Size(max_width, total_height)
