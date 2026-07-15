export type RepoVisibility = "public" | "private";

export type Repository = {
  id: string;
  owner: string;
  name: string;
  description: string;
  visibility: RepoVisibility;
  defaultBranch: string;
  openPullRequests: number;
  openIssues: number;
  updatedAt: string;
};

export type PullRequest = {
  id: string;
  number: number;
  title: string;
  author: string;
  status: "open" | "draft" | "merged";
  updatedAt: string;
};

export type Issue = {
  id: string;
  number: number;
  title: string;
  author: string;
  labels: string[];
  updatedAt: string;
};
