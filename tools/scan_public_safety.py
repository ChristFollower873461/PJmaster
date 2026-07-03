#!/usr/bin/env python3
"""Scan a public family handoff repo for obvious private data accidents."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".csv",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yml",
    ".yaml",
}

SKIP_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "dist",
}

SKIP_SUFFIXES = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".zip",
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
    snippet: str


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


def text_files(root: Path):
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        for filename in files:
            path = Path(current_root) / filename
            if path.suffix.lower() in SKIP_SUFFIXES:
                continue
            if path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"Makefile", "LICENSE"}:
                yield path


def scan_file(path: Path) -> list[Finding]:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    findings: list[Finding] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        for kind, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append(Finding(path, line_number, kind, line.strip()[:160]))

        for possible_card in re.findall(r"\b(?:\d[ -]?){13,19}\b", line):
            if is_luhn_valid(possible_card):
                findings.append(
                    Finding(path, line_number, "payment-card-like number", line.strip()[:160])
                )

    return findings


def scan(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in text_files(root):
        findings.extend(scan_file(path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repo root to scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings = scan(root)

    if findings:
        print("Public safety scan found potential private data:")
        for finding in findings:
            rel = finding.path.resolve().relative_to(root)
            print(f"- {rel}:{finding.line} [{finding.kind}] {finding.snippet}")
        return 1

    print("Public safety scan passed: no obvious private data patterns found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
