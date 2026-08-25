import { test } from "node:test";
import assert from "node:assert/strict";
import { ingestPaste, DEMO_ENTRIES } from "../js/engine.mjs";
import {
  SEARCH_ENGINE_VERSION,
  searchEntries,
  searchVault,
  buildIndex,
  parseQuery,
  bestWindow,
  ndcgAt,
  mrr,
} from "../js/search.mjs";

function ids(hits) {
  return hits.map((h) => h.entry.id);
}

test("search engine version is BM25F, not a boolean filter", () => {
  assert.match(SEARCH_ENGINE_VERSION, /bm25f/i);
  const result = searchVault(DEMO_ENTRIES, "euler identity");
  assert.equal(result.engine, SEARCH_ENGINE_VERSION);
  assert.ok(result.hits[0].score > 0);
  assert.ok(result.hits[0].snippets.length >= 1);
  assert.ok(result.hits[0].matched_fields.includes("title") || result.hits[0].matched_fields.includes("content"));
});

test("title match outranks a later body-only mention of the same token", () => {
  const titleHit = ingestPaste(
    ["TITLE: Euler identity as a definitional fact", "SOURCE_AI: Grok", "", "Short body."].join("\n")
  );
  const bodyHit = ingestPaste(
    [
      "TITLE: Weekly lab logistics",
      "SOURCE_AI: ChatGPT",
      "",
      "Someone mentioned Euler in passing while booking the seminar room. No identity was discussed.",
    ].join("\n")
  );
  const decoy = ingestPaste("TITLE: Token bucket notes\n\nImplement the rate limiter.");
  const ranked = searchVault([bodyHit, decoy, titleHit], "euler identity");
  assert.equal(ranked.hits[0].entry.id, titleHit.id);
  assert.ok(ranked.hits[0].score > ranked.hits[1].score);
  assert.ok(ids(ranked.hits).includes(bodyHit.id));
  assert.equal(ids(ranked.hits).includes(decoy.id), false);
});

test("phrase query is a hard gate and still ranks", () => {
  const ns = ingestPaste(
    [
      "TITLE: Spectral regularity for Navier–Stokes",
      "GAP: A complete a-priori bound preventing finite-time blow-up is missing.",
      "",
      "Conditional note only.",
    ].join("\n")
  );
  const party = ingestPaste("TITLE: Birthday blow-up plans\n\nParty blow-up balloons.");
  const hits = searchVault([party, ns], '"finite-time blow-up"');
  assert.equal(hits.total, 1);
  assert.equal(hits.hits[0].entry.id, ns.id);
  assert.ok(hits.hits[0].snippets.some((s) => /finite-time blow-up/i.test(s.text)));
});

test("fielded claim: and gap: do not leak into other fields", () => {
  const entries = DEMO_ENTRIES;
  const claims = searchEntries(entries, "claim:definitional");
  assert.equal(claims.length, 1);
  assert.match(claims[0].title, /Euler/i);
  const gaps = searchEntries(entries, "gap:blow-up");
  assert.equal(gaps.length, 1);
  assert.match(gaps[0].title, /Navier/i);
  const party = ingestPaste("TITLE: Birthday blow-up plans\n\nParty blow-up balloons.");
  assert.equal(searchEntries([party, ...entries], "gap:blow-up").length, 1);
});

test("claim snippet carries ledger status and never hides OPEN", () => {
  const entry = ingestPaste(
    [
      "TITLE: Open regularity note",
      "CLAIM: Global regularity is not established in this vault.",
      "GAP: finite-time blow-up bound is missing.",
      "",
      "Raw note stays raw.",
    ].join("\n")
  );
  const result = searchVault([entry], "gap:blow-up");
  const gapSnippet = result.hits[0].snippets.find((s) => s.field === "gap");
  assert.ok(gapSnippet);
  assert.equal(gapSnippet.ledger_status, "OPEN");
  assert.ok(gapSnippet.marks.length >= 1);
});

test("filters still apply after ranking", () => {
  assert.equal(searchEntries(DEMO_ENTRIES, "mnemonic", { visibility: "professional" }).length, 0);
  assert.equal(searchEntries(DEMO_ENTRIES, "", { visibility: "private" }).length, 1);
  assert.equal(searchEntries(DEMO_ENTRIES, "", { book: "Research & Ideas" }).length, 2);
});

test("empty query preserves store order and scores zero", () => {
  const result = searchVault(DEMO_ENTRIES, "");
  assert.deepEqual(
    result.hits.map((h) => h.entry.id),
    DEMO_ENTRIES.map((e) => e.id)
  );
  assert.ok(result.hits.every((h) => h.score === 0));
  assert.ok(result.hits.every((h) => h.snippets.length === 0));
});

test("bestWindow highlights the densest match cluster", () => {
  const text = "aaaa " + "x".repeat(80) + " euler identity euler " + "y".repeat(80);
  const win = bestWindow(text, ["euler", "identity"], 40);
  assert.match(win.text, /euler/i);
  assert.ok(win.marks.length >= 1);
});

test("parseQuery keeps field aliases and OR clauses", () => {
  const parsed = parseQuery('claims:"definitional identity" OR gap:blow-up');
  assert.equal(parsed.mode, "or");
  assert.equal(parsed.clauses[0].phrases[0].field, "claim");
  assert.equal(parsed.clauses[1].terms[0].field, "gap");
});

test("inverted index documents every indexed term", () => {
  const index = buildIndex(DEMO_ENTRIES);
  assert.equal(index.N, DEMO_ENTRIES.length);
  assert.ok(index.df.get("euler") >= 1);
  assert.ok(index.avgLen.content > 0);
});

test("nDCG and MRR helpers match textbook values", () => {
  const grades = { a: 3, b: 2, c: 0 };
  assert.equal(ndcgAt(["a", "b", "c"], grades, 3), 1);
  assert.ok(ndcgAt(["c", "b", "a"], grades, 3) < 1);
  assert.equal(mrr(["c", "a"], { a: 3 }), 0.5);
});
