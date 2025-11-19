# Reifire Detailed Project Plan

**Version**: 1.0
**Date**: 2025-11-18
**Status**: Pre-Alpha → Production
**Timeline**: 16 weeks (4 months)
**Goal**: Transform reifire into a production-ready reification library with web API

---

## Table of Contents

1. [Overview](#overview)
2. [Phase 1: Foundation (Weeks 1-4)](#phase-1-foundation-weeks-1-4)
3. [Phase 2: Core Reification (Weeks 5-8)](#phase-2-core-reification-weeks-5-8)
4. [Phase 3: Web API (Weeks 9-12)](#phase-3-web-api-weeks-9-12)
5. [Phase 4: Polish & Launch (Weeks 13-16)](#phase-4-polish--launch-weeks-13-16)
6. [Implementation Details](#implementation-details)
7. [Testing Strategy](#testing-strategy)
8. [Deployment Strategy](#deployment-strategy)
9. [Success Criteria](#success-criteria)

---

## Overview

### Current State
- ✅ Articulation system (442 lines) - Production ready
- ✅ Visualization system (~1,500 lines) - Production ready
- ✅ Data specification - Comprehensive
- ❌ Core reification (0 lines) - **DOES NOT EXIST**
- ❌ Tests - Broken
- ❌ Web API - Not started

### Target State
- ✅ Core reification with multi-LLM support
- ✅ Comprehensive test coverage (>80%)
- ✅ Litestar-based web API
- ✅ Extended icon support (emoji, Font Awesome, custom uploads)
- ✅ Production deployment with monitoring
- ✅ Complete documentation
- ✅ PyPI publication

### Resource Requirements
- **Development Time**: 1 full-time developer, 16 weeks
- **API Costs**: ~$200/month for LLM testing
- **Infrastructure**: ~$50/month for web hosting (initial)
- **Tools**: GitHub Actions (free), ReadTheDocs (free), PyPI (free)

---

## Phase 1: Foundation (Weeks 1-4)

**Goal**: Fix critical infrastructure issues and implement basic reification

### Week 1: Infrastructure Fixes

#### Day 1-2: Test Suite Repair 🔴 CRITICAL

**Tasks**:
1. Debug package import issues
   - Verify package installation: `python -c "import reifire; print(reifire.__version__)"`
   - Check PYTHONPATH configuration
   - Review `conftest.py` files
   - Add root conftest.py with path setup if needed

2. Install test dependencies
   ```bash
   pip install pytest pytest-cov pytest-asyncio pytest-mock
   ```

3. Fix all 12 test files to run successfully
   - `tests/reifire/test_articulation.py`
   - `tests/reifire/test_reification.py`
   - `tests/reifire/visualization/test_*.py` (10 files)

4. Set up GitHub Actions CI
   ```yaml
   # .github/workflows/test.yml
   name: Tests
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: [3.9, 3.10, 3.11, 3.12]
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: ${{ matrix.python-version }}
         - run: pip install -e ".[dev]"
         - run: pytest --cov=reifire --cov-report=xml
         - uses: codecov/codecov-action@v3
   ```

**Deliverables**:
- [ ] All tests passing
- [ ] CI running on GitHub Actions
- [ ] Coverage report >60%

**Success Criteria**: Green CI badge in README

---

#### Day 3-5: Package Configuration Modernization 🔴 CRITICAL

**Tasks**:
1. Migrate to modern `pyproject.toml`
   - Remove or minimize `setup.py`
   - Add all metadata (author, license, classifiers)
   - Define dependencies properly
   - Add optional dependencies groups: `dev`, `web`, `all`

2. Complete `pyproject.toml` structure:
   ```toml
   [build-system]
   requires = ["setuptools>=61.0", "wheel"]
   build-backend = "setuptools.build_meta"

   [project]
   name = "reifire"
   version = "0.1.0"
   description = "Reify natural language prompts into interactive visual objects"
   readme = "README.md"
   authors = [
       {name = "Scott Bronson", email = "brons_reifire@rinspin.com"}
   ]
   license = {text = "MIT"}
   classifiers = [
       "Development Status :: 2 - Pre-Alpha",
       "Intended Audience :: Developers",
       "Topic :: Software Development :: Libraries :: Python Modules",
       "Topic :: Scientific/Engineering :: Artificial Intelligence",
       "License :: OSI Approved :: MIT License",
       "Programming Language :: Python :: 3",
       "Programming Language :: Python :: 3.9",
       "Programming Language :: Python :: 3.10",
       "Programming Language :: Python :: 3.11",
       "Programming Language :: Python :: 3.12",
   ]
   requires-python = ">=3.9"
   dependencies = [
       "requests>=2.25.0",
       "requests_oauthlib>=1.3.0",
       "nltk>=3.8.1",
       "jinja2>=3.0.0",
       "openai>=1.0.0",
       "anthropic>=0.18.0",
       "pydantic>=2.0.0",
       "jsonschema>=4.0.0",
       "emoji>=2.0.0",
       "pillow>=10.0.0",
       "python-dotenv>=1.0.0",
   ]

   [project.optional-dependencies]
   dev = [
       "pytest>=7.0.0",
       "pytest-cov>=4.0.0",
       "pytest-asyncio>=0.21.0",
       "pytest-mock>=3.12.0",
       "black>=23.0.0",
       "isort>=5.12.0",
       "mypy>=1.0.0",
       "flake8>=6.0.0",
       "sphinx>=7.0.0",
       "sphinx-rtd-theme>=1.3.0",
   ]
   web = [
       "litestar>=2.0.0",
       "uvicorn[standard]>=0.24.0",
       "python-multipart>=0.0.6",
       "redis>=5.0.0",
   ]
   all = [
       "reifire[dev,web]",
   ]

   [project.scripts]
   reifire = "reifire.cli:main"

   [project.urls]
   Homepage = "https://github.com/scott2b/reifire"
   Documentation = "https://reifire.readthedocs.io"
   Repository = "https://github.com/scott2b/reifire"
   Issues = "https://github.com/scott2b/reifire/issues"

   [tool.setuptools.packages.find]
   where = ["src"]

   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = ["test_*.py"]
   python_classes = ["Test*"]
   python_functions = ["test_*"]
   addopts = "-v --cov=reifire --cov-report=html --cov-report=term --cov-report=xml"

   [tool.black]
   line-length = 100
   target-version = ['py39', 'py310', 'py311', 'py312']
   include = '\.pyi?$'

   [tool.isort]
   profile = "black"
   line_length = 100

   [tool.mypy]
   python_version = "3.9"
   warn_return_any = true
   warn_unused_configs = true
   disallow_untyped_defs = true
   ignore_missing_imports = true
   ```

3. Update requirements.txt to point to pyproject.toml
   ```
   # requirements.txt
   # Install with: pip install -e .
   # Dev install: pip install -e ".[dev]"
   # All features: pip install -e ".[all]"
   -e .
   ```

4. Create separate requirements files for clarity:
   - `requirements-dev.txt` - development tools
   - `requirements-web.txt` - web API dependencies
   - `requirements-test.txt` - testing dependencies

**Deliverables**:
- [ ] Modern pyproject.toml
- [ ] Clean dependency management
- [ ] Installable with `pip install -e ".[dev]"`

**Success Criteria**: Package installs cleanly in fresh virtualenv

---

#### Day 6-7: Documentation Update 🟡

**Tasks**:
1. Update README.md to reflect current state
   - Add honest "Current Status" section
   - Mark unimplemented features as "Planned"
   - Show working examples (articulation + visualization)
   - Add badges (CI, coverage, PyPI, Python versions)
   - Fix installation instructions

2. Updated README structure:
   ```markdown
   # reifire 🔥

   [![Tests](https://github.com/scott2b/reifire/workflows/Tests/badge.svg)](...)
   [![Coverage](https://codecov.io/gh/scott2b/reifire/badge.svg)](...)
   [![Python](https://img.shields.io/pypi/pyversions/reifire.svg)](...)
   [![PyPI](https://badge.fury.io/py/reifire.svg)](...)

   Reify your natural language prompts into interactive visual objects.

   > **⚠️ Current Status: Pre-Alpha**
   >
   > Reifire is under active development. The following features are currently available:
   > - ✅ Articulation (reified structure → natural language)
   > - ✅ Interactive visualizations
   > - 🚧 Reification (natural language → reified structure) - **IN DEVELOPMENT**
   > - 🚧 Web API - **PLANNED**

   ## What Works Now

   [Show articulation and visualization examples]

   ## Planned Features

   [List reification, web API, etc.]

   ## Installation

   ### For Development
   ```bash
   git clone https://github.com/scott2b/reifire.git
   cd reifire
   pip install -e ".[dev]"
   ```

   ### API Keys
   [Document environment variables]

   ## Quick Start

   [Working example with articulation + visualization]

   ## Roadmap

   See [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed roadmap.
   ```

3. Add LICENSE file (MIT)

4. Add CONTRIBUTING.md

**Deliverables**:
- [ ] Updated README.md
- [ ] LICENSE file
- [ ] CONTRIBUTING.md

**Success Criteria**: Clear, honest documentation that doesn't mislead users

---

### Week 2: Pydantic Schema Models

#### Day 8-10: Core Schema Definitions 🔴 CRITICAL

**Tasks**:
1. Create Pydantic models matching DATASPEC.md

   **File**: `src/reifire/schema/__init__.py`
   ```python
   """Pydantic models for reified data structures."""
   from .models import (
       ReifiedStructure,
       ObjectComponent,
       TypeComponent,
       ArtifactComponent,
       Modifier,
       ArtifactAttribute,
       Visualization,
       Relationship,
       Metadata,
   )

   __all__ = [
       "ReifiedStructure",
       "ObjectComponent",
       "TypeComponent",
       "ArtifactComponent",
       "Modifier",
       "ArtifactAttribute",
       "Visualization",
       "Relationship",
       "Metadata",
   ]
   ```

   **File**: `src/reifire/schema/models.py`
   ```python
   """Pydantic models for validation."""
   from typing import Any, Dict, List, Optional
   from pydantic import BaseModel, Field, validator


   class Visualization(BaseModel):
       """Visualization metadata."""
       source: str = Field(..., description="Source of visualization (nounproject, colors, openai, emoji, etc.)")
       name: str = Field(..., description="Identifier for the visualization")
       image: Optional[str] = Field(None, description="Primary image reference")
       images: Optional[List[str]] = Field(None, description="Multiple images (e.g., color schemes)")
       attribution: Optional[str] = Field(None, description="Attribution text")
       alternatives: Optional[List['Visualization']] = Field(None, description="Alternative visualizations")
       properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional properties")


   class Modifier(BaseModel):
       """Object modifier."""
       name: str = Field(..., description="Modifier name (e.g., 'age', 'type', 'scope')")
       value: Any = Field(..., description="Modifier value")
       category: Optional[str] = Field(None, description="Modifier category")
       visualization: Optional[Visualization] = Field(None, description="Visual representation")
       alternatives: Optional[List['Modifier']] = Field(None, description="Alternative values")
       properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional properties")


   class ObjectComponent(BaseModel):
       """The primary subject of the reified prompt."""
       name: str = Field(..., description="Object name (e.g., 'Cthulhu', 'authentication')")
       modifiers: Optional[List[Modifier]] = Field(None, description="Object modifiers")
       description: Optional[str] = Field(None, description="Object description")
       variants: Optional[List['ObjectComponent']] = Field(None, description="Object variants")
       properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional properties")


   class TypeComponent(BaseModel):
       """The category or form of the output artifact."""
       name: str = Field(..., description="Type name (e.g., 'illustration', 'implementation')")
       category: str = Field(..., description="Type category (visual, textual, interactive, code, data)")
       visualization: Optional[Visualization] = Field(None, description="Visual representation")
       properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional properties")

       @validator('category')
       def validate_category(cls, v):
           valid_categories = ['visual', 'textual', 'interactive', 'code', 'data']
           if v not in valid_categories:
               raise ValueError(f"Category must be one of {valid_categories}")
           return v


   class Relationship(BaseModel):
       """Relationship between components."""
       type: str = Field(..., description="Relationship type (contains, depends_on, references, compares, uses)")
       source: str = Field(..., description="Source component")
       target: str = Field(..., description="Target component")
       visualization: Optional[Visualization] = Field(None, description="Visual representation")
       properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional properties")


   class ArtifactAttribute(BaseModel):
       """Attribute of the output artifact."""
       name: str = Field(..., description="Attribute name (e.g., 'style', 'language', 'mood')")
       value: Any = Field(..., description="Attribute value")
       category: Optional[str] = Field(None, description="Attribute category")
       visualization: Optional[Visualization] = Field(None, description="Visual representation")
       alternatives: Optional[List['ArtifactAttribute']] = Field(None, description="Alternative values")
       properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional properties")


   class ArtifactComponent(BaseModel):
       """The output representation and its attributes."""
       type: str = Field(..., description="Artifact type (image, text, qa, code, query, ui_element)")
       attributes: Optional[List[ArtifactAttribute]] = Field(None, description="Artifact attributes")
       visualization: Optional[Visualization] = Field(None, description="Visual representation")
       relationships: Optional[List[Relationship]] = Field(None, description="Relationships to other components")
       properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional properties")


   class Metadata(BaseModel):
       """Metadata about the reification process."""
       timestamp: Optional[str] = Field(None, description="Timestamp of creation")
       version: str = Field(default="1.0", description="Schema version")
       original_prompt: str = Field(..., description="Original natural language prompt")
       articulated_prompt: Optional[str] = Field(None, description="Re-articulated prompt")
       processing_info: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Processing metadata")
       visualization_config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Visualization configuration")


   class ReifiedStructure(BaseModel):
       """Complete reified data structure."""
       object: ObjectComponent = Field(..., description="Primary object")
       type: TypeComponent = Field(..., description="Output type")
       artifact: ArtifactComponent = Field(..., description="Output artifact")
       metadata: Metadata = Field(..., description="Metadata")

       class Config:
           json_schema_extra = {
               "example": {
                   "object": {
                       "name": "dragon",
                       "modifiers": [{"name": "mood", "value": "fierce"}]
                   },
                   "type": {
                       "name": "illustration",
                       "category": "visual"
                   },
                   "artifact": {
                       "type": "image",
                       "attributes": [
                           {"name": "style", "value": "dark fantasy"}
                       ]
                   },
                   "metadata": {
                       "version": "1.0",
                       "original_prompt": "Create a fierce dragon illustration in dark fantasy style"
                   }
               }
           }


   # Update forward references
   Visualization.model_rebuild()
   Modifier.model_rebuild()
   ObjectComponent.model_rebuild()
   ```

2. Add validation utilities

   **File**: `src/reifire/schema/validators.py`
   ```python
   """Validation utilities for reified structures."""
   from typing import Dict, Any, List
   from pydantic import ValidationError
   from .models import ReifiedStructure


   class ValidationResult:
       """Result of validation."""

       def __init__(self, valid: bool, errors: List[str] = None, warnings: List[str] = None):
           self.valid = valid
           self.errors = errors or []
           self.warnings = warnings or []

       def __bool__(self):
           return self.valid


   def validate_reified_structure(data: Dict[str, Any]) -> ValidationResult:
       """
       Validate a reified structure against the schema.

       Args:
           data: Dictionary to validate

       Returns:
           ValidationResult with validation status and messages
       """
       try:
           ReifiedStructure(**data)
           return ValidationResult(valid=True)
       except ValidationError as e:
           errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
           return ValidationResult(valid=False, errors=errors)


   def validate_and_fix(data: Dict[str, Any]) -> tuple[Dict[str, Any], ValidationResult]:
       """
       Validate and attempt to fix common issues.

       Returns:
           (fixed_data, validation_result)
       """
       fixed = data.copy()
       warnings = []

       # Add missing metadata fields
       if 'metadata' not in fixed:
           fixed['metadata'] = {
               'version': '1.0',
               'original_prompt': 'Unknown'
           }
           warnings.append("Added missing metadata")

       # Ensure required fields exist
       if 'object' not in fixed:
           return data, ValidationResult(valid=False, errors=["Missing 'object' component"])

       if 'type' not in fixed:
           return data, ValidationResult(valid=False, errors=["Missing 'type' component"])

       if 'artifact' not in fixed:
           return data, ValidationResult(valid=False, errors=["Missing 'artifact' component"])

       # Validate fixed structure
       result = validate_reified_structure(fixed)
       result.warnings = warnings

       return fixed, result
   ```

3. Create JSON schema export utility

   **File**: `src/reifire/schema/export.py`
   ```python
   """Export Pydantic schemas to JSON Schema."""
   import json
   from pathlib import Path
   from .models import ReifiedStructure


   def export_json_schema(output_path: Path = None) -> Dict[str, Any]:
       """
       Export the ReifiedStructure schema as JSON Schema.

       Args:
           output_path: Optional path to write JSON schema file

       Returns:
           JSON Schema dictionary
       """
       schema = ReifiedStructure.model_json_schema()

       if output_path:
           output_path.write_text(json.dumps(schema, indent=2))

       return schema
   ```

**Deliverables**:
- [ ] Complete Pydantic models for all DATASPEC components
- [ ] Validation utilities
- [ ] JSON schema export
- [ ] Unit tests for schema validation

**Success Criteria**: All example JSON files validate successfully

---

#### Day 11-14: LLM Backend Architecture 🔴 CRITICAL

**Tasks**:
1. Create abstract LLM backend interface

   **File**: `src/reifire/backends/__init__.py`
   ```python
   """LLM backend integrations."""
   from .base import LLMBackend, LLMResponse
   from .openai_backend import OpenAIBackend
   from .anthropic_backend import AnthropicBackend
   from .factory import get_backend

   __all__ = [
       "LLMBackend",
       "LLMResponse",
       "OpenAIBackend",
       "AnthropicBackend",
       "get_backend",
   ]
   ```

   **File**: `src/reifire/backends/base.py`
   ```python
   """Abstract base class for LLM backends."""
   from abc import ABC, abstractmethod
   from typing import Dict, Any, Optional, Type
   from dataclasses import dataclass
   from pydantic import BaseModel


   @dataclass
   class LLMResponse:
       """Response from LLM."""
       content: Dict[str, Any]
       raw_response: Any
       model: str
       tokens_used: int
       cost_usd: float
       cached: bool = False


   class LLMBackend(ABC):
       """Abstract base class for LLM backends."""

       def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
           """
           Initialize backend.

           Args:
               api_key: API key (or None to use environment variable)
               model: Model name (or None for default)
           """
           self.api_key = api_key
           self.model = model or self.default_model()

       @abstractmethod
       def parse_prompt(
           self,
           prompt: str,
           schema: Type[BaseModel],
           system_prompt: str,
           **kwargs
       ) -> LLMResponse:
           """
           Parse a prompt using the LLM with structured output.

           Args:
               prompt: Natural language to parse
               schema: Pydantic model for structured output
               system_prompt: Instructions for the LLM
               **kwargs: Backend-specific options

           Returns:
               LLMResponse with parsed structure
           """
           pass

       @abstractmethod
       def estimate_cost(self, prompt: str, schema: Type[BaseModel]) -> float:
           """
           Estimate cost in USD for this request.

           Args:
               prompt: Natural language prompt
               schema: Expected output schema

           Returns:
               Estimated cost in USD
           """
           pass

       @abstractmethod
       def is_available(self) -> bool:
           """
           Check if backend is configured and available.

           Returns:
               True if backend can be used
           """
           pass

       @classmethod
       @abstractmethod
       def default_model(cls) -> str:
           """Return default model name for this backend."""
           pass

       @abstractmethod
       def count_tokens(self, text: str) -> int:
           """Count tokens in text."""
           pass
   ```

2. Implement OpenAI backend

   **File**: `src/reifire/backends/openai_backend.py`
   ```python
   """OpenAI backend implementation."""
   import os
   import json
   from typing import Dict, Any, Type, Optional
   from pydantic import BaseModel
   from openai import OpenAI
   import tiktoken

   from .base import LLMBackend, LLMResponse


   class OpenAIBackend(LLMBackend):
       """OpenAI GPT-4 backend."""

       # Pricing per 1M tokens (as of Nov 2024)
       PRICING = {
           "gpt-4o": {"input": 2.50, "output": 10.00},
           "gpt-4o-mini": {"input": 0.150, "output": 0.600},
           "gpt-4-turbo": {"input": 10.00, "output": 30.00},
       }

       def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
           super().__init__(api_key, model)
           self.client = OpenAI(api_key=self.api_key or os.getenv("OPENAI_API_KEY"))
           self.encoder = tiktoken.encoding_for_model(self.model)

       @classmethod
       def default_model(cls) -> str:
           return "gpt-4o"

       def parse_prompt(
           self,
           prompt: str,
           schema: Type[BaseModel],
           system_prompt: str,
           **kwargs
       ) -> LLMResponse:
           """Parse prompt using OpenAI structured outputs."""
           try:
               response = self.client.beta.chat.completions.parse(
                   model=self.model,
                   messages=[
                       {"role": "system", "content": system_prompt},
                       {"role": "user", "content": prompt}
                   ],
                   response_format=schema,
                   **kwargs
               )

               parsed = response.choices[0].message.parsed
               usage = response.usage

               cost = self._calculate_cost(usage.prompt_tokens, usage.completion_tokens)

               return LLMResponse(
                   content=parsed.model_dump(),
                   raw_response=response,
                   model=self.model,
                   tokens_used=usage.total_tokens,
                   cost_usd=cost,
                   cached=False
               )

           except Exception as e:
               raise RuntimeError(f"OpenAI API error: {e}")

       def estimate_cost(self, prompt: str, schema: Type[BaseModel]) -> float:
           """Estimate cost based on token count."""
           # Rough estimate: prompt + schema + typical response
           prompt_tokens = self.count_tokens(prompt)
           schema_tokens = self.count_tokens(json.dumps(schema.model_json_schema()))
           estimated_response_tokens = 1000  # Conservative estimate

           input_tokens = prompt_tokens + schema_tokens
           output_tokens = estimated_response_tokens

           return self._calculate_cost(input_tokens, output_tokens)

       def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
           """Calculate actual cost from token counts."""
           pricing = self.PRICING.get(self.model, self.PRICING["gpt-4o"])

           input_cost = (input_tokens / 1_000_000) * pricing["input"]
           output_cost = (output_tokens / 1_000_000) * pricing["output"]

           return input_cost + output_cost

       def count_tokens(self, text: str) -> int:
           """Count tokens using tiktoken."""
           return len(self.encoder.encode(text))

       def is_available(self) -> bool:
           """Check if OpenAI is available."""
           try:
               # Simple test call
               self.client.models.list()
               return True
           except Exception:
               return False
   ```

3. Implement Anthropic backend

   **File**: `src/reifire/backends/anthropic_backend.py`
   ```python
   """Anthropic Claude backend implementation."""
   import os
   import json
   from typing import Dict, Any, Type, Optional
   from pydantic import BaseModel
   from anthropic import Anthropic

   from .base import LLMBackend, LLMResponse


   class AnthropicBackend(LLMBackend):
       """Anthropic Claude backend."""

       # Pricing per 1M tokens (as of Nov 2024)
       PRICING = {
           "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
           "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
           "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
       }

       # Prompt caching pricing (cache writes/reads)
       CACHE_PRICING = {
           "claude-3-5-sonnet-20241022": {"write": 3.75, "read": 0.30},
       }

       def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
           super().__init__(api_key, model)
           self.client = Anthropic(api_key=self.api_key or os.getenv("ANTHROPIC_API_KEY"))

       @classmethod
       def default_model(cls) -> str:
           return "claude-3-5-sonnet-20241022"

       def parse_prompt(
           self,
           prompt: str,
           schema: Type[BaseModel],
           system_prompt: str,
           use_cache: bool = True,
           **kwargs
       ) -> LLMResponse:
           """Parse prompt using Claude with JSON mode."""
           # Build schema description
           schema_json = schema.model_json_schema()
           schema_desc = json.dumps(schema_json, indent=2)

           # Build system prompt with caching
           system_messages = [
               {
                   "type": "text",
                   "text": system_prompt + f"\n\nOutput JSON matching this schema:\n{schema_desc}",
                   "cache_control": {"type": "ephemeral"} if use_cache else None
               }
           ]

           # Remove None cache_control
           if not use_cache:
               system_messages[0].pop("cache_control", None)

           try:
               response = self.client.messages.create(
                   model=self.model,
                   max_tokens=4096,
                   system=system_messages,
                   messages=[{"role": "user", "content": prompt}],
                   **kwargs
               )

               # Parse JSON from response
               content_text = response.content[0].text
               parsed_json = json.loads(content_text)

               # Validate against schema
               validated = schema(**parsed_json)

               # Calculate cost
               usage = response.usage
               cost = self._calculate_cost(
                   input_tokens=usage.input_tokens,
                   output_tokens=usage.output_tokens,
                   cache_creation_tokens=getattr(usage, 'cache_creation_input_tokens', 0),
                   cache_read_tokens=getattr(usage, 'cache_read_input_tokens', 0)
               )

               return LLMResponse(
                   content=validated.model_dump(),
                   raw_response=response,
                   model=self.model,
                   tokens_used=usage.input_tokens + usage.output_tokens,
                   cost_usd=cost,
                   cached=usage.cache_read_input_tokens > 0 if hasattr(usage, 'cache_read_input_tokens') else False
               )

           except json.JSONDecodeError as e:
               raise RuntimeError(f"Failed to parse Claude response as JSON: {e}")
           except Exception as e:
               raise RuntimeError(f"Anthropic API error: {e}")

       def estimate_cost(self, prompt: str, schema: Type[BaseModel]) -> float:
           """Estimate cost based on token count."""
           # Rough token estimation (Claude uses different tokenizer)
           prompt_tokens = len(prompt) // 4  # Rough estimate
           schema_tokens = 500  # Typical schema size
           estimated_response_tokens = 1000

           input_tokens = prompt_tokens + schema_tokens
           output_tokens = estimated_response_tokens

           return self._calculate_cost(input_tokens, output_tokens)

       def _calculate_cost(
           self,
           input_tokens: int,
           output_tokens: int,
           cache_creation_tokens: int = 0,
           cache_read_tokens: int = 0
       ) -> float:
           """Calculate cost including cache pricing."""
           pricing = self.PRICING.get(self.model, self.PRICING["claude-3-5-sonnet-20241022"])

           # Base cost
           input_cost = (input_tokens / 1_000_000) * pricing["input"]
           output_cost = (output_tokens / 1_000_000) * pricing["output"]

           # Cache costs (if applicable)
           cache_cost = 0
           if self.model in self.CACHE_PRICING:
               cache_pricing = self.CACHE_PRICING[self.model]
               cache_cost = (
                   (cache_creation_tokens / 1_000_000) * cache_pricing["write"] +
                   (cache_read_tokens / 1_000_000) * cache_pricing["read"]
               )

           return input_cost + output_cost + cache_cost

       def count_tokens(self, text: str) -> int:
           """Rough token count (Anthropic doesn't provide tokenizer)."""
           return len(text) // 4  # Rough estimate

       def is_available(self) -> bool:
           """Check if Anthropic is available."""
           try:
               # Test with minimal request
               self.client.messages.create(
                   model=self.model,
                   max_tokens=1,
                   messages=[{"role": "user", "content": "test"}]
               )
               return True
           except Exception:
               return False
   ```

4. Create backend factory

   **File**: `src/reifire/backends/factory.py`
   ```python
   """Backend factory for selecting LLM providers."""
   from typing import Optional
   from .base import LLMBackend
   from .openai_backend import OpenAIBackend
   from .anthropic_backend import AnthropicBackend


   BACKENDS = {
       "openai": OpenAIBackend,
       "anthropic": AnthropicBackend,
   }


   def get_backend(
       provider: str = "openai",
       api_key: Optional[str] = None,
       model: Optional[str] = None
   ) -> LLMBackend:
       """
       Get LLM backend by provider name.

       Args:
           provider: Provider name (openai, anthropic)
           api_key: Optional API key
           model: Optional model name

       Returns:
           Initialized LLM backend

       Raises:
           ValueError: If provider is unknown
       """
       if provider not in BACKENDS:
           raise ValueError(f"Unknown provider: {provider}. Available: {list(BACKENDS.keys())}")

       backend_class = BACKENDS[provider]
       return backend_class(api_key=api_key, model=model)


   def list_backends() -> list[str]:
       """List available backend providers."""
       return list(BACKENDS.keys())
   ```

**Deliverables**:
- [ ] Abstract LLMBackend base class
- [ ] OpenAIBackend implementation
- [ ] AnthropicBackend implementation
- [ ] Backend factory
- [ ] Cost estimation utilities
- [ ] Unit tests with mocked API responses

**Success Criteria**: Both backends can parse prompts with structured output (using mocks)

---

### Week 3: Prompt Templates & Classification

#### Day 15-17: Prompt Type Classification 🔴

**Tasks**:
1. Create prompt classifier

   **File**: `src/reifire/parsing/__init__.py`
   ```python
   """Prompt parsing and classification."""
   from .classifier import PromptClassifier, PromptType
   from .prompt_templates import PromptTemplateManager
   from .llm_parser import LLMParser

   __all__ = [
       "PromptClassifier",
       "PromptType",
       "PromptTemplateManager",
       "LLMParser",
   ]
   ```

   **File**: `src/reifire/parsing/classifier.py`
   ```python
   """Classify prompts by type."""
   from enum import Enum
   from typing import Optional, Dict, Any
   import re


   class PromptType(Enum):
       """Types of prompts."""
       VISUAL = "visual"          # Images, illustrations, scenes
       CODE = "code"              # Code generation, APIs, functions
       DATA = "data"              # Queries, analysis, transformations
       TEXT = "text"              # Articles, documentation, content
       UI = "ui"                  # UI components, interfaces
       QA = "qa"                  # Questions, explanations


   class PromptClassifier:
       """Classify prompts into types."""

       # Keywords for each prompt type
       KEYWORDS = {
           PromptType.VISUAL: [
               "image", "illustration", "picture", "scene", "visual", "photo",
               "painting", "drawing", "render", "artwork", "design", "graphic",
               "color", "style", "mood", "composition"
           ],
           PromptType.CODE: [
               "code", "function", "class", "method", "api", "endpoint",
               "implementation", "algorithm", "program", "script", "module",
               "package", "library", "framework", "language", "middleware"
           ],
           PromptType.DATA: [
               "query", "database", "sql", "data", "analysis", "aggregate",
               "filter", "join", "group", "sort", "metrics", "statistics",
               "report", "dashboard", "chart", "graph", "visualization"
           ],
           PromptType.TEXT: [
               "article", "blog", "post", "essay", "document", "content",
               "write", "draft", "text", "copy", "description", "review",
               "summary", "report", "documentation"
           ],
           PromptType.UI: [
               "component", "widget", "form", "button", "input", "modal",
               "dialog", "menu", "navigation", "interface", "ui", "ux",
               "responsive", "layout", "screen", "page"
           ],
           PromptType.QA: [
               "explain", "what is", "how does", "why", "describe",
               "question", "answer", "definition", "meaning", "concept"
           ]
       }

       # Action verbs that suggest prompt type
       ACTION_VERBS = {
           PromptType.VISUAL: ["create", "generate", "draw", "paint", "render", "design"],
           PromptType.CODE: ["implement", "write", "create", "build", "develop", "code"],
           PromptType.DATA: ["analyze", "query", "aggregate", "filter", "calculate"],
           PromptType.TEXT: ["write", "draft", "compose", "summarize"],
           PromptType.UI: ["create", "build", "design", "implement"],
           PromptType.QA: ["explain", "describe", "define", "answer"]
       }

       def classify(self, prompt: str) -> PromptType:
           """
           Classify a prompt into a type.

           Args:
               prompt: Natural language prompt

           Returns:
               PromptType enum value
           """
           prompt_lower = prompt.lower()
           scores = {ptype: 0 for ptype in PromptType}

           # Score based on keywords
           for ptype, keywords in self.KEYWORDS.items():
               for keyword in keywords:
                   # Word boundary matching
                   if re.search(rf'\b{keyword}\b', prompt_lower):
                       scores[ptype] += 1

           # Score based on action verbs (higher weight)
           for ptype, verbs in self.ACTION_VERBS.items():
               for verb in verbs:
                   if re.search(rf'\b{verb}\b', prompt_lower):
                       scores[ptype] += 2

           # Return type with highest score
           if max(scores.values()) == 0:
               # Default to TEXT if no matches
               return PromptType.TEXT

           return max(scores, key=scores.get)

       def classify_with_confidence(self, prompt: str) -> tuple[PromptType, float]:
           """
           Classify prompt and return confidence score.

           Returns:
               (PromptType, confidence score 0-1)
           """
           prompt_lower = prompt.lower()
           scores = {ptype: 0 for ptype in PromptType}

           # Score keywords
           for ptype, keywords in self.KEYWORDS.items():
               for keyword in keywords:
                   if re.search(rf'\b{keyword}\b', prompt_lower):
                       scores[ptype] += 1

           # Score action verbs
           for ptype, verbs in self.ACTION_VERBS.items():
               for verb in verbs:
                   if re.search(rf'\b{verb}\b', prompt_lower):
                       scores[ptype] += 2

           # Calculate confidence
           total_score = sum(scores.values())
           if total_score == 0:
               return PromptType.TEXT, 0.0

           best_type = max(scores, key=scores.get)
           confidence = scores[best_type] / total_score

           return best_type, confidence
   ```

2. Add tests for classifier

   **File**: `tests/reifire/parsing/test_classifier.py`
   ```python
   """Tests for prompt classifier."""
   import pytest
   from reifire.parsing.classifier import PromptClassifier, PromptType


   def test_visual_classification():
       classifier = PromptClassifier()

       prompts = [
           "Create a dark fantasy dragon illustration",
           "Generate an image of a sunset",
           "Draw a cyberpunk cityscape"
       ]

       for prompt in prompts:
           assert classifier.classify(prompt) == PromptType.VISUAL


   def test_code_classification():
       classifier = PromptClassifier()

       prompts = [
           "Implement OAuth2 authentication middleware",
           "Write a Python function to sort a list",
           "Create a REST API endpoint"
       ]

       for prompt in prompts:
           assert classifier.classify(prompt) == PromptType.CODE


   def test_confidence_scores():
       classifier = PromptClassifier()

       prompt = "Create a dragon illustration"
       ptype, confidence = classifier.classify_with_confidence(prompt)

       assert ptype == PromptType.VISUAL
       assert 0 < confidence <= 1.0
   ```

**Deliverables**:
- [ ] PromptClassifier with keyword matching
- [ ] Confidence scoring
- [ ] Unit tests
- [ ] Documentation

**Success Criteria**: >90% accuracy on test prompts

---

#### Day 18-21: Prompt Templates 🔴

**Tasks**:
1. Create prompt template system

   **File**: `src/reifire/parsing/prompt_templates.py`
   ```python
   """Prompt templates for LLM-based reification."""
   from typing import Dict
   from .classifier import PromptType


   class PromptTemplateManager:
       """Manage prompt templates for different types."""

       SYSTEM_PROMPTS = {
           PromptType.VISUAL: """You are a visual content analyzer. Parse the user's prompt and extract:
   - The primary object being depicted
   - Object modifiers (age, size, mood, etc.)
   - The type of visual output (illustration, photo, scene, etc.)
   - Visual attributes (style, mood, color scheme, composition, time, weather, etc.)
   - Relationships between elements (what contains what, positioning, etc.)

   Output must be valid JSON matching the ReifiedStructure schema.
   Be precise and specific. Extract all visual details mentioned.""",

           PromptType.CODE: """You are a code requirements analyzer. Parse the user's prompt and extract:
   - The primary code component (function, class, API, etc.)
   - Component modifiers (type, scope, pattern, etc.)
   - The type of code output (implementation, refactor, etc.)
   - Code attributes (language, framework, style, documentation level, etc.)
   - Dependencies and relationships between components

   Output must be valid JSON matching the ReifiedStructure schema.
   Be precise about technical requirements.""",

           PromptType.DATA: """You are a data analysis requirements analyzer. Parse the user's prompt and extract:
   - The primary data object (table, dataset, etc.)
   - Data modifiers (time range, region, filters, etc.)
   - The type of data operation (query, analysis, transformation, etc.)
   - Data attributes (operations, grouping, metrics, format, etc.)
   - Relationships to other data sources

   Output must be valid JSON matching the ReifiedStructure schema.
   Be precise about data operations and metrics.""",

           PromptType.TEXT: """You are a content requirements analyzer. Parse the user's prompt and extract:
   - The primary content object (article, review, documentation, etc.)
   - Content modifiers (topic, subject, scope, etc.)
   - The type of text output (article, essay, documentation, etc.)
   - Text attributes (tone, perspective, structure, word count, etc.)
   - References and comparisons

   Output must be valid JSON matching the ReifiedStructure schema.
   Be precise about writing requirements.""",

           PromptType.UI: """You are a UI requirements analyzer. Parse the user's prompt and extract:
   - The primary UI component (button, form, page, etc.)
   - Component modifiers (type, scope, state, etc.)
   - The type of UI output (component, screen, layout, etc.)
   - UI attributes (framework, styling, theme, accessibility, etc.)
   - Component relationships and hierarchy

   Output must be valid JSON matching the ReifiedStructure schema.
   Be precise about UI/UX requirements.""",

           PromptType.QA: """You are a question/answer analyzer. Parse the user's prompt and extract:
   - The primary topic or concept being explained
   - Topic modifiers (scope, level of detail, etc.)
   - The type of explanation (definition, process, comparison, etc.)
   - Explanation attributes (complexity, format, tone, etc.)
   - Related concepts and dependencies

   Output must be valid JSON matching the ReifiedStructure schema.
   Be precise about educational requirements."""
       }

       USER_PROMPT_TEMPLATES = {
           PromptType.VISUAL: """Parse this visual content request:

   "{prompt}"

   Extract all details about the object, visual style, mood, colors, composition, and any relationships between elements.""",

           PromptType.CODE: """Parse this code generation request:

   "{prompt}"

   Extract all details about the code component, programming language, frameworks, style, documentation, and dependencies.""",

           PromptType.DATA: """Parse this data analysis request:

   "{prompt}"

   Extract all details about the data source, operations, grouping, metrics, format, and relationships.""",

           PromptType.TEXT: """Parse this content writing request:

   "{prompt}"

   Extract all details about the content type, tone, structure, word count, and references.""",

           PromptType.UI: """Parse this UI component request:

   "{prompt}"

   Extract all details about the component, framework, styling, theme, accessibility, and hierarchy.""",

           PromptType.QA: """Parse this explanation request:

   "{prompt}"

   Extract all details about the topic, complexity level, format, and related concepts."""
       }

       def get_system_prompt(self, prompt_type: PromptType) -> str:
           """Get system prompt for a given type."""
           return self.SYSTEM_PROMPTS[prompt_type]

       def get_user_prompt(self, prompt_type: PromptType, user_prompt: str) -> str:
           """Get formatted user prompt for a given type."""
           template = self.USER_PROMPT_TEMPLATES[prompt_type]
           return template.format(prompt=user_prompt)

       def get_prompts(self, prompt_type: PromptType, user_prompt: str) -> Dict[str, str]:
           """
           Get both system and user prompts.

           Returns:
               {"system": system_prompt, "user": user_prompt}
           """
           return {
               "system": self.get_system_prompt(prompt_type),
               "user": self.get_user_prompt(prompt_type, user_prompt)
           }
   ```

**Deliverables**:
- [ ] Template system for all 6 prompt types
- [ ] System prompts optimized for structured output
- [ ] User prompt templates
- [ ] Template tests

**Success Criteria**: Templates produce valid reified structures with test LLMs

---

### Week 4: Core Reify Function

#### Day 22-25: LLM Parser Implementation 🔴 CRITICAL

**Tasks**:
1. Implement core LLM parser

   **File**: `src/reifire/parsing/llm_parser.py`
   ```python
   """LLM-based prompt parser."""
   from typing import Dict, Any, Optional
   from pydantic import ValidationError

   from ..backends.base import LLMBackend, LLMResponse
   from ..backends.factory import get_backend
   from ..schema.models import ReifiedStructure
   from ..schema.validators import validate_and_fix
   from .classifier import PromptClassifier, PromptType
   from .prompt_templates import PromptTemplateManager


   class ParsingError(Exception):
       """Error during prompt parsing."""
       pass


   class LLMParser:
       """Parse prompts using LLM backends."""

       def __init__(
           self,
           backend: Optional[LLMBackend] = None,
           llm_provider: str = "openai",
           model: Optional[str] = None
       ):
           """
           Initialize LLM parser.

           Args:
               backend: LLM backend instance (or None to create from provider)
               llm_provider: Provider name if backend not provided
               model: Model name
           """
           self.backend = backend or get_backend(llm_provider, model=model)
           self.classifier = PromptClassifier()
           self.templates = PromptTemplateManager()

       def parse(
           self,
           prompt: str,
           prompt_type: Optional[PromptType] = None,
           auto_fix: bool = True,
           max_retries: int = 2
       ) -> Dict[str, Any]:
           """
           Parse a natural language prompt into reified structure.

           Args:
               prompt: Natural language prompt
               prompt_type: Optional prompt type (auto-detected if None)
               auto_fix: Attempt to fix validation errors
               max_retries: Max retry attempts on validation failure

           Returns:
               Reified structure dictionary

           Raises:
               ParsingError: If parsing fails after retries
           """
           # Classify prompt if type not provided
           if prompt_type is None:
               prompt_type, confidence = self.classifier.classify_with_confidence(prompt)
               if confidence < 0.3:
                   # Low confidence, try with TEXT type as fallback
                   prompt_type = PromptType.TEXT

           # Get appropriate prompts
           prompts = self.templates.get_prompts(prompt_type, prompt)

           # Attempt parsing with retries
           last_error = None
           for attempt in range(max_retries + 1):
               try:
                   # Call LLM
                   response = self.backend.parse_prompt(
                       prompt=prompts["user"],
                       schema=ReifiedStructure,
                       system_prompt=prompts["system"]
                   )

                   # Validate structure
                   if auto_fix:
                       fixed, validation = validate_and_fix(response.content)
                       if not validation.valid:
                           raise ParsingError(f"Validation failed: {validation.errors}")
                       reified = fixed
                   else:
                       reified = response.content

                   # Add metadata
                   if "metadata" not in reified:
                       reified["metadata"] = {}

                   reified["metadata"]["original_prompt"] = prompt
                   reified["metadata"]["prompt_type"] = prompt_type.value
                   reified["metadata"]["llm_model"] = response.model
                   reified["metadata"]["tokens_used"] = response.tokens_used
                   reified["metadata"]["cost_usd"] = response.cost_usd
                   reified["metadata"]["processing_info"] = {
                       "attempt": attempt + 1,
                       "auto_fixed": auto_fix,
                   }

                   return reified

               except ValidationError as e:
                   last_error = e
                   if attempt < max_retries:
                       # Add validation error to next prompt
                       prompts["user"] += f"\n\nPrevious attempt had errors: {e}\nPlease fix these issues."
                   continue

               except Exception as e:
                   last_error = e
                   if attempt < max_retries:
                       continue
                   break

           # All attempts failed
           raise ParsingError(f"Failed to parse prompt after {max_retries + 1} attempts: {last_error}")

       def estimate_cost(self, prompt: str) -> float:
           """Estimate cost of parsing this prompt."""
           return self.backend.estimate_cost(prompt, ReifiedStructure)
   ```

2. Add caching layer

   **File**: `src/reifire/parsing/cache.py`
   ```python
   """Caching layer for parsed prompts."""
   import hashlib
   import json
   from pathlib import Path
   from typing import Dict, Any, Optional
   from datetime import datetime, timedelta


   class ParseCache:
       """Cache for parsed prompts."""

       def __init__(self, cache_dir: Optional[Path] = None, ttl_days: int = 30):
           """
           Initialize cache.

           Args:
               cache_dir: Directory for cache files (default: ~/.reifire/parse_cache)
               ttl_days: Time-to-live for cache entries in days
           """
           self.cache_dir = cache_dir or (Path.home() / ".reifire" / "parse_cache")
           self.cache_dir.mkdir(parents=True, exist_ok=True)
           self.ttl = timedelta(days=ttl_days)

       def _get_cache_key(self, prompt: str, llm_model: str) -> str:
           """Generate cache key from prompt and model."""
           content = f"{prompt}:{llm_model}"
           return hashlib.sha256(content.encode()).hexdigest()

       def _get_cache_path(self, cache_key: str) -> Path:
           """Get path to cache file."""
           return self.cache_dir / f"{cache_key}.json"

       def get(self, prompt: str, llm_model: str) -> Optional[Dict[str, Any]]:
           """
           Get cached parse result.

           Returns:
               Cached reified structure or None if not found/expired
           """
           cache_key = self._get_cache_key(prompt, llm_model)
           cache_path = self._get_cache_path(cache_key)

           if not cache_path.exists():
               return None

           try:
               data = json.loads(cache_path.read_text())

               # Check expiration
               cached_at = datetime.fromisoformat(data["cached_at"])
               if datetime.now() - cached_at > self.ttl:
                   # Expired
                   cache_path.unlink()
                   return None

               return data["reified"]

           except Exception:
               # Corrupt cache file
               cache_path.unlink()
               return None

       def set(self, prompt: str, llm_model: str, reified: Dict[str, Any]) -> None:
           """Cache a parse result."""
           cache_key = self._get_cache_key(prompt, llm_model)
           cache_path = self._get_cache_path(cache_key)

           data = {
               "prompt": prompt,
               "llm_model": llm_model,
               "cached_at": datetime.now().isoformat(),
               "reified": reified
           }

           cache_path.write_text(json.dumps(data, indent=2))

       def clear(self) -> int:
           """
           Clear all cache entries.

           Returns:
               Number of entries cleared
           """
           count = 0
           for cache_file in self.cache_dir.glob("*.json"):
               cache_file.unlink()
               count += 1
           return count

       def clear_expired(self) -> int:
           """
           Clear expired cache entries.

           Returns:
               Number of entries cleared
           """
           count = 0
           for cache_file in self.cache_dir.glob("*.json"):
               try:
                   data = json.loads(cache_file.read_text())
                   cached_at = datetime.fromisoformat(data["cached_at"])
                   if datetime.now() - cached_at > self.ttl:
                       cache_file.unlink()
                       count += 1
               except Exception:
                   # Corrupt file, remove it
                   cache_file.unlink()
                   count += 1
           return count
   ```

3. Implement main `reify()` function

   **File**: `src/reifire/reify.py`
   ```python
   """Main reification function."""
   from typing import Dict, Any, Optional
   from .parsing.llm_parser import LLMParser
   from .parsing.cache import ParseCache
   from .parsing.classifier import PromptType


   def reify(
       prompt: str,
       llm_provider: str = "openai",
       model: Optional[str] = None,
       prompt_type: Optional[PromptType] = None,
       use_cache: bool = True,
       auto_fix: bool = True,
       max_retries: int = 2
   ) -> Dict[str, Any]:
       """
       Reify a natural language prompt into a structured representation.

       This is the main entry point for the reifire library. It takes a natural
       language prompt and converts it into a structured reified data format
       that can be manipulated, visualized, and re-articulated.

       Args:
           prompt: Natural language prompt to reify
           llm_provider: LLM provider to use (openai, anthropic)
           model: Specific model name (or None for default)
           prompt_type: Optional prompt type (auto-detected if None)
           use_cache: Whether to use cache for repeated prompts
           auto_fix: Attempt to fix validation errors automatically
           max_retries: Maximum retry attempts on parsing failures

       Returns:
           Reified structure dictionary matching DATASPEC schema

       Raises:
           ParsingError: If parsing fails after retries
           ValueError: If invalid parameters provided

       Example:
           >>> from reifire import reify
           >>> result = reify("Create a dark fantasy dragon illustration")
           >>> print(result["object"]["name"])
           'dragon'
           >>> print(result["type"]["category"])
           'visual'
       """
       # Initialize parser
       parser = LLMParser(llm_provider=llm_provider, model=model)

       # Check cache
       if use_cache:
           cache = ParseCache()
           cached_result = cache.get(prompt, parser.backend.model)
           if cached_result:
               # Add cache hit to metadata
               cached_result.setdefault("metadata", {}).setdefault("processing_info", {})["cached"] = True
               return cached_result

       # Parse prompt
       reified = parser.parse(
           prompt=prompt,
           prompt_type=prompt_type,
           auto_fix=auto_fix,
           max_retries=max_retries
       )

       # Cache result
       if use_cache:
           cache.set(prompt, parser.backend.model, reified)

       return reified
   ```

4. Update package `__init__.py`

   **File**: `src/reifire/__init__.py`
   ```python
   """Reifire package for converting between reified data structures and natural language prompts."""

   __version__ = "0.1.0"

   from .reify import reify  # noqa: F401
   from .articulation import articulate, articulate_alternatives  # noqa: F401
   from .parsing.classifier import PromptType  # noqa: F401
   from .schema.models import ReifiedStructure  # noqa: F401

   __all__ = [
       "reify",
       "articulate",
       "articulate_alternatives",
       "PromptType",
       "ReifiedStructure",
   ]
   ```

**Deliverables**:
- [ ] Complete LLMParser implementation
- [ ] Caching layer
- [ ] Main reify() function
- [ ] Updated package exports
- [ ] Unit tests with mocked LLM responses
- [ ] Integration tests with real APIs (optional, slow)

**Success Criteria**:
- `reify("Create a dragon illustration")` returns valid reified structure
- Cached calls are instant
- Tests pass with >80% coverage

---

#### Day 26-28: Testing & Documentation 🟡

**Tasks**:
1. Comprehensive testing
   - Unit tests for all parsing components
   - Integration tests with mocked LLM responses
   - End-to-end tests: `reify() → articulate() → reify()`
   - Performance tests (caching effectiveness)
   - Cost estimation tests

2. Update documentation
   - API reference for new functions
   - Usage examples in README
   - Add example notebook (Jupyter)

3. Create example scripts

   **File**: `examples/basic_reification.py`
   ```python
   """Basic reification example."""
   from reifire import reify, articulate
   import json

   # Reify a prompt
   prompt = "Create a dark fantasy dragon illustration with purple and black color scheme"

   print(f"Original prompt: {prompt}\n")

   # Perform reification
   reified = reify(prompt)

   # Show reified structure
   print("Reified structure:")
   print(json.dumps(reified, indent=2))

   # Articulate back to natural language
   articulated = articulate(reified)
   print(f"\nRe-articulated: {articulated}")
   ```

**Deliverables**:
- [ ] Complete test suite
- [ ] Updated API documentation
- [ ] Example scripts
- [ ] Jupyter notebook tutorial

**Success Criteria**:
- All tests passing
- Documentation complete
- Examples work end-to-end

---

## Phase 2: Core Reification (Weeks 5-8)

**Goal**: Expand reification to all domains, add emoji icons, improve quality

### Week 5: Multi-Domain Support

#### Day 29-31: Extended Prompt Templates 🟡

**Tasks**:
1. Refine templates for all 6 domains based on Week 4 results
2. Add domain-specific validation rules
3. Improve prompt engineering for better extraction
4. Add examples for each domain

**Deliverables**:
- [ ] Optimized templates for visual, code, data, text, UI, QA
- [ ] Domain-specific validators
- [ ] Example gallery with all domains

**Success Criteria**: >90% valid structures for each domain

---

#### Day 32-35: Alternative Generation 🟡

**Tasks**:
1. Implement alternative value generation

   **File**: `src/reifire/parsing/alternatives.py`
   ```python
   """Generate alternatives for reified components."""
   from typing import Dict, Any, List
   from ..backends.base import LLMBackend


   class AlternativeGenerator:
       """Generate alternatives for components."""

       def __init__(self, backend: LLMBackend):
           self.backend = backend

       def generate_alternatives(
           self,
           component: Dict[str, Any],
           component_type: str,
           count: int = 3
       ) -> List[Dict[str, Any]]:
           """
           Generate alternative values for a component.

           Args:
               component: Component to generate alternatives for
               component_type: Type of component (modifier, attribute, etc.)
               count: Number of alternatives to generate

           Returns:
               List of alternative component values
           """
           # Build prompt for alternatives
           prompt = f"""Given this {component_type}:

   {json.dumps(component, indent=2)}

   Generate {count} alternative values that would work in a similar context.
   For example, if the value is "dark fantasy", alternatives might be "gothic", "horror", "noir".

   Return JSON array of alternatives in the same format."""

           # Call LLM
           # ... implementation

       def enrich_with_alternatives(
           self,
           reified: Dict[str, Any],
           max_alternatives_per_component: int = 3
       ) -> Dict[str, Any]:
           """
           Add alternatives to all components in reified structure.

           Args:
               reified: Reified structure
               max_alternatives_per_component: Max alternatives per component

           Returns:
               Enhanced reified structure with alternatives
           """
           # Add alternatives to modifiers
           if "object" in reified and "modifiers" in reified["object"]:
               for modifier in reified["object"]["modifiers"]:
                   if "alternatives" not in modifier or not modifier["alternatives"]:
                       alternatives = self.generate_alternatives(
                           modifier, "modifier", max_alternatives_per_component
                       )
                       modifier["alternatives"] = alternatives

           # Add alternatives to attributes
           if "artifact" in reified and "attributes" in reified["artifact"]:
               for attribute in reified["artifact"]["attributes"]:
                   if "alternatives" not in attribute or not attribute["alternatives"]:
                       alternatives = self.generate_alternatives(
                           attribute, "attribute", max_alternatives_per_component
                       )
                       attribute["alternatives"] = alternatives

           return reified
   ```

2. Add alternative generation to reify() function
3. Test alternative swapping in visualizations

**Deliverables**:
- [ ] AlternativeGenerator class
- [ ] Integration with reify()
- [ ] Working alternative swapping in UI

**Success Criteria**: Alternatives are relevant and usable

---

### Week 6: Emoji Icon Support

#### Day 36-38: Emoji Provider 🟡

**Tasks**:
1. Implement EmojiProvider

   **File**: `src/reifire/visualization/emoji_provider.py`
   ```python
   """Emoji icon provider."""
   import emoji
   from typing import Optional, Dict, Any
   from PIL import Image, ImageDraw, ImageFont
   import base64
   from io import BytesIO


   class EmojiProvider:
       """Provide emoji as icons."""

       def __init__(self, emoji_font_path: Optional[str] = None):
           """
           Initialize emoji provider.

           Args:
               emoji_font_path: Path to emoji font (NotoColorEmoji.ttf)
                   If None, tries common system locations
           """
           self.emoji_font_path = emoji_font_path or self._find_emoji_font()

           # Term to emoji mapping (extensive list)
           self.term_to_emoji = {
               # Emotions
               "happy": "😊", "sad": "😢", "angry": "😠", "love": "❤️",
               "excited": "🤩", "scared": "😱", "surprised": "😲",

               # Tech
               "code": "💻", "api": "🔌", "database": "🗄️", "server": "🖥️",
               "bug": "🐛", "security": "🔒", "key": "🔑", "cloud": "☁️",

               # Visual
               "art": "🎨", "paint": "🖌️", "camera": "📷", "image": "🖼️",
               "color": "🌈", "star": "⭐", "sun": "☀️", "moon": "🌙",

               # UI
               "button": "🔘", "menu": "☰", "settings": "⚙️", "search": "🔍",
               "home": "🏠", "profile": "👤", "notification": "🔔",

               # Data
               "chart": "📊", "graph": "📈", "calendar": "📅", "file": "📄",

               # ... hundreds more
           }

       def _find_emoji_font(self) -> Optional[str]:
           """Find emoji font on system."""
           common_paths = [
               "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",  # Linux
               "/System/Library/Fonts/Apple Color Emoji.ttc",  # macOS
               "C:\\Windows\\Fonts\\seguiemj.ttf",  # Windows
           ]

           for path in common_paths:
               if Path(path).exists():
                   return path

           return None

       def get_emoji(self, term: str) -> Optional[str]:
           """
           Get emoji for term.

           Returns:
               Emoji character or None
           """
           # Direct lookup
           if term.lower() in self.term_to_emoji:
               return self.term_to_emoji[term.lower()]

           # Try emoji library search
           emojized = emoji.emojize(f":{term.lower().replace(' ', '_')}:", language='alias')
           if emojized != f":{term.lower().replace(' ', '_')}:":
               return emojized

           return None

       def emoji_to_data_uri(self, emoji_char: str, size: int = 72) -> str:
           """
           Convert emoji to data URI for HTML embedding.

           Args:
               emoji_char: Emoji character
               size: Image size in pixels

           Returns:
               Data URI string
           """
           if not self.emoji_font_path:
               # Fallback to text representation
               return f"data:text/plain;base64,{base64.b64encode(emoji_char.encode()).decode()}"

           # Render emoji to image
           img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
           draw = ImageDraw.Draw(img)

           # Load emoji font
           font_size = int(size * 0.9)
           font = ImageFont.truetype(self.emoji_font_path, font_size)

           # Draw emoji
           draw.text(
               (size * 0.05, size * 0.05),
               emoji_char,
               font=font,
               embedded_color=True
           )

           # Convert to data URI
           buffer = BytesIO()
           img.save(buffer, format='PNG')
           b64 = base64.b64encode(buffer.getvalue()).decode()

           return f"data:image/png;base64,{b64}"

       def get_icon(self, term: str) -> Optional[Dict[str, Any]]:
           """
           Get icon metadata for term.

           Returns:
               Icon metadata dict or None
           """
           emoji_char = self.get_emoji(term)
           if not emoji_char:
               return None

           return {
               "source": "emoji",
               "name": term,
               "emoji": emoji_char,
               "image": self.emoji_to_data_uri(emoji_char)
           }
   ```

2. Integrate with IconManager
3. Update visualizations to support emoji icons

**Deliverables**:
- [ ] EmojiProvider implementation
- [ ] Integration with IconManager
- [ ] Updated visualizations
- [ ] Tests

**Success Criteria**: Emoji icons display correctly in visualizations

---

#### Day 39-42: Icon Priority System 🟡

**Tasks**:
1. Implement configurable icon provider priority

   **File**: `src/reifire/visualization/icon_manager.py` (updated)
   ```python
   """Icon manager with priority system."""

   class IconManager:
       """Manage icons from multiple providers with priority."""

       def __init__(
           self,
           providers: Optional[List[IconProvider]] = None,
           default_priority: Optional[List[str]] = None
       ):
           """
           Initialize icon manager.

           Args:
               providers: List of icon providers
               default_priority: Default provider priority order
           """
           self.providers = providers or []
           self.default_priority = default_priority or [
               "emoji",           # Fast, always available
               "material",        # Local, fast
               "fontawesome",     # CDN, fast
               "nounproject",     # API, rate limited
               "custom",          # User uploads
           ]

       async def get_icon(
           self,
           term: str,
           priority: Optional[List[str]] = None
       ) -> Optional[Dict[str, Any]]:
           """
           Get icon with priority fallback.

           Args:
               term: Term to find icon for
               priority: Custom priority order (or None for default)

           Returns:
               Icon metadata or None
           """
           priority = priority or self.default_priority

           for provider_name in priority:
               provider = self._get_provider(provider_name)
               if not provider:
                   continue

               try:
                   icon = await provider.get_icon(term)
                   if icon:
                       return icon
               except Exception as e:
                   logger.warning(f"Provider {provider_name} failed for {term}: {e}")
                   continue

           return None
   ```

2. Add configuration for icon preferences
3. Update example configurations

**Deliverables**:
- [ ] Priority-based icon selection
- [ ] Configuration system
- [ ] Documentation

**Success Criteria**: Users can configure icon provider preferences

---

### Week 7: Quality Improvements

#### Day 43-45: Round-Trip Validation 🟡

**Tasks**:
1. Implement semantic similarity comparison

   **File**: `src/reifire/validation/roundtrip.py`
   ```python
   """Round-trip validation for reification quality."""
   from typing import Dict, Any
   from ..reify import reify
   from ..articulation import articulate


   def validate_roundtrip(prompt: str, similarity_threshold: float = 0.9) -> Dict[str, Any]:
       """
       Validate round-trip consistency: prompt -> reify -> articulate -> reify.

       Args:
           prompt: Original prompt
           similarity_threshold: Minimum similarity score (0-1)

       Returns:
           {
               "passed": bool,
               "similarity": float,
               "original_reified": dict,
               "roundtrip_reified": dict,
               "articulated": str,
               "differences": list
           }
       """
       # First reification
       reified1 = reify(prompt)

       # Articulate back
       articulated = articulate(reified1)

       # Second reification
       reified2 = reify(articulated)

       # Compare structures
       similarity = compute_semantic_similarity(reified1, reified2)
       differences = find_differences(reified1, reified2)

       return {
           "passed": similarity >= similarity_threshold,
           "similarity": similarity,
           "original_reified": reified1,
           "roundtrip_reified": reified2,
           "articulated": articulated,
           "differences": differences
       }


   def compute_semantic_similarity(reified1: Dict[str, Any], reified2: Dict[str, Any]) -> float:
       """
       Compute semantic similarity between two reified structures.

       Returns:
           Similarity score 0-1
       """
       # Compare key components
       scores = []

       # Object name similarity
       obj1_name = reified1.get("object", {}).get("name", "")
       obj2_name = reified2.get("object", {}).get("name", "")
       scores.append(string_similarity(obj1_name, obj2_name))

       # Type similarity
       type1 = reified1.get("type", {}).get("name", "")
       type2 = reified2.get("type", {}).get("name", "")
       scores.append(string_similarity(type1, type2))

       # Attribute similarity
       attrs1 = set(a["name"] for a in reified1.get("artifact", {}).get("attributes", []))
       attrs2 = set(a["name"] for a in reified2.get("artifact", {}).get("attributes", []))
       if attrs1 or attrs2:
           scores.append(len(attrs1 & attrs2) / len(attrs1 | attrs2))

       return sum(scores) / len(scores) if scores else 0.0


   def string_similarity(s1: str, s2: str) -> float:
       """Simple string similarity (can use more sophisticated methods)."""
       if not s1 and not s2:
           return 1.0
       if not s1 or not s2:
           return 0.0

       # Levenshtein distance ratio
       from difflib import SequenceMatcher
       return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
   ```

2. Add quality metrics dashboard
3. Create test suite for round-trip validation

**Deliverables**:
- [ ] Round-trip validation system
- [ ] Quality metrics
- [ ] Test suite

**Success Criteria**: >90% round-trip accuracy on test set

---

#### Day 46-49: Error Handling & Retry Logic 🟡

**Tasks**:
1. Improve error handling in LLM parser
2. Add exponential backoff for API failures
3. Implement fallback strategies
4. Add detailed error reporting

**Example**:
```python
class RetryStrategy:
    """Retry strategy for LLM calls."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
        max_delay: float = 60.0
    ):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay

    async def execute(self, func, *args, **kwargs):
        """Execute function with retry logic."""
        delay = self.initial_delay
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except RateLimitError:
                # Wait and retry
                await asyncio.sleep(delay)
                delay = min(delay * self.backoff_factor, self.max_delay)
                continue
            except ValidationError as e:
                # Try to fix and retry
                last_exception = e
                continue
            except Exception as e:
                last_exception = e
                break

        raise last_exception
```

**Deliverables**:
- [ ] Robust error handling
- [ ] Retry strategies
- [ ] Fallback mechanisms
- [ ] Error reporting

**Success Criteria**: Graceful handling of API failures

---

### Week 8: Performance & Optimization

#### Day 50-52: Async Support 🟡

**Tasks**:
1. Add async versions of all functions

   **File**: `src/reifire/async_reify.py`
   ```python
   """Async version of reification functions."""
   import asyncio
   from typing import Dict, Any, Optional
   from .parsing.llm_parser import LLMParser
   from .parsing.classifier import PromptType


   async def reify_async(
       prompt: str,
       llm_provider: str = "openai",
       model: Optional[str] = None,
       **kwargs
   ) -> Dict[str, Any]:
       """Async version of reify()."""
       # ... async implementation
       pass


   async def reify_batch(
       prompts: List[str],
       llm_provider: str = "openai",
       max_concurrent: int = 5,
       **kwargs
   ) -> List[Dict[str, Any]]:
       """
       Reify multiple prompts concurrently.

       Args:
           prompts: List of prompts to reify
           llm_provider: LLM provider
           max_concurrent: Max concurrent requests

       Returns:
           List of reified structures
       """
       semaphore = asyncio.Semaphore(max_concurrent)

       async def reify_with_semaphore(prompt):
           async with semaphore:
               return await reify_async(prompt, llm_provider, **kwargs)

       tasks = [reify_with_semaphore(p) for p in prompts]
       return await asyncio.gather(*tasks)
   ```

2. Add streaming support for visualization updates
3. Optimize for concurrent requests

**Deliverables**:
- [ ] Async API
- [ ] Batch processing
- [ ] Streaming support
- [ ] Tests

**Success Criteria**: 5x speedup on batch operations

---

#### Day 53-56: Cost Optimization 🟡

**Tasks**:
1. Implement intelligent caching strategies
2. Add cost tracking per user/session
3. Optimize prompt templates for token efficiency
4. Add budget limits and warnings

**File**: `src/reifire/cost_tracking.py`
```python
"""Cost tracking and budget management."""
from typing import Dict, Any
from datetime import datetime
import json
from pathlib import Path


class CostTracker:
    """Track API costs."""

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or (Path.home() / ".reifire" / "costs.json")
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.costs = self._load_costs()

    def record_cost(
        self,
        operation: str,
        llm_provider: str,
        model: str,
        cost_usd: float,
        tokens_used: int
    ):
        """Record a cost entry."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "llm_provider": llm_provider,
            "model": model,
            "cost_usd": cost_usd,
            "tokens_used": tokens_used
        }

        month_key = datetime.now().strftime("%Y-%m")
        if month_key not in self.costs:
            self.costs[month_key] = []

        self.costs[month_key].append(entry)
        self._save_costs()

    def get_monthly_cost(self, year: int, month: int) -> float:
        """Get total cost for a month."""
        month_key = f"{year:04d}-{month:02d}"
        entries = self.costs.get(month_key, [])
        return sum(e["cost_usd"] for e in entries)

    def get_current_month_cost(self) -> float:
        """Get cost for current month."""
        now = datetime.now()
        return self.get_monthly_cost(now.year, now.month)
```

**Deliverables**:
- [ ] Cost tracking system
- [ ] Budget warnings
- [ ] Optimization recommendations
- [ ] Cost dashboard

**Success Criteria**: <$0.05 per reification on average

---

## Phase 3: Web API (Weeks 9-12)

**Goal**: Build production-ready Litestar web API

### Week 9: API Foundation

#### Day 57-59: Litestar Setup 🟡

**Tasks**:
1. Create Litestar application structure

   **File**: `src/reifire/api/app.py`
   ```python
   """Litestar application."""
   from litestar import Litestar, Router
   from litestar.config.cors import CORSConfig
   from litestar.contrib.pydantic import PydanticPlugin

   from .routes import reification, articulation, visualization, health
   from .middleware.auth import AuthMiddleware
   from .middleware.rate_limit import RateLimitMiddleware
   from .config import get_settings


   def create_app() -> Litestar:
       """Create Litestar application."""
       settings = get_settings()

       # CORS config
       cors_config = CORSConfig(
           allow_origins=settings.cors_origins,
           allow_methods=["GET", "POST", "OPTIONS"],
           allow_headers=["*"],
       )

       # Router
       router = Router(
           path="/api/v1",
           route_handlers=[
               reification.router,
               articulation.router,
               visualization.router,
               health.router,
           ],
       )

       # Application
       app = Litestar(
           route_handlers=[router],
           cors_config=cors_config,
           plugins=[PydanticPlugin()],
           middleware=[AuthMiddleware, RateLimitMiddleware],
           debug=settings.debug,
       )

       return app


   app = create_app()
   ```

2. Set up configuration management

   **File**: `src/reifire/api/config.py`
   ```python
   """API configuration."""
   from pydantic_settings import BaseSettings
   from typing import List


   class Settings(BaseSettings):
       """Application settings."""

       # API settings
       api_title: str = "Reifire API"
       api_version: str = "1.0.0"
       debug: bool = False

       # CORS
       cors_origins: List[str] = ["*"]

       # Auth
       api_key_header: str = "X-API-Key"
       require_auth: bool = True

       # Rate limiting
       rate_limit_per_minute: int = 10

       # LLM
       default_llm_provider: str = "openai"
       openai_api_key: str = ""
       anthropic_api_key: str = ""

       # Redis (for caching/rate limiting)
       redis_url: str = "redis://localhost:6379"

       class Config:
           env_file = ".env"


   _settings = None


   def get_settings() -> Settings:
       """Get settings singleton."""
       global _settings
       if _settings is None:
           _settings = Settings()
       return _settings
   ```

3. Create request/response models

   **File**: `src/reifire/api/models/requests.py`
   ```python
   """API request models."""
   from pydantic import BaseModel, Field
   from typing import Optional, List
   from reifire.parsing.classifier import PromptType


   class ReifyRequest(BaseModel):
       """Request to reify a prompt."""

       prompt: str = Field(..., description="Natural language prompt to reify", min_length=1)
       llm_provider: str = Field(default="openai", description="LLM provider (openai, anthropic)")
       model: Optional[str] = Field(None, description="Specific model name")
       prompt_type: Optional[PromptType] = Field(None, description="Optional prompt type hint")
       use_cache: bool = Field(default=True, description="Use cache for repeated prompts")
       add_alternatives: bool = Field(default=True, description="Generate alternatives")
       icon_providers: Optional[List[str]] = Field(None, description="Icon provider priority")


   class ArticulateRequest(BaseModel):
       """Request to articulate a reified structure."""

       reified: dict = Field(..., description="Reified structure to articulate")
       style: str = Field(default="standard", description="Articulation style")


   class VisualizeRequest(BaseModel):
       """Request to generate visualization."""

       reified: dict = Field(..., description="Reified structure to visualize")
       layout: str = Field(default="hierarchical", description="Layout algorithm")
       include_icons: bool = Field(default=True, description="Include icons")
       icon_providers: Optional[List[str]] = Field(None, description="Icon provider priority")


   class WorkflowRequest(BaseModel):
       """Complete workflow request."""

       prompt: str = Field(..., description="Natural language prompt")
       steps: List[str] = Field(default=["reify", "visualize", "articulate"])
       llm_provider: str = Field(default="openai")
       model: Optional[str] = Field(None)
   ```

   **File**: `src/reifire/api/models/responses.py`
   ```python
   """API response models."""
   from pydantic import BaseModel
   from typing import Optional, Dict, Any


   class ProcessingMetadata(BaseModel):
       """Metadata about processing."""

       processing_time_ms: int
       cost_usd: float
       cached: bool
       tokens_used: Optional[int] = None
       llm_model: Optional[str] = None


   class ReifyResponse(BaseModel):
       """Response from reification."""

       reified: Dict[str, Any]
       metadata: ProcessingMetadata


   class ArticulateResponse(BaseModel):
       """Response from articulation."""

       prompt: str
       alternatives: Optional[list[str]] = None
       metadata: ProcessingMetadata


   class VisualizeResponse(BaseModel):
       """Response from visualization."""

       html: str
       metadata: ProcessingMetadata


   class WorkflowResponse(BaseModel):
       """Response from complete workflow."""

       reified: Optional[Dict[str, Any]] = None
       visualization_html: Optional[str] = None
       articulated_prompt: Optional[str] = None
       metadata: ProcessingMetadata
   ```

**Deliverables**:
- [ ] Litestar app structure
- [ ] Configuration management
- [ ] Request/response models
- [ ] Basic routing

**Success Criteria**: App starts and responds to health checks

---

#### Day 60-63: Core Endpoints 🔴

**Tasks**:
1. Implement reification endpoint

   **File**: `src/reifire/api/routes/reification.py`
   ```python
   """Reification endpoints."""
   from litestar import Router, post
   from litestar.exceptions import HTTPException
   from litestar.status_codes import HTTP_400_BAD_REQUEST
   import time

   from ..models.requests import ReifyRequest
   from ..models.responses import ReifyResponse, ProcessingMetadata
   from reifire import reify
   from reifire.parsing.alternatives import AlternativeGenerator


   @post("/reify")
   async def reify_endpoint(data: ReifyRequest) -> ReifyResponse:
       """
       Reify a natural language prompt.

       Args:
           data: Reification request

       Returns:
           ReifyResponse with reified structure

       Raises:
           HTTPException: If reification fails
       """
       start_time = time.time()

       try:
           # Perform reification
           reified = reify(
               prompt=data.prompt,
               llm_provider=data.llm_provider,
               model=data.model,
               prompt_type=data.prompt_type,
               use_cache=data.use_cache
           )

           # Add alternatives if requested
           if data.add_alternatives:
               from reifire.backends.factory import get_backend
               backend = get_backend(data.llm_provider, model=data.model)
               alt_gen = AlternativeGenerator(backend)
               reified = alt_gen.enrich_with_alternatives(reified)

           # Build metadata
           processing_time_ms = int((time.time() - start_time) * 1000)
           metadata = ProcessingMetadata(
               processing_time_ms=processing_time_ms,
               cost_usd=reified.get("metadata", {}).get("cost_usd", 0.0),
               cached=reified.get("metadata", {}).get("processing_info", {}).get("cached", False),
               tokens_used=reified.get("metadata", {}).get("tokens_used"),
               llm_model=reified.get("metadata", {}).get("llm_model")
           )

           return ReifyResponse(reified=reified, metadata=metadata)

       except Exception as e:
           raise HTTPException(
               status_code=HTTP_400_BAD_REQUEST,
               detail=f"Reification failed: {str(e)}"
           )


   router = Router(path="/reify", route_handlers=[reify_endpoint])
   ```

2. Implement articulation endpoint
3. Implement visualization endpoint
4. Implement workflow endpoint

**Deliverables**:
- [ ] All core endpoints implemented
- [ ] Error handling
- [ ] Request validation
- [ ] Response formatting

**Success Criteria**: All endpoints work with Postman/curl

---

### Week 10: Authentication & Security

#### Day 64-66: API Key Authentication 🔴

**Tasks**:
1. Implement API key middleware

   **File**: `src/reifire/api/middleware/auth.py`
   ```python
   """Authentication middleware."""
   from litestar import Request, Response
   from litestar.middleware import DefineMiddleware
   from litestar.exceptions import NotAuthorizedException
   from typing import Optional
   import secrets


   class APIKey:
       """API key model."""

       def __init__(self, key: str, user_id: str, tier: str):
           self.key = key
           self.user_id = user_id
           self.tier = tier


   class APIKeyStore:
       """In-memory API key store (use database in production)."""

       def __init__(self):
           self.keys: Dict[str, APIKey] = {}

       def create_key(self, user_id: str, tier: str = "free") -> str:
           """Create new API key."""
           key = f"reifire_{secrets.token_urlsafe(32)}"
           self.keys[key] = APIKey(key, user_id, tier)
           return key

       def get_key(self, key: str) -> Optional[APIKey]:
           """Get API key."""
           return self.keys.get(key)


   # Global key store (use Redis/DB in production)
   key_store = APIKeyStore()


   async def auth_middleware(request: Request, call_next) -> Response:
       """Verify API key from request header."""
       # Skip auth for health endpoint
       if request.url.path == "/health":
           return await call_next(request)

       # Get API key from header
       api_key = request.headers.get("X-API-Key")
       if not api_key:
           raise NotAuthorizedException("Missing API key")

       # Verify key
       key_obj = key_store.get_key(api_key)
       if not key_obj:
           raise NotAuthorizedException("Invalid API key")

       # Attach to request state
       request.state.api_key = key_obj

       return await call_next(request)


   AuthMiddleware = DefineMiddleware(auth_middleware)
   ```

2. Add user management endpoints
3. Implement tiered access (free/pro/enterprise)

**Deliverables**:
- [ ] API key authentication
- [ ] User management
- [ ] Tiered access
- [ ] Documentation

**Success Criteria**: Protected endpoints require valid API keys

---

#### Day 67-70: Rate Limiting 🔴

**Tasks**:
1. Implement Redis-based rate limiting

   **File**: `src/reifire/api/middleware/rate_limit.py`
   ```python
   """Rate limiting middleware."""
   from litestar import Request, Response
   from litestar.middleware import DefineMiddleware
   from litestar.exceptions import TooManyRequestsException
   import redis
   import time


   class RateLimiter:
       """Redis-based rate limiter."""

       def __init__(self, redis_url: str):
           self.redis = redis.from_url(redis_url)

       def check_rate_limit(self, key: str, max_requests: int, window_seconds: int = 60) -> bool:
           """
           Check if request is within rate limit.

           Returns:
               True if allowed, False if rate limit exceeded
           """
           current_time = int(time.time())
           window_start = current_time - window_seconds

           # Use Redis sorted set for sliding window
           pipe = self.redis.pipeline()

           # Remove old entries
           pipe.zremrangebyscore(key, 0, window_start)

           # Count requests in window
           pipe.zcard(key)

           # Add current request
           pipe.zadd(key, {str(current_time): current_time})

           # Set expiry
           pipe.expire(key, window_seconds)

           results = pipe.execute()
           request_count = results[1]

           return request_count < max_requests


   rate_limiter = None


   async def rate_limit_middleware(request: Request, call_next) -> Response:
       """Apply rate limiting."""
       global rate_limiter

       # Initialize rate limiter
       if rate_limiter is None:
           from ..config import get_settings
           settings = get_settings()
           rate_limiter = RateLimiter(settings.redis_url)

       # Skip for health endpoint
       if request.url.path == "/health":
           return await call_next(request)

       # Get user ID from API key
       api_key = getattr(request.state, "api_key", None)
       if not api_key:
           # Auth middleware should have caught this
           return await call_next(request)

       # Determine rate limit based on tier
       limits = {
           "free": 10,        # 10 req/min
           "pro": 60,         # 60 req/min
           "enterprise": 300  # 300 req/min
       }
       max_requests = limits.get(api_key.tier, 10)

       # Check rate limit
       rate_key = f"rate_limit:{api_key.user_id}"
       if not rate_limiter.check_rate_limit(rate_key, max_requests):
           raise TooManyRequestsException(
               detail=f"Rate limit exceeded. Max {max_requests} requests per minute for {api_key.tier} tier."
           )

       response = await call_next(request)

       # Add rate limit headers
       # ... (add X-RateLimit-* headers)

       return response


   RateLimitMiddleware = DefineMiddleware(rate_limit_middleware)
   ```

2. Add rate limit headers
3. Implement per-tier limits

**Deliverables**:
- [ ] Rate limiting system
- [ ] Per-tier limits
- [ ] Rate limit headers
- [ ] Tests

**Success Criteria**: Rate limits enforced correctly

---

### Week 11: Advanced Features

#### Day 71-73: Webhooks & Callbacks 🔵

**Tasks**:
1. Implement webhook support for long-running operations
2. Add callback URLs to async operations
3. Create webhook signature verification

**Deliverables**:
- [ ] Webhook system
- [ ] Callback support
- [ ] Signature verification

**Success Criteria**: Webhooks deliver results reliably

---

#### Day 74-77: Batch Operations 🔵

**Tasks**:
1. Add batch reification endpoint
2. Implement job queue (Celery/Redis)
3. Add status tracking for batch jobs

**Example**:
```python
@post("/reify/batch")
async def reify_batch_endpoint(
    data: BatchReifyRequest
) -> BatchReifyResponse:
    """
    Submit batch reification job.

    Returns job ID for status tracking.
    """
    job_id = await create_batch_job(data.prompts)
    return BatchReifyResponse(job_id=job_id, status="queued")


@get("/reify/batch/{job_id}")
async def get_batch_status(job_id: str) -> BatchStatusResponse:
    """Get batch job status."""
    status = await get_job_status(job_id)
    return BatchStatusResponse(**status)
```

**Deliverables**:
- [ ] Batch endpoints
- [ ] Job queue system
- [ ] Status tracking

**Success Criteria**: Can process 100+ prompts in batch

---

### Week 12: Deployment

#### Day 78-80: Docker & Deployment 🔴

**Tasks**:
1. Create Dockerfile

   **File**: `Dockerfile`
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gcc \
       && rm -rf /var/lib/apt/lists/*

   # Install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application
   COPY . .
   RUN pip install -e ".[web]"

   # Run migrations, setup, etc.
   RUN python -m reifire.api.setup

   # Expose port
   EXPOSE 8000

   # Run with Uvicorn
   CMD ["uvicorn", "reifire.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. Create docker-compose.yml

   **File**: `docker-compose.yml`
   ```yaml
   version: '3.8'

   services:
     api:
       build: .
       ports:
         - "8000:8000"
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
         - REDIS_URL=redis://redis:6379
       depends_on:
         - redis
       restart: unless-stopped

     redis:
       image: redis:7-alpine
       ports:
         - "6379:6379"
       volumes:
         - redis_data:/data
       restart: unless-stopped

     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
         - ./ssl:/etc/nginx/ssl
       depends_on:
         - api
       restart: unless-stopped

   volumes:
     redis_data:
   ```

3. Set up CI/CD pipeline

   **File**: `.github/workflows/deploy.yml`
   ```yaml
   name: Deploy

   on:
     push:
       branches: [main]

   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3

         - name: Build Docker image
           run: docker build -t reifire-api:latest .

         - name: Push to registry
           run: |
             docker tag reifire-api:latest registry.example.com/reifire-api:latest
             docker push registry.example.com/reifire-api:latest

         - name: Deploy to production
           run: |
             # Deploy to cloud provider
             # ... deployment commands
   ```

**Deliverables**:
- [ ] Dockerfile
- [ ] docker-compose.yml
- [ ] CI/CD pipeline
- [ ] Deployment documentation

**Success Criteria**: One-command deployment

---

#### Day 81-84: Monitoring & Logging 🟡

**Tasks**:
1. Set up structured logging
2. Add Prometheus metrics
3. Set up error tracking (Sentry)
4. Create monitoring dashboard

**Example logging**:
```python
import structlog

logger = structlog.get_logger()

@post("/reify")
async def reify_endpoint(data: ReifyRequest) -> ReifyResponse:
    logger.info(
        "reification_request",
        prompt_length=len(data.prompt),
        llm_provider=data.llm_provider,
        user_id=request.state.api_key.user_id
    )

    # ... process

    logger.info(
        "reification_complete",
        processing_time_ms=processing_time,
        cost_usd=cost,
        cached=cached
    )
```

**Deliverables**:
- [ ] Structured logging
- [ ] Metrics collection
- [ ] Error tracking
- [ ] Monitoring dashboard

**Success Criteria**: Full observability in production

---

## Phase 4: Polish & Launch (Weeks 13-16)

**Goal**: Documentation, examples, marketing, and launch

### Week 13: Documentation

#### Day 85-87: API Documentation 🟡

**Tasks**:
1. Set up Sphinx documentation
2. Auto-generate API reference
3. Create OpenAPI/Swagger docs for web API
4. Write usage guides

**Deliverables**:
- [ ] Complete API documentation
- [ ] Swagger UI for web API
- [ ] Usage guides
- [ ] FAQ

**Success Criteria**: All public APIs documented

---

#### Day 88-91: Tutorials & Examples 🟡

**Tasks**:
1. Create tutorial series
   - Getting started
   - Visual content reification
   - Code generation
   - Building applications with reifire
   - Web API integration

2. Create example gallery
   - Interactive web gallery
   - 20+ examples across all domains
   - Live demo

3. Video tutorials
   - Introduction to reifire
   - Building a reification app
   - API integration guide

**Deliverables**:
- [ ] 5+ written tutorials
- [ ] Interactive example gallery
- [ ] 3+ video tutorials
- [ ] Example GitHub repository

**Success Criteria**: New users can get started in <10 minutes

---

### Week 14: Testing & Quality

#### Day 92-94: Comprehensive Testing 🔴

**Tasks**:
1. Achieve >80% test coverage
2. Add integration tests
3. Add end-to-end tests
4. Performance benchmarks
5. Load testing for API

**Deliverables**:
- [ ] Complete test suite
- [ ] >80% coverage
- [ ] Performance benchmarks
- [ ] Load test results

**Success Criteria**: All tests passing, coverage >80%

---

#### Day 95-98: User Testing 🟡

**Tasks**:
1. Beta testing program
2. Collect user feedback
3. Fix reported issues
4. Iterate on UX

**Deliverables**:
- [ ] Beta program
- [ ] User feedback
- [ ] Bug fixes
- [ ] UX improvements

**Success Criteria**: >4/5 user satisfaction

---

### Week 15: Pre-Launch

#### Day 99-101: PyPI Publication 🔴

**Tasks**:
1. Prepare package for PyPI
2. Create release notes
3. Publish to PyPI
4. Test installation from PyPI

**Deliverables**:
- [ ] Published to PyPI
- [ ] Installation guide
- [ ] Release notes
- [ ] Version 1.0.0

**Success Criteria**: `pip install reifire` works

---

#### Day 102-105: Marketing Materials 🟡

**Tasks**:
1. Create landing page
2. Write blog post announcement
3. Create demo videos
4. Prepare social media content
5. Draft press release

**Deliverables**:
- [ ] Landing page
- [ ] Blog post
- [ ] Demo videos
- [ ] Social media content

**Success Criteria**: Professional marketing presence

---

### Week 16: Launch

#### Day 106-108: Soft Launch 🔴

**Tasks**:
1. Deploy web API to production
2. Announce on Twitter, HN, Reddit
3. Share with beta users
4. Monitor feedback and issues

**Deliverables**:
- [ ] Production deployment
- [ ] Public announcement
- [ ] Community engagement

**Success Criteria**: No critical issues in first 48 hours

---

#### Day 109-112: Post-Launch 🟡

**Tasks**:
1. Monitor metrics and feedback
2. Fix critical issues immediately
3. Engage with community
4. Plan next features based on feedback

**Deliverables**:
- [ ] Issue resolutions
- [ ] Community engagement
- [ ] Roadmap update

**Success Criteria**: Healthy growth, positive feedback

---

## Implementation Details

### Project Structure

```
reifire/
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
├── docs/
│   ├── conf.py
│   ├── index.md
│   ├── api/
│   ├── tutorials/
│   └── examples/
├── examples/
│   ├── basic_reification.py
│   ├── visual_examples.py
│   ├── code_generation.py
│   ├── web_api_client.py
│   └── notebooks/
│       └── getting_started.ipynb
├── src/
│   └── reifire/
│       ├── __init__.py
│       ├── reify.py
│       ├── async_reify.py
│       ├── articulation.py
│       ├── icon_registry.py
│       ├── cost_tracking.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── config.py
│       │   ├── models/
│       │   │   ├── requests.py
│       │   │   └── responses.py
│       │   ├── routes/
│       │   │   ├── reification.py
│       │   │   ├── articulation.py
│       │   │   ├── visualization.py
│       │   │   ├── health.py
│       │   │   └── webhooks.py
│       │   └── middleware/
│       │       ├── auth.py
│       │       ├── rate_limit.py
│       │       └── cost_tracking.py
│       ├── backends/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── openai_backend.py
│       │   ├── anthropic_backend.py
│       │   └── factory.py
│       ├── parsing/
│       │   ├── __init__.py
│       │   ├── classifier.py
│       │   ├── prompt_templates.py
│       │   ├── llm_parser.py
│       │   ├── cache.py
│       │   └── alternatives.py
│       ├── schema/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── validators.py
│       │   └── export.py
│       ├── validation/
│       │   ├── __init__.py
│       │   └── roundtrip.py
│       └── visualization/
│           ├── __init__.py
│           ├── emoji_provider.py
│           ├── icon_manager.py
│           ├── ... (existing files)
├── tests/
│   ├── conftest.py
│   ├── reifire/
│   │   ├── test_reify.py
│   │   ├── test_articulation.py
│   │   ├── parsing/
│   │   │   ├── test_classifier.py
│   │   │   ├── test_llm_parser.py
│   │   │   └── test_templates.py
│   │   ├── backends/
│   │   │   ├── test_openai.py
│   │   │   └── test_anthropic.py
│   │   ├── api/
│   │   │   ├── test_reification.py
│   │   │   ├── test_auth.py
│   │   │   └── test_rate_limit.py
│   │   └── validation/
│   │       └── test_roundtrip.py
├── scripts/
│   ├── setup_dev.sh
│   ├── run_tests.sh
│   └── deploy.sh
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── DATASPEC.md
├── VISUALIZATION_SPEC.md
├── ROADMAP.md
├── RECOMMENDATIONS.md
└── PROJECT_PLAN.md (this file)
```

---

## Testing Strategy

### Unit Tests
- Individual functions and classes
- Mocked external dependencies
- Fast execution (<1s per test)
- Target: >80% coverage

### Integration Tests
- Multiple components together
- Real LLM calls (cached responses)
- Moderate speed (~5s per test)
- Target: All major workflows covered

### End-to-End Tests
- Complete user workflows
- Real API calls (rate limited)
- Slow execution (~30s per test)
- Target: Critical paths covered

### Performance Tests
- Response time benchmarks
- Memory usage profiling
- Concurrent request handling
- Target: <2s for simple prompts

### Load Tests
- API stress testing
- Concurrent user simulation
- Resource usage monitoring
- Target: 100 concurrent users

---

## Deployment Strategy

### Development
- Local development with Docker Compose
- Hot reload for fast iteration
- Local Redis for caching
- Environment variables from .env

### Staging
- Identical to production setup
- Separate LLM API keys (dev accounts)
- Test data
- Used for final testing before release

### Production
- Docker containers
- Cloud deployment (AWS/GCP/Azure)
- Load balancer
- Auto-scaling
- Redis cluster
- Monitoring (Prometheus + Grafana)
- Error tracking (Sentry)
- Log aggregation (ELK stack)

---

## Success Criteria

### Technical Metrics
- ✅ All tests passing
- ✅ >80% code coverage
- ✅ <2s API response time (p95)
- ✅ >99% API uptime
- ✅ <$0.05 cost per reification
- ✅ >90% round-trip accuracy

### User Metrics
- ✅ 1,000 PyPI downloads/month (6 months)
- ✅ 500 GitHub stars (1 year)
- ✅ 100 web API users (6 months)
- ✅ 5+ active contributors
- ✅ >4/5 user satisfaction

### Business Metrics
- ✅ Self-sustaining (API revenue > costs)
- ✅ Positive community feedback
- ✅ Featured in AI/dev newsletters
- ✅ Used in production by 10+ companies

---

## Risk Mitigation

### Technical Risks
1. **LLM output inconsistency**
   - Mitigation: Extensive validation, multiple retries, fallback models
   - Monitoring: Track validation failure rate
   - Escalation: Switch to more reliable model if >10% failures

2. **API cost explosion**
   - Mitigation: Aggressive caching, rate limiting, cost caps
   - Monitoring: Real-time cost tracking per user
   - Escalation: Automatic throttling if budget exceeded

3. **Performance issues**
   - Mitigation: Async processing, caching, CDN
   - Monitoring: Response time metrics
   - Escalation: Auto-scaling if response time >5s

4. **Security vulnerabilities**
   - Mitigation: Regular security audits, dependency updates
   - Monitoring: Automated vulnerability scanning
   - Escalation: Immediate patching for critical CVEs

### Product Risks
1. **Low adoption**
   - Mitigation: Strong marketing, clear value prop, free tier
   - Monitoring: User signup rate, engagement metrics
   - Escalation: Pivot features based on feedback

2. **Competition**
   - Mitigation: Unique features (bidirectional, visual-first)
   - Monitoring: Competitor analysis
   - Escalation: Accelerate unique feature development

3. **Maintenance burden**
   - Mitigation: Good tests, documentation, automation
   - Monitoring: Issue resolution time
   - Escalation: Community involvement, hire help

---

## Resource Requirements

### Development
- **Personnel**: 1 full-time developer (or equivalent)
- **Time**: 16 weeks (4 months)
- **Skills**: Python, LLMs, web APIs, testing, DevOps

### Infrastructure
- **Development**: Local machine + Docker
- **Testing**: GitHub Actions (free)
- **Production**:
  - Web API hosting: ~$50-100/month
  - Redis: ~$20-40/month
  - Monitoring: ~$0-30/month
  - Total: ~$70-170/month

### API Costs
- **Development/Testing**: ~$100-200/month
- **Production**: Variable based on usage
  - Free tier: Minimal (<$50/month)
  - Growing usage: $200-500/month
  - At scale: Revenue should cover costs

### Total Budget
- **Phase 1 (4 weeks)**: ~$200-300
- **Phase 2 (4 weeks)**: ~$200-300
- **Phase 3 (4 weeks)**: ~$300-400
- **Phase 4 (4 weeks)**: ~$200-300
- **Total (16 weeks)**: ~$900-1,300

---

## Next Steps

### Immediate (This Week)
1. ✅ Fix test suite
2. ✅ Update README
3. ✅ Modernize package configuration
4. Start Week 2 tasks (Pydantic schemas)

### Short Term (Next 4 Weeks)
1. Complete Phase 1 (Foundation)
2. Get basic reify() working
3. Create end-to-end example
4. Prepare for PyPI

### Medium Term (2-3 Months)
1. Complete Phase 2 (Core Reification)
2. Complete Phase 3 (Web API)
3. Beta testing program

### Long Term (3-4 Months)
1. Complete Phase 4 (Polish & Launch)
2. Public launch
3. Community building
4. Feature expansion based on feedback

---

## Conclusion

This plan provides a comprehensive roadmap to transform reifire from a pre-alpha project with missing core functionality into a production-ready, commercially viable reification library with a robust web API.

**Key Milestones**:
- Week 4: Basic reification working
- Week 8: Full reification with all domains
- Week 12: Production web API
- Week 16: Public launch

**Success depends on**:
- Consistent execution of weekly goals
- Responsive iteration based on testing
- Community engagement and feedback
- Quality over speed

With focused effort over 16 weeks, reifire can become the premier tool for prompt reification and manipulation.
