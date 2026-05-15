# 快速入门

**60 秒**即可开始使用插件。

本仓库原生支持 **Claude Code 插件 marketplace**，并提供 **Codex Desktop / Codex CLI** 适配层。Claude Code 用户按下方 Claude Code 流程安装；Codex 用户可直接跳到「在 Codex 中安装」。

## 在 Codex 中安装

在仓库根目录运行：

```bash
scripts/install-codex.sh
```

默认会把 `.agents/skills/chinese-legal-*` 链接到：

```text
~/.codex/skills
```

安装后请重启 Codex Desktop 或重新打开 Codex CLI 会话。

Codex 中不需要输入 Claude Code slash command，直接用自然语言提出任务即可，例如：

```text
请审查这份供应商合同，重点看责任限制、解除、赔偿、数据处理和争议解决。
```

```text
我们准备上线用户画像推荐功能，请判断是否需要个人信息保护影响评估。
```

更多说明见 [INSTALL_CODEX.md](INSTALL_CODEX.md)。

## Claude Code 一键添加 marketplace

Claude Code 用户也可以先运行：

```bash
scripts/install-claude-code.sh
```

脚本会添加本地 marketplace，并打印可安装插件列表。安装具体插件时仍建议选择用户级（user scope）。

## 在 Claude Code 中安装

1. **打开 Claude Code**（在终端中）。

2. **添加市场源。** 在 Claude Code 中输入 `/plugin marketplace add `（末尾带空格），然后**将 `claude-for-legal-zh` 文件夹拖到终端窗口**——路径会自动填入。按回车。

   （或者输入完整路径：`/plugin marketplace add /Users/你/Desktop/claude-for-legal-zh`）

3. **安装你需要的插件。** 从下表中选择匹配你工作领域的插件，然后：
   ```
   /plugin install commercial-legal@claude-for-legal-zh
   ```

4. **⚠️ 重启 Claude Code。** 关闭并重新打开。此步骤不可跳过——重启后插件才会生效。

5. **运行初始化设置。** 快速入门 2 分钟，完整设置 10-15 分钟。
   ```
   /commercial-legal:cold-start-interview
   ```

6. **连接法律检索工具。** 没有连接检索工具时，引用的法规和案例将被标注为"未验证"。
   本插件已预配置 yuandian（元典）MCP 连接器用于案例检索和法规检索。首次需要时系统会提示授权。
   也可以手动配置其他中国法律检索工具（北大法宝、威科先行等）。

## 安装范围：选择用户级（user scope），而非项目级（project scope）

运行 `/plugin install` 时，系统可能询问是安装到当前项目还是所有项目。

**选择用户级（user scope）。**

项目级看似更安全，但会阻止插件读取项目文件夹之外的文件——你放在下载目录的合同、文档里的协议、桌面上的客户材料都无法访问。大多数技能需要读取你的文件。用户级不会给插件额外的文件访问权限——插件仍只能读取你明确指定或当前目录中的文件，只是让你在任何文件夹都能使用插件。

如果已安装为项目级想切换：`/plugin uninstall <插件名>`，然后从用户主目录执行 `/plugin install <插件名>@claude-for-legal-zh`。

## 我应该安装哪个插件？

| 你的角色 | 安装 | 首次命令 |
|---|---|---|
| 数据合规/隐私律师/DPO | `privacy-legal` | `/privacy-legal:use-case-triage` |
| 商事/合同律师/法务 | `commercial-legal` | `/commercial-legal:review` |
| 公司/并购律师 | `corporate-legal` | `/corporate-legal:diligence-issue-extraction` |
| 劳动法律师/HR 法务 | `employment-legal` | `/employment-legal:wage-hour-qa` |
| 产品/业务法务 | `product-legal` | `/product-legal:is-this-a-problem` |
| 知识产权律师/专利代理师 | `ip-legal` | `/ip-legal:clearance` |
| 诉讼/仲裁律师（法务或律所） | `litigation-legal` | `/litigation-legal:matter-intake` |
| 合规/监管法务 | `regulatory-legal` | `/regulatory-legal:reg-feed-watcher` |
| AI 治理负责人 | `ai-governance-legal` | `/ai-governance-legal:use-case-triage` |
| 法学院法律诊所指导老师 | `legal-clinic` | `/legal-clinic:cold-start-interview` |
| 法学院学生/法考生 | `law-student` | `/law-student:cold-start-interview` |
| 法律运营/寻找新技能 | `legal-builder-hub` | `/legal-builder-hub:registry-browser` |

## 你安装的是什么

每个插件通过初始化面试了解你的实务方式，写入实践画像文件（`~/.claude/plugins/config/claude-for-legal-zh/<插件名>/CLAUDE.md`），每个技能都从中读取。画像属于你——直接编辑、重新运行设置、或让技能更新它。

**所有输出均为律师审查草稿。** 插件会标记其不确定的内容，按来源标注引用，并对不可逆操作设置门槛。律师审查、核实并承担责任。插件让审查更快，但不能替代审查。

## 盒子里有什么

12 个业务领域插件，5 个托管 Agent 蓝图，yuandian MCP 连接器。完整参考见 [README.md](README.md)。

## 遇到问题？

- **安装后"Command not found"** → 你忘了第 4 步。重启 Claude Code。
- **提示"请先运行设置"** → 在任何其他命令之前先运行 `/<插件名>:cold-start-interview`。
- **引用标注为 `[需验证]`** → 连接检索工具（第 6 步）。没有连接时，每条引用都来自模型训练数据而非最新数据库。
- **"无法读取文件"** → 通常是插件安装为项目级而文件在项目文件夹之外。见上"安装范围"——重装为用户级或将文件移到项目文件夹。
- **插件不做某件事** → 运行 `/legal-builder-hub:related-skills-surfacer` 找更匹配的技能，或查看插件 README 中的"本插件不做什么"。
