import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SiteHeader } from "@/components/site-header";
import {
  formatRelativeDate,
  mockIssues,
  mockPullRequests,
  mockRepositories,
} from "@/lib/github/mock-data";

type PageProps = {
  params: Promise<{ owner: string; name: string }>;
};

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { owner, name } = await params;
  return { title: `${owner}/${name}` };
}

export default async function RepositoryPage({ params }: PageProps) {
  const { owner, name } = await params;
  const fullName = `${owner}/${name}`;
  const repo = mockRepositories.find(
    (item) => item.owner === owner && item.name === name,
  );

  if (!repo) {
    notFound();
  }

  const pullRequests = mockPullRequests[fullName] ?? [];
  const issues = mockIssues[fullName] ?? [];

  return (
    <div className="relative flex min-h-full flex-1 flex-col bg-foam">
      <SiteHeader ctaHref="/workspace" ctaLabel="All repos" />

      <main className="relative z-10 mx-auto w-full max-w-4xl flex-1 px-6 pb-16 pt-8 sm:px-10">
        <Link
          href="/workspace"
          className="text-sm text-ink-soft transition-colors hover:text-ink"
        >
          ← Workspace
        </Link>

        <header className="mt-6 mb-12">
          <p className="font-mono text-xs uppercase tracking-[0.18em] text-sea-deep">
            {repo.visibility} · {repo.defaultBranch}
          </p>
          <h1 className="mt-3 font-[family-name:var(--font-display)] text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            {owner}/{name}
          </h1>
          <p className="mt-3 max-w-2xl text-base leading-relaxed text-ink-soft">
            {repo.description}
          </p>
        </header>

        <section className="mb-12">
          <h2 className="font-[family-name:var(--font-display)] text-xl font-semibold text-ink">
            Pull requests
          </h2>
          <p className="mt-1 text-sm text-ink-soft">
            Review and ship without opening GitHub in another tab.
          </p>
          {pullRequests.length === 0 ? (
            <p className="mt-6 text-sm text-ink-soft">No open pull requests.</p>
          ) : (
            <ul className="mt-6 divide-y divide-line border-y border-line">
              {pullRequests.map((pr) => (
                <li
                  key={pr.id}
                  className="flex flex-col gap-1 py-4 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div>
                    <p className="font-medium text-ink">
                      #{pr.number} {pr.title}
                    </p>
                    <p className="mt-1 text-sm text-ink-soft">
                      {pr.author} · {pr.status}
                    </p>
                  </div>
                  <span className="text-sm text-ink-soft">
                    {formatRelativeDate(pr.updatedAt)}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section>
          <h2 className="font-[family-name:var(--font-display)] text-xl font-semibold text-ink">
            Issues
          </h2>
          <p className="mt-1 text-sm text-ink-soft">
            Track work that still needs a home.
          </p>
          {issues.length === 0 ? (
            <p className="mt-6 text-sm text-ink-soft">No open issues listed.</p>
          ) : (
            <ul className="mt-6 divide-y divide-line border-y border-line">
              {issues.map((issue) => (
                <li
                  key={issue.id}
                  className="flex flex-col gap-1 py-4 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div>
                    <p className="font-medium text-ink">
                      #{issue.number} {issue.title}
                    </p>
                    <p className="mt-1 text-sm text-ink-soft">
                      {issue.author}
                      {issue.labels.length > 0
                        ? ` · ${issue.labels.join(", ")}`
                        : ""}
                    </p>
                  </div>
                  <span className="text-sm text-ink-soft">
                    {formatRelativeDate(issue.updatedAt)}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}
