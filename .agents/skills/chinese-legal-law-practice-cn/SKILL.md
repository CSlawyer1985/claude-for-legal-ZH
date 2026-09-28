---
name: chinese-legal-law-practice-cn
description: "Use when the user needs Chinese legal work in the 中国律师业务 domain: 法律咨询分析、客户法律答复、法律服务方案、律师报价、一般投诉分流、举报申诉. This is a Codex adapter for claude-for-legal-ZH/law-practice-cn; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows."
---

# 中国律师业务 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/law-practice-cn` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `law-practice-cn`
- Domain profile template and shared rules: `law-practice-cn/CLAUDE.md`
- Original skills directory: `law-practice-cn/skills`
- Original plugin description: 中国律师业务工作流：法律咨询、一般投诉分流、服务方案与报价；区分客户材料、法源核验和对外动作。

## How To Use

1. Read `law-practice-cn/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/law-practice-cn/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/law-practice-cn:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`cold-start-interview`, `complaint-triage`, `consultation-analysis`, `legal-service-proposal`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
