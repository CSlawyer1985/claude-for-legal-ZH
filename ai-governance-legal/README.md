# AI 治理实务插件

企业内部 AI 治理律师工作流：应用场景分类、AI 影响评估（算法安全评估/科技伦理审查）、AI 供应商审查、法规与政策差距分析。基于团队实务画像构建，从你的 AI 使用政策、参考影响评估和关键 AI 供应商协议中学习。

**所有输出均为律师审阅草稿——经引用标注、标记和门控——而非法律结论。** 插件完成工作：读取文件、应用你的操作手册、发现问题、起草备忘录。律师审阅、验证并决定。引用按来源标注，让你知道哪些来自研究工具、哪些需要核实。特权标记保守适用，确保不会意外放弃。后果性行动——提交、发送、执行——需经明确确认方可进行。

## 适用人群

| 角色 | 主要工作流 |
|---|---|
| **个人信息保护律师 / AI 治理律师** | 影响评估、AI 供应商审查、法规差距分析 |
| **产品律师** | 应用场景分类、含 AI 组件的上线审查 |
| **总法律顾问 / 法律运营** | AI 政策治理、升级、董事会层面问题 |
| **采购 / 法律** | AI 供应商合同审查 |

## 首次运行：冷启动访谈

插件访谈你以了解：你是 AI 构建者、部署者还是两者兼有——哪些监管制度实际适用——你的应用场景红线是什么——以及好的影响评估在这里是什么样的。然后读取你的种子文件并学习你的真实立场和内部风格。

```
/ai-governance-legal:cold-start-interview
```

## 命令

| 命令 | 功能 |
|---|---|
| `/ai-governance-legal:cold-start-interview` | 冷启动访谈——编写你的实务画像 |
| `/ai-governance-legal:use-case-triage [use case]` | 对照你的登记册分类应用场景（批准 / 有条件 / 从未） |
| `/ai-governance-legal:aia-generation [use case]` | 按你的内部风格运行 AI 影响评估（算法安全评估/科技伦理审查） |
| `/ai-governance-legal:vendor-ai-review [vendor/file]` | 对照你的立场审查 AI 供应商协议 |
| `/ai-governance-legal:reg-gap-analysis [regulation]` | 对比新法规或指引与当前政策/实践的差异 |
| `/ai-governance-legal:policy-monitor` | 每周扫描 AI 政策偏差，或针对拟议新实践直接查询 |
| `/ai-governance-legal:policy-starter` | 从已发布的示范政策（生成式人工智能服务管理办法、科技伦理审查办法、算法推荐管理规定、行业自律公约）起草 AI 使用政策初稿，适配你的实务画像——供律师审阅的草案，非最终政策 |
| `/ai-governance-legal:matter-workspace` | 管理事项工作区（仅多客户私人执业）— 新建、列表、切换、关闭、无 |

## 技能

| 技能 | 用途 |
|---|---|
| **cold-start-interview** | 通过访谈 + 种子文件编写 `~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/CLAUDE.md` |
| **use-case-triage** | 对照登记册分类应用场景；标注缺失的评估 |
| **aia-generation** | 按内部格式生成 AI 影响评估（算法安全评估/科技伦理审查） |
| **vendor-ai-review** | 针对治理立场进行 AI 特定供应商合同审查 |
| **reg-gap-analysis** | 新法规/指引 vs 现状，整改计划 |
| **policy-monitor** | 扫描产出物中的实践偏差；起草 AI 政策语言更新 |
| **policy-starter** | 从已发布的示范政策生成 AI 使用政策初稿，适配你的实务画像——供律师审阅的草案，非最终政策 |
| **matter-workspace** | 创建、列表、切换和关闭多客户事项工作区；隔离各客户/事项，避免信息泄露 |

## 快速开始

### 1. 设置

```
/ai-governance-legal:cold-start-interview
```

准备好（如存在）：你的 AI 或可接受使用政策、一份既往影响评估、关键 AI 供应商协议、模型清单或已批准工具列表。

你的配置存储在 `~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/CLAUDE.md`，可跨插件更新保留。

### 2. 分类新应用场景

```
/ai-governance-legal:use-case-triage "销售团队希望使用 AI 自动评分潜在客户"
```

输出：风险层级、登记册匹配或差距、所需条件、是否需要影响评估。

### 3. 运行影响评估

```
/ai-governance-legal:aia-generation "面向 HR 的 AI 简历筛选"
```

接收问题 -> 按内部格式生成影响评估 -> 政策一致性检查 -> 缓解条件。

### 4. 审查 AI 供应商协议

```
/ai-governance-legal:vendor-ai-review openai-terms.pdf
```

输出：逐条与你的立场对比、建议修订、需升级的差距。

## 插件三角：AI 治理 ↔ 产品律师 ↔ 个人信息保护

这三个插件设计为协同工作。AI 治理是第三支柱。

- **产品律师**检测到产品上线含 AI 组件 -> 交接至 `/ai-governance-legal:use-case-triage` 和 `/ai-governance-legal:aia-generation`
- **个人信息保护**检测到 AI 应用场景涉及个人数据 -> 交接至 `/privacy-legal:pia-generation`（如插件已安装）
- **AI 治理**检测到影响评估涉及数据保护问题 -> 交接至 `/privacy-legal:pia-generation`（如插件已安装）

交接是明确的：每个插件标注何时需要另一个插件并说明需回答的问题。

## 文件结构

```
ai-governance-legal/
├── .claude-plugin/plugin.json
├── .mcp.json
├── CLAUDE.md
├── README.md
└── skills/
    ├── cold-start-interview/
    ├── use-case-triage/
    ├── aia-generation/
    ├── vendor-ai-review/
    ├── reg-gap-analysis/
    ├── policy-monitor/
    ├── policy-starter/
    └── matter-workspace/
```

## 如何持续学习

你的实务画像位于 `~/.claude/plugins/config/claude-for-legal-zh/ai-governance-legal/CLAUDE.md` 不是静态的——随着你使用插件不断改进。技能会告知你输出何时使用了应调整的默认值。`policy-monitor` 技能监测 AI 治理政策与实践之间的偏差并提议更新。你可以重新运行设置、直接编辑文件或告知技能记录新立场。

## 注意事项

- 差距检查（`reg-gap-analysis`）处理新法规。政策监测处理内部实践偏差。应对不同变化方向的工具。
- 政策监测需要配置输出文件夹（设置时指定）才能运行扫描。直接查询模式无需输出文件夹即可工作。
- 应用场景分类的效果取决于登记册的质量。在设置访谈中花时间把红线定对——它们驱动一切。
- 影响评估格式来自你的种子评估。如果设置时未提供，使用基线结构——用参考文献重新运行设置可改进。
- AI 构建者和部署者的义务分开处理。如果你两者都是，技能会在每个任务中询问你戴哪顶帽子。
- 差距分析是手动的（你指向某项法规或指引文件）。如需自动监测，如 `regulatory-legal` 插件已安装可搭配使用。
