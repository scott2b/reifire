"""Module for converting natural language prompts into reified data structures."""

from typing import Dict, Any, Optional
from .visualization.metadata import IconMetadata
from .visualization.registry import IconRegistry


class ReifiedConcept:
    """Base class for reified concepts."""

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
        self.icon: Optional[IconMetadata] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        data = self.data.copy()
        if self.icon:
            data["_icon"] = self.icon.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReifiedConcept":
        """Create from dictionary representation."""
        icon_data = data.pop("_icon", None)
        concept = cls(data)
        if icon_data:
            concept.icon = IconMetadata.from_dict(icon_data)
        return concept

    def set_icon(
        self,
        registry: IconRegistry,
        term: Optional[str] = None,
        icon_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Set an icon for this concept."""
        term = term or self.data.get("type", "")
        if icon_id:
            self.icon = IconMetadata(
                icon_id=icon_id, term=term, metadata=metadata or {}
            )
            registry.associate_icon(term, icon_id, metadata)
        else:
            suggestions = registry.suggest_icons(term)
            if suggestions:
                best_match = suggestions[0]
                best_id = best_match.get("id", best_match.get("name", ""))
                self.icon = IconMetadata(
                    icon_id=best_id,
                    term=term,
                    source=best_match.get("source", "bundled"),
                    metadata=metadata or {},
                )
                registry.associate_icon(term, best_id, metadata)

    def clear_icon(self) -> None:
        """Remove the icon from this concept."""
        self.icon = None


def reify(prompt: str, provider_chain: Optional[Any] = None) -> Dict[str, Any]:
    """
    Reify a natural language prompt into a structured representation.

    Args:
        prompt: The natural language prompt to reify.
        provider_chain: Optional ProviderChain for icon resolution.
            If None, creates a default chain (bundled icons always available).

    Returns:
        A dictionary containing the reified structure.
    """
    import warnings

    if provider_chain is None:
        from .visualization.providers.chain import ProviderChain

        provider_chain = ProviderChain()

    # Basic structure
    reified: Dict[str, Any] = {
        "object": {
            "name": prompt,
            "modifiers": [],
            "description": prompt,
            "variants": [],
            "properties": {},
        },
        "type": {"name": "concept", "category": "general", "properties": {}},
        "artifact": {
            "type": "visualization",
            "attributes": [],
            "visualization": None,
            "relationships": [],
            "properties": {},
        },
        "metadata": {
            "original_prompt": prompt,
            "version": "0.1.0",
        },
    }

    # Extract keywords using Spacy
    keywords = []
    try:
        import spacy

        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            from spacy.cli import download

            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")

        doc = nlp(prompt)

        # Extract nouns, proper nouns, verbs, and adjectives
        keywords = [
            token.lemma_
            for token in doc
            if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ"]
        ]

        # Fallback to all words if no keywords found
        if not keywords:
            keywords = [
                token.text
                for token in doc
                if not token.is_stop and not token.is_punct
            ]
    except Exception as e:
        warnings.warn(f"NLP extraction failed: {e}")
        keywords = prompt.split()

    # If prompt itself is short/simple, treat it as a keyword too
    if len(prompt.split()) <= 2 and prompt not in keywords:
        keywords.insert(0, prompt)

    # Deduplicate while preserving order
    keywords = list(dict.fromkeys(keywords))

    # Search for icons for each keyword
    found_icons = []
    for keyword in keywords:
        try:
            results = provider_chain.search(keyword, limit=1)
            if results:
                icon_data = results[0]
                viz = {
                    "source": icon_data.get("source", "bundled"),
                    "name": icon_data.get("name", keyword),
                    "image": icon_data.get("image", ""),
                    "attribution": icon_data.get("attribution", ""),
                    "properties": icon_data.get("metadata", {}),
                }
                found_icons.append({"keyword": keyword, "visualization": viz})
        except Exception as e:
            warnings.warn(f"Failed to search for {keyword}: {e}")

    if found_icons:
        reified["artifact"]["visualization"] = found_icons[0]["visualization"]
        reified["artifact"]["attributes"] = [
            {
                "name": item["keyword"],
                "value": "present",
                "category": "element",
                "visualization": item["visualization"],
            }
            for item in found_icons
        ]
    else:
        warnings.warn(f"No icons found for prompt '{prompt}' or its keywords.")

    return reified
