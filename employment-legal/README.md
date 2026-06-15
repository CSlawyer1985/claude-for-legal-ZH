# 中国劳动法插件

中国企业劳动法实务工作流：用工审查、解除风险评估、劳动关系认定、劳动规章制度起草与更新、假期管理、工资支付合规问答。基于 cold-start 时建立的管辖范围画像——插件知道你在中国哪些省/直辖市有员工，以及各地口径差异。

**每一份输出均为供律师审查的草案——附引用来源、标注风险、设审查门禁——不是法律结论。** 插件完成工作：读取文件，应用你的实务规则，发现问题，起草备忘录。律师审查、核实、决策。引用附来源标签，方便你判断哪些来自检索工具、哪些需要核实。保密标记谨慎适用，不因疏忽导致弃权。关键动作——发文、发送、签署——均设有显式确认门禁。

## 适用对象

| 角色 | 主要工作流 |
|---|---|
| **劳动法律师/法务** | 解除审查、劳动规章制度起草、工资工时分析 |
| **HRBP** | 用工审查、规章制度咨询、一线工资工时问答 |
| **法务负责人/GC** | 高风险解除和经济性裁员的上报接收 |

## 首次运行：cold-start

询问你在哪些省/直辖市有员工，读取你的劳动规章制度和三份近期解除备忘录，建立省/直辖市口径差异的上报表。

```
/employment-legal:cold-start-interview
```

你的配置存储于 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/CLAUDE.md`，不受插件更新影响。

## 前置条件

- **持久化数据路径。** 假期登记册、调查日志、跨省用工跟踪表写入 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/`——版本无关路径，不受插件更新影响。这些文件含有人事敏感信息——请确保该目录已备份且权限受控。
- **法律检索工具。** 本插件中的技能故意不存储实体法律规则（最低工资标准、竞业限制经济补偿、经济补偿金计算基数、各地特殊规定等）。每一省/直辖市的口径差异在审查时实时检索并引用。请确保会话已接入你依赖的检索工具（yuan dian MCP、联网搜索、内部参考资料）。
- **外部律师。** 涉及地方司法口径争议或新型用工问题的法律意见，应征询当地执业律师意见。

## 技能

| 技能 | 功能 |
|---|---|
| `/employment-legal:cold-start-interview` | Cold-start 访谈——从劳动规章制度+解除备忘录中学习管辖范围与上报规则 |
| `/employment-legal:hiring-review` | 录用通知书+竞业限制审查、管辖地检查 |
| `/employment-legal:termination-review` | 解除审查，含高风险标记检测 |
| `/employment-legal:policy-drafting [topic]` | 起草劳动规章制度，含各省/直辖市补充规定 |
| `/employment-legal:wage-hour-qa [question]` | 工资工时或一般劳动法问答，管辖地差异适配 |
| `/employment-legal:worker-classification` | 劳动关系的认定——劳社部发〔2005〕12号三要素分析 |
| `/employment-legal:expansion-kickoff [省/直辖市]` | 启动跨省/直辖市用工规划 |
| `/employment-legal:expansion-update [省/直辖市]` | 更新进行中的跨省用工跟踪表 |
| `/employment-legal:investigation-open` | 启动新的内部调查事项 |
| `/employment-legal:investigation-add` | 向进行中的调查添加文件、访谈纪要或观察 |
| `/employment-legal:investigation-query` | 对进行中的调查日志提问 |
| `/employment-legal:investigation-memo` | 起草或更新保密调查备忘录 |
| `/employment-legal:investigation-summary` | 从调查备忘录起草针对不同受众的摘要 |
| `/employment-legal:leave-tracker` | 检查未结假期事项，法定期限预警和必要决策提醒 |
| `/employment-legal:log-leave` | 将新的假期记录添加到假期登记册 |
| `/employment-legal:matter-workspace` | 管理事项工作区（仅多客户场景适用） |
| **handbook-updates** | 对比劳动规章制度修改前后差异，标注省/直辖市补充条款影响 |

## 交互式技能与定时代理人

上述技能由你主动调用——用于处理具体事项。以下代理人按计划自动运行——用于持续监控：

| 代理人 | 监控内容 | 默认频率 |
|---|---|---|
| **leave-tracker** | 涉及法定硬性期限的未结假期事项——年休假（职工带薪年休假条例）、产假（女职工劳动保护特别规定）、病假（企业职工患病或非因工负伤医疗期规定）、婚假等；在期限届满前发出决策预警 | 每周（周一） |

## 如何学习与进化

你的实践画像存储在 `~/.claude/plugins/config/claude-for-legal-zh/employment-legal/CLAUDE.md`——它不是静态的，随你使用插件而优化。技能会提示你某个输出使用了应调优的默认值。你可以重新运行设置、直接编辑文件，或告诉技能记录新的立场。

## 注意事项

- 管辖地差异是本插件的核心价值。插件知道北京、上海、广东、浙江等地在竞业限制经济补偿、最低工资、医疗期计算等方面的不同口径。
- 解除审查不能替代与HR和业务负责人的沟通——它是一份检查清单，用于捕捉容易被遗漏的风险点。
- 工资工时问答引用规则原文，但标注疑难问题供人工复核。劳动关系认定结论具有实质性法律后果。
- 所有输出中的法条引用均附来源溯源标签（`[法条原文]`/`[yuandian检索]`/`[模型知识 — 需验证]`等），律师应在信赖前核实。
