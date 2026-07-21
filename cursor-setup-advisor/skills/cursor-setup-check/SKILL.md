---
name: cursor-setup-check
description: Audit Jonathan's Cursor setup and recommend the next correct configuration steps. Use when he asks to check, review, audit, or finish setting up Cursor, or when he is unsure what is missing.
disable-model-invocation: false
---

# Cursor setup check

Run a practical audit of Cursor configuration and produce a prioritized action list.

## When to use

- "Am I set up correctly?"
- "What should I configure next in Cursor?"
- "Audit my Rules / Skills / Agents / MCP / Cloud setup"

## Procedure

Work through these areas in order. For each, report: **Present / Missing / Unclear**, then one recommended action.

### 1. Personal guidance layer
- User Rule for communication / preferences (Customize → Rules)
- User subagent `cursor-setup-advisor` at `~/.cursor/agents/cursor-setup-advisor.md` (or installed plugin)
- This skill available via `/cursor-setup-check`

### 2. Project guidance layer (current repo)
- `.cursor/rules/` or `AGENTS.md` for repo conventions
- Project skills under `.cursor/skills/` only if the repo needs them
- Avoid duplicating the same instruction in Rules and Skills

### 3. Integrations
- MCP servers: only keep ones Jonathan actively uses
- GitHub/GitLab connected if Cloud Agents or Bugbot are desired
- Secrets configured for any MCP/cloud tools that need them

### 4. Cloud & automation (optional)
- Cloud Agent environment at https://cursor.com/dashboard/cloud-agents#environments only if he wants cloud runs
- Private Automations only if there is a real schedule/event trigger
- Skip this section if he only uses desktop Agent chat

### 5. Quality tools (optional)
- Bugbot for PR review: https://cursor.com/dashboard/bugbot
- Do not recommend Bugbot as a setup advisor substitute

## Output format

```markdown
## Cursor setup status
- Overall: Ready / Almost ready / Needs setup

## Findings
| Area | Status | Next step |
| --- | --- | --- |
| ... | Present/Missing/Unclear | ... |

## Do this next (max 3)
1. ...
2. ...
3. ...

## Skip for now
- ...
```

## Rules of thumb while auditing

- Prefer **user-scoped** advisor pieces so they work in every project.
- One job → one feature.
- Cite official docs when recommending a feature.
- Read `references/decision-map.md` in this skill when choosing between features.
