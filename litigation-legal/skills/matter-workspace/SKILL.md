---
name: matter-workspace
description: >
  为多客户执业场景管理案件工作空间——创建、列表、切换、关闭或脱离活跃案件。
  当用户需要创建新案件工作空间、切换活跃案件、列出案件、归档案件或
  仅在实务级工作而不关联特定案件时使用。
argument-hint: "<new | list | switch | close | none> [代号]"
---

# /matter-workspace

律师在多个客户和案件之间工作。案件工作空间将一个客户或委托的上下文与其他所有隔离开来。本命令管理这些工作空间。

## 子命令

- `/litigation-legal:matter-workspace new <代号>` —— 创建新案件工作空间，运行简要登记，写入 `matter.md`
- `/litigation-legal:matter-workspace list` —— 列出案件及其状态和活跃标记
- `/litigation-legal:matter-workspace switch <代号>` —— 设置活跃案件
- `/litigation-legal:matter-workspace close <代号>` —— 归档案件（移至 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/_archived/`，永不清除）
- `/litigation-legal:matter-workspace none` —— 脱离任何活跃案件，仅在实务级工作

注意：`/litigation-legal:matter-briefing [代号]`（无子命令）是单独的命令，生成特定案件的简报——适用于法务案件组合审查。案件工作空间管理在此。

## 指令

1. 读取 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` —— 确认 `## 案件工作空间` 部分已填充。如果 `Enabled` 为 `✗`，告知用户："案件工作空间已关闭——你配置为单一客户的法务实践，插件自动使用实务级上下文。如果你确实服务于多个客户，重新运行 `/litigation-legal:cold-start-interview --redo` 并选择外部执业设置。否则，你完全不需要 `/matter-workspace`。"不要报错——禁用状态是法务用户的预期状态。
2. 按以下工作流操作。
3. 按 `$ARGUMENTS` 的第一个 token 分发：
   - `new` → 运行登记访谈，写入 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/<代号>/matter.md`，播种 `history.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/*/matter.md`，打印表格，标记活跃案件。
   - `switch` → 更新实务级 CLAUDE.md 中的 `Active matter:` 行。
   - `close` → 将 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/<代号>/` 移至 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/_archived/<代号>/`，在 `history.md` 中记录关闭日期。
   - `none` → 设置 `Active matter:` 为 `none — 仅实务级上下文`。
4. 展示变更内容并在写入前确认。

## 备注

- 除非实务级 CLAUDE.md 中 `Cross-matter context` 为 `on`，否则本技能绝不跨案件读取。
- 归档不是删除——已关闭案件保持可读，供保存/冲突检索目的。
- 代号为小写连字符格式。如代号在已归档和活跃之间重复使用，已归档的保留在 `_archived/<代号>/` 下。

---

# 案件工作空间

多客户执业者（外部执业——独立、小所、大所）在多个案件之间工作。一个案件的上下文不得泄露入另一个。本技能是使之成立的薄文件管理层。

**默认状态为关闭。** 法务用户永远看不到此——他们仅运行在实务级。案件工作空间在首次配置时对外部执业用户开启，或通过编辑实务级 CLAUDE.md 中的 `## 案件工作空间` 开启。如果 `Enabled` 为 `✗`，本技能不运行；`/matter-workspace` 技能解释禁用状态并建议需要案件隔离的用户运行 `/cold-start-interview --redo`。

## 存储布局

所有案件数据存放在：

```
~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/
├── CLAUDE.md                       # 实务级实践画像
└── matters/
    ├── <代号>/
    │   ├── matter.md               # 客户、对方、案件类型、关键事实、覆盖项
    │   ├── history.md              # 带日期的事件、决定、草稿、审查日志
    │   └── outputs/                # 本案技能输出（可选子文件夹）
    └── _archived/
        └── <代号>/                 # 已关闭案件——可读但非活跃
```

代号为小写连字符格式。示例：`acme-msa-2026`、`zenith-renewal`、`vendor-xyz-nda`。

## 活跃案件在实务 CLAUDE.md 中

实务级 CLAUDE.md 中 `## 案件工作空间` 下的 `Active matter:` 行是唯一真实来源。切换案件即编辑该行。没有独立的状态文件。

## 子命令逻辑

### `new <代号>`

1. 确认代号在 `matters/<代号>/` 或 `matters/_archived/<代号>/` 中不存在。如重复，请用户选择不同代号。
2. 运行登记访谈：
   - **委托人**（我们代表的当事人，或法务场景下的内部业务部门）
   - **对方当事人**（另一方——可能多个）
   - **案件类型**（读取插件实践画像中的典型类别；对 litigation-legal：合同纠纷 | 劳动争议 | 知识产权 | 行政监管/调查 | 产品责任 | 其他）
   - **保密级别**（标准 | 加强 | 清洁团队——加强提示跨案件设置中额外注意）
   - **关键事实**（2-5句话：本案是什么、相关方是谁、涉及什么利益）
   - **案件特定对实务手册的覆盖**（如"客户要求责任上限24个月而非事务所标准12个月"、"对方是战略合作伙伴——保持关系保护语调"）
   - **关联案件**（任何有关联案件的代号）
3. 使用以下模板写入 `matters/<代号>/matter.md`。
4. 播种 `matters/<代号>/history.md`，含一条"立案/登记"条目。
5. **不**自动切换到新案件。询问："是否要现在切换到 `<代号>`？（`/litigation-legal:matter-workspace switch <代号>`）"

### `list`

枚举 `matters/*/matter.md`。读取每个文件的前几行提取状态。打印表格：

| 代号 | 委托人 | 案件类型 | 状态 | 立案日期 | 活跃 |
|---|---|---|---|---|---|

用 `*` 标记当前活跃案件。如有归档案件，在单独的"已归档"标题下包含 `_archived/*`。

### `switch <代号>`

1. 确认 `matters/<代号>/matter.md` 存在。如否，提供 `/litigation-legal:matter-workspace new <代号>`。
2. 编辑实务级 CLAUDE.md 中的 `Active matter:` 行为 `Active matter: <代号>`。
3. 向用户展示 matter.md 摘要以便确认在正确的案件上。

### `close <代号>`

1. 确认 `matters/<代号>/` 存在。
2. 向 `matters/<代号>/history.md` 追加一条"已关闭"条目，日期为今天。
3. 移动 `matters/<代号>/` → `matters/_archived/<代号>/`。
4. 如已关闭案件是活跃案件，设置 `Active matter:` 为 `none — 仅实务级上下文`。

### `none`

设置实务级 CLAUDE.md 中的 `Active matter:` 为 `none — 仅实务级上下文`。与用户确认。

## `matter.md` 模板

```markdown
[工作成果标头——根据插件配置 ## 输出——因角色不同；见实务级 CLAUDE.md 中的 `## 使用者`]

# 案件：[委托人] —— [简要描述]

**代号：** [slug]
**立案/登记日期：** [YYYY-MM-DD]
**状态：** active
**保密级别：** [标准 / 加强 / 清洁团队]

---

## 当事人

**委托人：** [名称]
**对方当事人：** [名称]

## 案件类型

[合同纠纷 | 劳动争议 | 知识产权 | 行政监管/调查 | 其他 —— 附一句理由]

## 关键事实

[2-5句话。本案是什么。相关方是谁。涉及什么利益。与默认手册有何不同。]

## 案件特定覆盖项

*适用于本案且仅适用于本案的、相对实务级手册的偏离。*

- [如"责任上限：客户要求24个月，非事务所标准12个月。"]
- [如"语调：保持关系保护——对方是战略合作伙伴。"]

## 关联案件

- [代号 —— 一行说明关联原因]
```

## `history.md` 播种

```markdown
# 历史记录：[委托人] —— [简要描述]

仅追加的事件日志。最新记录在最前。

---

## [YYYY-MM-DD] —— 案件立案/登记

登记完成。代号：`[slug]`。状态：active。
[任何 worth 保留的、超出 matter.md 的初始上下文——如"应对方发来的合同草案而立案"。]
```

## 跨案件上下文

实务级 CLAUDE.md 有 `Cross-matter context:` 标记。当它为 `off`（默认）时，在案 A 中工作的技能**绝不**读取 `matters/B/` 中的文件（对任何其他 B）。不容例外。这是该设置为存在的保密保证。

当它为 `on` 时，技能仅在用户明确要求时才能跨案件文件夹读取文件（如"比较我们最近五个案件在责任上限条款上的立场"）。即使 `on`，默认也仅加载活跃案件，除非用户要求跨案件视图。

## 本技能不做什么

- **运行利益冲突检索。** 冲突检索是执业者/事务所的工作；登记仅捕获用户声明的内容。
- **执行保存期限。** 关闭即将案件归档；不删除。保存政策超出范围。
- **自动路由输出。** 实质性技能决定写入何处；本技能告诉它*哪个文件夹*是活跃的，而非放入什么。
- **决定跨案件是否合适。** 读取标记并遵从。
