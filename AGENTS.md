# Notes for Cursor agents

## Product direction (read this first)

Jonathan has **rejected** these early experiments. Do **not** set them up, extend them, or recommend merging them:

- **Ship it** — early Next.js “send path” / GitHub helper. Crappy early program. Dead.
- **Planet Hunter** (and ExoRatio-as-app / exoplanet-hunter product framing) — dead.
- **Scallion** branding/logo — mistake. Dead.

If a draft PR is mainly Ship It, Planet Hunter, or Scallion, **close it** or leave it alone. Do not continue that line of work unless Jonathan explicitly reverses this.

## Repo status on `main`

`main` is thin on purpose: branding assets under `assets/` plus this guidance. There is **no** canonical runnable app on `main` right now.

Prefer continuing from open drafts Jonathan still cares about (portfolio, AquaQuartz, rigor memos, Cursor setup advisor) — **not** from Ship It branches.

## Cursor Cloud

No `package.json` on `main`. Do not invent a Next.js Ship It app to “complete setup.”

If a future merged PR adds a real app with a lockfile, install with that package manager (`npm ci` / `npm install` when `package-lock.json` exists).

## How to work

1. One task → one branch → one PR.
2. Ask Jonathan which thread to extend when unclear — do not default to Ship It.
3. Keep secrets out of git.
4. Explain changes in plain language in the PR body.

## Cursor Cloud specific instructions

- **Do not boot Ship It.** Prefer static portfolio/docs work, or whatever app Jonathan has explicitly approved after the abandoned list above.
- Lint/test/build commands only exist if a merged app brings them; check `package.json` / README on the branch you are actually on.
- For static HTML drafts (portfolio branches), a simple static server is enough, e.g. `python3 -m http.server 8080`.
