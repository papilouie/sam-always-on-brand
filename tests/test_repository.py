from __future__ import annotations

import importlib.util
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "packages" / "sam-aobpg" / "scripts" / "validate_pack.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("sam_validate_pack", VALIDATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_example_brand_pack_is_valid():
    validator = load_validator()
    errors = validator.validate_pack(ROOT / "examples" / "brands" / "sunny-spoon")
    assert errors == []


def test_example_campaign_pack_is_valid():
    validator = load_validator()
    errors = validator.validate_pack(ROOT / "examples" / "campaigns" / "sunny-spoon-back-to-school")
    assert errors == []


def test_skill_frontmatter_and_invocation_policy():
    skill = (ROOT / "packages" / "sam-aobpg" / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\n")
    frontmatter = yaml.safe_load(skill.split("---", 2)[1])
    assert frontmatter["name"] == "sam-aobpg"
    assert "on-brand" in frontmatter["description"]

    metadata = yaml.safe_load(
        (ROOT / "packages" / "sam-aobpg" / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    assert metadata["policy"]["allow_implicit_invocation"] is True
    assert "$sam-aobpg" in metadata["interface"]["default_prompt"]


def test_decision_support_and_approval_are_core_contracts():
    skill = (ROOT / "packages" / "sam-aobpg" / "SKILL.md").read_text(encoding="utf-8")
    workflow = (ROOT / "packages" / "sam-aobpg" / "references" / "workflow.md").read_text(encoding="utf-8")
    assert "suggestions or examples" in skill
    assert "recommend the best choice" in skill
    assert "Do not generate final content" in skill
    assert "Approval gates" in workflow


def test_release_builder_creates_installable_archives(tmp_path):
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_releases.py")], cwd=ROOT, check=True)

    openai_zip = ROOT / "releases" / "sam-openai-skill-v1.0.0.zip"
    claude_zip = ROOT / "releases" / "sam-claude-skill-v1.0.0.zip"
    custom_zip = ROOT / "releases" / "sam-custom-gpt-v1.0.0.zip"
    assert openai_zip.is_file() and claude_zip.is_file() and custom_zip.is_file()

    with zipfile.ZipFile(openai_zip) as archive:
        names = set(archive.namelist())
        assert "sam-aobpg/SKILL.md" in names
        assert "sam-aobpg/agents/openai.yaml" in names
        assert "sam-aobpg/schemas/brand-pack.schema.json" in names
        archive.extractall(tmp_path / "openai")

    with zipfile.ZipFile(claude_zip) as archive:
        names = set(archive.namelist())
        assert "sam-aobpg/SKILL.md" in names
        assert "sam-aobpg/agents/openai.yaml" not in names

    with zipfile.ZipFile(custom_zip) as archive:
        names = set(archive.namelist())
        assert "sam-custom-gpt/instructions.md" in names
        assert "sam-custom-gpt/knowledge/sam-knowledge.md" in names

    installed_validator = tmp_path / "openai" / "sam-aobpg" / "scripts" / "validate_pack.py"
    result = subprocess.run(
        [sys.executable, str(installed_validator), str(ROOT / "examples" / "brands" / "sunny-spoon")],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
