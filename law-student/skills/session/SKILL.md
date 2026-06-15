---
name: session
description: >
  在一个科目上运行一场集中的 N 题练习——客观题、主观题或记忆卡片。
  追踪表现并更新学习计划。当用户说"给我出10道[科目]题""做一场[科目]练习"
  "做5张[科目]卡片"或想练习固定数量的题目并让计划随之调整时使用。
argument-hint: "<科目> <n> [--客观题 | --主观题 | --记忆卡片]"
---

# /session

1. 解析 `$ARGUMENTS`——科目和 N。如果缺失，问：
   > 什么科目，多少道题？（例如 `刑法 10` 或 `民法 5 --主观题`。）
2. 加载 `~/.claude/plugins/config/claude-for-legal-zh/law-student/CLAUDE.md` → 考试类型、薄弱科目。
3. 加载 `~/.claude/plugins/config/claude-for-legal-zh/law-student/study-plan.yaml`（如存在）。读取该科目的 `session_history`，将子主题权重倾向学生曾经薄弱的地方。
4. 按方法标志路由：
   - `--客观题`（法考备考科目默认）：加载 `bar-prep-questions` 技能，运行 N 道客观题。适用省级口径处理（见该技能的 `## 省级口径处理`）。每题标注 `[全国统一规定]` 或 `[省级口径]`。
   - `--主观题`：加载 `bar-prep-questions`，运行 N 道主观题。按主观题评分标准批改。
   - `--记忆卡片`：加载 `flashcards` 技能，在 `--drill` 模式下运行 N 张卡片。
5. 逐题运行 N 题。每题后解释对/错，当法域存在差异时标注适用的规则体系。
6. 练习结束时，写入练习结果：
   - 如果 `study-plan.yaml` 存在：按 `study-plan` 技能中的 schema 追加到 `session_history`。
   - 否则：写入 `~/.claude/plugins/config/claude-for-legal-zh/law-student/session-history.yaml`。
7. 报告：
   - 得分：X/N（百分比）
   - 错题：列表附子主题标签
   - 本次练习的薄弱子主题
   - 与该科目既往练习的模式对比（如有 2+ 历史记录）
   - 学习计划现在建议的下一步
