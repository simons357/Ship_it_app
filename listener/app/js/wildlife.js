/**
 * Wildlife-only gate. Never transcribe. Never identify a speaker.
 * Classifiers are fallible — decisions are labeled, not claimed as truth.
 */
export function excludeProbableHuman(encounter, reason = "probable_human_speech") {
  return {
    ...encounter,
    kind: "probable_human_excluded",
    excluded: true,
    exclusionReason: reason,
    humanSpeechGate: "excluded_as_human",
    label: "EXCLUDED · PROBABLE HUMAN",
    candidateId: null,
    confidence: null,
  };
}

export function confirmNonHuman(encounter) {
  if (encounter.kind === "probable_human_excluded") {
    return { ok: false, encounter, reason: "Already excluded as probable human speech." };
  }
  return {
    ok: true,
    encounter: {
      ...encounter,
      humanSpeechGate: "excluded",
      kind: encounter.kind === "wildlife" ? "wildlife" : "unknown",
    },
  };
}

export function markUnknown(encounter) {
  return {
    ...encounter,
    kind: "unknown",
    label: encounter.label && encounter.label !== "EXCLUDED · PROBABLE HUMAN"
      ? encounter.label
      : "UNKNOWN",
    candidateId: null,
    confidence: null,
    provenance: encounter.provenance || "user",
  };
}

/** No speech-to-text. Recording is evidence, not a transcript. */
export function mustNotTranscribe() {
  return true;
}

/**
 * Acoustic features only — never a transcript, never a speaker id.
 * Conservative: speech-like band + syllable-rate modulation.
 */
export function featuresSuggestHumanSpeech(features) {
  if (!features) return false;
  const rms = Number(features.rms) || 0;
  const peakHz = Number(features.peakHz);
  const modulationHz = Number(features.modulationHz);
  const speech = Number(features.bandEnergySpeech) || 0;
  const total = Number(features.bandEnergyTotal) || 0;
  if (rms < 0.01 || total <= 0) return false;
  const ratio = speech / total;
  const voiceBand = Number.isFinite(peakHz) && peakHz >= 85 && peakHz <= 3500;
  const syllable = Number.isFinite(modulationHz) && modulationHz >= 2 && modulationHz <= 8;
  return ratio > 0.55 && voiceBand && syllable;
}

/**
 * Wildlife-only pipeline. UNKNOWN is first-class. Never invent a species.
 * Probable human speech: no encounter, no library contribute.
 */
export function processSignal(input = {}) {
  const transcript = null;
  const speakerId = null;
  const candidateSpecies = null;
  const human =
    input.probableHumanSpeech === true || featuresSuggestHumanSpeech(input.features);
  if (human) {
    return {
      createEncounter: false,
      contribute: false,
      kind: "probable_human_excluded",
      internalLabel: "probable-human-exclusion",
      label: "EXCLUDED · PROBABLE HUMAN",
      transcript,
      speakerId,
      candidateSpecies,
    };
  }
  return {
    createEncounter: true,
    contribute: "opt-in-after-confirm",
    kind: "unknown",
    internalLabel: "unknown-biological-candidate",
    label: input.label || "UNKNOWN",
    transcript,
    speakerId,
    candidateSpecies,
  };
}
