"""Viewer for visualization output."""

from typing import Dict, Any, Optional
from pathlib import Path
import webbrowser
import tempfile
import os
import atexit

from .htmlrenderer import HTMLRenderer


class VisualizationViewer:
    """Simple viewer for visualization output."""

    def __init__(self) -> None:
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
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
                f.write(result)
                webbrowser.open(f"file://{Path(f.name).resolve()}")

    def open_in_browser(self, html_content: str) -> None:
        """Open HTML content in the default web browser.

        Args:
            html_content: The HTML content to display
        """
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write(str(html_content))  # Convert to string to handle Path objects
            temp_path = f.name

        # Open in browser
        webbrowser.open(f"file://{temp_path}")

        # Schedule file deletion
        def cleanup() -> None:
            try:
                os.unlink(temp_path)
            except OSError as e:
                print(f"Error cleaning up temporary file: {e}")

        atexit.register(cleanup)
