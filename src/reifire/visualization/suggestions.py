from typing import List, Dict, Any, Optional
import json
from pathlib import Path
from dataclasses import dataclass
import nltk
from nltk.corpus import wordnet


@dataclass
class ScoredIcon:
    """Icon with relevance score."""

    icon_data: Dict[str, Any]
    score: float


class IconSuggester:
    """Suggests icons based on terms and context."""

    def __init__(self, usage_data_path: Optional[Path] = None) -> None:
        """Initialize the suggester."""
        self.usage_data_path = (
            usage_data_path or Path.home() / ".reifire" / "icon_usage.json"
        )
        self.usage_data_path.parent.mkdir(parents=True, exist_ok=True)
        self._load_usage_data()

        # Download required NLTK data
        try:
            nltk.data.find("corpora/wordnet")
        except LookupError:
            nltk.download("wordnet", quiet=True)

    def _load_usage_data(self) -> None:
        """Load icon usage statistics."""
        self.usage_data: Dict[str, Dict[str, int]] = {}
        if self.usage_data_path.exists():
            self.usage_data = json.loads(self.usage_data_path.read_text())

    def _save_usage_data(self) -> None:
        """Save icon usage statistics."""
        self.usage_data_path.write_text(json.dumps(self.usage_data, indent=2))

    def get_related_terms(self, term: str) -> List[str]:
        """Get related terms using WordNet."""
        related_terms: set[str] = set()

        # Get synsets for the term
        synsets = wordnet.synsets(term)
        for synset in synsets:
            # Add synonyms
            related_terms.update(lemma.name() for lemma in synset.lemmas())

            # Add hypernyms (more general terms)
            for hypernym in synset.hypernyms():
                related_terms.update(lemma.name() for lemma in hypernym.lemmas())

            # Add hyponyms (more specific terms)
            for hyponym in synset.hyponyms():
                related_terms.update(lemma.name() for lemma in hyponym.lemmas())

        # Remove the original term and clean up underscores
        related_terms.discard(term)
        return [t.replace("_", " ") for t in related_terms]

    def record_selection(self, term: str, icon_id: str) -> None:
        """Record that an icon was selected for a term."""
        if term not in self.usage_data:
            self.usage_data[term] = {}
        self.usage_data[term][icon_id] = self.usage_data[term].get(icon_id, 0) + 1
        self._save_usage_data()

    def score_icon(
        self, icon: Dict[str, Any], term: str, context: Optional[Dict[str, Any]] = None
    ) -> float:
        """Score an icon's relevance."""
        score = 0.0
        term = term.lower()

        # Direct term match
        if term in icon.get("term", "").lower():
            score += 0.5

        # Tag matches
        tags = [t.lower() for t in icon.get("tags", [])]
        if term in tags:
            score += 0.3

        # Related term matches
        related = self.get_related_terms(term)
        if any(r.lower() in icon.get("term", "").lower() for r in related):
            score += 0.2
        if any(r.lower() in tag for r in related for tag in tags):
            score += 0.1

        # Usage history
        if term in self.usage_data and icon["id"] in self.usage_data[term]:
            usage_score = self.usage_data[term][icon["id"]] / max(
                self.usage_data[term].values()
            )
            score += 0.2 * usage_score

        return min(score, 1.0)

    def sort_suggestions(
        self,
        icons: List[Dict[str, Any]],
        term: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Sort icon suggestions by relevance score."""
        scored_icons = [
            ScoredIcon(icon, self.score_icon(icon, term, context)) for icon in icons
        ]
        scored_icons.sort(key=lambda x: x.score, reverse=True)
        return [icon.icon_data for icon in scored_icons]
