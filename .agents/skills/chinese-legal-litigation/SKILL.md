---
name: chinese-legal-litigation
description: Use when the user needs Chinese legal work in the 诉讼仲裁 domain: 案件登记、诉讼仲裁、律师函、要件分析、大事记、证据三性、庭前准备、保全、传票、法律文书. This is a Codex adapter for claude-for-legal-ZH/litigation-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows.
---

# 诉讼仲裁 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/litigation-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `litigation-legal`
- Domain profile template and shared rules: `litigation-legal/CLAUDE.md`
- Original skills directory: `litigation-legal/skills`
- Original plugin description: 中国诉讼业务管理插件：案件组合管理、期限追踪、证据保全、律师函起草、外部律师协调——涵盖要件分析表（构成要件逐项分析）、大事记/时间线、庭前准备提纲、证据三性审查、起诉状/答辩状/代理词起草。适配法务/律师/独立执业等不同角色。

## How To Use

1. Read `litigation-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/litigation-legal/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/litigation-legal:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`brief-section-drafter`, `chronology`, `claim-chart`, `cold-start-interview`, `customize`, `demand-draft`, `demand-intake`, `demand-received`, `deposition-prep`, `legal-hold`, `matter-briefing`, `matter-close`, `matter-intake`, `matter-update`, `matter-workspace`, `oc-status`, `portfolio-status`, `privilege-log-review`, `subpoena-triage`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
