import type { RecentShip, RepoEntry, Repository } from "./types";

export const mockRepositories: Repository[] = [
  {
    id: "1",
    owner: "simons357",
    name: "Ship_it_app",
    description: "Manage GitHub content without living on github.com.",
    visibility: "private",
    defaultBranch: "main",
    fileCount: 12,
    updatedAt: "2026-07-14T18:22:00Z",
  },
  {
    id: "2",
    owner: "simons357",
    name: "harbor-notes",
    description: "Personal shipping notes and release checklists.",
    visibility: "private",
    defaultBranch: "main",
    fileCount: 8,
    updatedAt: "2026-07-12T09:10:00Z",
  },
  {
    id: "3",
    owner: "simons357",
    name: "dockside-cli",
    description: "Command-line helpers for repo cleanup and releases.",
    visibility: "public",
    defaultBranch: "main",
    fileCount: 21,
    updatedAt: "2026-07-10T15:44:00Z",
  },
];

export const mockRepoTrees: Record<string, RepoEntry[]> = {
  "simons357/Ship_it_app": [
    {
      id: "d-assets",
      name: "assets",
      path: "assets",
      kind: "dir",
      updatedAt: "2026-07-14T18:22:00Z",
    },
    {
      id: "d-docs",
      name: "docs",
      path: "docs",
      kind: "dir",
      updatedAt: "2026-07-14T14:10:00Z",
    },
    {
      id: "d-src",
      name: "src",
      path: "src",
      kind: "dir",
      updatedAt: "2026-07-15T10:00:00Z",
    },
    {
      id: "f-readme",
      name: "README.md",
      path: "README.md",
      kind: "file",
      sizeLabel: "2.1 KB",
      updatedAt: "2026-07-15T11:00:00Z",
    },
    {
      id: "f-pkg",
      name: "package.json",
      path: "package.json",
      kind: "file",
      sizeLabel: "612 B",
      updatedAt: "2026-07-15T10:00:00Z",
    },
  ],
  "simons357/Ship_it_app/assets": [
    {
      id: "f-icon",
      name: "shipit_final_apple_icon.png",
      path: "assets/shipit_final_apple_icon.png",
      kind: "file",
      sizeLabel: "2.3 MB",
      updatedAt: "2026-07-14T18:20:00Z",
    },
    {
      id: "f-wall",
      name: "shipit_final_desktop_wallpaper.png",
      path: "assets/shipit_final_desktop_wallpaper.png",
      kind: "file",
      sizeLabel: "3.8 MB",
      updatedAt: "2026-07-14T18:22:00Z",
    },
  ],
  "simons357/Ship_it_app/docs": [
    {
      id: "f-help",
      name: "HELP.md",
      path: "docs/HELP.md",
      kind: "file",
      sizeLabel: "5.4 KB",
      updatedAt: "2026-07-14T14:10:00Z",
    },
  ],
  "simons357/Ship_it_app/src": [
    {
      id: "d-app",
      name: "app",
      path: "src/app",
      kind: "dir",
      updatedAt: "2026-07-15T10:00:00Z",
    },
    {
      id: "d-components",
      name: "components",
      path: "src/components",
      kind: "dir",
      updatedAt: "2026-07-15T10:00:00Z",
    },
  ],
  "simons357/harbor-notes": [
    {
      id: "f-inbox",
      name: "inbox.md",
      path: "inbox.md",
      kind: "file",
      sizeLabel: "1.4 KB",
      updatedAt: "2026-07-12T09:10:00Z",
    },
    {
      id: "f-ship-log",
      name: "ship-log.md",
      path: "ship-log.md",
      kind: "file",
      sizeLabel: "3.2 KB",
      updatedAt: "2026-07-11T16:40:00Z",
    },
    {
      id: "d-checklists",
      name: "checklists",
      path: "checklists",
      kind: "dir",
      updatedAt: "2026-07-10T12:00:00Z",
    },
  ],
  "simons357/harbor-notes/checklists": [
    {
      id: "f-release",
      name: "release.md",
      path: "checklists/release.md",
      kind: "file",
      sizeLabel: "890 B",
      updatedAt: "2026-07-10T12:00:00Z",
    },
  ],
  "simons357/dockside-cli": [
    {
      id: "f-cli-readme",
      name: "README.md",
      path: "README.md",
      kind: "file",
      sizeLabel: "4.0 KB",
      updatedAt: "2026-07-10T15:44:00Z",
    },
    {
      id: "d-bin",
      name: "bin",
      path: "bin",
      kind: "dir",
      updatedAt: "2026-07-09T11:20:00Z",
    },
    {
      id: "f-license",
      name: "LICENSE",
      path: "LICENSE",
      kind: "file",
      sizeLabel: "1.1 KB",
      updatedAt: "2026-06-01T08:00:00Z",
    },
  ],
  "simons357/dockside-cli/bin": [
    {
      id: "f-dock",
      name: "dock",
      path: "bin/dock",
      kind: "file",
      sizeLabel: "2.8 KB",
      updatedAt: "2026-07-09T11:20:00Z",
    },
  ],
};

export const mockRecentShips: Record<string, RecentShip[]> = {
  "simons357/Ship_it_app": [
    {
      id: "ship-1",
      action: "add",
      path: "assets/shipit_final_desktop_wallpaper.png",
      message: "Add desktop wallpaper assets",
      sha: "46684be",
      createdAt: "2026-07-14T18:22:00Z",
    },
    {
      id: "ship-2",
      action: "update",
      path: "README.md",
      message: "Clarify local setup steps",
      sha: "71f909e",
      createdAt: "2026-07-15T11:07:00Z",
    },
  ],
  "simons357/harbor-notes": [
    {
      id: "ship-3",
      action: "update",
      path: "inbox.md",
      message: "Capture week-of shipping notes",
      sha: "a91c2ef",
      createdAt: "2026-07-12T09:10:00Z",
    },
  ],
  "simons357/dockside-cli": [
    {
      id: "ship-4",
      action: "add",
      path: "bin/dock",
      message: "Add dock helper script",
      sha: "c4e81aa",
      createdAt: "2026-07-09T11:20:00Z",
    },
  ],
};

export function getRepository(owner: string, name: string) {
  return mockRepositories.find(
    (item) => item.owner === owner && item.name === name,
  );
}

export function getTreeEntries(owner: string, name: string, dirPath = "") {
  const key = dirPath
    ? `${owner}/${name}/${dirPath}`
    : `${owner}/${name}`;
  return mockRepoTrees[key] ?? [];
}

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

export function actionLabel(action: RecentShip["action"]): string {
  switch (action) {
    case "add":
      return "Added";
    case "update":
      return "Updated";
    case "delete":
      return "Deleted";
  }
}
