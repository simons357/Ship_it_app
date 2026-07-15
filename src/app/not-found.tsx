import Link from "next/link";
import { BrandMark } from "@/components/brand-mark";

export default function NotFound() {
  return (
    <div className="flex min-h-full flex-1 flex-col items-center justify-center px-6 text-center">
      <BrandMark size="md" />
      <h1 className="mt-8 font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
        Repo not found
      </h1>
      <p className="mt-3 max-w-md text-ink-soft">
        That repository is not in the local sample set yet.
      </p>
      <Link
        href="/workspace"
        className="mt-8 rounded-md bg-sea px-5 py-2.5 text-sm font-semibold text-foam transition-colors hover:bg-sea-deep"
      >
        Back to workspace
      </Link>
    </div>
  );
}
