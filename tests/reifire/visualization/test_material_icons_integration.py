"""Integration tests for Material Design Icons provider."""

import os
import pytest
import shutil
from pathlib import Path
from typing import Generator
from reifire.visualization.material_icons import MaterialIconProvider
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def save_icon_to_assets(source_path: Path, dest_dir: Path) -> None:
    """Save an icon to the test assets directory."""
    # Just copy the file with its name
    dest_path = dest_dir / source_path.name
    if not dest_path.exists():
        logger.debug(f"Saving icon to: {dest_path}")
        shutil.copy2(source_path, dest_path)


@pytest.fixture
def icon_provider(material_icons_dir: Path) -> Generator[MaterialIconProvider, None, None]:
    """Create a Material Design Icons provider with environment configuration."""
    source_dir = os.environ.get("MATERIAL_DESIGN_ICONS_DIR")
    logger.debug(f"Material Design Icons source directory from environment: {source_dir}")
    
    if not source_dir:
        pytest.skip("MATERIAL_DESIGN_ICONS_DIR not found in environment")
    
    source_path = Path(source_dir)
    if not source_path.exists():
        pytest.skip(f"Material Design Icons source directory does not exist: {source_path}")
    
    # Use source directory directly
    os.environ["MATERIAL_DESIGN_ICONS_DIR"] = str(source_path)
    provider = MaterialIconProvider()
    
    if not provider.is_available():
        logger.debug("Material Design Icons provider not available")
        pytest.skip("Material Design Icons provider not available")
    
    logger.debug(f"Successfully initialized Material Design Icons provider with directory: {source_path}")
    yield provider


@pytest.mark.integration
def test_icon_loading(icon_provider: MaterialIconProvider, material_icons_dir: Path) -> None:
    """Test that we can load Material Design icons."""
    # Verify that icons were loaded
    assert icon_provider._available_icons
    total_icons = sum(len(icons) for icons in icon_provider._available_icons.values())
    print(f"\nLoaded {total_icons} Material Design icons")
    
    # Print some example categories and icons
    print("\nExample categories and icons:")
    for category, icons in list(icon_provider._available_icons.items())[:5]:  # Show first 5 categories
        print(f"\nCategory: {category}")
        print(f"Number of icons: {len(icons)}")
        if icons:
            print(f"Example icons: {', '.join(icons[:5])}")
            # Save example icons
            for icon_name in icons[:5]:
                icon_path = icon_provider._build_icon_path(category, icon_name)
                if icon_path and icon_path.exists():
                    save_icon_to_assets(icon_path, material_icons_dir)


@pytest.mark.integration
def test_semantic_matching(icon_provider: MaterialIconProvider, material_icons_dir: Path) -> None:
    """Test semantic matching of terms to icons."""
    test_terms = [
        "settings",  # Direct match
        "configuration",  # Semantic match for settings
        "user",  # Common icon
        "profile",  # Semantic match for user/person
        "save",  # Common action
        "store",  # Semantic match for save
        "warning",  # Common status
        "error",  # Common status
        "calendar",  # Common UI element
        "schedule",  # Semantic match for calendar
    ]
    
    print("\nTesting semantic matching:")
    for term in test_terms:
        icon_path = icon_provider.get_icon_path(term)
        if icon_path:
            print(f"\nTerm: {term}")
            print(f"Found icon: {icon_path}")
            assert Path(icon_path).exists()
            save_icon_to_assets(Path(icon_path), material_icons_dir)
        else:
            print(f"\nNo icon found for term: {term}")


@pytest.mark.integration
def test_term_variations(icon_provider: MaterialIconProvider, material_icons_dir: Path) -> None:
    """Test matching of term variations."""
    variations = [
        ("delete", "remove"),  # Synonyms
        ("settings", "configure"),  # Related terms
        ("person", "user"),  # Common alternatives
        ("calendar", "date"),  # Related concepts
        ("warning", "alert"),  # Similar meanings
    ]
    
    print("\nTesting term variations:")
    for term1, term2 in variations:
        path1 = icon_provider.get_icon_path(term1)
        path2 = icon_provider.get_icon_path(term2)
        
        print(f"\nTerm pair: {term1} / {term2}")
        if path1:
            print(f"Icon for {term1}: {path1}")
            save_icon_to_assets(Path(path1), material_icons_dir)
        if path2:
            print(f"Icon for {term2}: {path2}")
            save_icon_to_assets(Path(path2), material_icons_dir)
        
        # At least one term in each pair should find an icon
        assert path1 is not None or path2 is not None


@pytest.mark.integration
def test_ui_component_terms(icon_provider: MaterialIconProvider, material_icons_dir: Path) -> None:
    """Test matching of common UI component terms."""
    ui_terms = [
        "button",
        "checkbox",
        "radio_button",
        "text_field",
        "dropdown",
        "menu",
        "dialog",
        "tooltip",
        "progress",
        "slider",
    ]
    
    print("\nTesting UI component terms:")
    matches = 0
    for term in ui_terms:
        icon_path = icon_provider.get_icon_path(term)
        if icon_path:
            matches += 1
            print(f"\nFound icon for {term}: {icon_path}")
            assert Path(icon_path).exists()
            save_icon_to_assets(Path(icon_path), material_icons_dir)
        else:
            print(f"\nNo icon found for {term}")
    
    # We should find icons for at least some UI terms
    assert matches > 0
    print(f"\nFound icons for {matches} out of {len(ui_terms)} UI terms")


@pytest.mark.integration
def test_technical_terms(icon_provider: MaterialIconProvider, material_icons_dir: Path) -> None:
    """Test matching of technical and development-related terms."""
    tech_terms = [
        "code",
        "bug",
        "database",
        "cloud",
        "security",
        "api",
        "network",
        "storage",
        "sync",
        "analytics",
    ]
    
    print("\nTesting technical terms:")
    matches = 0
    for term in tech_terms:
        icon_path = icon_provider.get_icon_path(term)
        if icon_path:
            matches += 1
            print(f"\nFound icon for {term}: {icon_path}")
            assert Path(icon_path).exists()
            save_icon_to_assets(Path(icon_path), material_icons_dir)
        else:
            print(f"\nNo icon found for {term}")
    
    # We should find icons for at least some technical terms
    assert matches > 0
    print(f"\nFound icons for {matches} out of {len(tech_terms)} technical terms") 