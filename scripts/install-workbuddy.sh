#!/usr/bin/env bash
# Install claude-for-legal-ZH WorkBuddy adapters.
#
#   scripts/install-workbuddy.sh          # symlink mode (default, auto-updates on git pull)
#   scripts/install-workbuddy.sh copy     # copy mode (standalone snapshot)
#
# What it does:
#   1. Links/copies .workbuddy/skills/chinese-legal-* into ~/.workbuddy/skills/
#   2. Records the absolute repository path in ~/.workbuddy/legal-zh/repo
#      (adapters read it to resolve repository-relative paths from any cwd)
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/.workbuddy/skills"
WB_HOME_DIR="${WORKBUDDY_HOME:-$HOME/.workbuddy}"
TARGET_DIR="$WB_HOME_DIR/skills"
STATE_DIR="$WB_HOME_DIR/legal-zh"
MODE="${1:-link}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "未找到 WorkBuddy skills 目录：$SOURCE_DIR" >&2
  echo "请先运行：python3 scripts/generate_workbuddy_adapters.py" >&2
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
    echo "用法：scripts/install-workbuddy.sh [link|copy]" >&2
    exit 1
    ;;
esac

# Record the repository location so user-level adapters can resolve
# repository-relative paths (domain CLAUDE.md, skills, references) from any
# workspace. Plain text file, one absolute path, no secrets.
printf '%s\n' "$ROOT_DIR" > "$STATE_DIR/repo"
echo "已登记仓库路径：$STATE_DIR/repo -> $ROOT_DIR"

echo
echo "WorkBuddy 适配技能已安装到：$TARGET_DIR"
echo "请在 WorkBuddy 的「专家·技能·连接器」面板确认新技能已启用。"
