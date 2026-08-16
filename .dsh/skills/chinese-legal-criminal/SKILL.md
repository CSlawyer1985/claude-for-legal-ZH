---
name: chinese-legal-criminal
description: "Use when the user needs Chinese legal work in the 刑事辩护与合规 domain: 刑事辩护、阅卷笔录梳理、取保候审、羁押必要性审查、辩护策略、罪与非罪、涉案企业合规不起诉、刑事控告. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/criminal-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows."
---

# 刑事辩护与合规 DeepSeek Harness Adapter

This skill lets DeepSeek Harness (`dsh`) use the original `claude-for-legal-ZH/criminal-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `criminal-legal`
- Domain profile template and shared rules: `criminal-legal/CLAUDE.md`
- Original skills directory: `criminal-legal/skills`
- Original plugin description: 中国刑事辩护与刑事合规插件：脱敏前提下的阅卷笔录与证据链梳理、取保候审及羁押必要性审查辅助、辩护策略与类案法理分析、涉案企业合规不起诉审查。内置刑事诉讼法核心条文与合规评估基准参考库，强制脱敏红线与防幻觉校验纪律。适配刑事辩护律师、企业合规顾问等不同角色。

## Path Resolution

The repository-relative paths above resolve against the `claude-for-legal-ZH` repository root:

- If the current workspace contains the repository, resolve them against the repository root directly.
- Otherwise (user-level install), run `cat ~/.dsh/legal-zh/repo` once to get the absolute repository path recorded by `scripts/install-dsh.sh`, then prefix the relative paths with it.

## How To Use

1. Read `criminal-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into dsh actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use dsh filesystem, shell, web, and MCP tools for local files, verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For DeepSeek Harness, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.dsh/legal-zh/criminal-legal/CLAUDE.md` for dsh-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/criminal-legal:some-command`, interpret that as: load `criminal-legal/skills/some-command/SKILL.md` and perform the workflow in dsh.

## Legal Retrieval MCP

If the active dsh profile mounts the `chineselaw` or `yuandian` MCP servers (see `INSTALL_DSH.md`), prefer `mcp__chineselaw__*` and `mcp__yuandian__*` tools for statute, case, and regulatory verification. Without them, mark time-sensitive legal facts as requiring verification before reliance.

## Available Original Skills

`bail-application`, `case-analysis`, `cold-start-interview`, `compliance-non-prosecution`, `customize`, `defense-strategy`, `matter-workspace`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
