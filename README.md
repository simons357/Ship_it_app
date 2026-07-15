# Ship it

Manage what you put on GitHub without living on github.com — review repos, pull requests, and issues from one calm workspace.

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

| Command        | Description                |
| -------------- | -------------------------- |
| `npm run dev`  | Start local development    |
| `npm run build`| Production build           |
| `npm run start`| Serve the production build |
| `npm run lint` | Run ESLint                 |

## What's included

- Branded landing page
- Workspace with sample repositories
- Repo detail view with mock pull requests and issues
- Type stubs ready for a real GitHub API / OAuth connection

## GitHub connection (next step)

1. Create a GitHub OAuth App at https://github.com/settings/developers
2. Set the callback URL to `http://localhost:3000/api/auth/callback`
3. Put the client id and secret in `.env.local` (see `.env.example`)
4. Replace the mock data in `src/lib/github/mock-data.ts` with live Octokit calls

## Brand assets

Original artwork lives in `assets/`. The PNG/JPG uploads in this repo were corrupted during commit (binary bytes replaced), so the UI currently uses a typographic wordmark. Re-export `shipit_final_apple_icon.png` and `shipit_final_desktop_wallpaper.png` as valid binary files when you have the source art again.

## Stack

- Next.js (App Router) + React + TypeScript
- Tailwind CSS v4
