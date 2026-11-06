import {
  DEMO_ENTRIES,
  SCHEMA_VERSION,
  LEDGER_STATUSES,
  SOURCE_AIS,
  ingestPaste,
  searchVault,
  exportVault,
  importVault,
  reviewLedgerItem,
  attachLocator,
  createStore,
} from "./engine.mjs";
import { LOCATOR_KINDS, makeLocator } from "./locators.mjs";
import { SEARCH_ENGINE_VERSION, ndcgAt } from "./search.mjs";
import { layoutConstellation } from "./atlas.mjs";
import { SKINS, SKIN_IDS, loadSkin, saveSkin, applySkin } from "./skins.mjs";
import { ledgerSpectrum } from "./spectrum.mjs";

const STORAGE_KEY = "chatvault.engine.v1";
const PAGE_SIZE = 50;
const root = document.getElementById("app");

function loadPersisted() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEMO_ENTRIES;
    const parsed = JSON.parse(raw);
    if (parsed.format === "chatvault-export") return importVault(parsed);
    if (Array.isArray(parsed)) return parsed;
  } catch {
    /* fall through to demo */
  }
  return DEMO_ENTRIES;
}

const store = createStore(loadPersisted());
store.subscribe((entries) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(exportVault(entries)));
  } catch {
    /* quota */
  }
});

const state = {
  view: "vault",
  query: "",
  visibility: "",
  source_ai: "",
  selectedId: null,
  notice: "",
  error: "",
  ingestText: "",
  locatorValue: "",
  locatorKind: "auto",
  attachValue: "",
  attachKind: "auto",
  page: 0,
  fatal: null,
  skin: applySkin(loadSkin()),
};

function set(patch) {
  Object.assign(state, patch);
  render();
}

function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function nav(id, label) {
  const current = state.view === id ? ' aria-current="page"' : "";
  return `<button class="nav-btn" data-view="${id}"${current}>${label}</button>`;
}

function skinSwitcher() {
  return `<div class="skins" role="group" aria-label="Skins">
    ${SKIN_IDS.map((id) => {
      const skin = SKINS[id];
      const pressed = state.skin === id ? "true" : "false";
      return `<button type="button" class="skin-swatch" data-set-skin="${id}" data-skin="${id}" aria-pressed="${pressed}" title="${escapeHtml(skin.label)} — ${escapeHtml(skin.blurb)}"></button>`;
    }).join("")}
  </div>`;
}

function renderSpectrum() {
  const spec = ledgerSpectrum(store.list());
  if (!spec.total) return "";
  const track = spec.bands
    .map(
      (b) =>
        `<span class="spectrum-band ${escapeHtml(b.status.toLowerCase())}" style="flex:${b.count}" title="${escapeHtml(b.status)} ${b.count}"></span>`
    )
    .join("");
  const mix = spec.bands.map((b) => `${b.status} ${b.count}`).join(" · ");
  return `<div class="spectrum">
    <div class="spectrum-track">${track}</div>
    <p class="caption">${escapeHtml(mix)}. ${escapeHtml(spec.caption)}</p>
  </div>`;
}

function ranked() {
  return searchVault(store.list(), state.query, {
    visibility: state.visibility || undefined,
    source_ai: state.source_ai || undefined,
  });
}

function renderSky(layout, matchIds) {
  const active = matchIds ? new Set(matchIds) : null;
  const nodeById = new Map(layout.nodes.map((n) => [n.id, n]));
  const lines = layout.edges
    .map((edge) => {
      const a = nodeById.get(edge.from);
      const b = nodeById.get(edge.to);
      if (!a || !b) return "";
      const on = !active || (active.has(a.id) && active.has(b.id));
      return `<line class="link${on ? "" : " dim"}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" />`;
    })
    .join("");
  const hubs = layout.hubs
    .map(
      (h) =>
        `<text class="hub" x="${h.x}" y="${h.y - 42}">${escapeHtml(h.cluster)}</text>`
    )
    .join("");
  const stars = layout.nodes
    .map((n) => {
      const on = !active || active.has(n.id);
      const klass = `star ${escapeHtml(n.visibility)}${on ? "" : " dim"}`;
      return `<g class="${klass}" data-open="${escapeHtml(n.id)}">
        <circle cx="${n.x}" cy="${n.y}" r="${n.r}" />
        <text x="${n.x}" y="${n.y + n.r + 12}">${escapeHtml(n.title.slice(0, 28))}</text>
      </g>`;
    })
    .join("");
  return `<svg class="sky" viewBox="0 0 ${layout.width} ${layout.height}" role="img" aria-label="Vault constellation">
    ${lines}${hubs}${stars}
  </svg>`;
}

function renderBeams(hits, querying) {
  if (!hits.length) {
    return `<p class="empty">No matching records. An empty vault is different from a failed load — this search simply matched nothing.</p>`;
  }
  return hits
    .map((h, i) => {
      const snip = h.snippets?.[0]?.text || (h.entry.summary || h.entry.content_text || "").slice(0, 160);
      const why = (h.matched_fields || []).join(" · ") || (querying ? "ranked" : h.entry.project_category || "unfiled");
      const score = querying ? h.score.toFixed(1) : "—";
      return `<article class="beam" data-open="${escapeHtml(h.entry.id)}">
        <div class="beam-meta">
          <span class="rank">${i + 1}</span>
          <span class="score">${score}</span>
        </div>
        <h3>${escapeHtml(h.entry.title)}</h3>
        <p class="why">${escapeHtml(why)} · ${escapeHtml(h.entry.source_ai)}</p>
        <p>${escapeHtml(snip)}</p>
      </article>`;
    })
    .join("");
}

function renderVault() {
  const result = ranked();
  const emptyVault = store.list().length === 0;
  const querying = Boolean(state.query.trim());
  const pageCount = Math.max(1, Math.ceil(result.hits.length / PAGE_SIZE));
  if (state.page >= pageCount) state.page = pageCount - 1;
  const pageHits = result.hits.slice(state.page * PAGE_SIZE, (state.page + 1) * PAGE_SIZE);
  const matchIds = querying ? pageHits.map((h) => h.entry.id) : null;
  const layout = layoutConstellation(store.list());
  const pager =
    result.hits.length > PAGE_SIZE
      ? `<p class="pager">
          <button class="btn ghost" id="page-prev" ${state.page === 0 ? "disabled" : ""}>Previous</button>
          <span class="meta">Page ${state.page + 1} of ${pageCount} · ${result.hits.length} matches</span>
          <button class="btn ghost" id="page-next" ${state.page >= pageCount - 1 ? "disabled" : ""}>Next</button>
        </p>`
      : "";

  const stage = emptyVault
    ? `<p class="empty">Vault is empty on this device (not a failed load). <button class="btn ghost" id="load-demo">Load example fixtures</button></p>`
    : `<div class="atlas-stage">
        <div class="sky-wrap">${renderSky(layout, matchIds)}</div>
        <div class="beams">
          <p class="meta">${querying ? `${result.hits.length} ranked · ${result.took_ms.toFixed(1)} ms · ${escapeHtml(SEARCH_ENGINE_VERSION)}` : `${result.hits.length} of ${store.list().length} in the sky. Type a query to rank.`}</p>
          ${renderBeams(pageHits, querying)}
          ${pager}
        </div>
      </div>`;

  return `
    <header class="hero">
      <h1>Atlas</h1>
      <p class="kicker">OS for your AI · not a notebook</p>
      <p class="meta">${store.list().length} records · engine ${escapeHtml(SCHEMA_VERSION)} · ranker ${escapeHtml(SEARCH_ENGINE_VERSION)}</p>
      <p class="banner">Stars are records. Size is claims + theorems + gaps. Lines are shared tags. Search is a ranked beam (BM25F + 3-grams + cosine, fused). Ledger status is never a score.</p>
      ${renderSpectrum()}
    </header>
    <div class="toolbar">
      <input type="search" id="q" placeholder='claim:  gap:  address:  "phrase"  OR  ai:Grok' value="${escapeHtml(state.query)}" />
      <button class="btn ghost" id="do-search">Rank</button>
      <button class="btn" data-view="ingest">+ Ingest</button>
    </div>
    <div class="filters">
      <select id="vis">
        <option value="">Visibility: all</option>
        <option value="professional"${state.visibility === "professional" ? " selected" : ""}>professional</option>
        <option value="private"${state.visibility === "private" ? " selected" : ""}>private</option>
      </select>
      <select id="ai">
        <option value="">Source AI: all</option>
        ${SOURCE_AIS.map((a) => `<option${state.source_ai === a ? " selected" : ""}>${a}</option>`).join("")}
      </select>
    </div>
    <p class="error">${escapeHtml(state.error)}</p>
    <p class="notice">${escapeHtml(state.notice)}</p>
    ${stage}
  `;
}

function ledgerList(entry, field) {
  const items = entry[field] || [];
  if (!items.length) return `<p class="meta">None recorded. Absence is explicit.</p>`;
  return `<ul class="ledger">${items
    .map(
      (item) => `<li>
        <code>${escapeHtml(item.status)}</code> — ${escapeHtml(item.text)}
        <select data-review="${field}:${item.id}">
          ${LEDGER_STATUSES.map((s) => `<option${item.status === s ? " selected" : ""}>${s}</option>`).join("")}
        </select>
      </li>`
    )
    .join("")}</ul>`;
}

function renderDetail(entry) {
  if (!entry) {
    return `<p class="empty">That record is gone. If a delete failed, it would still be listed in the vault.</p>`;
  }
  return `
    <p><button class="btn ghost" data-view="vault">← Back to vault</button></p>
    <header class="hero">
      <h1>${escapeHtml(entry.title)}</h1>
      <p class="kicker">${escapeHtml(entry.source_ai)} · ${escapeHtml(entry.source_type)}</p>
    </header>
    <div class="detail">
      <div class="panel">
        <h3>Raw content (immutable)</h3>
        <pre class="raw">${escapeHtml(entry.raw_content)}</pre>
        <h3>Optional summary</h3>
        <p>${escapeHtml(entry.summary || "—")}</p>
      </div>
      <div class="panel">
        <p><span class="badge ${entry.visibility}">${escapeHtml(entry.visibility)}</span>
           <span class="badge">${escapeHtml(entry.source_file || "no address")}</span></p>
        <p class="meta">Ingested ${escapeHtml(entry.ingested_at)} · item date ${escapeHtml(entry.item_date)}</p>
        <h3>Addresses</h3>
        ${
          (entry.locators || []).length
            ? `<ul class="locators">${(entry.locators || [])
                .map(
                  (l) =>
                    `<li><code>${escapeHtml(l.code)}</code> · ${escapeHtml(l.kind)} · ${escapeHtml(l.value)}</li>`
                )
                .join("")}</ul>`
            : `<p class="meta">None yet. Attach any URL, DOI, path, coordinates, postal, or handle.</p>`
        }
        <p class="locator-row">
          <input type="text" id="attach-locator" placeholder="Add any address" value="${escapeHtml(state.attachValue)}" />
          <select id="attach-kind">
            <option value="auto"${state.attachKind === "auto" ? " selected" : ""}>detect kind</option>
            ${LOCATOR_KINDS.map(
              (k) => `<option value="${k}"${state.attachKind === k ? " selected" : ""}>${k}</option>`
            ).join("")}
          </select>
          <button class="btn ghost" id="do-attach">Attach</button>
        </p>
        <h3>Claims</h3>${ledgerList(entry, "key_claims")}
        <h3>Theorems</h3>${ledgerList(entry, "theorems")}
        <h3>Open gaps</h3>${ledgerList(entry, "open_gaps")}
        <h3>Action items</h3><p>${escapeHtml((entry.action_items || []).join(" · ") || "—")}</p>
        <p>
          <button class="btn ghost" id="export-one">JSON</button>
          <button class="btn danger" id="delete-one">Delete…</button>
        </p>
      </div>
    </div>
  `;
}

function renderIngest() {
  return `
    <header class="hero">
      <h1>Ingest</h1>
      <p class="kicker">Raw text is stored first. Summaries never replace it.</p>
    </header>
      <p class="banner">Paste the body. The address field takes any kind of locator — URL, DOI, file path, lat,lng, postal, @handle, or a line that starts ADDRESS: / URL: / DOI:.</p>
    <p class="locator-row">
      <input type="text" id="locator" placeholder="Address — any kind" value="${escapeHtml(state.locatorValue)}" />
      <select id="locator-kind">
        <option value="auto"${state.locatorKind === "auto" ? " selected" : ""}>detect kind</option>
        ${LOCATOR_KINDS.map(
          (k) => `<option value="${k}"${state.locatorKind === k ? " selected" : ""}>${k}</option>`
        ).join("")}
      </select>
    </p>
    <textarea id="ingest">${escapeHtml(state.ingestText)}</textarea>
    <p class="error">${escapeHtml(state.error)}</p>
    <p><button class="btn" id="do-ingest">Extract &amp; index</button></p>
  `;
}

function renderExport() {
  const all = exportVault(store.list());
  const professional = exportVault(store.list(), { includePrivate: false });
  return `
    <header class="hero">
      <h1>Export &amp; restore</h1>
      <p class="kicker">Portability is part of the engine, not an afterthought.</p>
    </header>
    <p class="banner">Full export includes private records. Professional export strips visibility=private.</p>
    <p>
      <button class="btn" id="dl-all">Download full vault (${all.count})</button>
      <button class="btn ghost" id="dl-pro">Professional only (${professional.count})</button>
    </p>
    <p><label>Restore from JSON <input type="file" id="restore" accept="application/json,.json" /></label></p>
    <p class="error">${escapeHtml(state.error)}</p>
  `;
}

function renderPrivacy() {
  return `
    <header class="hero">
      <h1>Privacy &amp; data</h1>
      <p class="kicker">Personal vault. No accounts. No inbox.</p>
    </header>
    <div class="panel">
      <p>Records live in this browser’s local storage unless you export them. There is no ChatVault cloud account in this engine build, so there is no inbox for strangers to message you through the app.</p>
      <p>Private vs professional is a user-controlled plane. Professional export omits private records.</p>
      <p>On iPhone: Safari → Share → Add to Home Screen. That is the install path. An Apple Developer membership can sign a later binary; it does not make this web vault an App Store listing, and we are not submitting one.</p>
      <p><button class="btn danger" id="wipe">Delete all local ChatVault data…</button></p>
    </div>
  `;
}

function renderDisclaimer() {
  return `
    <header class="hero">
      <h1>Disclaimer</h1>
      <p class="kicker">Not a truth engine.</p>
    </header>
    <div class="panel">
      <p>ChatVault captures, organizes, and retrieves material you ingest. AI-assisted labels and summaries can be wrong.</p>
      <p>CLAIM_LEDGER statuses are human-reviewed classifications. PROVED means a person marked it proved inside this vault — not that a journal, court, or prize committee agrees.</p>
      <p>Keep your own backups. This build does not guarantee retention.</p>
    </div>
  `;
}

function fixtureBench() {
  const cases = [
    { q: "euler identity", title: /Euler/i },
    { q: '"finite-time blow-up"', title: /Navier/i },
    { q: "claim:definitional", title: /Euler/i },
    { q: "gap:blow-up", title: /Navier/i },
  ];
  const rows = cases.map((c) => {
    const result = searchVault(DEMO_ENTRIES, c.q);
    const top = result.hits[0]?.entry;
    const grades = {};
    for (const e of DEMO_ENTRIES) grades[e.id] = c.title.test(e.title) ? 3 : 0;
    const ndcg = ndcgAt(
      result.hits.map((h) => h.entry.id),
      grades,
      5
    );
    const ok = top && c.title.test(top.title);
    return `<tr>
      <td><code>${escapeHtml(c.q)}</code></td>
      <td>${escapeHtml(top?.title || "none")}</td>
      <td>${result.took_ms.toFixed(1)} ms</td>
      <td>nDCG@5 ${ndcg.toFixed(2)} ${ok ? "hit" : "miss"}</td>
    </tr>`;
  });
  return `<table class="bench">
    <thead><tr><th>Query</th><th>Top hit (fixtures)</th><th>Time</th><th>Grade</th></tr></thead>
    <tbody>${rows.join("")}</tbody>
  </table>
  <p class="meta">Fixture bench, not your corpus. A miss here is a bug. A hit here does not prove search on your chats.</p>`;
}

function renderGuide() {
  return `
    <header class="hero">
      <h1>Why this engine</h1>
      <p class="kicker">The tagline is “OS for your AI.” The product is provenance + retrieval.</p>
    </header>
    <div class="panel">
      <p>Clippers already exist. ChatVault competes by refusing to collapse a conversation into a vibes summary.</p>
      <ol>
        <li>Raw text is immutable after ingest.</li>
        <li>Source AI and an address (URL / DOI / path) stay attached.</li>
        <li>Claims, theorems, and gaps are searchable fields with statuses.</li>
        <li>Search is hybrid ranker ${SEARCH_ENGINE_VERSION}: boolean gate, then BM25F + character 3-grams + TF-IDF cosine fused by RRF. Field prefixes (<code>claim:</code>, <code>gap:</code>) are hard gates. Ledger status is never a score.</li>
        <li>The surface is an atlas (constellation), not an Evernote notebook stack.</li>
        <li>Private material can be kept off professional export.</li>
      </ol>
      <h3>Fixture bench (honest, simulated on demo records)</h3>
      ${fixtureBench()}
    </div>
  `;
}

function shell(inner) {
  return `
    <aside class="sidebar">
      <div class="brand">
        <div class="dial" aria-hidden="true"></div>
        <strong>CHAT VAULT</strong>
      </div>
      ${nav("vault", "Atlas")}
      ${nav("ingest", "Ingest")}
      ${nav("export", "Export")}
      ${nav("guide", "Engine")}
      ${nav("privacy", "Privacy")}
      ${nav("disclaimer", "Disclaimer")}
      ${skinSwitcher()}
      <p class="foot">${escapeHtml(SKINS[state.skin].label)} · local · not App Store</p>
    </aside>
    <main class="main">${inner}</main>
  `;
}

function renderFatal(err) {
  const message = err && err.message ? err.message : String(err || "Unknown render error");
  root.innerHTML = `<main class="main">
    <div class="panel fatal">
      <h1>ChatVault stopped rendering</h1>
      <p>This is an error boundary, not an empty vault. The last error was:</p>
      <pre class="raw">${escapeHtml(message)}</pre>
      <p><button class="btn" id="recover">Reload vault view</button></p>
    </div>
  </main>`;
}

function render() {
  if (state.fatal) {
    renderFatal(state.fatal);
    return;
  }
  try {
    let inner = "";
    if (state.view === "vault") inner = renderVault();
    else if (state.view === "detail") inner = renderDetail(store.get(state.selectedId));
    else if (state.view === "ingest") inner = renderIngest();
    else if (state.view === "export") inner = renderExport();
    else if (state.view === "privacy") inner = renderPrivacy();
    else if (state.view === "disclaimer") inner = renderDisclaimer();
    else inner = renderGuide();
    root.innerHTML = shell(inner);
  } catch (err) {
    state.fatal = err;
    renderFatal(err);
  }
}

function downloadJson(name, obj) {
  const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  URL.revokeObjectURL(a.href);
}

root.addEventListener("click", (ev) => {
  if (ev.target.id === "recover") {
    state.fatal = null;
    set({ view: "vault", error: "", notice: "Recovered from a render error." });
    return;
  }
  const skinBtn = ev.target.closest("[data-set-skin]");
  if (skinBtn) {
    const skin = applySkin(saveSkin(skinBtn.dataset.setSkin));
    set({ skin, notice: `${SKINS[skin].label} — ${SKINS[skin].blurb}` });
    return;
  }
  const viewBtn = ev.target.closest("[data-view]");
  if (viewBtn) {
    set({ view: viewBtn.dataset.view, error: "", notice: "", page: 0 });
    return;
  }
  const open = ev.target.closest("[data-open]");
  if (open) {
    set({ view: "detail", selectedId: open.dataset.open, error: "" });
    return;
  }
  if (ev.target.id === "load-demo") {
    store.load(DEMO_ENTRIES);
    set({ view: "vault", error: "" });
    return;
  }
  if (ev.target.id === "page-prev") {
    set({ page: Math.max(0, state.page - 1) });
    return;
  }
  if (ev.target.id === "page-next") {
    set({ page: state.page + 1 });
    return;
  }
  if (ev.target.id === "do-search") {
    const q = document.getElementById("q")?.value ?? state.query;
    set({ query: q, error: "", notice: "", page: 0 });
    return;
  }
  if (ev.target.id === "do-ingest") {
    try {
      const loc = makeLocator(state.locatorValue, state.locatorKind);
      const entry = ingestPaste(state.ingestText, loc ? { locators: [loc] } : {});
      store.add(entry);
      set({ view: "detail", selectedId: entry.id, ingestText: "", locatorValue: "", error: "" });
    } catch (err) {
      set({ error: err.message });
    }
    return;
  }
  if (ev.target.id === "do-attach") {
    const current = store.get(state.selectedId);
    if (!current) return;
    try {
      const next = attachLocator(current, state.attachValue, state.attachKind);
      store.replaceAfterSuccess(current.id, next);
      set({ attachValue: "", error: "", notice: "Address attached." });
    } catch (err) {
      set({ error: err.message });
    }
    return;
  }
  if (ev.target.id === "export-one") {
    const entry = store.get(state.selectedId);
    if (entry) downloadJson(`${entry.id}.json`, exportVault([entry]));
    return;
  }
  if (ev.target.id === "dl-all") {
    downloadJson("chatvault-full.json", exportVault(store.list()));
    return;
  }
  if (ev.target.id === "dl-pro") {
    downloadJson("chatvault-professional.json", exportVault(store.list(), { includePrivate: false }));
    return;
  }
  if (ev.target.id === "delete-one") {
    if (!window.confirm("Delete this record? This cannot be undone in this local vault.")) return;
    try {
      store.deleteConfirmed(state.selectedId);
      set({ view: "vault", selectedId: null, error: "" });
    } catch (err) {
      set({ error: err.message });
    }
    return;
  }
  if (ev.target.id === "wipe") {
    if (!window.confirm("Delete ALL local ChatVault data on this device?")) return;
    localStorage.removeItem(STORAGE_KEY);
    store.load([]);
    set({ view: "vault", selectedId: null, error: "" });
  }
});

root.addEventListener("input", (ev) => {
  if (ev.target.id === "q") state.query = ev.target.value;
  if (ev.target.id === "ingest") state.ingestText = ev.target.value;
  if (ev.target.id === "locator") state.locatorValue = ev.target.value;
  if (ev.target.id === "attach-locator") state.attachValue = ev.target.value;
});

root.addEventListener("change", (ev) => {
  if (ev.target.id === "q") set({ query: ev.target.value });
  if (ev.target.id === "vis") set({ visibility: ev.target.value, page: 0 });
  if (ev.target.id === "ai") set({ source_ai: ev.target.value, page: 0 });
  if (ev.target.id === "locator-kind") set({ locatorKind: ev.target.value });
  if (ev.target.id === "attach-kind") set({ attachKind: ev.target.value });
  if (ev.target.id === "restore" && ev.target.files?.[0]) {
    const file = ev.target.files[0];
    file.text().then((text) => {
      try {
        const restored = importVault(JSON.parse(text));
        store.load(restored);
        set({ view: "vault", error: "" });
      } catch (err) {
        set({ error: err.message });
      }
    });
  }
  const review = ev.target.dataset?.review;
  if (review) {
    const [field, id] = review.split(":");
    const current = store.get(state.selectedId);
    if (!current) return;
    const next = reviewLedgerItem(current, field, id, ev.target.value, { humanReviewed: true });
    store.replaceAfterSuccess(current.id, next);
    set({ error: "" });
  }
});

root.addEventListener("keydown", (ev) => {
  if (ev.target.id === "q" && ev.key === "Enter") {
    set({ query: ev.target.value, page: 0 });
  }
});

window.addEventListener("error", (ev) => {
  state.fatal = ev.error || new Error(ev.message || "window error");
  render();
});
window.addEventListener("unhandledrejection", (ev) => {
  state.fatal = ev.reason instanceof Error ? ev.reason : new Error(String(ev.reason));
  render();
});

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js").catch(() => {
    /* PWA optional; engine still runs */
  });
}

render();
