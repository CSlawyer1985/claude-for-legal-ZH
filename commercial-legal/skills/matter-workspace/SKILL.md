---
name: matter-workspace
description: >
  管理事项工作区——新建、列出、切换、关闭或脱离（业务领域级）。当多客户执业者
  需要创建事项、切换当前事项、列出事项、归档事项或脱离至业务领域级上下文时使用，
  或当其他技能需要知道当前在哪个事项中工作时使用。
argument-hint: "<new | list | switch | close | none> [简称]"
---

# /matter-workspace

多客户执业者跨多个客户和事项工作。事项工作区将一个客户或委托的上下文与其他客户或委托隔离开来。本命令管理这些工作区。

## 子命令

- `/commercial-legal:matter-workspace new <slug>` — 创建新事项工作区，运行简短收案访谈，写入 `matter.md`
- `/commercial-legal:matter-workspace list` — 列出事项及其状态
- `/commercial-legal:matter-workspace switch <slug>` — 设置当前事项
- `/commercial-legal:matter-workspace close <slug>` — 归档事项（移至 `_archived/`，绝不删除）
- `/commercial-legal:matter-workspace none` — 脱离任何当前事项，纯业务领域级工作

## 指令

1. 读取审查指引——确认 `## 事项工作区` 部分已填充。如果 `Enabled` 为 `✗`，告知用户事项工作区已关闭——适用于仅服务一家公司的企业法务用户。不要报错——关闭状态是企业法务用户的预期状态。
2. 使用以下子命令逻辑。
3. 根据子命令分发。
4. 向用户展示变更内容并在写入前确认。

## 说明

- 除非业务领域级 CLAUDE.md 中 `跨事项上下文` 为 `on`，技能绝不跨事项读取文件。
- 归档不是删除——已关闭的事项保持可读状态以供保留/利益冲突目的。
- 简称使用小写加连字符。如简称在已归档和当前事项中被重用，已归档的保留在 `_archived/<slug>/` 下。

---

多客户执业者（私人执业——个人执业、小型律所、大型律所）跨多个事项工作。一个事项的上下文不得泄露至另一个事项。

**默认状态为关闭。** 企业法务用户永远不会看到——他们仅以业务领域级别运行。事项工作区在冷启动时为私人执业用户开启，或通过编辑审查指引中的 `## 事项工作区` 开启。

## 存储布局

所有事项数据位于：

```
~/.claude/plugins/config/claude-for-legal-zh/commercial-legal/
├── CLAUDE.md                       # 业务领域级审查指引
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、对方当事人、事项类型、关键事实、覆盖规则
    │   ├── history.md              # 日期化的事件日志
    │   ├── notes.md                # 自由形式的工作笔记
    │   └── outputs/                # 事项的技能输出（可选子文件夹）
    └── _archived/
        └── <slug>/                 # 已关闭的事项——可读但非当前
```

## 子命令逻辑

### `new <slug>`

1. 确认简称未被占用。如被占用，要求用户选择其他简称。
2. 运行收案访谈：客户、对方当事人、事项类型、保密级别、关键事实、事项特定覆盖规则、关联事项。
3. 按模板写入 `matters/<slug>/matter.md`。
4. 种子 `history.md`。
5. 创建空 `notes.md`。
6. 不要自动切换。询问是否切换。

### `list`

列举 `matters/*/matter.md`。打印表格。标记当前事项为 `*`。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。
2. 编辑审查指引中的 `Active matter:` 行。
3. 向用户展示 matter.md 摘要。

### `close <slug>`

1. 确认文件夹存在。
2. 追加"已关闭"条目至 `history.md`。
3. 移动文件夹至 `_archived/`。
4. 如果是当前事项，设置 `Active matter:` 为 `none`。

### `none`

设置 `Active matter:` 为 `none`。与用户确认。

## 跨事项上下文

当 `Cross-matter context:` 为 `off`（默认）时，在事项A中工作的技能绝不读取事项B的文件。当为 `on` 时，技能仅在用户明确要求时跨事项读取。

## 本技能不做的事

- **不运行利益冲突检查。** 利益冲突是执业者/律所的工作。
- **不执行保留政策。** 关闭归档但不删除。
- **不自动路由输出。** 实质性技能决定写入位置；本技能告知哪个文件夹是当前的。
