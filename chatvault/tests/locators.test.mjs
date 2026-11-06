import { test } from "node:test";
import assert from "node:assert/strict";
import { ingestPaste, attachLocator, searchEntries } from "../js/engine.mjs";
import { classifyLocator, makeLocator, locatorCode } from "../js/locators.mjs";

test("classifyLocator detects url, doi, geo, path, handle", () => {
  assert.equal(classifyLocator("https://example.com/a"), "url");
  assert.equal(classifyLocator("10.5281/zenodo.22050963"), "doi");
  assert.equal(classifyLocator("40.7128, -74.0060"), "geo");
  assert.equal(classifyLocator("/tmp/notes.md"), "path");
  assert.equal(classifyLocator("@primefield"), "handle");
});

test("paste ADDRESS and UI locator both attach; codes are stable", () => {
  const pasted = ingestPaste("TITLE: With doi\nDOI: 10.5281/zenodo.22050963\n\nBody.");
  assert.equal(pasted.locators.length, 1);
  assert.equal(pasted.locators[0].kind, "doi");
  assert.equal(pasted.source_file, "10.5281/zenodo.22050963");
  const extra = makeLocator("https://primefield.tech/note");
  const both = ingestPaste("TITLE: Two\nADDRESS: 40.7, -74.0\n\nBody.", { locators: [extra] });
  assert.equal(both.locators.length, 2);
  assert.equal(locatorCode("https://primefield.tech/note"), extra.code);
});

test("attachLocator adds a second address without touching raw text", () => {
  const entry = ingestPaste("TITLE: Note\n\nRaw stays.");
  const next = attachLocator(entry, "https://example.com/x");
  assert.equal(next.raw_content, entry.raw_content);
  assert.equal(next.locators.length, 1);
  assert.equal(next.locators[0].kind, "url");
});

test("address: search finds DOI and short code", () => {
  const entry = ingestPaste("TITLE: Zenodo\nDOI: 10.5281/zenodo.22050963\n\nBody.");
  const byDoi = searchEntries([entry], "address:10.5281");
  assert.equal(byDoi.length, 1);
  const byCode = searchEntries([entry], `locator:${entry.locators[0].code}`);
  assert.equal(byCode.length, 1);
});
