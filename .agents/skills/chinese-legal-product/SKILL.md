---
name: chinese-legal-product
description: Use when the user needs Chinese legal work in the 产品与营销合规 domain: 产品上线审查、营销文案审查、广告法、反不正当竞争、功能法律风险、业务法务快速咨询. This is a Codex adapter for claude-for-legal-ZH/product-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows.
---

# 产品与营销合规 Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/product-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `product-legal`
- Domain profile template and shared rules: `product-legal/CLAUDE.md`
- Original skills directory: `product-legal/skills`
- Original plugin description: 依据您的风险校准审查产品上线，在数分钟内解答「这有问题吗？」类问题，审查营销文案中需证实的宣传主张，并在任何人开口之前标记即将需要法务介入的上线项目。

## How To Use

1. Read `product-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/product-legal/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/product-legal:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

`cold-start-interview`, `customize`, `feature-risk-assessment`, `is-this-a-problem`, `launch-review`, `marketing-claims-review`, `matter-workspace`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
