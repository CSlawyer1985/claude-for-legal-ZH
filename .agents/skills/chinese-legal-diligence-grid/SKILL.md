---
name: chinese-legal-diligence-grid
description: Use when the user needs a Chinese legal managed workflow for 尽调问题表格工作流: 并购尽调材料读取、问题抽取、尽调表格、披露问题清单、法律尽调多文档归一化. This is a Codex adapter for claude-for-legal-ZH/managed-agent-cookbooks/diligence-grid.
---

# 尽调问题表格工作流 Codex Adapter

This skill ports the original managed-agent cookbook into Codex workflow form.

## Source Files

- Cookbook root: `managed-agent-cookbooks/diligence-grid`
- Read first: `managed-agent-cookbooks/diligence-grid/README.md`
- Agent blueprint: `managed-agent-cookbooks/diligence-grid/agent.yaml`
- Steering examples: `managed-agent-cookbooks/diligence-grid/steering-examples.json`
- Subagent blueprints: `managed-agent-cookbooks/diligence-grid/subagents`

## How To Use

1. Read the cookbook `README.md` and `agent.yaml` before running the workflow.
2. Translate Claude managed-agent concepts into Codex execution:
   - Use local file reads/writes for repositories, trackers, tables, and source documents.
   - Use Codex subagents only if the user explicitly asks for parallel agents or the workflow itself is requested as a multi-agent run.
   - Use Codex automations only when the user asks to monitor, remind, watch, or repeat the workflow over time.
3. If the cookbook references subagents, read only the relevant YAML files under `subagents/`.
4. Preserve legal review limits: all outputs are lawyer-review drafts; verify current legal facts and deadlines before reliance.
5. Produce the cookbook's intended artifact, such as a grid, tracker update, alert, digest, or memo, in the user's requested location or inline if no location is specified.
