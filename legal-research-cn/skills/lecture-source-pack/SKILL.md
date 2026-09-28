---
name: lecture-source-pack
description: 当用户准备中国法律主题讲座、培训或公开分享，需建立来源包、案例清单和讲述提纲时使用；单个法条核对改用 authority-check。
argument-hint: "[主题、听众、时长、讲座日期和地区]"
---

# 法律讲座来源包

先读领域 `CLAUDE.md` 和目标工作区规则，明确听众、时长、目的、地区、拟讲日期与是否公开传播。保留用户已有的主题、议程和文案；个人实务案例须先取得使用授权并脱敏，不能把案卷发送到商业 MCP。

1. 将主题拆为听众必须理解的法律问题、常见误区、示例与可执行动作，建立主张清单。每项重要主张连接原始法源或已核实案例；记录版本、生效日和讲座日期的关系。
2. 用 `authority-check` 方法核验法条，用 `case-comparison` 方法核验案例身份、状态与适用差异。政策解读与法律义务分开；未决草案、征求意见稿及商业数据库摘要显著标注，不写成现行法。
3. 输出讲述提纲、来源台账、案例/示例使用状态、幻灯片建议、问答备选和讲前复核表。讲座日期前复查可能变化的法规与监管口径；无法核验的事实或数字从公开版删除或显著保留。
4. 公开发布、发送讲义、使用客户或第三方素材须另有授权；本技能只制作可供讲者审核的材料。

逐项检查 `task_context`、`jurisdiction`、`temporal`、`actors`、`matter`、`claims_and_elements`、`authority_and_interpretation`、`proof`、`procedure`、`outcomes_and_enforcement`、`strategy_and_uncertainty`、`governance`；与主题无关的模块说明理由，时效或案例授权受阻时暂停对应内容。

## 作者与来源

- 作者：CSlawyer
- 主页：https://chenshi.ai
- 编制方法：legal-meta-skill；讲座内容须在交付及公开前复核。
