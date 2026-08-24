import {
  DEMO_ENTRIES,
  SCHEMA_VERSION,
  LEDGER_STATUSES,
  SOURCE_AIS,
  ingestPaste,
  searchEntries,
  exportVault,
  importVault,
  updateEntry,
  reviewLedgerItem,
  createStore,
} from "./engine.mjs";

const STORAGE_KEY = "chatvault.engine.v1";
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

function filtered() {
  return searchEntries(store.list(), state.query, {
    visibility: state.visibility || undefined,
    source_ai: state.source_ai || undefined,
  });
}

function renderVault() {
  const rows = filtered();
  const emptyVault = store.list().length === 0;
  const cards = emptyVault
    ? `<p class="empty">Vault is empty on this device (not a failed load). <button class="btn ghost" id="load-demo">Load example fixtures</button></p>`
    : rows.length
    ? rows
        .map((e) => {
          const statuses = [...(e.key_claims || []), ...(e.theorems || []), ...(e.open_gaps || [])]
            .map((x) => x.status)
            .filter(Boolean);
          const status = statuses[0] || "NOTE";
          return `<article class="card" data-open="${escapeHtml(e.id)}">
            <span class="badge">${escapeHtml(e.source_ai)}</span>
            <span class="badge ${e.visibility}">${escapeHtml(e.visibility)}</span>
            <span class="badge ${status.toLowerCase()}">${escapeHtml(status)}</span>
            <h3>${escapeHtml(e.title)}</h3>
            <p>${escapeHtml((e.summary || e.content_text || "").slice(0, 160))}</p>
          </article>`;
        })
        .join("")
    : `<p class="empty">No matching records. An empty vault is different from a failed load — this search simply matched nothing.</p>`;

  return `
    <header class="hero">
      <h1>Conversation Vault</h1>
      <p class="kicker">OS for your AI</p>
      <p class="meta">${store.list().length} records indexed · local-first engine ${escapeHtml(SCHEMA_VERSION)}</p>
      <p class="banner">This is knowledge capture with provenance and a claim ledger. It does not prove theorems, verify science, or replace a human review.</p>
    </header>
    <div class="toolbar">
      <input type="search" id="q" placeholder="Search raw text, claims, theorems, gaps… Use OR, quotes, claim:" value="${escapeHtml(state.query)}" />
      <button class="btn ghost" id="do-search">Search</button>
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
    <div class="grid">${cards}</div>
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
           <span class="badge">${escapeHtml(entry.source_file || "no source file")}</span></p>
        <p class="meta">Ingested ${escapeHtml(entry.ingested_at)} · item date ${escapeHtml(entry.item_date)}</p>
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
    <p class="banner">Optional structured lines: TITLE, SOURCE_AI, CLAIM, THEOREM, GAP, ACTION, QUESTION, VISIBILITY. CLAIM_LEDGER starts at UNREVIEWED. Nothing is auto-PROVED.</p>
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
      <p class="kicker">Local-first on this device. Not an App Store build yet.</p>
    </header>
    <div class="panel">
      <p>Records live in this browser’s local storage unless you export them. There is no ChatVault cloud account in this engine build.</p>
      <p>Private vs professional is a user-controlled plane. Professional export omits private records.</p>
      <p>Apple App Store submission still needs a signed developer account, a hosted privacy policy URL, account deletion if accounts exist, and a packaged iOS binary. This page is the disclosure draft for that later step.</p>
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
        <li>Source AI and source file stay attached.</li>
        <li>Claims, theorems, and gaps are searchable fields with statuses.</li>
        <li>Search is AND by default, with OR, "phrases", and field prefixes.</li>
        <li>Private material can be kept off professional export.</li>
      </ol>
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
      ${nav("vault", "Vault")}
      ${nav("ingest", "Ingest")}
      ${nav("export", "Export")}
      ${nav("guide", "Engine")}
      ${nav("privacy", "Privacy")}
      ${nav("disclaimer", "Disclaimer")}
      <p class="foot">Local engine · not App Store certified</p>
    </aside>
    <main class="main">${inner}</main>
  `;
}

function render() {
  let inner = "";
  if (state.view === "vault") inner = renderVault();
  else if (state.view === "detail") inner = renderDetail(store.get(state.selectedId));
  else if (state.view === "ingest") inner = renderIngest();
  else if (state.view === "export") inner = renderExport();
  else if (state.view === "privacy") inner = renderPrivacy();
  else if (state.view === "disclaimer") inner = renderDisclaimer();
  else inner = renderGuide();
  root.innerHTML = shell(inner);
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
  const viewBtn = ev.target.closest("[data-view]");
  if (viewBtn) {
    set({ view: viewBtn.dataset.view, error: "" });
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
  if (ev.target.id === "do-search") {
    const q = document.getElementById("q")?.value ?? state.query;
    set({ query: q, error: "" });
    return;
  }
  if (ev.target.id === "do-ingest") {
    try {
      const entry = ingestPaste(state.ingestText);
      store.add(entry);
      set({ view: "detail", selectedId: entry.id, ingestText: "", error: "" });
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
});

root.addEventListener("change", (ev) => {
  if (ev.target.id === "q") set({ query: ev.target.value });
  if (ev.target.id === "vis") set({ visibility: ev.target.value });
  if (ev.target.id === "ai") set({ source_ai: ev.target.value });
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
    set({ query: ev.target.value });
  }
});

render();
