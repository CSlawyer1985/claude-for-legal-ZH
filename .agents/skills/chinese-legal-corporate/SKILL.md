---
name: chinese-legal-corporate
description: Use when the user needs Chinese legal work in the 公司与并购 domain: 并购尽调、重大合同披露、董事会/股东会决议、交割清单、公司合规、投后整合、公司法. This is a Codex adapter for claude-for-legal-ZH/corporate-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows.
---

# 公司与并购 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/corporate-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `corporate-legal`
- Domain profile template and shared rules: `corporate-legal/CLAUDE.md`
- Original skills directory: `corporate-legal/skills`
- Original plugin description: 规模化开展并购尽调（附引用来源的表格化审查），制作披露函与交割检查表，按公司格式起草董事会决议与股东会决议，跨法域追踪主体合规期限。

## How To Use

1. Read `corporate-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/corporate-legal/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/corporate-legal:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`ai-tool-handoff`, `board-minutes`, `closing-checklist`, `cold-start-interview`, `customize`, `deal-team-summary`, `diligence-issue-extraction`, `entity-compliance`, `integration-management`, `material-contract-schedule`, `matter-workspace`, `tabular-review`, `written-consent`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
