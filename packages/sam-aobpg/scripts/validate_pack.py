#!/usr/bin/env python3
"""Validate a SAM Brand Pack or Campaign Pack and its referenced files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


SCHEMAS = {
    "sam-brand-pack": "brand-pack.schema.json",
    "sam-campaign-pack": "campaign-pack.schema.json",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def safe_reference(pack_dir: Path, relative: str) -> Path:
    candidate = (pack_dir / relative).resolve()
    root = pack_dir.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"Referenced path escapes the pack: {relative}")
    return candidate


def schema_root() -> Path:
    script = Path(__file__).resolve()
    candidates = [script.parents[1] / "schemas", script.parents[3] / "schemas"]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("Could not locate the SAM schemas directory")


def validate_document(data: dict[str, Any], schema_name: str) -> list[str]:
    schema = __import__("json").loads(
        (schema_root() / schema_name).read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path))
    ]


def validate_pack(pack_dir: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = pack_dir / "manifest.yaml"
    if not manifest_path.is_file():
        return [f"Missing manifest: {manifest_path}"]

    try:
        manifest = load_yaml(manifest_path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [str(exc)]

    pack_type = manifest.get("pack_type")
    schema_name = SCHEMAS.get(pack_type)
    if schema_name is None:
        return [f"Unsupported pack_type: {pack_type!r}"]

    errors.extend(validate_document(manifest, schema_name))

    referenced: list[tuple[str, str]] = []
    for label, value in manifest.get("files", {}).items():
        if isinstance(value, str) and value:
            referenced.append((f"files.{label}", value))
    for section in ("channels", "offers"):
        for index, item in enumerate(manifest.get(section, [])):
            if isinstance(item, dict) and isinstance(item.get("file"), str):
                referenced.append((f"{section}[{index}].file", item["file"]))
    for label, value in manifest.get("assets", {}).items():
        if isinstance(value, str) and value:
            referenced.append((f"assets.{label}", value))

    for label, relative in referenced:
        try:
            target = safe_reference(pack_dir, relative)
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            continue
        if not target.is_file():
            errors.append(f"{label}: referenced file does not exist: {relative}")

    structured = []
    if pack_type == "sam-brand-pack":
        structured.append((manifest.get("files", {}).get("brand_profile"), "brand-profile.schema.json"))
        structured.extend((item.get("file"), "offer.schema.json") for item in manifest.get("offers", []))
    else:
        structured.append((manifest.get("files", {}).get("campaign_brief"), "campaign-brief.schema.json"))

    for relative, child_schema in structured:
        if not relative:
            continue
        try:
            target = safe_reference(pack_dir, relative)
            if target.is_file():
                errors.extend(f"{relative}: {message}" for message in validate_document(load_yaml(target), child_schema))
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{relative}: {exc}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path, help="Directory containing manifest.yaml")
    args = parser.parse_args()
    errors = validate_pack(args.pack)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALID: {args.pack}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
