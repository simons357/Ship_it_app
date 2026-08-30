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
