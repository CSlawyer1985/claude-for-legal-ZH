#!/usr/bin/env python3
"""Check new domain registration and generated cross-host routing consistency."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW_DOMAINS = {"legal-research-cn", "law-practice-cn", "procurement-legal"}
NEW_SKILLS = {
    "legal-research-cn": {"cold-start-interview", "authority-check", "case-comparison", "issue-memo", "lecture-source-pack"},
    "procurement-legal": {"cold-start-interview", "regime-triage", "bid-review", "challenge-complaint", "contract-performance"},
    "law-practice-cn": {"cold-start-interview", "consultation-analysis", "legal-service-proposal", "complaint-triage"},
    "commercial-legal": {"construction-contract-review"},
    "corporate-legal": {"diligence-evidence-matrix"},
    "litigation-legal": {"neutral-hearing-outline"},
}
MODULES = {
    "task_context", "jurisdiction", "temporal", "actors", "matter",
    "claims_and_elements", "authority_and_interpretation", "proof", "procedure",
    "outcomes_and_enforcement", "strategy_and_uncertainty", "governance",
}


def main() -> int:
    errors: list[str] = []
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    registered = {plugin["name"] for plugin in marketplace["plugins"]}
    if not NEW_DOMAINS <= registered:
        errors.append(f"marketplace missing {sorted(NEW_DOMAINS - registered)}")

    spec = importlib.util.spec_from_file_location("adapters", ROOT / "scripts/generate_codex_adapters.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for domain, skills in NEW_SKILLS.items():
        for skill in skills:
            source = ROOT / domain / "skills" / skill / "SKILL.md"
            if not source.is_file():
                errors.append(f"missing source {domain}/{skill}")
                continue
            content = source.read_text(encoding="utf-8")
            if skill != "cold-start-interview" and any(f"`{module}`" not in content for module in MODULES):
                errors.append(f"{domain}/{skill}: incomplete legal capability review")
        meta = module.DOMAINS.get(domain)
        if not meta:
            errors.append(f"{domain}: missing adapter generator entry")
            continue
        adapter = meta["codex_name"]
        for host in (".agents", ".dsh", ".workbuddy"):
            path = ROOT / host / "skills" / adapter / "SKILL.md"
            if not path.is_file():
                errors.append(f"missing {host}/{adapter}")
                continue
            content = path.read_text(encoding="utf-8")
            for skill in skills:
                if f"`{skill}`" not in content:
                    errors.append(f"{host}/{adapter}: missing route {skill}")

    for domain, agent in (("legal-research-cn", "law-change-watch"), ("procurement-legal", "notice-watch")):
        path = ROOT / domain / "agents" / f"{agent}.md"
        if not path.is_file():
            errors.append(f"{domain}/{agent}: missing agent")
            continue
        content = path.read_text(encoding="utf-8")
        if "不自动" not in content or 'tools: ["Read", "WebSearch", "WebFetch"]' not in content:
            errors.append(f"{domain}/{agent}: missing read-only guard")
    takedown = (ROOT / "ip-legal/skills/takedown/SKILL.md").read_text(encoding="utf-8")
    if any(phrase in takedown for phrase in ("第24条四因素", "联邦管辖", "伪证双重关口")):
        errors.append("ip-legal/takedown: inherited US-law test remains in China route")
    if any(phrase in takedown for phrase in ("15个工作日", "15 个工作日", "十五个工作日")):
        errors.append("ip-legal/takedown: e-commerce counter-notice period is calendar days, not working days")
    if "平台转送声明到达权利人后十五日内" not in takedown:
        errors.append("ip-legal/takedown: e-commerce counter-notice trigger is missing")
    investigation = (ROOT / "employment-legal/skills/internal-investigation/SKILL.md").read_text(encoding="utf-8")
    if "法域门禁：" not in investigation or "work product protection applies" in investigation:
        errors.append("employment-legal/internal-investigation: missing China-law gate")
    cases = json.loads((ROOT / "evals/upgrade-cases.json").read_text(encoding="utf-8"))
    if cases.get("provider_backed") is not False:
        errors.append("static cases must not claim provider-backed evidence")
    for case in cases["cases"]:
        path = ROOT / case["expected_skill"]
        if not path.is_file() or case["boundary"] not in path.read_text(encoding="utf-8"):
            errors.append(f"missing route or boundary: {case['expected_skill']}")
    print(f"checked {len(NEW_SKILLS)} affected domains, {sum(map(len, NEW_SKILLS.values()))} new skills, 3 adapter hosts, {len(cases['cases'])} static cases")
    for error in errors:
        print(f"ERROR {error}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
