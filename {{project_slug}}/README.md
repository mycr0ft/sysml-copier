# {{ project_name }}

> {{ project_short_description }}

## Getting started

This project uses [sysmlpy](https://github.com/mycr0ft/sysmlpy) for SysML v2 model parsing, automation, and visualization, and [sysml-style](https://github.com/mycr0ft/sysml-style) for linting and formatting.

### Prerequisites

- Python 3.10+
- [Hatch](https://hatch.pypa.io) (`pip install hatch`)
- VS Code with the [SysIDE CE](https://github.com/sensmetry/sysml-2ls) extension

### Setup

```bash
hatch install
pre-commit install
```

See [developing.md](./docs/developing.md) for the full development guide.

## Usage

### SysML models

Write your SysML v2 textual notation models in `sysml/models/`. An example model (`mymodel.sysml`) is provided showing parts, ports, connections, requirements, and actions.

### Linting and formatting

```bash
hatch run check          # Lint for style issues
hatch run format         # Auto-format models
hatch run format-check   # Check if formatting is needed (CI gate)
```

### Semantic analysis

```bash
hatch run analyze        # Run semantic validation
```

### Visualization

```bash
hatch run render         # Generate PlantUML diagrams to output/
```

### Jupyter notebooks

```bash
hatch run jupyter lab notebooks/model_exploration.ipynb
```

### Tests

```bash
hatch run test
```

### Documentation

```bash
hatch run serve         # Live docs at http://127.0.0.1:8000
hatch run docs          # Build to site/
```

SysML code blocks in the docs are syntax-highlighted via [pygments-sysml](https://github.com/mycr0ft/pygments-sysml).

## Project structure

| Path | Description |
|------|-------------|
| `sysml/models/` | Your SysML v2 models (textual notation) |
| `sysml/sysml.library/` | SysML v2 standard library (for SysIDE syntax highlighting) |
| `src/{{ project_slug }}/examples/` | Example Python automation scripts |
| `docs/` | MkDocs documentation pages (with SysML syntax highlighting) |
| `mkdocs.yml` | MkDocs configuration (Material theme, nav, extensions) |
| `notebooks/` | Jupyter notebooks for model exploration |
| `tests/` | Tests (verifies model parses and passes analysis) |

## License

{{ license }} — see [LICENSE](./LICENSE).


## Contributing

Contributions are welcome! Please open an issue or PR.
