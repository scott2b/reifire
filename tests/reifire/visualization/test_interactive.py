"""Tests for interactive visualization components."""

import pytest
from reifire.visualization.interactive import (
    InteractiveComponent,
    InteractionType,
    InteractionEvent,
    Position
)
from reifire.visualization.layout import LayoutComponent, ComponentType, Size


@pytest.fixture
def basic_component() -> InteractiveComponent:
    """Create a basic interactive component for testing."""
    layout = LayoutComponent(
        id="test",
        type=ComponentType.OBJECT,
        position=Position(10, 10),
        size=Size(100, 50)
    )
    return InteractiveComponent(layout)


def test_component_initialization(basic_component: InteractiveComponent) -> None:
    """Test component initialization."""
    assert basic_component.layout.id == "test"
    assert InteractionType.CLICK in basic_component.enabled_interactions
    assert InteractionType.HOVER in basic_component.enabled_interactions
    assert len(basic_component.state) == 0


def test_event_handling(basic_component: InteractiveComponent) -> None:
    """Test event handling."""
    events_received = []
    
    def handler(event: InteractionEvent) -> None:
        events_received.append(event)
        
    basic_component.add_handler(InteractionType.CLICK, handler)
    
    event = InteractionEvent(
        type=InteractionType.CLICK,
        position=Position(15, 15),
        target_id="test"
    )
    
    basic_component.handle_event(event)
    assert len(events_received) == 1
    assert events_received[0].type == InteractionType.CLICK
    assert events_received[0].target_id == "test"


def test_disabled_interaction(basic_component: InteractiveComponent) -> None:
    """Test handling of disabled interactions."""
    events_received = []
    
    def handler(event: InteractionEvent) -> None:
        events_received.append(event)
        
    # Try to add handler for disabled interaction
    with pytest.raises(ValueError):
        basic_component.add_handler(InteractionType.DRAG, handler)
    
    # Try to handle disabled interaction event
    event = InteractionEvent(
        type=InteractionType.DRAG,
        position=Position(15, 15),
        target_id="test"
    )
    
    basic_component.handle_event(event)
    assert len(events_received) == 0


def test_state_management(basic_component: InteractiveComponent) -> None:
    """Test component state management."""
    basic_component.update_state({"selected": True})
    assert basic_component.get_state()["selected"] is True
    
    basic_component.update_state({"color": "blue"})
    state = basic_component.get_state()
    assert state["selected"] is True
    assert state["color"] == "blue"


def test_interaction_enabling(basic_component: InteractiveComponent) -> None:
    """Test enabling/disabling interactions."""
    assert not basic_component.is_interaction_enabled(InteractionType.DRAG)
    
    basic_component.enable_interaction(InteractionType.DRAG)
    assert basic_component.is_interaction_enabled(InteractionType.DRAG)
    
    basic_component.disable_interaction(InteractionType.DRAG)
    assert not basic_component.is_interaction_enabled(InteractionType.DRAG)


def test_bounds_checking(basic_component: InteractiveComponent) -> None:
    """Test point containment checking."""
    # Point inside
    assert basic_component.contains_point(Position(15, 15))
    
    # Points outside
    assert not basic_component.contains_point(Position(5, 15))  # Left
    assert not basic_component.contains_point(Position(115, 15))  # Right
    assert not basic_component.contains_point(Position(15, 5))  # Top
    assert not basic_component.contains_point(Position(15, 65))  # Bottom 