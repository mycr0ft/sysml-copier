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
- `.kpar` packaging — bundle your model into a standard KerML Project Archive and verify any `.kpar`
- `%%sysml` Jupyter cell magic — write SysML v2 directly in notebooks, backed by sysmlpy

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
├── scripts/
│   ├── make_kpar.py            # Bundle sysml/models into a .kpar archive
│   └── verify_kpar.py          # Validate any .kpar (structure, index, checksums)
├── src/my_project/
│   ├── __about__.py
│   ├── __init__.py
│   ├── sysml_magic.py         # %%sysml Jupyter cell magic
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

## SysML in Jupyter: the %%sysml magic

Generated projects include an IPython extension that adds a `%%sysml` cell
magic to the ordinary Python kernel — write SysML v2 textual notation in
notebook cells, backed by [sysmlpy](https://github.com/mycr0ft/sysmlpy).
No JVM, no extra kernel install.

```python
# once per notebook:
%load_ext my_project.sysml_magic
```

```python
%%sysml
package Vehicle {
    part def Engine {
        attribute fuelRate : Real;
    }
    part def Vehicle {
        part engine : Vehicle::Engine;
    }
}
```

The parsed model accumulates across cells into a persistent `model` object
(alias `_sysml`) usable from normal Python cells:

```python
model.find(name='Engine')          # query elements
engine.attributes                  # typed navigation
```

Re-declaring a package merges at member granularity: elements with the same
`name` + `sysml_type` replace prior definitions, everything else is kept —
so you can iterate on one part in a single cell.

Line magics (analogues of the OMG Pilot Implementation kernel commands):

```python
%sysml_reset                  # discard the session model
%sysml_list [NAME]            # list packages, or find elements by exact name
%sysml_show NAME [--json]     # print the AST rooted at a named element
%sysml_viz NAME [--view V]    # PlantUML view (general|tree|package|action|interconnection)
```

Cell options: `%%sysml --reset` (fresh model), `--file PATH` (parse from a
file; use `-` as the cell body), `--show` (print the round-tripped model).

Full command reference — including the complete magic set of the official
OMG Pilot Implementation Jupyter kernel this feature draws from, and a
compatibility table — is in [`docs/sysml-magics.md`]({{ repo_url }}/blob/main/%7B%7Bproject_slug%7D%7D/docs/sysml-magics.md).

## Packaging models as .kpar

Generated projects include a script that bundles `sysml/models/` into a
[`.kpar` file](https://github.com/Systems-Modeling/SysML-v2-Release) — the
standard KerML Project Archive (KerML spec clause 10) used for model
interchange between SysML v2 tools (SysIDE, Sysand, etc.). A `.kpar` is a ZIP
containing `.project.json` (name, version, description, usage), `.meta.json`
(package index + SHA256 checksums), and the model files themselves.

```bash
cd my-project

# Bundle sysml/models/ → dist/<name>-<version>.kpar
python scripts/make_kpar.py

# Explicit overrides (defaults come from pyproject.toml / existing .project.json)
python scripts/make_kpar.py --name my_model --version 1.2.0 \
    --description "My model" -o dist/my_model-1.2.0.kpar

# Verify any .kpar — including OMG standard library archives (e.g. downloaded
# from https://github.com/Systems-Modeling/SysML-v2-Release/releases)
python scripts/verify_kpar.py sysml.library.kpar
```

`make_kpar.py` resolves project name/version from (in order): CLI flags,
an existing `sysml/models/.project.json`, `pyproject.toml`, then the directory
name. If your model directory already contains `.project.json` / `.meta.json`
(as the standard library dirs do), they are preserved — checksums are always
recomputed from the bundled files. Both scripts are stdlib-only (Python ≥3.11
for `tomllib`; 3.10 works when no `pyproject.toml` fallback is needed).

## Migration from the cookiecutter template

This template is a drop-in replacement for `sysml-cookiecutter`. The generated project is functionally identical. The key difference is update support: `copier update` re-applies template diffs without overwriting your work, while cookiecutter + `cruft update` is more fragile.
