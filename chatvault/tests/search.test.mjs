import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { ingestPaste, reviewLedgerItem, DEMO_ENTRIES } from "../js/engine.mjs";
import {
  SEARCH_ENGINE_VERSION,
  RANK_FIELDS,
  SEARCH_FIELDS,
  searchEntries,
  searchVault,
  buildIndex,
  parseQuery,
  bestWindow,
  ndcgAt,
  mrr,
  stem,
  editDistanceAtMost,
  reciprocalRankFusion,
} from "../js/search.mjs";

function ids(hits) {
  return hits.map((h) => h.entry.id);
}

test("search engine version is hybrid, not a boolean filter", () => {
  assert.equal(SEARCH_ENGINE_VERSION, "chatvault-hybrid-0.2.0");
  assert.match(SEARCH_ENGINE_VERSION, /hybrid/i);
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

test("one-edit typos and stems still retrieve the intended record", () => {
  assert.equal(stem("limiters"), stem("limiter"));
  assert.equal(editDistanceAtMost("eulr", "euler", 1), true);
  assert.equal(editDistanceAtMost("euler", "navier", 1), false);
  const titleHit = ingestPaste(
    ["TITLE: Euler identity as a definitional fact", "SOURCE_AI: Grok", "", "Short body."].join("\n")
  );
  const limiter = ingestPaste(
    ["TITLE: Token bucket rate limiter notes", "", "Implement the rate limiter."].join("\n")
  );
  const typo = searchVault([limiter, titleHit], "eulr identity");
  assert.equal(typo.hits[0].entry.id, titleHit.id);
  const stemmed = searchVault([titleHit, limiter], "rate limiters");
  assert.equal(stemmed.hits[0].entry.id, limiter.id);
});

test("OPEN can outrank PROVED; harmonic_note is never a score", () => {
  const openGap = ingestPaste(
    [
      "TITLE: Spectral bound still missing",
      "GAP: A complete a-priori bound preventing finite-time blow-up is missing.",
      "",
      "The spectral bound is the open problem in this note.",
    ].join("\n")
  );
  let provedWeak = ingestPaste(
    [
      "TITLE: Unrelated logistics",
      "CLAIM: Token bucket exists.",
      "",
      "No spectral discussion. A hallway mention of a bound.",
    ].join("\n")
  );
  provedWeak = reviewLedgerItem(
    provedWeak,
    "key_claims",
    provedWeak.key_claims[0].id,
    "PROVED",
    { humanReviewed: true }
  );
  provedWeak.harmonic_note = "echoes the spectral bound thread across the whole vault";
  const ranked = searchVault([provedWeak, openGap], "spectral bound");
  assert.equal(ranked.hits[0].entry.id, openGap.id);
  assert.equal(provedWeak.key_claims[0].status, "PROVED");
  assert.equal(openGap.open_gaps[0].status, "OPEN");

  const withNote = searchVault(
    [{ ...openGap, harmonic_note: "one-line cross-conversation pattern about spectral bound resonance" }],
    "spectral bound"
  );
  const withoutNote = searchVault([{ ...openGap, harmonic_note: "" }], "spectral bound");
  assert.equal(withNote.hits[0].score, withoutNote.hits[0].score);
  assert.equal(withNote.hits[0].matched_fields.includes("status"), false);
});

test("status: remains a field query and is not an unfielded quality boost", () => {
  const openOnly = ingestPaste("TITLE: Open gap card\nGAP: finite-time blow-up bound is missing.\n\nRaw.");
  const draft = ingestPaste("TITLE: Reviewed claim card\nCLAIM: Token bucket exists.\n\nRaw.");
  const provedOnly = reviewLedgerItem(
    draft,
    "key_claims",
    draft.key_claims[0].id,
    "PROVED",
    { humanReviewed: true }
  );
  const fielded = searchVault([openOnly, provedOnly], "status:OPEN");
  assert.equal(fielded.total, 1);
  assert.equal(fielded.hits[0].entry.id, openOnly.id);
});

test("RRF prefers documents that win more than one list", () => {
  const scores = reciprocalRankFusion(
    [
      ["a", "b"],
      ["a", "c"],
      ["b", "a"],
    ],
    60
  );
  assert.ok(scores.get("a") > scores.get("b"));
  assert.ok(scores.get("a") > scores.get("c"));
});

test("origin:ai and origin:human filter; unfielded ai does not rank-boost every AI chat", () => {
  const grokChat = ingestPaste("TITLE: Token bucket notes\n\nDesign a limiter with a bucket.", {
    source_ai: "Grok",
  });
  const claudeChat = ingestPaste("TITLE: Cooking caramel\n\nHow to brown onions slowly.", {
    source_ai: "Claude",
  });
  const letter = ingestPaste("TITLE: Handwritten letter to a colleague\n\nDear colleague, about fluids on Tuesday.", {
    source_ai: "human",
    source_type: "letter",
  });
  assert.equal(grokChat.origin_class, "ai_generated");
  assert.equal(claudeChat.origin_class, "ai_generated");
  assert.equal(letter.origin_class, "human_record");

  const parsedAi = parseQuery("origin:ai");
  assert.equal(parsedAi.terms[0].field, "origin");
  assert.equal(parsedAi.terms[0].term, "ai_generated");
  const parsedHuman = parseQuery("origin:human");
  assert.equal(parsedHuman.terms[0].term, "human_record");

  const corpus = [grokChat, claudeChat, letter];
  const aiHits = searchEntries(corpus, "origin:ai");
  assert.equal(aiHits.length, 2);
  assert.ok(aiHits.every((e) => e.origin_class === "ai_generated"));
  const humanHits = searchEntries(corpus, "origin:human");
  assert.equal(humanHits.length, 1);
  assert.equal(humanHits[0].id, letter.id);

  const uiFilter = searchEntries(corpus, "", { origin_class: "human_record" });
  assert.equal(uiFilter.length, 1);
  assert.equal(uiFilter[0].id, letter.id);

  const unfielded = searchVault(corpus, "ai");
  const unfieldedIds = unfielded.hits.map((h) => h.entry.id);
  assert.equal(unfieldedIds.includes(grokChat.id), false);
  assert.equal(unfieldedIds.includes(claudeChat.id), false);
  assert.equal(unfieldedIds.includes(letter.id), false);
});

test("origin and status are searchable fields but not RANK_FIELDS", () => {
  assert.equal("origin" in SEARCH_FIELDS, true);
  assert.equal("status" in SEARCH_FIELDS, true);
  assert.equal("origin" in RANK_FIELDS, false);
  assert.equal("status" in RANK_FIELDS, false);
  assert.equal("title" in RANK_FIELDS, true);
  assert.equal("content" in RANK_FIELDS, true);
});

test("search.mjs is a standalone ranker: no DOM, no localStorage, no engine import", () => {
  const root = join(dirname(fileURLToPath(import.meta.url)), "..");
  const src = readFileSync(join(root, "js/search.mjs"), "utf8");
  const api = readFileSync(join(root, "js/ENGINE.md"), "utf8");
  assert.doesNotMatch(src, /\blocalStorage\b/);
  assert.doesNotMatch(src, /\bdocument\./);
  assert.doesNotMatch(src, /\bwindow\./);
  assert.doesNotMatch(src, /from\s+["']\.\/engine\.mjs["']/);
  assert.match(src, /export function searchVault/);
  assert.doesNotMatch(src, /export function rankedSearch/);
  assert.match(api, /chatvault-hybrid-0\.2\.0/);
  assert.match(api, /import \{/);
  assert.match(api, /What you do not get/);
});
