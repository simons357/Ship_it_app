import Link from "next/link";

export function DemoBanner() {
  return (
    <div className="border-b border-line bg-mist/80 px-6 py-3 text-sm text-ink-soft sm:px-10">
      <p className="mx-auto max-w-5xl">
        Demo mode — browsing sample repos and shipping changes locally.{" "}
        <Link href="/help#connect-github" className="text-sea-deep underline-offset-2 hover:underline">
          Connect GitHub
        </Link>{" "}
        when you are ready for live commits.
      </p>
    </div>
  );
}
