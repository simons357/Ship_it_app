#!/usr/bin/env node
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { runBench, formatBenchReport } from "../js/bench.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const summary = runBench();
const report = formatBenchReport(summary);
writeFileSync(join(root, "..", "docs", "chatvault-audit", "WEEKLY-BENCH.md"), `${report}\n`);
writeFileSync(join(root, "bench", "LAST.json"), `${JSON.stringify(summary, null, 2)}\n`);
process.stdout.write(`${report}\n`);
process.exitCode = summary.pass ? 0 : 1;
