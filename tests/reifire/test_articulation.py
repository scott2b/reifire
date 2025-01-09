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
        "Create a baby Cthulu in children's illustration style, "
        "in a scary-cute way, with brown-green-purple color scheme."
    )
    assert prompt == expected


def test_question_answer() -> None:
    """Test question-answer prompt generation."""
    reified = load_example("question_answer")
    prompt = articulate(reified)
    expected = (
        "Explain process photosynthesis in step-by-step style, "
        "elementary, in educational style."
    )
    assert prompt == expected


def test_code_generation() -> None:
    """Test code generation prompt."""
    reified = load_example("code_generation")
    prompt = articulate(reified)
    expected = (
        "Implement a oauth2 middleware authentication using python, fastapi, "
        "in functional style, detailed, using user_model."
    )
    assert prompt == expected


def test_complex_visual_scene() -> None:
    """Test complex visual scene prompt generation."""
    reified = load_example("complex_visual_scene")
    prompt = articulate(reified)
    expected = (
        "Create a future tokyo cityscape in cyberpunk style, night, rain, "
        "street level view, with neon_signs throughout, with flying_vehicles sky."
    )
    assert prompt == expected


def test_data_analysis() -> None:
    """Test data analysis prompt generation."""
    reified = load_example("data_analysis")
    prompt = articulate(reified)
    expected = (
        "Generate last_quarter north_america sales_data, aggregation, "
        "product_category and month, revenue and growth_rate, sql, "
        "referencing product_catalog."
    )
    assert prompt == expected


def test_ui_component() -> None:
    """Test UI component prompt generation."""
    reified = load_example("ui_component")
    prompt = articulate(reified)
    expected = (
        "Create a multi calendar date_picker using react, tailwind, "
        "in dark style, with wcag_aa compliance, containing calendar_grid, "
        "containing time_selector."
    )
    assert prompt == expected


def test_content_generation() -> None:
    """Test content generation prompt."""
    reified = load_example("content_generation")
    prompt = articulate(reified)
    expected = (
        "Write a Apple iPhone 15 Pro long_term product_review in professional style, "
        "expert, covering design, performance, camera, battery, verdict in 2000 words, "
        "referencing technical_specs, comparing performance and camera with iphone_14_pro."
    )
    assert prompt == expected


def test_alternatives() -> None:
    """Test alternatives prompt generation."""
    reified = load_example("basic_illustration")
    alt_prompt = articulate_alternatives(reified, ["object.modifiers.0"])
    expected = (
        "Create a adult Cthulu in children's illustration style, "
        "in a scary-cute way, with brown-green-purple color scheme."
    )
    assert alt_prompt == expected
