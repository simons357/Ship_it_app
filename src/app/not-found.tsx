import Link from "next/link";
import { BrandMark } from "@/components/brand-mark";

export default function NotFound() {
  return (
    <div className="flex min-h-full flex-1 flex-col items-center justify-center px-6 text-center">
      <BrandMark size="md" />
      <h1 className="mt-8 font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
        Nothing here
      </h1>
      <p className="mt-3 max-w-md text-ink-soft">
        That page isn’t on the path. Head home or start a ship.
      </p>
      <div className="mt-8 flex flex-wrap justify-center gap-3">
        <Link
          href="/"
          className="rounded-md px-5 py-2.5 text-sm font-medium text-ink-soft transition-colors hover:text-ink"
        >
          Home
        </Link>
        <Link
          href="/ship"
          className="rounded-md bg-sea px-5 py-2.5 text-sm font-semibold text-foam transition-colors hover:bg-sea-deep"
        >
          Ship it
        </Link>
      </div>
    </div>
  );
}
