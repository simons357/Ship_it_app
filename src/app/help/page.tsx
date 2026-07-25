import type { Metadata } from "next";
import Link from "next/link";
import { SiteHeader } from "@/components/site-header";

export const metadata: Metadata = {
  title: "Help",
  description:
    "How Ship it works — a short path from done to delivered.",
};

const steps = [
  {
    title: "Ship it to?",
    body: "Pick a standard destination or choose Custom and type exactly where it should go.",
  },
  {
    title: "What do you want to happen?",
    body: "Put the outcome in the box — send a file, share a link, deliver work, save it, or Custom. Attach a file or link if you need to.",
  },
  {
    title: "Semi-personal note",
    body: "Add a short human line, glance at the summary, then tap Ship it.",
  },
];

export default function HelpPage() {
  return (
    <div className="relative flex min-h-full flex-1 flex-col bg-foam">
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-72 bg-[radial-gradient(ellipse_at_top,color-mix(in_oklab,var(--sea)_16%,transparent),transparent_70%)]"
        aria-hidden="true"
      />
      <SiteHeader ctaHref="/ship" ctaLabel="Ship it" />

      <main className="relative z-10 mx-auto w-full max-w-3xl flex-1 px-6 pb-20 pt-8 sm:px-10">
        <header className="mb-12">
          <p className="font-mono text-xs uppercase tracking-[0.18em] text-sea-deep">
            Help
          </p>
          <h1 className="mt-3 font-[family-name:var(--font-display)] text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            A standard path when you’re done
          </h1>
          <p className="mt-4 text-base leading-relaxed text-ink-soft">
            No maze. One question at a time, always a Custom option, then a
            note — and it’s taken care of.
          </p>
        </header>

        <section className="mb-14">
          <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
            The path
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
            href="/ship"
            className="mt-8 inline-flex rounded-md bg-sea px-5 py-2.5 text-sm font-semibold text-foam transition-colors hover:bg-sea-deep"
          >
            Start shipping
          </Link>
        </section>

        <section className="mb-14">
          <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
            Why it’s built this way
          </h2>
          <p className="mt-3 text-sm leading-relaxed text-ink-soft">
            Finishing something shouldn’t mean another twenty minutes of
            figuring out how to send it. Ship it keeps the same short line every
            time so you can count on the path — A to B to C — then boom.
          </p>
        </section>

        <section>
          <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
            What’s next
          </h2>
          <p className="mt-3 text-sm leading-relaxed text-ink-soft">
            Today the flow runs in demo mode and confirms locally. Live
            destinations (email, drive, messaging) plug into the same steps —
            the path stays standard; only the last mile gets real.
          </p>
        </section>
      </main>
    </div>
  );
}
