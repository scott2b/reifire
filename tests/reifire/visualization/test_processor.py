"""Tests for the visualization processor."""

import pytest
from reifire.visualization.processor import VisualizationProcessor
from typing import Dict, Any


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """Sample JSON data for testing."""
    return {
        "object": {
            "name": "test_object",
            "visualization": {
                "source": "nounproject",
                "name": "test",
                "image": "test.svg",
            },
        },
        "type": {
            "name": "test_type",
            "category": "test",
            "visualization": {
                "source": "nounproject",
                "name": "type_test",
                "image": "type.svg",
            },
        },
        "artifact": {
            "type": "test_artifact",
            "attributes": [
                {
                    "name": "attr1",
                    "value": "value1",
                    "visualization": {
                        "source": "nounproject",
                        "name": "attr1",
                        "image": "attr1.svg",
                    },
                    "alternatives": [
                        {
                            "name": "attr1",
                            "value": "alt_value1",
                            "visualization": {
                                "source": "nounproject",
                                "name": "alt_attr1",
                                "image": "alt_attr1.svg",
                            },
                        }
                    ],
                }
            ],
            "relationships": [
                {
                    "type": "depends_on",
                    "source": "component1",
                    "target": "component2",
                    "visualization": {
                        "source": "nounproject",
                        "name": "dependency",
                        "image": "dependency.svg",
                    },
                }
            ],
        },
    }


def test_processor_initialization() -> None:
    """Test processor initialization."""
    processor = VisualizationProcessor()
    assert processor.components == []
    assert processor.connections == []
    assert processor.current_y == 0
    assert processor.spacing == 100


def test_process_json(sample_data: Dict[str, Any]) -> None:
    """Test processing JSON data."""
    processor = VisualizationProcessor()
    components, connections = processor.process_json(sample_data)

    # Check components
    assert (
        len(components) == 6
    )  # object, type, artifact, attribute, alternative, relationship
    assert (
        len(connections) >= 5
    )  # At least one connection for each component relationship

    # Check specific components
    component_types = [c.type for c in components]
    assert "object" in component_types
    assert "type" in component_types
    assert "artifact" in component_types
    assert "attribute" in component_types
    assert "alternative" in component_types
    assert "relationship" in component_types

    # Check connections
    connection_types = [c.type for c in connections]
    assert "type" in connection_types
    assert "artifact" in connection_types
    assert "attribute" in connection_types
    assert "alternative" in connection_types


def test_add_object_component() -> None:
    """Test adding an object component."""
    processor = VisualizationProcessor()
    obj = {
        "name": "test",
        "visualization": {"source": "nounproject", "name": "test", "image": "test.svg"},
    }
    component_id = processor._add_object_component(obj, "test_type")

    assert len(processor.components) == 1
    component = processor.components[0]
    assert component.id == component_id
    assert component.type == "test_type"
    assert component.label == "test"
    assert component.properties["visualization"]["name"] == "test"


def test_add_modifier_component() -> None:
    """Test adding a modifier component."""
    processor = VisualizationProcessor()
    modifier = {
        "name": "test_mod",
        "value": "test_value",
        "visualization": {"source": "nounproject", "name": "test", "image": "test.svg"},
    }
    component_id = processor._add_modifier_component(modifier)

    assert len(processor.components) == 1
    component = processor.components[0]
    assert component.id == component_id
    assert component.type == "modifier"
    assert component.label == "test_mod: test_value"


def test_add_attribute_component() -> None:
    """Test adding an attribute component."""
    processor = VisualizationProcessor()
    attr = {
        "name": "test_attr",
        "value": "test_value",
        "visualization": {"source": "nounproject", "name": "test", "image": "test.svg"},
    }
    component_id = processor._add_attribute_component(attr)

    assert len(processor.components) == 1
    component = processor.components[0]
    assert component.id == component_id
    assert component.type == "attribute"
    assert component.label == "test_attr: test_value"


def test_add_relationship_component() -> None:
    """Test adding a relationship component."""
    processor = VisualizationProcessor()
    rel = {
        "type": "depends_on",
        "source": "comp1",
        "target": "comp2",
        "visualization": {
            "source": "nounproject",
            "name": "dependency",
            "image": "dependency.svg",
        },
    }
    component_id = processor._add_relationship_component(rel)

    assert len(processor.components) == 1
    component = processor.components[0]
    assert component.id == component_id
    assert component.type == "relationship"
    assert component.label == "depends_on: comp1 -> comp2"


def test_add_connection() -> None:
    """Test adding a connection."""
    processor = VisualizationProcessor()
    processor._add_connection("source", "target", "test_type")

    assert len(processor.connections) == 1
    connection = processor.connections[0]
    assert connection.source == "source"
    assert connection.target == "target"
    assert connection.type == "test_type"
