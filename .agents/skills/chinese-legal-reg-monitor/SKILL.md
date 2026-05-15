---
name: chinese-legal-reg-monitor
description: Use when the user needs a Chinese legal managed workflow for 监管动态监控工作流: 监管动态监控、法规 feed、监管摘要、重大性过滤、合规周报. This is a Codex adapter for claude-for-legal-ZH/managed-agent-cookbooks/reg-monitor.
---

# 监管动态监控工作流 Codex Adapter

This skill ports the original managed-agent cookbook into Codex workflow form.

## Source Files

- Cookbook root: `managed-agent-cookbooks/reg-monitor`
- Read first: `managed-agent-cookbooks/reg-monitor/README.md`
- Agent blueprint: `managed-agent-cookbooks/reg-monitor/agent.yaml`
- Steering examples: `managed-agent-cookbooks/reg-monitor/steering-examples.json`
- Subagent blueprints: `managed-agent-cookbooks/reg-monitor/subagents`

## How To Use

1. Read the cookbook `README.md` and `agent.yaml` before running the workflow.
2. Translate Claude managed-agent concepts into Codex execution:
   - Use local file reads/writes for repositories, trackers, tables, and source documents.
   - Use Codex subagents only if the user explicitly asks for parallel agents or the workflow itself is requested as a multi-agent run.
   - Use Codex automations only when the user asks to monitor, remind, watch, or repeat the workflow over time.
3. If the cookbook references subagents, read only the relevant YAML files under `subagents/`.
4. Preserve legal review limits: all outputs are lawyer-review drafts; verify current legal facts and deadlines before reliance.
5. Produce the cookbook's intended artifact, such as a grid, tracker update, alert, digest, or memo, in the user's requested location or inline if no location is specified.
