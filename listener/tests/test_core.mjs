import assert from "node:assert/strict";
import test from "node:test";
import {
  FAILURE,
  canContribute,
  canShareCard,
  coarseLocation,
  coherenceFromField,
  contributionPayload,
  emptyEncounter,
  emptySession,
  emptyNode,
  emptyBroadcast,
  emptyNote,
  emptyCard,
} from "../app/js/contracts.js";
import {
  confirmNonHuman,
  excludeProbableHuman,
  featuresSuggestHumanSpeech,
  mustNotTranscribe,
  processSignal,
} from "../app/js/wildlife.js";
import { gpsQuality, distanceM, projectRelative } from "../app/js/geo.js";

test("coarse location rounds to ~11 km and never stays exact", () => {
  const c = coarseLocation(32.01234, -81.09876);
  assert.equal(c.lat, 32);
  assert.equal(c.lon, -81.1);
  assert.equal(c.precision, "coarse");
  assert.equal(coarseLocation(NaN, -81), null);
});

test("wildlife exclusion: no transcript, no speaker, no encounter, no contribute", () => {
  const decision = processSignal({ probableHumanSpeech: true });
  assert.equal(decision.createEncounter, false);
  assert.equal(decision.contribute, false);
  assert.equal(decision.transcript, null);
  assert.equal(decision.speakerId, null);
  assert.equal(decision.candidateSpecies, null);
  assert.equal(decision.internalLabel, "probable-human-exclusion");
  assert.equal(mustNotTranscribe(), true);

  const enc = excludeProbableHuman(emptyEncounter({ kind: "unknown" }));
  assert.equal(canContribute(enc).ok, false);
  const payload = contributionPayload(enc, { lat: 32.01, lon: -81.09 }, { contributeLibrary: true });
  assert.equal(payload.ok, false);
  assert.equal(payload.transcript, null);
  assert.equal(payload.speakerId, null);
});

test("UNKNOWN is first-class and never invents a species", () => {
  const decision = processSignal({ probableHumanSpeech: false });
  assert.equal(decision.createEncounter, true);
  assert.equal(decision.kind, "unknown");
  assert.equal(decision.candidateSpecies, null);
  assert.equal(decision.transcript, null);
  assert.equal(decision.label, "UNKNOWN");
});

test("speech-like features exclude without transcription", () => {
  assert.equal(
    featuresSuggestHumanSpeech({
      rms: 0.2,
      peakHz: 180,
      modulationHz: 4,
      bandEnergySpeech: 8,
      bandEnergyTotal: 10,
    }),
    true
  );
  assert.equal(
    featuresSuggestHumanSpeech({
      rms: 0.2,
      peakHz: 6200,
      modulationHz: 40,
      bandEnergySpeech: 1,
      bandEnergyTotal: 10,
    }),
    false
  );
});

test("contribute requires non-human confirmation; share is a different permission", () => {
  let enc = emptyEncounter({ kind: "unknown", lat: 32.05, lon: -80.97 });
  assert.equal(canContribute(enc).ok, false);
  enc = confirmNonHuman(enc).encounter;
  assert.equal(canContribute(enc).ok, true);
  const share = canShareCard(enc);
  assert.equal(share.ok, true);
  assert.equal(share.contributesOriginal, false);
  const payload = contributionPayload(enc, { lat: 32.05, lon: -80.97 }, { contributeLibrary: true });
  assert.equal(payload.ok, true);
  assert.equal(payload.location.precision, "coarse");
  assert.equal(payload.location.lat, 32.1);
  assert.equal(payload.transcript, null);
});

test("failure language is consumer copy", () => {
  assert.match(FAILURE.scoutLost, /Scout connection lost\. Still recording/);
  assert.equal(/peer socket|route negotiation/i.test(FAILURE.scoutLost), false);
});

test("session object model: Broadcast → Session → Node → Encounter → Note → Card", () => {
  const session = emptySession({ door: "listen", role: "base" });
  assert.ok(session.id.startsWith("ses_"));
  assert.equal(session.role, "base");
  assert.equal(session.returnActive, false);
  const broadcast = emptyBroadcast({ sessionId: session.id });
  const node = emptyNode({ sessionId: session.id, role: "base" });
  const encounter = emptyEncounter({ sessionId: session.id });
  const note = emptyNote({ sessionId: session.id, encounterId: encounter.id, kind: "mystery" });
  const card = emptyCard({ sessionId: session.id, encounterId: encounter.id });
  assert.equal(broadcast.sessionId, session.id);
  assert.equal(node.sessionId, session.id);
  assert.equal(note.encounterId, encounter.id);
  assert.equal(card.contributeLibrary, false);
  assert.equal(card.sharePublic, false);
  assert.equal(encounter.candidateId, null);
});

test("DA / Coh-Rez stays blank without 2+ synchronized nodes and a real window", () => {
  const one = coherenceFromField([{ nearby: true, synchronized: true }], 400, 0.4);
  assert.equal(one.display, "—");
  assert.equal(one.status, "INSUFFICIENT FIELD DATA");
  const twoNoMeasure = coherenceFromField(
    [
      { nearby: true, synchronized: true },
      { nearby: true, synchronized: true },
    ],
    400,
    null
  );
  assert.equal(twoNoMeasure.computed, false);
  assert.equal(twoNoMeasure.display, "—");
});

test("GPS quality is honest", () => {
  assert.equal(gpsQuality(8), "good");
  assert.equal(gpsQuality(30), "fair");
  assert.equal(gpsQuality(80), "fading");
  assert.equal(gpsQuality(undefined), "unknown");
});

test("relative plot stays finite", () => {
  const start = { lat: 32.0, lon: -81.0 };
  const p = projectRelative(start, { lat: 32.0004, lon: -80.9996 });
  assert.ok(p.left >= 8 && p.left <= 92);
  assert.ok(distanceM(start, { lat: 32.001, lon: -81.0 }) > 80);
});
