# Codex 安装指南

本仓库原生支持 Claude Code 插件，同时提供 Codex Desktop / Codex CLI 可用的适配技能。

## 这是什么

`claude-for-legal-ZH` 的原始形态是 **Claude Code 插件 marketplace**，不是 Claude 网页版或云端版插件。

Codex 适配层不会重写法律工作流，而是复用原仓库中的：

- 各领域 `CLAUDE.md`
- 各领域 `skills/*/SKILL.md`
- `managed-agent-cookbooks/*`

Codex adapter 只负责把自然语言请求路由到对应工作流。

## 一键安装到 Codex

在仓库根目录运行：

```bash
scripts/install-codex.sh
```

默认使用符号链接安装到：

```text
~/.codex/skills
```

如果你希望复制一份而不是链接：

```bash
scripts/install-codex.sh copy
```

安装后请重启 Codex Desktop 或重新打开 Codex CLI 会话。

## Codex 中怎么用

不用输入 Claude Code slash command，直接自然语言描述任务即可：

```text
请审查这份供应商合同，重点看责任限制、解除、赔偿、数据处理和争议解决。
```

```text
我们准备上线一个用户画像推荐功能，请判断是否需要个人信息保护影响评估。
```

```text
请根据这个尽调资料文件夹生成重大问题清单和逐项引用。
```

Codex 会根据任务触发 `chinese-legal-*` adapter，再读取原始法律工作流。

## 可用 Codex skills

16 个领域入口：

- `chinese-legal-commercial`
- `chinese-legal-privacy`
- `chinese-legal-product`
- `chinese-legal-corporate`
- `chinese-legal-employment`
- `chinese-legal-regulatory`
- `chinese-legal-ai-governance`
- `chinese-legal-litigation`
- `chinese-legal-criminal`
- `chinese-legal-ip`
- `chinese-legal-law-student`
- `chinese-legal-clinic`
- `chinese-legal-builder-hub`
- `chinese-legal-research-cn`
- `chinese-legal-law-practice-cn`
- `chinese-legal-procurement`

5 个托管工作流入口：

- `chinese-legal-diligence-grid`
- `chinese-legal-docket-watcher`
- `chinese-legal-launch-radar`
- `chinese-legal-reg-monitor`
- `chinese-legal-renewal-watcher`

## 配置画像

原 Claude Code 插件会把个人实践画像写入：

```text
~/.claude/plugins/config/...
```

Codex adapter 会优先读取已有的 Claude Code 画像。若没有，可在 Codex 中使用：

```text
~/.codex/legal-zh/<domain>/CLAUDE.md
```

保存 Codex 专用画像。不要把这些个人画像提交进仓库。

## 法律检索与连接器

各领域 `.mcp.json` 的法律检索部分默认声明元典统一入口；部分领域还保留协作工具的原有声明。元典地址为 `https://open.chineselaw.com/mcp`；Codex 是否能调用仍取决于当前宿主是否发现该服务、用户是否完成授权以及本次工具调用是否成功。元典[官方接入页](https://open.chineselaw.com/mcp-config/)和北大法宝[官方指南](https://mcp.pkulaw.com/docs)列有当前接入方式；服务端点与证据状态见 [CONNECTORS.md](CONNECTORS.md)。不要把 API Key 或 Access Token 写入仓库或命令日志。

尚未接入商业 MCP 时，仍可用公开官方法源开展研究。法规、案例、期限和监管动态须记录实际来源、版本、检索日期与核验状态；配置声明和数据库命中不自动构成已核验法律依据。

## 是否需要 npx 一键安装

可以做，但本仓库暂不默认发布 npm 包。

`npx` 方案的本质是发布一个 npm CLI 包，例如：

```bash
npx claude-legal-zh install codex
```

该 CLI 会：

1. 下载或更新 GitHub 仓库。
2. 检测用户要安装到 Claude Code、Codex，或其他代理环境。
3. 执行对应安装脚本。
4. 打印重启和初始化提示。

这会引入 npm 包名、版本发布、供应链安全和跨平台测试成本。当前先采用仓库内脚本，便于审计和维护；如维护者希望统一多端安装，可在后续 PR 中加入 npm 包。

## 卸载

删除已安装的 Codex skills：

```bash
rm -rf ~/.codex/skills/chinese-legal-*
```

如使用了 `~/.codex/legal-zh` 保存个人画像，按需自行保留或删除。
