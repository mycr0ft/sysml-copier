"""Run semantic analysis on the SysML models in sysml/models/."""

import sys
from pathlib import Path

from sysmlpy import load_project, analyze


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

    print("Running semantic analysis ...")
    result = analyze(model, style_checks=True)

    if result.errors:
        print(f"\n{len(result.errors)} error(s):")
        for issue in result.errors:
            print(f"  [{issue.code}] {issue.message}")
    else:
        print("\nNo errors found.")

    if result.warnings:
        print(f"\n{len(result.warnings)} warning(s):")
        for issue in result.warnings:
            print(f"  [{issue.code}] {issue.message}")
    else:
        print("No warnings found.")

    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
