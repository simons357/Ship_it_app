import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";
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
  fieldNoteLabel,
} from "../app/js/contracts.js";
import {
  confirmNonHuman,
  excludeProbableHuman,
  featuresSuggestHumanSpeech,
  firstSoundDecision,
  mustNotTranscribe,
  processSignal,
} from "../app/js/wildlife.js";
import { gpsQuality, distanceM, projectRelative } from "../app/js/geo.js";
import { makeLocalOriginalBlob } from "../app/js/audio.js";
import { skyPeriod, weatherLine } from "../app/js/weather.js";
import { ownerEndpoints } from "../app/js/plugins.js";
import { STORIES, tonightStory, tonightPool, dayNumber, listeningRank, ageLine, inferYear, inferRarity } from "../app/js/stories.js";
import { LESSONS, todayLesson } from "../app/js/lessons.js";

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

test("first sound is rain or UNKNOWN — never a species, never auto-contributed", () => {
  const rain = firstSoundDecision("rain");
  assert.equal(rain.createEncounter, true);
  assert.equal(rain.kind, "unknown");
  assert.equal(rain.label, "rain");
  assert.equal(rain.candidateSpecies, null);
  assert.equal(rain.transcript, null);
  assert.equal(rain.speakerId, null);
  assert.equal(rain.contribute, "opt-in-after-confirm");
  assert.equal(firstSoundDecision("").label, "UNKNOWN");
  assert.equal(fieldNoteLabel(""), "UNKNOWN");
  assert.equal(fieldNoteLabel("  rain  "), "rain");

  let enc = emptyEncounter({ kind: "unknown", label: "rain", firstSound: true });
  assert.equal(enc.firstSound, true);
  assert.equal(enc.contributed, false);
  assert.equal(canContribute(enc).ok, false);
  enc = confirmNonHuman(enc).encounter;
  assert.equal(canContribute(enc).ok, true);
  assert.equal(enc.kind, "unknown");
  assert.equal(enc.label, "rain");
  const payload = contributionPayload(enc, { lat: 32.05, lon: -80.97 }, { contributeLibrary: false });
  assert.equal(payload.ok, false);
});

test("rain-like broadband is not human speech", () => {
  assert.equal(
    featuresSuggestHumanSpeech({
      rms: 0.12,
      peakHz: 6500,
      modulationHz: 0.4,
      bandEnergySpeech: 1.5,
      bandEnergyTotal: 12,
    }),
    false
  );
});

test("mic denied copy is honest and keeps the session", () => {
  assert.match(FAILURE.micDenied, /microphone to keep the original/i);
  assert.match(FAILURE.micDenied, /session is still here/i);
  assert.equal(/getUserMedia|NotAllowedError|permission denied/i.test(FAILURE.micDenied), false);
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

test("local original is a kept file, never a species label", async () => {
  const blob = makeLocalOriginalBlob({ seconds: 0.4, hz: 180 });
  assert.equal(blob.type, "audio/wav");
  assert.ok(blob.size > 44);
});

test("sky is from this clock; weather is the owner's app", () => {
  assert.equal(["night", "dawn", "day", "dusk"].includes(skyPeriod(new Date("2026-08-30T12:00:00"))), true);
  assert.equal(skyPeriod(new Date("2026-08-30T12:00:00")), "day");
  assert.equal(skyPeriod(new Date("2026-08-30T22:00:00")), "night");
  const line = weatherLine(null, new Date("2026-08-30T12:00:00"));
  assert.match(line, /your weather not connected|waiting on your weather/);
  assert.equal(ownerEndpoints().weather, "");
  assert.equal(ownerEndpoints().search, "");
});

test("ON AIR stays hidden until recording — display:flex must not leak past [hidden]", async () => {
  const css = await readFile(new URL("../app/css/app.css", import.meta.url), "utf8");
  const html = await readFile(new URL("../app/index.html", import.meta.url), "utf8");
  assert.match(html, /id="onAir"[^>]*hidden/);
  assert.match(html, /id="recordBtn"[^>]*>LISTEN TO THE FIELD</);
  assert.match(html, /storyListen/);
  assert.match(html, /A STORY IS SOMETHING YOU LISTEN TO/);
  assert.match(html, /bedtime\.html/);
  assert.match(html, /GREEN SCREEN · READ TO THE CHILDREN/);
  assert.match(html, /id="greenLink"/);
  assert.match(html, /older and rarer/);
  assert.equal(/id="recordBtn"[^>]*\bstart\b/.test(html), false);
  assert.match(html, /icon-192\.png/);
  assert.equal(html.includes("LISTEN TO THIS RAIN"), false);
  const app = await readFile(new URL("../app/js/app.js", import.meta.url), "utf8");
  assert.equal(app.includes("Tap START"), false);
  assert.match(css, /\.on-air\[hidden\][\s\S]*display:\s*none\s*!important/);
  assert.match(css, /\.live-meter\[hidden\]/);
});

test("one little bedtime story a day — same calendar day, same story", () => {
  const morning = tonightStory(new Date(2026, 8, 7, 8, 0, 0));
  const night = tonightStory(new Date(2026, 8, 7, 22, 30, 0));
  const tomorrow = tonightStory(new Date(2026, 8, 8, 8, 0, 0));
  assert.equal(morning.id, night.id);
  assert.notEqual(morning.id, tomorrow.id);
  assert.equal(morning.bedtime, true);
  assert.equal(morning.rare, true);
  assert.ok(morning.pages.length >= 5);
  assert.equal(dayNumber(new Date(2026, 8, 7, 1)), dayNumber(new Date(2026, 8, 7, 23)));
});

test("stories are public-domain or original — no copyrighted picture books", () => {
  const banned = /Where the Wild Things|Cat in the Hat|Green Eggs|Goodnight Moon|Sendak|Seuss|Harry Potter/;
  assert.ok(STORIES.length >= 10);
  for (const s of STORIES) {
    assert.match(s.rights, /public-domain|original/);
    assert.equal(s.bedtime, true);
    assert.ok(s.pages.every((p) => typeof p === "string" && p.length > 0));
    assert.equal(banned.test([s.title, s.source, ...s.pages].join(" ")), false);
  }
});

test("green-screen bedtime page is chroma green and tonight-only", async () => {
  const html = await readFile(new URL("../app/bedtime.html", import.meta.url), "utf8");
  assert.match(html, /#00FF00/);
  assert.match(html, /tonightStory/);
  assert.match(html, /todayLesson/);
  assert.match(html, /I’LL READ|I'LL READ/);
  assert.match(html, /I’LL TEACH|I'LL TEACH/);
  assert.match(html, /NIGHT LAMP/);
  assert.match(html, /HIDE BUTTONS/);
  assert.match(html, /stopPropagation/);
  assert.equal(html.includes("Where the Wild Things"), false);
  assert.equal(/Dr\.|Professor |TED Talk/.test(html), false);
});

test("daily stories prefer older and rarer — famous common tales stay in MORE STORIES", () => {
  const pool = tonightPool();
  const ids = pool.map((s) => s.id);
  assert.equal(ids.includes("goldilocks"), false);
  assert.equal(ids.includes("cinderella"), false);
  assert.equal(ids.includes("peter-rabbit"), false);
  assert.equal(ids.includes("three-pigs"), false);
  assert.ok(ids.includes("diamonds-toads") || ids.includes("donkeyskin"));
  assert.ok(ids.includes("star-money"));
  assert.ok(ids.includes("buried-moon"));
  for (const s of pool) {
    assert.ok(inferRarity(s) >= 4, s.id);
  }
  const perrault = STORIES.find((s) => s.id === "diamonds-toads");
  const tin = STORIES.find((s) => s.id === "tin-soldier");
  assert.ok(inferYear(perrault) < inferYear(tin));
  assert.ok(listeningRank(perrault) > listeningRank(tin));
  assert.match(ageLine(perrault), /older · rarer/);
  assert.match(ageLine(perrault), /1697/);
  assert.equal(/· 0 ·/.test(ageLine({ source: "For whoever is teaching", rare: true })), false);
  assert.match(ageLine({ source: "For whoever is teaching", rare: true }), /older · rarer/);
});

test("someone can teach listening — older and rarer, no invented expert", () => {
  const morning = todayLesson(new Date(2026, 8, 7, 8, 0, 0));
  const night = todayLesson(new Date(2026, 8, 7, 22, 30, 0));
  const tomorrow = todayLesson(new Date(2026, 8, 8, 8, 0, 0));
  assert.equal(morning.id, night.id);
  assert.notEqual(morning.id, tomorrow.id);
  assert.ok(LESSONS.length >= 5);
  const banned = /Dr\.|Professor |PhD|TED Talk|active listening workshop|Where the Wild Things|Seuss/;
  for (const lesson of LESSONS) {
    assert.equal(lesson.source, "For whoever is teaching");
    assert.match(lesson.rights, /original/);
    assert.equal(lesson.rare, true);
    assert.ok(lesson.pages.length >= 5);
    assert.equal(banned.test([lesson.title, lesson.source, ...lesson.pages].join(" ")), false);
  }
  const corpus = LESSONS.flatMap((l) => [l.title, ...l.pages]).join(" ");
  assert.match(corpus, /older|Older/);
  assert.match(corpus, /rarer|Rarer/);
});

test("relative plot stays finite", () => {
  const start = { lat: 32.0, lon: -81.0 };
  const p = projectRelative(start, { lat: 32.0004, lon: -80.9996 });
  assert.ok(p.left >= 8 && p.left <= 92);
  assert.ok(distanceM(start, { lat: 32.001, lon: -81.0 }) > 80);
});
