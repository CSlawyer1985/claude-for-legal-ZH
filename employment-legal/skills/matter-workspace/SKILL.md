---
name: matter-workspace
description: >
  管理案件工作空间——新建、列表、切换、关闭或解除（实务级）。
  创建、列举、切换、关闭和解除活跃案件，使一个客户委托的上下文
  绝不泄露到另一个。当多客户执业者说"新案件"、"切换案件"、
  "列出我的案件"、"关闭此案件"或需要管理哪个案件活跃时使用。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

执业者跨多个客户和案件工作。案件工作空间使一个客户或委托的上下文与其他每个分开。本技能管理这些工作空间。

## 子命令

- `/employment-legal:matter-workspace new <slug>` —— 创建新案件工作空间，运行简短立案登记，写入 `matter.md`
- `/employment-legal:matter-workspace list` —— 列举案件及其状态和活跃标记
- `/employment-legal:matter-workspace switch <slug>` —— 设置活跃案件
- `/employment-legal:matter-workspace close <slug>` —— 归档案件（移至 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/matters/_archived/`，永不删除）
- `/employment-legal:matter-workspace none` —— 解除任何活跃案件，仅在实务级工作

## 指令

1. 读取 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/CLAUDE.md`——确认 `## Matter workspaces` 部分已填充。如果 `Enabled` 为 `✗`，告诉用户："案件工作空间已关闭——你配置为法务单一客户模式，插件自动从实务级上下文运行。如果你实际跨多个客户工作，重新运行 `/employment-legal:cold-start-interview --redo` 并选择私人执业设置。否则你根本不需要 `/matter-workspace`。"不要报错——禁用状态是法务用户的预期状态。
2. 使用以下子命令逻辑。
3. 根据首个匹配的指令分发：
   - `new` → 运行立案访谈，写入 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/matters/<slug>/matter.md`，生成 `history.md` 和 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/matters/*/matter.md`，打印表格，标记活跃案件。
   - `switch` → 更新实务级 CLAUDE.md 中的 `Active matter:` 行。
   - `close` → 将 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/matters/<slug>/` 移至 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/matters/_archived/<slug>/`，在 `history.md` 中记录关闭日期。
   - `none` → 将 `Active matter:` 设置为 `none — 仅实务级上下文`。
4. 向用户显示变更内容并在写入前确认。

## 备注

- 本技能绝不跨案件读取，除非实务级 CLAUDE.md 中 `Cross-matter context` 为 `on`。
- 归档不是删除——已关闭案件保持可读，用于保存记录/利益冲突检索目的。
- slug 使用小写加连字符。如果 slug 在归档和活跃中重复使用，归档的保留在 `_archived/<slug>/` 下。

---

## 参考

多客户执业者（私人执业——独立执业、小型律所、大型律所）跨多个案件工作。一个案件的上下文不得泄露到另一个。本技能是确保这一点的薄文件管理层。

**默认状态为关闭。** 法务用户从不看到此——他们仅在实务级运行。案件工作空间在 cold-start 时为私人执业用户开启，或通过编辑实务级 CLAUDE.md 中的 `## Matter workspaces` 开启。如果 `Enabled` 为 `✗`，本技能不运行；相反它解释禁用状态，并为实际需要案件隔离的用户建议 `/employment-legal:cold-start-interview --redo`。

## 存储布局

所有案件数据位于：

```
~/.claude/plugins/config/claude-for-legal-zh/employment-legal/
├── CLAUDE.md                       # 实务级实践画像
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、对方当事人、案件类型、关键事实、覆盖项
    │   ├── history.md              # 事件、决定、草案、审查的日期日志
    │   ├── notes.md                # 自由形式工作笔记
    │   └── outputs/                # 本案的技能输出（可选子文件夹）
    └── _archived/
        └── <slug>/                 # 已关闭案件——可读但不活跃
```

slug 使用小写加连字符。示例：`acme-劳动合同争议-2026`、`zenith-竞业限制审查`、`供应商-xyz-保密协议`。

## 活跃案件在实务级 CLAUDE.md 中

实务级 CLAUDE.md 中 `## Matter workspaces` 下的 `Active matter:` 行是唯一真相来源。切换案件编辑该行。没有单独的状态文件。

## 子命令逻辑

### `new <slug>`

1. 确认 slug 不存在于 `matters/<slug>/` 或 `matters/_archived/<slug>/`。如果重复使用，要求用户选择不同的 slug。
2. 运行立案访谈：
   - **委托人**（我们代表的当事方，或法务对应的内部业务单位）
   - **对方当事人**（另一方——可能有多个）
   - **案件类型**（读取插件的实践画像获取典型类别；对于 employment-legal：录用 | 解除 | 调查 | 假期 | 劳动关系认定 | 跨地域用工 | 制度项目 | 其他）
   - **保密级别**（标准 | 加强 | 洁净团队——加强提示跨案件设置中的额外注意）
   - **关键事实**（2-5句话：本案是关于什么的，利益相关者是谁，利害关系在哪）
   - **对实务实践的个案特定覆盖项**（例如"客户要求竞业限制期限上限24个月而非12个月"、"对方当事人是战略合作伙伴——关系维护语气"）
   - **关联案件**（任何关联案件的 slug）
3. 使用以下模板写入 `matters/<slug>/matter.md`。
4. 生成 `matters/<slug>/history.md` 并写入单条"已立案"条目。
5. 创建空的 `matters/<slug>/notes.md`。
6. **不要**自动切换到新案件。询问："要现在切换到 `<slug>` 吗？（`/employment-legal:matter-workspace switch <slug>`）"

### `list`

枚举 `matters/*/matter.md`。读取每个文件的开头几行以提取状态。打印表格：

| Slug | 委托人 | 案件类型 | 状态 | 立案日期 | 活跃 |
|---|---|---|---|---|---|

标记当前活跃案件为 `*`。如存在，在单独的"已归档"标题下包含 `_archived/*`。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。如不存在，提供 `/employment-legal:matter-workspace new <slug>`。
2. 编辑实务级 CLAUDE.md 中的 `Active matter:` 行为 `Active matter: <slug>`。
3. 向用户显示 matter.md 摘要以便确认他们在正确的案件上。

### `close <slug>`

1. 确认 `matters/<slug>/` 存在。
2. 向 `matters/<slug>/history.md` 追加一条"已关闭"条目，包含当天日期。
3. 将 `matters/<slug>/` → `matters/_archived/<slug>/` 移动。
4. 如果关闭的案件是活跃案件，将 `Active matter:` 设置为 `none — 仅实务级上下文`。

### `none`

将实务级 CLAUDE.md 中的 `Active matter:` 设置为 `none — 仅实务级上下文`。与用户确认。

## `matter.md` 模板

```markdown
[工作成果标题——根据插件配置 ## Outputs——因角色不同；见实务级 CLAUDE.md 中的 `## Who's using this`]

# 案件：[委托人] — [简短描述]

**Slug：** [slug]
**立案日期：** [YYYY-MM-DD]
**状态：** active
**保密级别：** [标准 / 加强 / 洁净团队]

---

## 当事方

**委托人：** [名称]
**对方当事人：** [名称]

## 案件类型

[录用 | 解除 | 调查 | 假期 | 劳动关系认定 | 跨地域用工 | 制度项目 | 其他——附一行理由]

## 关键事实

[2-5句话。本案是关于什么的。利益相关者是谁。利害关系在哪。什么使其与默认实务实践不同。]

## 个案特定覆盖项

*对实务级实践的偏离，仅适用于本案。*

- [例如："竞业限制期限上限：客户要求24个月，非常规标准12个月。"]
- [例如："语气：关系维护——对方当事人是战略合作伙伴。"]
- [例如："管辖：须为中国法，排除域外适用。"]

## 关联案件

- [slug——一行说明为何关联]

## 保密说明

[如为加强或洁净团队，说明原因。谁可以查看案件文件。即使全局开启，跨案件上下文是否允许。]
```

## `history.md` 种子

```markdown
# 历史记录：[委托人] — [简短描述]

仅追加的事件日志。最新条目在顶部。

---

## [YYYY-MM-DD] —— 案件立案

立案完成。Slug：`[slug]`。状态：active。
[任何超出 matter.md 值得保留的初始上下文——例如"因收到[对方当事人]的劳动合同解除通知而立案。"。]
```

## 跨案件上下文

实务级 CLAUDE.md 中有 `Cross-matter context:` 标记。当为 `off`（默认值）时，工作在案件A中的技能**绝不读取**任何其他 `B` 的 `matters/B/` 中的文件。句号。这是该设置存在的保密保证。

当为 `on` 时，技能仅在用户明确要求时（例如"比较我们过去五个供应商案件中的责任上限立场"）才可以跨案件文件夹读取文件。即使为 `on`，默认也仅加载活跃案件，除非用户要求跨案件视图。

## 本技能不做什么

- **运行利益冲突检索。** 利益冲突是执业者/律所的工作；立案仅捕获用户声明的内容。
- **强制执行保存政策。** 关闭归档案件；不删除。保存政策不在范围内。
- **自动路由输出。** 实体技能决定写入哪里；本技能告诉它*哪个文件夹*是活跃的，而不是放什么内容。
- **决定跨案件是否合适。** 它读取标记并遵守。
