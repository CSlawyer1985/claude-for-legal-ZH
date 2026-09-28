---
name: complaint-triage
description: 当用户需要处理非政府采购的一般投诉、举报、申诉或其答复，需判断受理机关、程序、证据和期限时使用；政府采购质疑投诉改用 procurement-legal 的 challenge-complaint。
argument-hint: "[投诉对象、事项、身份、收到或知悉日期]"
---

# 投诉与举报程序分流

先读 `law-practice-cn/CLAUDE.md` 和目标工作区规则，确认我方是投诉人、被投诉人还是处理机关，区分投诉、举报、申诉、行政复议、诉讼和民事协商。政府采购质疑投诉路由 `procurement-legal/skills/challenge-complaint/SKILL.md`；不得将其前置程序套到其他渠道。

1. 建材料台账：事项发生与知悉日期、文书版本、送达凭证、证据来源、既有沟通和已启动程序。把当事人陈述、可核事实、争议事实、法律评价分开。
2. 按事项、地域、主管职责和服务角色筛选候选渠道；逐一核对受理条件、前置步骤、管辖、重复处理、保密及个人信息要求。渠道无法确认时先列候选，不写确定受理机关。
3. 期限只在起算事实、送达证据与适用时点的官方规则都核实时计算。缺任一项则输出候选窗口及需立即核对的材料，不断言已逾期或可受理。
4. 输出程序分流表、争点证据矩阵、相反解释、处理选项、候选期限底稿和文书草稿。若处理对象为被投诉人，逐项回应而非仅写否认。提交、发送、公开或联系他人须用户明确授权。

逐项检查 `task_context`、`jurisdiction`、`temporal`、`actors`、`matter`、`claims_and_elements`、`authority_and_interpretation`、`proof`、`procedure`、`outcomes_and_enforcement`、`strategy_and_uncertainty`、`governance`；受理机关、证据或时点受阻时停止对应确定性程序判断。

## 作者与来源

- 作者：CSlawyer
- 主页：https://chenshi.ai
- 编制方法：legal-meta-skill；投诉渠道与期限须在运行时核验。
