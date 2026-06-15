---
name: gaps
description: 开放差距跟踪器——已标记但尚未关闭的事项。适用于用户询问"有哪些开放的差距"、"差距跟踪器"、"整改状态"，或想关闭（--close GAP-ID）或风险接受（--accept GAP-ID）一个已跟踪的差距时。
argument-hint: "[可选: --close GAP-ID | --accept GAP-ID]"
---

# /gaps

1. 读取位于 `~/.claude/plugins/config/claude-for-legal-zh/regulatory-legal/gap-tracker.yaml` 的差距跟踪器。
2. 如果 `--close`：标记差距已关闭，附解决方案说明。
3. 如果 `--accept`：记录风险接受理由和接受人，状态 → risk-accepted。
4. 否则：按年龄和重要度报告开放差距。

> 详细的跟踪器 schema、状态报告格式、负责人通知逻辑（逐次发送确认，无例外）、提醒频率、关闭/风险接受模式以及后果性行动闸门位于 **gap-surfacer** 参考技能中——在实质工作前加载它。
