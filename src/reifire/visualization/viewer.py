"""Viewer for visualization output."""

from typing import Dict, Any, Optional
from pathlib import Path
import webbrowser

from .htmlrenderer import HTMLRenderer

class VisualizationViewer:
    """Simple viewer for visualization output."""

    def __init__(self):
        self.renderer = HTMLRenderer()

    def view(self, data: Dict[str, Any], output_file: Optional[Path] = None) -> None:
        """View visualization data in the default web browser.
        
        Args:
            data: The visualization data to render
            output_file: Optional output file path. If not provided, will return HTML content.
        """
        # Generate the visualization
        result = self.renderer.render(data, output_file)
        
        # If output file was provided, open it in browser
        if output_file:
            webbrowser.open(f"file://{Path(result).resolve()}")
        else:
            # Create a temporary file and open it
            import tempfile
            with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
                f.write(result)
                webbrowser.open(f"file://{Path(f.name).resolve()}") 