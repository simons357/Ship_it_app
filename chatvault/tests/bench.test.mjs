import { test } from "node:test";
import assert from "node:assert/strict";
import { runBench, BASELINE, BENCH_CASES } from "../js/bench.mjs";
import { applySessionContext } from "../js/memory.mjs";
import { searchVault, DEMO_ENTRIES } from "../js/engine.mjs";

test("frozen fixture bench meets baseline floors", () => {
  const summary = runBench();
  assert.equal(summary.cases, BENCH_CASES.length);
  assert.ok(summary.pass, `bench failed: ${JSON.stringify(summary.rows.filter((r) => !r.hit))}`);
  assert.ok(summary.mean_ndcg5 >= BASELINE.mean_ndcg5);
  assert.ok(summary.mean_mrr >= BASELINE.mean_mrr);
  assert.ok(summary.mean_took_ms <= BASELINE.mean_took_ms_max);
});

test("session memory may boost same project but must not invert the blow-up phrase gate", () => {
  const vanilla = searchVault(DEMO_ENTRIES, '"finite-time blow-up"');
  const nudged = applySessionContext(vanilla, { lastProject: "product" });
  assert.match(vanilla.hits[0].entry.title, /Navier/i);
  assert.match(nudged.hits[0].entry.title, /Navier/i);
});
