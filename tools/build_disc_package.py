#!/usr/bin/env python3
"""Build a local CD-friendly zip package and text manifest."""

from __future__ import annotations

import hashlib
import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ZIP_PATH = DIST / "PJmaster-disc.zip"
MANIFEST_PATH = DIST / "PJmaster-disc-manifest.txt"

SKIP_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "dist",
}


def should_include(path: Path) -> bool:
    parts = set(path.relative_to(ROOT).parts)
    return not parts.intersection(SKIP_DIRS)


def iter_files():
    for current_root, dirs, files in os.walk(ROOT):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        for filename in files:
            path = Path(current_root) / filename
            if should_include(path):
                yield path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    DIST.mkdir(exist_ok=True)
    files = sorted(iter_files(), key=lambda item: item.relative_to(ROOT).as_posix())

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())

    lines = [
        "PJmaster Disc Manifest",
        f"Built: {datetime.now(timezone.utc).isoformat()}",
        f"Repo: https://github.com/ChristFollower873461/PJmaster",
        "",
        "Files:",
    ]
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f"{sha256(path)}  {rel}")

    MANIFEST_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {ZIP_PATH.relative_to(ROOT)}")
    print(f"Wrote {MANIFEST_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
