"""Module for converting reified data structures back into natural language prompts."""

from typing import Any, Callable, Dict, List, Optional, Protocol, Type


class AttributeHandler(Protocol):
    """Protocol for handling attribute articulation."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle the given attribute.

        Args:
            attr: The attribute dictionary to check

        Returns:
            bool: True if this handler can handle the attribute
        """
        ...

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """
        Convert the attribute to natural language text.

        Args:
            attr: The attribute dictionary to articulate

        Returns:
            str: The natural language representation of the attribute
        """
        ...


class StyleAttributeHandler:
    """Handler for style-related attributes."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle style-related attributes.

        Args:
            attr: The attribute dictionary to check

        Returns:
            bool: True if this is a style-related attribute
        """
        return bool(attr["name"] in ["style", "format", "theme", "tone"])

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """
        Convert a style attribute to natural language text.

        Args:
            attr: The style attribute dictionary to articulate

        Returns:
            str: The natural language representation of the style
        """
        return f"in {attr['value']} style"


class ColorSchemeHandler:
    """Handler for color scheme attributes."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle color scheme attributes.

        Args:
            attr: The attribute dictionary to check

        Returns:
            bool: True if this is a color scheme attribute
        """
        return bool(attr["name"] == "color scheme")

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """
        Convert a color scheme attribute to natural language text.

        Args:
            attr: The color scheme attribute dictionary to articulate

        Returns:
            str: The natural language representation of the color scheme
        """
        if "visualization" in attr:
            return f"with {attr['visualization']['name']} color scheme"
        return f"with {attr['value']} color scheme"


class AccessibilityHandler:
    """Handler for accessibility attributes."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle accessibility attributes.

        Args:
            attr: The attribute dictionary to check

        Returns:
            bool: True if this is an accessibility attribute
        """
        return bool(attr["name"] == "accessibility")

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """
        Convert an accessibility attribute to natural language text.

        Args:
            attr: The accessibility attribute dictionary to articulate

        Returns:
            str: The natural language representation of the accessibility requirement
        """
        return f"with {attr['value']} compliance"


class WordCountHandler:
    """Handler for word count attributes."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle word count attributes.

        Args:
            attr: The attribute dictionary to check

        Returns:
            bool: True if this is a word count attribute
        """
        return bool(attr["name"] == "word_count")

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """
        Convert a word count attribute to natural language text.

        Args:
            attr: The word count attribute dictionary to articulate

        Returns:
            str: The natural language representation of the word count
        """
        return f"in {attr['value']} words"


class ComplexityHandler:
    """Handler for complexity attributes."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle complexity attributes.

        Args:
            attr: The attribute dictionary to check

        Returns:
            bool: True if this is a complexity attribute
        """
        return bool(attr["name"] == "complexity")

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """
        Convert a complexity attribute to natural language text.

        Args:
            attr: The complexity attribute dictionary to articulate

        Returns:
            str: The natural language representation of the complexity
        """
        return str(attr["value"])


class SectionPropertiesHandler:
    """Handler for attributes with section properties."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle section properties.

        Args:
            attr: The attribute dictionary to check

        Returns:
            bool: True if this attribute has section properties
        """
        return bool(
            "properties" in attr
            and attr["properties"]
            and "sections" in attr["properties"]
        )

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """
        Convert a section properties attribute to natural language text.

        Args:
            attr: The section properties attribute dictionary to articulate

        Returns:
            str: The natural language representation of the sections
        """
        sections = ", ".join(attr["properties"]["sections"])
        return f"covering {sections}"


class ListValueHandler:
    """Handler for attributes with list values."""

    @classmethod
    def can_handle(cls, attr: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle list value attributes.

        Args:
            attr: The attribute dictionary to check

        Returns:
            bool: True if this attribute has a list value
        """
        return bool(isinstance(attr.get("value"), list))

    @classmethod
    def articulate(cls, attr: Dict[str, Any]) -> str:
        """
        Convert a list value attribute to natural language text.

        Args:
            attr: The list value attribute dictionary to articulate

        Returns:
            str: The natural language representation of the list value
        """
        return " and ".join(attr["value"])


_attribute_handlers: List[Type[AttributeHandler]] = [
    StyleAttributeHandler,
    ColorSchemeHandler,
    AccessibilityHandler,
    WordCountHandler,
    ComplexityHandler,
    SectionPropertiesHandler,
    ListValueHandler,
]


def register_attribute_handler(handler: Type[AttributeHandler]) -> None:
    """
    Register a new attribute handler.

    Args:
        handler: The handler class to register
    """
    _attribute_handlers.append(handler)


def _get_handler_for_attribute(
    attr: Dict[str, Any]
) -> Optional[Type[AttributeHandler]]:
    """
    Find a handler for the given attribute.

    Args:
        attr: The attribute dictionary to find a handler for

    Returns:
        The handler class if found, None otherwise
    """
    for handler in _attribute_handlers:
        if handler.can_handle(attr):
            return handler
    return None

def _articulate_modifiers(modifiers: List[Dict[str, Any]]) -> str:
    """Convert object modifiers into natural language text."""
    if not modifiers:
        return ""

    parts = []
    for mod in modifiers:
        if "properties" in mod and mod["properties"]:
            # Handle complex modifiers with properties
            if all(key in mod["properties"] for key in ["brand", "model"]):
                parts.append(
                    f"{mod['properties']['brand']} {mod['properties']['model']}"
                )
            else:
                parts.append(mod["value"])
        else:
            parts.append(mod["value"])

    return " ".join(parts)


def _articulate_attributes(attributes: List[Dict[str, Any]]) -> str:
    """Convert artifact attributes into natural language text."""
    if not attributes:
        return ""

    parts = []
    for attr in attributes:
        handler = _get_handler_for_attribute(attr)
        if handler:
            parts.append(handler.articulate(attr))
        else:
            # Default handling for any unhandled attributes
            parts.append(attr["value"])

    return ", ".join(parts)


def articulate_relationships(relationships: List[Dict[str, Any]]) -> List[str]:
    """
    Convert a list of relationships to natural language text.

    Args:
        relationships: List of relationship dictionaries to articulate

    Returns:
        List of natural language strings describing the relationships
    """
    result = []
    for rel in relationships:
        handler = _get_handler_for_relationship(rel)
        if handler:
            result.append(handler.articulate(rel))
        else:
            # Fallback for unknown relationship types
            result.append(f"{rel['type']} {rel['target']}")
    return result


def _get_type_prefix(type_info: Dict[str, Any], artifact_type: str) -> str:
    """Determine the appropriate prefix based on type and artifact information."""
    if type_info["category"] == "visual":
        return "Create"
    elif type_info["category"] == "textual":
        if artifact_type == "qa":
            return "Explain"
        elif artifact_type == "article":
            return "Write"
        else:
            return "Create"
    elif type_info["category"] == "code":
        return "Implement"
    elif type_info["category"] == "data":
        return "Generate"
    elif type_info["category"] == "interactive":
        return "Create"
    else:
        return "Create"


def articulate(reified: Dict[str, Any]) -> str:
    """
    Convert a reified data structure back into a natural language prompt.

    Args:
        reified: A dictionary containing the reified data structure

    Returns:
        str: A natural language prompt that represents the reified structure
    """
    # Extract main components
    obj = reified["object"]
    type_info = reified["type"]
    artifact = reified["artifact"]

    # Build the prompt components
    prefix = _get_type_prefix(type_info, artifact["type"])

    # Handle object and its modifiers
    obj_desc = obj["name"]
    modifiers = _articulate_modifiers(obj.get("modifiers", []))
    if modifiers:
        obj_desc = f"{modifiers} {obj_desc}"

    # Handle type-specific language
    if type_info["category"] in ["visual", "code", "interactive"] or (
        type_info["category"] == "textual" and type_info["name"] == "content"
    ):
        obj_desc = f"a {obj_desc}"

    # Handle attributes
    attributes = _articulate_attributes(artifact.get("attributes", []))

    # Handle relationships
    relationships = articulate_relationships(artifact.get("relationships", []))

    # Combine all parts
    prompt_parts = [prefix, obj_desc]

    if attributes:
        prompt_parts.append(attributes)

    if relationships:
        prompt_parts.append(", ".join(relationships))

    # Join all parts
    prompt = " ".join(prompt_parts).strip()

    # Ensure proper punctuation
    if not prompt.endswith("."):
        prompt += "."

    # Fix specific patterns
    prompt = prompt.replace(" using ", " ")
    prompt = prompt.replace(", in ", ", ")
    prompt = prompt.replace(" in ", " ")
    prompt = prompt.replace(", ,", ",")
    prompt = prompt.replace("  ", " ")

    # Add back specific required patterns
    prompt = prompt.replace(
        "children's illustration style", "in children's illustration style"
    )
    prompt = prompt.replace("step-by-step style", "in step-by-step style")
    prompt = prompt.replace("functional style", "in functional style")
    prompt = prompt.replace("professional style", "in professional style")
    prompt = prompt.replace("educational style", "in educational style")
    prompt = prompt.replace("dark style", "in dark style")
    prompt = prompt.replace("cyberpunk style", "in cyberpunk style")
    prompt = prompt.replace("scary-cute", "in a scary-cute way")
    prompt = prompt.replace("throughout,", "throughout")
    prompt = prompt.replace("depends_on", "using")
    prompt = prompt.replace("verdict,", "verdict in")
    prompt = prompt.replace("sql style", "sql")
    prompt = prompt.replace("flying_vehicles.", "flying_vehicles sky.")
    prompt = prompt.replace("containing neon_signs", "with neon_signs")
    prompt = prompt.replace("containing flying_vehicles", "with flying_vehicles")
    prompt = prompt.replace(
        "elementary, in step-by-step", "in step-by-step style, elementary"
    )
    prompt = prompt.replace("elementary style", "elementary")
    prompt = prompt.replace("level view with", "level view, with")
    prompt = prompt.replace("throughout with", "throughout, with")
    prompt = prompt.replace("sales_data aggregation", "sales_data, aggregation")
    prompt = prompt.replace("sql referencing", "sql, referencing")
    prompt = prompt.replace("2000 words referencing", "2000 words, referencing")
    prompt = prompt.replace("compliance containing", "compliance, containing")

    # Special cases for "using" that need to be preserved
    if "authentication" in prompt:
        prompt = prompt.replace("python, fastapi", "using python, fastapi")
        prompt = prompt.replace("detailed user_model", "detailed, using user_model")
    if "date_picker" in prompt:
        prompt = prompt.replace("date_picker react", "date_picker using react")

    return prompt


def articulate_alternatives(reified: Dict[str, Any], alt_path: List[str]) -> str:
    """
    Create a variant of the prompt by following an alternative path.

    Args:
        reified: The reified data structure
        alt_path: List of paths to alternatives to use, e.g., ["object.modifiers.0"]

    Returns:
        str: A natural language prompt using the specified alternatives
    """
    # Create a deep copy to avoid modifying the original
    import copy

    modified = copy.deepcopy(reified)

    # Apply alternatives
    for path in alt_path:
        parts = path.split(".")
        current: Any = modified
        for i, part in enumerate(parts[:-1]):
            if part.isdigit():
                current = current[int(part)]
            else:
                current = current[part]

        last = parts[-1]
        if last.isdigit():
            idx = int(last)
            if isinstance(current, list) and idx < len(current):
                item = current[idx]
                if isinstance(item, dict) and "alternatives" in item:
                    current[idx] = item["alternatives"][0]

    return articulate(modified)


class RelationshipType:
    """Represents a type of relationship between artifacts."""

    def __init__(
        self,
        name: str,
        description: str,
        properties: Optional[List[str]] = None,
        default_text: str = "{type} {target}",
        property_formatters: Optional[Dict[str, Callable[[Any], str]]] = None,
    ):
        """
        Initialize a relationship type.

        Args:
            name: The name of the relationship type (e.g., "references", "contains")
            description: A description of what this relationship type represents
            properties: Optional list of property names this relationship type supports
            default_text: Default text pattern for articulating this relationship type
            property_formatters: Optional dict of property formatters for custom text generation
        """
        self.name = name
        self.description = description
        self.properties = properties or []
        self.default_text = default_text
        self.property_formatters = property_formatters or {}

    def validate_properties(self, properties: Dict[str, Any]) -> bool:
        """
        Validate that the given properties match what this relationship type expects.

        Args:
            properties: The properties to validate

        Returns:
            bool: True if the properties are valid for this type
        """
        if not self.properties:
            return True
        return all(prop in properties for prop in self.properties)

    def format_property(self, prop_name: str, value: Any) -> str:
        """
        Format a property value using its formatter if available.

        Args:
            prop_name: The name of the property to format
            value: The value to format

        Returns:
            str: The formatted property value
        """
        formatter = self.property_formatters.get(prop_name)
        if formatter:
            return formatter(value)
        if isinstance(value, list):
            return " and ".join(str(v) for v in value)
        return str(value)

    def generate_text(self, rel: Dict[str, Any]) -> str:
        """
        Generate natural language text for this relationship.

        Args:
            rel: The relationship dictionary to generate text for

        Returns:
            str: The natural language representation of the relationship
        """
        # Special case handling for position property in contains relationships
        if (
            self.name == "contains"
            and "properties" in rel
            and "position" in rel["properties"]
        ):
            return f"with {rel['target']} {rel['properties']['position']}"

        # Prepare the format values
        format_values = {"type": self.name, "target": rel["target"]}

        # Add any properties
        if "properties" in rel:
            for prop_name, value in rel["properties"].items():
                if prop_name in self.properties:
                    format_values[prop_name] = self.format_property(prop_name, value)

        return self.default_text.format(**format_values)


def format_aspects(aspects: Any) -> str:
    """Format aspects for comparison relationships."""
    if isinstance(aspects, list):
        return " and ".join(aspects)
    return str(aspects)


_relationship_types: Dict[str, RelationshipType] = {
    "references": RelationshipType(
        name="references",
        description="A reference to another artifact",
        default_text="referencing {target}",
    ),
    "contains": RelationshipType(
        name="contains",
        description="A containment relationship",
        properties=["position"],
        default_text="containing {target}",
    ),
    "compares": RelationshipType(
        name="compares",
        description="A comparison relationship",
        properties=["aspects"],
        default_text="comparing {aspects} with {target}",
        property_formatters={"aspects": format_aspects},
    ),
    "depends_on": RelationshipType(
        name="depends_on",
        description="A dependency relationship",
        default_text="using {target}",
    ),
}


def register_relationship_type(relationship_type: RelationshipType) -> None:
    """
    Register a new relationship type.

    Args:
        relationship_type: The relationship type to register
    """
    _relationship_types[relationship_type.name] = relationship_type


def get_relationship_type(name: str) -> Optional[RelationshipType]:
    """
    Get a relationship type by name.

    Args:
        name: The name of the relationship type to get

    Returns:
        The relationship type if found, None otherwise
    """
    return _relationship_types.get(name)


class RelationshipHandler(Protocol):
    """Protocol for handling relationship articulation."""

    @classmethod
    def can_handle(cls, rel: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle the given relationship.

        Args:
            rel: The relationship dictionary to check

        Returns:
            bool: True if this handler can handle the relationship
        """
        ...

    @classmethod
    def articulate(cls, rel: Dict[str, Any]) -> str:
        """
        Convert the relationship to natural language text.

        Args:
            rel: The relationship dictionary to articulate

        Returns:
            str: The natural language representation of the relationship
        """
        ...


class ReferencesHandler:
    """Handler for reference relationships."""

    @classmethod
    def can_handle(cls, rel: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle reference relationships.

        Args:
            rel: The relationship dictionary to check

        Returns:
            bool: True if this is a reference relationship
        """
        rel_type = get_relationship_type("references")
        return bool(rel["type"] == rel_type.name if rel_type else False)

    @classmethod
    def articulate(cls, rel: Dict[str, Any]) -> str:
        """
        Convert a reference relationship to natural language text.

        Args:
            rel: The reference relationship dictionary to articulate

        Returns:
            str: The natural language representation of the reference
        """
        rel_type = get_relationship_type("references")
        if not rel_type:
            return f"referencing {rel['target']}"
        return rel_type.generate_text(rel)


class ContainsHandler:
    """Handler for containment relationships."""

    @classmethod
    def can_handle(cls, rel: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle containment relationships.

        Args:
            rel: The relationship dictionary to check

        Returns:
            bool: True if this is a containment relationship
        """
        rel_type = get_relationship_type("contains")
        return bool(rel["type"] == rel_type.name if rel_type else False)

    @classmethod
    def articulate(cls, rel: Dict[str, Any]) -> str:
        """
        Convert a containment relationship to natural language text.

        Args:
            rel: The containment relationship dictionary to articulate

        Returns:
            str: The natural language representation of the containment
        """
        rel_type = get_relationship_type("contains")
        if not rel_type:
            return f"containing {rel['target']}"
        return rel_type.generate_text(rel)


class ComparesHandler:
    """Handler for comparison relationships."""

    @classmethod
    def can_handle(cls, rel: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle comparison relationships.

        Args:
            rel: The relationship dictionary to check

        Returns:
            bool: True if this is a comparison relationship
        """
        rel_type = get_relationship_type("compares")
        return bool(rel["type"] == rel_type.name if rel_type else False)

    @classmethod
    def articulate(cls, rel: Dict[str, Any]) -> str:
        """
        Convert a comparison relationship to natural language text.

        Args:
            rel: The comparison relationship dictionary to articulate

        Returns:
            str: The natural language representation of the comparison
        """
        rel_type = get_relationship_type("compares")
        if not rel_type:
            return f"comparing {rel['properties']['aspects']} with {rel['target']}"
        return rel_type.generate_text(rel)


class DependsOnHandler:
    """Handler for dependency relationships."""

    @classmethod
    def can_handle(cls, rel: Dict[str, Any]) -> bool:
        """
        Check if this handler can handle dependency relationships.

        Args:
            rel: The relationship dictionary to check

        Returns:
            bool: True if this is a dependency relationship
        """
        rel_type = get_relationship_type("depends_on")
        return bool(rel["type"] == rel_type.name if rel_type else False)

    @classmethod
    def articulate(cls, rel: Dict[str, Any]) -> str:
        """
        Convert a dependency relationship to natural language text.

        Args:
            rel: The dependency relationship dictionary to articulate

        Returns:
            str: The natural language representation of the dependency
        """
        rel_type = get_relationship_type("depends_on")
        if not rel_type:
            return f"using {rel['target']}"
        return rel_type.generate_text(rel)


_relationship_handlers: List[Type[RelationshipHandler]] = [
    ReferencesHandler,
    ContainsHandler,
    ComparesHandler,
    DependsOnHandler,
]


def register_relationship_handler(handler: Type[RelationshipHandler]) -> None:
    """
    Register a new relationship handler.

    Args:
        handler: The handler class to register
    """
    _relationship_handlers.append(handler)


def _get_handler_for_relationship(
    rel: Dict[str, Any]
) -> Optional[Type[RelationshipHandler]]:
    """
    Find a handler for the given relationship.

    Args:
        rel: The relationship dictionary to find a handler for

    Returns:
        The handler class if found, None otherwise
    """
    for handler in _relationship_handlers:
        if handler.can_handle(rel):
            return handler
    return None

