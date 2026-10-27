/** Shared LISTENER data contracts. No fake classifier claims. */
export const DOORS = Object.freeze(["listen", "scout", "broadcast"]);
export const ROLES = Object.freeze(["hub", "base", "scout", "node"]);
export const MAP_MODES = Object.freeze(["field", "satellite", "hybrid"]);
export const NOTE_KINDS = Object.freeze(["saw", "heard", "photo", "video", "mystery"]);
export const ENCOUNTER_KINDS = Object.freeze([
  "unknown",
  "wildlife",
  "probable_human_excluded",
]);
export const PROVENANCE = Object.freeze([
  "listener_measurement",
  "user",
  "classifier",
  "reference",
  "expert_validation",
]);

export const FAILURE = Object.freeze({
  scoutLost:
    "Scout connection lost. Still recording — we'll sync when you're back.",
  micDenied:
    "This phone needs the microphone to keep the original. Your session is still here.",
});

export const COH_INSUFFICIENT = Object.freeze({
  display: "—",
  status: "INSUFFICIENT FIELD DATA",
  computed: false,
});

export function newId(prefix) {
  return `${prefix}_${crypto.randomUUID()}`;
}

export function inviteCode() {
  const alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  let s = "";
  for (let i = 0; i < 6; i++) s += alphabet[Math.floor(Math.random() * alphabet.length)];
  return s;
}

/** ~11 km grid. Precise home/routes never leave the device by default. */
export function coarseLocation(lat, lon) {
  if (!Number.isFinite(lat) || !Number.isFinite(lon)) return null;
  return {
    lat: Math.round(lat * 10) / 10,
    lon: Math.round(lon * 10) / 10,
    precision: "coarse",
  };
}

export function emptySession(partial = {}) {
  const now = Date.now();
  return {
    id: partial.id || newId("ses"),
    startedAt: partial.startedAt || now,
    door: partial.door || "listen",
    role: partial.role || "base",
    inviteCode: partial.inviteCode || inviteCode(),
    startLat: partial.startLat ?? null,
    startLon: partial.startLon ?? null,
    startAccuracy: partial.startAccuracy ?? null,
    startGpsQuality: partial.startGpsQuality || "unknown",
    status: partial.status || "active",
    returnActive: false,
    mapMode: partial.mapMode || "field",
    title: partial.title || "Field session",
    broadcastId: partial.broadcastId || null,
  };
}

export function emptyEncounter(partial = {}) {
  return {
    id: partial.id || newId("enc"),
    sessionId: partial.sessionId,
    t: partial.t || Date.now(),
    kind: partial.kind || "unknown",
    label: partial.label || "UNKNOWN",
    candidateId: null,
    confidence: null,
    provenance: partial.provenance || "user",
    excluded: partial.kind === "probable_human_excluded",
    exclusionReason: partial.exclusionReason || null,
    originalAudioId: partial.originalAudioId || null,
    lat: partial.lat ?? null,
    lon: partial.lon ?? null,
    contributingNodeIds: partial.contributingNodeIds || [],
    humanSpeechGate: partial.humanSpeechGate || "pending",
    shared: false,
    contributed: false,
    firstSound: Boolean(partial.firstSound),
  };
}

/** User words or UNKNOWN. Never invent a species. */
export function fieldNoteLabel(text) {
  const words = String(text || "").trim();
  return words || "UNKNOWN";
}

export function canContribute(encounter) {
  if (!encounter) return { ok: false, reason: "No signal selected." };
  if (encounter.kind === "probable_human_excluded" || encounter.excluded) {
    return {
      ok: false,
      reason: "Probable human speech stays off the wildlife library.",
    };
  }
  if (encounter.humanSpeechGate !== "excluded") {
    return {
      ok: false,
      reason: "Confirm this is not human speech before sending it to the library.",
    };
  }
  return { ok: true };
}

export function canShareCard(encounter) {
  if (!encounter) return { ok: false, reason: "No card." };
  return { ok: true, contributesOriginal: false };
}

export function coherenceFromField(nodes = [], windowMs = 0, measuredValue = null) {
  const nearby = nodes.filter((n) => n.nearby && n.synchronized);
  if (nearby.length < 2 || windowMs <= 0 || measuredValue == null) {
    return { ...COH_INSUFFICIENT };
  }
  return {
    display: String(measuredValue),
    status: "MEASURED",
    computed: true,
    value: measuredValue,
  };
}

export function emptyBroadcast(partial = {}) {
  return {
    id: partial.id || newId("bc"),
    title: partial.title || "Field broadcast",
    createdAt: partial.createdAt || Date.now(),
    live: partial.live ?? true,
    sessionId: partial.sessionId || null,
    watchers: partial.watchers || 1,
    nodeOptIn: partial.nodeOptIn || false,
  };
}

export function emptyNode(partial = {}) {
  return {
    id: partial.id || newId("node"),
    sessionId: partial.sessionId,
    deviceId: partial.deviceId || null,
    role: partial.role || "base",
    label: partial.label || "LISTENER",
    lat: partial.lat ?? null,
    lon: partial.lon ?? null,
    accuracy: partial.accuracy ?? null,
    heading: partial.heading ?? null,
    nearby: partial.nearby ?? true,
    synchronized: partial.synchronized ?? false,
    lastSeen: partial.lastSeen || Date.now(),
  };
}

export function emptyNote(partial = {}) {
  return {
    id: partial.id || newId("note"),
    sessionId: partial.sessionId,
    encounterId: partial.encounterId || null,
    kind: partial.kind || "mystery",
    body: partial.body || "",
    mediaId: partial.mediaId || null,
    lat: partial.lat ?? null,
    lon: partial.lon ?? null,
    t: partial.t || Date.now(),
  };
}

export function emptyCard(partial = {}) {
  return {
    id: partial.id || newId("card"),
    encounterId: partial.encounterId,
    sessionId: partial.sessionId,
    sharePublic: !!partial.sharePublic,
    contributeLibrary: !!partial.contributeLibrary,
    coarse: partial.coarse || null,
    createdAt: partial.createdAt || Date.now(),
  };
}

export function contributionPayload(encounter, location, { contributeLibrary, sharePublic, exactLocation } = {}) {
  if (!canContribute(encounter).ok) {
    return { ok: false, reason: canContribute(encounter).reason, transcript: null, speakerId: null };
  }
  if (!contributeLibrary) {
    return { ok: false, reason: "Contribution is opt-in.", transcript: null, speakerId: null };
  }
  const loc = exactLocation && location
    ? { ...location, precision: "exact" }
    : location
      ? coarseLocation(location.lat, location.lon)
      : null;
  return {
    ok: true,
    location: loc,
    sharePublic: !!sharePublic,
    contributeLibrary: true,
    transcript: null,
    speakerId: null,
    candidateSpecies: encounter.candidateId,
  };
}
