---
name: matter-workspace
description: >
  管理事项工作区——创建、列表、切换、关闭或解除（实务级）。
  为多客户执业者保持一个客户或委托的上下文与其他客户隔绝。
  用于用户想要开启新事项、切换事项、列出事项、关闭/归档事项或仅在实务级工作时。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

执业者跨多个客户和事项工作。事项工作区将一个客户或委托的上下文与其他全部隔离。本技能管理这些工作区。

## 子命令

- `/ip-legal:matter-workspace new <slug>` — 创建新事项工作区，执行简短的采集面谈，写入 `matter.md`
- `/ip-legal:matter-workspace list` — 列明事项及其状态和活跃标记
- `/ip-legal:matter-workspace switch <slug>` — 设置活跃事项
- `/ip-legal:matter-workspace close <slug>` — 归档事项（移动至 `~/.claude/plugins/config/claude-for-legal-zh/ip-legal/matters/_archived/`，绝不删除）
- `/ip-legal:matter-workspace none` — 解除任何活跃事项，仅在实务级工作

## 使用说明

1. 读取 `~/.claude/plugins/config/claude-for-legal-zh/ip-legal/CLAUDE.md` — 确认 `## 事项工作区` 分区已填充。如 `Enabled` 为 `✗`，告知用户："事项工作区已关闭——你配置为公司法务，仅有一个客户，插件自动以实务级上下文运行。如你实际跨多个客户工作，重新运行 `/ip-legal:cold-start-interview --redo` 并选择私人执业设置。否则，你不需要 `/ip-legal:matter-workspace`。"不用报错——关闭状态是法务用户的预期状态。
2. 按以下子命令逻辑操作。
3. 按 `$ARGUMENTS` 的首个标记分派：
   - `new` → 执行采集面谈，写入 `~/.claude/plugins/config/claude-for-legal-zh/ip-legal/matters/<slug>/matter.md`，种子 `history.md` 和 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-zh/ip-legal/matters/*/matter.md`，打印表格，标记活跃事项。
   - `switch` → 更新实务级 CLAUDE.md 中的 `Active matter:` 行。
   - `close` → 移动 `~/.claude/plugins/config/claude-for-legal-zh/ip-legal/matters/<slug>/` 至 `~/.claude/plugins/config/claude-for-legal-zh/ip-legal/matters/_archived/<slug>/`，在 `history.md` 中记录关闭日期。
   - `none` → 将 `Active matter:` 设置为 `none — 仅实务级上下文`。
4. 向用户显示变更内容，写入前确认。

## 说明

- 除非实务级 CLAUDE.md 中 `跨事项上下文` 开启，技能绝不跨事项读取。
- 归档不是删除——已关闭事项仍然可读，用于留档/冲突目的。
- slug 小写使用连字符。如 slug 在已归档和活跃中重复使用，已归档事项保留在 `_archived/<slug>/`。

---

多客户执业者（私人执业——独立、小型律所、大型律所）跨多个事项工作。一个事项的上下文不得泄露到另一个。本技能是实现这一点的薄文件管理层。

**默认状态为关闭。** 法务用户永远看不到这个——他们仅在实务级运行。事项工作区在冷启动时对私人执业用户开启，或通过编辑实务级 CLAUDE.md 中的 `## 事项工作区` 开启。如 `Enabled` 为 `✗`，本技能不运行；转而解释关闭状态并建议需要事项隔离的用户运行 `/ip-legal:cold-start-interview --redo`。

## 存储布局

所有事项数据位于：

```
~/.claude/plugins/config/claude-for-legal-zh/ip-legal/
├── CLAUDE.md                       # 实务级画像
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、相对方、事项类型、关键事实、覆盖设置
    │   ├── history.md              # 事件、决策、草稿、审查的日期记录
    │   ├── notes.md                # 自由形式工作笔记
    │   └── outputs/                # 本事项的技能输出（可选的子文件夹）
    └── _archived/
        └── <slug>/                 # 已关闭事项 — 可读但不活跃
```

slug 小写使用连字符。示例：`acme-商标-2026`、`zenith-信息网络传播权`、`novacorp-FTO`。

## 活跃事项保存在实务 CLAUDE.md 中

实务级 CLAUDE.md 中 `## 事项工作区` 下的 `Active matter:` 行是唯一真相来源。切换事项编辑该行。无独立状态文件。

## 子命令逻辑

### `new <slug>`

1. 确认 slug 不在 `matters/<slug>/` 或 `matters/_archived/<slug>/` 中已存在。如重复使用，要求用户另选 slug。
2. 执行采集面谈：
   - **客户**（我们代表的当事人，或法务用户的内部业务单位）
   - **相对方**（对方——可为多个；可为"未知第三方侵权人"用于监视服务触发的事项）
   - **事项类型**（阅读插件实务画像中的典型类别；对 ip-legal：商标确权 | 商标维权 | 信息网络传播权 | 专利FTO | 专利侵权 | 知识产权条款审查 | 开源合规 | 组合维护 | 其他）
   - **保密级别**（标准 | 加强 | 洁净团队——加强提示在跨事项场景中额外小心；洁净团队在专利FTO工作中常见）
   - **关键事实**（2-5句：此事是关于什么的，谁是利益相关方，什么关乎利害）
   - **事项特定的实务立场覆盖**（如"客户要求此商标以激进立场对待"、"相对方是战略合作伙伴——仅用稳健语调"、"发明人不可用——不在面谈中出现"）
   - **关联事项**（任何关联事项的 slug）
3. 按以下模板写入 `matters/<slug>/matter.md`。
4. 种子 `matters/<slug>/history.md`，添加一条"已开启"记录。
5. 创建空 `matters/<slug>/notes.md`。
6. **不**自动切换至新事项。询问："要现在切换至 `<slug>` 吗？（`/ip-legal:matter-workspace switch <slug>`）"

### `list`

枚举 `matters/*/matter.md`。读取每份文件的 front-matter 或前几行以提取状态。打印表格：

| Slug | 客户 | 事项类型 | 状态 | 开启日 | 活跃 |
|---|---|---|---|---|---|

以 `*` 标记当前活跃事项。如存在已归档事项，在单独的"已归档"标题下列出 `_archived/*`。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。如否，提供 `/ip-legal:matter-workspace new <slug>`。
2. 编辑实务级 CLAUDE.md 中的 `Active matter:` 行为 `Active matter: <slug>`。
3. 向用户显示 matter.md 摘要，使其确认在正确事项上。

### `close <slug>`

1. 确认 `matters/<slug>/` 存在。
2. 在 `matters/<slug>/history.md` 中追加一条"已关闭"记录，附今天日期。
3. 移动 `matters/<slug>/` → `matters/_archived/<slug>/`。
4. 如关闭的事项是活跃事项，将 `Active matter:` 设置为 `none — 仅实务级上下文`。

### `none`

将实务级 CLAUDE.md 中的 `Active matter:` 设置为 `none — 仅实务级上下文`。与用户确认。

## `matter.md` 模板

```markdown
[工作成果页眉 — 按插件配置 ## 输出 — 因角色而异；见实务级 CLAUDE.md 中的 `## 使用者`]

# 事项：[客户] — [简短描述]

**Slug：** [slug]
**开启日：** [YYYY-MM-DD]
**状态：** 活跃
**保密级别：** [标准 / 加强 / 洁净团队]

---

## 当事人

**客户：** [名称]
**相对方：** [名称]

## 事项类型

[商标确权 | 商标维权 | 信息网络传播权 | 专利FTO | 专利侵权 | 知识产权条款审查 | 开源合规 | 组合维护 | 其他 — 附一行理由]

## 关键事实

[2-5句。此事是关于什么的。谁是利益相关方。什么关乎利害。什么使其不同于默认立场。]

## 事项特定覆盖设置

*任何仅适用于本事项、偏离实务级立场的调整。*

- [如"维权立场：即使所内默认为激进，此处采用稳健——相对方是重要渠道合作伙伴。"]
- [如"维权审批：任何函件发出前需市场部额外签署。"]
- [如"洁净团队：即使全局跨事项上下文开启，事项文件不可读取。"]

## 关联事项

- [slug — 一行说明为何关联]

## 保密说明

[如为加强或洁净团队，描述原因。谁可查看事项文件。即使全局开启，跨事项上下文是否允许。]
```

## `history.md` 种子

```markdown
# 历史：[客户] — [简短描述]

追加式事件日志。最新在上。

---

## [YYYY-MM-DD] — 事项开启

面谈完成。Slug：`[slug]`。状态：活跃。
[超出 matter.md 值得保存的任何初始上下文 — 如"因监视服务在第25类发现'APEXLEAF'标记而开启。"]
```

## 跨事项上下文

实务级 CLAUDE.md 有一个 `跨事项上下文：` 标记。当它为 `关闭`（默认），在事项A中工作的技能**绝不读取** `matters/B/` 中的任何文件。期限。这是此设置提供的保密保证。

当它为 `开启`，技能可仅在用户明确要求时跨事项文件夹读取文件（如"向我展示我们跨事项在此商标上发送出的每封维权函"）。即使 `开启`，除非用户要求跨事项视图，默认也仅加载活跃事项。

## 本技能不做什么

- **不执行冲突检查。** 冲突是执业者/律所的工作；采集面谈记录用户声明的内容。
- **不强制执行留存。** 关闭归档事项；不删除。留存政策不在范围内。
- **不自动路由输出。** 实质性技能决定写入何处；本技能告诉它哪个文件夹是活跃的，不规定放什么。
- **不决定跨事项是否合适。** 读取标记并遵守。
