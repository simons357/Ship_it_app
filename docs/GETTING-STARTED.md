# Getting started — how this repo and agents work

Plain map for Jonathan. The repo name on GitHub is still `Ship_it_app`. That does **not** mean you are building Ship it.

## What went wrong earlier

Agents saw the repo name **Ship_it_app** and turned “Ship it” into setup files, app drafts, and merge checklists.

You abandoned that app. Those files were a wrong assumption about the product — not a requirement.

**Rule going forward:** treat `Ship_it_app` as a **workspace name**, not a product brief.

---

## The three layers

```text
You
  │
  ├─ GitHub repo = permanent home for files
  │     main   = official snapshot right now
  │     branch = sandbox for one idea
  │     PR     = “please put this branch into main”
  │
  └─ Cursor agent = helper that edits a branch
        and usually opens a PR for you to review
```

| Word | Meaning |
| --- | --- |
| **Repo** | The project on GitHub |
| **`main`** | What’s “in” unless you say otherwise |
| **Branch** | A copy where one idea can change safely |
| **PR (pull request)** | A proposal to merge a branch into `main` |
| **Cloud Agent** | Cursor on a remote machine → edits → PR |

Nothing an agent builds is official until you **merge** (or you keep it as a draft on purpose).

---

## What `main` is today

Science / experiment thread: **HB Experiment 01** (closed — held-out null).

See the root [`README.md`](../README.md).

Abandoned product names that should **not** come back:

- Ship it
- Planet Hunter
- Scallion

There is also an open draft that spells this out for agents: [PR #13](https://github.com/simons357/Ship_it_app/pull/13).

---

## How to use agents without getting lost

1. **One clear job** — “Update the HB report summary” beats “set everything up.”
2. **Name the thread** — “anesthesia docs”, “AquaQuartz brochure”, “HB experiment” — not the repo nickname.
3. **Review the PR** — skim summary → files → merge, request changes, or close.
4. **Close dead drafts** — closing is cleanup, not failure. Ship It app PRs should stay closed.

### Cloud vs desktop

- **Cloud Agent** — remote work, good when you want a PR from your phone or while away.
- **Desktop Agent** — live pairing in the Cursor app on your computer.

### Other Cursor pieces (later)

| Tool | When |
| --- | --- |
| Rules | Standing preferences |
| Skills | Repeatable checklists |
| Subagents | Named specialists |
| MCP | Outside tools (Notion, Linear, Figma, …) |
| Automations | Recurring triggers — after basics feel solid |

---

## Suggested next moves

1. Merge a small **workspace foundation** PR (this guide + `AGENTS.md`) so future agents stop reviving Ship it.
2. Merge [PR #13](https://github.com/simons357/Ship_it_app/pull/13) if you still want the longer abandon / anesthesia notes.
3. Pick **one** open draft you care about (AquaQuartz, portfolio, TITAN-X, setup advisor, …) and tell an agent: “Continue from PR #N only.”
4. Leave Ship It / Scallion / Planet Hunter PRs closed.

## Official Cursor docs

- [Cloud Agents](https://cursor.com/docs/cloud-agent.md)
- [Rules](https://cursor.com/docs/rules.md)
- [Skills](https://cursor.com/docs/skills.md)
- [Subagents](https://cursor.com/docs/subagents.md)
