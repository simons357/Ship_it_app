# Cursor Setup Advisor

Personal Cursor agent for **jonathan simons** — helps you navigate Cursor features and configure them correctly.

## What you get

| Piece | What it does | How to use |
| --- | --- | --- |
| **cursor-setup-advisor** subagent | Decision coach for Rules, Skills, Subagents, Cloud Agents, Automations, MCP, Plugins, Bugbot | Ask Agent to use `cursor-setup-advisor`, or `/cursor-setup-advisor` |
| **/cursor-setup-check** skill | Audits your setup and lists the next 3 actions | Type `/cursor-setup-check` in Agent chat |
| **/choose-cursor-feature** skill | Picks the right feature for a goal | Type `/choose-cursor-feature` or ask "what should I use for…" |
| Project rule | Auto-surfaces this guidance when you ask setup questions | Works in this repo via `.cursor/rules/` |

## Use it in this repo (already wired)

This repository includes:

```text
.cursor/
├── agents/cursor-setup-advisor.md
├── rules/cursor-setup-advisor.mdc
└── skills/
    ├── cursor-setup-check/
    └── choose-cursor-feature/
```

Open Agent chat in this project and try:

- `Use cursor-setup-advisor: should I use a Rule or a Skill for my coding style?`
- `/cursor-setup-check`
- `/choose-cursor-feature I want something that reviews PRs automatically`

## Install for all projects (recommended)

So the advisor follows you everywhere, install it at **user** scope.

### Option A — User subagent + skills (simplest)

From this repo root:

```bash
mkdir -p ~/.cursor/agents \
  ~/.cursor/skills/cursor-setup-check/references \
  ~/.cursor/skills/choose-cursor-feature

cp .cursor/agents/cursor-setup-advisor.md ~/.cursor/agents/
cp .cursor/skills/cursor-setup-check/SKILL.md ~/.cursor/skills/cursor-setup-check/
cp .cursor/skills/cursor-setup-check/references/decision-map.md ~/.cursor/skills/cursor-setup-check/references/
cp .cursor/skills/choose-cursor-feature/SKILL.md ~/.cursor/skills/choose-cursor-feature/
```

Then reload Cursor (**Developer: Reload Window**) and confirm under **Customize** (filter: user).

### Option B — Local plugin

```bash
mkdir -p ~/.cursor/plugins/local
ln -s "$(pwd)/cursor-setup-advisor" ~/.cursor/plugins/local/cursor-setup-advisor
```

Reload Cursor, then check **Customize** for the **Cursor Setup Advisor** plugin components.

### Option C — Paste a User Rule (always-on nudge)

In **Customize → Rules → User Rules**, add:

```text
When I ask about Cursor setup, configuration, or which Cursor feature to use
(Rules, Skills, Subagents, Cloud Agents, Automations, MCP, Plugins, Bugbot),
act as my setup advisor: recommend one primary feature, give exact steps,
prefer the smallest correct setup, and point to official Cursor docs.
Prefer the cursor-setup-advisor subagent and /cursor-setup-check when available.
```

## First decisions this agent will help with

1. **User Rules vs Project Rules** — global preference vs repo standard  
2. **Skill vs Subagent** — checklist vs named specialist  
3. **Desktop Agent vs Cloud Agent** — chat coding vs remote VM / PR workflows  
4. **Automation or not** — only when you have a real schedule/event trigger  
5. **Which MCP to enable** — only tools you actually use  

## Official docs

- [Customize](https://cursor.com/docs/customize-cursor.md)
- [Rules](https://cursor.com/docs/rules.md)
- [Skills](https://cursor.com/docs/skills.md)
- [Subagents](https://cursor.com/docs/subagents.md)
- [Cloud Agents](https://cursor.com/docs/cloud-agent.md)
- [Automations](https://cursor.com/docs/cloud-agent/automations.md)
- [Plugins](https://cursor.com/docs/plugins.md)

## Plugin package

The installable plugin lives in [`cursor-setup-advisor/`](../cursor-setup-advisor/).
