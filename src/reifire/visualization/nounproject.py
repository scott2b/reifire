"""Client for interacting with The Noun Project API."""

from typing import Dict, Any, Optional, cast
import requests
from requests_oauthlib import OAuth1
from pathlib import Path
import json
import time
from functools import lru_cache


class NounProjectClient:
    """Client for interacting with The Noun Project API."""

    BASE_URL = "https://api.thenounproject.com/v2"

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        cache_dir: Optional[Path] = None,
        rate_limit: int = 50,  # requests per minute
    ) -> None:
        """Initialize the Noun Project client.

        Args:
            api_key: The Noun Project API key
            api_secret: The Noun Project API secret
            cache_dir: Optional directory for caching icon data
            rate_limit: Maximum requests per minute

        Raises:
            ValueError: If credentials are missing or invalid
        """
        if not api_key or not api_secret:
            raise ValueError(
                "Noun Project API credentials not provided. "
                "Set NOUN_PROJECT_KEY and NOUN_PROJECT_SECRET environment variables "
                "or pass them directly to the constructor."
            )

        # Only show first few characters of credentials in logs
        key_preview = api_key[:4] if len(api_key) >= 4 else "****"
        print(f"Initializing Noun Project client with key: {key_preview}...")

        self.auth = OAuth1(
            client_key=api_key,
            client_secret=api_secret,
            signature_type="auth_header",
            signature_method="HMAC-SHA1",
        )
        self.cache_dir = cache_dir or Path.home() / ".reifire" / "icon_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.rate_limit = rate_limit
        self._last_request_time: float = 0.0

        # Test the credentials with a simple API call
        try:
            # Use the client/usage endpoint for authentication test
            self._make_request("client/usage")
            print("Successfully authenticated with Noun Project API")
        except Exception as e:
            raise ValueError(f"Failed to authenticate with Noun Project API: {e}")

    def _rate_limit_wait(self) -> None:
        """Implement basic rate limiting."""
        current_time = time.time()
        elapsed = current_time - self._last_request_time
        min_interval = 60.0 / self.rate_limit

        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)

        self._last_request_time = current_time

    def _make_request(
        self, endpoint: str, method: str = "GET", params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make a rate-limited request to the API."""
        self._rate_limit_wait()

        url = f"{self.BASE_URL}/{endpoint}"
        print(f"Making API request to: {url}")
        if params:
            print(f"With parameters: {params}")

        try:
            response = requests.request(method, url, auth=self.auth, params=params)
            response.raise_for_status()
            print(f"Got response status: {response.status_code}")
            raw_data = response.json()
            # Explicitly cast the response to Dict[str, Any]
            data: Dict[str, Any] = cast(Dict[str, Any], raw_data)
            return data
        except requests.exceptions.HTTPError as e:
            response = cast(requests.Response, e.response)
            print(f"HTTP error: {e}")
            print(
                f"Response content: {response.text if response else 'No response content'}"
            )
            if response and response.status_code == 404:
                return {"error": "not_found"}
            raise ValueError(f"API request failed: {e}")
        except (json.JSONDecodeError, requests.exceptions.RequestException) as e:
            print(f"Request error: {e}")
            if hasattr(e, "response"):
                response = cast(requests.Response, getattr(e, "response"))
                if response and hasattr(response, "text"):
                    print(f"Response content: {response.text}")
            raise ValueError("API request failed")

    @lru_cache(maxsize=1000)
    def get_icon(self, icon_id: str) -> Dict[str, Any]:
        """Retrieve a specific icon by ID.

        Args:
            icon_id: The ID of the icon to retrieve

        Returns:
            A dictionary containing the icon data
        """
        print(f"Getting icon details for ID: {icon_id}")
        cache_file = self.cache_dir / f"icon_{icon_id}.json"

        if cache_file.exists():
            print("Found cached icon data")
            try:
                raw_data = json.loads(cache_file.read_text())
                data: Dict[str, Any] = cast(Dict[str, Any], raw_data)
                return data
            except json.JSONDecodeError:
                print("Invalid cached data, fetching fresh data")
                cache_file.unlink(missing_ok=True)

        print("Fetching icon data from API")
        response = self._make_request(f"icon/{icon_id}")

        if response.get("error") == "not_found":
            print(f"Icon {icon_id} not found")
            return {"error": "not_found"}

        # Extract the icon data and ensure it has a preview URL
        raw_icon_data = response.get("icon", {})
        icon_data: Dict[str, Any] = cast(Dict[str, Any], raw_icon_data)
        if not icon_data:
            print("No icon data in response")
            return {"error": "no_data"}

        if "preview_url" not in icon_data and "preview_url_84" in icon_data:
            icon_data["preview_url"] = icon_data["preview_url_84"]

        if "preview_url" not in icon_data and "icon_url" in icon_data:
            icon_data["preview_url"] = icon_data["icon_url"]

        if "preview_url" not in icon_data:
            print("No preview URL available")

        print(f"Got icon data with preview URL: {icon_data.get('preview_url')}")
        cache_file.write_text(json.dumps(icon_data))
        return icon_data

    def search_icons(self, term: str, limit: int = 10) -> Dict[str, Any]:
        """Search for icons matching a term.

        Args:
            term: The search term
            limit: Maximum number of results to return

        Returns:
            A dictionary containing the search results
        """
        print(f"Searching for icons matching term: {term}")
        response = self._make_request(
            "collection",
            params={
                "query": term,
                "limit": limit,
            },
        )

        # Extract and process the icons from the response
        collections = response.get("collections", [])
        if not collections:
            return {"icons": []}

        # Get the first collection's icons
        collection_id = collections[0]["id"]
        collection_response = self._make_request(
            f"collection/{collection_id}",
            params={
                "limit": limit,
                "thumbnail_size": 84,  # API docs specify valid sizes: 42, 84, 200
                "include_svg": 1,  # API docs specify this is needed for SVG URLs
            },
        )

        collection = collection_response.get("collection", {})
        icons = collection.get("icons", [])
        print(f"Found {len(icons)} icons")

        # Filter out icons without preview URLs and ensure each has one
        valid_icons = []
        for icon in icons:
            if "preview_url" not in icon and "thumbnail_url" in icon:
                icon["preview_url"] = icon["thumbnail_url"]
            if "preview_url" in icon:
                valid_icons.append(icon)
            else:
                print(f"Skipping icon {icon.get('id')} - no preview URL")

        if not valid_icons:
            print("No valid icons found with preview URLs")
        else:
            print(f"Returning {len(valid_icons)} valid icons")

        return {"icons": valid_icons}
