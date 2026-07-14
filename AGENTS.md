# Ship It — agent notes

Ship It helps people manage files on GitHub without using the GitHub website: connect an account, pick a repo, and add / update / delete files with clear commit messages.

## Repo status

Today this repository mainly holds branding assets and docs. Application source is expected to land as a standard React + Vite project (Base44-style layout is fine: `src/pages`, `src/components`, `package.json`, `vite.config.js`).

Related placeholder reference: [`simons357/ship-it-code`](https://github.com/simons357/ship-it-code) (`pages/Home.js` notes code may come from Base44).

User-facing help lives in `docs/HELP.md` when that branch is merged.

## Cursor Cloud specific instructions

### Already on the VM

- Node.js 22 + npm / pnpm / yarn
- GitHub CLI (`gh`) authenticated for this workspace
- Python 3.12

### Boot / install

`.cursor/environment.json` runs an idempotent install:

```bash
if [ -f package.json ]; then npm ci 2>/dev/null || npm install; fi
```

Once `package.json` exists, that keeps dependencies current on every agent boot.

### After app source is present

```bash
npm install
npm run dev
```

Vite typically listens on port **5173** (declared in `environment.json`).

If this is a Base44-linked app, create `.env.local` (or add Cloud Agent secrets) with:

```bash
VITE_BASE44_APP_ID=<app id>
VITE_BASE44_APP_BASE_URL=<https://your-app.base44.app>
```

Do not commit secrets. Prefer the Cloud Agents Secrets tab.

### GitHub API work

Use `gh` for GitHub REST/GraphQL when testing repository flows. Prefer fine-scoped tokens or the workspace `gh` auth already available to the agent.

### Branding

Assets under `assets/`:

- `shipit_final_apple_icon.png` — app icon
- `shipit_final_desktop_wallpaper.png` — brand wallpaper
- JPG mockup / reference photo

Reuse these when building UI; do not invent a different logo mark.

### What agents should avoid

- Do not require Docker unless a task truly needs it (not installed by default here).
- Do not invent production OAuth credentials; document required secrets instead.
- Keep `install` light — heavy one-off setup belongs in task-specific commands, not the boot script.
