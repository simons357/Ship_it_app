import { test } from "node:test";
import assert from "node:assert/strict";
import { loadEngine } from "./load.mjs";

const { TraumaPhys } = loadEngine("trauma_physiology.js");

function run(state, seconds, dt, clockRate) {
  let s = { ...state };
  const steps = Math.ceil(seconds / dt);
  for (let i = 0; i < steps; i++) {
    s = TraumaPhys.step(s, dt, clockRate);
    if (s.arrest) return s;
  }
  return s;
}

test("needle relief is temporising and decays back toward tension", () => {
  const start = { ...TraumaPhys.seed(), live: true, relief: TraumaPhys.NEEDLE_RELIEF };
  const later = run(start, 20, 0.05, 1.0);
  assert.ok(later.relief < TraumaPhys.NEEDLE_RELIEF);
  assert.ok(later.relief > 0);
  assert.equal(later.arrest, false);
});

test("a tube (relief 1) holds and does not arrest", () => {
  const start = { ...TraumaPhys.seed(), live: true, relief: TraumaPhys.TUBE_RELIEF };
  const later = run(start, 90, 0.05, 1.45);
  assert.equal(later.relief, 1);
  assert.equal(later.arrest, false);
  assert.ok(later.sbp > 90);
  assert.ok(later.spo2 > 90);
});

test("doing nothing under a live clock eventually voids the case", () => {
  const start = { ...TraumaPhys.seed(), live: true, relief: 0, sbp: 52, spo2: 74 };
  const later = run(start, 50, 0.05, 1.0);
  assert.equal(later.arrest, true);
  assert.ok(later.timeCritical > TraumaPhys.ARREST_AFTER);
});

test("handover envelope opens on high severity", () => {
  const crashing = TraumaPhys.severity({ relief: 0, sbp: 50, arrested: false });
  const holding = TraumaPhys.severity({ relief: 1, sbp: 114, arrested: false });
  assert.ok(crashing > 0.7);
  assert.ok(holding < 0.3);
});

test("give() latches a tube at 1.0 and a needle at 0.55", () => {
  assert.equal(TraumaPhys.give(0, TraumaPhys.NEEDLE_RELIEF), 0.55);
  assert.equal(TraumaPhys.give(0.55, TraumaPhys.TUBE_RELIEF), 1);
});
