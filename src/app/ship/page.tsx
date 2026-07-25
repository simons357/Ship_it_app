import type { Metadata } from "next";
import { BrandMark } from "@/components/brand-mark";
import { ShipFlow } from "@/components/ship-flow";
import { SiteHeader } from "@/components/site-header";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Ship",
  description:
    "Follow a short path — where it goes, what should happen, a note — then ship it.",
};

export default function ShipPage() {
  return (
    <div className="relative flex min-h-full flex-1 flex-col bg-foam">
      <div className="atmosphere opacity-60" aria-hidden="true" />
      <SiteHeader ctaHref="/" ctaLabel="Home" />

      <main className="relative z-10 flex flex-1 flex-col px-6 pb-16 pt-6 sm:px-10">
        <div className="mb-10 flex items-center justify-between gap-4">
          <Link href="/" className="transition-opacity hover:opacity-80 sm:hidden">
            <BrandMark size="sm" />
          </Link>
          <p className="hidden text-sm text-ink-soft sm:block">
            A → B → C. Then boom.
          </p>
        </div>
        <ShipFlow />
      </main>
    </div>
  );
}
