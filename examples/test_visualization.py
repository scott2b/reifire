"""Test the visualization system with a sample layout."""

from pathlib import Path
from reifire.visualization.layout import (
    LayoutEngine,
    ComponentType,
    LayoutType,
    Size,
    ConnectionType,
)
from reifire.visualization.htmlrenderer import HTMLRenderer

def main():
    # Create a layout engine
    engine = LayoutEngine(layout_type=LayoutType.HIERARCHICAL)

    # Add some test components
    main = engine.add_component(
        id="main",
        type=ComponentType.OBJECT,
        size=Size(150, 50),
        properties={"label": "Main Component"}
    )

    attr1 = engine.add_component(
        id="attr1",
        type=ComponentType.ATTRIBUTE,
        size=Size(120, 40),
        parent_id="main",
        properties={"label": "Attribute 1"}
    )

    attr2 = engine.add_component(
        id="attr2",
        type=ComponentType.ATTRIBUTE,
        size=Size(120, 40),
        parent_id="main",
        properties={"label": "Attribute 2"}
    )

    # Add some explicit connections
    engine.add_connection(
        "attr1",
        "attr2",
        ConnectionType.DEPENDENCY,
        properties={"label": "depends on"}
    )

    # Create the renderer and generate the visualization
    renderer = HTMLRenderer()
    html = renderer.render_layout(engine)

    # Save to file
    output_path = Path(__file__).parent / "test_visualization.html"
    output_path.write_text(html)
    print(f"Visualization saved to: {output_path}")

if __name__ == "__main__":
    main() 