---
name: case-comparison
description: 当用户要求中国法院类案检索、指导性案例或参考案例比较、裁判分歧分析时使用；只有案号格式校对时改用 authority-check。
argument-hint: "[争点、法院、时间与待比较事实]"
---

# 类案对比

先读领域 `CLAUDE.md`，确定研究争点、法律关系、地域、审级、事实时点与拟用论点。敏感案件事实先在本地抽象成检索词；未经授权不把案卷或身份信息送往 MCP。

1. 用精确争点、法条、案由、法院、关键词及反向词检索；区分人民法院案例库、原始裁判文书、商业数据库和评论文章。记录检索式、日期、结果数及排除理由。
2. 对每个拟引用案例读取可用全文，核对案号、法院、审级、生效/再审状态、关键事实、争点、裁判理由和不利段落。仅有摘要的案例标为“线索”。
3. 比较“共同要件事实、关键差异、程序差异、规范版本差异、对本案有利/不利之处”。不得只按关键词相同认定类案。
4. 输出案例矩阵：`case_id｜来源与定位｜身份及状态｜事实/争点｜规则与引用姿态｜可比性｜不利内容｜核验状态`，并给出相反案例或检索缺口。
5. 对未能确认生效状态、全文或规范时点的案例，不写成确定裁判趋势；保留人工复核事项。

逐一检查 `task_context`、`jurisdiction`、`temporal`、`actors`、`matter`、`claims_and_elements`、`authority_and_interpretation`、`proof`、`procedure`、`outcomes_and_enforcement`、`strategy_and_uncertainty`、`governance`。本技能尤其展开时间、请求要件、法源、证据、程序与人工复核；其他模块仍记录适用、不适用理由或阻塞缺口。

## 作者与来源

- 作者：CSlawyer
- 主页：https://chenshi.ai
- 编制方法：legal-meta-skill；法律依据与项目规则均须在运行时复核。
