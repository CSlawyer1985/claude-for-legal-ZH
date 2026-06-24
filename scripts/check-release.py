#!/usr/bin/env python3
"""Release readiness checks for claude-for-legal-ZH.

This script is intentionally portable: it runs on Windows without bash and on
Linux CI. It checks the public package shape, not legal correctness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - dependency failure path
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
DOMAIN_NAMES = {
    "commercial-legal",
    "privacy-legal",
    "product-legal",
    "corporate-legal",
    "employment-legal",
    "regulatory-legal",
    "ai-governance-legal",
    "litigation-legal",
    "ip-legal",
    "law-student",
    "legal-clinic",
    "legal-builder-hub",
}
REQUIRED_README_MARKERS = [
    "律师审查草稿",
    "在 Claude Code 中安装",
    "Codex",
    "知识库路径可配置",
    "Anthropic claude-for-legal",
]
PRIVATE_PATH_PATTERNS = [
    re.compile("/Users/" + r"CS/Documents/知识库"),
    re.compile(r"C:\\Users\\ZWY", re.IGNORECASE),
]
SECRET_PATTERNS = [
    re.compile(r"sk-(?!ant-\.\.\.)[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|cookie|secret|password)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"),
]
TEXT_EXTENSIONS = {
    "",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".sh",
    ".html",
    ".txt",
    ".gitignore",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix in TEXT_EXTENSIONS or path.name in {".gitignore"}:
            files.append(path)
    return sorted(files)


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{rel(path)}: not valid UTF-8 ({exc})")
    return ""


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = read_text(path, errors)
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        errors.append(f"{rel(path)}: missing YAML frontmatter")
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    for key in ("name", "description"):
        if key not in data or not data[key]:
            errors.append(f"{rel(path)}: frontmatter missing {key}")
    return data


def check_skill_frontmatter(errors: list[str]) -> None:
    skills = [
        p
        for domain in DOMAIN_NAMES
        for p in sorted((ROOT / domain / "skills").glob("*/SKILL.md"))
    ]
    if len(skills) != 150:
        errors.append(f"expected 150 domain SKILL.md files, found {len(skills)}")
    for path in skills:
        parse_frontmatter(path, errors)


def check_codex_manifest(errors: list[str]) -> None:
    manifest_path = ROOT / "codex" / "manifest.json"
    if not manifest_path.exists():
        errors.append("codex/manifest.json is missing")
        return
    manifest = json.loads(read_text(manifest_path, errors) or "{}")
    for key in ("suite", "sourceRoot", "domains"):
        if key not in manifest:
            errors.append(f"codex/manifest.json: missing top-level {key}")
    if manifest.get("suite") != "cflz-legal-suite":
        errors.append("codex/manifest.json: suite must be cflz-legal-suite")
    domains = manifest.get("domains", [])
    seen_names: set[str] = set()
    seen_sources: set[str] = set()
    for domain in domains:
        for key in ("domain", "codexPrefix", "skills"):
            if key not in domain:
                errors.append(f"codex/manifest.json: domain entry missing {key}")
        domain_name = domain.get("domain", "")
        if domain_name not in DOMAIN_NAMES:
            errors.append(f"codex/manifest.json: unknown domain {domain_name}")
        expected_prefix = f"cflz-{domain_name}-"
        if domain.get("codexPrefix") != expected_prefix:
            errors.append(f"codex/manifest.json: bad prefix for {domain_name}")
        for skill in domain.get("skills", []):
            for key in ("slug", "source", "codexName"):
                if key not in skill:
                    errors.append(f"codex/manifest.json: skill in {domain_name} missing {key}")
            source = skill.get("source", "")
            codex_name = skill.get("codexName", "")
            if codex_name in seen_names:
                errors.append(f"codex/manifest.json: duplicate codexName {codex_name}")
            seen_names.add(codex_name)
            if source in seen_sources:
                errors.append(f"codex/manifest.json: duplicate source {source}")
            seen_sources.add(source)
            if not codex_name.startswith(expected_prefix):
                errors.append(f"codex/manifest.json: {codex_name} does not start with {expected_prefix}")
            if source and not (ROOT / source).exists():
                errors.append(f"codex/manifest.json: missing source {source}")
    if len(seen_names) != 150:
        errors.append(f"codex/manifest.json: expected 150 codex skills, found {len(seen_names)}")
    suite_skill = ROOT / "codex" / "cflz-legal-suite" / "SKILL.md"
    if not suite_skill.exists():
        errors.append("codex/cflz-legal-suite/SKILL.md is missing")
    else:
        parse_frontmatter(suite_skill, errors)


def check_json_yaml(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            json.loads(read_text(path, errors))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel(path)}: invalid JSON ({exc})")
    if yaml is None:
        errors.append("PyYAML is not installed; cannot validate YAML")
        return
    for path in sorted([*ROOT.rglob("*.yaml"), *ROOT.rglob("*.yml")]):
        if ".git" in path.parts:
            continue
        try:
            yaml.safe_load(read_text(path, errors))
        except yaml.YAMLError as exc:
            errors.append(f"{rel(path)}: invalid YAML ({exc})")


def check_public_safety(errors: list[str]) -> None:
    for path in text_files():
        text = read_text(path, errors)
        for pattern in PRIVATE_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel(path)}: contains private machine path matching {pattern.pattern}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel(path)}: contains possible secret matching {pattern.pattern}")


def check_readme(errors: list[str]) -> None:
    readme = read_text(ROOT / "README.md", errors)
    for marker in REQUIRED_README_MARKERS:
        if marker not in readme:
            errors.append(f"README.md: missing required marker {marker!r}")
    quickstart = read_text(ROOT / "QUICKSTART.md", errors)
    for marker in ("Claude Code", "Codex", "律师审查草稿"):
        if marker not in quickstart:
            errors.append(f"QUICKSTART.md: missing required marker {marker!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="fail on all release-readiness findings")
    parser.parse_args()

    errors: list[str] = []
    check_skill_frontmatter(errors)
    check_codex_manifest(errors)
    check_json_yaml(errors)
    check_public_safety(errors)
    check_readme(errors)

    if errors:
        print("release check FAILED:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("release check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
