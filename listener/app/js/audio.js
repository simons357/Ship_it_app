export async function listInputs() {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    return devices
      .filter((d) => d.kind === "audioinput")
      .map((d) => ({
        id: d.deviceId,
        label: d.label || "Microphone",
        airpods: /airpods|headset|bluetooth/i.test(d.label || ""),
      }));
  } catch {
    return [];
  }
}

export function pickPreferredInput(inputs) {
  const pods = inputs.find((i) => i.airpods);
  return pods || inputs[0] || { id: "default", label: "iPhone mic", airpods: false };
}

export function isMicPermissionDenied(err) {
  const name = String(err?.name || "");
  return name === "NotAllowedError" || name === "PermissionDeniedError" || name === "SecurityError";
}

export function isMicUnavailable(err) {
  if (typeof navigator === "undefined" || !navigator.mediaDevices?.getUserMedia) return true;
  const name = String(err?.name || "");
  return name === "NotFoundError" || name === "NotSupportedError" || name === "NotReadableError";
}

/** Quiet local WAV — a kept original, never a species label. */
export function makeLocalOriginalBlob({ seconds = 0.8, hz = 180 } = {}) {
  const sampleRate = 44100;
  const n = Math.max(1, Math.floor(sampleRate * seconds));
  const bytes = 44 + n * 2;
  const buf = new ArrayBuffer(bytes);
  const view = new DataView(buf);
  const writeStr = (offset, s) => {
    for (let i = 0; i < s.length; i++) view.setUint8(offset + i, s.charCodeAt(i));
  };
  writeStr(0, "RIFF");
  view.setUint32(4, bytes - 8, true);
  writeStr(8, "WAVE");
  writeStr(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeStr(36, "data");
  view.setUint32(40, n * 2, true);
  for (let i = 0; i < n; i++) {
    const sample = Math.sin((2 * Math.PI * hz * i) / sampleRate) * 0.08;
    view.setInt16(44 + i * 2, Math.max(-1, Math.min(1, sample)) * 0x7fff, true);
  }
  return new Blob([buf], { type: "audio/wav" });
}

export async function startLocalOriginalRecording() {
  const started = Date.now();
  return {
    localOriginal: true,
    stream: null,
    recorder: null,
    mime: "audio/wav",
    async stop() {
      const seconds = Math.max(0.4, Math.min(8, (Date.now() - started) / 1000));
      return makeLocalOriginalBlob({ seconds, hz: 180 });
    },
  };
}

export async function startRecording(deviceId) {
  const constraints = {
    audio: deviceId && deviceId !== "default"
      ? { deviceId: { exact: deviceId } }
      : { echoCancellation: false, noiseSuppression: false, autoGainControl: false },
    video: false,
  };
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  const mime = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
    ? "audio/webm;codecs=opus"
    : "audio/webm";
  const recorder = new MediaRecorder(stream, { mimeType: mime });
  const chunks = [];
  recorder.ondataavailable = (e) => {
    if (e.data.size) chunks.push(e.data);
  };
  const stopped = new Promise((resolve) => {
    recorder.onstop = () => {
      stream.getTracks().forEach((t) => t.stop());
      resolve(new Blob(chunks, { type: mime }));
    };
  });
  recorder.start(250);
  return {
    stream,
    recorder,
    mime,
    async stop() {
      if (recorder.state !== "inactive") recorder.stop();
      return stopped;
    },
  };
}
