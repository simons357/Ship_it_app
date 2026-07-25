/**
 * Placeholder for a live GitHub client (Octokit + OAuth).
 * The UI currently reads from `mock-data.ts` so local demos work offline.
 *
 * Wire-up checklist:
 * 1. Create a GitHub OAuth App
 * 2. Fill `.env.local` from `.env.example`
 * 3. Exchange the code for a token in `/api/auth/callback`
 * 4. Replace mock helpers with Octokit Contents API calls
 */

export type GitHubClientConfig = {
  token: string;
};

export function createGitHubClient(_config: GitHubClientConfig) {
  throw new Error(
    "Live GitHub client is not wired yet. Use mock data locally, or implement Octokit calls here.",
  );
}
