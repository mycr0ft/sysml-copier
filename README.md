# Copier template for SysML v2 projects

A [Copier](https://copier.science) template that scaffolds a SysML v2 project with:
- [sysmlpy](https://github.com/mycr0ft/sysmlpy) for parsing, semantic analysis, and PlantUML rendering
- [sysml-style](https://github.com/mycr0ft/sysml-style) for linting and formatting
- [Hatch](https://hatch.pypa.io) for project management
- Pre-commit hooks for `.sysml` files
- GitHub Actions CI (lint, format check, analyze, test)
- Jupyter notebook for model exploration
- VS Code settings (SysIDE, PlantUML, Python)
- Bundled SysML v2 standard library for IDE syntax highlighting

## Usage

```bash
pip install copier
copier copy /path/to/sysml-copier /path/to/my-project
```

Answer the prompts (project name, author, license, etc.) and Copier generates a ready-to-use project.

## Updating a generated project

Copier records the template version and your answers in `.copier-answers.yml`. To pull in template improvements:

```bash
cd my-project
copier update
```

Copier re-applies only the diffs while preserving your customizations.

## Prompts

| Prompt | Default | Description |
|--------|---------|-------------|
| `author` | Your Name | Full name for copyright |
| `email` | example@example.com | Email for author metadata |
| `github_username` | example | GitHub username (repo URL) |
| `project_name` | my-project | Human-readable name |
| `project_slug` | derived from `project_name` | Python package name (snake_case) |
| `project_short_description` | A SysML v2 model... | One-line description |
| `repo_url` | derived | Repository URL |
| `license` | MIT | MIT, Apache-2.0, GPL-3.0, or proprietary |
| `sysml_naming_convention` | strict | strict or relaxed naming rules |

## Generated structure

```
my_project/
├── .editorconfig
├── .github/workflows/ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .vscode/
│   ├── extensions.json
│   └── settings.json
├── docs/developing.md
├── notebooks/model_exploration.ipynb
├── pyproject.toml
├── README.md
├── src/my_project/
│   ├── __about__.py
│   ├── __init__.py
│   └── examples/
│       ├── analyze_model.py
│       ├── navigate_model.py
│       └── render_diagrams.py
├── sysml/
│   ├── models/mymodel.sysml
│   └── sysml.library/          # Bundled standard library
└── tests/
    └── test_model.py
```

## Migration from the cookiecutter template

This template is a drop-in replacement for `sysml-cookiecutter`. The generated project is functionally identical. The key difference is update support: `copier update` re-applies template diffs without overwriting your work, while cookiecutter + `cruft update` is more fragile.
