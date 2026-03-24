"""Bundled icon provider — ships curated Lucide + Octicons SVGs with the package."""

import base64
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

ICONS_DIR = Path(__file__).parent / "icons"


class BundledIconProvider:
    """Zero-config icon provider using SVGs bundled with the package."""

    def __init__(self) -> None:
        self._manifest: Optional[Dict[str, Any]] = None
        self._svg_cache: Dict[str, str] = {}

    @property
    def name(self) -> str:
        return "bundled"

    @property
    def priority(self) -> int:
        return 10

    def is_available(self) -> bool:
        return (ICONS_DIR / "manifest.json").exists()

    def _load_manifest(self) -> Dict[str, Any]:
        if self._manifest is None:
            manifest_path = ICONS_DIR / "manifest.json"
            self._manifest = json.loads(manifest_path.read_text())
        assert self._manifest is not None
        return self._manifest

    def _svg_to_data_uri(self, svg_path: Path) -> str:
        """Read an SVG file and return a base64 data URI."""
        cache_key = str(svg_path)
        if cache_key not in self._svg_cache:
            svg_content = svg_path.read_bytes()
            b64 = base64.b64encode(svg_content).decode()
            self._svg_cache[cache_key] = f"data:image/svg+xml;base64,{b64}"
        return self._svg_cache[cache_key]

    def _match_terms(self, term: str, limit: int) -> List[str]:
        """Find icon IDs matching a search term."""
        manifest = self._load_manifest()
        term_index = manifest.get("term_index", {})
        normalized = term.lower().replace(" ", "-").replace("_", "-")

        # Collect matches with rough relevance scoring
        scored: List[tuple[int, str]] = []
        seen: Set[str] = set()

        # Exact match on term
        if normalized in term_index:
            for icon_id in term_index[normalized]:
                if icon_id not in seen:
                    scored.append((0, icon_id))
                    seen.add(icon_id)

        # Try individual words
        words = normalized.split("-")
        for word in words:
            if word in term_index:
                for icon_id in term_index[word]:
                    if icon_id not in seen:
                        scored.append((1, icon_id))
                        seen.add(icon_id)

        # Try plural/singular
        for word in words:
            variants = []
            if word.endswith("s") and len(word) > 2:
                variants.append(word[:-1])
            else:
                variants.append(word + "s")
            for variant in variants:
                if variant in term_index:
                    for icon_id in term_index[variant]:
                        if icon_id not in seen:
                            scored.append((2, icon_id))
                            seen.add(icon_id)

        # Substring match on icon tags
        if not scored:
            icons = manifest.get("icons", {})
            for icon_id, entry in icons.items():
                if icon_id in seen:
                    continue
                for tag in entry.get("tags", []):
                    if normalized in tag or tag in normalized:
                        scored.append((3, icon_id))
                        seen.add(icon_id)
                        break

        scored.sort(key=lambda x: x[0])
        return [icon_id for _, icon_id in scored[:limit]]

    def search(self, term: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search bundled icons by term."""
        if not self.is_available():
            return []

        manifest = self._load_manifest()
        icons = manifest.get("icons", {})
        matched_ids = self._match_terms(term, limit)
        results = []

        for icon_id in matched_ids:
            entry = icons.get(icon_id)
            if not entry:
                continue
            svg_path = ICONS_DIR / entry["file"]
            if not svg_path.exists():
                continue
            results.append({
                "id": icon_id,
                "name": entry["name"],
                "source": self.name,
                "image": self._svg_to_data_uri(svg_path),
                "tags": entry.get("tags", []),
            })

        return results

    def get_icon(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get a specific bundled icon by its ID (e.g. 'lucide/package')."""
        if not self.is_available():
            return None

        manifest = self._load_manifest()
        icons = manifest.get("icons", {})
        entry = icons.get(identifier)
        if not entry:
            return None

        svg_path = ICONS_DIR / entry["file"]
        if not svg_path.exists():
            return None

        return {
            "id": identifier,
            "name": entry["name"],
            "source": self.name,
            "image": self._svg_to_data_uri(svg_path),
            "tags": entry.get("tags", []),
        }
