"""Tests for the visualization layout engine."""

from reifire.visualization.layout import (
    LayoutEngine,
    ComponentType,
    LayoutType,
    Size,
)
from reifire.visualization.factory import ComponentFactory


def test_basic_layout() -> None:
    """Test basic layout functionality."""
    engine = LayoutEngine(layout_type=LayoutType.VERTICAL)

    # Create a simple component hierarchy
    engine.add_component(
        id="root",
        type=ComponentType.OBJECT,
        size=Size(100, 50),
    )

    engine.add_component(
        id="child1",
        type=ComponentType.MODIFIER,
        size=Size(80, 40),
        parent_id="root",
    )

    engine.add_component(
        id="child2",
        type=ComponentType.MODIFIER,
        size=Size(80, 40),
        parent_id="root",
    )

    # Calculate layout
    layout = engine.layout()

    # Verify positions
    assert layout["root"][0].y == 0  # Root at top
    assert layout["child1"][0].y > layout["root"][0].y  # Child1 below root
    assert layout["child2"][0].y > layout["child1"][0].y  # Child2 below child1


def test_hierarchical_layout() -> None:
    """Test hierarchical layout with nested components."""
    engine = LayoutEngine(layout_type=LayoutType.HIERARCHICAL)

    # Create a more complex hierarchy
    engine.add_component(
        id="root",
        type=ComponentType.OBJECT,
        size=Size(100, 50),
    )

    engine.add_component(
        id="group1",
        type=ComponentType.GROUP,
        size=Size(80, 40),
        parent_id="root",
    )

    engine.add_component(
        id="group2",
        type=ComponentType.GROUP,
        size=Size(80, 40),
        parent_id="root",
    )

    engine.add_component(
        id="child1",
        type=ComponentType.MODIFIER,
        size=Size(60, 30),
        parent_id="group1",
    )

    engine.add_component(
        id="child2",
        type=ComponentType.MODIFIER,
        size=Size(60, 30),
        parent_id="group2",
    )

    # Calculate layout
    layout = engine.layout()

    # Verify hierarchy
    assert layout["root"][0].y < layout["group1"][0].y  # Groups below root
    assert layout["root"][0].y < layout["group2"][0].y
    assert layout["group1"][0].y < layout["child1"][0].y  # Children below groups
    assert layout["group2"][0].y < layout["child2"][0].y


def test_component_factory() -> None:
    """Test component factory with example data."""
    factory = ComponentFactory()

    # Example reified data structure
    data = {
        "object": {
            "name": "test_object",
            "modifiers": [
                {
                    "name": "mod1",
                    "value": "value1",
                    "visualization": {
                        "source": "nounproject",
                        "name": "icon1",
                        "image": "icon1.svg",
                    },
                }
            ],
        },
        "type": {
            "name": "test_type",
            "category": "test",
        },
        "artifact": {
            "type": "test",
            "attributes": [
                {
                    "name": "attr1",
                    "value": "value1",
                    "visualization": {
                        "source": "nounproject",
                        "name": "icon2",
                        "image": "icon2.svg",
                    },
                }
            ],
        },
    }

    # Create component from data
    component = factory.create_from_reified(data)

    # Verify component structure
    assert component.type == ComponentType.OBJECT
    assert component.id == "obj_test_object"
    assert len(component.children) == 1  # One modifier

    # Verify modifier
    modifier = component.children[0]
    assert modifier.type == ComponentType.MODIFIER
    assert modifier.properties["name"] == "mod1"
    assert modifier.properties["value"] == "value1"


def test_layout_with_factory() -> None:
    """Test layout engine with factory-created components."""
    factory = ComponentFactory()
    engine = LayoutEngine(layout_type=LayoutType.HIERARCHICAL)

    # Example data
    data = {
        "object": {
            "name": "test_object",
            "modifiers": [
                {
                    "name": "mod1",
                    "value": "value1",
                    "visualization": {
                        "source": "nounproject",
                        "name": "icon1",
                        "image": "icon1.svg",
                        "properties": {
                            "width": 60,
                            "height": 30,
                        },
                    },
                }
            ],
        },
        "visualization": {
            "properties": {
                "width": 100,
                "height": 50,
            },
        },
    }

    # Create and add components
    root_component = factory.create_from_reified(data)
    engine.add_component(
        id=root_component.id,
        type=root_component.type,
        size=root_component.size,
    )

    for child in root_component.children:
        engine.add_component(
            id=child.id,
            type=child.type,
            size=child.size,
            parent_id=root_component.id,
            properties=child.properties,
        )

    # Calculate layout
    layout = engine.layout()

    # Verify layout
    assert len(layout) == 2  # Root and one modifier
    root_pos = layout[root_component.id][0]
    mod_pos = layout[root_component.children[0].id][0]
    assert mod_pos.y > root_pos.y  # Modifier below root


def test_grid_layout() -> None:
    """Test grid layout with multiple components."""
    engine = LayoutEngine(layout_type=LayoutType.GRID)

    # Create a root with multiple children
    engine.add_component(
        id="root",
        type=ComponentType.OBJECT,
        size=Size(100, 50),
    )

    # Add 4 children to create a 2x2 grid
    for i in range(4):
        engine.add_component(
            id=f"child{i}",
            type=ComponentType.ICON,
            size=Size(40, 40),
            parent_id="root",
        )

    # Calculate layout
    layout = engine.layout()

    # Verify grid structure
    positions = [layout[f"child{i}"][0] for i in range(4)]

    # Check that we have two rows
    row1_y = positions[0].y
    row2_y = positions[2].y
    assert row1_y < row2_y

    # Check that we have two columns
    col1_x = positions[0].x
    col2_x = positions[1].x
    assert col1_x < col2_x
