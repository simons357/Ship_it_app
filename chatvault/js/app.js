import {
  DEMO_ENTRIES,
  SCHEMA_VERSION,
  LEDGER_STATUSES,
  SOURCE_AIS,
  SOURCE_TYPES,
  ORIGIN_CLASSES,
  MAX_PASTE_CHARS,
  ingestPaste,
  ingestBulk,
  searchEntries,
  searchVault,
  SEARCH_ENGINE_VERSION,
  exportVault,
  importVault,
  updateEntry,
  reviewLedgerItem,
  createStore,
  listTags,
  listBooks,
  listArtifacts,
  vaultStats,
  uniqueProjects,
  statusClass,
} from "./engine.mjs";
import {
  DA_DRAIN_URLS,
  MAX_IMAGE_BYTES,
  classifyFilename,
  ingestNamedSource,
  ingestNoticeForResults,
  loadInboxFromRepo,
  postInboxExport,
  pullDaDrain,
} from "./drain.mjs";
import { SKINS, SKIN_IDS, loadSkin, saveSkin, applySkin } from "./skins.mjs";

const STORAGE_KEY = "chatvault.engine.v1";
const BOOKS_KEY = "chatvault.books.extra.v1";
const PAGE_SIZE = 50;
const root = document.getElementById("app");
const currentSkin = { id: applySkin(loadSkin()) };

function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

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

function loadExtraBooks() {
  try {
    const raw = localStorage.getItem(BOOKS_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed.map((n) => String(n)).filter(Boolean) : [];
  } catch {
    return [];
  }
}

const store = createStore(loadPersisted());
let persistOk = true;
store.subscribe((entries) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(exportVault(entries)));
    persistOk = true;
  } catch {
    persistOk = false;
  }
});

const state = {
  view: "vault",
  query: "",
  visibility: "",
  source_ai: "",
  source_type: "",
  origin_class: "",
  book: "",
  tag: "",
  project: "",
  starredOnly: false,
  selectedId: null,
  selectedTag: "",
  notice: "",
  error: "",
  ingestText: "",
  ingestTab: "single",
  ingestAi: "unknown",
  ingestVis: "professional",
  ingestBook: "",
  ingestOrigin: "",
  ingestType: "",
  page: 0,
  extraBooks: loadExtraBooks(),
  fatal: null,
};

function persistExtraBooks() {
  try {
    localStorage.setItem(BOOKS_KEY, JSON.stringify(state.extraBooks));
  } catch {
    /* quota */
  }
}

function set(patch) {
  Object.assign(state, patch);
  syncHash();
  render();
}

function syncHash() {
  let hash = state.view;
  if (state.view === "detail" && state.selectedId) hash = `detail/${state.selectedId}`;
  if (state.view === "ingest") hash = `ingest/${state.ingestTab}`;
  if (state.view === "tags" && state.selectedTag) hash = `tags/${encodeURIComponent(state.selectedTag)}`;
  const next = `#${hash}`;
  if (location.hash !== next) history.replaceState(null, "", next);
}

function launchQuery() {
  try {
    const fromSearch = new URLSearchParams(location.search).get("q");
    const hash = (location.hash || "").slice(1);
    const qPart = hash.includes("?") ? hash.slice(hash.indexOf("?") + 1) : "";
    const fromHash = new URLSearchParams(qPart).get("q");
    return fromSearch || fromHash || "";
  } catch {
    return "";
  }
}

function applyHash() {
  const raw = (location.hash || "#vault").slice(1).split("?")[0];
  const [view, rest] = raw.split("/");
  const q = launchQuery();
  if (q) state.query = q;
  if (view === "detail" && rest) {
    state.view = "detail";
    state.selectedId = rest;
    return;
  }
  if (view === "ingest") {
    state.view = "ingest";
    state.ingestTab = rest === "bulk" || rest === "files" || rest === "drain" ? rest : "single";
    return;
  }
  if (view === "tags") {
    state.view = "tags";
    state.selectedTag = rest ? decodeURIComponent(rest) : "";
    return;
  }
  const known = ["vault", "books", "tags", "artifacts", "dashboard", "export", "guide", "privacy", "disclaimer", "ingest"];
  state.view = known.includes(view) ? view : "vault";
}

function nav(id, label, icon) {
  const current = state.view === id ? ' aria-current="page"' : "";
  return `<button class="nav-btn" data-view="${id}"${current}>${icon}<span>${label}</span></button>`;
}

const ICONS = {
  vault: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 5v14M4 10h16"/></svg>',
  ingest: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 5v14M5 12h14"/></svg>',
  books: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 5h7v14H4zM13 5h7v14h-7z"/></svg>',
  tags: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 12l8-8h8v8l-8 8z"/><circle cx="16" cy="8" r="1.2"/></svg>',
  artifacts: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>',
  dashboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 19a9 9 0 1 1 14 0"/><path d="M12 12l4-3"/></svg>',
  export: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 4v10M8 8l4-4 4 4M5 20h14"/></svg>',
  guide: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2"/></svg>',
  privacy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="6" y="11" width="12" height="9" rx="2"/><path d="M9 11V8a3 3 0 0 1 6 0v3"/></svg>',
  disclaimer: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16.5h.01"/></svg>',
};

function activeFilters() {
  return {
    visibility: state.visibility || undefined,
    source_ai: state.source_ai || undefined,
    source_type: state.source_type || undefined,
    origin_class: state.origin_class || undefined,
    book: state.book || undefined,
    tag: state.tag || undefined,
    project: state.project || undefined,
    starred: state.starredOnly || undefined,
  };
}

function rankedSearch() {
  return searchVault(store.list(), state.query, activeFilters());
}

function originBadge(entry) {
  const origin = entry.origin_class === "ai_generated" ? "ai_generated" : "human_record";
  const label = origin === "ai_generated" ? "AI conversation" : "Real record";
  return `<span class="badge origin-${origin === "ai_generated" ? "ai" : "human"}">${label}</span>`;
}

function persistBanner() {
  if (persistOk) return "";
  return `<p class="banner warn">This vault is larger than browser localStorage (often 5–10 MB). Records are in this session — export JSON now. IndexedDB is the next persistence step.</p>`;
}

function highlightSnippet(snippet) {
  const text = String(snippet.text || "");
  const marks = [...(snippet.marks || [])].sort((a, b) => a[0] - b[0]);
  if (!marks.length) return escapeHtml(text);
  let out = "";
  let cursor = 0;
  for (const [start, end] of marks) {
    const s = Math.max(0, Math.min(text.length, start));
    const e = Math.max(s, Math.min(text.length, end));
    if (s < cursor) continue;
    out += escapeHtml(text.slice(cursor, s));
    out += `<mark>${escapeHtml(text.slice(s, e))}</mark>`;
    cursor = e;
  }
  out += escapeHtml(text.slice(cursor));
  return out;
}

function booksForUi() {
  const fromEntries = listBooks(store.list());
  const names = new Set(fromEntries.map((b) => b.name.toLowerCase()));
  const extras = state.extraBooks
    .filter((name) => !names.has(name.toLowerCase()))
    .map((name) => ({ name, count: 0, ids: [] }));
  return [...fromEntries.filter((b) => b.name !== "(unfiled)"), ...extras, ...fromEntries.filter((b) => b.name === "(unfiled)")];
}

function tagChips(entries, active) {
  return listTags(entries)
    .slice(0, 36)
    .map((t) => {
      const pressed = active && active.toLowerCase() === t.tag.toLowerCase();
      return `<button class="chip" data-tag="${escapeHtml(t.tag)}" aria-pressed="${pressed ? "true" : "false"}">${escapeHtml(t.tag)} ${t.count}</button>`;
    })
    .join("");
}

function renderVault() {
  const ranked = rankedSearch();
  const rows = ranked.hits;
  const emptyVault = store.list().length === 0;
  const pageCount = Math.max(1, Math.ceil(rows.length / PAGE_SIZE));
  if (state.page >= pageCount) state.page = pageCount - 1;
  const pageRows = rows.slice(state.page * PAGE_SIZE, (state.page + 1) * PAGE_SIZE);
  const stats = vaultStats(store.list());
  const searching = Boolean(String(state.query || "").trim());
  const pager =
    rows.length > PAGE_SIZE
      ? `<p class="pager">
          <button class="btn ghost" id="page-prev" ${state.page === 0 ? "disabled" : ""}>Previous</button>
          <span class="meta">Page ${state.page + 1} of ${pageCount} · ${rows.length} matches</span>
          <button class="btn ghost" id="page-next" ${state.page >= pageCount - 1 ? "disabled" : ""}>Next</button>
        </p>`
      : "";
  const cards = emptyVault
    ? `<p class="empty">Vault is empty on this device (not a failed load). <button class="btn ghost" id="load-demo">Load example fixtures</button></p>`
    : rows.length
    ? pageRows
        .map((hit) => {
          const e = hit.entry;
          const statuses = [...(e.key_claims || []), ...(e.theorems || []), ...(e.open_gaps || [])]
            .map((x) => x.status)
            .filter(Boolean);
          const status = (hit.snippets.find((s) => s.ledger_status) || {}).ledger_status || statuses[0] || "NOTE";
          const tags = [...(e.search_tags || [])].slice(0, 4)
            .map((t) => `<span class="tag">${escapeHtml(t)}</span>`)
            .join("");
          const snippet = hit.snippets[0];
          const body = searching && snippet
            ? `<p class="clamp snippet"><span class="hit-field">${escapeHtml(snippet.field)}${snippet.ledger_status ? ` · ${escapeHtml(snippet.ledger_status)}` : ""}</span> ${highlightSnippet(snippet)}</p>`
            : `<p class="clamp">${escapeHtml((e.summary || e.content_text || "").slice(0, 220))}</p>`;
          const rankMeta = searching
            ? `<span class="hit-meta">score ${hit.score.toFixed(2)}${hit.matched_fields.length ? ` · ${escapeHtml(hit.matched_fields.slice(0, 3).join(" · "))}` : ""}</span>`
            : `<span>${escapeHtml((e.related_projects || [])[0] || "")}</span>`;
          return `<article class="card" data-open="${escapeHtml(e.id)}">
            <div class="card-top">
              <div>
                <span class="badge">${escapeHtml(e.source_ai)}</span>
                ${originBadge(e)}
                <span class="badge ${escapeHtml(e.visibility)}">${escapeHtml(e.visibility)}</span>
                <span class="badge ${escapeHtml(statusClass(status))}">${escapeHtml(status)}</span>
              </div>
              <button class="icon-btn${e.starred ? " star" : ""}" data-star="${escapeHtml(e.id)}" aria-label="Star">${e.starred ? "★" : "☆"}</button>
            </div>
            <h3>${escapeHtml(e.title)}</h3>
            ${body}
            <div class="chips">${tags}</div>
            <div class="card-foot">
              <span>${escapeHtml(e.project_category || e.source_type)}</span>
              ${rankMeta}
            </div>
          </article>`;
        })
        .join("")
    : `<p class="empty">No matching records. An empty vault is different from a failed load — this search simply matched nothing.</p>`;

  const projects = uniqueProjects(store.list());
  const bookOptions = booksForUi()
    .map((b) => `<option value="${escapeHtml(b.name)}"${state.book === b.name ? " selected" : ""}>${escapeHtml(b.name)}</option>`)
    .join("");

  return `
    <div class="hero-row">
      <header class="hero">
        <h1>ChatVault</h1>
        <p class="kicker">OS for your AI</p>
        <p class="meta">${stats.total} records indexed · ${stats.by_origin?.ai_generated || 0} AI · ${stats.by_origin?.human_record || 0} real · ${stats.starred} starred · ${searching ? `${ranked.total} ranked · ${ranked.took_ms.toFixed(1)} ms ·` : ""} ${escapeHtml(SEARCH_ENGINE_VERSION)}</p>
      </header>
      <button class="btn" data-view="ingest">+ Ingest</button>
    </div>
    <p class="banner">OS for your AI. Provenance for chats, and a searchable shelf for real papers, letters, pictures, and movies. It does not prove theorems.</p>
    ${persistBanner()}
    <div class="search-panel">
      <div class="toolbar">
        <input type="search" id="q" placeholder='euler identity · origin:ai · origin:human · claim:definitional · ai:Claude' value="${escapeHtml(state.query)}" />
        <button class="btn ghost" id="do-search">Search</button>
      </div>
      <p class="help">Type the words you remember. Best match first. Quotes for an exact phrase. <code>origin:ai</code> vs <code>origin:human</code> splits AI chats from real records. <code>claim:</code> <code>gap:</code> <code>ai:</code> look in one slot. Status on a card is the ledger, not the rank.</p>
      <div class="filters">
        <button class="chip" id="star-filter" aria-pressed="${state.starredOnly ? "true" : "false"}">${state.starredOnly ? "★ Starred" : "☆ Starred"}</button>
        <select id="vis">
          <option value="">Visibility: all</option>
          <option value="professional"${state.visibility === "professional" ? " selected" : ""}>professional</option>
          <option value="private"${state.visibility === "private" ? " selected" : ""}>private</option>
        </select>
        <select id="ai">
          <option value="">Source AI: all</option>
          ${SOURCE_AIS.map((a) => `<option${state.source_ai === a ? " selected" : ""}>${escapeHtml(a)}</option>`).join("")}
        </select>
        <select id="origin">
          <option value="">Origin: all</option>
          ${ORIGIN_CLASSES.map((o) => {
            const label = o === "ai_generated" ? "AI conversations" : "Real records";
            return `<option value="${escapeHtml(o)}"${state.origin_class === o ? " selected" : ""}>${label}</option>`;
          }).join("")}
        </select>
        <select id="stype">
          <option value="">Source type: all</option>
          ${SOURCE_TYPES.map((a) => `<option${state.source_type === a ? " selected" : ""}>${escapeHtml(a)}</option>`).join("")}
        </select>
        <select id="project">
          <option value="">Project: all</option>
          ${projects.map((p) => `<option${state.project === p ? " selected" : ""}>${escapeHtml(p)}</option>`).join("")}
        </select>
        <select id="book">
          <option value="">Book: all</option>
          ${bookOptions}
        </select>
      </div>
      <div class="chips">${tagChips(store.list(), state.tag)}</div>
    </div>
    <p class="error">${escapeHtml(state.error)}</p>
    <p class="notice">${escapeHtml(state.notice)}</p>
    ${pager}
    <div class="grid">${cards}</div>
  `;
}

function ledgerList(entry, field) {
  const items = entry[field] || [];
  if (!items.length) return `<p class="meta">None recorded. Absence is explicit.</p>`;
  return `<ul class="ledger">${items
    .map(
      (item) => `<li>
        <span><code class="badge ${escapeHtml(statusClass(item.status))}">${escapeHtml(item.status)}</code> ${escapeHtml(item.text)}</span>
        <select data-review-field="${escapeHtml(field)}" data-review-id="${escapeHtml(item.id)}">
          ${LEDGER_STATUSES.map((s) => `<option${item.status === s ? " selected" : ""}>${escapeHtml(s)}</option>`).join("")}
        </select>
      </li>`
    )
    .join("")}</ul>`;
}

function renderRaw(entry) {
  if (entry.file_url && String(entry.file_url).startsWith("data:image/")) {
    return `<img class="vault-media" src="${escapeHtml(entry.file_url)}" alt="${escapeHtml(entry.title)}" />`;
  }
  if (["movie", "audio", "pdf", "docx", "picture"].includes(entry.source_type) && !entry.file_url) {
    const media = entry.media_path
      ? `<p class="help">Repo media: <code>${escapeHtml(entry.media_path)}</code>. Binary is not in BM25 raw_content.</p>`
      : `<p class="help">Indexed as human record stub (binary not stored in the browser vault; use CLI --ingest-chatvault to copy into the repo inbox).</p>`;
    return `<pre class="raw">${escapeHtml(entry.raw_content)}</pre>${media}`;
  }
  const raw = String(entry.raw_content || "");
  if (raw.length > 200000) {
    return `<pre class="raw">${escapeHtml(raw.slice(0, 200000))}\n\n… viewer truncated (${raw.length} chars stored) …</pre>`;
  }
  return `<pre class="raw">${escapeHtml(raw)}</pre>`;
}

function renderDetail(entry) {
  if (!entry) {
    return `<p class="empty">That record is gone. If a delete failed, it would still be listed in the vault.</p>`;
  }
  const books = booksForUi();
  const tags = (entry.search_tags || [])
    .map((t) => `<button class="chip" data-remove-tag="${escapeHtml(t)}">${escapeHtml(t)} ×</button>`)
    .join("");
  return `
    <button class="back" data-view="vault">← Back to vault</button>
    <div class="hero-row">
      <header class="hero">
        <p><span class="badge">${escapeHtml(entry.source_ai)}</span>
           ${originBadge(entry)}
           <span class="badge">${escapeHtml(entry.source_type)}</span>
           <span class="badge ${escapeHtml(entry.visibility)}">${escapeHtml(entry.visibility)}</span></p>
        <h1>${escapeHtml(entry.title)}</h1>
        <p class="kicker">${escapeHtml(entry.source_file || "no source file")} · ingested ${escapeHtml(entry.ingested_at.slice(0, 10))}</p>
      </header>
      <p>
        <button class="icon-btn${entry.starred ? " star" : ""}" data-star="${escapeHtml(entry.id)}" aria-label="Star">${entry.starred ? "★" : "☆"}</button>
        <button class="btn ghost" id="export-one">JSON</button>
        <button class="btn danger" id="delete-one">Delete…</button>
      </p>
    </div>
    <p class="error">${escapeHtml(state.error)}</p>
    <div class="detail">
      <div class="panel">
        <h3>Raw content (immutable)</h3>
        ${renderRaw(entry)}
        <h3>Optional summary</h3>
        <p>${escapeHtml(entry.summary || "—")}</p>
      </div>
      <div>
        <div class="panel">
          <h3>CLAIM_LEDGER</h3>
          <h4>Claims</h4>${ledgerList(entry, "key_claims")}
          <h4>Theorems</h4>${ledgerList(entry, "theorems")}
          <h4>Open gaps</h4>${ledgerList(entry, "open_gaps")}
          <h4>Action items</h4><p>${escapeHtml((entry.action_items || []).join(" · ") || "—")}</p>
          <h4>Open questions</h4><p>${escapeHtml((entry.open_questions || []).join(" · ") || "—")}</p>
        </div>
        <div class="panel" style="margin-top:1rem">
          <h3>Books</h3>
          <div class="chips">
            ${books
              .filter((b) => b.name !== "(unfiled)")
              .map((b) => {
                const on = (entry.related_projects || []).includes(b.name);
                return `<button class="chip" data-toggle-book="${escapeHtml(b.name)}" aria-pressed="${on ? "true" : "false"}">${escapeHtml(b.name)}</button>`;
              })
              .join("")}
          </div>
          <h3>Tags</h3>
          <div class="chips">${tags || '<span class="meta">None yet.</span>'}</div>
          <p class="toolbar">
            <input type="text" id="new-tag" placeholder="Add tags, comma separated…" />
            <button class="btn ghost" id="add-tags">+ Add</button>
          </p>
          <p>
            <label>Visibility
              <select id="set-vis">
                <option value="professional"${entry.visibility === "professional" ? " selected" : ""}>professional</option>
                <option value="private"${entry.visibility === "private" ? " selected" : ""}>private</option>
              </select>
            </label>
          </p>
        </div>
      </div>
    </div>
  `;
}

function renderIngest() {
  const tab = state.ingestTab;
  return `
    <button class="back" data-view="vault">← Back to vault</button>
    <header class="hero">
      <h1>Slide it in</h1>
      <p class="kicker">OS for your AI</p>
      <p class="meta">Drop a finished chat, a ChatGPT export, a Domain Architect audit, or a real paper / letter / picture / movie. Huge paste cap (${MAX_PASTE_CHARS.toLocaleString()} chars). Browser storage is still ~5–10 MB until IndexedDB.</p>
    </header>
    <div class="tabs">
      <button class="tab" data-ingest-tab="single" aria-current="${tab === "single"}">Single</button>
      <button class="tab" data-ingest-tab="bulk" aria-current="${tab === "bulk"}">Bulk</button>
      <button class="tab" data-ingest-tab="files" aria-current="${tab === "files"}">Files</button>
      <button class="tab" data-ingest-tab="drain" aria-current="${tab === "drain"}">Drain</button>
    </div>
    <div class="panel drop-target" id="ingest-drop">
      <p class="banner">Structured lines are optional: TITLE, SOURCE_AI, SOURCE_TYPE, ORIGIN, CLAIM, THEOREM, GAP, ACTION, QUESTION, TAG, BOOK, VISIBILITY. CLAIM_LEDGER starts at UNREVIEWED. Nothing is auto-PROVED. No LLM is called. Origin marks AI conversations vs real records.</p>
      <div class="ingest-meta">
        <select id="ingest-ai">
          ${SOURCE_AIS.map((a) => `<option${state.ingestAi === a ? " selected" : ""}>${escapeHtml(a)}</option>`).join("")}
        </select>
        <select id="ingest-origin">
          <option value=""${state.ingestOrigin === "" ? " selected" : ""}>Origin: infer</option>
          ${ORIGIN_CLASSES.map((o) => {
            const label = o === "ai_generated" ? "AI conversation" : "Real record";
            return `<option value="${escapeHtml(o)}"${state.ingestOrigin === o ? " selected" : ""}>${label}</option>`;
          }).join("")}
        </select>
        <select id="ingest-type">
          <option value=""${state.ingestType === "" ? " selected" : ""}>Type: infer</option>
          ${SOURCE_TYPES.map((a) => `<option${state.ingestType === a ? " selected" : ""}>${escapeHtml(a)}</option>`).join("")}
        </select>
        <select id="ingest-vis">
          <option value="professional"${state.ingestVis === "professional" ? " selected" : ""}>professional</option>
          <option value="private"${state.ingestVis === "private" ? " selected" : ""}>private</option>
        </select>
        <input type="text" id="ingest-book" placeholder="Book (optional)" value="${escapeHtml(state.ingestBook)}" />
      </div>
      ${
        tab === "files"
          ? `<div class="dropzone" id="dropzone">
               <p><strong>Drop the whole conversation or any file here.</strong></p>
               <p class="help">txt md json csv html · ChatGPT conversations.json · DA audit JSON · pictures under ${(MAX_IMAGE_BYTES / (1024 * 1024)).toFixed(0)} MB · movies / pdf / audio become searchable stubs</p>
               <p><label>Choose files <input type="file" id="ingest-files" multiple /></label></p>
               <p><button class="btn ghost" id="load-inbox">Load inbox from repo</button></p>
             </div>`
          : tab === "drain"
          ? `<p>Domain Architect is a math auditor, not this vault’s brain. When an audit finishes, drain it here. The repo inbox is how sounds, video, papers, and letters get into git — not only localStorage.</p>
             <p class="help">1. <code>python3 -m domain_architect --drain-server</code><br/>2. <code>python3 -m domain_architect --drain-chatvault "∇²Φ = 4πGρ"</code><br/>3. Pull. Or drop the JSON on Files. Loopback only: ${escapeHtml(DA_DRAIN_URLS[0])}</p>
             <p class="help">Any-source into the repo: <code>python3 -m domain_architect --ingest-chatvault PATH</code> writes JSON under <code>chatvault/inbox/</code>.</p>
             <p><button class="btn" id="pull-da">Pull from Domain Architect</button>
                <button class="btn ghost" id="load-inbox">Load inbox from repo</button>
                <button class="btn ghost" id="send-inbox">Send this vault JSON to repo</button></p>`
          : `<textarea id="ingest" placeholder="${tab === "bulk" ? "Paste several records separated by a line of ---" : "Paste the whole conversation here, then extract & index."}">${escapeHtml(state.ingestText)}</textarea>`
      }
      <p class="error">${escapeHtml(state.error)}</p>
      <p class="notice">${escapeHtml(state.notice)}</p>
      ${persistBanner()}
      ${tab === "files" || tab === "drain" ? "" : `<p><button class="btn" id="do-ingest">${tab === "bulk" ? "Index all chunks" : "Extract &amp; index"}</button> <span class="help">Parses locally. Uses AI to extract is not a feature of this engine.</span></p>`}
    </div>
  `;
}

function renderBooks() {
  const books = booksForUi();
  const cards = books
    .map(
      (b) => `<article class="card" data-open-book="${escapeHtml(b.name)}">
        <h3>${escapeHtml(b.name)}</h3>
        <p>${b.name === "(unfiled)" ? "Records with no book assignment." : "Collection of related vault records."}</p>
        <div class="card-foot"><span>${b.count} conversation${b.count === 1 ? "" : "s"}</span></div>
      </article>`
    )
    .join("");
  return `
    <button class="back" data-view="vault">← Back to vault</button>
    <div class="hero-row">
      <header class="hero">
        <h1>Books</h1>
        <p class="meta">${books.filter((b) => b.name !== "(unfiled)").length} books · ${store.list().length} conversations</p>
      </header>
      <button class="btn" id="new-book">+ New book</button>
    </div>
    <p class="notice">${escapeHtml(state.notice)}</p>
    <div class="grid">${cards || '<p class="empty">No books yet.</p>'}</div>
  `;
}

function renderTags() {
  const tags = listTags(store.list());
  const selected = tags.find((t) => t.tag.toLowerCase() === state.selectedTag.toLowerCase());
  const rows = tags
    .map(
      (t) => `<div class="tag-row" data-select-tag="${escapeHtml(t.tag)}">
        <span>${escapeHtml(t.tag)} <span class="meta">${t.count}</span></span>
        <span class="meta">open in vault →</span>
      </div>`
    )
    .join("");
  const convos = selected
    ? searchEntries(store.list(), "", { tag: selected.tag })
        .map((e) => `<article class="card" data-open="${escapeHtml(e.id)}"><h3>${escapeHtml(e.title)}</h3><p class="clamp">${escapeHtml(e.summary || "")}</p></article>`)
        .join("")
    : `<p class="empty">Select a tag to see its conversations.</p>`;
  return `
    <button class="back" data-view="vault">← Back to vault</button>
    <header class="hero">
      <h1>Tags</h1>
      <p class="meta">${tags.length} unique tags across ${store.list().length} conversations.</p>
    </header>
    <div class="detail">
      <div class="panel">${rows || '<p class="empty">No tags yet. Add them on ingest or on a record.</p>'}</div>
      <div>${convos}</div>
    </div>
  `;
}

function renderArtifacts() {
  const items = listArtifacts(store.list());
  const cards = items
    .map(
      (a) => `<article class="card" data-open="${escapeHtml(a.entry_id)}">
        <div class="card-top">
          <span class="badge ${escapeHtml(statusClass(a.status))}">${escapeHtml(a.kind)} · ${escapeHtml(a.status)}</span>
          <span class="badge">${escapeHtml(a.source_ai)}</span>
        </div>
        <h3>${escapeHtml(a.text.slice(0, 120))}</h3>
        <p class="meta">${escapeHtml(a.entry_title)}</p>
      </article>`
    )
    .join("");
  return `
    <button class="back" data-view="vault">← Back to vault</button>
    <header class="hero">
      <h1>Artifacts</h1>
      <p class="kicker">Derived from claims, theorems, gaps, and actions. Not an LLM extraction stub.</p>
      <p class="meta">${items.length} artifacts</p>
    </header>
    <div class="grid">${cards || '<p class="empty">No artifacts yet. Ingest a record with CLAIM / THEOREM / GAP / ACTION lines.</p>'}</div>
  `;
}

function barRows(map) {
  const entries = Object.entries(map);
  const max = Math.max(1, ...entries.map(([, n]) => n));
  return entries
    .sort((a, b) => b[1] - a[1])
    .map(
      ([k, n]) => `<div class="bar-row"><span>${escapeHtml(k)}</span><div class="bar"><i style="width:${Math.round((n / max) * 100)}%"></i></div><span>${n}</span></div>`
    )
    .join("");
}

function renderDashboard() {
  const stats = vaultStats(store.list());
  return `
    <div class="hero-row">
      <img class="dash-mark" src="./assets/chatvault-mark-light.png" alt="ChatVault" width="112" height="112" />
      <header class="hero">
        <h1>Project ledger</h1>
        <p class="kicker">A live snapshot of this device’s vault. Not a readiness score and not a proof dashboard.</p>
      </header>
    </div>
    <div class="stats">
      <div class="stat"><b>${stats.total}</b><span>Total records</span></div>
      <div class="stat"><b>${stats.by_origin?.ai_generated || 0}</b><span>AI conversations</span></div>
      <div class="stat"><b>${stats.by_origin?.human_record || 0}</b><span>Real records</span></div>
      <div class="stat"><b>${stats.starred}</b><span>Starred</span></div>
      <div class="stat"><b>${stats.private}</b><span>Private</span></div>
      <div class="stat"><b>${stats.claims}</b><span>Claims</span></div>
      <div class="stat"><b>${stats.theorems}</b><span>Theorems</span></div>
      <div class="stat"><b>${stats.gaps}</b><span>Open gaps</span></div>
    </div>
    <div class="detail">
      <div class="panel"><h3>By origin</h3>${barRows(stats.by_origin) || '<p class="meta">None</p>'}</div>
      <div class="panel"><h3>By source AI</h3>${barRows(stats.by_ai) || '<p class="meta">None</p>'}</div>
      <div class="panel"><h3>By ledger status</h3>${barRows(stats.by_status) || '<p class="meta">None</p>'}</div>
    </div>
    <div class="panel" style="margin-top:1rem"><h3>By project</h3>${barRows(stats.by_project) || '<p class="meta">No project labels yet.</p>'}</div>
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
    <div class="panel">
      <p class="banner">Full export includes private records. Professional export strips visibility=private.</p>
      <p>
        <button class="btn" id="dl-all">Download full vault (${all.count})</button>
        <button class="btn ghost" id="dl-pro">Professional only (${professional.count})</button>
      </p>
      <p><label>Restore from JSON <input type="file" id="restore" accept="application/json,.json" /></label></p>
      <p class="error">${escapeHtml(state.error)}</p>
      <p class="notice">${escapeHtml(state.notice)}</p>
    </div>
  `;
}

function renderPrivacy() {
  return `
    <header class="hero">
      <h1>Privacy &amp; data</h1>
      <p class="kicker">Local-first on this device. Not an App Store build.</p>
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
      <p>ChatVault captures, organizes, and retrieves material you ingest. Labels you type can be wrong. This build does not call an extraction LLM.</p>
      <p>CLAIM_LEDGER statuses are human-reviewed classifications. PROVED means a person marked it proved inside this vault — not that a journal, court, or prize committee agrees.</p>
      <p>Keep your own backups. This build does not guarantee retention.</p>
    </div>
  `;
}

function renderGuide() {
  return `
    <header class="hero">
      <h1>Why this engine</h1>
      <p class="kicker">The tagline is “OS for your AI.” The product is provenance + retrieval — for AI chats and for real papers, letters, pictures, and movies.</p>
    </header>
    <div class="panel">
      <p>Clippers already exist. ChatVault competes by refusing to collapse a conversation into a vibes summary.</p>
      <ol>
        <li>Raw text is immutable after ingest. Slide a finished chat onto ingest when the conversation is done.</li>
        <li>AI conversations vs real records: <code>origin_class</code> is <code>ai_generated</code> or <code>human_record</code>. Search <code>origin:ai</code> / <code>origin:human</code>.</li>
        <li>Source AI and source file stay attached. Domain Architect audits drain in as real FRA reports, not proofs.</li>
        <li>Claims, theorems, and gaps are searchable fields with statuses.</li>
        <li>Private material can be kept off professional export.</li>
        <li>Books, tags, and artifacts are derived from your records. They are not a second database and not an LLM.</li>
      </ol>
    </div>
    <div class="panel" style="margin-top:1rem">
      <h3>How to search — you type, the engine ranks</h3>
      <p>You do not pick an algorithm. The box already ranks. Type the words you remember.</p>
      <ul>
        <li><code>euler identity</code> — both words must appear. Best match first, not oldest first.</li>
        <li><code>"finite-time blow-up"</code> — that exact phrase.</li>
        <li><code>euler OR navier-stokes</code> — either topic.</li>
        <li><code>origin:ai</code> / <code>origin:human</code> — AI chats vs real papers, letters, pictures, movies.</li>
        <li><code>claim:definitional</code> / <code>gap:blow-up</code> / <code>ai:Claude</code> — look only in that slot.</li>
      </ul>
      <p>Accent highlights are the words that scored. A field label (claim, gap, title) tells you <em>where</em> they hit. OPEN / CONJECTURAL on a card is the ledger, not a popularity score — an open gap can still win the ranking.</p>
      <p class="meta">The box ranks. Rare words count more. A hit in a title or claim beats the same word buried in a long paste. A near-miss spelling or a plural still counts. You never have to tune it. If a wrong card comes first, that is my bug: send the query and the record that should have won.</p>
    </div>
    <p class="meta">A React-CDN “ChatVault 2” HTML paste was recovered as historical source under docs/chatvault-audit/. It is not this product. Projects there are Books here.</p>
  `;
}

function skinSwitcher() {
  const buttons = SKIN_IDS.map((id) => {
    const skin = SKINS[id];
    const pressed = currentSkin.id === id ? "true" : "false";
    return `<button type="button" class="skin-btn" data-set-skin="${id}" aria-pressed="${pressed}" title="${escapeHtml(skin.blurb)}"><span class="skin-swatch" data-skin="${id}" aria-hidden="true"></span>${escapeHtml(skin.label)}</button>`;
  }).join("");
  return `<div class="skin-switch" role="group" aria-label="Skin">
      <span class="skin-switch-label">Skin</span>
      ${buttons}
    </div>`;
}

function shell(inner) {
  const skin = SKINS[currentSkin.id] || SKINS.steel;
  return `
    <aside class="sidebar">
      <div class="brand">
        <img class="brand-mark" src="./assets/chatvault-mark-dark.jpg" alt="ChatVault" width="168" height="168" />
      </div>
      ${nav("vault", "Vault", ICONS.vault)}
      ${nav("ingest", "+ Ingest", ICONS.ingest)}
      ${nav("books", "Books", ICONS.books)}
      ${nav("tags", "Tags", ICONS.tags)}
      ${nav("artifacts", "Artifacts", ICONS.artifacts)}
      ${nav("dashboard", "Dashboard", ICONS.dashboard)}
      ${nav("export", "Export", ICONS.export)}
      ${nav("guide", "Guide", ICONS.guide)}
      ${nav("privacy", "Privacy", ICONS.privacy)}
      ${nav("disclaimer", "Disclaimer", ICONS.disclaimer)}
      ${skinSwitcher()}
      <p class="foot">${escapeHtml(skin.label)} · OS for your AI · local engine</p>
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
    else if (state.view === "books") inner = renderBooks();
    else if (state.view === "tags") inner = renderTags();
    else if (state.view === "artifacts") inner = renderArtifacts();
    else if (state.view === "dashboard") inner = renderDashboard();
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

function ingestOverrides() {
  const related = state.ingestBook.trim() ? [state.ingestBook.trim()] : undefined;
  const patch = {
    source_ai: state.ingestAi,
    visibility: state.ingestVis,
    related_projects: related,
  };
  if (state.ingestOrigin) patch.origin_class = state.ingestOrigin;
  if (state.ingestType) patch.source_type = state.ingestType;
  return patch;
}

function applyIngestResults(results, fileCount) {
  const entries = results.flatMap((r) => r.entries || []);
  const errors = results.flatMap((r) => r.errors || []);
  if (!entries.length) {
    throw new Error(errors[0]?.message || "Nothing ingestible in those files.");
  }
  store.addMany(entries);
  const quota = persistOk ? "" : " localStorage quota hit — export JSON now.";
  set({
    view: "vault",
    error: "",
    notice: `${ingestNoticeForResults(results, { fileCount })}${quota}`,
    selectedId: entries[0]?.id || null,
  });
}

function readFilePayload(file) {
  const mime = file.type || "";
  const kind = classifyFilename(file.name, mime);
  if (kind === "picture" && file.size <= MAX_IMAGE_BYTES) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve({ dataUrl: String(reader.result || ""), mime, size: file.size });
      reader.onerror = () => reject(reader.error || new Error("Could not read image."));
      reader.readAsDataURL(file);
    });
  }
  if (kind === "picture" || kind === "movie" || kind === "audio" || kind === "pdf" || kind === "docx") {
    return Promise.resolve({ mime, size: file.size });
  }
  return file.text().then((text) => ({ text, mime, size: file.size }));
}

function ingestDroppedFiles(fileList) {
  const files = [...fileList];
  return Promise.all(
    files.map((file) =>
      readFilePayload(file).then((payload) => ingestNamedSource(file.name, payload, ingestOverrides()))
    )
  ).then((results) => applyIngestResults(results, files.length));
}

function toggleStar(id) {
  const current = store.get(id);
  if (!current) return;
  store.replaceAfterSuccess(id, updateEntry(current, { starred: !current.starred }));
}

root.addEventListener("click", (ev) => {
  const star = ev.target.closest("[data-star]");
  if (star) {
    ev.preventDefault();
    ev.stopPropagation();
    toggleStar(star.dataset.star);
    set({ notice: "" });
    return;
  }
  if (ev.target.id === "recover") {
    state.fatal = null;
    set({ view: "vault", error: "", notice: "Recovered from a render error." });
    return;
  }
  const skinBtn = ev.target.closest("[data-set-skin]");
  if (skinBtn) {
    currentSkin.id = applySkin(saveSkin(skinBtn.dataset.setSkin));
    set({ notice: `Skin: ${SKINS[currentSkin.id].label}.` });
    return;
  }
  const ingestTab = ev.target.closest("[data-ingest-tab]");
  if (ingestTab) {
    set({ ingestTab: ingestTab.dataset.ingestTab, error: "", notice: "" });
    return;
  }
  const viewBtn = ev.target.closest("[data-view]");
  if (viewBtn) {
    set({ view: viewBtn.dataset.view, error: "", notice: "", page: 0 });
    return;
  }
  const open = ev.target.closest("[data-open]");
  if (open) {
    set({ view: "detail", selectedId: open.dataset.open, error: "", notice: "" });
    return;
  }
  const openBook = ev.target.closest("[data-open-book]");
  if (openBook) {
    set({ view: "vault", book: openBook.dataset.openBook, page: 0, notice: `Filtered to ${openBook.dataset.openBook}.` });
    return;
  }
  const selectTag = ev.target.closest("[data-select-tag]");
  if (selectTag) {
    set({ selectedTag: selectTag.dataset.selectTag });
    return;
  }
  const tagBtn = ev.target.closest("[data-tag]");
  if (tagBtn) {
    const next = state.tag === tagBtn.dataset.tag ? "" : tagBtn.dataset.tag;
    set({ tag: next, page: 0 });
    return;
  }
  const removeTag = ev.target.closest("[data-remove-tag]");
  if (removeTag) {
    const current = store.get(state.selectedId);
    if (!current) return;
    const nextTags = (current.search_tags || []).filter((t) => t !== removeTag.dataset.removeTag);
    store.replaceAfterSuccess(current.id, updateEntry(current, { search_tags: nextTags }));
    set({});
    return;
  }
  const toggleBook = ev.target.closest("[data-toggle-book]");
  if (toggleBook) {
    const current = store.get(state.selectedId);
    if (!current) return;
    const name = toggleBook.dataset.toggleBook;
    const has = (current.related_projects || []).includes(name);
    const related_projects = has
      ? current.related_projects.filter((b) => b !== name)
      : [...(current.related_projects || []), name];
    store.replaceAfterSuccess(current.id, updateEntry(current, { related_projects }));
    set({});
    return;
  }
  if (ev.target.id === "load-demo") {
    store.load(DEMO_ENTRIES);
    set({ view: "vault", error: "", notice: "Loaded research-memory fixtures." });
    return;
  }
  if (ev.target.id === "star-filter") {
    set({ starredOnly: !state.starredOnly, page: 0 });
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
  if (ev.target.id === "pull-da") {
    pullDaDrain()
      .then((result) => {
        if (!result.entries.length) {
          set({
            notice: `Drain at ${result.origin} had nothing queued. Start python3 -m domain_architect --drain-server, then --drain-chatvault, or drop the JSON on Files.`,
            error: "",
          });
          return;
        }
        store.addMany(result.entries);
        set({
          view: "vault",
          error: "",
          notice: `Pulled ${result.entries.length} Domain Architect audit(s) from ${result.origin}.`,
          selectedId: result.entries[0]?.id || null,
        });
      })
      .catch((err) => set({ error: err.message || String(err) }));
    return;
  }
  if (ev.target.id === "load-inbox") {
    loadInboxFromRepo()
      .then((result) => {
        if (!result.entries.length) {
          set({
            notice: `Inbox at ${result.origin} had no sidecars. Run python3 -m domain_architect --ingest-chatvault PATH.`,
            error: "",
          });
          return;
        }
        store.addMany(result.entries);
        set({
          view: "vault",
          error: "",
          notice: `Loaded ${result.entries.length} inbox record(s) from ${result.origin}.`,
          selectedId: result.entries[0]?.id || null,
        });
      })
      .catch((err) => set({ error: err.message || String(err) }));
    return;
  }
  if (ev.target.id === "send-inbox") {
    postInboxExport(exportVault(store.list()))
      .then((result) => {
        set({
          notice: `Wrote ${result.count || 0} sidecar(s) to the repo inbox. Large media is not uploaded; use CLI --ingest-chatvault.`,
          error: "",
        });
      })
      .catch((err) => set({ error: err.message || String(err) }));
    return;
  }
  if (ev.target.id === "do-ingest") {
    try {
      if (state.ingestTab === "bulk") {
        const { entries, errors } = ingestBulk(state.ingestText, ingestOverrides());
        store.addMany(entries);
        const fail = errors.length ? ` ${errors.length} chunk(s) skipped.` : "";
        set({
          view: "vault",
          ingestText: "",
          error: "",
          notice: `Indexed ${entries.length} record(s).${fail}`,
          selectedId: entries[0]?.id || null,
        });
      } else {
        const entry = ingestPaste(state.ingestText, ingestOverrides());
        store.add(entry);
        set({ view: "detail", selectedId: entry.id, ingestText: "", error: "", notice: "" });
      }
    } catch (err) {
      set({ error: err.message });
    }
    return;
  }
  if (ev.target.id === "add-tags") {
    const current = store.get(state.selectedId);
    const raw = document.getElementById("new-tag")?.value || "";
    if (!current || !raw.trim()) return;
    const added = raw.split(",").map((t) => t.trim()).filter(Boolean);
    store.replaceAfterSuccess(
      current.id,
      updateEntry(current, { search_tags: [...new Set([...(current.search_tags || []), ...added])] })
    );
    set({});
    return;
  }
  if (ev.target.id === "new-book") {
    const name = window.prompt("New book name");
    if (!name || !name.trim()) return;
    const trimmed = name.trim();
    if (!state.extraBooks.includes(trimmed)) {
      state.extraBooks = [...state.extraBooks, trimmed];
      persistExtraBooks();
    }
    set({ notice: `Book “${trimmed}” is ready. Assign it on a record.` });
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
      set({ view: "vault", selectedId: null, error: "", notice: "Record deleted." });
    } catch (err) {
      set({ error: err.message });
    }
    return;
  }
  if (ev.target.id === "wipe") {
    if (!window.confirm("Delete ALL local ChatVault data on this device?")) return;
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(BOOKS_KEY);
    store.load([]);
    state.extraBooks = [];
    set({ view: "vault", selectedId: null, error: "", notice: "Local vault wiped." });
  }
});

root.addEventListener("input", (ev) => {
  if (ev.target.id === "q") state.query = ev.target.value;
  if (ev.target.id === "ingest") state.ingestText = ev.target.value;
  if (ev.target.id === "ingest-book") state.ingestBook = ev.target.value;
});

root.addEventListener("change", (ev) => {
  if (ev.target.id === "q") set({ query: ev.target.value, page: 0 });
  if (ev.target.id === "vis") set({ visibility: ev.target.value, page: 0 });
  if (ev.target.id === "ai") set({ source_ai: ev.target.value, page: 0 });
  if (ev.target.id === "origin") set({ origin_class: ev.target.value, page: 0 });
  if (ev.target.id === "stype") set({ source_type: ev.target.value, page: 0 });
  if (ev.target.id === "project") set({ project: ev.target.value, page: 0 });
  if (ev.target.id === "book") set({ book: ev.target.value, page: 0 });
  if (ev.target.id === "ingest-ai") state.ingestAi = ev.target.value;
  if (ev.target.id === "ingest-origin") state.ingestOrigin = ev.target.value;
  if (ev.target.id === "ingest-type") state.ingestType = ev.target.value;
  if (ev.target.id === "ingest-vis") state.ingestVis = ev.target.value;
  if (ev.target.id === "set-vis") {
    const current = store.get(state.selectedId);
    if (!current) return;
    store.replaceAfterSuccess(current.id, updateEntry(current, { visibility: ev.target.value }));
    set({});
    return;
  }
  if (ev.target.id === "restore" && ev.target.files?.[0]) {
    const file = ev.target.files[0];
    file
      .text()
      .then((text) => {
        const restored = importVault(JSON.parse(text));
        store.load(restored);
        set({ view: "vault", error: "", notice: `Restored ${restored.length} record(s).` });
      })
      .catch((err) => set({ error: err.message || String(err) }));
    return;
  }
  if (ev.target.id === "ingest-files" && ev.target.files?.length) {
    ingestDroppedFiles(ev.target.files).catch((err) => set({ error: err.message || String(err) }));
    return;
  }
  if (ev.target.dataset?.reviewField && ev.target.dataset?.reviewId) {
    const current = store.get(state.selectedId);
    if (!current) return;
    const next = reviewLedgerItem(current, ev.target.dataset.reviewField, ev.target.dataset.reviewId, ev.target.value, {
      humanReviewed: true,
    });
    store.replaceAfterSuccess(current.id, next);
    set({ error: "", notice: "Ledger updated." });
  }
});

function ingestDropZone(ev) {
  return ev.target.closest?.("#ingest-drop") || ev.target.closest?.("#dropzone") || null;
}

root.addEventListener("dragenter", (ev) => {
  const zone = ingestDropZone(ev);
  if (!zone) return;
  ev.preventDefault();
  document.getElementById("dropzone")?.classList.add("drag");
  document.getElementById("ingest-drop")?.classList.add("drag");
});

root.addEventListener("dragover", (ev) => {
  const zone = ingestDropZone(ev);
  if (!zone) return;
  ev.preventDefault();
  if (ev.dataTransfer) ev.dataTransfer.dropEffect = "copy";
});

root.addEventListener("dragleave", (ev) => {
  const zone = ingestDropZone(ev);
  if (!zone) return;
  if (zone.contains(ev.relatedTarget)) return;
  zone.classList.remove("drag");
  document.getElementById("dropzone")?.classList.remove("drag");
});

root.addEventListener("drop", (ev) => {
  const zone = ingestDropZone(ev);
  if (!zone) return;
  ev.preventDefault();
  document.getElementById("dropzone")?.classList.remove("drag");
  document.getElementById("ingest-drop")?.classList.remove("drag");
  if (ev.dataTransfer?.files?.length) {
    ingestDroppedFiles(ev.dataTransfer.files).catch((err) => set({ error: err.message || String(err) }));
  }
});

root.addEventListener("keydown", (ev) => {
  if (ev.target.id === "q" && ev.key === "Enter") {
    set({ query: ev.target.value, page: 0 });
  }
  if (ev.target.id === "new-tag" && ev.key === "Enter") {
    document.getElementById("add-tags")?.click();
  }
});

window.addEventListener("hashchange", () => {
  applyHash();
  render();
});

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js?v=0.7.0").catch(() => {
    /* PWA optional; engine still runs */
  });
}

applyHash();
render();
