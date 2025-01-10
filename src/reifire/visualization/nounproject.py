from typing import Optional, Dict, Any
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
        self.auth = OAuth1(api_key, api_secret)
        self.cache_dir = cache_dir or Path.home() / ".reifire" / "icon_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.rate_limit = rate_limit
        self._last_request_time: float = 0.0

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
        response = requests.request(method, url, auth=self.auth, params=params)

        try:
            response.raise_for_status()
            data: Dict[str, Any] = response.json()
            return data
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"API request failed: {e}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from API")

    @lru_cache(maxsize=1000)
    def get_icon(self, icon_id: str) -> Dict[str, Any]:
        """Retrieve a specific icon by ID."""
        cache_file = self.cache_dir / f"icon_{icon_id}.json"

        if cache_file.exists():
            data: Dict[str, Any] = json.loads(cache_file.read_text())
            return data

        response = self._make_request(f"icon/{icon_id}")
        data = response.get("icon", response)  # Handle both response formats
        cache_file.write_text(json.dumps(data))
        return data

    def search_icons(self, term: str, limit: int = 10) -> Dict[str, Any]:
        """Search for icons matching a term."""
        return self._make_request(
            "icon",
            params={
                "query": term,
                "limit": limit,
                "preview_size": 84,  # Request preview URLs at 84px size
            },
        )
