---
name: legal-service-proposal
description: 当律师需要起草或核对中国法律服务洽商方案、服务范围和报价结构时使用；一般合同价款审查改用商事或采购合同技能。
argument-hint: "[客户需求、事项类型、服务范围与团队约束]"
---

# 法律服务方案与报价

先读 `law-practice-cn/CLAUDE.md`、仓库 `references/pricing-proposal-framework.md` 和目标工作区规则。确认客户、服务角色、利益冲突、事项性质、决策人、交付物、时限、团队与内部审批边界。客户预算、竞争报价和历史费率只能使用已授权的本地材料，不向外部 MCP 发送。

1. 把需求拆为核心服务、可选服务、明确排除项、客户配合事项和阶段性交付。把尚需尽调或法律研究才能确定的工作量列为报价假设，不能暗示承诺结果。
2. 按事项类型列固定、计时、分阶段等候选收费结构；风险代理只作为需另行核查的候选，先核对现行法律、地方规则、律所政策和事项禁限，不凭共享参考表直接推荐。市场价格须有本次可核验来源，否则不填写虚构区间。
3. 建可复算底稿：任务、人员、工时或计价基础、税费与第三方费用、范围变更触发、确认程序。检查小计与总价、付款节点、逾期与终止安排一致。
4. 输出客户版方案草稿和内部版假设/风险/审批清单。客户版清楚写范围、团队、成果、时间、费用、排除及变更机制；在授权前不发送、不签署、不提交报价。

逐项检查 `task_context`、`jurisdiction`、`temporal`、`actors`、`matter`、`claims_and_elements`、`authority_and_interpretation`、`proof`、`procedure`、`outcomes_and_enforcement`、`strategy_and_uncertainty`、`governance`；与报价无关的模块说明理由，收费合规与事实缺口受阻时停止确定报价。

## 作者与来源

- 作者：CSlawyer
- 主页：https://chenshi.ai
- 编制方法：legal-meta-skill；收费规则和市场数据须在运行时核验。
