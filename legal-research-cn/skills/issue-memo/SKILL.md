---
name: issue-memo
description: 当用户要就中国法争点形成可追溯研究备忘录、相反观点与行动建议时使用；单个法条真伪核对改用 authority-check。
argument-hint: "[问题、角色、事实时点与用途]"
---

# 争点研究备忘录

先读领域 `CLAUDE.md`，确认代表谁、为谁决策、法律时点和备忘录用途。把开放问题拆成“法律关系—请求/抗辩—要件—待证事实—来源”问题树，列出未经证实的假设。

按争点进行三轮检索：精确依据、同义/上下位补漏、相反观点与冲突；记录每轮工具、日期、检索式和来源 ID。关键规范交 `authority-check` 的核验方法处理，类案交 `case-comparison` 的比较方法处理；无需为形式调用另一个 Skill。官方原文与商业数据库摘要分层。

输出先写条件化结论，再按每个争点列：已知/待证事实、适用规则与效力、构成要件、证据与举证责任、对方最强论点、法律上成立与实际可执行的差别、程序与期限、风险和下一步。末尾附来源台账、未覆盖项、核验日期、律师复核清单。关键依据缺失时停止对应确定结论，不用模型记忆填空。

用 `task_context`、`jurisdiction`、`temporal`、`actors`、`matter`、`claims_and_elements`、`authority_and_interpretation`、`proof`、`procedure`、`outcomes_and_enforcement`、`strategy_and_uncertainty`、`governance` 十二模块状态表逐项标为适用、不适用或受阻，给出最低输出、具体理由或缺口与降级路径。材料、事实、法律评价与程序状态四层分开。

## 作者与来源

- 作者：CSlawyer
- 主页：https://chenshi.ai
- 编制方法：legal-meta-skill；法律依据与项目规则均须在运行时复核。
