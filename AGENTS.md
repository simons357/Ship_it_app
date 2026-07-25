# Ship It — notes for Cursor agents

Ship It is Jonathan Simons’ product workspace. The long-term idea: when something is done, follow one short path to send it where it needs to go — instead of reopening the maze of “how do I deliver this?”

## Current product direction

Preferred direction (from draft work already in PRs):

1. **Ship it to?** — destination (preset or Custom)
2. **What do you want to happen?** — outcome (+ optional file/link)
3. **Semi-personal note** — short human line
4. **Ship it** — confirm / send

Older framing (“simpler GitHub file browser”) is historical. Prefer the ship-flow product unless Jonathan explicitly asks otherwise.

## Repo status on `main`

`main` is intentionally thin until foundation PRs are merged:

- Branding under `assets/`
- This file (`AGENTS.md`)
- Human onboarding in `docs/GETTING-STARTED.md`
- Cloud boot config in `.cursor/environment.json`

Application source (Next.js) already exists on draft branches — do **not** rebuild from scratch. Prefer continuing from:

- App + ship flow: PR #8 (`cursor/ship-it-app-e279`)
- Earlier GitHub-workspace prototype: PR #4 (`cursor/initial-app-setup-3441`) — superseded by #8 for product direction

## Cursor Cloud boot

`.cursor/environment.json` runs:

```bash
if [ -f package.json ]; then npm ci 2>/dev/null || npm install; fi
```

Once `package.json` exists:

```bash
npm install
npm run dev    # http://localhost:3000
npm run lint
npm run build
```

## How to work in this repo

1. One task → one branch → one PR.
2. Prefer extending existing draft branches over inventing parallel apps.
3. Keep secrets out of git; use Cloud Agent secrets / `.env.local` from `.env.example`.
4. Reuse branding in `assets/` (icon + wallpaper). If binaries look corrupted, keep the typographic wordmark and note it.
5. Explain changes in plain language in the PR body — Jonathan is learning the workflow.

## What agents should avoid

- Do not create another empty “initial setup” that ignores existing draft PRs.
- Do not require Docker unless the task truly needs it.
- Do not invent OAuth / API credentials; document required secrets instead.
- Do not pile portfolio / art / unrelated experiments into the Ship It app unless asked.
