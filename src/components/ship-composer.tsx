"use client";

import { startTransition, useState, type FormEvent } from "react";
import type { RecentShip, RepoEntry, ShipAction } from "@/lib/github/types";
import { actionLabel } from "@/lib/github/mock-data";

type ShipComposerProps = {
  owner: string;
  name: string;
  branch: string;
  selectedFile?: RepoEntry | null;
  onShipped?: (ship: RecentShip) => void;
};

const actions: { id: ShipAction; label: string }[] = [
  { id: "add", label: "Add" },
  { id: "update", label: "Update" },
  { id: "delete", label: "Delete" },
];

function makeSha() {
  return Math.random().toString(16).slice(2, 9);
}

export function ShipComposer({
  owner,
  name,
  branch,
  selectedFile,
  onShipped,
}: ShipComposerProps) {
  const [action, setAction] = useState<ShipAction>("add");
  const [path, setPath] = useState("");
  const [fileName, setFileName] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<"idle" | "shipping" | "done">("idle");
  const [lastShip, setLastShip] = useState<RecentShip | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Keep path in sync when the user picks a file from the browser
  const effectivePath =
    action !== "add" && selectedFile && !path ? selectedFile.path : path;

  function applySelectedFile() {
    if (!selectedFile) return;
    startTransition(() => {
      setAction("update");
      setPath(selectedFile.path);
      setFileName(selectedFile.name);
      setError(null);
      setStatus("idle");
    });
  }

  async function handleShip(event: FormEvent) {
    event.preventDefault();
    setError(null);

    const targetPath = effectivePath.trim();
    if (!targetPath) {
      setError("Choose a path in the repository.");
      return;
    }
    if ((action === "add" || action === "update") && !fileName && !selectedFile) {
      setError("Pick a file from your device to ship.");
      return;
    }
    if (!message.trim()) {
      setError("Add a short commit message.");
      return;
    }

    setStatus("shipping");
    await new Promise((resolve) => setTimeout(resolve, 700));

    const ship: RecentShip = {
      id: `local-${Date.now()}`,
      action,
      path: targetPath,
      message: message.trim(),
      sha: makeSha(),
      createdAt: new Date().toISOString(),
    };

    setLastShip(ship);
    setStatus("done");
    onShipped?.(ship);
  }

  function resetForm() {
    setPath("");
    setFileName("");
    setMessage("");
    setStatus("idle");
    setLastShip(null);
    setError(null);
  }

  return (
    <section className="border-t border-line pt-8 lg:border-t-0 lg:border-l lg:pl-10 lg:pt-0">
      <header className="mb-6">
        <h2 className="font-[family-name:var(--font-display)] text-xl font-semibold text-ink">
          Ship a change
        </h2>
        <p className="mt-1 text-sm text-ink-soft">
          {owner}/{name} · branch{" "}
          <span className="font-mono text-ink">{branch}</span>
        </p>
      </header>

      {selectedFile ? (
        <button
          type="button"
          onClick={applySelectedFile}
          className="mb-5 w-full border border-line px-4 py-3 text-left text-sm transition-colors hover:border-sea hover:bg-mist/50"
        >
          <span className="block text-ink-soft">Selected from browser</span>
          <span className="mt-1 block font-medium text-ink">
            {selectedFile.path}
          </span>
          <span className="mt-1 block text-sea-deep">Use for update / delete</span>
        </button>
      ) : null}

      <div
        className="mb-6 flex gap-2"
        role="tablist"
        aria-label="Ship action"
      >
        {actions.map((item) => {
          const active = action === item.id;
          return (
            <button
              key={item.id}
              type="button"
              role="tab"
              aria-selected={active}
              onClick={() => {
                setAction(item.id);
                setStatus("idle");
                setError(null);
              }}
              className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                active
                  ? "bg-sea text-foam"
                  : "bg-mist text-ink-soft hover:text-ink"
              }`}
            >
              {item.label}
            </button>
          );
        })}
      </div>

      {status === "done" && lastShip ? (
        <div className="ship-confirm border border-sea/30 bg-mist/70 px-5 py-5">
          <p className="font-mono text-xs uppercase tracking-[0.18em] text-sea-deep">
            Shipped (demo)
          </p>
          <p className="mt-3 font-[family-name:var(--font-display)] text-lg font-semibold text-ink">
            {actionLabel(lastShip.action)} {lastShip.path}
          </p>
          <p className="mt-2 text-sm text-ink-soft">{lastShip.message}</p>
          <p className="mt-4 font-mono text-sm text-ink">
            commit {lastShip.sha}
          </p>
          <button
            type="button"
            onClick={resetForm}
            className="mt-6 rounded-md bg-ink px-4 py-2 text-sm font-medium text-foam transition-colors hover:bg-ink-soft"
          >
            Ship another
          </button>
        </div>
      ) : (
        <form onSubmit={handleShip} className="space-y-5">
          <label className="block">
            <span className="text-sm font-medium text-ink">Path in repo</span>
            <input
              value={effectivePath}
              onChange={(event) => setPath(event.target.value)}
              placeholder={
                action === "add"
                  ? "assets/new-wallpaper.png"
                  : "path/to/existing-file.md"
              }
              className="mt-2 w-full rounded-md border border-line bg-foam px-3 py-2.5 text-ink outline-none transition-shadow focus:border-sea focus:ring-2 focus:ring-sea/20"
            />
          </label>

          {action !== "delete" ? (
            <label className="block">
              <span className="text-sm font-medium text-ink">
                File from your device
              </span>
              <input
                type="file"
                onChange={(event) => {
                  const file = event.target.files?.[0];
                  setFileName(file?.name ?? "");
                  if (file && action === "add" && !path) {
                    setPath(file.name);
                  }
                }}
                className="mt-2 block w-full text-sm text-ink-soft file:mr-4 file:rounded-md file:border-0 file:bg-sea file:px-4 file:py-2 file:text-sm file:font-medium file:text-foam hover:file:bg-sea-deep"
              />
              {fileName ? (
                <span className="mt-2 block text-sm text-ink-soft">
                  Ready: {fileName}
                </span>
              ) : null}
            </label>
          ) : null}

          <label className="block">
            <span className="text-sm font-medium text-ink">Commit message</span>
            <input
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              placeholder={
                action === "add"
                  ? "Add product wallpaper assets"
                  : action === "update"
                    ? "Fix icons for App Store listing"
                    : "Remove unused icon"
              }
              className="mt-2 w-full rounded-md border border-line bg-foam px-3 py-2.5 text-ink outline-none transition-shadow focus:border-sea focus:ring-2 focus:ring-sea/20"
            />
          </label>

          {error ? (
            <p className="text-sm text-signal" role="alert">
              {error}
            </p>
          ) : (
            <p className="text-sm text-ink-soft">
              Demo ships stay on this device. Live GitHub commits arrive after
              OAuth is connected.
            </p>
          )}

          <button
            type="submit"
            disabled={status === "shipping"}
            className="w-full rounded-md bg-sea px-5 py-3 text-base font-semibold text-foam transition-transform transition-colors hover:bg-sea-deep hover:scale-[1.01] active:scale-[0.99] disabled:cursor-wait disabled:opacity-70"
          >
            {status === "shipping" ? "Shipping…" : "Ship"}
          </button>
        </form>
      )}
    </section>
  );
}
