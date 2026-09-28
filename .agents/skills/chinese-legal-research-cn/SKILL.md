---
name: chinese-legal-research-cn
description: "Use when the user needs Chinese legal work in the 中国法研究 domain: 法源核验、法规版本、类案对比、案例状态、法律检索、争点研究备忘录、法律讲座备课. This is a Codex adapter for claude-for-legal-ZH/legal-research-cn; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows."
---

# 中国法研究 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/legal-research-cn` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `legal-research-cn`
- Domain profile template and shared rules: `legal-research-cn/CLAUDE.md`
- Original skills directory: `legal-research-cn/skills`
- Original plugin description: 中国法争点检索、法源与版本核验、类案对比及可追溯研究备忘录；区分公开来源、商业数据库结果与律师判断。

## How To Use

1. Read `legal-research-cn/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/legal-research-cn/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/legal-research-cn:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`authority-check`, `case-comparison`, `cold-start-interview`, `issue-memo`, `lecture-source-pack`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
