"""Provider chain that tries icon providers in priority order."""

import logging
from typing import Dict, Any, List, Optional

from .base import IconProvider

logger = logging.getLogger(__name__)


class ProviderChain:
    """Tries icon providers in priority order until one returns results."""

    def __init__(self, providers: Optional[List[IconProvider]] = None) -> None:
        if providers is None:
            providers = self._default_providers()
        self._providers = sorted(providers, key=lambda p: p.priority)

    @staticmethod
    def _default_providers() -> List[IconProvider]:
        """Create default provider list — bundled always, others if available."""
        providers: List[IconProvider] = []

        # Bundled is always available
        from .bundled import BundledIconProvider

        providers.append(BundledIconProvider())

        # Material if configured
        from .material import MaterialIconProviderAdapter

        mat = MaterialIconProviderAdapter()
        if mat.is_available():
            providers.append(mat)

        # Noun Project if credentials available
        from .nounproject import NounProjectProviderAdapter

        np_provider = NounProjectProviderAdapter()
        if np_provider.is_available():
            providers.append(np_provider)

        return providers

    @property
    def providers(self) -> List[IconProvider]:
        """Return the list of providers in priority order."""
        return list(self._providers)

    def search(self, term: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search providers in priority order, return first non-empty result."""
        for provider in self._providers:
            if not provider.is_available():
                continue
            try:
                results = provider.search(term, limit)
                if results:
                    logger.debug(
                        "Provider '%s' returned %d results for '%s'",
                        provider.name,
                        len(results),
                        term,
                    )
                    return results
            except Exception:
                logger.exception(
                    "Provider '%s' failed searching for '%s'", provider.name, term
                )
        return []

    def search_all(self, term: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search all available providers and aggregate results."""
        all_results: List[Dict[str, Any]] = []
        for provider in self._providers:
            if not provider.is_available():
                continue
            try:
                results = provider.search(term, limit)
                all_results.extend(results)
            except Exception:
                logger.exception(
                    "Provider '%s' failed searching for '%s'", provider.name, term
                )
        return all_results

    def get_icon(self, source: str, identifier: str) -> Optional[Dict[str, Any]]:
        """Get a specific icon from a specific provider by name."""
        for provider in self._providers:
            if provider.name == source and provider.is_available():
                try:
                    return provider.get_icon(identifier)
                except Exception:
                    logger.exception(
                        "Provider '%s' failed getting icon '%s'",
                        provider.name,
                        identifier,
                    )
        return None
