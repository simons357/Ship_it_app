#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { runBench, formatBenchReport } from "../js/bench.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const lastPath = join(root, "bench", "LAST.json");
let previous = null;
try {
  previous = JSON.parse(readFileSync(lastPath, "utf8"));
} catch {
  previous = null;
}
const summary = runBench();
const report = formatBenchReport(summary, previous);
writeFileSync(join(root, "..", "docs", "chatvault-audit", "WEEKLY-BENCH.md"), `${report}\n`);
writeFileSync(lastPath, `${JSON.stringify(summary, null, 2)}\n`);
process.stdout.write(`${report}\n`);
process.exitCode = summary.pass ? 0 : 1;
