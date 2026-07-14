"""Generate PlantUML diagrams from the SysML models in sysml/models/."""

import sys
from pathlib import Path

from sysmlpy import load_project
from sysmlpy.plantuml import (
    as_general_view,
    as_interconnection_view,
    as_action_flow_view,
    as_package_view,
    as_tree_diagram,
)


def main() -> int:
    models_dir = Path("sysml/models")
    if not models_dir.exists():
        print(f"ERROR: {models_dir} not found", file=sys.stderr)
        return 1

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print(f"Loading SysML models from {models_dir}/ ...")
    model = load_project(str(models_dir))

    if model is None:
        print("ERROR: Failed to parse model", file=sys.stderr)
        return 1

    views = [
        ("general_view", as_general_view),
        ("interconnection_view", as_interconnection_view),
        ("action_flow_view", as_action_flow_view),
        ("package_view", as_package_view),
        ("tree_diagram", as_tree_diagram),
    ]

    for name, func in views:
        print(f"Generating {name} ...")
        try:
            puml = func(model, style="bw")
            output_file = output_dir / f"{name}.puml"
            output_file.write_text(puml, encoding="utf-8")
            print(f"  -> {output_file}")
        except Exception as exc:
            print(f"  WARNING: Could not generate {name}: {exc}")

    print(f"\nDone. Diagrams written to {output_dir}/")
    print("Render them with: plantuml output/*.puml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
