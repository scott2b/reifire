"""Tests for the articulation module."""

import json
from pathlib import Path
from typing import Any, Dict

from reifire.articulation import articulate, articulate_alternatives


def load_example(name: str) -> Dict[str, Any]:
    """
    Load an example from the examples directory.

    Args:
        name: The name of the example file (without .json extension)

    Returns:
        The loaded JSON data as a dictionary
    """
    example_path = Path(__file__).parent.parent.parent / "examples" / f"{name}.json"
    with open(example_path) as f:
        data: Dict[str, Any] = json.load(f)
        return data


def test_basic_illustration() -> None:
    """Test basic illustration prompt generation."""
    reified = load_example("basic_illustration")
    prompt = articulate(reified)
    expected = (
        "Create a scary-cute baby Cthulhu "
        "with a brown-green-purple color scheme "
        "in children's illustration style."
    )
    assert prompt == expected


def test_question_answer() -> None:
    """Test question-answer prompt generation."""
    reified = load_example("question_answer")
    prompt = articulate(reified)
    expected = (
        "Explain the process of photosynthesis "
        "in elementary, step-by-step, educational style."
    )
    assert prompt == expected


def test_code_generation() -> None:
    """Test code generation prompt."""
    reified = load_example("code_generation")
    prompt = articulate(reified)
    expected = (
        "Implement an oauth2 middleware authentication in functional style "
        "with detailed documentation using python and fastapi, requiring user_model."
    )
    assert prompt == expected


def test_complex_visual_scene() -> None:
    """Test complex visual scene prompt generation."""
    reified = load_example("complex_visual_scene")
    prompt = articulate(reified)
    expected = (
        "Create a future tokyo cityscape in cyberpunk style, night, rain, "
        "street level view, with neon signs throughout with flying vehicles in the sky."
    )
    assert prompt == expected


def test_data_analysis() -> None:
    """Test data analysis prompt generation."""
    reified = load_example("data_analysis")
    prompt = articulate(reified)
    expected = (
        "Generate last_quarter north_america sales_data, aggregation, "
        "product_category and month, revenue and growth_rate in SQL, "
        "referencing product_catalog."
    )
    assert prompt == expected


def test_ui_component() -> None:
    """Test UI component prompt generation."""
    reified = load_example("ui_component")
    prompt = articulate(reified)
    expected = (
        "Create a multi calendar date_picker "
        "with wcag_aa compliance "
        "in dark style "
        "using react and tailwind, "
        "containing calendar_grid and time_selector."
    )
    assert prompt == expected


def test_content_generation() -> None:
    """Test content generation prompt."""
    reified = load_example("content_generation")
    prompt = articulate(reified)
    expected = (
        "Write an Apple iPhone 15 Pro product review in professional style, "
        "expert, covering design, performance, camera, battery, verdict in 2000 words, "
        "referencing technical specs comparing performance and camera with iPhone 14 Pro."
    )
    assert prompt == expected


def test_alternatives() -> None:
    """Test alternatives prompt generation."""
    reified = load_example("basic_illustration")
    alt_prompt = articulate_alternatives(
        reified,
        ["object.modifiers.0", "artifact.attributes.0", "artifact.attributes.1"],
    )
    expected = (
        "Create a terrifying Cthulhu "
        "with a brown-green-purple color scheme "
        "in dark fantasy style."
    )
    assert alt_prompt == expected
