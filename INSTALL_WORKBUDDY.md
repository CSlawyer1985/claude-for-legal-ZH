# WorkBuddy 安装指南

本仓库原生支持 Claude Code 插件，同时提供 Codex、DeepSeek Harness（dsh）与 [WorkBuddy](https://cloud.tencent.com/document/product/1831/134432)（腾讯出品的工作智能体）适配层。本文档覆盖 WorkBuddy 侧的安装、使用、MCP 配置与卸载。

## 这是什么

WorkBuddy 适配层不会重写法律工作流，而是复用原仓库中的：

- 各领域 `CLAUDE.md`
- 各领域 `skills/*/SKILL.md`
- `managed-agent-cookbooks/*`

WorkBuddy 的技能体系与 Claude Code 同属 SKILL.md 生态（YAML frontmatter + Markdown 正文，支持 `scripts/`、`references/`、`assets/` 资源），adapter 只负责把自然语言请求路由到对应工作流。WorkBuddy 扫描用户级 `~/.workbuddy/skills/` 与项目级 `.workbuddy/skills/`，adapter 即存放于这两处。

## 两种使用模式

### 模式 A：仓库即工作区（零安装，适合体验与开发）

在 WorkBuddy 中把本仓库目录作为项目目录打开：`.workbuddy/skills/chinese-legal-*` 会被自动发现，无需任何安装。

### 模式 B：用户级安装（适合在任意案件目录工作）

在仓库根目录运行：

```bash
scripts/install-workbuddy.sh
```

默认使用符号链接安装到 `~/.workbuddy/skills`（`git pull` 后无需重装）。如希望复制一份独立快照：

```bash
scripts/install-workbuddy.sh copy
```

安装脚本做两件事：

1. 将 `.workbuddy/skills/chinese-legal-*` 链接/复制到 `~/.workbuddy/skills/`；
2. 把仓库绝对路径登记到 `~/.workbuddy/legal-zh/repo`（纯文本，无密钥）——adapter 通过 `cat ~/.workbuddy/legal-zh/repo` 取得仓库根目录后拼接领域文件路径，因此在任何工作区都能定位法律工作流。

安装后在 WorkBuddy 的「专家·技能·连接器」面板确认新技能已启用。

## WorkBuddy 中怎么用

不用输入 Claude Code slash command，直接自然语言描述任务即可。adapter 的 description 为中文并含触发词，WorkBuddy 会自动匹配调用：

```text
请审查这份供应商合同，重点看责任限制、解除、赔偿、数据处理和争议解决。
```

```text
我们准备上线一个用户画像推荐功能，请判断是否需要个人信息保护影响评估。
```

```text
请根据这个尽调资料文件夹生成重大问题清单和逐项引用。
```

## 可用 WorkBuddy skills

13 个领域入口（`chinese-legal-commercial`、`chinese-legal-privacy`、`chinese-legal-product`、`chinese-legal-corporate`、`chinese-legal-employment`、`chinese-legal-regulatory`、`chinese-legal-ai-governance`、`chinese-legal-litigation`、`chinese-legal-criminal`、`chinese-legal-ip`、`chinese-legal-law-student`、`chinese-legal-clinic`、`chinese-legal-builder-hub`）+ 5 个托管工作流入口（`chinese-legal-diligence-grid`、`chinese-legal-docket-watcher`、`chinese-legal-launch-radar`、`chinese-legal-reg-monitor`、`chinese-legal-renewal-watcher`），与 Codex、dsh 适配层同名同构。

## 配置画像

原 Claude Code 插件会把个人实践画像写入 `~/.claude/plugins/config/...`。WorkBuddy adapter 的读取顺序：

1. 已存在 Claude Code 画像 → 直接复用；
2. 否则使用或创建 `~/.workbuddy/legal-zh/<domain>/CLAUDE.md` 保存 WorkBuddy 专用画像。

不要把个人画像、客户材料、API key 提交进仓库。

## MCP 法律检索配置

WorkBuddy 的 MCP 配置文件为 `~/.workbuddy/mcp.json`，采用标准 `mcpServers` 格式。接入法条与案例检索服务的最小示例：

```json
{
  "mcpServers": {
    "chineselaw": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "chineselaw-mcp"],
      "env": { "CHINESELAW_API_KEY": "你的-api-key" }
    },
    "yuandian": {
      "type": "http",
      "url": "https://mcp.yuandian.com/mcp"
    }
  }
}
```

未配置任何法律检索服务时，adapter 会把法规、案例、期限等时效性内容标注为“需验证”，依赖前请用可靠来源核验。

## 已知边界

- **hooks 不迁移**：Claude Code 的 hooks.json 在 WorkBuddy 中没有等价物；本仓库各领域的 hooks 当前均为空，无实际损失。
- **slash command 命名空间**：`/<domain>:<command>` 是 Claude Code 概念；WorkBuddy 中由 adapter 依据 description 自动触发替代。
- **与既有 `cflz-*` 技能的关系**：本仓库的 WorkBuddy 适配层使用与各端统一的 `chinese-legal-*` 命名，路径通过 `~/.workbuddy/legal-zh/repo` 动态解析（不内置仓库拷贝，不会随时间过期）。如果你此前手工安装过带 `_cflz` 数据目录的 `cflz-*` 技能，二者功能重叠，建议保留其一——保留本适配层可获得与仓库同步更新。
- **企业版技能市场**：WorkBuddy Enterprise 支持上传本地技能包。也可以把 `.workbuddy/skills/chinese-legal-*` 打包后通过「添加技能 → 上传本地技能包」分发，但符号链接安装仍是更新最方便的方式。

## 更新与卸载

仓库更新后：

```bash
git pull
python3 scripts/generate_workbuddy_adapters.py   # 重新生成（如 adapter 模板有变化）
scripts/install-workbuddy.sh                     # copy 模式需要重装；link 模式只需重跑生成器
```

卸载：

```bash
rm -rf ~/.workbuddy/skills/chinese-legal-*
```

`~/.workbuddy/legal-zh/` 如保存了个人画像，按需自行保留或删除。

## 安全提醒

- 所有法律输出均为律师审查草稿；法规、案例、期限和监管动态等时效性内容必须用可靠来源核验后再依赖。
- 不要把个人画像、客户材料、API key、MCP 授权状态提交进仓库。
