"""Tests for the HTML renderer."""

import pytest
from pathlib import Path
from reifire.visualization.htmlrenderer import HTMLRenderer

@pytest.fixture
def sample_data():
    """Sample JSON data for testing."""
    return {
        "object": {
            "name": "test_object",
            "visualization": {
                "source": "nounproject",
                "name": "test",
                "image": "test.svg"
            }
        },
        "type": {
            "name": "test_type",
            "category": "test",
            "visualization": {
                "source": "nounproject",
                "name": "type_test",
                "image": "type.svg"
            }
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
                        "image": "attr1.svg"
                    }
                }
            ]
        }
    }

def test_renderer_initialization():
    """Test renderer initialization."""
    renderer = HTMLRenderer()
    assert renderer.env is not None
    assert renderer.processor is not None

def test_render_basic(sample_data, tmp_path):
    """Test basic rendering functionality."""
    renderer = HTMLRenderer()
    output_file = tmp_path / "test.html"
    
    # Render to string
    html = renderer.render(sample_data)
    assert isinstance(html, str)
    assert "test_object" in html
    assert "test_type" in html
    assert "attr1" in html
    
    # Render to file
    html = renderer.render(sample_data, output_file=output_file)
    assert output_file.exists()
    assert output_file.read_text() == html

def test_component_to_dict():
    """Test component conversion to dictionary."""
    renderer = HTMLRenderer()
    components, _ = renderer.processor.process_json({
        "object": {
            "name": "test",
            "visualization": {
                "source": "test",
                "name": "test",
                "image": "test.svg"
            }
        },
        "type": {
            "name": "test_type",
            "category": "test"
        }
    })
    
    component = components[0]
    component_dict = renderer._component_to_dict(component)
    
    assert component_dict["id"] == component.id
    assert component_dict["type"] == component.type
    assert component_dict["label"] == component.label
    assert component_dict["x"] == component.x
    assert component_dict["y"] == component.y
    assert component_dict["width"] == component.width
    assert component_dict["height"] == component.height
    assert component_dict["properties"] == component.properties

def test_connection_to_dict():
    """Test connection conversion to dictionary."""
    renderer = HTMLRenderer()
    _, connections = renderer.processor.process_json({
        "object": {
            "name": "test"
        },
        "type": {
            "name": "test_type"
        }
    })
    
    connection = connections[0]
    connection_dict = renderer._connection_to_dict(connection)
    
    assert connection_dict["source"] == connection.source
    assert connection_dict["target"] == connection.target
    assert connection_dict["type"] == connection.type
    assert connection_dict["properties"] == connection.properties

def test_render_complex(sample_data, tmp_path):
    """Test rendering with complex data structures."""
    renderer = HTMLRenderer()
    
    # Add some complex structures to the sample data
    sample_data["artifact"]["relationships"] = [
        {
            "type": "depends_on",
            "source": "component1",
            "target": "component2",
            "visualization": {
                "source": "nounproject",
                "name": "dependency",
                "image": "dependency.svg"
            }
        }
    ]
    sample_data["artifact"]["attributes"][0]["alternatives"] = [
        {
            "name": "attr1",
            "value": "alt_value",
            "visualization": {
                "source": "nounproject",
                "name": "alt",
                "image": "alt.svg"
            }
        }
    ]
    
    # Render
    html = renderer.render(sample_data)
    
    # Check for complex elements
    assert "depends_on" in html
    assert "component1" in html
    assert "component2" in html
    assert "alt_value" in html 