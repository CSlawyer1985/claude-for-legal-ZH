---
name: matter-workspace
description: >
  管理事项工作空间——新建、列表、切换、关闭或脱钩（实务级）。
  当您为多个客户或事项工作、需要创建、列出、切换、关闭或脱钩活跃事项
  以防一个委托事项的上下文泄漏到另一个时使用。
argument-hint: "<new | list | switch | close | none> [事项简称]"
---

# /matter-workspace

律师为多个客户和事项工作。事项工作空间将每个客户或委托事项的上下文独立保持。本技能管理这些工作空间。

## 子命令

- `/product-legal:matter-workspace new <事项简称>` —— 创建新事项工作空间，运行简短收案，写入 `matter.md`
- `/product-legal:matter-workspace list` —— 列出事项，含状态和活跃标记
- `/product-legal:matter-workspace switch <事项简称>` —— 设置活跃事项
- `/product-legal:matter-workspace close <事项简称>` —— 归档事项（移至 `~/.claude/plugins/config/claude-for-legal-zh/product-legal/matters/_archived/`，绝不删除）
- `/product-legal:matter-workspace none` —— 脱离任何活跃事项，仅在实务级工作

## 指令

1. 读取 `~/.claude/plugins/config/claude-for-legal-zh/product-legal/CLAUDE.md`——确认 `## 事项工作空间` 节已填充。如果 `Enabled` 为 `✗`，告诉用户："事项工作空间已关闭——您被配置为服务一家公司的企业产品法务，插件自动以实务级上下文运行。如果您实际为多个客户工作，请重新运行 `/product-legal:cold-start-interview --redo` 并选择私人执业设置。否则，您完全不需要 `/matter-workspace`。"不要报错——禁用状态是企业法务用户的预期状态。
2. 应用以下存储布局和子命令逻辑。
3. 按 `$ARGUMENTS` 的第一个标记分发：
   - `new` → 运行收案访谈，写入 `~/.claude/plugins/config/claude-for-legal-zh/product-legal/matters/<事项简称>/matter.md`，播种 `history.md` 和 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-zh/product-legal/matters/*/matter.md`，打印表格，标记活跃事项。
   - `switch` → 更新实务级 CLAUDE.md 中的 `Active matter:` 行。
   - `close` → 将 `~/.claude/plugins/config/claude-for-legal-zh/product-legal/matters/<事项简称>/` 移至 `~/.claude/plugins/config/claude-for-legal-zh/product-legal/matters/_archived/<事项简称>/`，在 `history.md` 中记录关闭日期。
   - `none` → 将 `Active matter:` 设为 `none — practice-level context only`。
4. 向用户展示变更内容并在写入前确认。

## 备注

- 除非实务级 CLAUDE.md 中 `Cross-matter context` 为 `on`，本技能绝不跨事项读取。
- 归档不是删除——已关闭事项仍可读取，用于档案保存/利益冲突目的。
- 事项简称为小写加连字符。如果一个简称在已归档和活跃事项中重复使用，已归档版本保留在 `_archived/<事项简称>/` 下。

---

# 事项工作空间

多客户律师（私人执业——个人执业、小型律所、大型律所）处理众多事项。一个事项的上下文不能泄漏到另一个。本技能是实现这一点的轻量文件管理层。

**默认状态为关闭。** 企业法务用户从不看到此项——他们仅在实务级运行。事项工作空间在冷启动时为私人执业用户开启，或通过编辑实务级 CLAUDE.md 中的 `## 事项工作空间`。如果 `Enabled` 为 `✗`，本技能不运行；`/matter-workspace` 命令说明禁用状态并建议需要事项隔离的用户 `/cold-start-interview --redo`。

## 存储布局

所有事项数据位于：

```
~/.claude/plugins/config/claude-for-legal-zh/product-legal/
├── CLAUDE.md                       # 实务级实务画像
└── matters/
    ├── <事项简称>/
    │   ├── matter.md               # 客户、对方、事项类型、关键事实、覆盖规则
    │   ├── history.md              # 带日期的事件、决策、草稿、审查日志
    │   ├── notes.md                # 自由形式工作笔记
    │   └── outputs/                # 本事项的技能输出（可选子文件夹）
    └── _archived/
        └── <事项简称>/             # 已关闭事项——可读但非活跃
```

事项简称为小写加连字符。示例：`acme-msa-2026`、`zenith-renewal`、`vendor-xyz-nda`。

## 活跃事项在实务级 CLAUDE.md 中

实务级 CLAUDE.md 中 `## 事项工作空间` 下的 `Active matter:` 行是唯一真实来源。切换事项编辑该行。无独立状态文件。

## 子命令逻辑

### `new <事项简称>`

1. 确认简称在 `matters/<事项简称>/` 或 `matters/_archived/<事项简称>/` 中不存在。如重复，请用户选择其他简称。
2. 运行收案访谈：
   - **客户**（我们代表的当事方，或企业法务中的内部业务单元）
   - **对方**（另一方——可能有多个）
   - **事项类型**（读取插件的实务画像获取典型类别；对于产品法务：上线 | 功能审查 | 营销宣传审查 | 风险深度评估 | 产品领域（持续） | 其他）
   - **保密级别**（标准 | 增强 | 清洁团队——增强提示跨事项设置中格外小心）
   - **关键事实**（2-5句：本事项关于什么，利益相关方是谁，利害关系）
   - **对实务审查指引的事项特定覆盖规则**（例如"客户要求24个月责任上限而非所内标准12个月"，"对方为战略合作伙伴——保持关系语调"）
   - **关联事项**（任何关联事项的简称）
3. 使用以下模板写入 `matters/<事项简称>/matter.md`。
4. 播种 `matters/<事项简称>/history.md`，含单条"已开设"记录。
5. 创建空 `matters/<事项简称>/notes.md`。
6. **不要**自动切换到新事项。询问："要现在切换到 `<事项简称>` 吗？（`/product-legal:matter-workspace switch <事项简称>`）"

### `list`

枚举 `matters/*/matter.md`。读取每个文件的前置元数据或开头几行提取状态。打印表格：

| 简称 | 客户 | 事项类型 | 状态 | 开设日期 | 活跃 |
|---|---|---|---|---|---|

用 `*` 标记当前活跃事项。如有归档事项，在单独的"已归档"标题下包含 `_archived/*`。

### `switch <事项简称>`

1. 确认 `matters/<事项简称>/matter.md` 存在。如不存在，建议 `/product-legal:matter-workspace new <事项简称>`。
2. 将实务级 CLAUDE.md 中的 `Active matter:` 行编辑为 `Active matter: <事项简称>`。
3. 向用户展示 matter.md 摘要以便确认在正确的事项上。

### `close <事项简称>`

1. 确认 `matters/<事项简称>/` 存在。
2. 在 `matters/<事项简称>/history.md` 中追加"已关闭"条目，附今日日期。
3. 将 `matters/<事项简称>/` → 移至 `matters/_archived/<事项简称>/`。
4. 如果关闭的事项是活跃事项，将 `Active matter:` 设为 `none — practice-level context only`。

### `none`

将实务级 CLAUDE.md 中的 `Active matter:` 设为 `none — practice-level context only`。与用户确认。

## `matter.md` 模板

```markdown
[工作成果页眉 — 按插件配置 ## 输出规范 — 因角色而异；参见实务级 CLAUDE.md 中的 `## 使用者`]

# 事项：[客户] — [简短描述]

**简称：**[事项简称]
**开设日期：**[YYYY-MM-DD]
**状态：** 活跃
**保密级别：**[标准 / 增强 / 清洁团队]

---

## 当事方

**客户：**[名称]
**对方：**[名称]

## 事项类型

[供应商协议 | 客户协议 | 保密协议 | SaaS订阅 | 修订 | 续约 | 其他——附一句话理由]

## 关键事实

[2-5句。本事项关于什么。利益相关方是谁。利害关系。与默认审查指引有何不同。]

## 事项特定覆盖规则

*任何偏离实务级审查指引、仅适用于本事项的规则。*

- [例如"责任上限：客户要求24个月，非所内标准12个月。"]
- [例如"语气：保持关系——对方为战略合作伙伴。"]
- [例如"管辖法律：须为中国法，非约定境外法。"]

## 关联事项

- [事项简称——一句话说明为何关联]

## 保密备注

[如为增强或清洁团队，描述原因。谁可查看事项文件。即使全局开启跨事项上下文是否允许。]
```

## `history.md` 种子

```markdown
# 历史：[客户] — [简短描述]

仅追加事件日志。最新在上。

---

## [YYYY-MM-DD] — 事项开设

收案完成。简称：`[事项简称]`。状态：活跃。
[值得在matter.md之外保留的任何初始上下文——例如"因收到[对方]发来的服务协议草案而开设。" ]
```

## 跨事项上下文

实务级 CLAUDE.md 有 `Cross-matter context:` 标志。当为 `off`（默认值）时，事项A中的技能**绝不读取**任何其他事项B的 `matters/B/` 文件。句号。这是该设置存在的保密保证。

当为 `on` 时，技能仅在用户明确要求时可跨事项文件夹读取（例如"比较我们过去五个供应商事项中责任上限的立场"）。即使为 `on`，默认仅加载活跃事项，除非用户要求跨事项视角。

## 本技能不做什么

- **运行利益冲突检查。** 利益冲突是律师/律所的工作；收案仅记录用户声明的内容。
- **强制执行档案保留。** 关闭即归档；不删除。档案保留政策不在范围内。
- **自动路由输出。** 实质性技能决定写入何处；本技能告诉它*哪个文件夹*是活跃的，而非在其中放入什么。
- **决定跨事项是否适当。** 读取标志并遵守。
