"""LLM-powered SVG icon generation provider using Pydantic AI."""

import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = Path.home() / ".reifire" / "llm_icons"

SVG_SYSTEM_PROMPT = """\
You are an icon designer. Generate clean, simple SVG icons suitable for use as UI icons.

Rules:
- Output a single SVG element with viewBox="0 0 24 24"
- Use only path, circle, rect, line, polyline, polygon elements
- Use stroke-based design (stroke="currentColor", fill="none", stroke-width="2",
  stroke-linecap="round", stroke-linejoin="round")
- Keep it simple — 1-3 shapes maximum
- No text elements, no embedded images, no gradients
- No XML declaration or doctype — just the <svg> element
"""


class LLMSVGProvider:
    """Generate SVG icons on demand using an LLM via Pydantic AI.

    Requires the `pydantic-ai` package to be installed. The provider is
    unavailable if the package is not present.

    Usage:
        provider = LLMSVGProvider(model="anthropic:claude-haiku-4-5-20251001")
        results = provider.search("database")
    """

    def __init__(
        self,
        model: Optional[str] = None,
        cache_dir: Optional[Path] = None,
    ) -> None:
        """Initialize the LLM SVG provider.

        Args:
            model: Pydantic AI model string (e.g. "anthropic:claude-haiku-4-5-20251001",
                   "openai:gpt-4o-mini"). If None, uses pydantic-ai default.
            cache_dir: Directory for caching generated SVGs. Defaults to ~/.reifire/llm_icons/
        """
        self._model = model
        self._cache_dir = cache_dir or DEFAULT_CACHE_DIR
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._agent = None
        self._pydantic_ai_available = self._check_pydantic_ai()

    def _check_pydantic_ai(self) -> bool:
        """Check if pydantic-ai is installed and set up the agent."""
        try:
            from pydantic import BaseModel
            from pydantic_ai import Agent

            class GeneratedIcon(BaseModel):
                svg: str
                name: str
                tags: list[str]

            self._generated_icon_cls = GeneratedIcon
            agent_kwargs: Dict[str, Any] = {
                "system_prompt": SVG_SYSTEM_PROMPT,
                "output_type": GeneratedIcon,
            }
            if self._model:
                agent_kwargs["model"] = self._model

            self._agent = Agent(**agent_kwargs)
            return True
        except ImportError:
            logger.debug("pydantic-ai not installed — LLM SVG provider unavailable")
            return False

    @property
    def name(self) -> str:
        return "llm_svg"

    @property
    def priority(self) -> int:
        return 80

    def is_available(self) -> bool:
        return self._pydantic_ai_available and self._agent is not None

    def _cache_key(self, term: str) -> str:
        """Generate a filesystem-safe cache key for a term."""
        return hashlib.sha256(term.lower().encode()).hexdigest()[:16]

    def _get_cached(self, term: str) -> Optional[Dict[str, Any]]:
        """Look up a cached icon."""
        cache_file = self._cache_dir / f"{self._cache_key(term)}.json"
        if cache_file.exists():
            try:
                return json.loads(cache_file.read_text())
            except (json.JSONDecodeError, OSError):
                return None
        return None

    def _save_cache(self, term: str, result: Dict[str, Any]) -> None:
        """Save a generated icon to cache."""
        cache_file = self._cache_dir / f"{self._cache_key(term)}.json"
        try:
            cache_file.write_text(json.dumps(result))
        except OSError:
            logger.warning("Failed to cache LLM icon for '%s'", term)

    def _svg_to_data_uri(self, svg: str) -> str:
        """Convert SVG string to a data URI."""
        import base64

        b64 = base64.b64encode(svg.encode()).decode()
        return f"data:image/svg+xml;base64,{b64}"

    def search(self, term: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Generate an SVG icon for the given term."""
        if not self.is_available():
            return []

        # Check cache first
        cached = self._get_cached(term)
        if cached:
            logger.debug("Cache hit for LLM icon '%s'", term)
            return [cached]

        # Generate via LLM
        try:
            result = self._agent.run_sync(
                f"Generate a simple icon for the concept: {term}"
            )
            icon_data = result.output

            entry = {
                "id": f"llm/{self._cache_key(term)}",
                "name": icon_data.name,
                "source": self.name,
                "image": self._svg_to_data_uri(icon_data.svg),
                "tags": icon_data.tags,
            }
            self._save_cache(term, entry)
            return [entry]
        except Exception:
            logger.exception("LLM SVG generation failed for '%s'", term)
            return []

    def get_icon(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get a cached LLM-generated icon by identifier."""
        # Identifier format: "llm/{hash}" — extract hash and look up cache
        if identifier.startswith("llm/"):
            cache_hash = identifier[4:]
            cache_file = self._cache_dir / f"{cache_hash}.json"
            if cache_file.exists():
                try:
                    return json.loads(cache_file.read_text())
                except (json.JSONDecodeError, OSError):
                    pass
        return None
