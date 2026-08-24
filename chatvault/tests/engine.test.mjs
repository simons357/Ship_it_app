import { test } from "node:test";
import assert from "node:assert/strict";
import {
  SCHEMA_VERSION,
  ingestPaste,
  searchEntries,
  exportVault,
  importVault,
  updateEntry,
  reviewLedgerItem,
  createStore,
  DEMO_ENTRIES,
  assertNotAutoProved,
} from "../js/engine.mjs";

test("ingest keeps raw text and will not let a summary replace it", () => {
  const raw = "TITLE: Probe\nCLAIM: 2+2=4\n\nThe identity e^{iπ} + 1 = 0 remains a definitional Euler identity.";
  const entry = ingestPaste(raw, { summary: "A short note." });
  assert.equal(entry.raw_content, raw);
  assert.notEqual(entry.summary, entry.raw_content);
  assert.equal(entry.key_claims.length, 1);
  assert.equal(entry.key_claims[0].status, "UNREVIEWED");
  assert.throws(() => ingestPaste(""));
});

test("ingest never auto-marks PROVED", () => {
  assert.equal(assertNotAutoProved("PROVED", { humanReviewed: false }), "UNREVIEWED");
  assert.equal(assertNotAutoProved("PROVED", { humanReviewed: true }), "PROVED");
});

test("raw_content is immutable after ingest", () => {
  const entry = ingestPaste("hello vault");
  assert.throws(() => updateEntry(entry, { raw_content: "tampered" }));
  const next = updateEntry(entry, { title: "Hello vault" });
  assert.equal(next.raw_content, "hello vault");
  assert.equal(next.title, "Hello vault");
});

test("search supports AND, OR, phrase, and field filters", () => {
  const entries = DEMO_ENTRIES;
  assert.equal(searchEntries(entries, "euler identity").length, 1);
  assert.equal(searchEntries(entries, '"finite-time blow-up"').length, 1);
  assert.ok(searchEntries(entries, "euler OR navier-stokes").length >= 2);
  assert.equal(searchEntries(entries, "claim:definitional").length, 1);
  assert.equal(searchEntries(entries, "theorem:cos").length, 1);
  assert.equal(searchEntries(entries, "gap:blow-up").length, 1);
  assert.equal(searchEntries(entries, "ai:Claude").length, 1);
  assert.equal(searchEntries(entries, "", { visibility: "private" }).length, 1);
  assert.equal(searchEntries(entries, "mnemonic", { visibility: "professional" }).length, 0);
});

test("export round-trips metadata needed to restore a record", () => {
  const bundle = exportVault(DEMO_ENTRIES);
  assert.equal(bundle.format, "chatvault-export");
  assert.equal(bundle.schema_version, SCHEMA_VERSION);
  const restored = importVault(bundle);
  assert.equal(restored.length, DEMO_ENTRIES.length);
  const euler = restored.find((e) => e.title.includes("Euler"));
  assert.ok(euler.raw_content.includes("e^{iπ}"));
  assert.equal(euler.source_ai, "Grok");
  const ns = restored.find((e) => e.title.includes("Navier"));
  assert.equal(ns.key_claims[0].status, "CONJECTURAL");
  const professional = exportVault(DEMO_ENTRIES, { includePrivate: false });
  assert.equal(professional.count, 2);
  assert.ok(professional.entries.every((e) => e.visibility !== "private"));
});

test("store updates local state only after confirmed operations", () => {
  const store = createStore([]);
  const a = store.add(ingestPaste("alpha"));
  assert.equal(store.list().length, 1);
  store.replaceAfterSuccess(a.id, updateEntry(a, { title: "Alpha" }));
  assert.equal(store.get(a.id).title, "Alpha");
  store.deleteConfirmed(a.id);
  assert.equal(store.list().length, 0);
  assert.throws(() => store.deleteConfirmed("missing"));
});

test("human review can set CONJECTURAL; PROVED requires human flag", () => {
  const entry = ingestPaste("TITLE: x\nCLAIM: maybe\n\nbody");
  const claimId = entry.key_claims[0].id;
  const reviewed = reviewLedgerItem(entry, "key_claims", claimId, "CONJECTURAL", { humanReviewed: true });
  assert.equal(reviewed.key_claims[0].status, "CONJECTURAL");
  const proved = reviewLedgerItem(entry, "key_claims", claimId, "PROVED", { humanReviewed: true });
  assert.equal(proved.key_claims[0].status, "PROVED");
  const refused = reviewLedgerItem(entry, "key_claims", claimId, "PROVED", { humanReviewed: false });
  assert.equal(refused.key_claims[0].status, "UNREVIEWED");
});
