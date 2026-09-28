---
name: chinese-legal-law-practice-cn
description: "Use when the user needs Chinese legal work in the 中国律师业务 domain: 法律咨询分析、客户法律答复、法律服务方案、律师报价、一般投诉分流、举报申诉. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/law-practice-cn; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows."
---

# 中国律师业务 DeepSeek Harness Adapter

This skill lets DeepSeek Harness (`dsh`) use the original `claude-for-legal-ZH/law-practice-cn` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `law-practice-cn`
- Domain profile template and shared rules: `law-practice-cn/CLAUDE.md`
- Original skills directory: `law-practice-cn/skills`
- Original plugin description: 中国律师业务工作流：法律咨询、一般投诉分流、服务方案与报价；区分客户材料、法源核验和对外动作。

## Path Resolution

The repository-relative paths above resolve against the `claude-for-legal-ZH` repository root:

- If the current workspace contains the repository, resolve them against the repository root directly.
- Otherwise (user-level install), run `cat ~/.dsh/legal-zh/repo` once to get the absolute repository path recorded by `scripts/install-dsh.sh`, then prefix the relative paths with it.

## How To Use

1. Read `law-practice-cn/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into dsh actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use dsh filesystem, shell, web, and MCP tools for local files, verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For DeepSeek Harness, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.dsh/legal-zh/law-practice-cn/CLAUDE.md` for dsh-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/law-practice-cn:some-command`, interpret that as: load `law-practice-cn/skills/some-command/SKILL.md` and perform the workflow in dsh.

## Legal Retrieval MCP

If the active dsh profile mounts an authenticated legal MCP such as `yuandian` or `pkulaw` (see `INSTALL_DSH.md`), inspect the live tool list before use. Database results are discovery evidence; verify key law, case status, and deadlines against original sources. If unavailable, record the gap and use official public sources where possible.

## Available Original Skills

`cold-start-interview`, `complaint-triage`, `consultation-analysis`, `legal-service-proposal`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
