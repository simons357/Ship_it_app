# Cursor feature decision map

Use this when recommending what to configure.

## Always-on behavior
→ **User Rules** (all projects) or **Project Rules** / **AGENTS.md** (one repo)

## Named personal helper
→ **User Subagent** in `~/.cursor/agents/`

## Checklist / repeatable workflow
→ **Skill** in `~/.cursor/skills/<name>/SKILL.md` or project `.cursor/skills/`

## Talk to Notion / Linear / Figma / Datadog / etc.
→ **MCP** via Customize

## Bundle and reuse across machines
→ **Plugin** (local: `~/.cursor/plugins/local/`, or Marketplace)

## Background coding on a repo
→ **Cloud Agents** + environment setup

## Scheduled or event-driven agent
→ **Private Automation** (`/automate` or https://cursor.com/automations)

## PR review quality
→ **Bugbot**

## Anti-patterns
- Putting setup advice only in `AGENTS.md` (that is project-scoped, not personal)
- Creating an Automation for interactive Q&A
- Duplicating the same text as Rule + Skill + Subagent
- Enabling many MCP servers "just in case"
