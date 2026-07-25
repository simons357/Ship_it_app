# Ship it

When you’re done, don’t reopen the maze. Answer a few short questions, drop a note, and ship it where you want it.

**Path:** To → What happens → Note → Boom

## Start here

If you’re learning how this repo and Cursor agents fit together, read:

**[docs/GETTING-STARTED.md](docs/GETTING-STARTED.md)**

That page explains repos, branches, pull requests, and how to use agents without getting lost.

## What’s on `main` right now

Foundation only:

| Path | Purpose |
| --- | --- |
| `docs/GETTING-STARTED.md` | Human map — repos + agents |
| `AGENTS.md` | Instructions for Cursor agents |
| `.cursor/environment.json` | Cloud Agent boot / install |
| `assets/` | Brand icon + wallpaper |

The clickable Next.js app already exists as a **draft PR** — it is not on `main` until you merge it.

## Recommended merge order

1. This foundation (map + agent boot)
2. [PR #8 — ship flow app](https://github.com/simons357/Ship_it_app/pull/8)
3. Optional: [PR #6 — Cursor setup advisor](https://github.com/simons357/Ship_it_app/pull/6)

After PR #8 is merged:

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Product idea

Finishing something shouldn’t cost another pile of time just to send it. Ship it keeps one short path you can count on. Presets for speed, Custom when you need it, then a semi-personal note — and it’s taken care of.

## Brand assets

- `assets/shipit_final_apple_icon.png`
- `assets/shipit_final_desktop_wallpaper.png`
