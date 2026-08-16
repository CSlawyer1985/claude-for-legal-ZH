---
name: chinese-legal-launch-radar
description: "Use when the user needs a Chinese legal managed workflow for 产品上线雷达工作流: 产品上线列表、功能风险分类、上线法律风险雷达、产品发布合规摘要. This is a DeepSeek Harness (dsh) adapter for claude-for-legal-ZH/managed-agent-cookbooks/launch-radar."
---

# 产品上线雷达工作流 DeepSeek Harness Adapter

This skill ports the original managed-agent cookbook into a DeepSeek Harness (`dsh`) workflow.

## Source Files

- Cookbook root: `managed-agent-cookbooks/launch-radar`
- Read first: `managed-agent-cookbooks/launch-radar/README.md`
- Agent blueprint: `managed-agent-cookbooks/launch-radar/agent.yaml`
- Steering examples: `managed-agent-cookbooks/launch-radar/steering-examples.json`
- Subagent blueprints: `managed-agent-cookbooks/launch-radar/subagents`

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
