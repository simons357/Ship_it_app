import {
  DEMO_ENTRIES,
  SCHEMA_VERSION,
  LEDGER_STATUSES,
  SOURCE_AIS,
  SOURCE_TYPES,
  ingestPaste,
  ingestBulk,
  ingestTextFile,
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

const STORAGE_KEY = "chatvault.engine.v1";
const BOOKS_KEY = "chatvault.books.extra.v1";
const PAGE_SIZE = 50;
const root = document.getElementById("app");

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
  source_type: "",
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

function applyHash() {
  const raw = (location.hash || "#vault").slice(1);
  const [view, rest] = raw.split("/");
  if (view === "detail" && rest) {
    state.view = "detail";
    state.selectedId = rest;
    return;
  }
  if (view === "ingest") {
    state.view = "ingest";
    state.ingestTab = rest === "bulk" || rest === "files" ? rest : "single";
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
    book: state.book || undefined,
    tag: state.tag || undefined,
    project: state.project || undefined,
    starred: state.starredOnly || undefined,
  };
}

function rankedSearch() {
  return searchVault(store.list(), state.query, activeFilters());
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
            ? `<span class="hit-meta">BM25F ${hit.score.toFixed(2)}${hit.matched_fields.length ? ` · ${escapeHtml(hit.matched_fields.slice(0, 3).join(" · "))}` : ""}</span>`
            : `<span>${escapeHtml((e.related_projects || [])[0] || "")}</span>`;
          return `<article class="card" data-open="${escapeHtml(e.id)}">
            <div class="card-top">
              <div>
                <span class="badge">${escapeHtml(e.source_ai)}</span>
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
        <h1>Conversation Vault</h1>
        <p class="kicker">OS for your AI</p>
        <p class="meta">${stats.total} conversations indexed · ${stats.starred} starred · ${searching ? `${ranked.total} ranked · ${ranked.took_ms.toFixed(1)} ms ·` : ""} ${escapeHtml(SEARCH_ENGINE_VERSION)}</p>
      </header>
      <button class="btn" data-view="ingest">+ Ingest</button>
    </div>
    <p class="banner">Knowledge capture with provenance and a claim ledger. It does not prove theorems, verify science, or replace a human review.</p>
    <div class="search-panel">
      <div class="toolbar">
        <input type="search" id="q" placeholder='BM25F: euler identity · "finite-time blow-up" · claim:definitional · gap:blow-up · ai:Claude' value="${escapeHtml(state.query)}" />
        <button class="btn ghost" id="do-search">Search</button>
      </div>
      <p class="help">Ranked BM25F over title, claims, theorems, gaps, tags, and raw text. AND by default. OR, "phrases", and field prefixes. Ledger status is shown, never used as a score. No LLM ranking.</p>
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
        <pre class="raw">${escapeHtml(entry.raw_content)}</pre>
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
      <h1>Ingest a conversation</h1>
      <p class="kicker">Raw text is stored first. Summaries never replace it.</p>
    </header>
    <div class="tabs">
      <button class="tab" data-ingest-tab="single" aria-current="${tab === "single"}">Single</button>
      <button class="tab" data-ingest-tab="bulk" aria-current="${tab === "bulk"}">Bulk</button>
      <button class="tab" data-ingest-tab="files" aria-current="${tab === "files"}">Files</button>
    </div>
    <div class="panel">
      <p class="banner">Structured lines are optional: TITLE, SOURCE_AI, CLAIM, THEOREM, GAP, ACTION, QUESTION, TAG, BOOK, VISIBILITY. CLAIM_LEDGER starts at UNREVIEWED. Nothing is auto-PROVED. No LLM is called.</p>
      <div class="ingest-meta">
        <select id="ingest-ai">
          ${SOURCE_AIS.map((a) => `<option${state.ingestAi === a ? " selected" : ""}>${escapeHtml(a)}</option>`).join("")}
        </select>
        <select id="ingest-vis">
          <option value="professional"${state.ingestVis === "professional" ? " selected" : ""}>professional</option>
          <option value="private"${state.ingestVis === "private" ? " selected" : ""}>private</option>
        </select>
        <input type="text" id="ingest-book" placeholder="Book (optional)" value="${escapeHtml(state.ingestBook)}" />
      </div>
      ${
        tab === "files"
          ? `<p><label>Upload txt / md / json / csv / html <input type="file" id="ingest-files" accept=".txt,.md,.markdown,.json,.csv,.html,.htm,text/plain" multiple /></label></p>
             <p class="help">JSON ChatVault exports restore the bundle. Other text files become new records with source_file set.</p>`
          : `<textarea id="ingest" placeholder="${tab === "bulk" ? "Paste several records separated by a line of ---" : "Paste your conversation here…"}">${escapeHtml(state.ingestText)}</textarea>`
      }
      <p class="error">${escapeHtml(state.error)}</p>
      <p class="notice">${escapeHtml(state.notice)}</p>
      ${tab === "files" ? "" : `<p><button class="btn" id="do-ingest">${tab === "bulk" ? "Index all chunks" : "Extract &amp; index"}</button> <span class="help">Parses locally. Uses AI to extract is not a feature of this engine.</span></p>`}
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
      <div class="stat"><b>${stats.total}</b><span>Total conversations</span></div>
      <div class="stat"><b>${stats.starred}</b><span>Starred</span></div>
      <div class="stat"><b>${stats.private}</b><span>Private</span></div>
      <div class="stat"><b>${stats.claims}</b><span>Claims</span></div>
      <div class="stat"><b>${stats.theorems}</b><span>Theorems</span></div>
      <div class="stat"><b>${stats.gaps}</b><span>Open gaps</span></div>
    </div>
    <div class="detail">
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
      <p class="kicker">The tagline is “OS for your AI.” The product is provenance + retrieval.</p>
    </header>
    <div class="panel">
      <p>Clippers already exist. ChatVault competes by refusing to collapse a conversation into a vibes summary.</p>
      <ol>
        <li>Raw text is immutable after ingest.</li>
        <li>Source AI and source file stay attached.</li>
        <li>Claims, theorems, and gaps are searchable fields with statuses.</li>
        <li>Search is BM25F: inverted index, field boosts, ranked hits, highlighted snippets. AND by default, with OR, "phrases", and field prefixes. It is not a boolean dump and not an LLM.</li>
        <li>BM25F means: rare words count more, a word in a title or claim beats the same word buried in a long body, and results are ordered by score instead of dump order. You do not need to tune it. Type like a person; use <code>claim:</code> or quotes when you already know the field or the exact phrase.</li>
        <li>Private material can be kept off professional export.</li>
        <li>Books, tags, and artifacts are derived from your records. They are not a second database and not an LLM.</li>
      </ol>
    </div>
  `;
}

function shell(inner) {
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
      <p class="foot">Midnight glass · local engine · not App Store certified</p>
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
  return {
    source_ai: state.ingestAi,
    visibility: state.ingestVis,
    related_projects: related,
  };
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
  if (ev.target.id === "stype") set({ source_type: ev.target.value, page: 0 });
  if (ev.target.id === "project") set({ project: ev.target.value, page: 0 });
  if (ev.target.id === "book") set({ book: ev.target.value, page: 0 });
  if (ev.target.id === "ingest-ai") state.ingestAi = ev.target.value;
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
    const files = [...ev.target.files];
    Promise.all(
      files.map((file) =>
        file.text().then((text) => ingestTextFile(file.name, text, ingestOverrides()))
      )
    )
      .then((results) => {
        const entries = results.flatMap((r) => r.entries);
        store.addMany(entries);
        set({
          view: "vault",
          error: "",
          notice: `Indexed ${entries.length} record(s) from ${files.length} file(s).`,
        });
      })
      .catch((err) => set({ error: err.message || String(err) }));
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
  navigator.serviceWorker.register("./sw.js").catch(() => {
    /* PWA optional; engine still runs */
  });
}

applyHash();
render();
