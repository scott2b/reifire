"""Module for converting reified data structures back into natural language prompts."""

from typing import Any, Callable, Dict, List, Optional


class TextRule:
    """A rule for transforming text based on a condition."""

    def __init__(
        self,
        name: str,
        condition: Callable[[str], bool],
        transform: Callable[[str], str],
        description: str,
    ):
        """Initialize a text transformation rule."""
        self.name = name
        self.condition = condition
        self.transform = transform
        self.description = description


class TextTransformer:
    """Rule-based text transformation system."""

    def __init__(self) -> None:
        """Initialize the transformer."""
        self.rules: List[TextRule] = []

    def add_rule(self, rule: TextRule) -> None:
        """Add a new transformation rule."""
        self.rules.append(rule)

    def transform(self, text: str) -> str:
        """Apply all applicable rules to transform the text."""
        result = text
        for rule in self.rules:
            if rule.condition(result):
                result = rule.transform(result)
        return result.strip()


class ArtifactRelationship:
    """Represents a relationship between artifacts in the graph."""

    def __init__(
        self,
        relationship_type: str,
        source: str,
        target: str,
        properties: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a relationship between artifacts."""
        self.type = relationship_type
        self.source = source
        self.target = target
        self.properties = properties or {}

    def articulate(self) -> str:
        """Generate natural language description of the relationship."""
        if self.type == "contains":
            position = self.properties.get("position", "")
            if position == "throughout":
                return f"with {self.target} throughout"
            elif position == "sky":
                return f"with {self.target} in the sky"
            return f"containing {self.target}"
        if self.type == "color_scheme":
            return f"with {self.target} color scheme"
        if self.type == "compares":
            aspects = self.properties.get("aspects", [])
            if aspects:
                return f"comparing {' and '.join(aspects)} with {self.target}"
            return f"comparing with {self.target}"
        if self.type == "uses":
            return f"using {self.target}"
        if self.type == "references":
            return f"referencing {self.target}"
        if self.type == "depends_on":
            return f"requiring {self.target}"
        return f"{self.type} {self.target}"


class AttributeHandler:
    """Base class for handling attribute articulation."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """Check if this handler can handle the given attribute."""
        return False

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """Convert the attribute to natural language text."""
        if isinstance(attr.get("value"), list):
            return " and ".join(str(v) for v in attr["value"])
        return str(attr.get("value", ""))


class StyleHandler(AttributeHandler):
    """Handler for style-related attributes."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """Check if this is a style-related attribute."""
        return bool(attr["name"] in ["style", "format", "theme", "tone"])

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """Convert style attribute to natural language."""
        return str(attr["value"])


class MoodHandler(AttributeHandler):
    """Handler for mood-related attributes."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """Check if this is a mood-related attribute."""
        return bool(attr["name"] == "mood")

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """Convert mood attribute to natural language."""
        return str(attr["value"])


class PropertyHandler(AttributeHandler):
    """Handler for property-based attributes."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """Check if this is a property-based attribute."""
        return bool("properties" in attr and attr["properties"])

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """Convert property-based attribute to natural language."""
        props = attr.get("properties", {})
        if not props or not isinstance(props, dict):
            return ""
        if "format" in props:
            return f"{str(props['format'])} format"
        if "context" in props:
            return f"{str(props['context'])} context"
        if "sections" in props:
            return f"covering {' and '.join(str(s) for s in props['sections'])}"
        return " ".join(f"{k}: {str(v)}" for k, v in props.items())


# Initialize global handlers
_handlers = [MoodHandler, StyleHandler, PropertyHandler]


def articulate(reified: Dict[str, Any]) -> str:
    """Convert a reified data structure back into a natural language prompt."""
    # Extract components
    obj = reified["object"]
    type_info = reified["type"]
    artifact = reified["artifact"]

    # Build prompt components
    parts = []

    # Add prefix based on type
    prefix = "Create"
    if type_info["category"] == "textual":
        if artifact["type"] == "qa":
            prefix = "Explain"
        elif artifact["type"] == "article":
            prefix = "Write"
    elif type_info["category"] == "code":
        prefix = "Implement"
    elif type_info["category"] == "data":
        prefix = "Generate"
    parts.append(prefix)

    # Get modifiers and mood
    modifiers: List[str] = []
    mood: Optional[str] = None
    if "modifiers" in obj:
        modifiers.extend(
            mod["value"] for mod in obj["modifiers"] if mod["value"] is not None
        )
    if "attributes" in artifact:
        for attr in artifact["attributes"]:
            if attr["name"] == "mood":
                mood = attr["value"]
                break

    # Build object description
    if mood:
        modifiers.insert(0, mood)  # Put mood first
    obj_desc = obj["name"]

    # Handle product properties if they exist
    if "modifiers" in obj:
        for mod in obj["modifiers"]:
            if "properties" in mod:
                props = mod["properties"]
                if "brand" in props and "model" in props:
                    obj_desc = f"{props['brand']} {props['model']}"

    if modifiers:
        if type_info["category"] == "textual" and artifact["type"] == "qa":
            # For QA types, handle "the process of X" type constructions
            if "process" in modifiers:
                obj_desc = f"the process of {obj_desc}"
            else:
                obj_desc = f"{' '.join(modifiers)} {obj_desc}"
        else:
            obj_desc = f"{' '.join(modifiers)} {obj_desc}"
    elif type_info["category"] == "textual" and artifact["type"] == "qa":
        obj_desc = f"the {obj_desc}"  # Add "the" for QA types

    # Add article if needed
    needs_article = type_info["category"] in ["visual", "code", "interactive"] or (
        type_info["category"] == "textual" and artifact["type"] == "article"
    )
    if needs_article and not obj_desc.startswith(("a ", "an ", "the ")):
        if obj_desc.lower()[0] in "aeiou":
            obj_desc = f"an {obj_desc}"
        else:
            obj_desc = f"a {obj_desc}"
    parts.append(obj_desc)

    # Process remaining attributes
    if "attributes" in artifact:
        # Group attributes by type
        styles: List[str] = []
        scene_attrs: List[str] = []
        docs: List[str] = []
        tools: List[str] = []
        data_attrs: Dict[str, Optional[str]] = {
            "operation": None,
            "grouping": None,
            "metrics": None,
            "format": None,
        }
        perspective: Optional[str] = None
        word_count: Optional[int] = None
        sections: Optional[List[str]] = None

        for attr in artifact["attributes"]:
            if attr["name"] == "mood":
                continue
            elif attr["name"] == "perspective":
                perspective = attr["value"]
            elif attr["name"] == "word_count":
                word_count = attr["value"]
            elif attr["name"] == "structure" and "properties" in attr:
                if "sections" in attr["properties"]:
                    sections = attr["properties"]["sections"]
            elif attr["name"] == "style":
                styles.append(attr["value"])
            elif attr["name"] == "tone":
                styles.append(attr["value"])
            elif attr["name"] == "complexity":
                styles.append(attr["value"])
            elif attr["name"] == "format":
                if attr["value"].lower() in ["sql", "json", "csv", "xml"]:
                    data_attrs["format"] = attr["value"]
                else:
                    styles.append(attr["value"])
            elif attr["name"] in ["time", "weather", "composition"]:
                scene_attrs.append(attr["value"])
            elif attr["name"] == "documentation":
                docs.append(attr["value"])
            elif attr["name"] in ["language", "framework", "style_system"]:
                tools.append(attr["value"])
            elif attr["name"] == "theme":
                styles.append(attr["value"])
            elif attr["name"] == "accessibility":
                parts.append("with")
                parts.append(f"{attr['value']} compliance")
            elif attr["name"] == "color scheme":
                parts.append("with")
                if "visualization" in attr:
                    parts.append(f"a {attr['visualization']['name']} color scheme")
                else:
                    parts.append(f"a {attr['value']} color scheme")
            elif attr["name"] == "operation":
                data_attrs["operation"] = attr["value"]
            elif attr["name"] == "grouping":
                if isinstance(attr["value"], list):
                    data_attrs["grouping"] = " and ".join(attr["value"])
            elif attr["name"] == "metrics":
                if isinstance(attr["value"], list):
                    data_attrs["metrics"] = " and ".join(attr["value"])

        # Add styles
        if styles:
            parts.append("in")
            if len(styles) > 1:
                last_style = styles[-1]
                other_styles = styles[:-1]
                parts.append(f"{', '.join(other_styles)}, {last_style} style")
            else:
                parts.append(f"{styles[0]} style")

        # Add perspective
        if perspective:
            parts.append(",")
            parts.append(perspective)

        # Add sections
        if sections:
            parts.append(",")
            parts.append(f"covering {', '.join(sections)}")

        # Add word count
        if word_count:
            parts.append(f"in {word_count} words")

        # Add scene attributes
        if scene_attrs:
            parts.append(", ")  # Add comma after style
            parts.append(", ".join(scene_attrs))

        # Add data attributes in specific order
        ordered_attrs: List[str] = []
        if data_attrs["operation"]:
            ordered_attrs.append(data_attrs["operation"])
        if data_attrs["grouping"]:
            ordered_attrs.append(data_attrs["grouping"])
        if data_attrs["metrics"]:
            ordered_attrs.append(data_attrs["metrics"])

        if ordered_attrs:
            parts.append(", ")
            parts.append(", ".join(ordered_attrs))
            if data_attrs["format"]:
                parts.append("in")
                parts.append(
                    data_attrs["format"].upper()
                    if data_attrs["format"].lower() in ["sql", "json", "csv", "xml"]
                    else data_attrs["format"]
                )

        # Add documentation
        if docs:
            parts.append("with")
            parts.append(f"{' '.join(docs)} documentation")

        # Add tools/technologies
        if tools:
            parts.append("using")
            parts.append(" and ".join(tools))

    # Add relationships
    if "relationships" in artifact:
        rels: List[str] = []
        positioned_contains: Dict[str, List[str]] = {}
        unpositioned_contains: List[str] = []

        for rel_data in artifact["relationships"]:
            rel = ArtifactRelationship(
                rel_data["type"],
                rel_data.get("source", ""),
                rel_data["target"],
                rel_data.get("properties"),
            )
            if rel.type == "contains":
                position = rel_data.get("properties", {}).get("position", "")
                if position:
                    if position not in positioned_contains:
                        positioned_contains[position] = []
                    positioned_contains[position].append(rel.target)
                else:
                    unpositioned_contains.append(rel.target)
            else:
                result = rel.articulate()
                if result:
                    rels.append(result)

        # Handle positioned contains
        for position, targets in positioned_contains.items():
            if position == "throughout":
                rels.append(f"with {' and '.join(targets)} throughout")
            elif position == "sky":
                rels.append(f"with {' and '.join(targets)} in the sky")
            else:
                rels.append(f"with {' and '.join(targets)} {position}")

        # Handle unpositioned contains
        if unpositioned_contains:
            rels.append(f"containing {' and '.join(unpositioned_contains)}")

        if rels:
            # Add comma before relationships if we have previous content
            if parts:
                parts.append(",")
            parts.extend(rels)

    # Combine parts
    prompt = " ".join(filter(None, parts))

    # Clean up spaces around commas
    prompt = prompt.replace(" ,", ",")
    prompt = prompt.replace(",,", ",")
    prompt = prompt.replace(",", ", ")
    prompt = " ".join(prompt.split())

    # Ensure proper punctuation
    if not prompt.endswith("."):
        prompt += "."

    return prompt


def articulate_alternatives(reified: Dict[str, Any], alt_path: List[str]) -> str:
    """Create a variant of the prompt by following an alternative path."""
    import copy

    modified = copy.deepcopy(reified)

    for path in alt_path:
        parts = path.split(".")
        current = modified  # type: Any

        # Navigate to the parent of the target
        for part in parts[:-1]:
            if isinstance(current, dict):
                current = current[part]
            elif isinstance(current, list) and part.isdigit():
                current = current[int(part)]

        # Handle the target element
        last = parts[-1]
        if isinstance(current, dict) and last in current:
            target = current[last]
            if isinstance(target, dict) and "alternatives" in target:
                current[last] = target["alternatives"][0]
        elif isinstance(current, list) and last.isdigit():
            idx = int(last)
            if 0 <= idx < len(current):
                target = current[idx]
                if isinstance(target, dict) and "alternatives" in target:
                    current[idx] = target["alternatives"][0]

    return articulate(modified)
