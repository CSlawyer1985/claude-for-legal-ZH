---
name: chinese-legal-ip
description: "Use when the user needs Chinese legal work in the 知识产权 domain: 商标可注册性、FTO、侵权警告函、通知删除、开源许可证、知识产权条款、专利、著作权、商标. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/ip-legal; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows."
---

# 知识产权 DeepSeek Harness Adapter

This skill lets DeepSeek Harness (`dsh`) use the original `claude-for-legal-ZH/ip-legal` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `ip-legal`
- Domain profile template and shared rules: `ip-legal/CLAUDE.md`
- Original skills directory: `ip-legal/skills`
- Original plugin description: 知识产权实务：商标可注册性检索（相同/近似分析）、自由实施（FTO）初步分析、发明披露初步专利性筛选、起草和分类侵权警告函及信息网络传播权通知（发送与应对）、开源许可证合规审查、知识产权条款审查、知识产权组合管理与续展跟踪。

## Path Resolution

The repository-relative paths above resolve against the `claude-for-legal-ZH` repository root:

- If the current workspace contains the repository, resolve them against the repository root directly.
- Otherwise (user-level install), run `cat ~/.dsh/legal-zh/repo` once to get the absolute repository path recorded by `scripts/install-dsh.sh`, then prefix the relative paths with it.

## How To Use

1. Read `ip-legal/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into dsh actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use dsh filesystem, shell, web, and MCP tools for local files, verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For DeepSeek Harness, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.dsh/legal-zh/ip-legal/CLAUDE.md` for dsh-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/ip-legal:some-command`, interpret that as: load `ip-legal/skills/some-command/SKILL.md` and perform the workflow in dsh.

## Legal Retrieval MCP

If the active dsh profile mounts the `chineselaw` or `yuandian` MCP servers (see `INSTALL_DSH.md`), prefer `mcp__chineselaw__*` and `mcp__yuandian__*` tools for statute, case, and regulatory verification. Without them, mark time-sensitive legal facts as requiring verification before reliance.

## Available Original Skills

`cease-desist`, `clearance`, `cold-start-interview`, `customize`, `fto-triage`, `infringement-triage`, `invention-intake`, `ip-clause-review`, `matter-workspace`, `oss-review`, `portfolio`, `takedown`

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
