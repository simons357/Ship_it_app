import { FAILURE, newId } from "./contracts.js";

export class OfflineQueue {
  constructor(state) {
    this.state = state;
    if (!Array.isArray(this.state.syncQueue)) this.state.syncQueue = [];
  }

  enqueue(type, payload) {
    this.state.syncQueue.push({
      id: newId("q"),
      t: Date.now(),
      type,
      payload,
      delivered: false,
    });
  }

  pending() {
    return this.state.syncQueue.filter((e) => !e.delivered);
  }
}

export class SyncTransport {
  constructor(name) {
    this.name = name;
  }
  async send(_event) {
    throw new Error("replaceable transport: implement send");
  }
  async pull() {
    return [];
  }
}

/** Same-browser / same-origin stand-in. Replace with Multipeer or hub HTTP. */
export class LocalBroadcastTransport extends SyncTransport {
  constructor() {
    super("local-broadcast");
    this.channel = typeof BroadcastChannel !== "undefined"
      ? new BroadcastChannel("listener.sync")
      : null;
  }
  async send(event) {
    this.channel?.postMessage(event);
    return { ok: true, transport: this.name };
  }
}

export class HubTransport extends SyncTransport {
  constructor(baseUrl) {
    super("hub");
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }
  async send(event) {
    const res = await fetch(`${this.baseUrl}/v1/events`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(event),
    });
    if (!res.ok) throw new Error(FAILURE.scoutLost);
    return res.json();
  }
  async pull(sessionId) {
    const res = await fetch(`${this.baseUrl}/v1/sessions/${encodeURIComponent(sessionId)}/events`);
    if (!res.ok) throw new Error(FAILURE.scoutLost);
    return res.json();
  }
}

export async function flushQueue(queue, transport) {
  const pending = queue.pending();
  for (const event of pending) {
    try {
      await transport.send(event);
      event.delivered = true;
    } catch {
      return { ok: false, message: FAILURE.scoutLost, remaining: queue.pending().length };
    }
  }
  return { ok: true, remaining: 0 };
}
