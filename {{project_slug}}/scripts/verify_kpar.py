#!/usr/bin/env python3
"""Verify a .kpar (KerML Project Archive) file: structure, index, and checksums.

Checks that the archive:
  - is a readable ZIP
  - contains .project.json and .meta.json
  - .meta.json's checksum entries match the actual bundled files (SHA256)
  - .meta.json's index entries point at files present in the archive

Works on any conformant .kpar, including OMG-shipped standard libraries.

Usage:
    python scripts/verify_kpar.py FILE.kpar [FILE.kpar ...]

Exits 0 if all archives verify, 1 otherwise. Stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path


def verify(path: Path) -> bool:
    ok = True
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        for required in (".project.json", ".meta.json"):
            if required not in names:
                print(f"{path}: MISSING {required}")
                return False
        meta = json.loads(z.read(".meta.json"))
        for fname, entry in meta.get("checksum", {}).items():
            if fname not in names:
                print(f"{path}: index/checksum references missing file {fname}")
                ok = False
                continue
            digest = hashlib.sha256(z.read(fname)).hexdigest()
            if entry.get("algorithm") == "SHA256" and digest != entry.get("value"):
                print(f"{path}: checksum mismatch for {fname}")
                ok = False
        for _pkg, fname in meta.get("index", {}).items():
            if fname not in names:
                print(f"{path}: index points at missing file {fname}")
                ok = False
        # .project.json must be valid JSON with at least a name and version
        project = json.loads(z.read(".project.json"))
        if not project.get("name") or not project.get("version"):
            print(f"{path}: .project.json lacks name/version")
            ok = False
    print(f"{path}: {'OK' if ok else 'FAILED'}")
    return ok


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(__doc__)
        return 2
    results = [verify(Path(p)) for p in args]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())