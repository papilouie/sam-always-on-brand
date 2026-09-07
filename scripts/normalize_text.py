#!/usr/bin/env python3
"""Normalize repository text files to UTF-8 with one trailing newline."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".toml", ".txt"}
NAMES = {"LICENSE", ".gitignore"}
IGNORED_PARTS = {".git", ".venv", "releases", "__pycache__"}


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in SUFFIXES and path.name not in NAMES:
            continue
        original = path.read_text(encoding="utf-8")
        normalized = original.rstrip() + "\n"
        if normalized != original:
            path.write_text(normalized, encoding="utf-8", newline="\n")
            changed += 1
    print(f"Normalized {changed} files")


if __name__ == "__main__":
    main()
