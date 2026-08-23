#!/usr/bin/env python3
"""Build a local CD-friendly zip package and text manifest."""

from __future__ import annotations

import hashlib
import os
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from tools.scan_public_safety import SKIP_DIRS, scan
except ModuleNotFoundError:  # Direct execution from tools/.
    from scan_public_safety import SKIP_DIRS, scan


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ZIP_PATH = DIST / "PJmaster-disc.zip"
MANIFEST_PATH = DIST / "PJmaster-disc-manifest.txt"

def iter_files(root: Path = ROOT):
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue

        relative = Path(os.fsdecode(raw_path))
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError(f"Unsafe tracked path: {relative}")
        if any(part in SKIP_DIRS for part in relative.parts[:-1]):
            raise RuntimeError(
                f"Refusing tracked file in scanner-skipped directory: {relative}"
            )

        path = root / relative
        if path.is_symlink():
            raise RuntimeError(f"Refusing to package symbolic link: {relative}")
        if not path.is_file():
            raise RuntimeError(f"Tracked file is missing: {relative}")
        yield path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    findings = scan(ROOT)
    if findings:
        print("Refusing to build a public disc package while the safety scan has findings:")
        for finding in findings:
            relative = finding.path.relative_to(ROOT)
            location = f"{relative}:{finding.line}" if finding.line else str(relative)
            print(f"- {location} [{finding.kind}] {finding.snippet}")
        return 1

    DIST.mkdir(exist_ok=True)
    try:
        files = sorted(iter_files(), key=lambda item: item.relative_to(ROOT).as_posix())
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Refusing to build the public disc package: {error}")
        return 1

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
