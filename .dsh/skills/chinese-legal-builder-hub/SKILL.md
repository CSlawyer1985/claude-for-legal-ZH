---
name: chinese-legal-builder-hub
description: "Use when the user needs Chinese legal work in the 法律技能运营 domain: 查找法律技能、评估社区技能、安装法律技能、技能安全审查、法律工作流构建、法律运营. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/legal-builder-hub; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows."
---

# 法律技能运营 DeepSeek Harness Adapter

This skill lets DeepSeek Harness (`dsh`) use the original `claude-for-legal-ZH/legal-builder-hub` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `legal-builder-hub`
- Domain profile template and shared rules: `legal-builder-hub/CLAUDE.md`
- Original skills directory: `legal-builder-hub/skills`
- Original plugin description: 发现、评估和安装社区法律技能 — 以安全审查门控确保任何内容进入你的环境前经过检查。支持白名单（allowlist）、SHA 锁定更新、信任检查与技能质量评估框架。

## Path Resolution

The repository-relative paths above resolve against the `claude-for-legal-ZH` repository root:

- If the current workspace contains the repository, resolve them against the repository root directly.
- Otherwise (user-level install), run `cat ~/.dsh/legal-zh/repo` once to get the absolute repository path recorded by `scripts/install-dsh.sh`, then prefix the relative paths with it.

## How To Use

1. Read `legal-builder-hub/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into dsh actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use dsh filesystem, shell, web, and MCP tools for local files, verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For DeepSeek Harness, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.dsh/legal-zh/legal-builder-hub/CLAUDE.md` for dsh-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/legal-builder-hub:some-command`, interpret that as: load `legal-builder-hub/skills/some-command/SKILL.md` and perform the workflow in dsh.

## Legal Retrieval MCP

If the active dsh profile mounts the `chineselaw` or `yuandian` MCP servers (see `INSTALL_DSH.md`), prefer `mcp__chineselaw__*` and `mcp__yuandian__*` tools for statute, case, and regulatory verification. Without them, mark time-sensitive legal facts as requiring verification before reliance.

## Available Original Skills

`auto-updater`, `cold-start-interview`, `customize`, `disable`, `registry-browser`, `related-skills-surfacer`, `skill-installer`, `skill-manager`, `skills-qa`, `uninstall`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
