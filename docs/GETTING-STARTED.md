# Getting started — repos, agents, and this project

This page is the map. Read it once, then use it whenever things feel confusing.

## The big picture (3 layers)

```text
You (Jonathan)
   │
   ├─ GitHub repo = the permanent home for code
   │     main     = the “official” version
   │     branch   = a workspace for one idea
   │     PR       = “please review / merge this idea into main”
   │
   └─ Cursor agent = a helper that edits code on a branch
         and usually opens a PR for you
```

### Repo

A **repository** (repo) is a project folder on GitHub. Yours for this product is:

[https://github.com/simons357/Ship_it_app](https://github.com/simons357/Ship_it_app)

Right now `main` is almost empty on purpose. Most of the real work is sitting in **draft pull requests** waiting for you to approve.

### Branch

A **branch** is a named copy of the project where an agent (or you) can change things without breaking `main`.

Example: `cursor/ship-it-app-e279`

### Pull request (PR)

A **pull request** is a proposal: “take the work on this branch and put it into `main`.”

- **Draft** = not ready / needs your eyes
- **Open** = ready to review
- **Merged** = now part of `main` (this is when the foundation becomes real)

**Important:** agents can build a lot, but nothing becomes the official project until you **merge** a PR.

### Cloud agent

A **Cloud Agent** is Cursor working on a remote computer connected to your GitHub repo. You give it a goal in plain English. It:

1. Creates a branch
2. Makes changes
3. Commits and pushes
4. Opens a PR for you to review

You do **not** need to know all the git commands. You need to decide: keep, change, or close each PR.

Desktop Agent (in the Cursor app on your computer) is different: it edits files locally while you watch. Cloud Agent is better when you want “go do this and open a PR.”

---

## Your Ship It status today

| Piece | Status |
| --- | --- |
| GitHub repo | Exists and is connected |
| `main` branch | Thin — README + assets + this foundation |
| Working app code | Already drafted in PRs (not merged yet) |
| Branding assets | In `assets/` |
| Cloud Agents | Connected (you’ve already run several) |

### Draft PRs worth knowing

Merge in this order when you’re ready:

| Order | PR | What it is | Recommendation |
| --- | ---: | --- | --- |
| 1 | This foundation PR | Map + agent boot config | Merge first |
| 2 | [#8](https://github.com/simons357/Ship_it_app/pull/8) | Next.js app + ship flow | Merge next — this is the product |
| 3 | [#6](https://github.com/simons357/Ship_it_app/pull/6) | Personal Cursor setup advisor | Optional — helps you use Cursor |
| — | [#4](https://github.com/simons357/Ship_it_app/pull/4) | Earlier GitHub workspace prototype | Skip if you take #8 |
| — | [#2](https://github.com/simons357/Ship_it_app/pull/2) | Older cloud env setup | Superseded by this foundation |
| — | [#1](https://github.com/simons357/Ship_it_app/pull/1), [#3](https://github.com/simons357/Ship_it_app/pull/3), [#5](https://github.com/simons357/Ship_it_app/pull/5), [#7](https://github.com/simons357/Ship_it_app/pull/7), [#9](https://github.com/simons357/Ship_it_app/pull/9) | Help / portfolio / logo / experiments | Keep only if you still want that content |

Closing unused draft PRs is healthy. It is not failure — it is cleanup.

---

## How to use agents well (simple rules)

### 1. Give one clear job per agent

Good:

> Merge-ready: add a /ship page with destination → outcome → note → confirm.

Too vague:

> Set everything up and make the app good.

### 2. Say which repo and which direction

Good:

> In Ship_it_app, continue from the ship-flow product (PR #8). Do not rebuild a GitHub file browser.

### 3. Review the PR, then merge or request changes

On GitHub (or in the Cursor agent page):

1. Open the PR
2. Skim the summary
3. Look at the changed files
4. Merge if it looks right — or reply to the agent: “change X”

### 4. Keep `main` sacred

Only merge work you understand at a high level. After a merge, future agents start from that better `main`.

---

## Cursor building blocks (cheat sheet)

| Tool | Use it when… |
| --- | --- |
| **Cloud Agent** | You want remote work that opens a PR |
| **Desktop Agent** | You’re in the editor and want live pairing |
| **Rules** | Standing preferences (“always use TypeScript”) |
| **Skills** | Repeatable checklists (`/cursor-setup-check`) |
| **Subagents** | Named specialists (setup advisor, reviewer) |
| **MCP** | Connect outside tools (Notion, Linear, Figma, Datadog) |
| **Automations** | Recurring triggers (nightly, on PR open) — later |

Start with Cloud Agents + merging PRs. Add Rules/Skills after the app exists on `main`.

---

## Your next 15 minutes

1. **Merge this foundation PR** so `main` has the map.
2. Open [PR #8](https://github.com/simons357/Ship_it_app/pull/8), read the summary, merge if you want the ship-flow app.
3. On your computer (or a new agent), run:

   ```bash
   npm install
   npm run dev
   ```

4. Open http://localhost:3000 and click through `/ship`.
5. Start a new agent with one concrete next task, for example:

   > Wire the Ship button to create a GitHub issue from the note (demo mode OK).

---

## Official Cursor docs

- [Cloud Agents](https://cursor.com/docs/cloud-agent.md)
- [Rules](https://cursor.com/docs/rules.md)
- [Skills](https://cursor.com/docs/skills.md)
- [Subagents](https://cursor.com/docs/subagents.md)
- [Automations](https://cursor.com/docs/cloud-agent/automations.md)
