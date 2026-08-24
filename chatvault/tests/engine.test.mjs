import { test } from "node:test";
import assert from "node:assert/strict";
import {
  SCHEMA_VERSION,
  ingestPaste,
  ingestBulk,
  ingestTextFile,
  searchEntries,
  exportVault,
  importVault,
  updateEntry,
  reviewLedgerItem,
  createStore,
  DEMO_ENTRIES,
  assertNotAutoProved,
  emptyEntry,
  listTags,
  listBooks,
  listArtifacts,
  vaultStats,
  safeId,
  statusClass,
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
  assert.equal(searchEntries(entries, "", { book: "Research & Ideas" }).length, 2);
  assert.equal(searchEntries(entries, "", { tag: "teaching" }).length, 1);
  assert.equal(searchEntries(entries, "", { starred: true }).length, 1);
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
  assert.ok(euler.related_projects.includes("Research & Ideas"));
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
  store.addMany([ingestPaste("beta"), ingestPaste("gamma")]);
  assert.equal(store.list().length, 3);
  store.deleteConfirmed(a.id);
  assert.equal(store.list().length, 2);
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

test("import sanitizes ledger ids and never keeps auto-PROVED gaps or stale human_reviewed", () => {
  const poisoned = {
    format: "chatvault-export",
    schema_version: SCHEMA_VERSION,
    entries: [
      {
        id: `ent_" onclick="alert(1)`,
        title: "x",
        raw_content: "hello",
        open_gaps: [
          {
            id: `lg_" onclick="alert(1)`,
            text: "gap",
            status: "PROVED",
            human_reviewed: false,
          },
        ],
        key_claims: [
          {
            id: "ok_claim",
            text: "c",
            status: "PROVED",
            human_reviewed: false,
          },
        ],
        theorems: [
          {
            id: "thm_1",
            text: "t",
            status: "not-a-status",
            human_reviewed: true,
          },
        ],
      },
    ],
  };
  const [entry] = importVault(poisoned);
  assert.equal(entry.open_gaps[0].status, "UNREVIEWED");
  assert.equal(entry.open_gaps[0].human_reviewed, false);
  assert.equal(entry.key_claims[0].status, "UNREVIEWED");
  assert.equal(entry.key_claims[0].human_reviewed, false);
  assert.equal(entry.theorems[0].status, "UNREVIEWED");
  assert.match(entry.id, /^[A-Za-z0-9._-]+$/);
  assert.match(entry.open_gaps[0].id, /^[A-Za-z0-9._-]+$/);
  assert.equal(statusClass(entry.open_gaps[0].status), "unreviewed");
  assert.equal(statusClass(`PROVED"><img`), "unreviewed");
  assert.ok(safeId(`lg_" onclick="alert(1)`).match(/^[A-Za-z0-9._-]+$/));
});

test("emptyEntry does not spread hostile extra keys onto ledger rows", () => {
  const entry = emptyEntry({
    raw_content: "body",
    key_claims: [{ text: "c", status: "OPEN", onclick: "alert(1)", extra: "nope" }],
  });
  assert.equal(entry.key_claims[0].status, "OPEN");
  assert.equal(entry.key_claims[0].onclick, undefined);
  assert.equal(entry.key_claims[0].extra, undefined);
});

test("form defaults do not clobber SOURCE_AI structured lines", () => {
  const entry = ingestPaste(
    "TITLE: Probe\nSOURCE_AI: Grok\n\nbody of the probe",
    { source_ai: "unknown", visibility: "professional" }
  );
  assert.equal(entry.source_ai, "Grok");
  assert.equal(entry.visibility, "professional");
  const forced = ingestPaste("TITLE: Probe\nSOURCE_AI: Grok\n\nbody", { source_ai: "Claude" });
  assert.equal(forced.source_ai, "Claude");
});

test("bulk ingest splits on --- and keeps each raw chunk", () => {
  const raw = "TITLE: One\n\nfirst body\n---\nTITLE: Two\nCLAIM: split works\n\nsecond body";
  const { entries, errors } = ingestBulk(raw);
  assert.equal(entries.length, 2);
  assert.equal(errors.length, 0);
  assert.equal(entries[0].title, "One");
  assert.equal(entries[1].title, "Two");
  assert.ok(entries[0].raw_content.includes("first body"));
  assert.ok(entries[1].raw_content.includes("second body"));
  assert.throws(() => ingestBulk("   \n---\n   "));
});

test("text file ingest indexes raw bytes and restores ChatVault JSON bundles", () => {
  const note = ingestTextFile("notes.md", "TITLE: File note\n\nmarkdown body");
  assert.equal(note.kind, "entry");
  assert.equal(note.entries[0].source_file, "notes.md");
  assert.equal(note.entries[0].source_type, "markdown");
  assert.equal(note.entries[0].raw_content.includes("markdown body"), true);
  const bundle = exportVault(DEMO_ENTRIES);
  const restored = ingestTextFile("vault.json", JSON.stringify(bundle));
  assert.equal(restored.kind, "bundle");
  assert.equal(restored.entries.length, DEMO_ENTRIES.length);
  assert.throws(() => ingestTextFile("photo.png", "nope"));
});

test("tags, books, artifacts, and dashboard stats are derived without an LLM", () => {
  const tags = listTags(DEMO_ENTRIES);
  assert.ok(tags.find((t) => t.tag === "euler" && t.count === 1));
  const books = listBooks(DEMO_ENTRIES);
  assert.ok(books.find((b) => b.name === "Research & Ideas" && b.count === 2));
  const artifacts = listArtifacts(DEMO_ENTRIES);
  assert.ok(artifacts.some((a) => a.kind === "claim"));
  assert.ok(artifacts.some((a) => a.kind === "gap"));
  assert.ok(artifacts.some((a) => a.kind === "action"));
  const stats = vaultStats(DEMO_ENTRIES);
  assert.equal(stats.total, 3);
  assert.equal(stats.starred, 1);
  assert.equal(stats.private, 1);
  assert.equal(stats.books, 2);
  assert.ok(stats.claims >= 2);
});
