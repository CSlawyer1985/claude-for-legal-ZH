#!/usr/bin/env python3
"""Generate WorkBuddy skill adapters for claude-for-legal-ZH.

The upstream repository is a Claude Code plugin marketplace. WorkBuddy (Tencent)
discovers skills from `<project>/.workbuddy/skills` and `~/.workbuddy/skills`,
using the same SKILL.md convention (YAML frontmatter + Markdown body). This
script creates a WorkBuddy-native routing layer so WorkBuddy can reuse the
original domain `CLAUDE.md`, `skills/*/SKILL.md`, and managed-agent cookbook
content without duplicating the legal workflows.

Descriptions are written in Chinese with explicit trigger words, matching
WorkBuddy's description-driven auto-invocation design. Domain and cookbook
metadata are imported from generate_codex_adapters.py so all harness adapters
share one source of truth.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_codex_adapters import (  # noqa: E402
    COOKBOOKS,
    DOMAINS,
    ROOT,
    plugin_description,
    skill_names,
)

SKILLS_ROOT = ROOT / ".workbuddy" / "skills"

PATH_RESOLUTION = """## 路径解析

上述仓库相对路径以 `claude-for-legal-ZH` 仓库根目录为基准：

- 当前工作区包含本仓库时，直接按仓库根目录解析。
- 用户级安装后，先运行 `cat ~/.workbuddy/legal-zh/repo` 取得安装脚本登记的仓库绝对路径，再拼接相对路径。
"""


def yaml_string(text: str) -> str:
    """Quote a scalar for YAML frontmatter (JSON string = valid YAML flow scalar)."""
    return json.dumps(text, ensure_ascii=False)


def adapter_body(domain: str, meta: dict, skills: list[str], description: str) -> str:
    commands = "、".join(f"`{name}`" for name in skills)
    desc = f'{meta["display"]}领域法律工作：{meta["triggers"]}。claude-for-legal-ZH/{domain} 的 WorkBuddy 路由技能，把自然语言请求路由到原领域 CLAUDE.md 与 skills/*/SKILL.md 工作流。'
    return f"""---
name: {meta["codex_name"]}
description: {yaml_string(desc)}
---

# {meta["display"]} — claude-for-legal-ZH（WorkBuddy 适配）

本技能让 WorkBuddy 复用 `claude-for-legal-ZH/{domain}` 的原始内容，无需 Claude Code slash command。

## 源文件

- 领域根目录：`{domain}`
- 领域画像与共享规则：`{domain}/CLAUDE.md`
- 原始技能目录：`{domain}/skills`
- 原插件说明：{description or "见插件清单。"}

{PATH_RESOLUTION}
## 使用方式

1. 处理实质法律工作前，先读取 `{domain}/CLAUDE.md`。
2. 从下方技能清单选择最接近的原始技能，读取其 `SKILL.md`。
3. 按该技能的工作流执行，把 Claude Code slash command 表述转写为 WorkBuddy 的文件、Shell、文档与自动化动作。
4. 多个原始技能同时适用时，按工作流隐含顺序依次执行并合并结果。
5. 不执行 Claude 专属插件命令，忽略 Claude hooks。本地文件、检索核验、文档渲染与用户可见输出均使用 WorkBuddy 工具完成。

## 配置兼容

原项目把实践画像存放在 `~/.claude/plugins/config/...`。WorkBuddy 中按以下顺序：

1. 已存在 Claude 画像时，直接读取作为现有执业画像。
2. 否则使用或创建 `~/.workbuddy/legal-zh/{domain}/CLAUDE.md` 保存 WorkBuddy 专用画像。
3. 所选技能要求初始化且画像仍含 `[PLACEHOLDER]` 时，先以对话方式完成该领域的 `cold-start-interview` 冷启动面试，再产出定制化法律工作。

原指令中的 `/{domain}:some-command` 应解释为：读取 `{domain}/skills/some-command/SKILL.md` 并在 WorkBuddy 中执行该工作流。

## 法律检索连接器

WorkBuddy 的 MCP 配置位于 `~/.workbuddy/mcp.json`（标准 `mcpServers` 格式）。已配置 `chineselaw` 或 `yuandian`（元典）等法律检索服务时（见 `INSTALL_WORKBUDDY.md`），优先用其核验法条、案例与监管动态；未配置时，时效性法律事实一律标注"需验证"。

## 可用原始技能

{commands}

## 法律输出规则

- 所有输出均为律师审查草稿，不替代律师专业判断。
- 不确定的法条引用或案例参考须标注"需验证"，除非本次会话已从可靠来源核验。
- 法条、案例、监管动态、期限等时效性内容，依赖前必须用可靠来源核验。
- 保留原工作流的升级、审批、保密与来源标注要求。
"""


def cookbook_body(cookbook: str, meta: dict) -> str:
    root = f"managed-agent-cookbooks/{cookbook}"
    desc = f'{meta["display"]}：{meta["triggers"]}。claude-for-legal-ZH/managed-agent-cookbooks/{cookbook} 的 WorkBuddy 路由技能。'
    return f"""---
name: {meta["codex_name"]}
description: {yaml_string(desc)}
---

# {meta["display"]} — claude-for-legal-ZH（WorkBuddy 适配）

本技能把原托管 Agent cookbook 转写为 WorkBuddy 工作流。

## 源文件

- Cookbook 根目录：`{root}`
- 先读：`{root}/README.md`
- Agent 蓝图：`{root}/agent.yaml`
- 引导示例：`{root}/steering-examples.json`
- 子 Agent 蓝图：`{root}/subagents`

{PATH_RESOLUTION}
## 使用方式

1. 运行工作流前，先读 cookbook 的 `README.md` 与 `agent.yaml`。
2. 把 Claude 托管 Agent 概念转写为 WorkBuddy 执行：
   - 台账、表格、源文档读写使用 WorkBuddy 本地文件工具。
   - 仅在用户明确要求并行 agent 或多 agent 运行时，才使用 WorkBuddy 的多任务并行。
   - 仅在用户要求监控、提醒、看守或周期重复时，才使用 WorkBuddy 的定时自动化。
3. cookbook 引用子 agent 时，只读取 `subagents/` 下相关的 YAML 文件。
4. 保留法律审查边界：所有产出均为律师审查草稿，时效性法律事实与期限依赖前必须核验。
5. 产出 cookbook 预期的交付物（表格、台账更新、预警、摘要或备忘录），位置按用户指定；未指定时对话内输出。
"""


def main() -> None:
    SKILLS_ROOT.mkdir(parents=True, exist_ok=True)
    for domain, meta in DOMAINS.items():
        domain_root = ROOT / domain
        if not domain_root.exists():
            raise SystemExit(f"Missing domain root: {domain_root}")
        out_dir = SKILLS_ROOT / meta["codex_name"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "SKILL.md").write_text(
            adapter_body(domain, meta, skill_names(domain_root), plugin_description(domain_root)),
            encoding="utf-8",
        )
    for cookbook, meta in COOKBOOKS.items():
        root = ROOT / "managed-agent-cookbooks" / cookbook
        if not root.exists():
            raise SystemExit(f"Missing cookbook root: {root}")
        out_dir = SKILLS_ROOT / meta["codex_name"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "SKILL.md").write_text(cookbook_body(cookbook, meta), encoding="utf-8")
    print(f"Generated {len(DOMAINS) + len(COOKBOOKS)} WorkBuddy adapters under {SKILLS_ROOT}")


if __name__ == "__main__":
    main()
