---
name: chinese-legal-renewal-watcher
description: "合同续约监控工作流：合同续约监控、自动续约、终止通知期限、续约提醒、合同台账读取。claude-for-legal-ZH/managed-agent-cookbooks/renewal-watcher 的 WorkBuddy 路由技能。"
---

# 合同续约监控工作流 — claude-for-legal-ZH（WorkBuddy 适配）

本技能把原托管 Agent cookbook 转写为 WorkBuddy 工作流。

## 源文件

- Cookbook 根目录：`managed-agent-cookbooks/renewal-watcher`
- 先读：`managed-agent-cookbooks/renewal-watcher/README.md`
- Agent 蓝图：`managed-agent-cookbooks/renewal-watcher/agent.yaml`
- 引导示例：`managed-agent-cookbooks/renewal-watcher/steering-examples.json`
- 子 Agent 蓝图：`managed-agent-cookbooks/renewal-watcher/subagents`

## 路径解析

上述仓库相对路径以 `claude-for-legal-ZH` 仓库根目录为基准：

- 当前工作区包含本仓库时，直接按仓库根目录解析。
- 用户级安装后，先运行 `cat ~/.workbuddy/legal-zh/repo` 取得安装脚本登记的仓库绝对路径，再拼接相对路径。

## 使用方式

1. 运行工作流前，先读 cookbook 的 `README.md` 与 `agent.yaml`。
2. 把 Claude 托管 Agent 概念转写为 WorkBuddy 执行：
   - 台账、表格、源文档读写使用 WorkBuddy 本地文件工具。
   - 仅在用户明确要求并行 agent 或多 agent 运行时，才使用 WorkBuddy 的多任务并行。
   - 仅在用户要求监控、提醒、看守或周期重复时，才使用 WorkBuddy 的定时自动化。
3. cookbook 引用子 agent 时，只读取 `subagents/` 下相关的 YAML 文件。
4. 保留法律审查边界：所有产出均为律师审查草稿，时效性法律事实与期限依赖前必须核验。
5. 产出 cookbook 预期的交付物（表格、台账更新、预警、摘要或备忘录），位置按用户指定；未指定时对话内输出。
