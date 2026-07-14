"""Navigate and query the SysML model in sysml/models/."""

import sys
from pathlib import Path

from sysmlpy import load_project


def main() -> int:
    models_dir = Path("sysml/models")
    if not models_dir.exists():
        print(f"ERROR: {models_dir} not found", file=sys.stderr)
        return 1

    print(f"Loading SysML models from {models_dir}/ ...")
    model = load_project(str(models_dir))

    if model is None:
        print("ERROR: Failed to parse model", file=sys.stderr)
        return 1

    print(f"\nModel: {model}")
    print(f"Total child elements: {len(model)}")

    print("\nPackages:")
    for pkg in model.packages:
        print(f"  {pkg.name}")
        for child in pkg:
            print(f"    {child.sysml_type}: {child.name}")

    print("\nParts (recursive):")
    for part in model.find(sysml_type="part"):
        print(f"  {part.name}")

    print("\nActions (recursive):")
    for action in model.find(sysml_type="action"):
        print(f"  {action.name}")

    print("\nRequirements (recursive):")
    for req in model.find(sysml_type="requirement"):
        print(f"  {req.name}")

    camera = model.find_one("Camera")
    if camera:
        print(f"\nFound Camera: {camera.name}")
        print(f"  Children: {len(camera)}")
        for child in camera:
            print(f"    {child.sysml_type}: {child.name}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
