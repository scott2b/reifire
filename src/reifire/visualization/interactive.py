"""Interactive component system for visualization."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Callable
from enum import Enum
from .layout import LayoutComponent, Position, Size


class InteractionType(Enum):
    """Types of interactions supported by components."""

    CLICK = "click"
    HOVER = "hover"
    DRAG = "drag"
    ZOOM = "zoom"
    PAN = "pan"
    RESIZE = "resize"


@dataclass
class InteractionEvent:
    """Event data for component interactions."""

    type: InteractionType
    position: Position
    target_id: str
    data: Dict[str, Any] = field(default_factory=dict)


class InteractiveComponent:
    """Base class for interactive visualization components."""

    def __init__(
        self,
        layout_component: LayoutComponent,
        enabled_interactions: Optional[List[InteractionType]] = None,
    ) -> None:
        """Initialize the interactive component.

        Args:
            layout_component: The underlying layout component
            enabled_interactions: List of interaction types to enable
        """
        self.layout = layout_component
        self.enabled_interactions = enabled_interactions or [
            InteractionType.CLICK,
            InteractionType.HOVER,
        ]
        self.handlers: Dict[
            InteractionType, List[Callable[[InteractionEvent], None]]
        ] = {itype: [] for itype in InteractionType}
        self.state: Dict[str, Any] = {}

    def add_handler(
        self,
        interaction_type: InteractionType,
        handler: Callable[[InteractionEvent], None],
    ) -> None:
        """Add an event handler for a specific interaction type."""
        if interaction_type not in self.enabled_interactions:
            raise ValueError(f"Interaction type {interaction_type} is not enabled")
        self.handlers[interaction_type].append(handler)

    def handle_event(self, event: InteractionEvent) -> None:
        """Handle an interaction event."""
        if event.type not in self.enabled_interactions:
            return

        for handler in self.handlers[event.type]:
            handler(event)

    def update_state(self, updates: Dict[str, Any]) -> None:
        """Update the component's state."""
        self.state.update(updates)

    def get_state(self) -> Dict[str, Any]:
        """Get the current state."""
        return self.state.copy()

    def is_interaction_enabled(self, interaction_type: InteractionType) -> bool:
        """Check if an interaction type is enabled."""
        return interaction_type in self.enabled_interactions

    def enable_interaction(self, interaction_type: InteractionType) -> None:
        """Enable an interaction type."""
        if interaction_type not in self.enabled_interactions:
            self.enabled_interactions.append(interaction_type)

    def disable_interaction(self, interaction_type: InteractionType) -> None:
        """Disable an interaction type."""
        if interaction_type in self.enabled_interactions:
            self.enabled_interactions.remove(interaction_type)

    def get_bounds(self) -> tuple[Position, Size]:
        """Get the component's position and size."""
        return (self.layout.position, self.layout.size)

    def contains_point(self, point: Position) -> bool:
        """Check if a point is within the component's bounds."""
        pos, size = self.get_bounds()
        return (
            pos.x <= point.x <= pos.x + size.width
            and pos.y <= point.y <= pos.y + size.height
        )
