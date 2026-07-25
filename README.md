# Ship it

When you’re done, don’t reopen the maze. Answer a few short questions, drop a note, and ship it where you want it.

**Path:** To → What happens → Note → Boom

## Requirements

- Node.js 20+ (22 recommended)
- npm 10+

## Local setup

```bash
npm install
cp .env.example .env.local   # optional for now
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Scripts

| Command         | Description                |
| --------------- | -------------------------- |
| `npm run dev`   | Start local development    |
| `npm run build` | Production build           |
| `npm run start` | Serve the production build |
| `npm run lint`  | Run ESLint                 |

## What's included

- Branded landing page (`/`)
- Linear ship flow (`/ship`) — destination, outcome, note, confirmation
- Always-available **Custom** answers on the choice steps
- In-app Help (`/help`) and [docs/HELP.md](docs/HELP.md)

## Product idea

Finishing something shouldn’t cost another pile of time just to send it. Ship it keeps one standard line you can count on. Presets for speed, Custom when you need it, then a semi-personal note — and it’s taken care of.

Live destinations (email, drive, messaging) plug into the same steps later. Demo mode confirms locally today.

## Brand assets

Artwork lives in `assets/`. Some PNG/JPG uploads were corrupted during an earlier commit; re-export the logo/wallpaper as valid binaries when you have the source art. The UI uses a typographic wordmark until then.

## Stack

- Next.js (App Router) + React + TypeScript
- Tailwind CSS v4
