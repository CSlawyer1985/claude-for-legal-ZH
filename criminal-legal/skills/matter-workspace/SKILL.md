---
name: matter-workspace
description: >
  管理事项工作区——创建、列表、切换、关闭或解除（实务级）。
  为多案件执业者保持一个委托的上下文与其他案件隔绝——刑事案件间的
  事实隔离同时是保密义务要求。用于开启新案件、切换案件、列出案件、
  关闭/归档案件或仅在实务级工作时。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

刑事律师通常同时办理多个委托。事项工作区将一个案件的上下文与其他全部隔离——刑事案件间的事实隔离同时是《律师法》第38条保密义务的要求。本技能管理这些工作区。

## 子命令

- `/criminal-legal:matter-workspace new <slug>` — 创建新案件工作区，执行简短的采集面谈，写入 `matter.md`
- `/criminal-legal:matter-workspace list` — 列明案件及其状态和活跃标记
- `/criminal-legal:matter-workspace switch <slug>` — 设置活跃案件
- `/criminal-legal:matter-workspace close <slug>` — 归档案件（移动至 `~/.claude/plugins/config/claude-for-legal-zh/criminal-legal/matters/_archived/`，绝不删除）
- `/criminal-legal:matter-workspace none` — 解除任何活跃案件，仅在实务级工作

## 使用说明

1. 读取 `~/.claude/plugins/config/claude-for-legal-zh/criminal-legal/CLAUDE.md` — 确认 `## 事项工作区` 分区已填充。如 `已启用` 为 `✗`，告知用户："事项工作区已关闭——你配置为单一客户模式。如你实际同时办理多个委托，重新运行 `/criminal-legal:cold-start-interview --redo` 并选择多案件设置。"不用报错。
2. 按 `$ARGUMENTS` 的首个标记分派：
   - `new` → 执行采集面谈（委托人角色、办案阶段、涉嫌罪名类别、脱敏代号），写入 `~/.claude/plugins/config/claude-for-legal-zh/criminal-legal/matters/<slug>/matter.md`，种子 `history.md` 和 `notes.md`。**matter.md 中同样只记录脱敏信息。**
   - `list` → 枚举 `matters/*/matter.md`，打印表格，标记活跃案件。
   - `switch` → 更新实务级 CLAUDE.md 中的 `活跃事项:` 行。
   - `close` → 移动至 `matters/_archived/<slug>/`，在 `history.md` 中记录关闭日期。
   - `none` → 将 `活跃事项:` 设置为 `none — 仅实务级上下文`。
3. 向用户显示变更内容，写入前确认。

## 说明

- 除非实务级 CLAUDE.md 中 `跨事项背景` 开启，技能绝不跨案件读取。
- 归档不是删除——已关闭案件仍然可读，用于留档/利冲排查目的。
- slug 小写使用连字符。**slug 本身也不得包含可识别案件信息**（用 `case-a-2026` 而非当事人姓名）。
