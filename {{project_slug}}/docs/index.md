# {{ project_name }}

{{ project_short_description }}

## What's included

- [sysmlpy](https://github.com/mycr0ft/sysmlpy) — SysML v2 parser, semantic analyzer, and PlantUML renderer
- [sysml-style](https://github.com/mycr0ft/sysml-style) — linter and auto-formatter for `.sysml` files
- [pygments-sysml](https://github.com/mycr0ft/pygments-sysml) — SysML v2 syntax highlighting for docs
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) — project documentation site
- [Hatch](https://hatch.pypa.io) — Python project management
- Pre-commit hooks for automatic linting
- GitHub Actions CI pipeline

## Quick start

```bash
hatch install
pre-commit install
hatch run check       # lint SysML models
hatch run analyze     # semantic validation
hatch run test        # run tests
hatch run serve       # docs site at http://127.0.0.1:8000
```

## Example model

The project includes an example SysML v2 model in `sysml/models/mymodel.sysml`:

```sysml
package MyModel {
    public import SI::*;

    port def PowerPort;
    port def ImagePort;

    part def Lens {
        attribute focalLength : Real = 35 [mm];
    }

    part def Camera {
        attribute mass : Real = 500 [g];
        part lens : Lens;
        port powerPort : PowerPort;
    }
}
```

## Next steps

- [Getting Started](getting-started.md) — setup and workflow guide
- [Developing](developing.md) — full development reference
