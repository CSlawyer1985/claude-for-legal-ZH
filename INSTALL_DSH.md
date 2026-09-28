# DeepSeek Harness（dsh）安装指南

本仓库原生支持 Claude Code 插件，同时提供 Codex 与 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（`dsh`）两套适配层。本文档覆盖 dsh 侧的安装、使用、MCP 配置与卸载。

> 适配基于 `@deepseek-ai/dsh@0.1.0-rc.6`（developer preview）验证。dsh 处于预览期，官方声明会有兼容性破坏变更；本适配层只使用其公开的 skills / instructions / MCP 配置机制，不耦合内部 API，升级 dsh 后重新运行生成器与安装脚本即可。

## 这是什么

dsh 适配层不会重写法律工作流，而是复用原仓库中的：

- 各领域 `CLAUDE.md`
- 各领域 `skills/*/SKILL.md`
- `managed-agent-cookbooks/*`

dsh adapter 只负责把自然语言请求路由到对应工作流。dsh 官方技能发现机制原生扫描 `.dsh/skills`（项目级，rank 100）与 `~/.dsh/skills`（用户级，rank 400），adapter 即存放于这两处。

## 两种使用模式

### 模式 A：仓库即工作区（零安装，适合体验与开发）

直接在 dsh web 中把本仓库目录添加为工作区并选中：

1. `.dsh/skills/chinese-legal-*` 被自动扫描进入技能目录（同名时优先于 `.agents/skills` 中的 Codex 版本，措辞自动切换为 dsh 版）；
2. 仓库根 `AGENTS.md` 与各目录 `CLAUDE.md` 作为工作区指令自动注入；
3. 领域文件直接使用仓库相对路径，无需任何安装。

### 模式 B：用户级安装（适合在任意案件目录工作）

在仓库根目录运行：

```bash
scripts/install-dsh.sh
```

默认使用符号链接安装到 `~/.dsh/skills`（`git pull` 后无需重装）。如希望复制一份独立快照：

```bash
scripts/install-dsh.sh copy
```

安装脚本做三件事：

1. 将 `.dsh/skills/chinese-legal-*` 链接/复制到 `~/.dsh/skills/`；
2. 把仓库绝对路径登记到 `~/.dsh/legal-zh/repo`（纯文本，无密钥）——adapter 通过 `cat ~/.dsh/legal-zh/repo` 取得仓库根目录后拼接领域文件路径，因此在任何工作区都能定位法律工作流；
3. 向 `~/.dsh/AGENTS.md` 幂等写入一段 `legal-zh` 受管块（中国法律工作守则），dsh 会把它作为用户全局指令注入每个会话；重复安装只替换该块，不影响文件中其他内容。

安装后新开会话立即可见；进行中的会话会在下一步自动刷新技能目录。

## dsh 中怎么用

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

dsh 会根据任务匹配 `chinese-legal-*` adapter，再由 adapter 引导读取原始领域工作流。也可以在输入中直接点名技能（如“用 chinese-legal-litigation 帮我整理这个案子的大事记”），dsh 会把技能内容直接注入会话。

## 可用 dsh skills

16 个领域入口：

- `chinese-legal-commercial`（商事合同）
- `chinese-legal-privacy`（数据合规与隐私）
- `chinese-legal-product`（产品与营销合规）
- `chinese-legal-corporate`（公司与并购）
- `chinese-legal-employment`（劳动用工）
- `chinese-legal-regulatory`（监管合规）
- `chinese-legal-ai-governance`（AI 治理）
- `chinese-legal-litigation`（诉讼仲裁）
- `chinese-legal-criminal`（刑事辩护与合规）
- `chinese-legal-ip`（知识产权）
- `chinese-legal-law-student`（法学学习与法考）
- `chinese-legal-clinic`（法律诊所）
- `chinese-legal-builder-hub`（法律技能运营）
- `chinese-legal-research-cn`（中国法研究）
- `chinese-legal-law-practice-cn`（中国律师业务）
- `chinese-legal-procurement`（政府采购与招标投标）

5 个托管工作流入口：

- `chinese-legal-diligence-grid`（尽调问题表格）
- `chinese-legal-docket-watcher`（案件期限监控）
- `chinese-legal-launch-radar`（产品上线雷达）
- `chinese-legal-reg-monitor`（监管动态监控）
- `chinese-legal-renewal-watcher`（合同续约监控）

## 配置画像

原 Claude Code 插件会把个人实践画像写入 `~/.claude/plugins/config/...`。dsh adapter 的读取顺序：

1. 已存在 Claude Code 画像 → 直接复用；
2. 否则使用或创建 `~/.dsh/legal-zh/<domain>/CLAUDE.md` 保存 dsh 专用画像。

不要把个人画像、客户材料、API key 提交进仓库。

## MCP 连接器配置（法条与案例检索）

元典现行官方入口为 `https://open.chineselaw.com/mcp`。DSH 可按[元典官方接入页](https://open.chineselaw.com/mcp-config/)与[官方 dsh 插件项目](https://github.com/yuandian-ailaw/yuandian_dsh_plugin)接入：先检查官方发布版本、兼容范围和包摘要，再由用户在宿主设置页选择 OAuth 或 API Key，最后以公开法条做一次真实调用。旧版 `https://mcp.yuandian.com/mcp` 配置片段不再推荐；不要在仓库或 patch 文件中保存凭据。

北大法宝的 [MCP 接入指南](https://mcp.pkulaw.com/docs) 提供法规、案例、引用校验等独立端点，须用用户自己的 Access Token 在宿主配置。其公开地址登记于 `connectors/catalog.json`，本仓库没有替用户启用。

DSH adapter 的工具名以当前实际加载清单为准。未授权、无权限、额度不足或服务未挂载时，记录失败状态并改走官方网页核验，不将检索失败解释为法律不存在，也不以模型知识补足关键法条或期限。

## 权限预设建议（可选）

dsh 的 permission presets 可与法律项目的 `input/`（只读原始材料）、`scratch/`（工作区）、`output/`（交付区）三层目录对齐。在同一 patch 文件中追加：

```yaml
- id: permission
  config:
    presets:
      legal-readonly:
        sandbox: read-only
        approval: ask
        name: legal-readonly
        description: "只读 input 和已登记知识库；禁止联网。"
      matter-write:
        sandbox: workspace-write
        approval: ask
        name: matter-write
        description: "读 input；写当前案件的 scratch；默认禁止联网。"
      export-only:
        sandbox: workspace-write
        approval: ask
        name: export-only
        description: "读 scratch；只写待确认导出区；禁止联网。"
```

在 dsh web 的会话工具栏可按案件阶段切换预设——阅卷用 `legal-readonly`，分析写作用 `matter-write`，导出交付用 `export-only`。

## 已知边界

- **hooks 不迁移**：Claude Code 的 hooks.json 在 dsh 中没有声明式等价物；本仓库各领域的 hooks 当前均为空，无实际损失。
- **slash command 命名空间**：`/<domain>:<command>` 是 Claude Code 概念；dsh 中由 adapter 路由 + 技能直接调用替代。
- **agent presets**：dsh 的 preset（`agent.cordis.yml` 组合）可进一步封装“法律人格 + 技能 + MCP”，本适配层暂未使用，待 dsh 组合格式稳定后再提供。
- **同名优先级**：`.dsh/skills`（rank 100）高于 `.agents/skills`（rank 200），`~/.dsh/skills`（rank 400）高于 `~/.agents/skills`（rank 500）——dsh 版 adapter 永远覆盖同名 Codex 版，两套并存互不干扰。

## 更新与卸载

仓库更新后：

```bash
git pull
python3 scripts/generate_dsh_adapters.py   # 重新生成 .dsh/skills（如 adapter 模板有变化）
scripts/install-dsh.sh                     # copy 模式需要重装；link 模式只需重跑生成器
```

卸载：

```bash
rm -rf ~/.dsh/skills/chinese-legal-*
```

然后删除 `~/.dsh/AGENTS.md` 中 `<!-- legal-zh:start -->` 到 `<!-- legal-zh:end -->` 之间的受管块；`~/.dsh/legal-zh/` 如保存了个人画像，按需自行保留或删除。

## 安全提醒

- 所有法律输出均为律师审查草稿；法规、案例、期限和监管动态等时效性内容必须用可靠来源核验后再依赖。
- 不要把个人画像、客户材料、API key、MCP 授权状态提交进仓库。
