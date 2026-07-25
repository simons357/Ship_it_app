# Ship it

Manage what you put on GitHub without living on github.com — pick a repo, browse files, and ship adds, updates, and deletions with a clear commit message.

## Requirements

- Node.js 20+ (22 recommended)
- npm 10+

## Local setup

```bash
# Install dependencies
npm install

# Copy environment template (optional until OAuth is wired)
cp .env.example .env.local

# Start the Next.js dev server
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

- Branded landing page
- Workspace with sample repositories
- Repo file browser + ship composer (add / update / delete)
- Recent ships history (local demo)
- In-app Help (`/help`) and markdown guide (`docs/HELP.md`)
- Type stubs ready for a real GitHub API / OAuth connection

## Product flow

1. Open the workspace and choose a repository
2. Browse folders and select a file (optional)
3. Choose Add, Update, or Delete
4. Set the path, attach a file when needed, write a commit message
5. Tap **Ship** — demo mode confirms locally; live mode will commit via GitHub

## GitHub connection (next step)

1. Create a GitHub OAuth App at https://github.com/settings/developers
2. Set the callback URL to `http://localhost:3000/api/auth/callback`
3. Put the client id and secret in `.env.local` (see `.env.example`)
4. Replace the mock helpers in `src/lib/github/` with live Octokit Contents API calls

## Help

- In-app: [/help](http://localhost:3000/help)
- Markdown: [docs/HELP.md](docs/HELP.md)

## Brand assets

Original artwork lives in `assets/`. The PNG/JPG uploads in this repo were corrupted during commit (binary bytes replaced), so the UI currently uses a typographic wordmark. Re-export `shipit_final_apple_icon.png` and `shipit_final_desktop_wallpaper.png` as valid binary files when you have the source art again.

## Stack

- Next.js (App Router) + React + TypeScript
- Tailwind CSS v4
