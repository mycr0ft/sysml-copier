# Developing this project

This guide covers setting up and using the SysML v2 development environment.

## Prerequisites

- **Python 3.10+** (for sysmlpy and sysml-style)
- **Hatch** — Python project manager (`pip install hatch`)
- **Graphviz** (optional) — for rendering PlantUML diagrams to images
- **PlantUML** (optional) — for rendering `.puml` files to diagrams
- **VS Code** — recommended editor

No Java or Miniconda is required. This template uses pure-Python tooling.

## First time setup

### Install dependencies

From the project root:

```bash
hatch install
```

This creates a virtual environment with:
- **sysmlpy** — SysML v2 parser, navigator, semantic analyzer, and PlantUML renderer
- **sysml-style** — SysML v2 linter and auto-formatter
- **mkdocs-material** — documentation site generator with Material theme
- **pygments-sysml** — SysML v2 syntax highlighting for MkDocs code blocks
- **Jupyter** — for notebook-based model exploration
- **pytest** — for running tests
- **pre-commit** — for git hooks

### Install pre-commit hooks

```bash
pre-commit install
```

This sets up automatic linting and formatting of `.sysml` files on every commit.

### VS Code: SysIDE CE extension

Find and install the [SysIDE CE extension](https://github.com/sensmetry/sysml-2ls) within VS Code.

When prompted, direct the extension to the SysML standard library at `./sysml/sysml.library`. Set this as a **Workspace** setting (not User), so different projects can use different library versions.

The `.vscode/settings.json` file in this project already configures this path for you.

### VS Code: Jupyter extension

Install the `Jupyter` extension for VS Code to work with notebooks.

## Workflow

### Editing SysML models

Write your SysML v2 models in `sysml/models/` using the textual notation. The example `mymodel.sysml` shows parts, ports, connections, requirements, and actions.

### Linting

Check your models for style issues:

```bash
hatch run check
```

This runs `sysml-style check`, which reports 14 style rules (SML1xx–SML4xx) with file:line:col locations.

### Formatting

Auto-format your models:

```bash
hatch run format
```

Or check if formatting would change anything (for CI):

```bash
hatch run format-check
```

### Semantic analysis

Run semantic validation to detect undefined symbols, unresolved imports, and naming issues:

```bash
hatch run analyze
```

This loads all `.sysml` files in `sysml/models/` and runs the sysmlpy semantic analyzer.

### Visualization

Generate PlantUML diagrams from your model:

```bash
hatch run render
```

This writes `.puml` files to `output/`. Render them to images with:

```bash
plantuml output/*.puml
```

Or use the PlantUML VS Code extension to preview them directly.

### Jupyter notebooks

Open the example notebook:

```bash
hatch run jupyter lab notebooks/model_exploration.ipynb
```

The notebook demonstrates loading a model, interactive tree views, semantic analysis, navigation, and PlantUML diagram generation.

### Running tests

```bash
hatch run test
```

This runs `pytest`, which includes tests that verify your model parses and passes semantic analysis.

### Documentation

Serve the MkDocs documentation site with live reload:

```bash
hatch run serve
```

This starts a local server at `http://127.0.0.1:8000`. The docs use [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) with [pygments-sysml](https://github.com/mycr0ft/pygments-sysml) for SysML v2 syntax highlighting in code blocks.

Build the docs to `site/`:

```bash
hatch run docs
```

Edit documentation pages in `docs/` and configure the site in `mkdocs.yml`. Use ` ```sysml ` fenced code blocks for syntax-highlighted SysML examples.

## Project structure

```bash
{{ project_slug }}/
├── .editorconfig                   # Editor indentation settings
├── .github/workflows/ci.yml        # CI: lint, format check, analyze, test, docs
├── .pre-commit-config.yaml         # Pre-commit hooks for .sysml and .py files
├── .vscode/                        # VS Code settings and extension recommendations
├── docs/                           # MkDocs documentation pages
│   ├── index.md                    # Home page
│   ├── getting-started.md          # Quick start guide
│   └── developing.md               # This file
├── mkdocs.yml                      # MkDocs configuration (theme, nav, extensions)
├── notebooks/                      # Jupyter notebooks for model exploration
│   └── model_exploration.ipynb
├── pyproject.toml                  # Project config (deps, sysml-style config, scripts)
├── src/
│   └── {{ project_slug }}/
│       ├── __about__.py
│       ├── __init__.py
│       └── examples/               # Example automation scripts
│           ├── analyze_model.py    # Semantic analysis
│           ├── render_diagrams.py  # PlantUML generation
│           └── navigate_model.py   # Model navigation/querying
├── sysml/
│   ├── models/                     # Your SysML v2 models go here
│   │   └── mymodel.sysml           # Example model
│   └── sysml.library/              # SysML v2 standard library (for SysIDE)
└── tests/
    ├── __init__.py
    └── test_model.py               # Tests for the example model
```

## Configuration

### sysml-style

Style rules are configured in `pyproject.toml` under `[tool.sysml-style]`:

```toml
[tool.sysml-style]
max_line_length = 120
indent_size = 4
ignore = []                          # Rule codes to suppress, e.g. ["SML401"]
naming_convention = "{{ sysml_naming_convention }}"
```

Available rules:
- **SML1xx** — Whitespace (spacing, trailing whitespace, indentation, blank lines)
- **SML2xx** — Naming (UpperCamelCase definitions, lowerCamelCase usages, Port suffix)
- **SML3xx** — Structure (import ordering, empty blocks, filename-package match)
- **SML4xx** — Idioms (doc comment placement, `doc` keyword usage)

Run `sysml-style check --help` for full details.

## Updating your project

This project was generated with [Copier](https://copier.science). To check for template updates and apply them:

```bash
copier update
```

Copier records the template version and your answers in `.copier-answers.yml`, then re-applies only the diffs from the template while preserving your customizations.
