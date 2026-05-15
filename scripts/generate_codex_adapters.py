#!/usr/bin/env python3
"""Generate Codex skill adapters for claude-for-legal-ZH.

The upstream repository is a Claude Code plugin marketplace. Codex consumes
skills through `.agents/skills` or `~/.codex/skills`. This script creates a
small routing layer so Codex can reuse the original domain `CLAUDE.md`,
`skills/*/SKILL.md`, and managed-agent cookbook content without duplicating the
legal workflows.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"

DOMAINS = {
    "commercial-legal": {
        "codex_name": "chinese-legal-commercial",
        "display": "商事合同",
        "triggers": "合同审查、NDA、供应商协议、SaaS/MSA、续约、合同利益方摘要、合同风险上报、商事法务",
    },
    "privacy-legal": {
        "codex_name": "chinese-legal-privacy",
        "display": "数据合规与隐私",
        "triggers": "个人信息保护影响评估、PIPL、数据处理协议、DSAR、隐私政策、数据合规差距、数据出境和隐私合规",
    },
    "product-legal": {
        "codex_name": "chinese-legal-product",
        "display": "产品与营销合规",
        "triggers": "产品上线审查、营销文案审查、广告法、反不正当竞争、功能法律风险、业务法务快速咨询",
    },
    "corporate-legal": {
        "codex_name": "chinese-legal-corporate",
        "display": "公司与并购",
        "triggers": "并购尽调、重大合同披露、董事会/股东会决议、交割清单、公司合规、投后整合、公司法",
    },
    "employment-legal": {
        "codex_name": "chinese-legal-employment",
        "display": "劳动用工",
        "triggers": "劳动合同解除、劳动关系认定、假期管理、员工调查、规章制度、工资工时、跨省用工、劳动法",
    },
    "regulatory-legal": {
        "codex_name": "chinese-legal-regulatory",
        "display": "监管合规",
        "triggers": "法规动态监控、监管简报、政策差异比对、合规差距、征求意见稿、监管政策重写、行政监管",
    },
    "ai-governance-legal": {
        "codex_name": "chinese-legal-ai-governance",
        "display": "AI 治理",
        "triggers": "AI 应用登记、算法安全评估、科技伦理审查、生成式 AI 合规、AI 供应商审查、AI 治理",
    },
    "litigation-legal": {
        "codex_name": "chinese-legal-litigation",
        "display": "诉讼仲裁",
        "triggers": "案件登记、诉讼仲裁、律师函、要件分析、大事记、证据三性、庭前准备、保全、传票、法律文书",
    },
    "ip-legal": {
        "codex_name": "chinese-legal-ip",
        "display": "知识产权",
        "triggers": "商标可注册性、FTO、侵权警告函、通知删除、开源许可证、知识产权条款、专利、著作权、商标",
    },
    "law-student": {
        "codex_name": "chinese-legal-law-student",
        "display": "法学学习与法考",
        "triggers": "法考、案例摘要、IRAC、课堂提问、法学写作、记忆卡片、学习计划、主观题和客观题训练",
    },
    "legal-clinic": {
        "codex_name": "chinese-legal-clinic",
        "display": "法律诊所",
        "triggers": "法律诊所、学生案件接待、诊所备忘录、研究路线、结案移交、指导老师审阅、当事人沟通",
    },
    "legal-builder-hub": {
        "codex_name": "chinese-legal-builder-hub",
        "display": "法律技能运营",
        "triggers": "查找法律技能、评估社区技能、安装法律技能、技能安全审查、法律工作流构建、法律运营",
    },
}

COOKBOOKS = {
    "diligence-grid": {
        "codex_name": "chinese-legal-diligence-grid",
        "display": "尽调问题表格工作流",
        "triggers": "并购尽调材料读取、问题抽取、尽调表格、披露问题清单、法律尽调多文档归一化",
    },
    "docket-watcher": {
        "codex_name": "chinese-legal-docket-watcher",
        "display": "案件期限监控工作流",
        "triggers": "诉讼案件台账、期限监控、案件 docket、开庭和举证期限、诉讼日程提醒",
    },
    "launch-radar": {
        "codex_name": "chinese-legal-launch-radar",
        "display": "产品上线雷达工作流",
        "triggers": "产品上线列表、功能风险分类、上线法律风险雷达、产品发布合规摘要",
    },
    "reg-monitor": {
        "codex_name": "chinese-legal-reg-monitor",
        "display": "监管动态监控工作流",
        "triggers": "监管动态监控、法规 feed、监管摘要、重大性过滤、合规周报",
    },
    "renewal-watcher": {
        "codex_name": "chinese-legal-renewal-watcher",
        "display": "合同续约监控工作流",
        "triggers": "合同续约监控、自动续约、终止通知期限、续约提醒、合同台账读取",
    },
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_names(domain_root: Path) -> list[str]:
    skills_dir = domain_root / "skills"
    if not skills_dir.exists():
        return []
    return sorted(p.parent.name for p in skills_dir.glob("*/SKILL.md"))


def plugin_description(domain_root: Path) -> str:
    manifest = domain_root / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        return ""
    return read_json(manifest).get("description", "").strip()


def adapter_body(domain: str, meta: dict, skills: list[str], description: str) -> str:
    commands = ", ".join(f"`{name}`" for name in skills)
    return f"""---
name: {meta["codex_name"]}
description: Use when the user needs Chinese legal work in the {meta["display"]} domain: {meta["triggers"]}. This is a Codex adapter for claude-for-legal-ZH/{domain}; it routes natural-language requests to the original domain CLAUDE.md and skills/*/SKILL.md workflows.
---

# {meta["display"]} Codex Adapter

This skill lets Codex use the original `claude-for-legal-ZH/{domain}` content without requiring Claude Code slash commands.

## Source Files

- Domain root: `{domain}`
- Domain profile template and shared rules: `{domain}/CLAUDE.md`
- Original skills directory: `{domain}/skills`
- Original plugin description: {description or "See plugin manifest."}

## How To Use

1. Read `{domain}/CLAUDE.md` before substantive work.
2. Select the closest original skill from the list below, then read its `SKILL.md`.
3. Follow that skill's workflow, translating Claude Code slash-command wording into Codex actions and natural conversation.
4. If multiple original skills apply, execute them in the order implied by the workflow and merge the result.
5. Do not run Claude-specific plugin commands. Ignore Claude hooks. Use Codex tools for local files, web verification, document rendering, and user-visible output.

## Configuration Compatibility

The original project stores setup profiles under `~/.claude/plugins/config/...`. For Codex, use this order:

1. If a populated Claude profile exists, read it as the user's existing practice profile.
2. Otherwise use or create `~/.codex/legal-zh/{domain}/CLAUDE.md` for Codex-specific setup.
3. If the selected skill requires setup and the profile still contains `[PLACEHOLDER]`, run the domain's `cold-start-interview` workflow in conversation before producing customized legal work.

When an original instruction says to run `/{domain}:some-command`, interpret that as: load `skills/some-command/SKILL.md` and perform the workflow in Codex.

## Available Original Skills

{commands}

## Legal Output Rules

- Treat all output as lawyer-review draft work, not legal advice replacing professional judgment.
- Mark uncertain legal citations or case references as requiring verification unless verified from a reliable source in this session.
- For current law, regulatory updates, case retrieval, filing requirements, deadlines, or other time-sensitive legal facts, verify with current sources before relying on them.
- Preserve the original workflow's escalation, approval, confidentiality, and source-labeling requirements.
"""


def cookbook_body(cookbook: str, meta: dict) -> str:
    root = f"managed-agent-cookbooks/{cookbook}"
    return f"""---
name: {meta["codex_name"]}
description: Use when the user needs a Chinese legal managed workflow for {meta["display"]}: {meta["triggers"]}. This is a Codex adapter for claude-for-legal-ZH/managed-agent-cookbooks/{cookbook}.
---

# {meta["display"]} Codex Adapter

This skill ports the original managed-agent cookbook into Codex workflow form.

## Source Files

- Cookbook root: `{root}`
- Read first: `{root}/README.md`
- Agent blueprint: `{root}/agent.yaml`
- Steering examples: `{root}/steering-examples.json`
- Subagent blueprints: `{root}/subagents`

## How To Use

1. Read the cookbook `README.md` and `agent.yaml` before running the workflow.
2. Translate Claude managed-agent concepts into Codex execution:
   - Use local file reads/writes for repositories, trackers, tables, and source documents.
   - Use Codex subagents only if the user explicitly asks for parallel agents or the workflow itself is requested as a multi-agent run.
   - Use Codex automations only when the user asks to monitor, remind, watch, or repeat the workflow over time.
3. If the cookbook references subagents, read only the relevant YAML files under `subagents/`.
4. Preserve legal review limits: all outputs are lawyer-review drafts; verify current legal facts and deadlines before reliance.
5. Produce the cookbook's intended artifact, such as a grid, tracker update, alert, digest, or memo, in the user's requested location or inline if no location is specified.
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


if __name__ == "__main__":
    main()
