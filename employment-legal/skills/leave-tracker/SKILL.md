---
name: leave-tracker
description: >
  检查进行中的假期，获取截止日期预警和需要做出的决策。仅呈现
  需要采取行动的假期并说明原因——不是状态面板。建议每周运行，
  或每当律师需要知道哪些假期有即将到来的审批、证明或到期截止时使用。
argument-hint: "[无需参数——从假期登记册 leave-register.yaml 读取]"
---

# /leave-tracker

检查所有有法定硬性截止日期的进行中假期，仅呈现需要决策或行动的项目。不是状态面板——告诉你需要做什么及为什么。

## 指令

1. 加载 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/CLAUDE.md` → 管辖地表和假期管理部分。

2. 如果 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/leave-register.yaml` 不存在或无数据，提示律师上传假期电子表格或使用 `/employment-legal:log-leave` 添加条目。

3. 仅对需要行动的假期发出预警。无问题的假期每项一行总结。

4. 检查以下截止日期类型：

| 假期类型 | 关键截止日期 | 法律依据 |
|---|---|---|
| 医疗期 | 医疗期满日（按工作年限3-24个月） | 企业职工患病或非因工负伤医疗期规定 `[法条原文]` |
| 产假 | 产假期满日（98天基础 + 省/直辖市奖励假） | 女职工劳动保护特别规定 `[法条原文]` |
| 年休假 | 年末未休结转截止（一般不跨年结转） | 职工带薪年休假条例第5条 `[法条原文]` |
| 工伤假 | 停工留薪期满日（一般不超过12个月） | 工伤保险条例第33条 `[法条原文]` |
| 婚假 | 各省/直辖市人口与计划生育条例规定 | 省/直辖市规定 |

## 示例

```
/employment-legal:leave-tracker
```

建议每周运行——设置周一上午提醒调用 `/employment-legal:leave-tracker`。自动排期需要单独的集成（日历提醒、定时任务等）；Claude Code 不自行排期。
