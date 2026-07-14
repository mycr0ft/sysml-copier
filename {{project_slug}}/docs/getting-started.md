# Getting Started

## Prerequisites

- **Python 3.10+**
- **Hatch** — Python project manager (`pip install hatch`)
- **VS Code** (recommended) with the [SysIDE CE](https://github.com/sensmetry/sysml-2ls) extension

## Setup

```bash
hatch install
pre-commit install
```

This creates a virtual environment with all tools: sysmlpy, sysml-style, mkdocs-material, pygments-sysml, Jupyter, pytest, and pre-commit.

## Writing SysML models

Models live in `sysml/models/` using SysML v2 textual notation. An example model is provided:

```sysml
package MyModel {
    public import SI::*;

    port def PowerPort;

    part def Lens {
        attribute focalLength : Real = 35 [mm];
    }

    part def Sensor {
        attribute pixelCount : Integer = 24000000;
        port powerPort : PowerPort;
    }

    part def Camera {
        attribute mass : Real = 500 [g];
        part lens : Lens;
        part sensor : Sensor;
        port powerPort : PowerPort;

        connection powerConnection from powerPort to sensor.powerPort;
    }

    requirement def CameraRequirement {
        doc /* The camera shall meet performance requirements. */
        constraint massConstraint { mass <= 600 [g] }
    }

    action def TakePicture {
        in exposureSetting : Real;
        action focus : Focus;
        action expose : Expose;
        action capture : Capture;
        flow focus.focusedDistance to expose.focusDistance;
    }
}
```

## Linting and formatting

Check models for style issues (SML1xx–SML4xx rules):

```bash
hatch run check
```

Auto-format:

```bash
hatch run format
```

Check formatting without writing (CI gate):

```bash
hatch run format-check
```

## Semantic analysis

Validate undefined symbols, unresolved imports, cyclic specialization, and other well-formedness rules:

```bash
hatch run analyze
```

## Visualization

Generate PlantUML diagrams:

```bash
hatch run render
```

Diagrams are written to `output/`. Render with `plantuml output/*.puml` or the VS Code PlantUML extension.

## Documentation

Serve the MkDocs documentation site locally:

```bash
hatch run serve
```

This starts a live-reload server at `http://127.0.0.1:8000`. SysML code blocks in the docs are syntax-highlighted via [pygments-sysml](https://github.com/mycr0ft/pygments-sysml).

Build the docs to `site/`:

```bash
hatch run docs
```

## Tests

```bash
hatch run test
```

Tests verify the example model parses and passes semantic analysis.
