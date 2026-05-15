#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/.agents/skills"
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
MODE="${1:-link}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "未找到 Codex skills 目录：$SOURCE_DIR" >&2
  echo "请先运行：python3 scripts/generate_codex_adapters.py" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

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
    echo "用法：scripts/install-codex.sh [link|copy]" >&2
    exit 1
    ;;
esac

echo
echo "Codex 适配技能已安装到：$TARGET_DIR"
echo "请重启 Codex Desktop 或 Codex CLI 会话，让新的 skills 进入索引。"
