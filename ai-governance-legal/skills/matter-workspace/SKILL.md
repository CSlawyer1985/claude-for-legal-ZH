---
name: matter-workspace
description: >
  管理事务工作区——创建、列表、切换、关闭或解除活跃事务。
  适用于多客户私人执业场景，将一个客户或委托的上下文与另一个
  隔离开。也可以在实质技能需要知道它在哪个事务中工作时使用。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

执业律师同时处理多个客户和事务。事务工作区将一个客户或委托的上下文与另一个隔离开。此技能管理工作区。

## 子命令

- `/ai-governance-legal:matter-workspace new <slug>` — 创建新的事务工作区，运行简短录入，写入 `matter.md`
- `/ai-governance-legal:matter-workspace list` — 列出事务及其状态和活跃标记
- `/ai-governance-legal:matter-workspace switch <slug>` — 设置活跃事务
- `/ai-governance-legal:matter-workspace close <slug>` — 归档事务（移动到 `~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/matters/_archived/`，不删除）
- `/ai-governance-legal:matter-workspace none` — 解除活跃事务，仅在实践层面工作

## 指令

1. 读取 `~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/CLAUDE.md` — 确认 `## 事务工作区` 部分已填充。如果 `已启用` 为 `✗`，告知用户："事务工作区已关闭——你被配置为法务内部实践，只有一个客户，因此插件自动从实践级上下文工作。如果你实际上跨多个客户工作，请重新运行 `/ai-governance-legal:cold-start-interview --redo` 并选择私人执业设置。否则，你不需要 `/ai-governance-legal:matter-workspace`。" 不要报错——关闭状态是法务内部用户的预期状态。
2. 按照以下子命令逻辑操作。
3. 根据 `$ARGUMENTS` 的第一个词分发：
   - `new` → 运行录入访谈，写入 `~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/matters/<slug>/matter.md`，种子化 `history.md` 和 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/matters/*/matter.md`，打印表格，标记活跃事务。
   - `switch` → 更新实践级 CLAUDE.md 中的 `活跃事务：` 行。
   - `close` → 将 `~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/matters/<slug>/` 移动到 `~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/matters/_archived/<slug>/`，在 `history.md` 中记录关闭日期。
   - `none` → 将 `活跃事务：` 设置为 `无 — 仅实践级上下文`。
4. 向用户展示变更内容，确认后再写入。

## 注意事项

- 除非实践级 CLAUDE.md 中 `跨事务上下文` 为 `开`，否则技能绝不跨事务读取。
- 归档不是删除——已关闭的事务保持可读，以供保留/冲突检查之用。
- Slug 使用小写字母加连字符。如果 slug 在已归档和活跃中被重复使用，已归档的保留在 `_archived/<slug>/` 下。

---

# 事务工作区

跨多客户执业的律师（私人执业——独立执业、小型律所、大型律所）处理多个事务。一个事务的上下文不得泄露到另一个事务中。此技能是使这一点成立的轻量文件管理层。

**默认状态是关闭的。** 法务内部用户永远看不到这个——他们仅在实践级运行。事务工作区在冷启动时为私人执业用户开启，或通过编辑实践级 CLAUDE.md 中的 `## 事务工作区` 开启。如果 `已启用` 为 `✗`，此技能不运行；上述工作流解释关闭状态并为确实需要事务隔离的用户建议 `/ai-governance-legal:cold-start-interview --redo`。

## 存储布局

所有事务数据位于：

```
~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/
├── CLAUDE.md                       # 实践级实践配置文件
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、对方、事务类型、关键事实、覆盖项
    │   ├── history.md              # 日期化的事件、决策、草稿、审查日志
    │   ├── notes.md                # 自由形式的工作笔记
    │   └── outputs/                # 此事务的技能输出（可选子文件夹）
    └── _archived/
        └── <slug>/                 # 已关闭的事务——可读但不活跃
```

Slug 使用小写字母加连字符。示例：`acme-ai-vendor-2026`、`zenith-algorithm-filing`、`novacorp-ai-policy`。

## 活跃事务在实践 CLAUDE.md 中

实践级 CLAUDE.md 中 `## 事务工作区` 下的 `活跃事务：` 行是唯一的真相来源。切换事务就是编辑该行。没有单独的状态文件。

## 子命令逻辑

### `new <slug>`

1. 确认 slug 在 `matters/<slug>/` 或 `matters/_archived/<slug>/` 中尚未出现。如果重复，要求用户选择不同的 slug。
2. 运行录入访谈：
   - **客户**（我们代表的当事方，或法务内部用户对应的业务部门）
   - **对方**（另一方——可能有多个）
   - **事务类型**（读取插件的实践配置获取典型类别；对于 ai-governance-legal：AI供应商合同审查 | 算法备案 | AI政策起草 | AI系统评估 | 科技伦理审查 | 监管问询/调查 | 其他）
   - **保密级别**（标准 | 加强 | 洁净团队——加强提示在跨事务设置中需额外注意）
   - **关键事实**（2-5句话：此事务关于什么，利益相关者是谁，利害关系是什么）
   - **事务特定覆盖项**（偏离实践级操作手册之处，如"客户要求AI训练数据条款禁止供应商使用任何客户数据进行训练，比实践默认立场更严格"）
   - **相关事务**（任何关联事务的 slug）
3. 使用以下模板写入 `matters/<slug>/matter.md`。
4. 种子化 `matters/<slug>/history.md`，写入一条"已开设"条目。
5. 创建空的 `matters/<slug>/notes.md`。
6. **不要**自动切换到新事务。询问："是否现在切换到 `<slug>`？（`/ai-governance-legal:matter-workspace switch <slug>`）"

### `list`

枚举 `matters/*/matter.md`。读取每个文件的前几行以提取状态。打印表格：

| Slug | 客户 | 事务类型 | 状态 | 开设日期 | 活跃 |
|------|------|----------|------|----------|------|

用 `*` 标记当前活跃事务。如果有已归档事务，在单独的"已归档"标题下列出 `_archived/*`。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。如果不存在，提供 `/ai-governance-legal:matter-workspace new <slug>`。
2. 编辑实践级 CLAUDE.md 中的 `活跃事务：` 行为 `活跃事务：<slug>`。
3. 向用户展示 matter.md 摘要，以便确认他们在正确的事务上。

### `close <slug>`

1. 确认 `matters/<slug>/` 存在。
2. 在 `matters/<slug>/history.md` 中追加一条"已关闭"条目，日期为当天。
3. 将 `matters/<slug>/` → 移动到 `matters/_archived/<slug>/`。
4. 如果关闭的事务是活跃事务，将 `活跃事务：` 设置为 `无 — 仅实践级上下文`。

### `none`

将实践级 CLAUDE.md 中的 `活跃事务：` 设置为 `无 — 仅实践级上下文`。与用户确认。

## `matter.md` 模板

```markdown
[工作成果头 — 按照插件配置 ## 输出 — 根据角色有所不同；见实践级 CLAUDE.md 中的 `## 谁在使用此工具`]

# 事务：[客户] — [简短描述]

**Slug：** [slug]
**开设日期：** [YYYY-MM-DD]
**状态：** 活跃
**保密级别：** [标准 / 加强 / 洁净团队]

---

## 当事方

**客户：** [名称]
**对方：** [名称]

## 事务类型

[AI供应商合同审查 | 算法备案 | AI政策起草 | AI系统评估 | 科技伦理审查 | 监管问询/调查 | 其他 — 附一行说明]

## 关键事实

[2-5句话。此事务关于什么。利益相关者是谁。利害关系是什么。与默认操作手册有何不同之处。]

## 事务特定覆盖项

*任何偏离实践级操作手册且仅适用于此事务的内容。*

- [例如"训练数据条款红线：本客户绝对禁止供应商使用任何客户数据进行模型训练——比实践默认立场更严格。"]
- [例如"时间紧迫——算法备案必须在30天内完成，平台上线日期已定。"]
- [例如"洁净团队：开源合规审查涉及高度敏感的商业策略信息。"]

## 相关事务

- [slug — 一句说明关联原因]

## 关于保密的说明

[如果为加强或洁净团队，说明原因。谁可以查看事务文件。即使全局开启，跨事务上下文是否允许。]
```

## `history.md` 种子

```markdown
# 历史：[客户] — [简短描述]

仅追加的事件日志。最新的在顶部。

---

## [YYYY-MM-DD] — 事务开设

录入完成。Slug：`[slug]`。状态：活跃。
[任何值得在 matter.md 之外保留的初始上下文——例如"应[对方]的AI供应商协议草案开设。" ]
```

## 跨事务上下文

实践级 CLAUDE.md 中有一个 `跨事务上下文：` 标志。当它为 `关`（默认）时，在事务A中工作的技能**绝不**读取任何其他事务B的 `matters/B/` 文件。句号。这是该设置旨在提供的保密保证。

当它为 `开` 时，技能只有在用户明确要求时才可以跨事务文件夹读取文件（例如"比较我们在所有AI供应商审查中关于模型训练数据条款的立场"）。即使为 `开`，默认只加载活跃事务，除非用户要求跨事务视图。

## 本技能不做的事

- **不运行冲突检查。** 冲突是执业律师/律所的职责；录入只捕获用户声明的内容。
- **不强制执行保留期。** 关闭即归档事务；不删除。保留政策不在范围内。
- **不自动路由输出。** 实质技能决定写入到哪里；此技能告诉它*哪个文件夹*是活跃的，不决定写入什么。
- **不决定跨事务是否合适。** 它读取标志并遵守。
