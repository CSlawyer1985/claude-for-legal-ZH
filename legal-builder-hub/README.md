# 法律构建中心插件（Legal Builder Hub）

社区法律技能发现与安装。浏览 GitHub 注册表（lpm-skills、[附加注册表 — 通过 `/legal-builder-hub:registry-browser` 添加] 等），安装与自动更新，在你的其他法律插件中浮现相关社区技能。cold-start 访谈本身就是入门技能包推荐器 — 询问你的实践类型，推荐安装内容。

**每个社区技能在安装前以原始形式呈现，经过提示注入（prompt-injection）模式扫描，并依据法律技能设计框架评估。插件帮你发现和评估；你决定信任什么。**

## 适用对象

所有使用其他法律插件的人。这是应用商店。

## 首次运行：cold-start 初始化访谈

询问你的实践类型、行业、团队规模、工具熟练程度。推荐匹配的社区技能入门包。安装你选择的技能。

```
/legal-builder-hub:cold-start-interview
```

你的配置存储在 `~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/CLAUDE.md`，插件更新时不受影响。

## 安全态势

安装的社区技能以你对客户数据、事项文件以及团队策略手册（playbook）的访问权限运行。中心将每次安装和每次更新视为一次信任决策。四层防御，任何单独一层均不充分：

- **白名单（Allowlist — 管理员控制）：**`~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/allowlist.yaml` 声明社区技能可以使用的注册表、发布者和 MCP 连接器。`permissive` 模式（默认）对列表外的任何内容发出警告；`restrictive` 模式（推荐用于律所/企业部署）予以拒绝。白名单在安装器读取任何第三方内容之前检查。参见 `skills/skill-installer/references/allowlist.md` 了解模式。
- **原始源文件，非摘要：**安装器在写入任何内容之前向你展示完整的原始 `SKILL.md` — 非 AI 摘要。摘要是便利；一个做了不当行为的技能必须在原始显示将展示的文本中做出。
- **启发式扫描：**安装器和 `skills-qa` 都对技能进行提示注入模式扫描（覆盖/权威声明、越权读写、外部 URL、隐藏 Unicode、shell 执行、凭证请求）。这些是 AI 启发式扫描，已明确标注 — 干净的扫描不是安全审计，而是提示你亲自阅读文本。
- **每次均需人工批准：**未经全新输入的 `yes`，无任何内容写入磁盘。批准不从先前的消息推断。为纵深防御，安装器建议在只读子代理中运行获取/分析，使写入能力仅在批准后才可用。

更新使用相同的态势：自动更新器锁定提交 SHA（commit SHAs）（非可变标签），显示包括 hooks 和 MCP 更改的完整 diff，并要求每次更新明确批准。没有自动应用模式。

如果安装后某个技能出问题：`/legal-builder-hub:disable [skill]` 使其静默而不删除文件；`/legal-builder-hub:uninstall [skill]` 完全删除。两者均限于通过此中心安装的社区技能 — 拒绝触碰第一方插件技能。

## 前置条件

- 来自 registry-sync 代理的 Slack 通知需要环境中配置了 Slack MCP 服务器。没有则代理将其摘要写入文件。
- `~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/CLAUDE.md` 中的默认注册表列表初始为空，仅含 `lpm-skills`。通过 `/legal-builder-hub:registry-browser` 添加你信任的注册表，或编辑配置文件。

## 命令列表

| 命令 | 功能 |
|---|---|
| `/legal-builder-hub:cold-start-interview` | 实践画像 + 入门技能包推荐 |
| `/legal-builder-hub:registry-browser [query]` | 搜索已关注的注册表中的技能 |
| `/legal-builder-hub:skill-installer [skill]` | 安装社区技能 |
| `/legal-builder-hub:auto-updater` | 检查已安装技能的更新 |
| `/legal-builder-hub:related-skills-surfacer` | 基于你正在做的事情推荐技能 |
| `/legal-builder-hub:skills-qa [skill]` | 在安装前依据法律技能设计框架评估技能 |
| `/legal-builder-hub:disable [skill]` | 禁用已安装的社区技能而不删除文件 |
| `/legal-builder-hub:uninstall [skill]` | 卸载通过此中心安装的社区技能 |

## 技能列表

| 技能 | 目的 |
|---|---|
| **cold-start-interview** | 实践画像 → 入门技能包 |
| **registry-browser** | 搜索已关注的注册表 |
| **skill-installer** | 白名单门控、获取、展示原始 SKILL.md、信任检查、质量评估、安装社区技能 |
| **uninstall** | 卸载通过此中心安装的社区技能（第一方插件技能不可卸载） |
| **disable** | 禁用社区技能而不删除其文件；稍后可重新启用 |
| **skill-manager** | 参考：`uninstall` 和 `disable` 技能使用的详细卸载/禁用/重新启用工作流程 |
| **skills-qa** | 依据法律技能设计框架评估技能 — 设计、失败模式、信任表面、提示注入启发式扫描 |
| **auto-updater** | 检查更新；显示 diff 和信任审查；仅经明确批准应用 |
| **related-skills-surfacer** | 在任务完成后浮现相关社区技能（直接或通过 hook） |

## 交互式命令 vs. 计划代理

以上命令在你调用时运行 — 用于处理事项时。以下代理按计划运行 — 用于你不在看时发生的变化：

| 代理 | 关注什么 | 默认节奏 |
|---|---|---|
| **registry-sync** | 已关注注册表中新增和更新的技能；按更新偏好发布通知 | 每周 |

## 已关注注册表（默认）

默认白名单预配置了我们已审核的社区注册表。编辑仓库中的 `references/allowlist-default.yaml` 或你的每安装白名单 `~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/allowlist.yaml`，以添加、删除或在限制模式与宽松模式之间切换。

- **lpm-skills** — 法律项目管理（Scott Margetts / LegalOps Consulting） — `github.com/legalopsconsulting/lpm-skills`
- **Lawvable / awesome-legal-skills** — 法律工作 AI 代理技能的精选列表 — `github.com/lawvable/awesome-legal-skills`
- **Lawvable / agent-skills** — 法律工作代理技能的精选合集 — `github.com/lawvable/agent-skills`
- 通过 `/legal-builder-hub:registry-browser` 或编辑白名单添加你自己的

## 它是如何学习的

你在 `~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/CLAUDE.md` 中的实践画像不是静态的 — 它随着你使用插件而改善。中心在每次 `/legal-builder-hub:registry-browser` 和 `/legal-builder-hub:related-skills-surfacer` 时重新读取它，因此调整你的实践类型、行业或已关注注册表能优化未来的推荐。直接编辑文件或在工作变化时重新运行 `/legal-builder-hub:cold-start-interview --redo`。

## 注意事项

- 社区技能在安装前被阅读。你在接受前看到的是**原始** SKILL.md — 非摘要。
- 自动更新默认关闭。如果你信任来源，可按技能打开。
- related-skills-surfacer 在其他插件内运行：当你在做任务时，它检查社区是否有相关内容。
- 企业/律所部署：在 `allowlist.yaml` 中设置 `mode: restrictive` 并填充 `registries`、`publishers` 和 `connectors` 列表。在限制模式下，安装器拒绝从非列表来源获取、分析或安装任何内容。
