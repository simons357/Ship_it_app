import { test } from "node:test";
import assert from "node:assert/strict";
import { exportVault, importVault, DEMO_ENTRIES } from "../js/engine.mjs";
import {
  LS_KEY,
  BENCH_HISTORY_KEY,
  savePersistent,
  loadPersistent,
  clearPersistent,
  appendBenchHistory,
  loadBenchHistory,
} from "../js/persist.mjs";

function memStore() {
  const map = new Map();
  return {
    getItem: (k) => (map.has(k) ? map.get(k) : null),
    setItem: (k, v) => map.set(k, String(v)),
    removeItem: (k) => map.delete(k),
  };
}

test("vault export round-trips through localStorage when IndexedDB is absent", async () => {
  const ls = memStore();
  const payload = exportVault(DEMO_ENTRIES);
  const wrote = await savePersistent(payload, ls);
  assert.equal(wrote.localStorage, true);
  assert.ok(ls.getItem(LS_KEY));
  const restored = await loadPersistent(importVault, ls);
  assert.equal(restored.length, DEMO_ENTRIES.length);
  assert.ok(restored.find((e) => /Euler/i.test(e.title)));
});

test("clearPersistent drops the localStorage vault key", async () => {
  const ls = memStore();
  await savePersistent(exportVault(DEMO_ENTRIES), ls);
  await clearPersistent(ls);
  assert.equal(ls.getItem(LS_KEY), null);
  const restored = await loadPersistent(importVault, ls);
  assert.equal(restored, null);
});

test("bench history keeps the newest run first", () => {
  const ls = memStore();
  const first = appendBenchHistory({ at: "2026-01-01T00:00:00.000Z", pass: true, mean_ndcg5: 1, mean_mrr: 1, mean_took_ms: 2, engine: "x" }, ls);
  const second = appendBenchHistory({ at: "2026-01-08T00:00:00.000Z", pass: true, mean_ndcg5: 1, mean_mrr: 1, mean_took_ms: 3, engine: "x" }, ls);
  assert.equal(second[0].at, "2026-01-08T00:00:00.000Z");
  assert.equal(second[1].at, first[0].at);
  assert.ok(ls.getItem(BENCH_HISTORY_KEY));
  assert.equal(loadBenchHistory(ls).length, 2);
});
