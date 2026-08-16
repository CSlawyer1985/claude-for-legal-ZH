---
name: chinese-legal-ai-governance
description: "Use when the user needs Chinese legal work in the AI 治理 domain: AI 应用登记、算法安全评估、科技伦理审查、生成式 AI 合规、AI 供应商审查、AI 治理. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/ai-governance-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows."
---

# AI 治理 DeepSeek Harness Adapter

This skill lets DeepSeek Harness (`dsh`) use the original `claude-for-legal-ZH/ai-governance-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `ai-governance-legal`
- Domain profile template and shared rules: `ai-governance-legal/CLAUDE.md`
- Original skills directory: `ai-governance-legal/skills`
- Original plugin description: AI 治理实务：对拟议的 AI 应用场景进行分类登记、依据适用监管体系开展算法安全评估与科技伦理审查、审查 AI 供应商条款中的训练数据使用和责任条款、保持 AI 使用政策与实践同步。

## Path Resolution

The repository-relative paths above resolve against the `claude-for-legal-ZH` repository root:

- If the current workspace contains the repository, resolve them against the repository root directly.
- Otherwise (user-level install), run `cat ~/.dsh/legal-zh/repo` once to get the absolute repository path recorded by `scripts/install-dsh.sh`, then prefix the relative paths with it.

## How To Use

1. Read `ai-governance-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into dsh actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use dsh filesystem, shell, web, and MCP tools for local files, verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For DeepSeek Harness, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.dsh/legal-zh/ai-governance-legal/CLAUDE.md` for dsh-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/ai-governance-legal:some-command`, interpret that as: load `ai-governance-legal/skills/some-command/SKILL.md` and perform the workflow in dsh.

## Legal Retrieval MCP

If the active dsh profile mounts the `chineselaw` or `yuandian` MCP servers (see `INSTALL_DSH.md`), prefer `mcp__chineselaw__*` and `mcp__yuandian__*` tools for statute, case, and regulatory verification. Without them, mark time-sensitive legal facts as requiring verification before reliance.

## Available Original Skills

`ai-inventory`, `aia-generation`, `cold-start-interview`, `customize`, `matter-workspace`, `policy-monitor`, `policy-starter`, `reg-gap-analysis`, `use-case-triage`, `vendor-ai-review`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
