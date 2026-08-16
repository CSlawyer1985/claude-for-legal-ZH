---
name: chinese-legal-renewal-watcher
description: "Use when the user needs a Chinese legal managed workflow for 合同续约监控工作流: 合同续约监控、自动续约、终止通知期限、续约提醒、合同台账读取. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/managed-agent-cookbooks/renewal-watcher."
---

# 合同续约监控工作流 DeepSeek Harness Adapter

This skill ports the original managed-agent cookbook into a DeepSeek Harness (`dsh`) workflow.

## Source Files

- Cookbook root: `managed-agent-cookbooks/renewal-watcher`
- Read first: `managed-agent-cookbooks/renewal-watcher/README.md`
- Agent blueprint: `managed-agent-cookbooks/renewal-watcher/agent.yaml`
- Steering examples: `managed-agent-cookbooks/renewal-watcher/steering-examples.json`
- Subagent blueprints: `managed-agent-cookbooks/renewal-watcher/subagents`

## Path Resolution

The repository-relative paths above resolve against the `claude-for-legal-ZH` repository root:

- If the current workspace contains the repository, resolve them against the repository root directly.
- Otherwise (user-level install), run `cat ~/.dsh/legal-zh/repo` once to get the absolute repository path recorded by `scripts/install-dsh.sh`, then prefix the relative paths with it.

## How To Use

1. Read the cookbook `README.md` and `agent.yaml` before running the workflow.
2. Translate Claude managed-agent concepts into dsh execution:
   - Use dsh filesystem tools for repositories, trackers, tables, and source documents.
   - Use the dsh subagent tool only if the user explicitly asks for parallel agents or the workflow itself is requested as a multi-agent run.
   - Use dsh jobs/schedules only when the user asks to monitor, remind, watch, or repeat the workflow over time.
3. If the cookbook references subagents, read only the relevant YAML files under `subagents/`.
4. Preserve legal review limits: all outputs are lawyer-review drafts; verify current legal facts and deadlines before reliance.
5. Produce the cookbook's intended artifact, such as a grid, tracker update, alert, digest, or memo, in the user's requested location or inline if no location is specified.
