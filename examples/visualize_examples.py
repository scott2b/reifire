"""Example script demonstrating the visualization system."""

import json
import os
import sys
from pathlib import Path
from reifire.visualization.htmlrenderer import HTMLRenderer
from reifire.visualization.icon_manager import IconManager
from reifire.visualization.nounproject import NounProjectClient
from reifire.icon_registry import IconRegistry


def main():
    """Run the visualization example."""
    # Check for Noun Project credentials
    api_key = os.environ.get("NOUN_PROJECT_API_KEY")
    api_secret = os.environ.get("NOUN_PROJECT_API_SECRET")
    
    if not api_key or not api_secret:
        print("Warning: Noun Project credentials not found in environment variables.")
        print("Set NOUN_PROJECT_API_KEY and NOUN_PROJECT_API_SECRET to enable icon fetching.")
        print("Continuing without icon support...")
        # Initialize renderer without icon support
        renderer = HTMLRenderer()
    else:
        print(f"Found Noun Project credentials (key starts with: {api_key[:4]})")
        # Initialize components with icon support
        icon_registry = IconRegistry()
        try:
            noun_project_client = NounProjectClient(
                api_key=api_key,
                api_secret=api_secret
            )
            icon_manager = IconManager(icon_registry, noun_project_client)
            # Initialize renderer with icon-enabled processor
            renderer = HTMLRenderer()
            renderer.processor.icon_manager = icon_manager  # Set the icon manager on the renderer's processor
            print("Successfully initialized icon support")
        except Exception as e:
            print(f"Warning: Failed to initialize icon support: {e}")
            print("Continuing without icon support...")
            renderer = HTMLRenderer()

    # Load example JSON files
    examples_dir = Path(__file__).parent
    example_files = [
        "basic_illustration.json",
        # "code_generation.json",
        # "data_analysis.json",
        # "content_generation.json",
        # "complex_visual_scene.json",
        # "ui_component.json"
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


if __name__ == "__main__":
    main() 