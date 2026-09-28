---
name: chinese-legal-procurement
description: "Use when the user needs Chinese legal work in the 政府采购与招标投标 domain: 政府采购、采购文件审查、投标资格、评分规则、质疑投诉、采购合同履行. This is a Codex adapter for claude-for-legal-ZH/procurement-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows."
---

# 政府采购与招标投标 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/procurement-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `procurement-legal`
- Domain profile template and shared rules: `procurement-legal/CLAUDE.md`
- Original skills directory: `procurement-legal/skills`
- Original plugin description: 中国政府采购与招标投标法律工作流：适用制度识别、资格与评分审查、质疑投诉、合同履行和期限线索。

## How To Use

1. Read `procurement-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/procurement-legal/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/procurement-legal:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`bid-review`, `challenge-complaint`, `cold-start-interview`, `contract-performance`, `regime-triage`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
