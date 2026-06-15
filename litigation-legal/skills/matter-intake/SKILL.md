---
name: matter-intake
description: >
  登记新案件——统一问题涵盖标识信息、利益冲突检索、来源、
  风险分流、重要性、外聘律师、内部负责人、证据保全和关键日期；
  写入 matter.md 和 history.md 并在 _log.yaml 中追加结构化行。
  当用户说"新案件"、"登记这个案件"或需要将新案件纳入案件组合时使用。
argument-hint: "[可选案件名称]"
---

# /matter-intake

1. 加载 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` → 风险校准（用于分流）、执业背景（用于上下文、冲突检索方法）、相关方（用于抄送人员）。
2. 按以下工作流操作。
3. 运行统一登记：标识信息、利益冲突检索、来源、风险分流、重要性、外聘律师、内部负责人、证据保全、关键日期、初始姿态。
4. 从案件名称生成代号（小写、连字符、年份）。
5. 创建 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/[slug]/matter.md` —— 完整记述式登记。
6. 创建 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/[slug]/history.md` —— 以本次登记作为首条记录。
7. 追加结构化行至 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/_log.yaml`。
8. 与用户确认："这是我将写入的行——需要修改吗？"

---

# 案件登记

## 目的

每个新案件统一登记，确保案件组合具有可比性。`_log.yaml` 中统一的行让组合状态技能可以汇总。`matter.md` 中的记述捕获行格式无法表达的内容。在此播种的历史文件成为事件记录。

## 加载上下文

- `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` —— 风险校准（分流门槛、重要性、和解阶梯）、执业背景（相关方、外聘律师库）。
- `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/_log.yaml` —— 确认代号唯一性。

## 登记内容

### 1. 标识信息

- 案件名称（常用指代，如"某某公司诉我方 2026 合同纠纷案"）
- 对方当事人
- 案件类别：`合同纠纷 | 劳动争议 | 知识产权 | 行政监管 | 内部调查 | 产品责任 | 其他`
- 案由（依据最高人民法院《民事案件案由规定》）`[法条原文]`
- 我方地位：`原告 | 被告 | 申请人 | 被申请人 | 被调查人`
  - 如实践画像的默认角色已设定，据此预填充并确认。如默认角色为"因案而异"，直接询问。
- 管辖（受理法院、仲裁机构或行政机关）

### 2. 利益冲突检索

在进一步操作前，按 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` → 利益冲突审查运行冲突检索步骤。

- **状态：** `已通过 | 待定 | 未运行 | 已豁免`
- **方式：** 匹配 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 声明的方式。
- **审查人：** 姓名/团队/律所
- **审查日期：** YYYY-MM-DD
- **审查对象：** 简要列出实际运行的特定名称/主体（对方、已知关联方、对方律师（如已知）、关键证人）。数量少没关系；"无"不行。
- **备注：** 任何标注但已通过的事项。

各状态的行为：

- `已通过` → 继续。
- `待定` → 继续登记；在 `matter.md` 和日志行中显著标注冲突尚未解决；每次 `/matter-update` 和 `/portfolio-status` 中再次提示，直至解决。
- `已豁免` → 罕见；需有冲突豁免理由（起草豁免书超出本技能——记录其存在、签署人和存放位置）。
- `未运行` → **停止。此处为门禁。** 冲突姿态解决前不创建 `matter.md`、`history.md` 或 `_log.yaml` 条目。三条可接受路径：

  **路径1 —— 现在运行冲突检索。** 暂停本登记。按 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 的冲突审查完成。返回时带 `status: cleared` 或 `status: waived` 附理由。

  **路径2 —— 标注待定，附负责人+截止日期。** 仅在 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 的冲突审查声明允许平行登记时可用。记录：谁在运行冲突检索、预计何时返回、检查哪些主体。登记继续；案件行携带 `conflicts.status: pending`；`/portfolio-status` 每次运行均标注；`/matter-update` 重复提示直至解决。

  **路径3 —— 附书面理由绕过。** 仅在用户明确确认绕过时可用。在 `conflicts.override` 中记录：

  ```yaml
  conflicts:
    status: not-run
    override:
      by: [用户名]
      date: [YYYY-MM-DD]
      rationale: [为什么绕过冲突检索——永久记录；不会自动过期]
  ```

  此字段在每次 `/portfolio-status`、每次 `/matter` 简报和每次 `/matter-update` 中可见，直至被移除。本技能不会自动移除——仅在用户明确编辑 `_log.yaml` 且在冲突实际清除后。

### 3. 来源

该案件如何进入？
- `律师函 | 起诉状送达 | 调查令/协查通知 | 行政监管问询 | 内部报告 | 诉前威胁`

### 4. 风险分流——对照事务所校准

- 严重性：高 | 中 | 低（参考 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 的严重性分级）
- 可能性：高 | 中 | 低（参考可能性分级）
- 综合风险评级（矩阵结果）：高 | 中 | 低 | 危急
- 赔偿敞口范围（最佳估计）
- 非金钱敞口（禁令？行政处罚？声誉影响？先例效应？）

### 5. 重要性

对照 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 中的事务所门槛：
- `需计提 | 已披露 | 监控中 | 不适用`

### 6. 外聘律师

- 律所
- 主办合伙人
- 委托合同状态：`已签署 | 待定 | 无`
- 预算授权：金额和审批人

如风险为中及以上且未指定外聘律师——标注。

### 7. 内部负责人

来自 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/CLAUDE.md` 执业背景——哪些内部相关方需要参与？
- 业务负责人
- HR 负责人（如是劳动争议）
- 公关联系人（如有声誉风险）
- 信息安全负责人（如涉及数据或网络安全）
- 其他

### 8. 证据保全

- 是否已发出？如是：日期、范围、保管人（姓名列表）。
- 下次刷新日期（默认：发出后六个月；按案件调整）。
- 如否且本案件为已进入诉讼或合理预期将进入诉讼：紧急标注。

### 9. 关键日期

- 答复期限（答辩、异议、反诉）
- 下次开庭/庭前会议
- 诉讼时效截止日（如适用）
- 任何行政监管期限

### 10. 初始姿态

一段话理论：
- 我方案件逻辑是什么？
- 对方案件逻辑是什么？
- 关键事实是什么？
- 初始姿态：`积极应对 | 寻求和解 | 调查中 | 观望`

## 写入输出

### 代号

小写、连字符、末尾年份。示例：`acme-v-us-2026`、`employment-smith-2026`、`ftc-inquiry-2026`。

写入前在 `_log.yaml` 中确认代号唯一。

### `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/[slug]/matter.md`

```markdown
[工作成果标头——根据插件配置 ## 输出——因角色不同；见 `## 使用者`]

# [案件名称]

**代号：** [slug]
**立案/登记日期：** [YYYY-MM-DD]
**我方地位：** [原告/被告等]
**状态：** [status]

---

## 标识信息

[对方、管辖、案件类别、案由、来源]

## 利益冲突

**状态：** [已通过 / 待定 / 未运行 / 已豁免]
**方式：** [事务所/外聘律师/其他]
**审查人：** [姓名]
**审查日期：** [YYYY-MM-DD]
**审查对象：** [已运行的实体]
**备注：** [任何标注但已通过的事项、豁免引用（如适用）]

## 风险分流

**严重性：** [分级] —— [理由，引用事务所严重性定义]
**可能性：** [分级] —— [理由]
**风险评级：** [高/中/低/危急]
**敞口：** [金额范围 + 非金钱敞口]

## 重要性

[需计提/已披露/监控中/不适用——附计提金额、披露位置或不适用理由]

## 外聘律师

[律所、主办人、委托状态、预算]

## 内部负责人

[相关方及各自参与理由]

## 证据保全

[状态、日期、范围]

## 关键日期

[列表]

## 初始理论

[一段：我方案件逻辑、对方案件逻辑、关键事实、初始姿态] `[需审查——登记时的理论是工作假设；在任何以此假设为前提的诉讼行为或实质性沟通前应经外聘律师确认]`

## 待解决问题

[任何尚未知晓但重要的事项——如"保险通知待定"、"是否涵盖X事项尚不明确"]
```

### `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/[slug]/history.md`

播种历史文件，以本次登记作为第零条记录：

```markdown
# 历史记录：[案件名称]

仅追加的事件日志。最新记录在最前。

---

## [YYYY-MM-DD] —— 案件立案/登记

[来源、由谁引入、初始分流摘要、外聘律师指定情况、证据保全发出情况（是/否）。]
```

### 追加至 `~/.claude/plugins/config/claude-for-legal-zh/litigation-legal/matters/_log.yaml`

按模式添加行。示例：

```yaml
- id: acme-v-us-2026
  name: "某某公司诉我方合同纠纷案"
  type: contract
  role: defendant
  counterparty: "某某公司"
  jurisdiction: "北京市朝阳区人民法院"
  status: active
  stage: pleadings
  source: complaint-served
  outside_counsel:
    firm: "某某律师事务所"
    lead: "张律师"
    email: "zhang@example.com"
    engagement: signed
  conflicts:
    status: cleared
    method: firm
    cleared_by: "内部法务"
    cleared_date: 2026-04-20
    override:
      by: null
      date: null
      rationale: null
  risk: high
  materiality: reserved
  exposure_range: "200万-500万元"
  internal_owners:
    business_lead: "业务负责人"
    hr_partner: null
    comms_contact: null
  legal_hold:
    issued: true
    issued_date: 2026-02-15
    scope: "销售部门 2023-2026"
    custodians: ["张三", "李四", "王五"]
    last_refresh: 2026-02-15
    next_refresh: 2026-08-15
    released: null
  related_matters: []
  opened: 2026-04-20
  next_deadline: 2026-05-15
  last_updated: 2026-04-20
  path: matters/acme-v-us-2026/
```

## 写入前确认

向用户展示日志行和 matter.md 内容：

> 这是我将写入的内容。在正式写入前，请标注任何错误或不足之处。

## 以下一步决策树收尾

以 CLAUDE.md `## 输出` 中的下一步决策树收尾。根据本技能刚产生的内容自定义选项——五个默认分支（起草X、上报、获取更多事实、观察等待、其他选择）是起点而非锁定项。决策树本身就是输出；由律师选择。

## 本技能不做什么

- **自行运行利益冲突检索。** 记录结果、状态、方式和审查实体。实际审查在事务所实践画像声明的不论什么系统（或判断）中完成。如用户说"已通过"，本技能按面值接受并记录元数据。
- 决定初始理论。记录用户所说的；不自行发明。
- 发出证据保全通知。如缺失则标注。用户发出。
