#!/usr/bin/env bash
# Install claude-for-legal-ZH DeepSeek Harness (dsh) adapters.
#
#   scripts/install-dsh.sh          # symlink mode (default, auto-updates on git pull)
#   scripts/install-dsh.sh copy     # copy mode (standalone snapshot)
#
# What it does:
#   1. Links/copies .dsh/skills/chinese-legal-* into ~/.dsh/skills/
#   2. Records the absolute repository path in ~/.dsh/legal-zh/repo
#      (adapters read it to resolve repository-relative paths from any cwd)
#   3. Merges an idempotent managed block into ~/.dsh/AGENTS.md
#      (dsh auto-loads it as the user-global instruction file)
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/.dsh/skills"
DSH_HOME_DIR="${DSH_HOME:-$HOME/.dsh}"
TARGET_DIR="$DSH_HOME_DIR/skills"
STATE_DIR="$DSH_HOME_DIR/legal-zh"
AGENTS_FILE="$DSH_HOME_DIR/AGENTS.md"
MODE="${1:-link}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "未找到 DSH skills 目录：$SOURCE_DIR" >&2
  echo "请先运行：python3 scripts/generate_dsh_adapters.py" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR" "$STATE_DIR"

case "$MODE" in
  link|--link)
    for skill_dir in "$SOURCE_DIR"/chinese-legal-*; do
      [[ -d "$skill_dir" ]] || continue
      name="$(basename "$skill_dir")"
      rm -rf "$TARGET_DIR/$name"
      ln -s "$skill_dir" "$TARGET_DIR/$name"
      echo "已链接：$TARGET_DIR/$name -> $skill_dir"
    done
    ;;
  copy|--copy)
    for skill_dir in "$SOURCE_DIR"/chinese-legal-*; do
      [[ -d "$skill_dir" ]] || continue
      name="$(basename "$skill_dir")"
      rm -rf "$TARGET_DIR/$name"
      cp -R "$skill_dir" "$TARGET_DIR/$name"
      echo "已复制：$TARGET_DIR/$name"
    done
    ;;
  *)
    echo "用法：scripts/install-dsh.sh [link|copy]" >&2
    exit 1
    ;;
esac

# Record the repository location so user-level adapters can resolve
# repository-relative paths (domain CLAUDE.md, skills, references) from any
# workspace. Plain text file, one absolute path, no secrets.
printf '%s\n' "$ROOT_DIR" > "$STATE_DIR/repo"
echo "已登记仓库路径：$STATE_DIR/repo -> $ROOT_DIR"

# Idempotent managed block in the user-global AGENTS.md. dsh loads
# ~/.dsh/AGENTS.md into every session's baseline instructions.
touch "$AGENTS_FILE"
BLOCK_START='<!-- legal-zh:start -->'
BLOCK_END='<!-- legal-zh:end -->'
if grep -qF "$BLOCK_START" "$AGENTS_FILE"; then
  # Replace the existing managed block in place (keep surrounding content).
  # awk index() = fixed-string match, portable across BSD/GNU (no sed -i divergence).
  tmp="$(mktemp)"
  awk -v s="$BLOCK_START" -v e="$BLOCK_END" '
    index($0, s) { skip = 1 }
    !skip { print }
    index($0, e) { skip = 0 }
  ' "$AGENTS_FILE" > "$tmp" && mv "$tmp" "$AGENTS_FILE"
fi
cat >> "$AGENTS_FILE" <<'EOF'

<!-- legal-zh:start -->
## 中国法律工作守则（claude-for-legal-zh）

任务涉及中国法律实务时：

- 优先调用匹配的 `chinese-legal-*` skill，路由到对应领域的工作流（领域 CLAUDE.md + skills/*/SKILL.md）。
- 领域文件的仓库相对路径以 `~/.dsh/legal-zh/repo` 中登记的仓库根目录为基准解析。
- 所有法律输出均为律师审查草稿，不替代律师专业判断。
- 法条、案例、期限、监管动态等时效性内容，未经可靠来源核验前一律标注“需验证”。
- 保留原工作流的升级、审批、保密与来源标注要求。
<!-- legal-zh:end -->
EOF
echo "已更新全局指令：${AGENTS_FILE}（legal-zh 受管块）"

echo
echo "DeepSeek Harness 适配技能已安装到：$TARGET_DIR"
echo "请重启 dsh 会话（或重新打开 dsh web 页面），让新的 skills 进入索引。"
