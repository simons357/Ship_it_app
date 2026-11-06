import { test } from "node:test";
import assert from "node:assert/strict";
import { DEMO_ENTRIES } from "../js/engine.mjs";
import { ledgerSpectrum } from "../js/spectrum.mjs";

test("spectrum counts ledger rows and does not treat PROVED as truth", () => {
  const spec = ledgerSpectrum(DEMO_ENTRIES);
  assert.ok(spec.total > 0);
  assert.equal(spec.provedShare, 0);
  assert.match(spec.caption, /not a proof/i);
  assert.ok(spec.counts.CONJECTURAL >= 1);
  assert.ok(spec.counts.OPEN >= 1);
});

test("empty vault spectrum is zero, not a failed load", () => {
  const spec = ledgerSpectrum([]);
  assert.equal(spec.total, 0);
  assert.equal(spec.bands.length, 0);
});
