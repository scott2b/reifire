# reifire 🔥

Reify your natural language prompts

**⚠️ Current Status: Alpha / Experimental**
 
Currently available:
- ✅ `reify()` - Convert natural language prompts to reified data (Basic NLP + Noun Project)
- ✅ `articulate()` - Convert reified data structures back to natural language
- ✅ `articulate_alternatives()` - Generate prompt variants
- ✅ Visualization system - Interactive HTML visualizations
- ✅ Icon integration - Noun Project, Material Icons, Octicons

## Quickstart

### Install Reifire

```bash
# From source (development)
git clone https://github.com/scott2b/reifire.git
cd reifire
pip install -e .
```

### Articulate a reified data structure

Currently, you can convert pre-existing reified data structures back to natural language:

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
'Create a baby Cthulhu illustration in children's illustration style with a brown-green-purple color scheme.'
```

See `examples/` directory for complete reified data structure examples.

## Project description

Reifire is a library / toolkit that empowers the reification of natural language prompts
into visual objects. The project was inspired by page 28 of the _Microsoft New Future of Work Report 2024_
which can be found [here](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/NFWReport2024_12.20.24.pdf)

The relevant content of that report follows:

> Initial evidence on post-chat interaction techniques suggests that they could help solve prompt engineering hurdles
> The principle of reification in human-computer interaction turns abstract commands into persistent reusable interface objects, which affords several benefits to users (Beaudoin-Lafon 2000). We can apply this principle to user prompts (or fragments of prompts), embodying them into interactive graphical objects persistent on screen for users to store and reuse multiple times, as well as alter and combine at will. Riche et al. (2024) call this next generation of widgets: “AI-instruments”.
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
The current implementation uses **Spacy** for Natural Language Processing (NLP) to extract key concepts (nouns, verbs, adjectives) and the **Noun Project API** to find relevant icons.
 
### Basic Usage
 
```python
from reifire import reify
 
# Reify a simple prompt
reification = reify("raining cats and dogs")
 
# Result includes:
# - Primary object: "raining cats and dogs"
# - Attributes: "rain", "cat", "dog" (extracted keywords)
# - Visualizations: Icons for each attribute from Noun Project
```
 
Currently, the reverse process (articulation) is also fully implemented - see examples above.

## Visualizations

Reifire can create visualization components for reified data structures.
Currently the following icon sources are supported:

  - [the Noun Project API](https://api.thenounproject.com/)
  - Material Design Icons (local)
  - Octicons (fallback)

The visualization system generates interactive HTML representations of reified structures.
See `examples/*.html` for examples of generated visualizations.

            "image": "bc.png"
        }
    },
    "type": {
        "name": "illustration",
        "visualization": {
            "source": "nounproject",
            "name": "illustration",
            "image": "illustration",
            "attribution": "somecreator",
        }
    },
    "attributes": [
        {
            "name": "color scheme",
            "visualization": {
                "source": "colors",
                "name": "brown-green-purple",
                "images": [
                    "brown.svg",
                    "green.svg",
                    "purple.svg",
                ],
            }
        }
    ]
}
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

### Project Structure

```
reifire/
├── examples/           # Example JSON files
├── src/               # Source code
│   └── reifire/       # Main package
├── tests/             # Test suite
│   └── reifire/       # Package tests
├── scripts/           # Development scripts
├── .pre-commit-config.yaml  # Pre-commit hook configuration
└── pyproject.toml     # Project metadata, build config, and tool configurations
```

## Icons

If avaiable, Material Icons are first checked for a suitable icon. Get the latest icons with the download instructions at https://developers.google.com/fonts/docs/material_icons/

Unzip the icons and set the environment variable `MATERIAL_ICONS_DIR` to the path of the unzipped icons.

The Noun Project API is used as a fallback. Set the following environment variables to use it:

```
NOUNPROJECT_API_KEY=your_api_key
NOUNPROJECT_API_SECRET=your_secret
```
