"""Demo of interactive visualization components."""

from reifire.visualization.interactive import (
    InteractiveComponent,
    InteractionType,
    InteractionEvent,
    Position
)
from reifire.visualization.layout import (
    LayoutComponent,
    ComponentType,
    Size
)
from reifire.visualization.viewer import ComponentViewer


def main() -> None:
    """Run the interactive demo."""
    print("Starting demo...")
    
    # Create viewer
    viewer = ComponentViewer(width=400, height=300)
    
    # Create a single test component
    layout = LayoutComponent(
        id="Test Component",
        type=ComponentType.OBJECT,
        position=Position(100, 100),
        size=Size(100, 50)
    )
    
    component = InteractiveComponent(
        layout,
        enabled_interactions=[
            InteractionType.CLICK,
            InteractionType.HOVER,
            InteractionType.DRAG
        ]
    )
    
    print("Adding component...")
    viewer.add_component(component)
    
    print("\nYou should see:")
    print("1. A window with a black border")
    print("2. A red square in the top-left")
    print("3. A title at the top")
    print("4. A blue rectangle with white text in the center")
    
    print("\nStarting viewer...")
    viewer.run()


if __name__ == "__main__":
    main() 