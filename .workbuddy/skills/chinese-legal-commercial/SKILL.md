---
name: chinese-legal-commercial
description: "商事合同领域法律工作：合同审查、NDA、供应商协议、SaaS/MSA、续约、合同利益方摘要、合同风险上报、商事法务。claude-for-legal-ZH/commercial-legal 的 WorkBuddy 路由技能，把自然语言请求路由到原领域 CLAUDE.md 与 skills/*/SKILL.md 工作流。"
---

# 商事合同 — claude-for-legal-ZH（WorkBuddy 适配）

本技能让 WorkBuddy 复用 `claude-for-legal-ZH/commercial-legal` 的原始内容，无需 Claude Code slash command。

## 源文件

- 领域根目录：`commercial-legal`
- 领域画像与共享规则：`commercial-legal/CLAUDE.md`
- 原始技能目录：`commercial-legal/skills`
- 原插件说明：依据供应商或采购方合同手册审查供应商协议、保密协议及SaaS订阅协议；自动追踪合同续约及终止期限，避免遗漏；将审批事项按规则路由至适当审批人；将法律审查结论转化为业务相关方能真正读懂的商业语言摘要。

## 路径解析

上述仓库相对路径以 `claude-for-legal-ZH` 仓库根目录为基准：

- 当前工作区包含本仓库时，直接按仓库根目录解析。
- 用户级安装后，先运行 `cat ~/.workbuddy/legal-zh/repo` 取得安装脚本登记的仓库绝对路径，再拼接相对路径。

## 使用方式

1. 处理实质法律工作前，先读取 `commercial-legal/CLAUDE.md`。
2. 从下方技能清单选择最接近的原始技能，读取其 `SKILL.md`。
3. 按该技能的工作流执行，把 Claude Code slash command 表述转写为 WorkBuddy 的文件、Shell、文档与自动化动作。
4. 多个原始技能同时适用时，按工作流隐含顺序依次执行并合并结果。
5. 不执行 Claude 专属插件命令，忽略 Claude hooks。本地文件、检索核验、文档渲染与用户可见输出均使用 WorkBuddy 工具完成。

## 配置兼容

原项目把实践画像存放在 `~/.claude/plugins/config/...`。WorkBuddy 中按以下顺序：

1. 已存在 Claude 画像时，直接读取作为现有执业画像。
2. 否则使用或创建 `~/.workbuddy/legal-zh/commercial-legal/CLAUDE.md` 保存 WorkBuddy 专用画像。
3. 所选技能要求初始化且画像仍含 `[PLACEHOLDER]` 时，先以对话方式完成该领域的 `cold-start-interview` 冷启动面试，再产出定制化法律工作。

原指令中的 `/commercial-legal:some-command` 应解释为：读取 `commercial-legal/skills/some-command/SKILL.md` 并在 WorkBuddy 中执行该工作流。

## 法律检索连接器

WorkBuddy 的 MCP 配置位于 `~/.workbuddy/mcp.json`（标准 `mcpServers` 格式）。已配置 `chineselaw` 或 `yuandian`（元典）等法律检索服务时（见 `INSTALL_WORKBUDDY.md`），优先用其核验法条、案例与监管动态；未配置时，时效性法律事实一律标注"需验证"。

## 可用原始技能

`amendment-history`、`cold-start-interview`、`customize`、`escalation-flagger`、`matter-workspace`、`nda-review`、`renewal-tracker`、`review`、`review-proposals`、`saas-msa-review`、`stakeholder-summary`、`vendor-agreement-review`

## 法律输出规则

- 所有输出均为律师审查草稿，不替代律师专业判断。
- 不确定的法条引用或案例参考须标注"需验证"，除非本次会话已从可靠来源核验。
- 法条、案例、监管动态、期限等时效性内容，依赖前必须用可靠来源核验。
- 保留原工作流的升级、审批、保密与来源标注要求。
