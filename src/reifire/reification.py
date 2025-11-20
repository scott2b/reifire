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
            # Use specific icon
            self.icon = IconMetadata(
                icon_id=icon_id, term=term, metadata=metadata or {}
            )
            registry.associate_icon(term, icon_id, metadata)
        else:
            # Get suggestions and use the best match
            suggestions = registry.suggest_icons(term)
            if suggestions:
                best_match = suggestions[0]
                self.icon = IconMetadata(
                    icon_id=best_match["id"], term=term, metadata=metadata or {}
                )
                registry.associate_icon(term, best_match["id"], metadata)

    def clear_icon(self) -> None:
        """Remove the icon from this concept."""
        self.icon = None


def reify(prompt: str) -> Dict[str, Any]:
    """
    Reify a natural language prompt into a structured representation.

    Args:
        prompt: The natural language prompt to reify.

    Returns:
        A dictionary containing the reified structure.
    """
    import os
    from .visualization.nounproject import NounProjectClient

    # Basic structure
    reified = {
        "object": {
            "name": prompt,  # Simplified: using whole prompt as object name for now
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
            # "timestamp": ... # TODO: Add timestamp
        },
    }

    import warnings

    # Try to get visualization from Noun Project
    api_key = os.environ.get("NOUNPROJECT_API_KEY") or os.environ.get("NOUN_PROJECT_KEY")
    api_secret = os.environ.get("NOUNPROJECT_API_SECRET") or os.environ.get(
        "NOUN_PROJECT_SECRET"
    )

    if api_key and api_secret:
        try:
            client = NounProjectClient(api_key, api_secret)
            
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
                # Use lemma_ for better search results (e.g. "raining" -> "rain", "cats" -> "cat")
                keywords = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ"]]
                
                # Fallback to all words if no nouns found
                if not keywords:
                    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
            except Exception as e:
                warnings.warn(f"NLP extraction failed: {e}")
                # Fallback to simple split if NLP fails
                keywords = prompt.split()

            # If prompt itself is short/simple, treat it as a keyword too
            if len(prompt.split()) <= 2 and prompt not in keywords:
                keywords.insert(0, prompt)

            # Deduplicate while preserving order
            keywords = list(dict.fromkeys(keywords))

            found_icons = []
            for keyword in keywords:
                try:
                    results = client.search_icons(keyword, limit=1)
                    icons = results.get("icons", [])
                    if icons:
                        icon_data = icons[0]
                        viz = {
                            "source": "nounproject",
                            "name": icon_data.get("term", keyword),
                            "image": icon_data.get("preview_url"),
                            "attribution": f"Created by {icon_data.get('uploader', {}).get('name', 'Unknown')} from the Noun Project",
                            "properties": {"icon_id": icon_data.get("id")},
                        }
                        found_icons.append({"keyword": keyword, "visualization": viz})
                except Exception as e:
                    print(f"Failed to search for {keyword}: {e}")

            if found_icons:
                # Use the first found icon as the primary visualization
                reified["artifact"]["visualization"] = found_icons[0]["visualization"]
                
                # Add all found icons as attributes
                reified["artifact"]["attributes"] = []
                for item in found_icons:
                    reified["artifact"]["attributes"].append({
                        "name": item["keyword"],
                        "value": "present",
                        "category": "element",
                        "visualization": item["visualization"]
                    })
            else:
                warnings.warn(f"No icons found for prompt '{prompt}' or its keywords.")
        except Exception as e:
            warnings.warn(f"Failed to fetch icon from Noun Project: {e}")
    else:
        warnings.warn(
            "Noun Project API keys not found. Visualization will be empty. "
            "Please set NOUNPROJECT_API_KEY and NOUNPROJECT_API_SECRET environment variables."
        )


    return reified
