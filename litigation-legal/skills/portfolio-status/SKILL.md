---
name: portfolio-status
description: >
  从 _log.yaml 汇总案件组合——风险分布、即将到期的节点、
  陈旧案件、重要性汇总、阶段分布和异常标注。
  当用户问"案件总体情况如何"、"有多少个未结案件"或需要案件组合汇总时使用。
argument-hint: "[--all | --risk=high | --stale]"
---

# /portfolio-status

1. 加载 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` → 风险校准（定义如何解读 `risk:` 字段）。
2. 按以下工作流操作。
3. 解析 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/_log.yaml`。默认过滤已结案件（使用 `--all` 包含）。
4. 生成汇总：风险分布、未来 14/30/60 天内到期节点、超过30天未更新案件、重要性汇总、阶段分布。
5. 标注异常——所有标记为危急、`next_deadline` 已逾期、风险为中或高但未指定外聘律师的案件。

---

# 案件组合状态

## 目的

一次阅读回答：我手上有多少案件、什么需要关注、什么在滑落？输出适合速览——为在下个电话前只有三分钟的律师设计。

## 加载上下文

- `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/_log.yaml` —— 真实来源
- `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` —— 风险校准（正确解读风险/重要性字段）

## 标记与过滤

默认：仅活跃案件（排除 `status: closed`）。

标记：
- `--all` —— 包含已结案件
- `--risk=high`（或 `critical` / `medium` / `low`）—— 按风险级别过滤
- `--stale` —— 仅 `last_updated` > 30天的案件
- `--type=employment` —— 按案件类别过滤
- `--owner=[姓名]` —— 按业务/HR/公关负责人过滤

## 汇总

```markdown
[工作成果标头——根据插件配置 ## 输出——因角色不同；见 `## 使用者`]

# 案件组合状态 —— [今天]

**活跃案件：** [N]
**已结（本年度）：** [N] *(仅使用 --all 时显示)*

---

## 按风险

| 风险 | 数量 | 案件 |
|---|---|---|
| 危急 | [N] | [代号] |
| 高 | [N] | [代号] |
| 中 | [N] | [仅数量——使用 `--risk=medium` 展开] |
| 低 | [N] | [仅数量] |

## 即将到期节点

| 期限内 | 案件 |
|---|---|
| 14天 | [代号 —— 节点 —— 简述] |
| 15–30天 | [...] |
| 31–60天 | [...] |

*逾期的 `next_deadline` 在下方单独标注。*

## 重要性

| 类别 | 数量 | 敞口合计（中位值） |
|---|---|---|
| 需计提 | [N] | [金额] |
| 已披露 | [N] | [金额] |
| 监控中 | [N] | — |
| 不适用 | [N] | — |

## 按阶段

[表格：起诉/答辩 / 证据交换 / 庭审 / 和解 / 上诉]

---

## 异常与标注

- **逾期节点：** [列出 next_deadline 已过的代号]
- **陈旧（>30天未更新）：** [列表]
- **利益冲突未解决：** [列出 conflicts.status 为 pending 或 not-run 的代号]
- **利益冲突已绕过（override 有效）：** [列出 conflicts.override.by 已填充的代号——在手动清除前永久标注]
- **高/危急风险但无外聘律师：** [列表]
- **已计提但 >60天未更新：** [列表] —— 计提重新校准可能已逾期
- **活跃诉讼中未发出证据保全：** [列表]
- **缺失字段：** [代号 → 字段]
```

## 异常规则

这些检查使本技能有用而非装饰性：

1. **逾期节点：** `next_deadline < 今天` 且 `status != closed`
2. **陈旧：** `last_updated < 今天 - 30天` 且 `status != closed`
3. **利益冲突未解决：** `conflicts.status in [pending, not-run]` 且 `status != closed`
3b. **利益冲突绕过有效：** `conflicts.override.by != null`（永不自清除）
4. **高风险无覆盖：** `risk in [high, critical]` 且 `outside_counsel.firm == null`
5. **计提陈旧：** `materiality == reserved` 且 `last_updated < 今天 - 60天`
6. **证据保全缺口：** 活跃案件且 `legal_hold.issued == false` —— 保全义务在合理预期诉讼时即附着
7. **缺失字段：** 任何必填字段为空——`risk`、`materiality`、`status`、`opened`、`conflicts.status`

## 以下一步决策树收尾

以 CLAUDE.md `## 输出` 中的下一步决策树收尾。根据本技能刚产生的内容自定义选项——五个默认分支（起草X、上报、获取更多事实、观察等待、其他选择）是起点而非锁定项。决策树本身就是输出；由律师选择。

如案件组合超过约10个案件，或在用户任何要求时：提出仪表板方案（见 CLAUDE.md `## 输出 → 数据密集输出的仪表板提议`）。为此输出定制提议——按风险级别计数、即将到期节点的时间线、及带状态、冲突检查和最后触及日期的可排序案件台账。

## 本技能不做什么

- 做出决定。浮现需要关注的事项；用户决定优先级。
- 假装拥有不存在的精度。敞口中位值是粗略估计，应如此标注。
- 替代真实的案件管理系统。这是工作记忆汇总，不是记录系统。
