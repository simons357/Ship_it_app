import Link from "next/link";
import { BrandMark } from "./brand-mark";

export function SiteHeader({
  ctaHref = "/workspace",
  ctaLabel = "Open workspace",
}: {
  ctaHref?: string;
  ctaLabel?: string;
}) {
  return (
    <header className="relative z-10 flex items-center justify-between px-6 py-5 sm:px-10">
      <Link href="/" className="transition-opacity hover:opacity-80">
        <BrandMark size="sm" />
      </Link>
      <nav className="flex items-center gap-6 text-sm text-ink-soft">
        <Link href="/workspace" className="transition-colors hover:text-ink">
          Workspace
        </Link>
        <Link
          href={ctaHref}
          className="rounded-md bg-ink px-4 py-2 font-medium text-foam transition-colors hover:bg-ink-soft"
        >
          {ctaLabel}
        </Link>
      </nav>
    </header>
  );
}
