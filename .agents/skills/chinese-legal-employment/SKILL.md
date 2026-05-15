---
name: chinese-legal-employment
description: Use when the user needs Chinese legal work in the 劳动用工 domain: 劳动合同解除、劳动关系认定、假期管理、员工调查、规章制度、工资工时、跨省用工、劳动法. This is a Codex adapter for claude-for-legal-ZH/employment-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows.
---

# 劳动用工 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/employment-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `employment-legal`
- Domain profile template and shared rules: `employment-legal/CLAUDE.md`
- Original skills directory: `employment-legal/skills`
- Original plugin description: 中国劳动法插件：用工审查与解除风险评估、劳动关系认定（劳社部发〔2005〕12号三要素）、假期管理与法定期限跟踪、内部调查、劳动规章制度起草（含民主程序+公示要求）及各省/直辖市口径差异适配。

## How To Use

1. Read `employment-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/employment-legal/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/employment-legal:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`cold-start-interview`, `customize`, `expansion-kickoff`, `expansion-update`, `handbook-updates`, `hiring-review`, `internal-investigation`, `international-expansion`, `investigation-add`, `investigation-memo`, `investigation-open`, `investigation-query`, `investigation-summary`, `leave-tracker`, `log-leave`, `matter-workspace`, `policy-drafting`, `termination-review`, `wage-hour-qa`, `worker-classification`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
