#!/usr/bin/env python3
"""Bundle a SysML v2 model directory into a .kpar (KerML Project Archive) file.

A .kpar file is a ZIP archive (KerML spec clause 10 model interchange) containing:
  - .project.json  project metadata: name, version, description, usage (dependencies)
  - .meta.json     package->file index, creation timestamp, SHA256 checksums
  - the model files themselves (.sysml / .kerml)

If the source directory already contains .project.json / .meta.json, they are
used as-is (checksums in .meta.json are recomputed). Otherwise both are
generated from the directory contents and CLI options.

Usage:
    python scripts/make_kpar.py [SOURCE_DIR] [-o OUTPUT.kpar]
        [--name NAME] [--version V] [--description DESC]

Defaults: SOURCE_DIR = sysml/models, output written to dist/<name>-<version>.kpar
Stdlib only — no third-party dependencies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

MODEL_SUFFIXES = (".sysml", ".kerml")
# Fixed timestamp for reproducible archives (ZIP min is 1980-01-01).
_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

_PACKAGE_RE = re.compile(r"^\s*(?:public\s+|private\s+|protected\s+)?package\s+([\w']+)")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _package_name(model_text: str) -> str | None:
    """First package declaration in the file, if any."""
    m = _PACKAGE_RE.search(model_text)
    if not m:
        return None
    return m.group(1).strip("'")


def _project_name_fallback() -> tuple[str | None, str]:
    """(name, description) from pyproject.toml, if running inside a generated project."""
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        return None, ""
    try:
        import tomllib
        with pyproject.open("rb") as f:
            data = tomllib.load(f)
        project = data.get("project", {})
        return project.get("name"), project.get("description", "")
    except Exception:
        return None, ""


def build_project_json(source: Path, name: str, version: str, description: str) -> dict:
    """Merge resolved name/version/description with an existing .project.json, if any.

    name/version arrive already resolved (CLI flag > on-disk file > fallback)
    and are applied unconditionally; description only overrides when non-empty.
    """
    existing = source / ".project.json"
    data: dict = {}
    if existing.exists():
        try:
            data = json.loads(existing.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            print(f"warning: ignoring unreadable .project.json: {e}", file=sys.stderr)
    data["name"] = name
    data["version"] = version
    if description:
        data["description"] = description
    data.setdefault("description", description)
    # NB: 'usage' (dependencies) is carried through untouched — version
    # constraints belong to the DEPENDENCY's version (as in OMG-shipped
    # .kpar files), not the project being bundled.
    return data


def build_meta_json(model_files: list[Path]) -> dict:
    index: dict[str, str] = {}
    checksums: dict[str, dict[str, str]] = {}
    for path in sorted(model_files):
        pkg = _package_name(path.read_text(encoding="utf-8")) or path.stem
        index[pkg] = path.name
        checksums[path.name] = {"value": _sha256(path), "algorithm": "SHA256"}
    return {
        "index": index,
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checksum": checksums,
    }


def make_kpar(
    source: Path,
    output: Path,
    name: str,
    version: str,
    description: str,
) -> Path:
    if not source.is_dir():
        raise SystemExit(f"error: source directory not found: {source}")

    model_files = [
        p for p in sorted(source.iterdir())
        if p.is_file() and p.suffix in MODEL_SUFFIXES
    ]
    if not model_files:
        raise SystemExit(f"error: no .sysml/.kerml files found in {source}")

    project = build_project_json(source, name, version, description)
    meta = build_meta_json(model_files)

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            zipfile.ZipInfo(".project.json", date_time=_ZIP_TIMESTAMP),
            json.dumps(project, indent=2) + "\n",
        )
        zf.writestr(
            zipfile.ZipInfo(".meta.json", date_time=_ZIP_TIMESTAMP),
            json.dumps(meta, indent=2) + "\n",
        )
        for path in model_files:
            zf.write(path, arcname=path.name)

    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="make_kpar",
        description="Bundle a SysML v2 model directory into a .kpar archive",
    )
    parser.add_argument("source", nargs="?", default="sysml/models",
                        help="directory containing .sysml/.kerml files (default: sysml/models)")
    parser.add_argument("-o", "--output", default=None, metavar="FILE",
                        help="output .kpar path (default: dist/<name>-<version>.kpar)")
    parser.add_argument("--name", default=None,
                        help="project name (default: .project.json, pyproject.toml, or dir name)")
    parser.add_argument("--version", default=None,
                        help="project version (default: .project.json version or 0.1.0)")
    parser.add_argument("--description", default="", help="project description")
    args = parser.parse_args(argv)

    source = Path(args.source)
    fallback_name, fallback_desc = _project_name_fallback()
    name = args.name or fallback_name or source.resolve().name
    version = args.version or "0.1.0"
    description = args.description or fallback_desc

    # Honour an existing .project.json for name/version, but explicit CLI flags win.
    existing = source / ".project.json"
    if existing.exists():
        try:
            data = json.loads(existing.read_text(encoding="utf-8"))
            name = args.name or data.get("name", name)
            version = args.version or data.get("version", version)
        except (json.JSONDecodeError, OSError) as e:
            print(f"warning: could not read existing .project.json: {e}", file=sys.stderr)

    output = Path(args.output) if args.output else Path("dist") / f"{name}-{version}.kpar"
    output = make_kpar(source, output, name, version, description)

    with zipfile.ZipFile(output) as zf:
        n = len(zf.namelist())
    print(f"created {output} ({output.stat().st_size} bytes, {n} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())