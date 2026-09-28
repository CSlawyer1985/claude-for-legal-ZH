---
name: regime-triage
description: 当用户需要判断项目适用政府采购法、招标投标法或其他采购制度，或要识别采购程序与审查职责时使用；已确定制度的单条合同修改不触发。
argument-hint: "[采购主体、资金、标的、阶段和地区]"
---

# 采购制度路由

先读领域 `CLAUDE.md`。建立输入卡：采购人法律地位、资金来源、项目/标的、预算或估算金额、实施地域、采购方式、公告时间、当前阶段、服务角色。缺少决定性字段时列候选制度及差异，不强选。

查询适用时点的法律、行政法规、部门规章、地方限额及项目公告原文；按主管机关、规范层级、适用对象和新旧法衔接逐项核对。输出“候选制度—适用要件—已知事实—待证事实—原文定位—核验状态”的矩阵，并给出程序入口与下一步材料清单。法律关系、资格、投诉路径和救济方式随制度分别展开。

对 `task_context`、`jurisdiction`、`temporal`、`actors`、`matter`、`claims_and_elements`、`authority_and_interpretation`、`proof`、`procedure`、`outcomes_and_enforcement`、`strategy_and_uncertainty`、`governance` 十二模块逐一判断。适用项给最低输出；不适用项给与本次制度路由有关的理由；阻塞项写缺口、补充路径和须停止的确定结论。四层区分原始文件、核实事实、制度评价和程序状态。

## 作者与来源

- 作者：CSlawyer
- 主页：https://chenshi.ai
- 编制方法：legal-meta-skill；法律依据与项目规则均须在运行时复核。
