export type RepoVisibility = "public" | "private";

export type Repository = {
  id: string;
  owner: string;
  name: string;
  description: string;
  visibility: RepoVisibility;
  defaultBranch: string;
  fileCount: number;
  updatedAt: string;
};

export type RepoEntryKind = "file" | "dir";

export type RepoEntry = {
  id: string;
  name: string;
  path: string;
  kind: RepoEntryKind;
  sizeLabel?: string;
  updatedAt: string;
};

export type ShipAction = "add" | "update" | "delete";

export type RecentShip = {
  id: string;
  action: ShipAction;
  path: string;
  message: string;
  sha: string;
  createdAt: string;
};
