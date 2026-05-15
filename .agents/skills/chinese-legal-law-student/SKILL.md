---
name: chinese-legal-law-student
description: Use when the user needs Chinese legal work in the 法学学习与法考 domain: 法考、案例摘要、IRAC、课堂提问、法学写作、记忆卡片、学习计划、主观题和客观题训练. This is a Codex adapter for claude-for-legal-ZH/law-student; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows.
---

# 法学学习与法考 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/law-student` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `law-student`
- Domain profile template and shared rules: `law-student/CLAUDE.md`
- Original skills directory: `law-student/skills`
- Original plugin description: 互动式案例教学训练、案例摘要（case brief）、知识体系搭建（outline builder）、法考备考（客观题+主观题）、IRAC 写作评估、学习计划制定 — 始终引导思考，不替答不代写。适配中国法学教育与国家统一法律职业资格考试。

## How To Use

1. Read `law-student/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/law-student/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/law-student:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`bar-prep-questions`, `case-brief`, `cold-call-prep`, `cold-start-interview`, `customize`, `exam-forecast`, `flashcards`, `irac-practice`, `legal-writing`, `outline-builder`, `session`, `socratic-drill`, `study-plan`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
