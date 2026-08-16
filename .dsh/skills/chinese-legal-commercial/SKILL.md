---
name: chinese-legal-commercial
description: "Use when the user needs Chinese legal work in the 商事合同 domain: 合同审查、NDA、供应商协议、SaaS/MSA、续约、合同利益方摘要、合同风险上报、商事法务. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/commercial-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows."
---

# 商事合同 DeepSeek Harness Adapter

This skill lets DeepSeek Harness (`dsh`) use the original `claude-for-legal-ZH/commercial-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `commercial-legal`
- Domain profile template and shared rules: `commercial-legal/CLAUDE.md`
- Original skills directory: `commercial-legal/skills`
- Original plugin description: 依据供应商或采购方合同手册审查供应商协议、保密协议及SaaS订阅协议；自动追踪合同续约及终止期限，避免遗漏；将审批事项按规则路由至适当审批人；将法律审查结论转化为业务相关方能真正读懂的商业语言摘要。

## Path Resolution

The repository-relative paths above resolve against the `claude-for-legal-ZH` repository root:

- If the current workspace contains the repository, resolve them against the repository root directly.
- Otherwise (user-level install), run `cat ~/.dsh/legal-zh/repo` once to get the absolute repository path recorded by `scripts/install-dsh.sh`, then prefix the relative paths with it.

## How To Use

1. Read `commercial-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into dsh actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use dsh filesystem, shell, web, and MCP tools for local files, verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For DeepSeek Harness, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.dsh/legal-zh/commercial-legal/CLAUDE.md` for dsh-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/commercial-legal:some-command`, interpret that as: load `commercial-legal/skills/some-command/SKILL.md` and perform the workflow in dsh.

## Legal Retrieval MCP

If the active dsh profile mounts the `chineselaw` or `yuandian` MCP servers (see `INSTALL_DSH.md`), prefer `mcp__chineselaw__*` and `mcp__yuandian__*` tools for statute, case, and regulatory verification. Without them, mark time-sensitive legal facts as requiring verification before reliance.

## Available Original Skills

`amendment-history`, `cold-start-interview`, `customize`, `escalation-flagger`, `matter-workspace`, `nda-review`, `renewal-tracker`, `review`, `review-proposals`, `saas-msa-review`, `stakeholder-summary`, `vendor-agreement-review`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
