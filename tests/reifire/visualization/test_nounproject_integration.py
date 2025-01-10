import os
import pytest
from typing import Generator
from reifire.visualization.nounproject import NounProjectClient
from pathlib import Path
import tempfile
import requests
import webbrowser


@pytest.fixture
def api_client() -> Generator[NounProjectClient, None, None]:
    """Create a client with API credentials from environment variables."""
    api_key = os.environ.get("NOUN_PROJECT_API_KEY")
    api_secret = os.environ.get("NOUN_PROJECT_API_SECRET")

    if not api_key or not api_secret:
        pytest.skip("Noun Project API credentials not found in environment")

    with tempfile.TemporaryDirectory() as tmpdir:
        yield NounProjectClient(
            api_key=api_key, api_secret=api_secret, cache_dir=Path(tmpdir)
        )


def download_and_open_icon(url: str, save_dir: Path, filename: str) -> None:
    """Download an icon and open it in the default viewer."""
    save_path = save_dir / filename
    print(f"Downloading from: {url}")
    response = requests.get(url)
    response.raise_for_status()
    save_path.write_bytes(response.content)
    print(f"Saved to: {save_path}")
    webbrowser.open(f"file://{save_path.absolute()}")


@pytest.mark.integration
def test_search_icons_integration(api_client: NounProjectClient) -> None:
    """Test that we can actually search for icons."""
    result = api_client.search_icons("computer")
    print(f"\nGot {len(result.get('icons', []))} results")
    assert "icons" in result
    assert len(result["icons"]) > 0

    # Create a directory for downloaded icons
    icon_dir = Path.cwd() / "downloaded_icons"
    icon_dir.mkdir(exist_ok=True)

    print("\nSearch Results:")
    for i, icon in enumerate(result["icons"][:5]):  # Show first 5 results
        print(f"{i+1}. {icon['attribution']}")
        print(f"   ID: {icon['id']}")
        print(f"   Available fields: {list(icon.keys())}")
        print(f"   Tags: {', '.join(icon.get('tags', []))}")
        if "thumbnail_url" in icon:
            print(f"   Thumbnail: {icon['thumbnail_url']}")
            # Download and open the icon
            download_and_open_icon(
                icon["thumbnail_url"], icon_dir, f"icon_{icon['id']}.png"
            )
        else:
            print("   No thumbnail URL available")
        print()


@pytest.mark.integration
def test_get_icon_integration(api_client: NounProjectClient) -> None:
    """Test that we can fetch a specific icon."""
    # First search for an icon
    search_result = api_client.search_icons("computer", limit=1)
    icon_id = search_result["icons"][0]["id"]

    # Then fetch its details
    icon = api_client.get_icon(icon_id)
    assert icon["id"] == icon_id
    print("\nDetailed Icon Info:")
    print(f"Attribution: {icon['attribution']}")
    print(f"ID: {icon['id']}")
    print(f"Tags: {', '.join(icon.get('tags', []))}")
    if "thumbnail_url" in icon:
        print(f"Thumbnail URL: {icon['thumbnail_url']}")
    print(f"License: {icon.get('license_description', 'N/A')}")
    if "term" in icon:
        print(f"Term: {icon['term']}")


@pytest.mark.integration
def test_caching_integration(api_client: NounProjectClient) -> None:
    """Test that caching works with real requests."""
    # First request should hit the API
    result1 = api_client.get_icon("1")

    # Second request should use cache
    result2 = api_client.get_icon("1")
    assert result2 == result1

    print("\nCaching test: second request used cached data")
