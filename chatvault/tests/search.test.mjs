import { test } from "node:test";
import assert from "node:assert/strict";
import { ingestPaste, DEMO_ENTRIES } from "../js/engine.mjs";
import { SEARCH_ENGINE_VERSION, searchVault, searchEntries } from "../js/search.mjs";

function ids(hits) {
  return hits.map((h) => h.entry.id);
}

test("search engine version is hybrid, not a boolean filter", () => {
  assert.equal(SEARCH_ENGINE_VERSION, "chatvault-hybrid-0.2.0");
  const result = searchVault(DEMO_ENTRIES, "euler identity");
  assert.equal(result.engine, SEARCH_ENGINE_VERSION);
  assert.ok(result.hits[0].score > 0);
  assert.ok(result.hits[0].snippets.length >= 1);
  assert.ok(
    result.hits[0].matched_fields.includes("title") ||
      result.hits[0].matched_fields.includes("content")
  );
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
});

test("fielded claim: and gap: do not leak into other fields", () => {
  const claims = searchEntries(DEMO_ENTRIES, "claim:definitional");
  assert.equal(claims.length, 1);
  assert.match(claims[0].title, /Euler/i);
  const gaps = searchEntries(DEMO_ENTRIES, "gap:blow-up");
  assert.equal(gaps.length, 1);
  assert.match(gaps[0].title, /Navier/i);
  const party = ingestPaste("TITLE: Birthday blow-up plans\n\nParty blow-up balloons.");
  assert.equal(searchEntries([party, ...DEMO_ENTRIES], "gap:blow-up").length, 1);
});

test("claim snippet carries ledger status", () => {
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
});
