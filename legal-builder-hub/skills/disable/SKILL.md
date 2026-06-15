---
name: disable
description: >
  禁用一个通过中心安装的社区技能而不移除其文件。当用户想临时停用一个
  社区技能（"禁用[技能]"）、保持配置但停止其 hooks 触发或重新启用
  之前已禁用的技能时使用。
argument-hint: "[技能名称]"
---

# /disable

针对命名技能运行 `skill-manager` 参考技能中的 `disable` 工作流。

禁用做什么：

- 将技能的 `SKILL.md` 重命名为 `SKILL.md.disabled`，使 Claude 不再将其发现为活跃技能。文件、参考、模板和配置保留在原位。
- 如果技能附有 `hooks/hooks.json` 中的 hooks，也将该文件重命名为 `hooks.json.disabled`，使技能禁用期间无自动触发器触发。
- 将操作记录到 `~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/install-log.yaml`。

安全规则：

1. **仅禁用通过本中心安装的社区技能。** 与卸载相同的检查——查阅安装日志和 CLAUDE.md 已安装表。
2. **绝不禁用第一方插件的技能。** 不可触碰。
3. **在重命名前确认。** 展示路径，获取明确同意。

重新启用：再次以相同技能名称运行该命令——skill-manager 工作流识别已禁用的技能并将重命名反转回来。

> 详细的卸载、禁用和重新启用工作流在 `skill-manager` 参考技能中——在进行实质性工作前加载它。
