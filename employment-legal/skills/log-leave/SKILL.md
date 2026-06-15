---
name: log-leave
description: >
  向假期登记册添加新假期条目，录入开始追踪截止日期所需的最低信息。
  当员工开始休假且你希望追踪器从第一天起监控审批、证明和到期时间时使用。
argument-hint: "[描述假期——员工/岗位、类型、管辖地、开始日期]"
---

# /log-leave

向 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/leave-register.yaml` 添加新假期条目，录入开始追踪截止日期所需的最低信息。当员工开始休假且你希望追踪器从第一天起监控时间节点时使用。

## 指令

1. 读取 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/CLAUDE.md` → 管辖地表和假期管理部分。

2. 一次性询问以下全部内容——不要逐个滴灌：

   > 几个快速问题以设置假期追踪：
   >
   > - 员工姓名或岗位（可匿名）
   > - 工作地？（省/直辖市——这决定适用哪些规则）
   > - 假期类型：病假/医疗期 / 产假（含各地奖励假） / 年休假 / 工伤假 / 婚假 / 育儿假 / 陪产假
   > - 假期开始日期
   > - 是否为间断性休假？
   > - 预计返岗日期（如已知——不知则留空）
   > - 请假申请是否已审批？如已审批，何时？
   > - 医疗证明是否已提交？（医疗期/病假需提供）如已提交，日期？

3. 使用 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/CLAUDE.md` 中的管辖地表，查找该管辖地该假期类型的适用假期权益（天数/月数）。主要法律依据：
   - 医疗期：企业职工患病或非因工负伤医疗期规定 `[法条原文]`（按工作年限3-24个月）
   - 产假：女职工劳动保护特别规定第7条 `[法条原文]`（98天基础）+ 各省/直辖市人口与计划生育条例奖励假
   - 年休假：职工带薪年休假条例第3条 `[法条原文]`（按累计工作年限5/10/15天）
   - 工伤假：工伤保险条例第33条 `[法条原文]`（停工留薪期一般不超过12个月）

4. 根据提供的信息计算首个即将到来的截止日期：
   - 请假申请尚未审批 → 截止日期为审批完成前（提醒管理者及时审批）
   - 医疗证明要求但未收到 → 提醒管理者索要
   - 假期到期前 → 在75%用尽时预警

5. 将新条目写入 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/leave-register.yaml`。如文件不存在，创建之。使用 YAML 格式：
   ```yaml
   - employee: "[员工/岗位]"
     type: "[假期类型]"
     jurisdiction: "[省/直辖市]"
     start_date: "[YYYY-MM-DD]"
     expected_return: "[YYYY-MM-DD或空]"
     intermittent: [true/false]
     approved: [true/false]
     approval_date: "[YYYY-MM-DD或空]"
     cert_submitted: [true/false]
     cert_date: "[YYYY-MM-DD或空]"
     notes: "[备注]"
   ```

6. 一行确认：
   > "已登记。[员工/岗位] — [假期类型] — [管辖地] — 始于[日期]。首个截止日期：[什么和何时]。假期追踪器将自动预警。"

## 示例

```
/employment-legal:log-leave
```

```
/employment-legal:log-leave
张工（高级工程师，在北京工作）今天开始休病假，需要手术。
连续休假。请假已审批，尚未提交医疗证明。
```
