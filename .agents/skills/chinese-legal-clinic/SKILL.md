---
name: chinese-legal-clinic
description: Use when the user needs Chinese legal work in the 法律诊所 domain: 法律诊所、学生案件接待、诊所备忘录、研究路线、结案移交、指导老师审阅、当事人沟通. This is a Codex adapter for claude-for-legal-ZH/legal-clinic; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows.
---

# 法律诊所 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/legal-clinic` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `legal-clinic`
- Domain profile template and shared rules: `legal-clinic/CLAUDE.md`
- Original skills directory: `legal-clinic/skills`
- Original plugin description: 配置法律诊所、导入学生、运行结构化接待（intake）、以执业风险意识追踪截止日期，并在学期结束时移交案件 — 依据中国法学院法律诊所实践规范与《律师执业管理办法》构建。

## How To Use

1. Read `legal-clinic/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/legal-clinic/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/legal-clinic:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`build-guide`, `client-comms-log`, `client-intake`, `client-letter`, `cold-start-interview`, `customize`, `deadlines`, `draft`, `form-generation`, `memo`, `plain-language-letters`, `ramp`, `research-start`, `semester-handoff`, `status`, `supervisor-review-queue`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
