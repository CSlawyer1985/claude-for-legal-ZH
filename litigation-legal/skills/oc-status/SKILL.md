---
name: oc-status
description: >
  为活跃案件组合中的各外聘律师生成每周状态请求邮件草稿——
  每案一份 markdown。当用户要求向外聘律师发状态请求、
  每周外聘律师检查或需要从案件组合日志中起草各案状态邮件时使用。
argument-hint: "[--all | --slug=foo | --no-gmail]"
---

# /oc-status

如需每周运行，设置定期提醒调用 `/litigation-legal:oc-status`。

1. 加载 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/_log.yaml`，按默认规则（或标记）过滤。
2. 加载 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` → 外聘律师沟通风格、签署人默认、预算姿态。
3. 按以下工作流操作。
4. 对范围内的每个案件：读取 `matter.md` + `history.md`，起草各案邮件。
5. 将 markdown 写入 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/oc-status/[YYYY-MM-DD]/[slug].md`。
6. 写入 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/oc-status/[YYYY-MM-DD]/_summary.md` —— 运行了什么、跳过了什么及其原因。

---

# 外聘律师状态

## 目的

每周向 5-15 个案件的外聘律师写同样的状态请求邮件是机械性的认知负担。内容因案而异（状态、待决定事项、预算检查）。受众一致（外聘主办律师）。语气一致（按事务所外聘律师沟通风格）。由技能起草全部邮件；律师审查并发送。

## 加载上下文

- `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/_log.yaml` —— 过滤和字段来源
- `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/[slug]/matter.md` —— 案件上下文（当前姿态、待解决问题）
- `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/[slug]/history.md` —— 近期事件，为询问什么提供信息
- `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` → 外聘律师沟通风格、签署人姓名/邮箱、预算姿态

## 过滤——哪些案件？

默认过滤：

- `status != closed`
- `outside_counsel.firm != null` AND `outside_counsel.lead != null`
- 满足以下之一：上次更新超过10天（可能有新进展）或 `next_deadline` 在21天以内

跳过刚在10天内更新的案件（无需再次催促）和 `outside_counsel.email` 为空的案件（无法发送邮件；仍生成 markdown）。

标记：
- `--all` → 为所有活跃案件起草，不论最近更新时间
- `--slug=[代号]` → 仅为一个案件起草（临时请求）
- `--no-gmail` → 不创建邮件草稿

## 各案邮件草案

每封邮件使用相同骨架；内容因案而异。

**主题：** 按事务所惯例（来自 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 外聘律师沟通风格；备用格式：`[案：[案件名称]] —— 案件进展询问`）

**正文骨架：**

```
[主办律师姓氏]律师，您好：

[一句话开场——自然，匹配事务所语调。]

关于[案件名称]，向您确认以下事项：

1. **自[history.md 最后更新日期]以来的进展** —— 有哪些推进？待定事项是什么？近期是否有起诉/答辩、开庭、往来函件或通话？

2. **即将到来的节点** —— 日志中显示 [next_deadline + matter.md 中的任何日期节点]。请确认应对方案及我们是否需要补充任何日期。

3. **待决定事项** —— [从 matter.md 中提取需要外聘律师意见的待解决问题；如无，省略本项并重新编号]

4. **预算** —— [按月/季度/按需，取决于 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 预算姿态]。目前相对 [matter.md 中的预算授权] 的使用情况如何？是否有需要标注的偏差？

[如重要且相关：5. 具体要求 —— 如"请在[日期]前将起诉状/答辩状最新稿发我"——从 matter.md 待解决问题中提取。]

[署名——姓名、职务、联系方式。来自 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 外聘律师沟通的签署人默认设置。]
```

根据 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 外聘律师沟通风格调整语气——有些事务所是"尊敬的律师"正式风格；另一些是直呼其名加要点列表。匹配。

## 输出

### Markdown 草稿

写入至：`~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/oc-status/[YYYY-MM-DD]/[slug].md`

每份文件为一封邮件，格式如下：

```markdown
[工作成果标头——根据插件配置 ## 输出——因角色不同；见 `## 使用者`]

# [案件名称] —— 外聘律师状态请求 —— [YYYY-MM-DD]

**收件人：** [日志中的 outside_counsel.email]（[outside_counsel.lead]，[outside_counsel.firm]）
**发件人：** [签署人姓名/邮箱，来自 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md`]
**主题：** [主题行]

> 上述工作成果标头适用于本内部记录。下方发出的邮件正文发送给委托案件的外聘律师，邮件本身属于保密通信——请在发送邮件顶部标注保密标记，通常为"保密 · 受律师-客户特权保护 —— 律师工作成果"，而非此内部工作成果标头。

---

[按骨架的正文]
```

### 发送门禁（每份草稿的收尾注释）

在每份 markdown 草稿底部、正文下方附加以下内容——发送前删除：

> 这是发送给外聘律师前的状态邮件草稿，供律师审查。请检查：是否包含您不打算在委托圈外分享的保密内容、事实准确性、语气和预算姿态。不要未经审查就发送——即使是常规的每周检查也可能暴露发送方无意书面化的理论、策略或让步。

### 运行摘要

处理完所有案件后，写入 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/oc-status/[YYYY-MM-DD]/_summary.md`：

```markdown
# 外聘律师状态运行 —— [YYYY-MM-DD]

**处理案件数：** [N]
**草稿创建数：** [N]

## 已起草

| 案件 | 外聘主办律师 | 最后更新 | 纳入原因 |
|---|---|---|---|
| [代号] | [主办] | [日期] | [陈旧 / 即将到期节点 / --all / --slug] |

## 已跳过

| 案件 | 原因 |
|---|---|
| [代号] | 近期已更新（最后触及 [日期]） |
| [代号] | 日志中无外聘律师邮箱——请通过 `/matter-update [代号]` 更新 |
```

## 本技能不做什么

- **发送邮件。** 仅生成草稿。律师审查并发送。
- **生成没有的内容。** 如果 `matter.md` 内容薄，邮件就短且询问宽泛的状态问题。本技能不从无到有发明具体问题。
- **重写 history.md。** 读取以获取上下文；不修改。（如外聘律师的回复浮现新事件，使用 `/matter-update [slug]` 记录。）
- **强制执行最低模板。** 如果事务所语气是"一句话，直呼其名，完事"，草稿尊重此风格并跳过要点结构。匹配 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md`。
