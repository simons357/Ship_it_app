---
name: choose-cursor-feature
description: Help Jonathan choose the right Cursor feature (Rules, Skills, Subagents, Automations, Cloud Agents, MCP, Plugins, Bugbot) for a goal. Use when he asks what to use, how to set something up, or which Cursor option fits.
---

# Choose the right Cursor feature

## Goal

Given what Jonathan wants, recommend **one** primary Cursor feature and the exact setup steps.

## Intake questions (ask only what is missing)

1. Is this for **all projects** or **one repo**?
2. Should it run **while chatting** or **in the background**?
3. Is it a **standing preference**, a **repeatable checklist**, or a **specialist role**?
4. Does it need **external tools** (GitHub events, Slack, Notion, etc.)?

## Decision tree

1. Standing preference / tone / always-true constraint  
   → **User Rules** (global) or **Project Rules** / **AGENTS.md** (repo)

2. Repeatable multi-step workflow he will invoke  
   → **Skill** (`/name`)

3. Specialist that needs its own context across chats/projects  
   → **User Subagent**

4. Needs Notion/Linear/Figma/Datadog/etc. during chat  
   → **MCP** (+ optional Skill that knows how to use it)

5. Should run on a schedule or on GitHub/Slack/webhook events  
   → **Private Automation**

6. Long unattended coding job on a connected repo  
   → **Cloud Agent**

7. Automatic PR bug finding  
   → **Bugbot**

8. Wants to package several of the above for reuse  
   → **Plugin**

## Response template

**Recommendation:** `<feature>`

**Why this fits:** one short paragraph

**Set it up:**
1. Exact clicks / paths / files
2. ...

**Do not use:** `<alternative>` — reason

**Docs:** URL
