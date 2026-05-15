# Codex 使用说明

本仓库上游是 Claude Code 插件 marketplace，同时提供 Codex 适配层。

## Codex 适配入口

Codex skills 位于 `.agents/skills/chinese-legal-*`。当用户提出中国法律相关任务时，优先使用匹配领域的 Codex adapter：

- `chinese-legal-commercial`：商事合同、NDA、供应商协议、SaaS/MSA、续约
- `chinese-legal-privacy`：个人信息保护、DPA、PIA、DSAR、隐私政策
- `chinese-legal-product`：产品上线、营销文案、广告法、业务法务
- `chinese-legal-corporate`：公司法、并购尽调、交割、决议、会议纪要
- `chinese-legal-employment`：劳动用工、解除、假期、调查、规章制度
- `chinese-legal-regulatory`：监管动态、政策差异、合规差距、征求意见稿
- `chinese-legal-ai-governance`：AI 应用、算法安全、科技伦理、AI 供应商
- `chinese-legal-litigation`：诉讼仲裁、案件管理、证据、大事记、文书
- `chinese-legal-ip`：商标、专利、著作权、FTO、开源许可证
- `chinese-legal-law-student`：法考、IRAC、案例摘要、学习计划
- `chinese-legal-clinic`：法律诊所、接待、备忘录、结案移交
- `chinese-legal-builder-hub`：法律技能发现、评估、安装和运营
- `chinese-legal-*watcher` / `*-grid` / `*-radar`：托管工作流 cookbook 的 Codex 入口

## Claude 指令到 Codex 工作流的映射

不要要求用户在 Codex 中输入 Claude Code slash command。上游说明里的：

```text
/<domain>:<command>
```

在 Codex 中应解释为：

1. 读取 `<domain>/CLAUDE.md` 获取领域规则和实践画像要求。
2. 读取 `<domain>/skills/<command>/SKILL.md`。
3. 用 Codex 的文件、网页、文档和自动化工具执行该工作流。

例如 `/commercial-legal:review` 等价于读取 `commercial-legal/skills/review/SKILL.md` 并执行合同审查流程。

## 配置与安全

- Claude Code 的个人画像通常位于 `~/.claude/plugins/config/...`。
- Codex 可使用 `~/.codex/legal-zh/<domain>/CLAUDE.md` 存放自己的实践画像。
- 不要把个人画像、客户材料、token、MCP 授权状态提交进仓库。
- 所有法律输出均为律师审查草稿；法规、案例、期限和监管动态等时效性内容必须用可靠来源核验后再依赖。
