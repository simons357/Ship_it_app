import { test } from "node:test";
import assert from "node:assert/strict";
import { loadEngine } from "./load.mjs";

const { AISS } = loadEngine("ai-surgeon-systems.js");

test("AISS attaches and keeps derived-band-only retention", () => {
  assert.equal(AISS.RETENTION, "derived-band-only");
  assert.ok(AISS.Profile);
  assert.ok(AISS.Handover);
  assert.ok(AISS.Ask);
  assert.ok(AISS.Progress);
});

test("profile set/restore and gloss", () => {
  AISS.Profile.set("none");
  assert.equal(AISS.Profile.current.key, "none");
  assert.match(AISS.Profile.gloss("taenia", "the white line"), /white line/);
  AISS.Profile.set("clinician");
  assert.equal(AISS.Profile.gloss("taenia", "the white line"), "taenia");
  AISS.Profile.set("student");
});

test("handover scoring: window beats a successful gamble", () => {
  AISS.Handover.reset();
  AISS.Handover.assess(0.8, 26);
  const inside = AISS.Handover.handOver({ harmed: false });
  assert.equal(inside.tag, "correct");
  assert.equal(inside.points, 40);

  AISS.Handover.reset();
  AISS.Handover.assess(0.9, 30);
  const gamble = AISS.Handover.pushedOn(true);
  assert.equal(gamble.tag, "gambleWon");
  assert.ok(gamble.points < inside.points);

  AISS.Handover.reset();
  AISS.Handover.assess(0.9, 30);
  const lost = AISS.Handover.pushedOn(false);
  assert.equal(lost.tag, "gambleLost");
  assert.equal(lost.points, -55);
});

test("ask answers from module content and refuses invention", () => {
  AISS.Ask.build({
    layers: [{ name: "Parietal pleura", note: "The last barrier before the chest." }],
    steps: [{ instr: "Kelly clamp", say: "Over the superior border of the rib below.", demo: "Feel bone, then the edge." }],
    extra: [{ kind: "anatomy", title: "Safe triangle", text: "Pec major, lat dorsi, nipple line." }],
  });
  const hit = AISS.Ask.answer("what is the parietal pleura");
  assert.match(hit.text, /last barrier/i);
  const miss = AISS.Ask.answer("how do I prove the Riemann hypothesis");
  assert.match(miss.text, /Not something I have at this field/);
  assert.equal(miss.confident, false);
});

test("humor is fenced while unstable or after harm", () => {
  AISS.Humor.reset();
  assert.equal(AISS.Humor.line("minor-error", { unstable: true }), null);
  assert.equal(AISS.Humor.line("minor-error", { harmed: true }), null);
  const ok = AISS.Humor.line("wrong-instrument", { unstable: false, harmed: false });
  assert.ok(ok && /Mayo|give it to you/i.test(ok.s));
});

test("two-axis tuning holds when accurate and overloaded", () => {
  AISS.Stress.arousal = 80;
  const hold = AISS.tuning(70);
  assert.equal(hold.note, "holding");
  AISS.Stress.arousal = 80;
  const back = AISS.tuning(40);
  assert.equal(back.note, "backing off");
  AISS.Stress.reset();
});

test("progress tracks domains and names a weakest fix", () => {
  AISS.Progress.init("unit-test-module");
  AISS.Progress.mark("anatomy", true);
  AISS.Progress.mark("anatomy", true);
  AISS.Progress.mark("instrument", false);
  AISS.Progress.mark("instrument", false);
  const w = AISS.Progress.weakest();
  assert.equal(w.key, "instrument");
  assert.match(AISS.Progress.table(), /Instrument naming is your weakest/);
});
