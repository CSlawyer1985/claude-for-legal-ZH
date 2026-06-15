---
name: renewal-tracker
description: >
  展示具有即将到来的取消截止日期的合同，在通知窗口关闭前发出预警，
  基于维护的续约登记册运行。当用户询问"什么即将续约""哪些续约即将到期"
  "我们是否错过了取消窗口""将此添加到续约追踪器"时使用，或按计划运行。
  接收来自 saas-msa-review 的交接数据。
argument-hint: "[--days N 变更窗口 | --missed 查看已过期的窗口]"
---

# /renewal-tracker

呈现哪些合同即将续约以及必须在何时之前取消。

## 指令

1. **读取 `~/.claude/plugins/config/claude-for-legal-zh/commercial-legal/renewal-register.yaml`**（配置目录——插件更新后仍保留）。

2. **默认模式：** 模式2——未来90天内即将到来的事项，按紧急程度分组。

3. **`--days N`：** 变更窗口。

4. **`--missed`：** 模式4——已过期的取消截止日期。

5. **如果登记册为空且合同管理系统已连接：** 提供模式3——扫描合同管理系统获取当前协议并批量加载。

6. **输出包含建议操作：** 联系谁（每条登记记录中的业务负责人）、哪些具有无上限定价。

## 示例

```
/commercial-legal:renewal-tracker
/commercial-legal:renewal-tracker --days 180
/commercial-legal:renewal-tracker --missed
```

---

## 目的

没有人读合同第二遍。续约日期在审查时提取一次，然后存于某处——最好是在取消截止日期前45天大声提醒，而不是45天后。

## 登记册

位于 `~/.claude/plugins/config/claude-for-legal-zh/commercial-legal/renewal-register.yaml`。

```yaml
- counterparty: "Acme SaaS Inc."
  agreement: "Acme平台订阅协议"
  signed_date: 2025-06-15
  initial_term_end: 2026-06-15
  current_term_end: 2026-06-15
  renewal_mechanism: "自动续约年度"
  notice_period_days: 60
  notice_method: "email"
  transit_buffer_days: 0
  cancel_by_calendar: 2026-04-16
  cancel_by_effective: 2026-04-16
  send_by_effective: 2026-04-16
  cancel_by_roll_note: ""
  cancel_by_provenance: "[模型计算 — 对照通知条款核实]"
  price_on_renewal: "当时价目表（无上限）"
  annual_value: 48000
  business_owner: "jane@company.com"
  clm_id: "IC-12345"
  status: "active"
  notes: "定价无上限——续约前重审。替代供应商：X, Y。"
```

**通知送达时间。** 计算 `send_by_effective = cancel_by_effective - transit_buffer_days`，以 `send_by_effective` 触发预警。

**滚动续约。** 存储 `initial_term_end` 供记录，但从 `current_term_end` 计算 `cancel_by_*`。

## 工作日检查

每个取消截止日期必须回退至最后一个工作日。中国法下，以合同约定的管辖法域确定节假日范围。记录 `cancel_by_calendar` 和 `cancel_by_effective` 两个日期。以有效日期触发预警。

## 模式

### 模式1：录入续约（来自审查的交接）

当SaaS审查或供应商协议审查发现续约条款时，交接记录。追加至登记册。

### 模式2：即将到来的事项

**默认回顾窗口：** 未来90天。紧急程度分组使用半开区间：
- 🔴 **0-13天**
- 🟠 **14-44天**
- 🟡 **45-89天**

```markdown
## 续约——未来90天

### 🔴 取消截止日期在0-13天内

| 对方当事人 | 取消截止日 | 续约日 | 年度金额 | 负责人 | 备注 |
|---|---|---|---|---|---|

### 🟠 取消截止日期在14-44天内

[同上表格]

### 🟡 取消截止日期在45-89天内

[同上表格]

---

**建议操作：**
- [ ] [对方当事人] — 联系 [业务负责人]：我们还要这个吗？
- [ ] [对方当事人] — 定价无上限；在失去谈判优势前获取替代报价
```

### 模式3：扫描合同管理系统/电子签章工具填充登记册

如果MCP已连接且登记册为空或过期：查询合同管理系统，扫描电子签章工具。

### 模式4：错过的窗口（坏消息报告）

```markdown
## 错过的取消窗口

| 对方当事人 | 取消截止日为 | 续约日 | 状态 |
|---|---|---|---|

**选项：**
- 协商逾期取消（很少成功但值得一问）
- 接受续约，现在标记下一年的取消截止日
- 检查协议中是否有其他终止权利
```

## 关卡：接受或拒绝续约

追踪续约日期是研究。*行动*——发送不续约通知、让自动续约生效或签署续约——是产生法律后果的步骤。如果角色为非律师，先检查是否已与律师审阅。

## 集成：续约提醒代理

续约提醒代理按计划运行本技能（默认每周），将"即将到来的事项"报告发布到审查指引中配置的频道。

## 本技能不做的事

- 不取消合同。告知你何时应做决定。
- 不决定是否续约。呈现截止日期和业务负责人。
- 不阅读合同以查找续约日期——这在审查时完成。
