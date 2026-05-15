---
name: chinese-legal-renewal-watcher
description: Use when the user needs a Chinese legal managed workflow for 合同续约监控工作流: 合同续约监控、自动续约、终止通知期限、续约提醒、合同台账读取. This is a Codex adapter for claude-for-legal-ZH/managed-agent-cookbooks/renewal-watcher.
---

# 合同续约监控工作流 Codex Adapter

This skill ports the original managed-agent cookbook into Codex workflow form.

## Source Files

- Cookbook root: `managed-agent-cookbooks/renewal-watcher`
- Read first: `managed-agent-cookbooks/renewal-watcher/README.md`
- Agent blueprint: `managed-agent-cookbooks/renewal-watcher/agent.yaml`
- Steering examples: `managed-agent-cookbooks/renewal-watcher/steering-examples.json`
- Subagent blueprints: `managed-agent-cookbooks/renewal-watcher/subagents`

## How To Use

1. Read the cookbook `README.md` and `agent.yaml` before running the workflow.
2. Translate Claude managed-agent concepts into Codex execution:
   - Use local file reads/writes for repositories, trackers, tables, and source documents.
   - Use Codex subagents only if the user explicitly asks for parallel agents or the workflow itself is requested as a multi-agent run.
   - Use Codex automations only when the user asks to monitor, remind, watch, or repeat the workflow over time.
3. If the cookbook references subagents, read only the relevant YAML files under `subagents/`.
4. Preserve legal review limits: all outputs are lawyer-review drafts; verify current legal facts and deadlines before reliance.
5. Produce the cookbook's intended artifact, such as a grid, tracker update, alert, digest, or memo, in the user's requested location or inline if no location is specified.
