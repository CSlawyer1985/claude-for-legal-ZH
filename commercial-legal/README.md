# 商事合同律师插件

企业法务商事合同工作流：供应商协议审查、保密协议分流、SaaS订阅审查、合同续约追踪、审批上报路由以及业务利益方摘要。围绕通过冷启动访谈生成的团队实务画像构建——插件学习的是*您的*合同手册，而非通用模板。

**每项输出均为供律师审查的草稿——附引用、已标记、设准入——而非法律结论。** 插件完成工作：阅读文件、适用您的合同手册、发现问题、起草备忘录。律师审查、核实并决策。引用按来源标注，以便您知晓哪些源自检索工具、哪些需核实。特权标识审慎适用，避免意外放弃。高后果动作——提交、发送、签署——均设有明确的确认准入。

## 适用对象

| 角色 | 主要工作流 |
|---|---|
| **商事合同律师/法务** | 供应商协议审查、审批上报路由、业务利益方摘要 |
| **合同管理员/法务助理** | 保密协议分流、续约追踪、首轮审查 |
| **采购** | 续约提醒、利益方摘要（作为接收方） |
| **销售/业务拓展** | 保密协议分流，在联系法务前自助 |

## 首次运行：冷启动访谈

首次使用时，插件将通过对话形式对您进行访谈——约十分钟——了解您团队的实际运作方式。询问您的合同手册立场、审批上报规则以及让您在材料到桌时头疼的事项。然后要求您提供5-10份近期已签署协议（越多越好，20份能呈现更清晰的模式），以便实地观察您的立场。

将学习到的内容写入 `~/.claude/plugins/config/claude-for-legal-zh/commercial-legal/CLAUDE.md` —— 一份关于您团队的通俗英语文档，所有其他技能在工作前均会读取。您编辑的是文档，而非配置文件。

```
/commercial-legal:cold-start-interview
```

**合同手册操作方。** 在设置初期，您将被问及是构建**销售方**合同手册（您出售产品/服务；您是供应商；通常使用您的合同模板）、**采购方**合同手册（您向供应商采购；您是客户；通常使用对方合同模板）还是两者。回答将翻转合同手册中几乎所有立场——责任上限、赔偿方向、合同解除权、知识产权归属——所以设置初期就需确定。如果选择两者，设置将先构建销售方；之后运行 `/commercial-legal:cold-start-interview --side purchasing` 构建另一方。您的配置将并行保存双方，审查技能在读取合同手册前先判断适用哪一方。

## 指令

| 指令 | 功能 |
|---|---|
| `/commercial-legal:cold-start-interview` | 运行（或重新运行）冷启动访谈 |
| `/commercial-legal:review [文件]` | 对照您的合同手册审查供应商协议、保密协议或SaaS订阅协议 |
| `/commercial-legal:renewal-tracker` | 未来90天内哪些合同需要续约，以及各合同的终止期限 |
| `/commercial-legal:escalation-flagger` | 将问题路由至适当审批人并起草审批请求 |
| `/commercial-legal:amendment-history [文件]` | 追溯合同从基础协议到各补充协议的变更轨迹 |
| `/commercial-legal:review-proposals` | 逐项审阅来自监控代理的待定合同手册更新提案 |
| `/commercial-legal:matter-workspace` | 管理事项工作空间（仅多客户私人执业）——新建、列表、切换、关闭、无事项 |

## 技能

| 技能 | 用途 |
|---|---|
| **cold-start-interview** | 首次运行访谈，写入 `~/.claude/plugins/config/claude-for-legal-zh/commercial-legal/CLAUDE.md` |
| **vendor-agreement-review** | 完整合同手册对合同偏差分析，附修订文本 |
| **nda-review** | 快速 GREEN/YELLOW/RED 分流，法务仅阅读需要介入的保密协议 |
| **saas-msa-review** | SaaS订阅专属叠加层：自动续约、价格递增、数据迁出、SLA |
| **renewal-tracker** | 终止期限登记册，呈现即将到期的合同 |
| **escalation-flagger** | 将问题匹配至审批上报矩阵，起草审批请求 |
| **stakeholder-summary** | 两段法律审查的商业语言翻译 |
| **amendment-history** | 总结基础协议与其补充协议之间的变更，或追溯特定条款至当前有效表述 |
| **matter-workspace** | 为多客户业务创建、列表、切换和关闭事项工作空间；隔离每个客户/事项，防止上下文泄露 |

## 交互指令 vs 定时代理

以上指令在您调用时运行——适用于您正在处理某事项时。以下代理按计划运行——适用于您未关注时的动态变化：

| 代理 | 监控对象 | 默认频次 |
|---|---|---|
| **renewal-watcher** | 续约登记册——发布未来90天内即将到期的合同，对终止窗口在0-13天内的合同进行红色预警上报 | 每周（周一） |
| **deal-debrief** | 近期已签署协议的合同手册偏差；提示律师在记忆仍在时记录上下文 | 每周（周一） |
| **playbook-monitor** | 偏差日志——当某一条款在滚动12个月窗口内被修改使用5次以上时，提议更新合同手册 | 数据驱动（每次deal-debrief后） |

## 集成

**首先对接法律检索工具——引用安全机制依赖于此。** 没有检索工具，每项引用均标记为 `[需核实]`，每项交付物上方的审查备注将记录来源未经核实。技能无论是否接入检索工具均可运行；yuandian MCP（中国法律法规与案例检索）可将核实工作从您的清单中移除。

随附 `.mcp.json` 中的连接器配置：

- **e签宝** —— 电子签名与签署状态追踪
- **法大大** —— 电子合同生命周期管理
- **yuandian（元典）** —— 中国法律法规与裁判文书语义检索
- **飞书** —— 即时通讯与文档协作
- **Slack** —— 消息搜索与频道阅读
- **Google Drive** —— 文档搜索、读取与获取

接入合同管理系统后：审查时将检查是否存在与同一对方当事人的先前协议，批量加载续约登记册，创建附带审查备忘录的记录。

接入电子签名后：追踪签署状态，按审批顺序路由签署流程。

## 快速入门

### 1. 接受访谈

```
/commercial-legal:cold-start-interview
```

约十分钟。准备好5-10份近期已签署协议以供分享（越多越好，20份能呈现更清晰的模式）。

您的配置存储于 `~/.claude/plugins/config/claude-for-legal-zh/commercial-legal/CLAUDE.md` 并在插件更新后继续生效。

### 2. 审查合同

```
/commercial-legal:review 供应商主协议.pdf
```

输出：对照您的合同手册逐项偏差分析备忘录，附具体修订语言和指定审批人。

### 3. 查看哪些合同即将续约

```
/commercial-legal:renewal-tracker
```

输出：未来90天内具有终止期限的所有合同，按紧急程度分组。

## 如何学习

您在 `~/.claude/plugins/config/claude-for-legal-zh/commercial-legal/CLAUDE.md` 中的实务画像并非一成不变——它会随着您使用插件而持续改进。技能会告知您何时某次输出使用了应予调整的默认值。`playbook-monitor` 代理在您的实务操作偏离合同手册时提议更新。您可以重新运行设置、直接编辑文件或告知某项技能记录新的立场。

## 文件结构

```
commercial-legal/
├── .claude-plugin/plugin.json
├── .mcp.json
├── CLAUDE.md                    # 您的团队实务画像 —— 由冷启动访谈撰写，由您编辑
├── README.md
├── agents/
│   ├── renewal-watcher.md
│   ├── deal-debrief.md
│   └── playbook-monitor.md
├── skills/
│   ├── cold-start-interview/
│   ├── review/
│   ├── review-proposals/
│   ├── vendor-agreement-review/
│   ├── nda-review/
│   ├── saas-msa-review/
│   ├── renewal-tracker/
│   │   └── references/renewal-register.yaml
│   ├── escalation-flagger/
│   ├── amendment-history/
│   ├── matter-workspace/
│   └── stakeholder-summary/
└── hooks/hooks.json
```

## 说明

- 在大多数审查中，插件假设您是**客户**（采购方）。当您是供应商（销售方）时，请予以标注，审查将翻转合同手册的立场。
- 保密协议分流专为非法务人员自助设计。GREEN 表示"可转签署"。它不会进行协商。
- 续约追踪仅对通过本插件审查或从合同管理系统批量加载的合同有效。安装本插件之前已签署的合同需进行一次初始扫描。
