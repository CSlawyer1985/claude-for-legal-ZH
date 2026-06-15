---
name: matter-workspace
description: 管理事务工作区——创建、列表、切换、关闭或解除活跃事务（实践层面）。适用于多客户/多事务工作场景，需要将一项委托的上下文与另一项隔离开，或实质技能需要知道它在哪个事务中工作时。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

执业律师同时处理多个客户和事务。事务工作区将一个客户或委托的上下文与另一个隔离开。此技能管理工作区。

## 子命令

- `/regulatory-legal:matter-workspace new <slug>` — 创建新的事务工作区，运行简短录入，写入 `matter.md`
- `/regulatory-legal:matter-workspace list` — 列出事务及其状态和活跃标记
- `/regulatory-legal:matter-workspace switch <slug>` — 设置活跃事务
- `/regulatory-legal:matter-workspace close <slug>` — 归档事务（移动到 `~/.claude/plugins/config/claude-for-legal-zh/regulatory-legal/matters/_archived/`，不删除）
- `/regulatory-legal:matter-workspace none` — 解除活跃事务，仅在实践层面工作

## 指令

1. 读取 `~/.claude/plugins/config/claude-for-legal-zh/regulatory-legal/CLAUDE.md` — 确认 `## 事务工作区` 部分已填充。如果 `已启用` 为 `✗`，告知用户："事务工作区已关闭——你被配置为法务内部实践，只有一个客户，因此插件自动从实践级上下文工作。如果你实际上跨多个客户工作，请重新运行 `/regulatory-legal:cold-start-interview --redo` 并选择私人执业设置。否则，你不需要 `/regulatory-legal:matter-workspace`。" 不要报错——关闭状态是法务内部用户的预期状态。
2. 按照以下子命令逻辑操作。
3. 根据 `$ARGUMENTS` 的第一个词分发：
   - `new` → 运行录入访谈，写入 `~/.claude/plugins/config/claude-for-legal-zh/regulatory-legal/matters/<slug>/matter.md`，种子化 `history.md` 和 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-zh/regulatory-legal/matters/*/matter.md`，打印表格，标记活跃事务。
   - `switch` → 更新实践级 CLAUDE.md 中的 `活跃事务：` 行。
   - `close` → 移动并归档事务，记录关闭日期。
   - `none` → 将 `活跃事务：` 设置为 `无 — 仅实践级上下文`。
4. 向用户展示变更内容，确认后再写入。

---

# 事务工作区

跨多客户执业的律师（私人执业——独立执业、小型律所、大型律所）处理多个事务。一个事务的上下文不得泄露到另一个事务中。此技能是使这一点成立的轻量文件管理层。

**默认状态是关闭的。** 法务内部用户永远看不到这个——他们仅在实践级运行。事务工作区在冷启动时为私人执业用户开启，或通过编辑实践级 CLAUDE.md 中的 `## 事务工作区` 开启。

## 存储布局

所有事务数据位于：

```
~/.claude/plugins/config/claude-for-legal-zh/regulatory-legal/
├── CLAUDE.md                       # 实践级实践配置文件
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、对方、事务类型、关键事实、覆盖项
    │   ├── history.md              # 日期化的事件、决策、草稿、审查日志
    │   ├── notes.md                # 自由形式的工作笔记
    │   └── outputs/                # 此事务的技能输出
    └── _archived/
        └── <slug>/                 # 已关闭的事务——可读但不活跃
```

Slug 使用小写字母加连字符。示例：`acme-regulatory-review`、`zenith-gap-remediation`。

## 子命令逻辑

### `new <slug>`

1. 确认 slug 不重复。
2. 运行录入访谈：
   - **客户**（我们代表的当事方）
   - **对方**（监管机构或另一方）
   - **事务类型**（对于 regulatory-legal：法规制定 | 意见征集 | 差距整改 | 监管问询 | 执法应对 | 常设议题 | 其他）
   - **保密级别**（标准 | 加强 | 洁净团队）
   - **关键事实**（2-5句话）
   - **事务特定覆盖项**
   - **相关事务**
3. 写入 `matters/<slug>/matter.md`。
4. 种子化 `history.md` 和 `notes.md`。
5. 不自动切换，询问用户是否切换。

### 其他子命令

与 privacy-legal、ip-legal、ai-governance-legal 插件中的 matter-workspace 技能一致。

## 跨事务上下文

除非 `跨事务上下文` 为 `开`，否则绝不跨事务读取文件。

## 本技能不做的事

- **不运行冲突检查。** 冲突是执业律师/律所的职责。
- **不强制执行保留期。** 关闭即归档；不删除。
- **不自动路由输出。** 实质技能决定写入到哪里。
- **不决定跨事务是否合适。** 读取标志并遵守。
