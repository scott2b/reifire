# reifire

Reify your natural language prompts

## Quickstart

### Install Reifire

(T.B.D.)

### Reifiy a prompt

```
>>> from reifire import reify
>>> reify("Scary-cute baby Cthulu illustration with brown-green-purple color scheme. Wide outlines, childrens illustration style.")
>>> { "object": {"name": "baby Cthulu"}, "type": {"name": "illustration"} }


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

Reifire parses a natural language prompt into components and converts them into constructs
that can be utilized in a visual computing environment. Usually this will mean presenting
object icons or other visual placeholders to the user for selection, manipulation, etc.
The model for the specific use case in mind is illustrated in the diagram above from the
Microsoft 2024 NFW report.

Reification is as simple as calling reifiy on a natural language prompt:

```
from reifire import reify
reification = reify(prompt)
```

## Visualizations

Reifire can call out to external libraries in order to create visualization components
as artifacts of reification. Currently the following are supported:

  - [the Noun Project API](https://api.thenounproject.com/)
  - Image generation calls to OpenAI
  - color blocks

Multiple visualiazation schemes can be passed to `reify` to support a fallback mechanism
for finding or generating component images.

```
>>> import json
>>> from reifire import reify
>>> from reifire.viz.types import COLORS, NOUNPROJECT, OPENAI
>>> r = reify(prompt, visualization=COLORS|NOUNPROJECT|OPENAI)
>>> print(json.dumps(r, indent=4))
{
    "object": {
        "name": "baby Cthulu",
        "visualization": {
            "source": "openai",
            "name": "baby cthulu",
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

Run all tests with tox (all Python versions and checks):
```bash
tox
```

Run specific test environments:
```bash
tox -e py39        # Run tests on Python 3.9
tox -e lint        # Run linting
tox -e typecheck   # Run type checking
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
├── .coveragerc        # Coverage configuration
├── .pre-commit-config.yaml  # Pre-commit hook configuration
├── pyproject.toml     # Project metadata and build config
├── setup.cfg         # Tool configurations
├── setup.py         # Package setup
└── tox.ini          # Test automation config
```
