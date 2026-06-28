#!/usr/bin/env sh
set -eu

SKILL_NAME="specforge-skill"
SRC_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PLATFORM="${1:-codex}"

copy_skill() {
  dest="$1"
  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  cp -R "$SRC_DIR" "$dest"
  echo "Installed $SKILL_NAME to $dest"
}

case "$PLATFORM" in
  --platform)
    PLATFORM="${2:-codex}"
    ;;
esac

case "$PLATFORM" in
  codex|universal)
    copy_skill "$HOME/.agents/skills/$SKILL_NAME"
    ;;
  claude)
    copy_skill "$HOME/.claude/skills/$SKILL_NAME"
    ;;
  cursor)
    copy_skill "$(pwd)/.cursor/skills/$SKILL_NAME"
    ;;
  antigravity)
    copy_skill "$(pwd)/.agent/skills/$SKILL_NAME"
    ;;
  all)
    copy_skill "$HOME/.agents/skills/$SKILL_NAME"
    copy_skill "$HOME/.claude/skills/$SKILL_NAME"
    copy_skill "$(pwd)/.cursor/skills/$SKILL_NAME"
    copy_skill "$(pwd)/.agent/skills/$SKILL_NAME"
    ;;
  *)
    echo "Unknown platform: $PLATFORM" >&2
    echo "Use: codex, universal, claude, cursor, antigravity, all" >&2
    exit 2
    ;;
esac

echo "Invoke with: /specforge <product idea>"
