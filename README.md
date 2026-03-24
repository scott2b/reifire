# reifire 🔥

Reify your natural language prompts

**⚠️ Current Status: Alpha / Experimental**

Currently available:
- ✅ `reify()` - Convert natural language prompts to reified data (Basic NLP + pluggable icon providers)
- ✅ `articulate()` - Convert reified data structures back to natural language
- ✅ `articulate_alternatives()` - Generate prompt variants
- ✅ Visualization system - Interactive HTML visualizations
- ✅ Bundled icons - 400+ curated Lucide & Octicons SVGs, zero-config
- ✅ Pluggable icon providers - Material Icons, Noun Project, LLM-generated SVGs

## Quickstart

### Install Reifire

```bash
# From source (development)
git clone https://github.com/scott2b/reifire.git
cd reifire
pip install -e .
```

### Reify a prompt

Icons are resolved automatically from the bundled icon set — no API keys needed:

```python
from reifire import reify

result = reify("a cat sitting on a table")
# Result includes extracted keywords with matched icons:
# - "cat" -> bundled Lucide cat icon
# - "table" -> bundled Lucide table icon
# - "sit" -> searched across available providers
```

### Articulate a reified data structure

Convert pre-existing reified data structures back to natural language:

```python
>>> from reifire import articulate
>>> reified = {
...     "object": {"name": "baby Cthulhu", "modifiers": []},
...     "type": {"name": "illustration", "category": "visual"},
...     "artifact": {
...         "type": "illustration",
...         "attributes": [
...             {"name": "style", "value": "children's illustration"},
...             {"name": "color scheme", "value": "brown-green-purple"}
...         ]
...     }
... }
>>> articulate(reified)
'Create a baby Cthulhu illustration in children\'s illustration style with a brown-green-purple color scheme.'
```

### Browse bundled icons

```bash
python examples/provider_demo.py
```

Opens a grid of bundled SVG icons in your browser.

See `examples/` directory for more examples.

## Project description

Reifire is a library / toolkit that empowers the reification of natural language prompts
into visual objects. The project was inspired by page 28 of the _Microsoft New Future of Work Report 2024_
which can be found [here](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/NFWReport2024_12.20.24.pdf)

The relevant content of that report follows:

> Initial evidence on post-chat interaction techniques suggests that they could help solve prompt engineering hurdles
> The principle of reification in human-computer interaction turns abstract commands into persistent reusable interface objects, which affords several benefits to users (Beaudoin-Lafon 2000). We can apply this principle to user prompts (or fragments of prompts), embodying them into interactive graphical objects persistent on screen for users to store and reuse multiple times, as well as alter and combine at will. Riche et al. (2024) call this next generation of widgets: "AI-instruments".
>
> An initial qualitative study with 12 users shows a few advantages of AI instruments over more linear typing-based interactions:
>   • Generating interactive objects surfacing different dimensions (or
aspects of a prompt) eliminates the need for users to articulate them in
their own words.
>   - Simple interactions with objects to add/remove dimensions or suggest
different dimensions facilitates exploration and iterative content
generation.
>   - Persistent objects on screen can be stored, combined and most importantly reused with minimal effort.
>
> References:
>   - Beaudouin-Lafon, M., (2000). Instrumental interaction: an interaction model for designing post-WIMP user interfaces. CHI 2024
>   - Riche, N. et al., (2024). AI-instruments: Embodying Prompts as Instruments to Abstract & Reflect Graphical Interface Commands as General-Purpose Tools (Preprint).
>
> <img src="https://github.com/scott2b/reifire/blob/main/reification.aka.ms.nfw.2024.png?raw=true" alt="Reification" width=500>
>
> Source: [Microsoft New Future of Work Report 2024](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/NFWReport2024_12.20.24.pdf). p. 28

The goal of the Reifire project is to give developers resources for easily integrating
reification of natural language prompts into their projects.


## Reification process

Reifire parses natural language prompts into structured components and enriches them with visualizations.
The current implementation uses **Spacy** for Natural Language Processing (NLP) to extract key concepts (nouns, verbs, adjectives) and a **pluggable icon provider system** to find relevant icons.

### Basic Usage

```python
from reifire import reify

# Reify a simple prompt — bundled icons work out of the box
reification = reify("raining cats and dogs")

# Result includes:
# - Primary object: "raining cats and dogs"
# - Attributes: "rain", "cat", "dog" (extracted keywords)
# - Visualizations: Icons for each attribute from bundled set
```

Currently, the reverse process (articulation) is also fully implemented - see examples above.

## Icon Providers

Reifire uses a pluggable provider system for icon resolution. Providers are tried in
priority order until one returns a match.

### Bundled Icons (default, zero-config)

Ships with 400+ curated SVGs from [Lucide](https://lucide.dev/) and
[GitHub Octicons](https://primer.style/foundations/icons). Always available, no setup needed.

### Material Design Icons (optional)

Set `MATERIAL_DESIGN_ICONS_DIR` to a local clone of Google's
[material-design-icons](https://github.com/google/material-design-icons) repo:

```bash
export MATERIAL_DESIGN_ICONS_DIR=/path/to/material-design-icons
```

### Noun Project (optional)

```bash
pip install reifire[nounproject]
export NOUNPROJECT_API_KEY=your_api_key
export NOUNPROJECT_API_SECRET=your_secret
```

### LLM-Generated SVGs (optional, experimental)

Generate icons on demand using any LLM via [Pydantic AI](https://ai.pydantic.dev/):

```bash
pip install reifire[llm]
```

```python
from reifire.visualization.providers.llm_svg import LLMSVGProvider
from reifire.visualization.providers import ProviderChain

llm_provider = LLMSVGProvider(model="anthropic:claude-haiku-4-5-20251001")
chain = ProviderChain([llm_provider])
```

### Custom Provider Chains

```python
from reifire.visualization.providers import ProviderChain
from reifire.visualization.providers.bundled import BundledIconProvider
from reifire.visualization.providers.nounproject import NounProjectProviderAdapter

chain = ProviderChain([
    BundledIconProvider(),                              # priority 10
    NounProjectProviderAdapter(api_key="...", api_secret="..."),  # priority 50
])

# Use with reify
from reifire import reify
result = reify("a sunset over mountains", provider_chain=chain)
```

## Reification data structure

For a complete specification of the reification data structure, see DATASPEC.md

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git

### Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/scott2b/reifire.git
   cd reifire
   ```

2. Run the development setup script:
   ```bash
   chmod +x scripts/setup_dev.sh
   ./scripts/setup_dev.sh
   ```

   This will:
   - Create a virtual environment
   - Install development dependencies
   - Set up pre-commit hooks

### Running Tests

Run all tests with hatch (all Python versions and checks):
```bash
hatch test
```

Run specific test environments:
```bash
hatch run test             # Run tests in default environment
hatch run lint:check       # Run linting
hatch run typecheck:check  # Run type checking
hatch run integration:test # Run integration tests
```

Run tests with coverage:
```bash
hatch run test-cov        # Run tests with coverage report
```

Run pytest directly (faster for development):
```bash
pytest tests/
```

### Code Quality

The project uses several tools to maintain code quality:

- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Style guide enforcement
- **mypy**: Static type checking

These are run automatically on commit via pre-commit hooks, but you can run them manually:

```bash
black src tests
isort src tests
flake8 src tests
mypy src tests
```

### Documentation

The project documentation is built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

To serve the documentation locally:
```bash
mkdocs serve
```

To build the documentation:
```bash
mkdocs build
```

### Project Structure

```
reifire/
├── examples/           # Example scripts and JSON files
├── src/               # Source code
│   └── reifire/       # Main package
│       └── visualization/
│           └── providers/  # Icon provider system
│               └── icons/  # Bundled SVG icons
├── tests/             # Test suite
│   └── reifire/       # Package tests
├── scripts/           # Development scripts
├── .pre-commit-config.yaml  # Pre-commit hook configuration
└── pyproject.toml     # Project metadata, build config, and tool configurations
```
