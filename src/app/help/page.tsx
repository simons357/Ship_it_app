import type { Metadata } from "next";
import Link from "next/link";
import { SiteHeader } from "@/components/site-header";

export const metadata: Metadata = {
  title: "Help",
  description:
    "Get started with Ship it — connect GitHub, pick a repo, and ship file changes.",
};

const steps = [
  {
    title: "Open the workspace",
    body: "Browse sample repositories locally. After OAuth is connected, this list becomes your live GitHub account.",
  },
  {
    title: "Choose a repository",
    body: "Confirm you’re on the right branch (usually main), then open the file browser.",
  },
  {
    title: "Ship a change",
    body: "Add, update, or delete a file, write a short commit message, and tap Ship.",
  },
];

const tasks = [
  {
    title: "Upload a new file",
    body: "Choose Add, set the path, pick a file from your device, write a message, then Ship.",
  },
  {
    title: "Update an existing file",
    body: "Select the file in the browser (or paste its path), choose Update, replace the file, then Ship.",
  },
  {
    title: "Delete a file",
    body: "Select the file, choose Delete, confirm with a commit message, then Ship.",
  },
];

export default function HelpPage() {
  return (
    <div className="relative flex min-h-full flex-1 flex-col bg-foam">
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-72 bg-[radial-gradient(ellipse_at_top,color-mix(in_oklab,var(--sea)_16%,transparent),transparent_70%)]"
        aria-hidden="true"
      />
      <SiteHeader ctaHref="/workspace" ctaLabel="Open workspace" />

      <main className="relative z-10 mx-auto w-full max-w-3xl flex-1 px-6 pb-20 pt-8 sm:px-10">
        <header className="mb-12">
          <p className="font-mono text-xs uppercase tracking-[0.18em] text-sea-deep">
            Help
          </p>
          <h1 className="mt-3 font-[family-name:var(--font-display)] text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Manage GitHub without the website maze
          </h1>
          <p className="mt-4 text-base leading-relaxed text-ink-soft">
            Ship it keeps everyday file uploads, updates, and deletions in one
            calm workspace. Full markdown help also lives in{" "}
            <code className="font-mono text-ink">docs/HELP.md</code>.
          </p>
        </header>

        <section className="mb-14">
          <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
            Getting started
          </h2>
          <ol className="mt-6 space-y-6">
            {steps.map((step, index) => (
              <li key={step.title} className="flex gap-4">
                <span className="font-mono text-sm text-sea-deep">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <div>
                  <h3 className="font-semibold text-ink">{step.title}</h3>
                  <p className="mt-1 text-sm leading-relaxed text-ink-soft">
                    {step.body}
                  </p>
                </div>
              </li>
            ))}
          </ol>
          <Link
            href="/workspace"
            className="mt-8 inline-flex rounded-md bg-sea px-5 py-2.5 text-sm font-semibold text-foam transition-colors hover:bg-sea-deep"
          >
            Try the demo workspace
          </Link>
        </section>

        <section className="mb-14">
          <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
            Everyday tasks
          </h2>
          <ul className="mt-6 divide-y divide-line border-y border-line">
            {tasks.map((task) => (
              <li key={task.title} className="py-5">
                <h3 className="font-semibold text-ink">{task.title}</h3>
                <p className="mt-1 text-sm leading-relaxed text-ink-soft">
                  {task.body}
                </p>
              </li>
            ))}
          </ul>
        </section>

        <section className="mb-14">
          <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
            Commit messages that help
          </h2>
          <p className="mt-3 text-sm leading-relaxed text-ink-soft">
            Prefer short, specific, present-tense messages.
          </p>
          <dl className="mt-6 space-y-3 text-sm">
            <div className="flex flex-col gap-1 sm:flex-row sm:gap-8">
              <dt className="font-medium text-ink">Add desktop wallpaper assets</dt>
              <dd className="text-ink-soft line-through">update</dd>
            </div>
            <div className="flex flex-col gap-1 sm:flex-row sm:gap-8">
              <dt className="font-medium text-ink">Fix icons for App Store listing</dt>
              <dd className="text-ink-soft line-through">stuff</dd>
            </div>
            <div className="flex flex-col gap-1 sm:flex-row sm:gap-8">
              <dt className="font-medium text-ink">Remove unused icon</dt>
              <dd className="text-ink-soft line-through">asdf</dd>
            </div>
          </dl>
        </section>

        <section id="connect-github" className="mb-14 scroll-mt-24">
          <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
            Connect GitHub
          </h2>
          <p className="mt-3 text-sm leading-relaxed text-ink-soft">
            The UI runs on sample data today. To land live commits:
          </p>
          <ol className="mt-6 list-decimal space-y-3 pl-5 text-sm leading-relaxed text-ink-soft">
            <li>
              Create a GitHub OAuth App at{" "}
              <a
                href="https://github.com/settings/developers"
                className="text-sea-deep underline-offset-2 hover:underline"
                target="_blank"
                rel="noreferrer"
              >
                github.com/settings/developers
              </a>
              .
            </li>
            <li>
              Set the callback URL to{" "}
              <code className="font-mono text-ink">
                http://localhost:3000/api/auth/callback
              </code>
              .
            </li>
            <li>
              Copy credentials into{" "}
              <code className="font-mono text-ink">.env.local</code> from{" "}
              <code className="font-mono text-ink">.env.example</code>.
            </li>
            <li>
              Replace helpers in{" "}
              <code className="font-mono text-ink">src/lib/github/</code> with
              Octokit Contents API calls.
            </li>
          </ol>
        </section>

        <section>
          <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
            FAQ
          </h2>
          <dl className="mt-6 space-y-6">
            <div>
              <dt className="font-semibold text-ink">
                Do I still need the GitHub website?
              </dt>
              <dd className="mt-1 text-sm leading-relaxed text-ink-soft">
                For everyday file uploads and updates, no. You may still use
                GitHub for pull requests, issues, or advanced git workflows.
              </dd>
            </div>
            <div>
              <dt className="font-semibold text-ink">
                Does Ship it replace git?
              </dt>
              <dd className="mt-1 text-sm leading-relaxed text-ink-soft">
                No. It’s for simple content management on GitHub. Branching,
                merging, and local development still work best with git tools.
              </dd>
            </div>
            <div>
              <dt className="font-semibold text-ink">
                Where are my files stored?
              </dt>
              <dd className="mt-1 text-sm leading-relaxed text-ink-soft">
                On GitHub, in the repository and path you choose — not as a
                permanent mirror only inside Ship it.
              </dd>
            </div>
          </dl>
        </section>
      </main>
    </div>
  );
}
