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
import { ingestNamedSource, classifyFilename, ingestNoticeForResults, loadInboxFromRepo, postInboxExport } from "/chatvault/js/drain.mjs";
import {
  defaultSearchMode,
  deepDiveLinks,
  filedHuntPayload,
  filedSearchPayload,
  parseShareTarget,
  shareIngestOverrides,
  snippetIngestOverrides,
} from "./da-search.mjs";

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
const diveEl = document.getElementById("cv-web-dive");
const installBtn = document.getElementById("cv-install");
const sourceTypeEl = document.getElementById("cv-source-type");

let deferredInstall = null;
let lastFiled = [];

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
  return modeEl?.value === "open" ? "open" : "here";
}

function isStandalone() {
  return (
    window.matchMedia("(display-mode: standalone)").matches ||
    window.navigator.standalone === true
  );
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
  const next = mode === "open" ? "open" : "here";
  if (modeEl) modeEl.value = next;
  try {
    localStorage.setItem(MODE_KEY, next);
  } catch {
    /* ignore */
  }
}

function selectedOrigin() {
  const checked = document.querySelector('input[name="cv-origin"]:checked');
  return checked?.value === "ai_generated" ? "ai_generated" : "human_record";
}

function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderHits(query) {
  const ranked = searchVault(store.list(), query);
  hitsEl.hidden = false;
  if (!ranked.hits.length) {
    hitsEl.innerHTML = `<p class="hint">No vault hits on this device. File a snippet below, or open ChatVault (demo fixtures load there). Vault is local — the web is a hunt in a new tab.</p>`;
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

function renderDeepDive(query) {
  if (!diveEl) return;
  const links = deepDiveLinks(query);
  diveEl.hidden = false;
  diveEl.innerHTML = `
    <p class="cv-dive-kicker">Deep dive on the web</p>
    <p class="hint">Vault is local. These open a hunt in a new tab — ChatVault does not crawl or index the internet.</p>
    <div class="cv-actions">
      ${links
        .map(
          (link) =>
            `<a class="ghost" href="${escapeHtml(link.href)}" target="_blank" rel="noopener">${escapeHtml(link.label)}</a>`
        )
        .join("")}
      <button type="button" class="ghost" id="cv-file-hunt">File this hunt</button>
    </div>
  `;
  document.getElementById("cv-file-hunt")?.addEventListener("click", () => fileHunt(query));
}

function runSearch(openApp) {
  const q = String(qEl?.value || "").trim();
  if (openApp) {
    location.href = chatvaultUrl(q);
    return;
  }
  if (currentMode() === "open") {
    location.href = chatvaultUrl(q);
    return;
  }
  if (!q) {
    setStatus("Type something to search, or open ChatVault.");
    return;
  }
  renderHits(q);
  renderDeepDive(q);
}

function runDeepDive() {
  const q = String(qEl?.value || "").trim();
  if (!q) {
    setStatus("Type a query for a deep dive. Vault is local; web hunts open in a new tab.");
    renderDeepDive("");
    return;
  }
  renderHits(q);
  renderDeepDive(q);
}

function indexSnippet(raw, overrides) {
  const entry = ingestPaste(raw, overrides);
  store.add(entry);
  lastFiled = [entry];
  return entry;
}

function fileThisSearch() {
  try {
    const q = String(qEl?.value || "").trim();
    const payload = filedSearchPayload(q);
    const entry = indexSnippet(payload.raw, payload.overrides);
    setStatus(`Filed “${entry.title}” as a human record.`);
    if (currentMode() === "here") {
      renderHits(q);
      renderDeepDive(q);
    }
  } catch (err) {
    setStatus(err.message || String(err));
  }
}

function fileHunt(query) {
  try {
    const q = String(query || qEl?.value || "").trim();
    const payload = filedHuntPayload(q);
    const entry = indexSnippet(payload.raw, payload.overrides);
    setStatus(`Filed “${entry.title}”. URLs only — not a web crawl.`);
    if (currentMode() === "here") {
      renderHits(q);
      renderDeepDive(q);
    }
  } catch (err) {
    setStatus(err.message || String(err));
  }
}

function captureSnippet() {
  try {
    const text = String(snipEl?.value || "");
    const entry = indexSnippet(
      text,
      snippetIngestOverrides({
        originClass: selectedOrigin(),
        sourceType: sourceTypeEl?.value,
      })
    );
    snipEl.value = "";
    setStatus(`Indexed “${entry.title}”. Open ChatVault to review.`);
  } catch (err) {
    setStatus(err.message || String(err));
  }
}

async function ingestFiles(fileList) {
  const files = [...fileList];
  const results = [];
  for (const file of files) {
    const mime = file.type || "";
    const kind = classifyFilename(file.name, mime);
    let payload;
    if (kind === "picture" && file.size <= 12 * 1024 * 1024) {
      payload = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve({ dataUrl: String(reader.result || ""), mime, size: file.size });
        reader.onerror = () => reject(reader.error || new Error("read failed"));
        reader.readAsDataURL(file);
      });
    } else if (kind === "picture" || kind === "movie" || kind === "audio" || kind === "pdf" || kind === "docx") {
      payload = { mime, size: file.size };
    } else {
      const text = await file.text();
      payload = { text, mime, size: file.size };
    }
    results.push(
      ingestNamedSource(file.name, payload, {
        visibility: "professional",
        origin_class: selectedOrigin(),
      })
    );
  }
  const entries = results.flatMap((r) => r.entries || []);
  if (!entries.length) throw new Error("Nothing ingestible.");
  store.addMany(entries);
  lastFiled = entries;
  setStatus(ingestNoticeForResults(results, { fileCount: files.length }));
}

function registerDaServiceWorker() {
  if (!("serviceWorker" in navigator)) return;
  if (location.protocol !== "http:" && location.protocol !== "https:") return;
  navigator.serviceWorker.register("/da-sw.js", { scope: "/" }).catch(() => {});
}

function setupInstall() {
  if (!installBtn) return;
  if (isStandalone()) {
    installBtn.hidden = true;
    return;
  }
  window.addEventListener("beforeinstallprompt", (ev) => {
    ev.preventDefault();
    if (isStandalone()) return;
    deferredInstall = ev;
    installBtn.hidden = false;
  });
  window.addEventListener("appinstalled", () => {
    deferredInstall = null;
    installBtn.hidden = true;
  });
  installBtn.addEventListener("click", async () => {
    if (!deferredInstall) return;
    deferredInstall.prompt();
    try {
      await deferredInstall.userChoice;
    } catch {
      /* user dismissed */
    }
    deferredInstall = null;
    installBtn.hidden = true;
  });
}

function consumeShareTarget() {
  const share = parseShareTarget(new URLSearchParams(location.search));
  if (!share.snippet) return;
  if (snipEl) snipEl.value = share.snippet;
  try {
    const entry = indexSnippet(share.snippet, shareIngestOverrides(share));
    setStatus(`Shared “${entry.title}” into ChatVault as a human record. Not a conversation dump.`);
  } catch (err) {
    setStatus(err.message || String(err));
  }
  try {
    const clean = new URL(location.href);
    clean.searchParams.delete("title");
    clean.searchParams.delete("text");
    clean.searchParams.delete("url");
    history.replaceState({}, "", `${clean.pathname}${clean.search}${clean.hash}`);
  } catch {
    /* ignore */
  }
}

document.getElementById("cv-search-form")?.addEventListener("submit", (ev) => {
  ev.preventDefault();
  runSearch(false);
});
document.getElementById("cv-open")?.addEventListener("click", () => runSearch(true));
document.getElementById("cv-web")?.addEventListener("click", () => runDeepDive());
document.getElementById("cv-file-search")?.addEventListener("click", () => fileThisSearch());
posEl?.addEventListener("change", () => applyDock(posEl.value));
modeEl?.addEventListener("change", () => applyMode(modeEl.value));

document.getElementById("cv-ingest")?.addEventListener("click", () => captureSnippet());
snipEl?.addEventListener("keydown", (ev) => {
  if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
    ev.preventDefault();
    captureSnippet();
  }
});

document.getElementById("cv-files")?.addEventListener("change", (ev) => {
  if (!ev.target.files?.length) return;
  ingestFiles(ev.target.files).catch((err) => setStatus(err.message || String(err)));
});

document.getElementById("cv-inbox")?.addEventListener("click", () => {
  loadInboxFromRepo()
    .then((result) => {
      if (!result.entries.length) {
        setStatus(`Inbox at ${result.origin} had no sidecars. Run python3 -m domain_architect --ingest-chatvault PATH.`);
        return;
      }
      store.addMany(result.entries);
      lastFiled = result.entries;
      setStatus(`Loaded ${result.entries.length} inbox record(s) from ${result.origin}.`);
    })
    .catch((err) => setStatus(err.message || String(err)));
});

document.getElementById("cv-send-repo")?.addEventListener("click", () => {
  const payload = lastFiled.length ? exportVault(lastFiled) : null;
  if (!payload) {
    setStatus("Index a file or snippet first, then send the JSON sidecar to the repo inbox.");
    return;
  }
  postInboxExport(payload)
    .then((result) => {
      setStatus(`Wrote ${result.count || 0} sidecar(s) to the repo inbox. Large media is not uploaded; use CLI --ingest-chatvault.`);
    })
    .catch((err) => setStatus(err.message || String(err)));
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
    outEl.textContent = `${err.message}\n\nStart the site: python3 -m domain_architect --site`;
  });
});
document.getElementById("da-drain")?.addEventListener("click", () => {
  const expression = document.getElementById("da-expr")?.value || "";
  audit(expression, true).catch((err) => {
    outEl.textContent = `${err.message}\n\nStart the site: python3 -m domain_architect --site`;
  });
});

try {
  applyDock(localStorage.getItem(DOCK_KEY) || "top-right");
  let stored = null;
  try {
    stored = localStorage.getItem(MODE_KEY);
  } catch {
    stored = null;
  }
  applyMode(defaultSearchMode({ stored, standalone: isStandalone() }));
} catch {
  applyDock("top-right");
  applyMode("here");
}

registerDaServiceWorker();
setupInstall();
consumeShareTarget();

if (!store.list().length) {
  setStatus("Vault is empty on this device. Paste a snippet, drop a file, or open ChatVault (demo fixtures load there).");
}
