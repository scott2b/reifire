"""Color swatch generation for visualizations."""

import re
from typing import Dict, List, Optional, Tuple

class ColorSwatchGenerator:
    """Generates SVG color swatches for visualization."""

    # Common color names to RGB values
    COLOR_MAP = {
        "red": "#FF0000",
        "green": "#00FF00",
        "blue": "#0000FF",
        "yellow": "#FFFF00",
        "purple": "#800080",
        "orange": "#FFA500",
        "brown": "#A52A2A",
        "pink": "#FFC0CB",
        "gray": "#808080",
        "black": "#000000",
        "white": "#FFFFFF",
    }

    @staticmethod
    def _parse_color(color: str) -> str:
        """Convert a color name to its hex value.
        
        Args:
            color: Color name or hex value
            
        Returns:
            Hex color value
        """
        # If it's already a hex color, return it
        if re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
            return color
            
        # Try to get from color map
        color = color.lower()
        return ColorSwatchGenerator.COLOR_MAP.get(color, "#808080")  # Default to gray if unknown

    @staticmethod
    def generate_swatch(color: str, size: int = 24) -> str:
        """Generate an SVG color swatch.
        
        Args:
            color: Color name or hex value
            size: Size of the swatch in pixels
            
        Returns:
            SVG string for the color swatch
        """
        hex_color = ColorSwatchGenerator._parse_color(color)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
    <rect width="{size}" height="{size}" fill="{hex_color}"/>
</svg>'''

    @staticmethod
    def generate_swatches(colors: List[str], size: int = 24) -> List[str]:
        """Generate multiple SVG color swatches.
        
        Args:
            colors: List of color names or hex values
            size: Size of each swatch in pixels
            
        Returns:
            List of SVG strings for the color swatches
        """
        return [ColorSwatchGenerator.generate_swatch(color, size) for color in colors] 