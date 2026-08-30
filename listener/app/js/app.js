import {
  COH_INSUFFICIENT,
  FAILURE,
  canContribute,
  coarseLocation,
  emptyEncounter,
  emptySession,
  fieldNoteLabel,
  newId,
} from "./contracts.js";
import { hydrate, loadState, putOriginal, rememberDevice, saveState } from "./db.js";
import { confirmNonHuman, excludeProbableHuman, firstSoundDecision, markUnknown, processSignal } from "./wildlife.js";
import { HubTransport, LocalBroadcastTransport, OfflineQueue, flushQueue } from "./sync.js";
import { bearingDeg, distanceM, projectRelative, watchPosition } from "./geo.js";
import {
  isMicPermissionDenied,
  isMicUnavailable,
  listInputs,
  pickPreferredInput,
  startLocalOriginalRecording,
  startRecording,
} from "./audio.js";
import { clockLabel, fetchFieldWeather, skyPeriod, weatherLine } from "./weather.js";
import { indexOwnerSearch, ownerEndpoints, queryOwnerSearch } from "./plugins.js";

const $ = (id) => document.getElementById(id);
let state = rememberDevice(loadState());
const queue = new OfflineQueue(state);
const localTransport = new LocalBroadcastTransport();
const hubUrl = localStorage.getItem("listener.hub") || "";
const transport = hubUrl ? new HubTransport(hubUrl) : localTransport;

let fix = null;
let stopWatch = null;
let rec = null;
let recStarted = 0;
let heading = 0;
let firstSoundArmed = false;
let firstSoundMicDenied = false;
let showInstrument = false;
let recordBusy = false;
let lastWeather = null;
let lastWxAt = 0;
let pendingKeep = null;
let recTick = null;
let airpodsOn = false;
let recordBound = false;

function persist() {
  saveState(state);
}

function toast(msg) {
  const el = $("toast");
  if (!el) return;
  el.hidden = false;
  el.textContent = msg;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => {
    el.hidden = true;
  }, 4200);
}

function anotherListenerAvailable() {
  return state.pairedDevices.length > 0 || state.sessions.length > 0;
}

function unprojectTap(start, leftPct, topPct, spanM = 120) {
  const dx = ((leftPct - 50) / 38) * spanM;
  const dy = ((58 - topPct) / 38) * spanM;
  const mLat = 111320;
  const mLon = 111320 * Math.cos((start.lat * Math.PI) / 180);
  return {
    lat: start.lat + dy / mLat,
    lon: start.lon + dx / (mLon || 1),
  };
}

function captionForMode(mode) {
  const el = $("mapCaption");
  if (!el) return;
  el.hidden = false;
  if (mode === "satellite") el.textContent = "SATELLITE · MapKit on iPhone · relative plot here";
  else if (mode === "hybrid") el.textContent = "HYBRID · MapKit on iPhone · relative plot here";
  else el.textContent = "FIELD · GPS-relative plot · no scraped map tiles";
}

function session() {
  return state.sessions.find((s) => s.id === state.activeSessionId) || null;
}

function sessionCrumbs() {
  const s = session();
  if (!s) return [];
  return state.breadcrumbs.filter((b) => b.sessionId === s.id);
}

function sessionNotes() {
  const s = session();
  if (!s) return [];
  return state.notes.filter((n) => n.sessionId === s.id);
}

function sessionEncounters() {
  const s = session();
  if (!s) return [];
  return state.encounters.filter((e) => e.sessionId === s.id && !e.excluded);
}

function firstSoundEncounter() {
  const s = session();
  return (
    state.encounters.find((e) => e.firstSound && !e.excluded && (!s || e.sessionId === s.id)) || null
  );
}

function allowLocalOriginalFallback() {
  try {
    return new URLSearchParams(location.search).has("localOriginal");
  } catch {
    return false;
  }
}

function padTime(n) {
  return String(n).padStart(2, "0");
}

function elapsedLabel(from) {
  const s = Math.max(0, Math.floor((Date.now() - from) / 1000));
  return `${padTime(Math.floor(s / 60))}:${padTime(s % 60)}`;
}

function applySky() {
  const el = $("onboard");
  if (!el) return;
  const period = skyPeriod();
  el.classList.remove("sky-night", "sky-dawn", "sky-day", "sky-dusk", "sky-wet");
  el.classList.add(`sky-${period}`);
  if (lastWeather?.wet) el.classList.add("sky-wet");
  const clock = $("fieldClock");
  const wx = $("fieldWeather");
  if (clock) clock.textContent = clockLabel();
  if (wx) {
    wx.hidden = !lastWeather;
    if (lastWeather) wx.textContent = weatherLine(lastWeather);
  }
}

async function refreshWeather() {
  if (Date.now() - lastWxAt < 60000 && lastWeather) {
    applySky();
    return;
  }
  lastWxAt = Date.now();
  const lat = fix?.lat;
  const lon = fix?.lon;
  lastWeather = await fetchFieldWeather(lat, lon).catch(() => null);
  applySky();
}

async function detectAirpods() {
  const inputs = await listInputs().catch(() => []);
  const pref = pickPreferredInput(inputs);
  airpodsOn = Boolean(pref.airpods);
  const role = $("fieldRole");
  if (role) {
    role.hidden = !airpodsOn;
    if (airpodsOn) role.textContent = "SCOUT · AirPods";
  }
  return airpodsOn;
}

function localHeard(q = "") {
  const needle = String(q || "").trim().toLowerCase();
  return state.encounters
    .filter((e) => !e.excluded)
    .filter((e) => !needle || String(e.label || "").toLowerCase().includes(needle))
    .slice(-12)
    .reverse();
}

async function renderHeard() {
  const list = $("heardList");
  const search = $("heardSearch");
  if (!list) return;
  const q = search?.value || "";
  let rows = localHeard(q);
  if (ownerEndpoints().search && q) {
    const remote = await queryOwnerSearch(q).catch(() => ({ results: [] }));
    if (remote.results?.length) {
      rows = remote.results.map((r) => ({
        id: r.id,
        t: r.t || Date.now(),
        label: r.label || "UNKNOWN",
        weather: r.weather,
        originalAudioId: r.hasOriginal,
      }));
    }
  }
  if (search) search.hidden = state.encounters.length === 0 && !ownerEndpoints().search;
  list.innerHTML = rows
    .map((e) => {
      const wx = e.weather?.label ? ` · ${e.weather.label}` : "";
      return `<div class="signal"><small>${new Date(e.t).toLocaleString()}${wx}</small><b>${e.label}</b><span>${e.originalAudioId ? "Original on this phone" : "No original"} · your search</span></div>`;
    })
    .join("");
}

function showWhatWasThat(on) {
  const form = $("whatWasThat");
  if (form) form.classList.toggle("hidden", !on);
}

function refreshRecordHome() {
  const recording = Boolean(rec);
  const denied = firstSoundMicDenied && !rec;
  const status = $("recordStatus");
  const btn = $("recordBtn");
  const timer = $("recTimer");
  if (status) {
    if (recording) status.textContent = "RECORDING. Original stays on this phone.";
    else if (denied) status.textContent = FAILURE.micDenied;
    else if (pendingKeep) status.textContent = "What was that?";
    else status.textContent = "Tap START. Put the phone down. Tap STOP when you are done.";
  }
  if (btn) {
    btn.disabled = false;
    btn.textContent = recording ? "STOP" : "START";
    btn.className = `record-btn ${recording ? "stop" : "start"}`;
  }
  if (timer) {
    timer.hidden = !recording;
    if (recording) timer.textContent = elapsedLabel(recStarted);
  }
  showWhatWasThat(Boolean(pendingKeep) && !recording);
  applySky();
  renderHeard();
}

function bindRecordHome() {
  if (recordBound) return;
  recordBound = true;
  const btn = $("recordBtn");
  if (btn) {
    btn.onclick = () => {
      if (rec) stopRecord();
      else startRecord();
    };
  }
  $("keepBtn")?.addEventListener("click", () => keepHeard($("whatText")?.value || "", $("whatPhoto")?.files?.[0] || null));
  $("unknownBtn")?.addEventListener("click", () => keepHeard("", $("whatPhoto")?.files?.[0] || null));
  $("heardSearch")?.addEventListener("input", () => renderHeard());
}

function showOnboard() {
  const el = $("onboard");
  if (showInstrument) {
    el.classList.remove("show");
    return;
  }
  el.classList.add("show");
  bindRecordHome();
  refreshRecordHome();
  detectAirpods();
}

function recordHomeHTML() {
  return "START STOP What was that? LOCAL FIELD";
}

async function ensureGeo() {
  if (stopWatch) return;
  stopWatch = watchPosition(
    (next) => {
      fix = next;
      heading = next.heading ?? heading;
      const s = session();
      if (s && s.role === "scout" && s.status === "active" && next.lat != null) {
        state.breadcrumbs.push({
          id: newId("bc"),
          sessionId: s.id,
          t: next.t,
          lat: next.lat,
          lon: next.lon,
          accuracy: next.accuracy,
          heading: next.heading,
          quality: next.quality,
        });
        persist();
      }
      refreshWeather();
      renderField();
    },
    () => {
      if (session()) toast("GPS unavailable — marks stay session-relative. RETURN still works on what you record.");
      refreshWeather();
      renderField();
    }
  );
}

async function beginDoor(door, opts = {}) {
  await ensureGeo();
  const role = opts.role || (door === "scout" ? "scout" : door === "broadcast" ? "hub" : "base");
  const s = emptySession({
    door,
    role,
    startLat: fix?.lat ?? null,
    startLon: fix?.lon ?? null,
    startAccuracy: fix?.accuracy ?? null,
    startGpsQuality: fix?.quality || "unknown",
    title: door === "broadcast" ? "Field broadcast" : "Field session",
    localFrame: !fix,
  });
  if (s.startLat == null) {
    s.localFrame = true;
    s.startLat = 0;
    s.startLon = 0;
  }
  if (door === "broadcast") {
    const b = {
      id: newId("bcst"),
      sessionId: s.id,
      title: "Field broadcast",
      startedAt: Date.now(),
      watchers: 1,
      sensorOptIn: false,
    };
    s.broadcastId = b.id;
    state.broadcasts.push(b);
  }
  state.sessions.push(s);
  state.activeSessionId = s.id;
  state.nodes.push({
    id: state.deviceId,
    sessionId: s.id,
    role: s.role,
    name: s.role === "base" ? "BASE · YOU" : s.role === "scout" ? "SCOUT · YOU" : "HUB · YOU",
    lat: s.startLat,
    lon: s.startLon,
    nearby: true,
    synchronized: false,
    lastSeen: Date.now(),
  });
  queue.enqueue("session.open", { sessionId: s.id, role: s.role, inviteCode: s.inviteCode });
  persist();
  if (!opts.stayOnboard) {
    showInstrument = true;
    $("onboard").classList.remove("show");
    if (door === "scout") openSheet("scout");
    else if (door === "broadcast") showTab("broadcast");
  }
  renderAll();
}

function startRecClock() {
  clearInterval(recTick);
  const timer = $("recTimer");
  recTick = setInterval(() => {
    if (!rec) {
      clearInterval(recTick);
      return;
    }
    if (timer) timer.textContent = elapsedLabel(recStarted);
  }, 250);
}

async function startRecord() {
  if (recordBusy || rec) return;
  recordBusy = true;
  const btn = $("recordBtn");
  if (btn) btn.disabled = true;
  try {
    if (pendingKeep) await keepHeard("", null);
    firstSoundArmed = true;
    firstSoundMicDenied = false;
    const pods = await detectAirpods();
    if (!session() || session().status !== "active") {
      await beginDoor(pods ? "scout" : "listen", {
        stayOnboard: true,
        role: pods ? "scout" : "base",
      });
    } else if (pods && session().role !== "scout") {
      session().role = "scout";
      persist();
    }
    const s = session();
    if (s) s.firstSoundAt = s.firstSoundAt || Date.now();
    persist();
    const armed = await startMic({ firstSound: true });
    firstSoundMicDenied = Boolean(armed?.denied);
    if (firstSoundMicDenied) toast(FAILURE.micDenied);
    if (rec) startRecClock();
    refreshWeather();
    showOnboard();
    renderAll();
  } finally {
    recordBusy = false;
  }
}

async function stopRecord() {
  if (recordBusy) return;
  recordBusy = true;
  const btn = $("recordBtn");
  if (btn) btn.disabled = true;
  try {
    let audioId = null;
    let localOriginal = false;
    const started = recStarted;
    if (rec) {
      localOriginal = Boolean(rec.localOriginal);
      audioId = await stopMicToOriginal();
    }
    clearInterval(recTick);
    pendingKeep = {
      audioId,
      localOriginal,
      started,
      ended: Date.now(),
      weather: lastWeather,
      airpods: airpodsOn,
    };
    showOnboard();
  } finally {
    recordBusy = false;
  }
}

async function keepHeard(text, photoFile) {
  await saveFirstSound("heard", text, photoFile);
  pendingKeep = null;
  const box = $("whatText");
  const pic = $("whatPhoto");
  if (box) box.value = "";
  if (pic) pic.value = "";
  showOnboard();
}

async function beginFirstSound() {
  if (rec && firstSoundArmed) {
    if (showInstrument) openSheet("first-sound");
    else showOnboard();
    return;
  }
  await startRecord();
}

function setMapMode(mode) {
  const s = session();
  if (s) s.mapMode = mode;
  $("field").className = mode;
  $("mapmodes").querySelectorAll("button").forEach((b) => {
    b.classList.toggle("on", b.dataset.mode === mode);
  });
  captionForMode(mode);
  persist();
}

function showTab(name) {
  document.querySelectorAll(".tabs button").forEach((b) => {
    b.classList.toggle("on", b.dataset.tab === name);
  });
  $("library").style.display = name === "library" ? "block" : "none";
  $("broadcast").style.display = name === "broadcast" ? "block" : "none";
  if (name === "library") renderLibrary();
  if (name === "broadcast") renderBroadcast();
}

function renderField() {
  const s = session();
  const net = $("network");
  if (!s) {
    net.textContent = "● WAITING\nNO SESSION";
    net.classList.remove("warn");
  } else {
    const n = state.nodes.filter((x) => x.sessionId === s.id).length;
    const fading = s.startGpsQuality === "fading" || fix?.quality === "fading" || (!fix && s.startGpsQuality === "unknown");
    net.classList.toggle("warn", fading);
    net.innerHTML = fading
      ? `● GPS ${fix?.quality === "fading" ? "FADING" : "UNAVAILABLE"}<br>${n} LISTENER${n === 1 ? "" : "S"}`
      : `● FIELD READY<br>${n} LISTENER${n === 1 ? "" : "S"}`;
  }

  $("coh").textContent = COH_INSUFFICIENT.display;
  $("cohStatus").textContent = COH_INSUFFICIENT.status;
  $("needle").style.transform = `rotate(${heading || 0}deg)`;

  const start = s && s.startLat != null ? { lat: s.startLat, lon: s.startLon } : null;
  const you = fix && fix.lat != null ? { lat: fix.lat, lon: fix.lon } : start;
  const markers = $("markers");
  markers.innerHTML = "";
  const crumbs = $("crumbs");
  crumbs.innerHTML = "";
  crumbs.classList.toggle("return", Boolean(s?.returnActive));

  if (s && start) {
    const p0 = projectRelative(start, start) || { left: 22, top: 62 };
    markers.insertAdjacentHTML(
      "beforeend",
      `<button class="start" style="left:${p0.left}%;top:${p0.top}%"><i></i><b>START</b></button>`
    );
  }

  state.nodes
    .filter((n) => s && n.sessionId === s.id && n.lat != null)
    .forEach((n) => {
      const p = (start && projectRelative(start, n)) || { left: 58, top: 46 };
      markers.insertAdjacentHTML(
        "beforeend",
        `<button class="node ${n.role}" style="left:${p.left}%;top:${p.top}%"><i></i><b>${n.name}</b></button>`
      );
    });

  if (s && you && (!state.nodes.some((n) => n.id === state.deviceId && n.lat != null))) {
    const p = (start && projectRelative(start, you)) || { left: 58, top: 46 };
    const label = s.role === "base" ? "BASE · YOU" : s.role === "scout" ? "SCOUT · YOU" : "YOU";
    markers.insertAdjacentHTML(
      "beforeend",
      `<button class="node ${s.role}" style="left:${p.left}%;top:${p.top}%"><i></i><b>${label}</b></button>`
    );
  }

  sessionNotes().forEach((note) => {
    if (note.excluded || note.lat == null || !start) return;
    const p = projectRelative(start, note);
    if (!p) return;
    const mystery = note.kind === "mystery";
    markers.insertAdjacentHTML(
      "beforeend",
      `<button class="event ${mystery ? "unknown" : ""}" style="left:${p.left}%;top:${p.top}%"><i></i><span>${note.kind.toUpperCase()}</span></button>`
    );
  });

  const pts = sessionCrumbs();
  if (start && pts.length) {
    const d = pts
      .map((c, i) => {
        const p = projectRelative(start, c);
        if (!p) return "";
        return `${i ? "L" : "M"} ${p.left} ${p.top}`;
      })
      .join(" ");
    crumbs.innerHTML = `<path d="${d}" />`;
  }

  const live = $("livecard");
  const last = sessionEncounters().at(-1);
  const first = firstSoundEncounter();
  const shown = first && (!last || last.id === first.id || last.firstSound) ? first : last;
  live.classList.toggle("cta", Boolean(s && !shown && !rec && !s.returnActive));
  live.classList.toggle("rec", Boolean(rec && firstSoundArmed));
  live.classList.toggle("rain", Boolean((s && !shown && !rec && !s.returnActive) || (rec && firstSoundArmed)));
  if (!s) {
    live.classList.remove("cta", "rec", "rain");
    live.querySelector("b").textContent = "Start a session to listen";
    live.querySelectorAll("small")[0].textContent = "LIVE FIELD";
    live.querySelectorAll("small")[1].textContent = "Private by default.";
    $("liveMeta").innerHTML = "PRIVATE<br>ON DEVICE";
  } else if (rec && firstSoundArmed) {
    live.querySelectorAll("small")[0].textContent = "RECORDING";
    live.querySelector("b").textContent = "Listening";
    live.querySelectorAll("small")[1].textContent = rec.localOriginal
      ? "Local original being kept. Not a species. Not contributed."
      : "Original being kept on this phone. Not contributed.";
    $("liveMeta").innerHTML = "REC<br>ON PHONE";
  } else if (shown) {
    const isFirst = Boolean(shown.firstSound);
    live.querySelectorAll("small")[0].textContent = isFirst
      ? "FIRST SOUND · ON THIS PHONE"
      : shown.kind === "unknown"
        ? "UNKNOWN · BIOLOGICAL CANDIDATE"
        : "FIELD NOTE · NON-HUMAN";
    live.querySelector("b").textContent = shown.label;
    live.querySelectorAll("small")[1].textContent = isFirst
      ? shown.originalAudioId
        ? "Original preserved. Not contributed."
        : "Session kept. No original yet — microphone was off."
      : "Original kept on this phone.";
    $("liveMeta").innerHTML = shown.contributed ? "IN LIBRARY" : "NOT<br>CONTRIBUTED";
  } else if (s.returnActive && start && you) {
    const m = distanceM(you, start);
    const brg = bearingDeg(you, start);
    live.querySelectorAll("small")[0].textContent = "RETURN · SAFETY AID";
    live.querySelector("b").textContent = "Trail back to Session Start";
    live.querySelectorAll("small")[1].textContent =
      m != null ? `${Math.round(m)} m · not a map replacement` : "Highlighting your breadcrumb";
    $("liveMeta").innerHTML = brg != null ? `BEARING<br>${Math.round((brg + 360) % 360)}°` : "START";
  } else {
    live.querySelectorAll("small")[0].textContent = "LOCAL FIELD";
    live.querySelector("b").textContent = "Tap START on the field screen";
    live.querySelectorAll("small")[1].textContent =
      s.startGpsQuality === "fading" || fix?.quality === "fading"
        ? "GPS fading — original will still stay on this phone."
        : "Original stays on this phone. Not contributed.";
    $("liveMeta").innerHTML = "ON<br>PHONE";
  }
}

function renderLibrary() {
  const list = $("libraryList");
  const rows = state.library;
  if (!rows.length) {
    list.innerHTML = `<div class="signal"><small>PRIVATE SESSION LIBRARY IS SEPARATE</small><b>Nothing contributed yet</b><span>Sharing a card is not the same as sending the original.</span></div>`;
    return;
  }
  list.innerHTML = rows
    .map(
      (r) => `<div class="signal"><small>${r.coarseLabel} · ${r.provenance}</small><b>${r.label}</b><span>${r.summary}</span></div>`
    )
    .join("");
}

function renderBroadcast() {
  const s = session();
  const b = state.broadcasts.find((x) => x.sessionId === s?.id);
  $("bcastLive").textContent = b ? "● LIVE BROADCAST" : "○ BROADCAST READY";
  $("bcastTitle").textContent = b?.title || "No broadcast yet";
  const nodes = s ? state.nodes.filter((n) => n.sessionId === s.id).length : 0;
  $("bcastBody").innerHTML = `
    <div class="viewer"><b>${b ? `${b.watchers} watching` : "0 watching"}</b><small>Watching needs no microphone and no precise location.</small></div>
    <div class="viewer"><b>FIELD · ${nodes} node${nodes === 1 ? "" : "s"}</b><small>Human speech is excluded from wildlife encounters. Sensor contribution is opt-in.</small></div>
    <div class="viewer"><b>Invite ${s?.inviteCode || "—"}</b><small>Pair another Listener. Transport can change. The session stays on the phone if the link drops.</small></div>`;
}

function closeSheet() {
  $("overlay").classList.remove("show");
}

function openSheet(type) {
  const s = session();
  const sheet = $("sheet");
  const views = {
    session: () => `
      <small class="label">LISTENER SESSION</small>
      <h2>Start a Session</h2>
      <p>Every Listener keeps its own evidence. If the link drops we keep recording and sync when you're back.</p>
      <div class="choices">
        <button data-door="listen">⌂ HOME FIELD</button>
        <button data-door="scout">⌁ WANDER / SCOUT</button>
        <button data-door="broadcast">● BROADCAST</button>
        <button data-act="pair">＋ ADD STATION</button>
      </div>
      <button class="ghost" data-act="listen-now">START LISTENING</button>`,
    scout: () => `
      <small class="label">STUPIDLY EASY SETUP</small>
      <h2>Go Scout</h2>
      <p>Take this phone. Listener checks location, microphone and connected AirPods, starts your breadcrumb trail, and links to a Base when one is there.</p>
      <div class="choices" id="micChoices"></div>
      <p id="micActive">Active input will show here.</p>
      <button class="wide" data-act="wander">START WANDER</button>`,
    note: () => `
      <small class="label">FIELD NOTE · AUTO-STAMPED</small>
      <h2>What happened?</h2>
      <div class="choices">
        <button data-note="saw">👁 SAW IT</button>
        <button data-note="heard">👂 HEARD IT</button>
        <button data-note="photo">📷 PHOTO</button>
        <button data-note="video">🎞 VIDEO</button>
        <button data-note="mystery">❓ MYSTERY</button>
        <button data-note="human">🗣 HUMAN SPEECH</button>
      </div>
      <textarea id="noteText" rows="3" placeholder="Optional words from you — never a transcript of the recording."></textarea>
      <input id="noteFile" type="file" accept="image/*,video/*" style="display:none">
      <button class="wide" data-act="save-note">SAVE EVIDENCE</button>`,
    "first-sound": () => firstSoundHTML(),
    contribute: () => contributeHTML(),
    invite: () => `
      <small class="label">JOIN THE FIELD</small>
      <h2>Invite somebody</h2>
      <p>Watching requires no microphone or precise location. Joining as a node is a separate yes.</p>
      <p><b>Pair code ${s?.inviteCode || "—"}</b></p>
      <div class="choices">
        <button data-act="watch">👀 JUST WATCH</button>
        <button data-act="node">＋ JOIN AS NODE</button>
      </div>
      <button class="wide" data-act="copy-code">COPY PAIR CODE</button>`,
  };
  sheet.innerHTML = (views[type] || views.session)();
  $("overlay").classList.add("show");
  bindSheet(type);
}

function firstSoundHTML() {
  const denied = firstSoundMicDenied && !rec;
  const local = Boolean(rec?.localOriginal);
  return `
    <small class="label">FIRST SOUND · ON THIS PHONE</small>
    <h2>${denied ? "Microphone is off" : "Listening to this rain"}</h2>
    <p>${
      denied
        ? FAILURE.micDenied
        : local
          ? "A local original is being kept on this phone. Not a species. Not contributed."
          : "The original is being kept. This is not a species and it is not contributed. No invented animals. UNKNOWN stays UNKNOWN."
    }</p>
    <div class="choices">
      <button data-note="heard" class="on">👂 HEARD</button>
      <button data-note="mystery">❓ MYSTERY</button>
    </div>
    <textarea id="noteText" rows="3" placeholder="Your words — rain, or leave UNKNOWN."></textarea>
    ${denied ? `<button class="wide" data-act="first-sound-retry">TRY THE MICROPHONE AGAIN</button>` : ""}
    <button class="${denied ? "ghost" : "wide"}" data-act="save-first-sound">${denied ? "KEEP A FIELD NOTE" : "STOP AND KEEP"}</button>
    <button class="ghost" data-act="close">KEEP THE SESSION</button>`;
}

function contributeHTML() {
  const pending = sessionEncounters();
  if (!pending.length) {
    return `<small class="label">CONTRIBUTE · OPT-IN</small><h2>Send us your Listener signals.</h2><p>Nothing in this session is ready. Save a non-human field note first. Sharing a card later is a different button.</p><button class="wide" data-act="close">OK</button>`;
  }
  const options = pending
    .map((e) => `<button data-enc="${e.id}">${e.label}<br><small>${e.humanSpeechGate}</small></button>`)
    .join("");
  return `
    <small class="label">CONTRIBUTE · OPT-IN</small>
    <h2>Send us your Listener signals.</h2>
    <p>Only non-human biological evidence. Precise home, raw Wander routes, and private media stay here unless you change that.</p>
    <div class="choices">${options}</div>
    <p>Human-speech exclusion must be confirmed before the common library gets anything.</p>
    <button class="ghost" data-act="confirm-wild">THIS IS NOT HUMAN SPEECH</button>
    <div class="choices">
      <button data-flag="audio">✓ ORIGINAL AUDIO</button>
      <button data-flag="features">✓ SIGNAL FEATURES</button>
      <button data-flag="coarse">✓ COARSE LOCATION</button>
      <button data-flag="provenance">✓ PROVENANCE</button>
    </div>
    <button class="wide" data-act="contribute-now" disabled>CONTRIBUTE SAFELY</button>
    <button class="ghost" data-act="share-card">SHARE A CARD ONLY</button>`;
}

function bindSheet(type) {
  const sheet = $("sheet");
  let noteKind = type === "first-sound" ? "heard" : "mystery";
  let selectedEnc = sessionEncounters().at(-1)?.id || null;
  let flags = { audio: true, features: true, coarse: true, provenance: true };
  let wildOk = false;

  if (type === "scout") fillMics();

  sheet.onclick = async (ev) => {
    const t = ev.target.closest("button");
    if (!t) return;
    if (t.dataset.door) {
      closeSheet();
      await beginDoor(t.dataset.door);
      return;
    }
    if (t.dataset.note) {
      noteKind = t.dataset.note;
      sheet.querySelectorAll("[data-note]").forEach((b) => b.classList.toggle("on", b === t));
      if (noteKind === "photo" || noteKind === "video") $("noteFile").click();
      return;
    }
    if (t.dataset.enc) {
      selectedEnc = t.dataset.enc;
      sheet.querySelectorAll("[data-enc]").forEach((b) => b.classList.toggle("on", b === t));
      return;
    }
    if (t.dataset.flag) {
      flags[t.dataset.flag] = !flags[t.dataset.flag];
      t.classList.toggle("on");
      return;
    }
    const act = t.dataset.act;
    if (act === "close") closeSheet();
    if (act === "listen-now") {
      closeSheet();
      if (!session()) await beginDoor("listen");
    }
    if (act === "first-sound") {
      closeSheet();
      await beginFirstSound();
      return;
    }
    if (act === "first-sound-retry") {
      firstSoundMicDenied = false;
      const armed = await startMic({ firstSound: true });
      firstSoundMicDenied = Boolean(armed?.denied);
      if (firstSoundMicDenied) toast(FAILURE.micDenied);
      openSheet("first-sound");
      renderAll();
      return;
    }
    if (act === "save-first-sound") {
      await saveFirstSound(noteKind === "mystery" ? "mystery" : "heard", $("noteText")?.value || "");
      return;
    }
    if (act === "wander") {
      const s = session();
      if (s) s.role = "scout";
      closeSheet();
      await startMic();
      renderAll();
    }
    if (act === "save-note") await saveNote(noteKind, $("noteText")?.value || "");
    if (act === "pair" || act === "watch" || act === "node") {
      const s = session();
      if (act === "node" && s) {
        state.pairedDevices.push({ id: newId("dev"), role: "node", at: Date.now() });
        queue.enqueue("node.join", { sessionId: s.id, watchOnly: false });
      }
      if (act === "watch" && s) queue.enqueue("broadcast.watch", { sessionId: s.id });
      persist();
      closeSheet();
      renderAll();
    }
    if (act === "copy-code") {
      const s = session();
      if (s) navigator.clipboard?.writeText(s.inviteCode);
    }
    if (act === "confirm-wild") {
      const enc = state.encounters.find((e) => e.id === selectedEnc);
      if (!enc) return;
      const next = confirmNonHuman(enc);
      if (next.ok) {
        Object.assign(enc, next.encounter);
        wildOk = true;
        persist();
        const go = sheet.querySelector("[data-act=contribute-now]");
        if (go) go.disabled = !canContribute(enc).ok;
      } else {
        alert(next.reason);
      }
    }
    if (act === "contribute-now") await contributeSelected(selectedEnc, flags, wildOk);
    if (act === "share-card") shareCard(selectedEnc);
  };
}

async function fillMics() {
  const box = document.getElementById("micChoices");
  const line = document.getElementById("micActive");
  if (!box) return;
  let inputs = [];
  try {
    inputs = await listInputs();
  } catch {
    inputs = [];
  }
  const pref = pickPreferredInput(inputs);
  box.innerHTML = `
    <button data-mic="airpods">🎧 AIRPODS<br><small>${inputs.some((i) => i.airpods) ? "supported" : "use if supported"}</small></button>
    <button data-mic="phone" class="on">📱 IPHONE MIC<br><small>${pref.label}</small></button>`;
  if (line) line.textContent = `Active input · ${pref.label}`;
}

async function startMic(opts = {}) {
  const inputs = await listInputs().catch(() => []);
  const pref = pickPreferredInput(inputs);
  const first = Boolean(opts.firstSound);
  $("micLine").textContent = `MIC · ${pref.label.toUpperCase()} · ARMING`;
  $("micLine").classList.add("on");
  try {
    rec = await startRecording(pref.id);
    rec.localOriginal = false;
    recStarted = Date.now();
    $("micLine").textContent = `MIC · ${pref.label.toUpperCase()} · RECORDING · ORIGINAL PRESERVED`;
    return { ok: true, denied: false, local: false, input: pref };
  } catch (err) {
    const denied = isMicPermissionDenied(err);
    if (allowLocalOriginalFallback() || (!denied && isMicUnavailable(err))) {
      try {
        rec = await startLocalOriginalRecording();
        recStarted = Date.now();
        $("micLine").textContent = "MIC · LOCAL ORIGINAL · RECORDING · NOT A SPECIES";
        $("micLine").classList.add("on");
        return { ok: true, denied: false, local: true, input: { label: "local original" } };
      } catch {
        /* fall through to honest copy */
      }
    }
    if (denied) {
      $("micLine").textContent = "MIC · PERMISSION NEEDED · SESSION STILL HERE";
      $("micLine").classList.remove("on");
      return { ok: false, denied: true, local: false, input: pref };
    }
    $("micLine").textContent = "MIC · UNAVAILABLE · SESSION STILL HERE";
    $("micLine").classList.remove("on");
    return { ok: false, denied: false, local: false, input: pref };
  }
}

async function stopMicToOriginal() {
  if (!rec) return null;
  const blob = await rec.stop();
  rec = null;
  const id = newId("aud");
  putOriginal(id, blob, { mime: blob.type, startedAt: recStarted, bytes: blob.size });
  $("micLine").textContent = "MIC · IDLE · LAST ORIGINAL KEPT";
  $("micLine").classList.remove("on");
  return id;
}

async function saveNote(kind, text) {
  const s = session();
  if (!s) {
    closeSheet();
    await beginDoor("listen");
    return saveNote(kind, text);
  }
  const file = document.getElementById("noteFile")?.files?.[0];
  let mediaId = null;
  if (file) {
    mediaId = newId("med");
    putOriginal(mediaId, file, { mime: file.type, name: file.name, bytes: file.size });
  }
  let audioId = null;
  if (kind === "heard" && rec) audioId = await stopMicToOriginal();

  const note = {
    id: newId("note"),
    sessionId: s.id,
    t: Date.now(),
    kind: kind === "human" ? "heard" : kind,
    excluded: kind === "human",
    text,
    mediaId,
    lat: fix?.lat ?? s.startLat,
    lon: fix?.lon ?? s.startLon,
  };
  state.notes.push(note);

  let enc = emptyEncounter({
    sessionId: s.id,
    label: kind === "mystery" ? "UNKNOWN" : text.trim() || kind.toUpperCase(),
    kind: "unknown",
    provenance: "user",
    originalAudioId: audioId,
    lat: note.lat,
    lon: note.lon,
    contributingNodeIds: [state.deviceId],
  });
  const decision = processSignal({ probableHumanSpeech: kind === "human" });
  if (!decision.createEncounter) {
    enc = excludeProbableHuman(enc);
    state.exclusions = state.exclusions || [];
    state.exclusions.push({
      id: enc.id,
      t: Date.now(),
      internalLabel: decision.internalLabel,
      transcript: null,
      speakerId: null,
    });
    persist();
    closeSheet();
    toast("Probable human speech kept off the wildlife record.");
    renderAll();
    return;
  }
  enc = markUnknown(enc);
  enc.label = decision.label || enc.label;
  state.encounters.push(enc);
  queue.enqueue("note.add", { noteId: note.id, encounterId: enc.id });
  persist();
  closeSheet();
  renderAll();
}

async function saveFirstSound(kind, text, photoFile = null) {
  const s = session();
  if (!s) {
    await beginDoor(airpodsOn ? "scout" : "listen", {
      stayOnboard: true,
      role: airpodsOn ? "scout" : "base",
    });
    return saveFirstSound(kind, text, photoFile);
  }
  let audioId = pendingKeep?.audioId ?? null;
  let localOriginal = Boolean(pendingKeep?.localOriginal);
  if (rec) {
    localOriginal = Boolean(rec.localOriginal);
    audioId = await stopMicToOriginal();
  }
  let mediaId = null;
  if (photoFile) {
    mediaId = newId("med");
    putOriginal(mediaId, photoFile, { mime: photoFile.type, name: photoFile.name, bytes: photoFile.size });
  }
  const words = fieldNoteLabel(text);
  const decision = firstSoundDecision(text);
  const note = {
    id: newId("note"),
    sessionId: s.id,
    t: Date.now(),
    kind: kind === "mystery" ? "mystery" : "heard",
    excluded: false,
    text: String(text || "").trim(),
    mediaId,
    lat: fix?.lat ?? s.startLat,
    lon: fix?.lon ?? s.startLon,
    firstSound: true,
    weather: lastWeather || pendingKeep?.weather || null,
    durationMs: pendingKeep ? pendingKeep.ended - pendingKeep.started : null,
    sky: skyPeriod(),
    input: airpodsOn ? "airpods" : "phone",
    role: s.role,
  };
  state.notes.push(note);

  let enc = emptyEncounter({
    sessionId: s.id,
    label: decision.label || words,
    kind: "unknown",
    provenance: "user",
    originalAudioId: audioId,
    lat: note.lat,
    lon: note.lon,
    contributingNodeIds: [state.deviceId],
    firstSound: true,
  });
  enc = markUnknown(enc);
  enc.label = decision.label || words;
  enc.firstSound = true;
  enc.contributed = false;
  enc.shared = false;
  enc.humanSpeechGate = "pending";
  enc.localOriginal = localOriginal;
  enc.weather = note.weather;
  enc.sky = note.sky;
  enc.durationMs = note.durationMs;
  enc.mediaId = mediaId;
  enc.role = s.role;
  state.encounters.push(enc);
  firstSoundArmed = false;
  firstSoundMicDenied = false;
  queue.enqueue("note.add", { noteId: note.id, encounterId: enc.id, firstSound: true });
  persist();
  closeSheet();
  if (ownerEndpoints().search) {
    indexOwnerSearch({
      encounterId: enc.id,
      label: enc.label,
      t: enc.t,
      weather: enc.weather,
      sky: enc.sky,
      role: enc.role,
      hasOriginal: Boolean(audioId),
      hasPhoto: Boolean(mediaId),
    }).catch(() => {});
  }
  toast(
    audioId
      ? "Kept on this phone. Original preserved. Not sent anywhere unless your search is connected."
      : "Session is still here. No original yet — this phone needs the microphone."
  );
  renderAll();
  renderHeard();
}

async function contributeSelected(id, flags) {
  const enc = state.encounters.find((e) => e.id === id);
  const gate = canContribute(enc);
  if (!gate.ok) {
    alert(gate.reason);
    return;
  }
  const coarse = flags.coarse ? coarseLocation(enc.lat, enc.lon) : null;
  const row = {
    id: newId("lib"),
    encounterId: enc.id,
    label: enc.label,
    provenance: enc.provenance,
    coarse,
    coarseLabel: coarse ? `${coarse.lat}, ${coarse.lon}` : "LOCATION HELD",
    summary: "Listener contribution · original stays referenced · not a species claim",
    includeAudio: Boolean(flags.audio && enc.originalAudioId),
    includeFeatures: Boolean(flags.features),
    sharedPublic: false,
  };
  enc.contributed = true;
  state.library.push(row);
  queue.enqueue("library.contribute", { libraryId: row.id });
  persist();
  closeSheet();
  showTab("library");
  renderAll();
}

function shareCard(id) {
  const enc = state.encounters.find((e) => e.id === id);
  if (!enc) return;
  enc.shared = true;
  state.cards.push({
    id: newId("card"),
    encounterId: enc.id,
    contributed: false,
    shared: true,
  });
  persist();
  closeSheet();
  alert("Card ready to share. The original was not sent to the library.");
}

function toggleReturn() {
  const s = session();
  if (!s) return;
  s.returnActive = !s.returnActive;
  persist();
  renderField();
}

function renderAll() {
  renderField();
  renderLibrary();
  renderBroadcast();
}

$("overlay").addEventListener("click", (e) => {
  if (e.target === $("overlay")) closeSheet();
});
document.querySelectorAll(".tabs button").forEach((b) => {
  b.onclick = () => showTab(b.dataset.tab);
});
$("mapmodes").querySelectorAll("button").forEach((b) => {
  b.onclick = () => setMapMode(b.dataset.mode);
});
$("btnSession").onclick = () => openSheet("session");
$("btnNote").onclick = () => openSheet("note");
$("btnReturn").onclick = toggleReturn;
$("btnScout").onclick = async () => {
  if (!session()) await beginDoor("scout");
  else openSheet("scout");
};
$("btnContribute").onclick = () => openSheet("contribute");
$("btnInvite").onclick = () => openSheet("invite");
$("livecard").onclick = () => {
  if (rec && firstSoundArmed) {
    openSheet("first-sound");
    return;
  }
  if (!firstSoundEncounter()) beginFirstSound();
};
$("livecard").addEventListener("keydown", (ev) => {
  if (ev.key === "Enter" || ev.key === " ") {
    ev.preventDefault();
    $("livecard").click();
  }
});

window.addEventListener("beforeunload", persist);

function markField(ev) {
  const s = session();
  if (!s || s.status !== "active") return;
  if (ev.target.closest("button")) return;
  const rect = $("field").getBoundingClientRect();
  const left = ((ev.clientX - rect.left) / rect.width) * 100;
  const top = ((ev.clientY - rect.top) / rect.height) * 100;
  const origin = { lat: s.startLat ?? 0, lon: s.startLon ?? 0 };
  const pt = unprojectTap(origin, left, top);
  state.breadcrumbs.push({
    id: newId("bc"),
    sessionId: s.id,
    t: Date.now(),
    lat: pt.lat,
    lon: pt.lon,
    accuracy: null,
    heading,
    quality: fix ? fix.quality : "unknown",
    source: fix ? "gps-tap" : "manual",
  });
  persist();
  renderField();
}

$("field").addEventListener("click", markField);

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}

if (new URLSearchParams(location.search).has("paired") && !state.pairedDevices.length) {
  state.pairedDevices.push({ id: "paired-local", role: "base", at: Date.now() });
}

flushQueue(queue, transport).then((res) => {
  if (res && res.ok === false) toast(FAILURE.scoutLost);
}).catch(() => toast(FAILURE.scoutLost));

hydrate().then((next) => {
  Object.assign(state, rememberDevice(next));
  showOnboard();
  renderAll();
  captionForMode(session()?.mapMode || "field");
  ensureGeo();
  refreshWeather();
});
showOnboard();
renderAll();
ensureGeo();
refreshWeather();
setInterval(applySky, 30000);
