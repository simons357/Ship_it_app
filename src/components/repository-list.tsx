import Link from "next/link";
import {
  formatRelativeDate,
  mockRepositories,
} from "@/lib/github/mock-data";

export function RepositoryList() {
  return (
    <ul className="divide-y divide-line border-y border-line">
      {mockRepositories.map((repo) => (
        <li key={repo.id}>
          <Link
            href={`/workspace/${repo.owner}/${repo.name}`}
            className="group flex flex-col gap-2 py-5 transition-colors hover:bg-mist/60 sm:flex-row sm:items-center sm:justify-between sm:gap-8"
          >
            <div className="min-w-0">
              <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                <span className="font-[family-name:var(--font-display)] text-lg font-semibold text-ink transition-colors group-hover:text-sea-deep">
                  {repo.owner}/{repo.name}
                </span>
                <span className="text-xs uppercase tracking-[0.14em] text-ink-soft">
                  {repo.visibility}
                </span>
              </div>
              <p className="mt-1 max-w-2xl text-sm leading-relaxed text-ink-soft">
                {repo.description}
              </p>
            </div>
            <div className="flex shrink-0 flex-wrap gap-4 text-sm text-ink-soft sm:justify-end">
              <span>{repo.openPullRequests} PRs</span>
              <span>{repo.openIssues} issues</span>
              <span>{formatRelativeDate(repo.updatedAt)}</span>
            </div>
          </Link>
        </li>
      ))}
    </ul>
  );
}
