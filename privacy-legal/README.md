# 个人信息保护实务插件

个人信息保护实务工作流：个人信息处理协议审查、个人信息主体权利响应（DSAR）起草、个人信息保护影响评估（PIA）生成、法规与政策差距分析。基于团队实务画像构建，从你的实际隐私政策、个人信息处理协议模板和参考影响评估中学习。

**所有输出均为律师审阅草稿——经引用标注、标记和门控——而非法律结论。** 插件完成工作：读取文件、应用你的操作手册、发现问题、起草备忘录。律师审阅、验证并决定。引用按来源标注，让你知道哪些来自研究工具、哪些需要核实。特权标记保守适用，确保不会意外放弃。后果性行动——提交、发送、执行——需经明确确认方可进行。

## 适用人群

| 角色 | 主要工作流 |
|---|---|
| **个人信息保护律师** | 个人信息处理协议审查、影响评估签批、法规差距分析 |
| **个人信息保护项目经理** | 主体权利响应处理、影响评估接收、供应商隐私审查 |
| **产品律师** | 产品上线影响评估生成 |
| **客服 / 支持** | 主体权利请求一线响应（含升级路径） |

## 首次运行：冷启动访谈

插件访谈你以了解：你是个人信息处理者还是受托处理者、哪些法规实际适用、你在个人信息处理协议中愿意和不愿意同意的条款。然后读取三份种子文件——你的隐私政策（个人信息处理规则）、你的个人信息处理协议模板、一份你认可的影响评估——并学习你的真实立场和内部风格。

你的配置存储在 `~/.claude/plugins/config/claude-for-legal-zh/privacy-legal/CLAUDE.md`，可跨插件更新保留。

```
/privacy-legal:cold-start-interview
```

## 命令

| 命令 | 功能 |
|---|---|
| `/privacy-legal:cold-start-interview` | 冷启动访谈 |
| `/privacy-legal:use-case-triage [activity]` | 此活动是否需要影响评估？快速分类 + 条件 |
| `/privacy-legal:dpa-review [file]` | 依据你的操作手册审查个人信息处理协议（自动检测方向） |
| `/privacy-legal:dsar-response` | 引导处理个人信息主体权利请求并起草响应 |
| `/privacy-legal:pia-generation [feature]` | 按你的内部风格生成个人信息保护影响评估 |
| `/privacy-legal:reg-gap-analysis [regulation]` | 对比新法规与当前政策/实践的差异 |
| `/privacy-legal:policy-monitor` | 每周扫描隐私政策偏差，或针对拟议新实践直接查询 |
| `/privacy-legal:matter-workspace` | 管理事项工作区（仅多客户私人执业）— 新建、列表、切换、关闭、无 |

## 技能

| 技能 | 用途 |
|---|---|
| **cold-start-interview** | 通过访谈 + 种子文件编写 CLAUDE.md |
| **use-case-triage** | 是否需要影响评估 / 能否继续？政策冲突检查 + 交接 |
| **dpa-review** | 双向（个人信息处理者/受托处理者）协议逐条审查 |
| **dsar-response** | 身份验证 -> 系统遍历 -> 豁免 -> 响应草案 |
| **pia-generation** | 按内部格式生成影响评估，含政策一致性检查 |
| **reg-gap-analysis** | 新法规 vs 现状，整改计划 |
| **policy-monitor** | 扫描产出物中的实践偏差；起草政策语言更新 |
| **matter-workspace** | 创建、列表、切换和关闭多客户事项工作区；隔离各客户/事项，避免信息泄露 |

## 快速开始

### 1. 设置

```
/privacy-legal:cold-start-interview
```

准备好：你的公开隐私政策 URL、你的标准个人信息处理协议、一份参考影响评估。

### 2. 分类新功能或处理活动

```
/privacy-legal:use-case-triage "市场部希望使用行为数据进行广告个性化"
```

输出：继续 / 需要影响评估 / 必须进行影响评估 / 停止 —— 附条件表、合法性基础问题和在同一对话中启动影响评估的提议。

### 3. 审查客户个人信息处理协议

```
/privacy-legal:dpa-review customer-dpa.pdf
```

输出：自动检测方向、逐条与操作手册对比、建议修订、政策一致性检查。

### 4. 处理个人信息主体权利请求

```
/privacy-legal:dsar-response
```

引导你完成：分类 -> 验证 -> 定位 -> 豁免 -> 起草。使用配置 CLAUDE.md 中的系统清单。

### 5. 为新功能生成影响评估

```
/privacy-legal:pia-generation "位置分享功能"
```

接收问题 -> 按内部格式生成影响评估 -> 政策差异 -> 条件清单。

## 如何持续学习

你的实务画像位于 `~/.claude/plugins/config/claude-for-legal-zh/privacy-legal/CLAUDE.md` 不是静态的——随着你使用插件不断改进。技能会告知你输出何时使用了应调整的默认值。`policy-monitor` 技能监测政策与实践之间的偏差并提议更新。你可以重新运行设置、直接编辑文件或告知技能记录新立场。

## 文件结构

```
privacy-legal/
├── .claude-plugin/plugin.json
├── .mcp.json
├── CLAUDE.md
├── README.md
├── skills/
│   ├── cold-start-interview/
│   ├── use-case-triage/
│   ├── dpa-review/
│   ├── dsar-response/
│   ├── pia-generation/
│   ├── reg-gap-analysis/
│   ├── policy-monitor/
│   └── matter-workspace/
└── hooks/hooks.json
```

## 注意事项

- 个人信息处理协议审查是双向的：同一技能处理客户协议（保护运营灵活度）和供应商协议（保护数据）。方向自动检测，也可询问。
- 影响评估格式来自你的种子影响评估。如果设置时未提供，使用通用结构——用参考影响评估重新运行设置即可修复。
- 差距分析（`reg-gap-analysis`）处理新法规。政策监测处理内部实践偏差。应对不同变化方向的工具。
- 政策监测需要配置输出文件夹（设置时指定）才能运行扫描。直接查询模式无需输出文件夹即可工作。
