/**
 * Domain Architect homepage — ChatVault is the site search engine.
 * Same origin as /chatvault/ so the vault localStorage is shared.
 */

import {
  createStore,
  exportVault,
  importVault,
  ingestPaste,
  searchVault,
} from "/chatvault/js/engine.mjs";
import { ingestNamedSource } from "/chatvault/js/drain.mjs";

const STORAGE_KEY = "chatvault.engine.v1";
const DOCK_KEY = "da.cvdock.v1";
const MODE_KEY = "da.cvsearch.v1";

function loadEntries() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (parsed.format === "chatvault-export") return importVault(parsed);
    if (Array.isArray(parsed)) return parsed;
  } catch {
    /* empty vault on this device */
  }
  return [];
}

function persist(entries) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(exportVault(entries)));
}

const store = createStore(loadEntries());
store.subscribe((entries) => {
  try {
    persist(entries);
  } catch {
    setStatus("Browser storage is full. Open ChatVault and export JSON.");
  }
});

const qEl = document.getElementById("cv-q");
const hitsEl = document.getElementById("cv-hits");
const statusEl = document.getElementById("cv-status");
const dropEl = document.getElementById("cv-drop");
const posEl = document.getElementById("cv-dock-pos");
const modeEl = document.getElementById("cv-mode");
const snipEl = document.getElementById("cv-snip");
const outEl = document.getElementById("da-out");

function setStatus(text) {
  if (statusEl) statusEl.textContent = text || "";
}

function chatvaultUrl(query, hash) {
  const url = new URL("/chatvault/", location.origin);
  if (query) url.searchParams.set("q", query);
  if (hash) url.hash = hash;
  return url.href;
}

function currentMode() {
  return modeEl?.value === "here" ? "here" : "open";
}

function applyDock(pos) {
  const next = pos === "bottom" ? "bottom" : "top-right";
  document.body.dataset.dock = next;
  if (posEl) posEl.value = next;
  try {
    localStorage.setItem(DOCK_KEY, next);
  } catch {
    /* ignore */
  }
}

function applyMode(mode) {
  const next = mode === "here" ? "here" : "open";
  if (modeEl) modeEl.value = next;
  try {
    localStorage.setItem(MODE_KEY, next);
  } catch {
    /* ignore */
  }
}

function renderHits(query) {
  const ranked = searchVault(store.list(), query);
  hitsEl.hidden = false;
  if (!ranked.hits.length) {
    hitsEl.innerHTML = `<p class="hint">No vault hits on this device. Use Open app, or drop a file. Fixtures load the first time you open ChatVault.</p>`;
    return;
  }
  hitsEl.innerHTML = ranked.hits
    .slice(0, 8)
    .map((hit) => {
      const e = hit.entry;
      const origin = e.origin_class === "ai_generated" ? "AI" : "Real";
      return `<a class="cv-hit" href="${chatvaultUrl("", `detail/${e.id}`)}"><strong>${escapeHtml(e.title)}</strong><br/><span class="hint">${escapeHtml(origin)} · ${escapeHtml(e.source_ai)} · score ${hit.score.toFixed(2)}</span></a>`;
    })
    .join("");
}

function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function runSearch(openApp) {
  const q = String(qEl?.value || "").trim();
  if (openApp || currentMode() === "open") {
    location.href = chatvaultUrl(q);
    return;
  }
  if (!q) {
    setStatus("Type something to search, or open ChatVault.");
    return;
  }
  renderHits(q);
}

async function ingestFiles(fileList) {
  const files = [...fileList];
  const results = [];
  for (const file of files) {
    const mime = file.type || "";
    let payload;
    if (mime.startsWith("image/") && file.size <= 12 * 1024 * 1024) {
      payload = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve({ dataUrl: String(reader.result || ""), mime, size: file.size });
        reader.onerror = () => reject(reader.error || new Error("read failed"));
        reader.readAsDataURL(file);
      });
    } else if (mime.startsWith("video/") || mime.startsWith("audio/") || mime === "application/pdf") {
      payload = { mime, size: file.size };
    } else {
      const text = await file.text();
      payload = { text, mime, size: file.size };
    }
    results.push(ingestNamedSource(file.name, payload, { visibility: "professional" }));
  }
  const entries = results.flatMap((r) => r.entries || []);
  if (!entries.length) throw new Error("Nothing ingestible.");
  store.addMany(entries);
  setStatus(`Indexed ${entries.length} record(s) into ChatVault.`);
}

document.getElementById("cv-search-form")?.addEventListener("submit", (ev) => {
  ev.preventDefault();
  runSearch(false);
});
document.getElementById("cv-open")?.addEventListener("click", () => runSearch(true));
document.getElementById("cv-web")?.addEventListener("click", () => {
  const q = String(qEl?.value || "").trim() || "ChatVault OS for your AI";
  window.open(`https://duckduckgo.com/?q=${encodeURIComponent(q)}`, "_blank", "noopener");
});
posEl?.addEventListener("change", () => applyDock(posEl.value));
modeEl?.addEventListener("change", () => applyMode(modeEl.value));

document.getElementById("cv-ingest")?.addEventListener("click", () => {
  try {
    const text = String(snipEl?.value || "");
    const entry = ingestPaste(text, {
      source_ai: "human",
      origin_class: "human_record",
      source_type: "letter",
    });
    store.add(entry);
    snipEl.value = "";
    setStatus(`Indexed “${entry.title}”. Open ChatVault to review.`);
  } catch (err) {
    setStatus(err.message || String(err));
  }
});

document.getElementById("cv-files")?.addEventListener("change", (ev) => {
  if (!ev.target.files?.length) return;
  ingestFiles(ev.target.files).catch((err) => setStatus(err.message || String(err)));
});

["dragover", "dragleave", "drop"].forEach((type) => {
  dropEl?.addEventListener(type, (ev) => {
    ev.preventDefault();
    if (type === "dragover") dropEl.classList.add("drag");
    else dropEl.classList.remove("drag");
    if (type === "drop" && ev.dataTransfer?.files?.length) {
      ingestFiles(ev.dataTransfer.files).catch((err) => setStatus(err.message || String(err)));
    }
  });
});

async function audit(expression, drain) {
  outEl.textContent = "Auditing…";
  const path = drain ? "/api/drain/queue" : "/api/audit";
  const res = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || res.statusText);
  if (drain && data.format === "chatvault-export") {
    const entries = importVault(data);
    if (entries.length) store.addMany(entries);
    outEl.textContent = `Drained ${entries.length} audit(s) into ChatVault.\n\n${entries[0]?.summary || ""}`;
    return;
  }
  outEl.textContent = data.narrative || JSON.stringify(data, null, 2);
}

document.getElementById("da-audit")?.addEventListener("click", () => {
  const expression = document.getElementById("da-expr")?.value || "";
  audit(expression, false).catch((err) => {
    outEl.textContent = `${err.message}\n\nStart the site: python -m domain_architect --site`;
  });
});
document.getElementById("da-drain")?.addEventListener("click", () => {
  const expression = document.getElementById("da-expr")?.value || "";
  audit(expression, true).catch((err) => {
    outEl.textContent = `${err.message}\n\nStart the site: python -m domain_architect --site`;
  });
});

try {
  applyDock(localStorage.getItem(DOCK_KEY) || "top-right");
  applyMode(localStorage.getItem(MODE_KEY) || "open");
} catch {
  applyDock("top-right");
  applyMode("open");
}

if (!store.list().length) {
  setStatus("Vault is empty on this device. Drop a file here, or open ChatVault (demo fixtures load there).");
}
