import { test } from "node:test";
import assert from "node:assert/strict";
import { ingestPaste, createStore, searchVault } from "../js/engine.mjs";
import {
  defaultSearchMode,
  deepDiveLinks,
  filedHuntPayload,
  filedSearchPayload,
  parseShareTarget,
  shareIngestOverrides,
  shouldHandleFetchInDaWorker,
  snippetIngestOverrides,
} from "../../domain_architect/static/da-search.mjs";

test("default search mode is here for standalone and for a fresh tab", () => {
  assert.equal(defaultSearchMode({ standalone: true, stored: "open" }), "here");
  assert.equal(defaultSearchMode({ standalone: false, stored: "open" }), "open");
  assert.equal(defaultSearchMode({ standalone: false, stored: "here" }), "here");
  assert.equal(defaultSearchMode({ standalone: false, stored: null }), "here");
  assert.equal(defaultSearchMode({}), "here");
});

test("share target GET is a human snippet, not a ChatGPT dump", () => {
  const empty = parseShareTarget(new URLSearchParams());
  assert.equal(empty.autoIndex, false);
  assert.equal(empty.snippet, "");

  const share = parseShareTarget(
    new URLSearchParams({
      title: "Letter from the field",
      text: "Keep the raw note.",
      url: "https://example.org/note",
    })
  );
  assert.equal(share.autoIndex, true);
  assert.match(share.snippet, /Letter from the field/);
  assert.match(share.snippet, /Keep the raw note/);
  assert.match(share.snippet, /example.org/);

  const entry = ingestPaste(share.snippet, shareIngestOverrides(share));
  assert.equal(entry.origin_class, "human_record");
  assert.equal(entry.source_type, "other");
  assert.equal(entry.source_ai, "human");
  assert.ok(entry.search_tags.includes("share-target"));
  assert.equal(entry.source_type !== "transcript", true);
  assert.equal(
    entry.key_claims.every((c) => c.status !== "PROVED"),
    true
  );
});

test("file this search stores a human stub without a conversation dump", () => {
  assert.throws(() => filedSearchPayload("  "));
  const payload = filedSearchPayload("euler identity");
  const entry = ingestPaste(payload.raw, payload.overrides);
  assert.equal(entry.title, "Search: euler identity");
  assert.equal(entry.origin_class, "human_record");
  assert.equal(entry.source_type, "other");
  assert.ok(entry.search_tags.includes("filed-search"));
  assert.match(entry.raw_content, /euler identity/);
  const store = createStore([entry]);
  const ranked = searchVault(store.list(), "euler identity");
  assert.equal(ranked.hits[0].entry.id, entry.id);
});

test("file this hunt records DDG and scholar URLs, not a crawl", () => {
  const payload = filedHuntPayload("navier stokes");
  assert.match(payload.raw, /duckduckgo\.com/);
  assert.match(payload.raw, /wikipedia\.org/);
  assert.match(payload.raw, /semanticscholar\.org|scholar\.google/);
  assert.match(payload.raw, /does not crawl/i);
  const entry = ingestPaste(payload.raw, payload.overrides);
  assert.equal(entry.title, "Web hunt: navier stokes");
  assert.equal(entry.origin_class, "human_record");
  assert.ok(entry.search_tags.includes("web-hunt"));
});

test("deep dive links open known hunts and do not invent a vault web index", () => {
  const links = deepDiveLinks("spectral regularity");
  const ids = links.map((l) => l.id);
  assert.deepEqual(ids, ["ddg", "wiki", "scholar", "gscholar"]);
  assert.ok(links.every((l) => /^https:\/\//.test(l.href)));
  assert.ok(links[0].href.includes("duckduckgo.com"));
});

test("snippet origin toggle maps AI vs human without auto-PROVE", () => {
  const human = snippetIngestOverrides({ originClass: "human_record", sourceType: "letter" });
  const ai = snippetIngestOverrides({ originClass: "ai_generated", sourceType: "snippet" });
  const letter = ingestPaste("A short letter home.", human);
  const note = ingestPaste("Model said maybe.", ai);
  assert.equal(letter.origin_class, "human_record");
  assert.equal(letter.source_type, "letter");
  assert.equal(note.origin_class, "ai_generated");
  assert.equal(note.source_type, "other");
  assert.equal(note.source_ai, "unknown");
  assert.equal(
    [...letter.key_claims, ...note.key_claims].every((c) => c.status !== "PROVED"),
    true
  );
});

test("DA service worker skips POST, APIs, and nested ChatVault", () => {
  assert.equal(shouldHandleFetchInDaWorker("POST", "/api/audit"), false);
  assert.equal(shouldHandleFetchInDaWorker("POST", "/api/inquiry"), false);
  assert.equal(shouldHandleFetchInDaWorker("POST", "/api/drain/queue"), false);
  assert.equal(shouldHandleFetchInDaWorker("GET", "/chatvault/js/engine.mjs"), false);
  assert.equal(shouldHandleFetchInDaWorker("GET", "/api/drain/health"), false);
  assert.equal(shouldHandleFetchInDaWorker("GET", "/"), true);
  assert.equal(shouldHandleFetchInDaWorker("GET", "/da-home.js"), true);
});
