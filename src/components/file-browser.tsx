"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import {
  formatRelativeDate,
  getTreeEntries,
} from "@/lib/github/mock-data";
import type { RepoEntry } from "@/lib/github/types";

type FileBrowserProps = {
  owner: string;
  name: string;
  onSelectFile?: (entry: RepoEntry) => void;
  selectedPath?: string;
};

export function FileBrowser({
  owner,
  name,
  onSelectFile,
  selectedPath,
}: FileBrowserProps) {
  const [dirPath, setDirPath] = useState("");
  const entries = useMemo(
    () => getTreeEntries(owner, name, dirPath),
    [owner, name, dirPath],
  );

  const crumbs = dirPath ? dirPath.split("/") : [];

  return (
    <div>
      <div className="flex flex-wrap items-center gap-2 text-sm text-ink-soft">
        <button
          type="button"
          onClick={() => setDirPath("")}
          className="transition-colors hover:text-ink"
        >
          {name}
        </button>
        {crumbs.map((crumb, index) => {
          const nextPath = crumbs.slice(0, index + 1).join("/");
          return (
            <span key={nextPath} className="flex items-center gap-2">
              <span aria-hidden="true">/</span>
              <button
                type="button"
                onClick={() => setDirPath(nextPath)}
                className="transition-colors hover:text-ink"
              >
                {crumb}
              </button>
            </span>
          );
        })}
      </div>

      {entries.length === 0 ? (
        <p className="mt-6 text-sm text-ink-soft">
          This folder is empty in the sample data.
        </p>
      ) : (
        <ul className="mt-4 divide-y divide-line border-y border-line">
          {entries.map((entry) => {
            const isSelected = selectedPath === entry.path;
            if (entry.kind === "dir") {
              return (
                <li key={entry.id}>
                  <button
                    type="button"
                    onClick={() => setDirPath(entry.path)}
                    className="flex w-full items-center justify-between gap-4 py-3.5 text-left transition-colors hover:bg-mist/60"
                  >
                    <span className="font-medium text-ink">
                      {entry.name}/
                    </span>
                    <span className="text-sm text-ink-soft">
                      {formatRelativeDate(entry.updatedAt)}
                    </span>
                  </button>
                </li>
              );
            }

            return (
              <li key={entry.id}>
                <button
                  type="button"
                  onClick={() => onSelectFile?.(entry)}
                  className={`flex w-full items-center justify-between gap-4 py-3.5 text-left transition-colors hover:bg-mist/60 ${
                    isSelected ? "bg-mist/80" : ""
                  }`}
                >
                  <span className="min-w-0">
                    <span className="block truncate font-medium text-ink">
                      {entry.name}
                    </span>
                    <span className="mt-0.5 block text-sm text-ink-soft">
                      {entry.path}
                      {entry.sizeLabel ? ` · ${entry.sizeLabel}` : ""}
                    </span>
                  </span>
                  <span className="shrink-0 text-sm text-ink-soft">
                    {formatRelativeDate(entry.updatedAt)}
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      )}

      <p className="mt-4 text-sm text-ink-soft">
        Prefer reading the guide?{" "}
        <Link href="/help" className="text-sea-deep underline-offset-2 hover:underline">
          Open Help
        </Link>
      </p>
    </div>
  );
}
