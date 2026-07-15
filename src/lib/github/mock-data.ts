import type { Issue, PullRequest, Repository } from "./types";

export const mockRepositories: Repository[] = [
  {
    id: "1",
    owner: "simons357",
    name: "Ship_it_app",
    description: "Manage GitHub work without living in github.com.",
    visibility: "private",
    defaultBranch: "main",
    openPullRequests: 2,
    openIssues: 4,
    updatedAt: "2026-07-14T18:22:00Z",
  },
  {
    id: "2",
    owner: "simons357",
    name: "harbor-notes",
    description: "Personal shipping notes and release checklists.",
    visibility: "private",
    defaultBranch: "main",
    openPullRequests: 0,
    openIssues: 1,
    updatedAt: "2026-07-12T09:10:00Z",
  },
  {
    id: "3",
    owner: "simons357",
    name: "dockside-cli",
    description: "Command-line helpers for repo cleanup and releases.",
    visibility: "public",
    defaultBranch: "main",
    openPullRequests: 1,
    openIssues: 3,
    updatedAt: "2026-07-10T15:44:00Z",
  },
];

export const mockPullRequests: Record<string, PullRequest[]> = {
  "simons357/Ship_it_app": [
    {
      id: "pr-1",
      number: 12,
      title: "Initial app setup and workspace shell",
      author: "simons357",
      status: "open",
      updatedAt: "2026-07-15T10:00:00Z",
    },
    {
      id: "pr-2",
      number: 9,
      title: "Draft GitHub OAuth connect flow",
      author: "simons357",
      status: "draft",
      updatedAt: "2026-07-13T16:30:00Z",
    },
  ],
};

export const mockIssues: Record<string, Issue[]> = {
  "simons357/Ship_it_app": [
    {
      id: "i-1",
      number: 4,
      title: "Wire real GitHub API for repository list",
      author: "simons357",
      labels: ["setup", "backend"],
      updatedAt: "2026-07-14T12:00:00Z",
    },
    {
      id: "i-2",
      number: 3,
      title: "Replace corrupted brand assets",
      author: "simons357",
      labels: ["design"],
      updatedAt: "2026-07-13T08:20:00Z",
    },
  ],
};

export function formatRelativeDate(iso: string): string {
  const then = new Date(iso).getTime();
  const now = Date.now();
  const diffHours = Math.max(1, Math.round((now - then) / (1000 * 60 * 60)));

  if (diffHours < 24) {
    return `${diffHours}h ago`;
  }

  const days = Math.round(diffHours / 24);
  return `${days}d ago`;
}
