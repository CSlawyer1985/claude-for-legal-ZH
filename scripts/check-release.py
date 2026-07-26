#!/usr/bin/env python3
"""Release readiness checks for claude-for-legal-ZH.

Checks the public package shape, not legal correctness. Portable: runs on
Windows without bash and on Linux CI.

Checks:
  1. Every domain SKILL.md has YAML frontmatter with name + description.
  2. All .json files parse; all .yaml/.yml files parse (if PyYAML available).
  3. No real absolute user-home paths leaked into the repo (e.g. /Users/<name>/).
  4. No likely secrets committed (API keys, tokens, passwords).

Adopted from community PR #4 (@Jamesyu0829), rewritten to avoid hardcoded
skill counts and to keep private-path patterns generic.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


ROOT = Path(__file__).resolve().parents[1]

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
}

# Real absolute home paths leaked from a contributor's machine. Placeholder
# usernames used in docs (e.g. `/Users/你/Desktop/...`) are allowlisted.
HOME_PATH_PATTERNS = [
    re.compile(r"/Users/([^/\s]+)/"),
    re.compile(r"[A-Za-z]:\\Users\\([^\\\s]+)", re.IGNORECASE),
    re.compile(r"/home/([^/\s]+)/"),
]
PLACEHOLDER_USERNAMES = {"你", "你的", "用户名", "user", "username", "your-name", "yourname", "name", "<user>", "xxx"}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|cookie|secret|password)\s*[:=]\s*['\"]([^'\"\s]{8,})['\"]"),
]
PLACEHOLDER_VALUE = re.compile(
    r"(?i)(your|xxx|placeholder|example|sample|dummy|test|changeme|\*+|<[^>]+>|你的|占位|示例)"
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


BINARY_NAMES = {".DS_Store"}


def repo_files(suffixes: set[str] | None = None) -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.name in BINARY_NAMES:
            continue
        if suffixes is None:
            # text scan: known text extensions plus extensionless dotfiles
            if path.suffix in TEXT_EXTENSIONS:
                files.append(path)
        elif path.suffix in suffixes:
            files.append(path)
    return files


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{rel(path)}: not valid UTF-8 ({exc})")
    return ""


def domain_roots() -> list[Path]:
    """A domain is a top-level directory carrying .claude-plugin/plugin.json."""
    roots = []
    for child in sorted(ROOT.iterdir()):
        if child.is_dir() and (child / ".claude-plugin" / "plugin.json").exists():
            roots.append(child)
    return roots


def check_skill_frontmatter(errors: list[str]) -> None:
    count = 0
    for domain in domain_roots():
        for path in sorted((domain / "skills").glob("*/SKILL.md")):
            count += 1
            text = read_text(path, errors)
            match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
            if not match:
                errors.append(f"{rel(path)}: missing YAML frontmatter")
                continue
            fm = match.group(1)
            for key in ("name", "description"):
                if not re.search(rf"^{key}:\s*\S", fm, re.MULTILINE):
                    errors.append(f"{rel(path)}: frontmatter missing {key}")
    print(f"  checked {count} domain skills across {len(domain_roots())} domains")


def check_json_yaml(errors: list[str]) -> None:
    for path in repo_files({".json"}):
        try:
            json.loads(read_text(path, errors))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel(path)}: invalid JSON ({exc})")
    if yaml is None:
        print("  note: PyYAML not installed, skipping YAML validation")
        return
    for path in repo_files({".yaml", ".yml"}):
        try:
            yaml.safe_load(read_text(path, errors))
        except yaml.YAMLError as exc:
            errors.append(f"{rel(path)}: invalid YAML ({exc})")


def check_public_safety(errors: list[str]) -> None:
    self_path = Path(__file__).resolve()
    for path in repo_files():
        if path.resolve() == self_path:
            continue  # the detection patterns legitimately live in this file
        text = read_text(path, errors)
        for pattern in HOME_PATH_PATTERNS:
            for m in pattern.finditer(text):
                username = m.group(1).strip("'\"")
                if username.lower() in PLACEHOLDER_USERNAMES or PLACEHOLDER_VALUE.search(username):
                    continue
                errors.append(f"{rel(path)}: absolute home path leaked ({m.group(0)})")
        for pattern in SECRET_PATTERNS:
            for m in pattern.finditer(text):
                value = m.group(m.lastindex or 0)
                if PLACEHOLDER_VALUE.search(value):
                    continue
                errors.append(f"{rel(path)}: possible secret ({m.group(0)[:24]}…)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="accepted for CI compatibility; findings always fail")
    parser.parse_args()

    errors: list[str] = []
    check_skill_frontmatter(errors)
    check_json_yaml(errors)
    check_public_safety(errors)

    if errors:
        print("release check FAILED:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("release check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
