import { test } from "node:test";
import assert from "node:assert/strict";
import {
  emptyMemory,
  loadMemory,
  rememberQuery,
  rememberOpen,
  applySessionContext,
  MEMORY_KEY,
} from "../js/memory.mjs";
import { searchVault, DEMO_ENTRIES } from "../js/engine.mjs";

function memStore() {
  const map = new Map();
  return {
    getItem: (k) => (map.has(k) ? map.get(k) : null),
    setItem: (k, v) => map.set(k, String(v)),
  };
}

test("memory persists queries and last project on this device only", () => {
  const storage = memStore();
  let mem = loadMemory(storage);
  mem = rememberQuery(mem, "gap:blow-up", storage);
  mem = rememberOpen(mem, { id: "ent_1", project_category: "fluids" }, storage);
  const again = loadMemory(storage);
  assert.equal(again.lastQuery, "gap:blow-up");
  assert.equal(again.lastProject, "fluids");
  assert.equal(again.opens[0].id, "ent_1");
  assert.ok(storage.getItem(MEMORY_KEY));
});

test("empty query is not stored", () => {
  const storage = memStore();
  const mem = rememberQuery(emptyMemory(), "  ", storage);
  assert.equal(mem.queries.length, 0);
});

test("session context labels last project and recency without hiding a miss", () => {
  const result = searchVault(DEMO_ENTRIES, "euler identity");
  const nudged = applySessionContext(result, { lastProject: "fluids", lastOpenedId: DEMO_ENTRIES[1].id });
  assert.match(nudged.hits[0].entry.title, /Euler/i);
  assert.match(nudged.context, /project:fluids/);
});
