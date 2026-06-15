---
name: uninstall
description: >
  卸载通过本中心安装的社区技能。删除文件前确认，拒绝触碰第一方插件技能，
  并记录每次操作。当用户想完全移除某个社区技能（"卸载[技能]"、
  "移除这个技能"）而非仅禁用它时使用。
argument-hint: "[技能名称]"
---

# /uninstall

针对命名技能运行 `skill-manager` 参考技能中的 `uninstall` 工作流。

安全规则：

1. **仅卸载通过本中心安装的社区技能。** 检查
   `~/.claude/plugins/config/claude-for-legal-zh/legal-builder-hub/install-log.yaml`
   和 CLAUDE.md 已安装入门包表。如果该技能未记录在其中，拒绝并告知用户。
2. **绝不卸载第一方插件的技能。** claude-for-legal 附带的 12 个核心插件
   对此命令是不可触碰的。如果命名技能解析到这些插件之一的路径内，拒绝。
3. **删除文件前确认。** 向用户展示将要删除的每条路径。
   仅在明确输入 `yes` 后才继续。
4. **记录卸载操作。** 将 `action: uninstall` 和时间戳追加到 `install-log.yaml`，
   使审计追踪完整保留。

如果用户想阻止技能运行但保留文件（例如为以后重新启用，或保留配置），建议使用 `/legal-builder-hub:disable`。

> 详细的卸载、禁用和重新启用工作流在 `skill-manager` 参考技能中——在进行实质性工作前加载它。
