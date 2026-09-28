---
name: bid-review
description: 当用户要求审查采购/招标文件、响应文件、资格条件、评分规则或投标风险时使用；单纯寻找公告改用 notice-watch。
argument-hint: "[文件夹或公告链接、服务角色和阶段]"
---

# 采购文件与投标审查

先读领域 `CLAUDE.md`，用 `regime-triage` 的方法核定制度；用户已有有据可查的制度结论时直接复核其适用范围。建立文件清单和版本链，记录招标公告、澄清、附件、响应、资格证明与最终文件的页码/条款定位，原件只读。

按“法定准入—公告/文件自定条件—响应证明—评分条款—合同义务”逐项映射。重点查资格条件合法性与歧视性、实质响应、评审标准一致性、无效响应条件、报价算术及异常低价处理、澄清边界、保密与利益冲突。缺少证据填“待核”，不得自动记零分或合格；只有真实评分记录和适用规则齐备时才可复算，不模拟真实评委结果。

输出问题矩阵：`issue_id｜文件版本与定位｜条件/条款｜证据状态｜风险与法律依据｜建议动作｜责任人/时点｜核验状态`。另列最可能改变结果的前三项、反方解释和未覆盖文件。所有限额、评分规则和期限在本次任务按官方来源核验。

逐一检查 `task_context`、`jurisdiction`、`temporal`、`actors`、`matter`、`claims_and_elements`、`authority_and_interpretation`、`proof`、`procedure`、`outcomes_and_enforcement`、`strategy_and_uncertainty`、`governance`。本技能重点展开主体资格、要件、证据、程序及不确定性，其他模块仍记录状态、理由或阻塞路径。

## 作者与来源

- 作者：CSlawyer
- 主页：https://chenshi.ai
- 编制方法：legal-meta-skill；法律依据与项目规则均须在运行时复核。
