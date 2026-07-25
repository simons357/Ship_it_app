"use client";

import { useState } from "react";
import { FileBrowser } from "@/components/file-browser";
import { ShipComposer } from "@/components/ship-composer";
import {
  actionLabel,
  formatRelativeDate,
  mockRecentShips,
} from "@/lib/github/mock-data";
import type { RecentShip, RepoEntry, Repository } from "@/lib/github/types";

export function RepoWorkspace({ repo }: { repo: Repository }) {
  const fullName = `${repo.owner}/${repo.name}`;
  const [selectedFile, setSelectedFile] = useState<RepoEntry | null>(null);
  const [ships, setShips] = useState<RecentShip[]>(
    () => mockRecentShips[fullName] ?? [],
  );

  return (
    <div className="grid gap-12 lg:grid-cols-[minmax(0,1.1fr)_minmax(280px,0.9fr)] lg:gap-0">
      <div className="min-w-0 lg:pr-10">
        <section>
          <h2 className="font-[family-name:var(--font-display)] text-xl font-semibold text-ink">
            Files
          </h2>
          <p className="mt-1 text-sm text-ink-soft">
            Browse the sample tree, then ship an add, update, or delete.
          </p>
          <div className="mt-6">
            <FileBrowser
              owner={repo.owner}
              name={repo.name}
              selectedPath={selectedFile?.path}
              onSelectFile={setSelectedFile}
            />
          </div>
        </section>

        <section className="mt-12">
          <h2 className="font-[family-name:var(--font-display)] text-xl font-semibold text-ink">
            Recent ships
          </h2>
          <p className="mt-1 text-sm text-ink-soft">
            Local demo history for this repository.
          </p>
          {ships.length === 0 ? (
            <p className="mt-6 text-sm text-ink-soft">
              Nothing shipped yet — send the first change from the panel.
            </p>
          ) : (
            <ul className="mt-6 divide-y divide-line border-y border-line">
              {ships.map((ship) => (
                <li
                  key={ship.id}
                  className="flex flex-col gap-1 py-4 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div>
                    <p className="font-medium text-ink">
                      {actionLabel(ship.action)}{" "}
                      <span className="font-normal text-ink-soft">
                        {ship.path}
                      </span>
                    </p>
                    <p className="mt-1 text-sm text-ink-soft">{ship.message}</p>
                  </div>
                  <div className="flex shrink-0 gap-3 text-sm text-ink-soft">
                    <span className="font-mono">{ship.sha}</span>
                    <span>{formatRelativeDate(ship.createdAt)}</span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>

      <ShipComposer
        owner={repo.owner}
        name={repo.name}
        branch={repo.defaultBranch}
        selectedFile={selectedFile}
        onShipped={(ship) => setShips((current) => [ship, ...current])}
      />
    </div>
  );
}
