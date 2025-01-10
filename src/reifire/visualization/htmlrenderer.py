"""HTML renderer for the visualization system."""

from typing import Dict, Any, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from .processor import (
    VisualizationProcessor,
    VisualizationComponent,
    VisualizationConnection,
)


class HTMLRenderer:
    """Renders visualization components as HTML."""

    def __init__(self, template_dir: Optional[Path] = None):
        # Set up template directory
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"
        self.template_dir = template_dir

        # Initialize Jinja environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,  # Enable autoescaping for security
            trim_blocks=True,  # Remove first newline after a block
            lstrip_blocks=True,  # Remove leading spaces and tabs
        )
        self.processor = VisualizationProcessor()

    def render(self, data: Dict[str, Any], output_file: Optional[Path] = None) -> str:
        """Render visualization data to HTML.

        Args:
            data: The visualization data to render
            output_file: Optional output file path. If not absolute, will be relative to
                current directory.

        Returns:
            The rendered HTML content as a string.
        """
        # Process the JSON data into components and connections
        components, connections = self.processor.process_json(data)

        # Prepare template data
        template_data = {
            "components": [self._component_to_dict(c) for c in components],
            "connections": [self._connection_to_dict(c) for c in connections],
            "metadata": {
                "title": data.get("metadata", {}).get("title", "Reifire Visualization"),
                "description": data.get("metadata", {}).get("description", ""),
                "visualization_config": (
                    data.get("metadata", {}).get("visualization_config", {})
                ),
            },
        }

        # Render template
        template = self.env.get_template("visualization.html")
        html = template.render(**template_data)

        # Save to file if specified
        if output_file:
            output_file = Path(output_file)
            # Create parent directories if needed
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(html)

        return html

    def _component_to_dict(self, component: VisualizationComponent) -> Dict[str, Any]:
        """Convert a component to a dictionary for the template."""
        return {
            "id": component.id,
            "type": component.type,
            "label": component.label,
            "x": component.x,
            "y": component.y,
            "width": component.width,
            "height": component.height,
            "properties": component.properties,
        }

    def _connection_to_dict(
        self, connection: VisualizationConnection
    ) -> Dict[str, Any]:
        """Convert a connection to a dictionary for the template."""
        return {
            "source": connection.source,
            "target": connection.target,
            "type": connection.type,
            "properties": connection.properties,
        }
