#!/usr/bin/env python3
"""Check public legal MCP declarations without contacting authenticated services."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "connectors/catalog.json").read_text(encoding="utf-8"))
YUANDIAN = next(p for p in CATALOG["providers"] if p["id"] == "yuandian")
PKULAW = next(p for p in CATALOG["providers"] if p["id"] == "pkulaw")
UNVERIFIED_LEGACY_DEFAULTS = {"飞书", "e签宝", "法大大"}


def main() -> int:
    errors: list[str] = []
    providers = {provider["id"]: provider for provider in CATALOG["providers"]}
    if set(providers) != {"yuandian", "pkulaw", "wkinfo", "jufa"}:
        errors.append("official provider catalog must cover four researched services")
    for provider in CATALOG["providers"]:
        if not provider["source"].startswith("https://") or provider["verified_live_call"] is not False:
            errors.append(f"{provider['id']}: source or live-call evidence status invalid")
        for url in provider.get("endpoints", {}).values():
            if not url.startswith("https://"):
                errors.append(f"{provider['id']}: non-HTTPS endpoint")
    domains = sorted(p.parent.parent for p in ROOT.glob("*/.claude-plugin/plugin.json"))
    for domain in domains:
        path = domain / ".mcp.json"
        if not path.is_file():
            errors.append(f"{domain.name}: missing .mcp.json")
            continue
        servers = json.loads(path.read_text(encoding="utf-8")).get("mcpServers", {})
        for name in sorted(UNVERIFIED_LEGACY_DEFAULTS.intersection(servers)):
            errors.append(f"{domain.name}: unverified legacy default {name}")
        yd = servers.get("yuandian", {})
        if yd.get("url") != YUANDIAN["url"] or yd.get("type") != "http":
            errors.append(f"{domain.name}: yuandian endpoint mismatch")
        for name, definition in servers.items():
            raw = json.dumps(definition, ensure_ascii=False)
            if any(stale in raw for stale in ("mcp.yuandian.com", "mcp.pkulaw.com/mcp")):
                errors.append(f"{domain.name}: stale endpoint in {name}")
            if any(key in definition for key in ("headers", "env")):
                errors.append(f"{domain.name}: credentials must be configured in host, not repo")
    if len(PKULAW["endpoints"]) < 5:
        errors.append("pkulaw documented endpoints incomplete")
    print(f"checked {len(domains)} domain declarations; {len(providers)} documented providers; {len(PKULAW['endpoints'])} opt-in pkulaw endpoints")
    for error in errors:
        print(f"ERROR {error}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
