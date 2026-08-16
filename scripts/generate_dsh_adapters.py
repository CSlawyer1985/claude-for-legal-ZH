#!/usr/bin/env python3
"""Generate DeepSeek Harness (dsh) skill adapters for claude-for-legal-ZH.

The upstream repository is a Claude Code plugin marketplace. DeepSeek Harness
discovers skills from `<project>/.dsh/skills` and `~/.dsh/skills` (it also
scans `.agents/skills`, where the Codex adapters live). This script creates a
dsh-native routing layer so dsh can reuse the original domain `CLAUDE.md`,
`skills/*/SKILL.md`, and managed-agent cookbook content without duplicating
the legal workflows.

Domain and cookbook metadata are imported from generate_codex_adapters.py so
both harness adapters share one source of truth.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_codex_adapters import (  # noqa: E402
    COOKBOOKS,
    DOMAINS,
    ROOT,
    plugin_description,
    skill_names,
)

SKILLS_ROOT = ROOT / ".dsh" / "skills"

PATH_RESOLUTION = """## Path Resolution

The repository-relative paths above resolve against the `claude-for-legal-ZH` repository root:

- If the current workspace contains the repository, resolve them against the repository root directly.
- Otherwise (user-level install), run `cat ~/.dsh/legal-zh/repo` once to get the absolute repository path recorded by `scripts/install-dsh.sh`, then prefix the relative paths with it.
"""


def yaml_string(text: str) -> str:
    """Quote a scalar for YAML frontmatter (JSON string = valid YAML flow scalar).

    Descriptions contain `: ` (e.g. "domain: ...") which breaks unquoted YAML
    plain scalars; dsh parses frontmatter with a strict YAML parser and drops
    unparseable skills from discovery.
    """
    return json.dumps(text, ensure_ascii=False)


def adapter_body(domain: str, meta: dict, skills: list[str], description: str) -> str:
    commands = ", ".join(f"`{name}`" for name in skills)
    desc = f'Use when the user needs Chinese legal work in the {meta["display"]} domain: {meta["triggers"]}. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/{domain}; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows.'
    return f"""---
name: {meta["codex_name"]}
description: {yaml_string(desc)}
---

# {meta["display"]} DeepSeek Harness Adapter

This skill lets DeepSeek Harness (`dsh`) use the original `claude-for-legal-ZH/{domain}` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `{domain}`
- Domain profile template and shared rules: `{domain}/CLAUDE.md`
- Original skills directory: `{domain}/skills`
- Original plugin description: {description or "See plugin manifest."}

{PATH_RESOLUTION}
## How To Use

1. Read `{domain}/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into dsh actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use dsh filesystem, shell, web, and MCP tools for local files, verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For DeepSeek Harness, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.dsh/legal-zh/{domain}/CLAUDE.md` for dsh-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/{domain}:some-command`, interpret that as: load `{domain}/skills/some-command/SKILL.md` and perform the workflow in dsh.

## Legal Retrieval MCP

If the active dsh profile mounts the `chineselaw` or `yuandian` MCP servers (see `INSTALL_DSH.md`), prefer `mcp__chineselaw__*` and `mcp__yuandian__*` tools for statute, case, and regulatory verification. Without them, mark time-sensitive legal facts as requiring verification before reliance.

## Available Original Skills

{commands}

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
"""


def cookbook_body(cookbook: str, meta: dict) -> str:
    root = f"managed-agent-cookbooks/{cookbook}"
    desc = f'Use when the user needs a Chinese legal managed workflow for {meta["display"]}: {meta["triggers"]}. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/managed-agent-cookbooks/{cookbook}.'
    return f"""---
name: {meta["codex_name"]}
description: {yaml_string(desc)}
---

# {meta["display"]} DeepSeek Harness Adapter

This skill ports the original managed-agent cookbook into a DeepSeek Harness (`dsh`) workflow.

## Source Files

- Cookbook root: `{root}`
- Read first: `{root}/README.md`
- Agent blueprint: `{root}/agent.yaml`
- Steering examples: `{root}/steering-examples.json`
- Subagent blueprints: `{root}/subagents`

{PATH_RESOLUTION}
## How To Use

1. Read the cookbook `README.md` and `agent.yaml` before running the workflow.
2. Translate Claude managed-agent concepts into dsh execution:
   - Use dsh filesystem tools for repositories, trackers, tables, and source documents.
   - Use the dsh subagent tool only if the user explicitly asks for parallel agents or the workflow itself is requested as a multi-agent run.
   - Use dsh jobs/schedules only when the user asks to monitor, remind, watch, or repeat the workflow over time.
3. If the cookbook references subagents, read only the relevant YAML files under `subagents/`.
4. Preserve legal review limits: all outputs are lawyer-review drafts; verify current legal facts and deadlines before reliance.
5. Produce the cookbook's intended artifact, such as a grid, tracker update, alert, digest, or memo, in the user's requested location or inline if no location is specified.
"""


def main() -> None:
    SKILLS_ROOT.mkdir(parents=True, exist_ok=True)
    for domain, meta in DOMAINS.items():
        domain_root = ROOT / domain
        if not domain_root.exists():
            raise SystemExit(f"Missing domain root: {domain_root}")
        out_dir = SKILLS_ROOT / meta["codex_name"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "SKILL.md").write_text(
            adapter_body(domain, meta, skill_names(domain_root), plugin_description(domain_root)),
            encoding="utf-8",
        )
    for cookbook, meta in COOKBOOKS.items():
        root = ROOT / "managed-agent-cookbooks" / cookbook
        if not root.exists():
            raise SystemExit(f"Missing cookbook root: {root}")
        out_dir = SKILLS_ROOT / meta["codex_name"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "SKILL.md").write_text(cookbook_body(cookbook, meta), encoding="utf-8")
    print(f"Generated {len(DOMAINS) + len(COOKBOOKS)} dsh adapters under {SKILLS_ROOT}")


if __name__ == "__main__":
    main()
