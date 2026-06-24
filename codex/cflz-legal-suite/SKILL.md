---
name: cflz-legal-suite
description: Router and public index for the claude-for-legal-ZH Chinese legal workflow suite. Use when the user mentions cflz, claude-for-legal-ZH, an original command such as /commercial-legal:review, or any Chinese legal workflow in contracts, privacy, product, corporate, employment, regulatory, AI governance, litigation, IP, legal education, legal clinic, or legal skill management.
---

# CFLZ Legal Suite Router

This is the Codex/Agent Skills routing layer for `claude-for-legal-ZH`.

The upstream repository is a Claude Code plugin marketplace. This adapter keeps the original legal workflow files as the source of truth and gives Codex a stable, unique naming scheme for all original skills.

## Routing Rule

When the user names an original Claude command:

```text
/<domain>:<skill>
```

map it to:

```text
cflz-<domain>-<skill>
```

Then read these files in order:

1. `<domain>/CLAUDE.md`
2. `<domain>/skills/<skill>/SKILL.md`
3. Any referenced files under that domain's `references/`, `agents/`, or cookbook folder.

Do not ask the user to run Claude Code slash commands inside Codex. Translate the workflow into Codex actions.

## Domain Index

| Original domain | Codex name pattern | Skills | Example |
|---|---|---:|---|
| `commercial-legal` | `cflz-commercial-legal-*` | 12 | `cflz-commercial-legal-amendment-history` ... |
| `privacy-legal` | `cflz-privacy-legal-*` | 9 | `cflz-privacy-legal-cold-start-interview` ... |
| `product-legal` | `cflz-product-legal-*` | 7 | `cflz-product-legal-cold-start-interview` ... |
| `corporate-legal` | `cflz-corporate-legal-*` | 13 | `cflz-corporate-legal-ai-tool-handoff` ... |
| `employment-legal` | `cflz-employment-legal-*` | 20 | `cflz-employment-legal-cold-start-interview` ... |
| `regulatory-legal` | `cflz-regulatory-legal-*` | 9 | `cflz-regulatory-legal-cold-start-interview` ... |
| `ai-governance-legal` | `cflz-ai-governance-legal-*` | 10 | `cflz-ai-governance-legal-ai-inventory` ... |
| `litigation-legal` | `cflz-litigation-legal-*` | 19 | `cflz-litigation-legal-brief-section-drafter` ... |
| `ip-legal` | `cflz-ip-legal-*` | 12 | `cflz-ip-legal-cease-desist` ... |
| `law-student` | `cflz-law-student-*` | 13 | `cflz-law-student-bar-prep-questions` ... |
| `legal-clinic` | `cflz-legal-clinic-*` | 16 | `cflz-legal-clinic-build-guide` ... |
| `legal-builder-hub` | `cflz-legal-builder-hub-*` | 10 | `cflz-legal-builder-hub-auto-updater` ... |

## Examples

- `/commercial-legal:amendment-history` -> `cflz-commercial-legal-amendment-history`
- `/privacy-legal:cold-start-interview` -> `cflz-privacy-legal-cold-start-interview`
- `/product-legal:cold-start-interview` -> `cflz-product-legal-cold-start-interview`
- `/corporate-legal:ai-tool-handoff` -> `cflz-corporate-legal-ai-tool-handoff`
- `/employment-legal:cold-start-interview` -> `cflz-employment-legal-cold-start-interview`
- `/regulatory-legal:cold-start-interview` -> `cflz-regulatory-legal-cold-start-interview`

## Manifest

The complete machine-readable index is `codex/manifest.json`.

## Configuration

- Claude Code practice profiles usually live under `~/.claude/plugins/config/claude-for-legal-zh/<domain>/CLAUDE.md`.
- Codex-specific profiles may live under `~/.codex/legal-zh/<domain>/CLAUDE.md`.
- If a workflow requires setup and the profile is missing or still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow conversationally before producing customized legal work.

## Safety Boundary

All outputs are lawyer-review drafts, not legal opinions replacing professional judgment. Current law, regulatory updates, cases, filing requirements, limitation periods, and other time-sensitive legal facts must be verified from reliable current sources before reliance.
