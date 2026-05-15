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

12 个领域入口：

- `chinese-legal-commercial`
- `chinese-legal-privacy`
- `chinese-legal-product`
- `chinese-legal-corporate`
- `chinese-legal-employment`
- `chinese-legal-regulatory`
- `chinese-legal-ai-governance`
- `chinese-legal-litigation`
- `chinese-legal-ip`
- `chinese-legal-law-student`
- `chinese-legal-clinic`
- `chinese-legal-builder-hub`

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

上游 `.mcp.json` 预置了元典、飞书、Google Drive、e 签宝、法大大等连接器说明。Codex 是否能直接调用，取决于你本机 Codex 是否已安装对应连接器或 MCP 服务。

没有连接器时，Codex 仍可执行流程，但法规、案例、监管动态、期限等时效性内容应标注为“需验证”，并在依赖前用可靠来源核验。

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
