"""Material Design Icons provider."""

import os
from pathlib import Path
from typing import Optional, Dict, List, Set
import logging

logger = logging.getLogger(__name__)

class MaterialIconProvider:
    """Provider for Material Design Icons."""

    def __init__(self):
        """Initialize the Material Design Icons provider."""
        self.base_dir = os.environ.get("MATERIAL_DESIGN_ICONS_DIR")
        self.style = "materialicons"  # Default style
        self.size = "24dp"           # Default size
        self.resolution = "1x"       # Default resolution
        self._icon_cache: Dict[str, str] = {}
        self._available_icons: Dict[str, List[str]] = {}  # category -> icon names
        self._term_to_icons: Dict[str, List[Tuple[str, str]]] = {}  # term -> [(category, icon_name)]
        
        if self.is_available():
            self._load_available_icons()
            logger.info(f"Loaded {sum(len(icons) for icons in self._available_icons.values())} Material Design icons")

    def is_available(self) -> bool:
        """Check if Material Design Icons are available."""
        return bool(self.base_dir and Path(self.base_dir).exists())

    def _load_available_icons(self) -> None:
        """Load all available icon names from the Material Design Icons directory."""
        base_path = Path(self.base_dir) / "png"
        if not base_path.exists():
            logger.warning(f"Material Design Icons directory not found at {base_path}")
            return

        for category in base_path.iterdir():
            if not category.is_dir():
                continue
            self._available_icons[category.name] = []
            for icon_dir in category.iterdir():
                if icon_dir.is_dir():
                    # Check if the icon actually exists with our style/size/resolution preferences
                    icon_path = (
                        icon_dir / 
                        self.style /
                        self.size /
                        self.resolution /
                        f"baseline_{icon_dir.name}_black_24dp.png"
                    )
                    if icon_path.exists():
                        self._available_icons[category.name].append(icon_dir.name)
                        # Add the icon name and its variations to term mappings
                        terms = self._extract_terms(icon_dir.name)
                        for term in terms:
                            if term not in self._term_to_icons:
                                self._term_to_icons[term] = []
                            self._term_to_icons[term].append((category.name, icon_dir.name))
                        logger.debug(f"Found icon {icon_dir.name} in category {category.name}")
            
            if self._available_icons[category.name]:
                logger.info(f"Loaded {len(self._available_icons[category.name])} icons from category {category.name}")
            else:
                logger.debug(f"No valid icons found in category {category.name}")

    def _extract_terms(self, icon_name: str) -> Set[str]:
        """Extract searchable terms from an icon name.
        
        Args:
            icon_name: The name of the icon
            
        Returns:
            Set of terms extracted from the icon name
        """
        terms = set()
        
        # Split on underscores and add each part
        parts = icon_name.split('_')
        terms.update(parts)
        
        # Add the full name
        terms.add(icon_name)
        
        # Add combinations of adjacent terms
        for i in range(len(parts) - 1):
            combined = '_'.join(parts[i:i+2])
            terms.add(combined)

        # Add plural/singular forms
        for part in parts:
            if part.endswith('s'):
                terms.add(part[:-1])
            else:
                terms.add(part + 's')

        return terms

    def get_icon_path(self, term: str) -> Optional[str]:
        """Get the path to a Material Design icon."""
        if not self.is_available():
            return None

        logger.debug(f"Looking up Material Design icon for term: {term}")

        # Check cache first
        if term in self._icon_cache:
            logger.debug(f"Found cached icon path for {term}")
            return self._icon_cache[term]

        # Normalize the term
        normalized_term = term.lower().replace(' ', '_').replace('-', '_')
        logger.debug(f"Normalized term: {normalized_term}")

        # Check term mappings
        matches = self._term_to_icons.get(normalized_term, [])
        if matches:
            category, icon_name = matches[0]  # Use first match
            icon_path = self._build_icon_path(category, icon_name)
            if icon_path and icon_path.exists():
                result = str(icon_path)
                self._icon_cache[term] = result
                logger.debug(f"Found icon match: {result}")
                return result

        # Try individual words if no direct match
        words = normalized_term.split('_')
        for word in words:
            matches = self._term_to_icons.get(word, [])
            if matches:
                category, icon_name = matches[0]  # Use first match
                icon_path = self._build_icon_path(category, icon_name)
                if icon_path and icon_path.exists():
                    result = str(icon_path)
                    self._icon_cache[term] = result
                    logger.debug(f"Found word match: {result}")
                    return result

        logger.debug(f"No Material Design icon found for {term}")
        return None

    def _build_icon_path(self, category: str, icon_name: str) -> Optional[Path]:
        """Build the full path to a Material Design icon.
        
        Args:
            category: The icon category (e.g., 'action', 'alert')
            icon_name: The name of the icon
            
        Returns:
            Path to the icon if it exists, None otherwise
        """
        icon_path = (
            Path(self.base_dir) / 
            "png" / 
            category /
            icon_name / 
            self.style / 
            self.size / 
            self.resolution / 
            f"baseline_{icon_name}_black_24dp.png"
        )
        return icon_path if icon_path.exists() else None 