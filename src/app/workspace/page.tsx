import type { Metadata } from "next";
import { DemoBanner } from "@/components/demo-banner";
import { SiteHeader } from "@/components/site-header";
import { RepositoryList } from "@/components/repository-list";

export const metadata: Metadata = {
  title: "Workspace",
};

export default function WorkspacePage() {
  return (
    <div className="relative flex min-h-full flex-1 flex-col bg-foam">
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-72 bg-[radial-gradient(ellipse_at_top,color-mix(in_oklab,var(--sea)_18%,transparent),transparent_70%)]"
        aria-hidden="true"
      />
      <SiteHeader ctaHref="/" ctaLabel="Back home" />
      <DemoBanner />

      <main className="relative z-10 mx-auto w-full max-w-4xl flex-1 px-6 pb-16 pt-8 sm:px-10">
        <header className="mb-10">
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Your repos
          </h1>
          <p className="mt-3 max-w-2xl text-base leading-relaxed text-ink-soft">
            Pick a repository to browse files and ship an add, update, or delete
            with a clear commit message.
          </p>
        </header>

        <RepositoryList />
      </main>
    </div>
  );
}
