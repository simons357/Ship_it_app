import Link from "next/link";
import { BrandMark } from "@/components/brand-mark";
import { SiteHeader } from "@/components/site-header";

export default function Home() {
  return (
    <div className="relative flex min-h-full flex-1 flex-col overflow-hidden">
      <div className="atmosphere" aria-hidden="true" />
      <div
        className="pointer-events-none absolute inset-0 opacity-40"
        aria-hidden="true"
        style={{
          backgroundImage:
            "linear-gradient(to right, color-mix(in oklab, var(--ink) 6%, transparent) 1px, transparent 1px), linear-gradient(to bottom, color-mix(in oklab, var(--ink) 6%, transparent) 1px, transparent 1px)",
          backgroundSize: "72px 72px",
          maskImage:
            "radial-gradient(ellipse 80% 70% at 50% 20%, black 20%, transparent 75%)",
        }}
      />

      <SiteHeader ctaHref="/ship" ctaLabel="Start shipping" />

      <main className="relative z-10 flex flex-1 flex-col justify-center px-6 pb-20 pt-10 sm:px-10 lg:px-16">
        <div className="mx-auto w-full max-w-5xl">
          <p className="hero-rise wave-line mb-6 font-mono text-xs uppercase tracking-[0.22em] text-sea-deep">
            Done means gone
          </p>

          <h1 className="hero-rise-delay max-w-4xl">
            <BrandMark size="lg" />
          </h1>

          <p className="hero-rise-delay-2 mt-6 max-w-xl text-lg leading-relaxed text-ink-soft sm:text-xl">
            When you’re finished, don’t reopen the maze. Answer a few short
            questions, drop a note, and ship it where you want it.
          </p>

          <div className="hero-rise-delay-2 mt-10 flex flex-wrap items-center gap-4">
            <Link
              href="/ship"
              className="rounded-md bg-sea px-6 py-3 text-base font-semibold text-foam transition-transform transition-colors hover:bg-sea-deep hover:scale-[1.02] active:scale-[0.99]"
            >
              Ship it
            </Link>
            <Link
              href="/help"
              className="rounded-md px-5 py-3 text-base font-medium text-ink-soft underline-offset-4 transition-colors hover:text-ink hover:underline"
            >
              How the path works
            </Link>
          </div>
        </div>
      </main>

      <footer className="relative z-10 px-6 py-6 text-sm text-ink-soft sm:px-10">
        To → What happens → Note → Boom
      </footer>
    </div>
  );
}
