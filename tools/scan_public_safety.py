#!/usr/bin/env python3
"""Scan a public family handoff repo for obvious private data accidents."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "dist",
    "node_modules",
    "venv",
}

APPROVED_BINARY_PATHS = {
    "print/PJmaster-CD-label.pdf",
}

BINARY_SUFFIXES = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".zip",
}

SENSITIVE_DIR_NAMES = {
    "private",
    "secrets",
    "vault",
}

SENSITIVE_FILE_NAMES = {
    ".env",
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "id_ed25519",
    "id_rsa",
    "secrets.json",
}

SENSITIVE_FILE_SUFFIXES = {
    ".key",
    ".p12",
    ".pem",
    ".pfx",
}

PATTERNS = {
    "private key marker": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "github token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "generic api key assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"][^'\"<]{8,}['\"]"
    ),
    "ssn-like number": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "email address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
}


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    kind: str


def has_control_characters(value: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in value)


def format_finding(root: Path, finding: Finding) -> str:
    relative = finding.path.relative_to(root.resolve()).as_posix()
    location = f"{relative!r}:{finding.line}" if finding.line else repr(relative)
    return f"{location} [{finding.kind}]"


def is_luhn_valid(number: str) -> bool:
    digits = [int(char) for char in number if char.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def repository_paths(root: Path):
    def raise_walk_error(error: OSError) -> None:
        raise error

    for current_root, dirs, files in os.walk(root, onerror=raise_walk_error):
        retained_dirs = []
        for name in dirs:
            path = Path(current_root) / name
            if name in SKIP_DIRS:
                continue
            if path.is_symlink():
                yield path
                continue
            retained_dirs.append(name)
        dirs[:] = retained_dirs

        for filename in files:
            yield Path(current_root) / filename


def path_findings(root: Path, path: Path) -> list[Finding]:
    relative = path.relative_to(root)
    relative_name = relative.as_posix()
    filename = path.name.casefold()
    findings: list[Finding] = []

    if has_control_characters(relative_name):
        findings.append(Finding(path, 0, "control character in path"))

    if path.is_symlink():
        findings.append(Finding(path, 0, "symbolic link"))
        return findings

    if any(part.casefold() in SENSITIVE_DIR_NAMES for part in relative.parts[:-1]):
        findings.append(Finding(path, 0, "sensitive directory name"))

    if (
        filename in SENSITIVE_FILE_NAMES
        or filename.startswith(".env.")
        or path.suffix.casefold() in SENSITIVE_FILE_SUFFIXES
    ):
        findings.append(Finding(path, 0, "sensitive filename"))

    if path.suffix.casefold() in BINARY_SUFFIXES:
        if relative_name not in APPROVED_BINARY_PATHS:
            findings.append(Finding(path, 0, "unapproved binary file"))
        return findings

    return findings


def scan_file(path: Path) -> list[Finding]:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [Finding(path, 0, "unreviewed non-text file")]

    findings: list[Finding] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        for kind, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append(Finding(path, line_number, kind))

        for possible_card in re.findall(r"\b(?:\d[ -]?){13,19}\b", line):
            if is_luhn_valid(possible_card):
                findings.append(
                    Finding(path, line_number, "payment-card-like number")
                )

    return findings


def scan(root: Path) -> list[Finding]:
    root = root.resolve()
    if not root.is_dir():
        raise NotADirectoryError("Scan root must be an existing directory")
    findings: list[Finding] = []
    for path in repository_paths(root):
        findings.extend(path_findings(root, path))
        if path.is_symlink() or path.suffix.casefold() in BINARY_SUFFIXES:
            continue
        findings.extend(scan_file(path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repo root to scan")
    args = parser.parse_args()

    try:
        root = Path(args.root).resolve()
        findings = scan(root)
    except OSError as error:
        # Exception messages can contain private paths; report only the error type.
        print(
            f"Public safety scan could not complete ({type(error).__name__}). "
            "Check that the root is a readable directory.",
            file=sys.stderr,
        )
        return 2

    if findings:
        print("Public safety scan found potential private data:")
        for finding in findings:
            print(f"- {format_finding(root, finding)}")
        return 1

    print("Public safety scan passed: no public-safety findings found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
