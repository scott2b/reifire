"""Example script demonstrating the visualization system."""

import json
from pathlib import Path
from reifire.visualization.htmlrenderer import HTMLRenderer

def main():
    """Run the visualization example."""
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

    # Initialize renderer
    renderer = HTMLRenderer()

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
                for attr in data["artifact"]["attributes"]:
                    print(f"    - {attr.get('name')}: {attr.get('value', '')}")
                    if "alternatives" in attr:
                        print(f"      - Alternatives: {len(attr['alternatives'])}")
        
        # Generate visualization
        output_file = output_dir / f"{filename.replace('.json', '.html')}"
        components, connections = renderer.processor.process_json(data)
        
        print("\nGenerated components:")
        for comp in components:
            print(f"- {comp.type}: {comp.label}")
        
        print("\nGenerated connections:")
        for conn in connections:
            print(f"- {conn.source} -> {conn.target} ({conn.type})")
        
        renderer.render(data, output_file=output_file)
        print(f"\nGenerated {output_file}")

if __name__ == "__main__":
    main() 