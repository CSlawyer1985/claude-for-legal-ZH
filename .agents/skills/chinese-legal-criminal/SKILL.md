---
name: chinese-legal-criminal
description: 刑事法律与合规领域工作流适配器。负责加载刑事案件脱敏规则，并路由至具体的阅卷梳理、合规不起诉、取保候审及辩护分析技能。
---

# 刑事法律与合规工作流 (Criminal Legal Suite)

> **代理人指令 (Agent Instruction)**：
> 当用户的问题属于**中国刑事辩护、企业刑事合规、取保候审、涉刑案件风险审查**时，你已进入刑事领域。
> 你的首要任务是：
> 1. 读取并应用该领域的底层防线与指导原则：`criminal-legal/CLAUDE.md`。
> 2. 从 `criminal-legal/skills/` 目录下选择最适合用户需求的具体技能（例如 `case-analysis`, `compliance-non-prosecution`, `bail-application`, `defense-strategy`）。
> 3. 严格遵循该领域特有的**强制脱敏红线**与**防法律幻觉（强制数据库校验）**的要求，在最终输出时带上免责声明。
> 
> 请勿在本文件中寻找具体的业务执行步骤，一切规则皆在 `criminal-legal/CLAUDE.md` 及其对应的技能文件夹内。
