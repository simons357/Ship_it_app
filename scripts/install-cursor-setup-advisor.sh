#!/usr/bin/env bash
# Install Cursor Setup Advisor into your user Cursor config (~/.cursor).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_AGENT="$ROOT/.cursor/agents/cursor-setup-advisor.md"
SRC_CHECK="$ROOT/.cursor/skills/cursor-setup-check"
SRC_CHOOSE="$ROOT/.cursor/skills/choose-cursor-feature"
PLUGIN_SRC="$ROOT/cursor-setup-advisor"

DEST_AGENTS="${HOME}/.cursor/agents"
DEST_SKILLS="${HOME}/.cursor/skills"
DEST_PLUGIN="${HOME}/.cursor/plugins/local/cursor-setup-advisor"

mkdir -p "$DEST_AGENTS" \
  "$DEST_SKILLS/cursor-setup-check/references" \
  "$DEST_SKILLS/choose-cursor-feature" \
  "$(dirname "$DEST_PLUGIN")"

cp "$SRC_AGENT" "$DEST_AGENTS/cursor-setup-advisor.md"
cp "$SRC_CHECK/SKILL.md" "$DEST_SKILLS/cursor-setup-check/SKILL.md"
cp "$SRC_CHECK/references/decision-map.md" "$DEST_SKILLS/cursor-setup-check/references/decision-map.md"
cp "$SRC_CHOOSE/SKILL.md" "$DEST_SKILLS/choose-cursor-feature/SKILL.md"

if [[ -e "$DEST_PLUGIN" || -L "$DEST_PLUGIN" ]]; then
  rm -rf "$DEST_PLUGIN"
fi
ln -s "$PLUGIN_SRC" "$DEST_PLUGIN"

cat <<EOF
Installed Cursor Setup Advisor for user: ${USER}

  Subagent:  ${DEST_AGENTS}/cursor-setup-advisor.md
  Skills:    ${DEST_SKILLS}/cursor-setup-check
             ${DEST_SKILLS}/choose-cursor-feature
  Plugin:    ${DEST_PLUGIN} -> ${PLUGIN_SRC}

Next:
  1. Reload Cursor (Command Palette → Developer: Reload Window)
  2. Open Customize and confirm user-scoped advisor / skills
  3. Optional: paste the User Rule from docs/CURSOR-SETUP-ADVISOR.md
  4. In Agent chat run: /cursor-setup-check
EOF
