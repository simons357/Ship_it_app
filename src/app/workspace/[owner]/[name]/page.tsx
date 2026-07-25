import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { DemoBanner } from "@/components/demo-banner";
import { RepoWorkspace } from "@/components/repo-workspace";
import { SiteHeader } from "@/components/site-header";
import { getRepository } from "@/lib/github/mock-data";

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
  const repo = getRepository(owner, name);

  if (!repo) {
    notFound();
  }

  return (
    <div className="relative flex min-h-full flex-1 flex-col bg-foam">
      <SiteHeader ctaHref="/workspace" ctaLabel="All repos" />
      <DemoBanner />

      <main className="relative z-10 mx-auto w-full max-w-5xl flex-1 px-6 pb-16 pt-8 sm:px-10">
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

        <RepoWorkspace repo={repo} />
      </main>
    </div>
  );
}
