#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARKETPLACE_NAME="claude-for-legal-zh"

if ! command -v claude >/dev/null 2>&1; then
  echo "未找到 Claude Code CLI：claude" >&2
  echo "请先安装 Claude Code，然后重新运行本脚本。" >&2
  exit 1
fi

echo "添加 Claude Code marketplace：$ROOT_DIR"
claude plugin marketplace add "$ROOT_DIR"

cat <<EOF

marketplace 已添加。请选择需要的插件安装，例如：

  claude plugin install --scope user commercial-legal@$MARKETPLACE_NAME
  claude plugin install --scope user privacy-legal@$MARKETPLACE_NAME
  claude plugin install --scope user corporate-legal@$MARKETPLACE_NAME
  claude plugin install --scope user employment-legal@$MARKETPLACE_NAME
  claude plugin install --scope user regulatory-legal@$MARKETPLACE_NAME

可选插件名称：
  commercial-legal, privacy-legal, product-legal, corporate-legal,
  employment-legal, regulatory-legal, ai-governance-legal, litigation-legal,
  law-student, legal-clinic, legal-builder-hub, ip-legal

安装后请重启 Claude Code。插件生效后先运行对应领域的 cold-start-interview
或 README/QUICKSTART 中列出的首次命令。
EOF
