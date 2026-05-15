---
name: chinese-legal-privacy
description: Use when the user needs Chinese legal work in the 数据合规与隐私 domain: 个人信息保护影响评估、PIPL、数据处理协议、DSAR、隐私政策、数据合规差距、数据出境和隐私合规. This is a Codex adapter for claude-for-legal-ZH/privacy-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows.
---

# 数据合规与隐私 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/privacy-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `privacy-legal`
- Domain profile template and shared rules: `privacy-legal/CLAUDE.md`
- Original skills directory: `privacy-legal/skills`
- Original plugin description: 个人信息保护实务：处理活动分类、生成个人信息保护影响评估（个保法第55条）、审查个人信息处理协议（作为处理者或受托处理者）、在法定期限内起草个人信息主体权利响应（个保法第44-50条）、监测隐私政策与实践之间的偏差。

## How To Use

1. Read `privacy-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/privacy-legal/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/privacy-legal:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`cold-start-interview`, `customize`, `dpa-review`, `dsar-response`, `matter-workspace`, `pia-generation`, `policy-monitor`, `reg-gap-analysis`, `use-case-triage`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
