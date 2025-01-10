"""Example script demonstrating the visualization system."""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Any
from reifire.visualization.htmlrenderer import HTMLRenderer
from reifire.visualization.icon_manager import IconManager
from reifire.visualization.nounproject import NounProjectClient
from reifire.visualization.material_icons import MaterialIconProvider
from reifire.icon_registry import IconRegistry
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('reifire.visualization')
logger.setLevel(logging.DEBUG)


class IconUsageTracker:
    """Track icon usage during visualization generation."""
    
    def __init__(self):
        """Initialize the tracker."""
        self.usage: Dict[str, List[Tuple[str, str, str]]] = defaultdict(list)
    
    def add_icon(self, visualization: str, term: str, source: str, icon_path: str):
        """Add an icon usage entry."""
        self.usage[visualization].append((term, source, icon_path))
    
    def print_report(self):
        """Print a report of icon usage."""
        print("\n=== Icon Usage Report ===")
        for visualization, icons in self.usage.items():
            print(f"\n{visualization}:")
            source_counts = defaultdict(int)
            for term, source, icon_path in icons:
                print(f"  - {term}: {source} ({icon_path})")
                source_counts[source] += 1
            print("  Summary:")
            for source, count in source_counts.items():
                print(f"    {source}: {count} icons")


class IconManagerWithTracking(IconManager):
    """Icon manager that tracks icon usage."""
    
    def __init__(self, icon_registry: IconRegistry, noun_project_client: NounProjectClient, tracker: IconUsageTracker):
        """Initialize the tracking icon manager."""
        super().__init__(icon_registry, noun_project_client)
        self.tracker = tracker
        self.current_visualization = "unknown"
    
    def get_visualization_properties(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Override to track icon usage."""
        result = super().get_visualization_properties(obj)
        if "image" in result:
            term = obj.get("name", "") or obj.get("type", "")
            source = result.get("source", "unknown")
            self.tracker.add_icon(self.current_visualization, term, source, result["image"])
        return result


def main():
    """Run the visualization example."""
    # Initialize renderer and icon registry
    renderer = HTMLRenderer()
    icon_registry = IconRegistry()
    icon_tracker = IconUsageTracker()
    
    # Initialize icon providers
    material_icons_available = False
    noun_project_available = False
    
    # Try to initialize Material Design Icons
    if material_icons_dir := os.environ.get("MATERIAL_DESIGN_ICONS_DIR"):
        print(f"Found Material Design Icons directory: {material_icons_dir}")
        material_provider = MaterialIconProvider()
        if material_provider.is_available():
            material_icons_available = True
            print("Successfully initialized Material Design Icons")
        else:
            print("Warning: Material Design Icons directory exists but provider not available")
    else:
        print("Warning: MATERIAL_DESIGN_ICONS_DIR not set")
    
    # Try to initialize Noun Project client
    api_key = os.environ.get("NOUN_PROJECT_API_KEY")
    api_secret = os.environ.get("NOUN_PROJECT_API_SECRET")
    noun_project_client = None
    
    if api_key and api_secret:
        print(f"Found Noun Project credentials (key starts with: {api_key[:4]})")
        try:
            noun_project_client = NounProjectClient(
                api_key=api_key,
                api_secret=api_secret
            )
            noun_project_available = True
            print("Successfully initialized Noun Project client")
        except Exception as e:
            print(f"Warning: Failed to initialize Noun Project client: {e}")
    else:
        print("Warning: Noun Project credentials not found in environment variables")
    
    # Initialize icon manager if any provider is available
    if material_icons_available or noun_project_available:
        icon_manager = IconManagerWithTracking(icon_registry, noun_project_client, icon_tracker)
        renderer.processor.icon_manager = icon_manager
        print("\nIcon support initialized with:")
        print(f"- Material Design Icons: {'Yes' if material_icons_available else 'No'}")
        print(f"- Noun Project: {'Yes' if noun_project_available else 'No'}")
    else:
        print("\nWarning: No icon providers available")
        print("Set MATERIAL_DESIGN_ICONS_DIR for Material Design Icons")
        print("Set NOUN_PROJECT_API_KEY and NOUN_PROJECT_API_SECRET for Noun Project")
        print("Continuing without icon support...")

    # Load example JSON files
    examples_dir = Path(__file__).parent
    example_files = [
        "basic_illustration.json",
        "code_generation.json",
        "data_analysis.json",
        "content_generation.json",
        "complex_visual_scene.json",
        "ui_component.json"
    ]

    # Create output directory
    output_dir = examples_dir / "visualizations"
    output_dir.mkdir(exist_ok=True)

    # Process each example
    for filename in example_files:
        print(f"\nProcessing {filename}...")
        
        # Load JSON data
        json_path = examples_dir / filename
        if not json_path.exists():
            print(f"Warning: {filename} not found")
            continue
            
        with open(json_path) as f:
            data = json.load(f)
        
        # Set current visualization for tracking
        if hasattr(renderer.processor, 'icon_manager'):
            renderer.processor.icon_manager.current_visualization = filename
        
        # Print structure before processing
        print("\nInput JSON structure:")
        if "object" in data:
            print(f"- Object: {data['object'].get('name')}")
            if "modifiers" in data["object"]:
                print(f"  - Modifiers: {len(data['object']['modifiers'])}")
        if "type" in data:
            print(f"- Type: {data['type'].get('name')}")
        if "artifact" in data:
            print(f"- Artifact: {data['artifact'].get('type')}")
            if "attributes" in data["artifact"]:
                print(f"  - Attributes: {len(data['artifact']['attributes'])}")
            if "relationships" in data["artifact"]:
                print(f"  - Relationships: {len(data['artifact']['relationships'])}")
        
        # Render visualization
        output_path = output_dir / f"{filename.replace('.json', '.html')}"
        renderer.render(data, output_file=output_path)
        print(f"Generated visualization: {output_path}")
    
    # Print final icon usage report
    icon_tracker.print_report()


if __name__ == "__main__":
    main() 