---
name: registry-browser
description: >
  搜索已监视注册表中的社区法律技能，显示匹配项及其描述，并提供在安装前
  查看完整 SKILL.md 的选项。当用户说"浏览""搜索技能""找某个方面的技能"
  "有什么可用的"或想添加新注册表到监视列表时使用。
argument-hint: "[搜索关键词]"
---

# /registry-browser

1. 加载 `~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/CLAUDE.md` → 已监视注册表。
2. 使用以下工作流。
3. 搜索每个注册表。显示匹配项及描述。
4. 对任意匹配项提供查看完整 SKILL.md 的选项。

---

## 目的

跨已监视注册表查找技能。搜索、预览、决策。

## 加载上下文

`~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/CLAUDE.md` → 已监视注册表列表。

## 工作流

### 第1步：获取注册表索引

对每个已监视注册表：

- GitHub 仓库：获取 `skills/` 目录列表及每个 `SKILL.md` 的 frontmatter（name + description）。
- 市场式注册表：获取索引。

将索引缓存到本地（`references/registry-cache.json`），使浏览更快。缓存超过 7 天或用户要求时刷新。

### 第2步：搜索

将查询词与技能名称和描述进行匹配。简单关键词匹配即可——这些数据规模足够小，模糊搜索是大材小用。

此外：若注册表按类别组织技能，支持按类别浏览。

### 第3步：呈现匹配项

```markdown
## 搜索："[关键词]"

**在 [M] 个注册表中找到 [N] 个技能：**

### [技能名称]
**来源：** [注册表名称]
**描述：** [来自 frontmatter]
[查看完整 SKILL.md] [安装]

### [技能名称]
[...]
```

### 第4步：预览

当用户选择"查看完整 SKILL.md"：获取并展示完整文件。用户在决定安装前阅读它。无意外。

### 第5步：添加注册表

如果用户有一个不在监视列表中的注册表 URL：

1. 获取它，验证它是技能仓库（有 `skills/` 或 `.claude-plugin/`）
2. 展示其中的内容
3. 经确认后添加到 `~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/CLAUDE.md` → 已监视注册表

## 默认注册表

- **lpm-skills** — 14 个法律项目管理技能。实践领域无关。良好的起点。
- 为生态系统的成长留出添加其他注册表的空间。

## 本技能不做什么

- 安装任何东西。它只浏览。skill-installer 负责安装。
- 评价或审查技能。它向你展示 SKILL.md；你来判断。
- 搜索整个互联网。仅搜索已监视注册表。
