/**
 * ChatVault drain + fat ingest.
 *
 * AI chats, Domain Architect audits, and real-world records (papers,
 * letters, pictures, movies) all land in the same vault. Origin class
 * tells them apart. This is OS for your AI — not a note-taking brand.
 *
 * Domain Architect is a math auditor. It is not ChatVault’s brain and
 * it does not prove Navier–Stokes or Riemann.
 */

import {
  emptyEntry,
  importVault,
  ingestPaste,
  ingestTextFile,
} from "./engine.mjs";

export const DRAIN_PROTOCOL = "chatvault-drain-0.1.0";
export const DA_DRAIN_URLS = Object.freeze([
  "http://127.0.0.1:7847",
  "http://localhost:7847",
]);

export function drainOrigins() {
  const extra = [];
  if (typeof location !== "undefined" && location.origin && location.origin !== "null") {
    extra.push(`${location.origin}/api/drain`);
  }
  return [...extra, ...DA_DRAIN_URLS];
}
export const MAX_IMAGE_BYTES = 12 * 1024 * 1024;
export const BROWSER_STUB_NOTICE =
  "Indexed as human record stub (binary not stored in the browser vault; use CLI --ingest-chatvault to copy into the repo inbox).";
export const INBOX_INDEX_PATHS = Object.freeze([
  "/api/inbox",
  "/chatvault/inbox/index.json",
  "./inbox/index.json",
]);

const TEXT_NAME = /\.(txt|md|markdown|json|csv|html|htm|xml|rtf|log)$/i;

export function classifyFilename(filename, mime = "") {
  const lower = String(filename || "").toLowerCase();
  const type = String(mime || "").toLowerCase();
  if (/\.(png|jpe?g|gif|webp|svg|heic|bmp|tiff?)$/i.test(lower) || type.startsWith("image/")) {
    return "picture";
  }
  if (/\.(mp4|mov|webm|mkv|avi|m4v)$/i.test(lower) || type.startsWith("video/")) return "movie";
  if (/\.(mp3|wav|m4a|aac|flac|ogg)$/i.test(lower) || type.startsWith("audio/")) return "audio";
  if (/\.pdf$/i.test(lower) || type === "application/pdf") return "pdf";
  if (/\.(docx?|odt)$/i.test(lower) || type.includes("wordprocessingml") || type.includes("msword")) {
    return "docx";
  }
  if (TEXT_NAME.test(lower) || type.startsWith("text/") || type === "application/json") return "text";
  return "other";
}

function messageText(node) {
  const msg = node?.message;
  if (!msg) return "";
  const content = msg.content;
  if (typeof content === "string") return content.trim();
  if (Array.isArray(content?.parts)) {
    return content.parts
      .map((part) => (typeof part === "string" ? part : part?.text || ""))
      .filter(Boolean)
      .join("\n")
      .trim();
  }
  if (typeof content?.text === "string") return content.text.trim();
  return "";
}

function formatNodes(nodes) {
  const lines = [];
  for (const node of nodes || []) {
    const role = node?.message?.author?.role || node?.message?.role || "";
    if (!role || role === "system") continue;
    const text = messageText(node);
    if (!text) continue;
    lines.push(`${String(role).toUpperCase()}:\n${text}`);
  }
  return lines.join("\n\n");
}

export function looksLikeChatGptConversation(value) {
  return Boolean(value && typeof value === "object" && value.mapping && typeof value.mapping === "object");
}

export function looksLikeChatGptExport(value) {
  if (!value || typeof value !== "object") return false;
  if (Array.isArray(value)) return value.some(looksLikeChatGptConversation);
  if (Array.isArray(value.conversations)) return value.conversations.some(looksLikeChatGptConversation);
  return looksLikeChatGptConversation(value);
}

function conversationBody(conv) {
  const mapping = conv.mapping || {};
  if (conv.current_node && mapping[conv.current_node]) {
    const chain = [];
    let id = conv.current_node;
    const seen = new Set();
    while (id && mapping[id] && !seen.has(id)) {
      seen.add(id);
      chain.push(mapping[id]);
      id = mapping[id].parent;
    }
    chain.reverse();
    const selected = formatNodes(chain);
    if (selected) return selected;
  }
  const roots = Object.keys(mapping).filter((id) => !mapping[id]?.parent || !mapping[mapping[id].parent]);
  const seen = new Set();
  const nodes = [];
  const walk = (id) => {
    if (!id || seen.has(id) || !mapping[id]) return;
    seen.add(id);
    nodes.push(mapping[id]);
    for (const child of mapping[id].children || []) walk(child);
  };
  for (const root of roots) walk(root);
  for (const id of Object.keys(mapping)) {
    if (!seen.has(id)) walk(id);
  }
  return formatNodes(nodes);
}

export function conversationsFromExport(value) {
  if (Array.isArray(value)) return value.filter(looksLikeChatGptConversation);
  if (Array.isArray(value?.conversations)) return value.conversations.filter(looksLikeChatGptConversation);
  if (looksLikeChatGptConversation(value)) return [value];
  return [];
}

export function ingestChatGptExport(value, overrides = {}) {
  const conversations = conversationsFromExport(value);
  const entries = [];
  const errors = [];
  conversations.forEach((conv, index) => {
    const body = conversationBody(conv);
    if (!body) {
      errors.push({ index, message: "Conversation had no user/assistant text." });
      return;
    }
    const created =
      typeof conv.create_time === "number"
        ? new Date(conv.create_time * 1000).toISOString()
        : undefined;
    try {
      entries.push(
        ingestPaste(body, {
          title: String(conv.title || "ChatGPT conversation").slice(0, 120),
          source_ai: "ChatGPT",
          source_type: "transcript",
          origin_class: "ai_generated",
          item_date: created ? created.slice(0, 10) : undefined,
          ingested_at: created,
          search_tags: ["chatgpt-export", "ai-conversation"],
          ...overrides,
          origin_class: "ai_generated",
          source_ai: overrides.source_ai && overrides.source_ai !== "unknown" ? overrides.source_ai : "ChatGPT",
          source_type: overrides.source_type || "transcript",
        })
      );
    } catch (err) {
      errors.push({ index, message: err.message || String(err) });
    }
  });
  if (!entries.length) {
    throw new Error("No ChatGPT conversations with text were found in that JSON.");
  }
  return { kind: "chatgpt", entries, errors };
}

export function looksLikeDaAudit(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  if (value.source === "domain-architect" && value.format === "chatvault-export") return true;
  return (
    typeof value.input_expression === "string" &&
    Object.prototype.hasOwnProperty.call(value, "canonical_sfe_status")
  );
}

export function ingestDaAudit(obj, overrides = {}) {
  if (obj.format === "chatvault-export") {
    return { kind: "bundle", entries: importVault(obj), errors: [] };
  }
  const expression = String(obj.input_expression || "expression");
  const narrative = String(obj.narrative || JSON.stringify(obj, null, 2));
  const evidence = obj.highest_evidence_label || "n/a";
  const status = obj.canonical_sfe_status || "unresolved";
  const entry = ingestPaste(narrative, {
    title: `DA audit: ${expression.slice(0, 72)}`,
    source_type: "da_audit",
    source_ai: "DomainArchitect",
    origin_class: "human_record",
    summary: `Domain Architect FRA audit. Evidence: ${evidence}. Canonical SFE status: ${status}. Not a proof.`,
    search_tags: ["domain-architect", "fra", "da_audit"],
    project_category: "Domain Architect",
    related_projects: ["Domain Architect"],
    ...overrides,
    origin_class: "human_record",
    source_ai: "DomainArchitect",
    source_type: "da_audit",
  });
  return { kind: "da_audit", entries: [entry], errors: [] };
}

export function isBrowserMediaStub(entry) {
  const type = entry?.source_type;
  if (!["movie", "audio", "pdf", "docx", "picture"].includes(type)) return false;
  if (entry?.file_url && String(entry.file_url).startsWith("data:")) return false;
  return !entry?.media_path;
}

function mediaStubRaw({ filename, mime, size, stored, mediaPath, sha256 }) {
  const lines = [
    `REAL ${String(classifyFilename(filename, mime) || "RECORD").toUpperCase()} ${stored ? "" : "STUB "}${filename}`,
    `mime=${mime || "unknown"}`,
    `size=${size || 0}`,
    `stored=${stored ? "data-url" : mediaPath ? "repo-media" : "metadata-only"}`,
  ];
  if (mediaPath) lines.push(`media_path=${mediaPath}`);
  if (sha256) lines.push(`sha256=${sha256}`);
  if (!stored && !mediaPath) {
    lines.push(
      "The binary is not in this vault. ChatVault indexes a searchable stub so you can look it up next to AI chats."
    );
    lines.push(BROWSER_STUB_NOTICE);
  }
  return `${lines.filter(Boolean).join("\n")}\n`;
}

export function ingestMediaStub({ filename, mime, size, dataUrl, mediaPath, sha256 }, overrides = {}) {
  const kind = classifyFilename(filename, mime);
  const stored = Boolean(dataUrl) && kind === "picture";
  const raw = mediaStubRaw({
    filename,
    mime,
    size,
    stored,
    mediaPath: mediaPath || "",
    sha256,
  });
  const tags = ["real-record", kind];
  if (mediaPath) tags.push("inbox");
  const entry = emptyEntry({
    title: String(filename || kind),
    source_type: kind === "other" ? "other" : kind,
    source_ai: "human",
    origin_class: "human_record",
    source_file: filename,
    file_url: stored ? dataUrl : "",
    media_path: mediaPath || "",
    linked_files: mediaPath ? [mediaPath] : [],
    raw_content: raw,
    content_text: raw,
    summary: stored
      ? `Real ${kind} stored as a data URL (${size || 0} bytes).`
      : mediaPath
        ? `Real ${kind} stub with repo media at ${mediaPath} (${size || 0} bytes). Not a theorem.`
        : `Real ${kind} stub — filename, type, and size only (${size || 0} bytes). ${BROWSER_STUB_NOTICE}`,
    search_tags: tags,
    ...overrides,
    origin_class: "human_record",
    source_ai: overrides.source_ai && overrides.source_ai !== "unknown" ? overrides.source_ai : "human",
    source_type: overrides.source_type || (kind === "other" ? "other" : kind),
    media_path: mediaPath || overrides.media_path || "",
  });
  return { kind: "media", entries: [entry], errors: [] };
}

function tryJsonSpecial(text, filename, overrides) {
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    return null;
  }
  if (parsed && parsed.format === "chatvault-export") {
    return { kind: "bundle", entries: importVault(parsed), errors: [] };
  }
  if (looksLikeDaAudit(parsed)) return ingestDaAudit(parsed, { source_file: filename, ...overrides });
  if (looksLikeChatGptExport(parsed)) {
    const result = ingestChatGptExport(parsed, { source_file: filename, ...overrides });
    return result;
  }
  return null;
}

function humanTextOverrides(overrides = {}) {
  return {
    source_ai: "human",
    origin_class: "human_record",
    ...overrides,
    origin_class: overrides.origin_class || "human_record",
    source_ai:
      overrides.source_ai && overrides.source_ai !== "unknown" ? overrides.source_ai : "human",
  };
}

export function ingestNamedSource(filename, payload = {}, overrides = {}) {
  const name = String(filename || "untitled");
  const mime = payload.mime || "";
  const size = payload.size || (payload.text ? payload.text.length : 0);
  const kind = classifyFilename(name, mime);
  const mediaMeta = {
    filename: name,
    mime,
    size,
    dataUrl: payload.dataUrl || "",
    mediaPath: payload.mediaPath || payload.media_path || "",
    sha256: payload.sha256 || "",
  };

  if (kind === "picture" && payload.dataUrl && size <= MAX_IMAGE_BYTES) {
    return ingestMediaStub(mediaMeta, overrides);
  }
  if (kind === "picture" || kind === "movie" || kind === "audio" || kind === "pdf" || kind === "docx") {
    return ingestMediaStub({ ...mediaMeta, dataUrl: kind === "picture" ? payload.dataUrl || "" : "" }, overrides);
  }
  if (payload.text != null) {
    const special = String(name).toLowerCase().endsWith(".json") || mime === "application/json"
      ? tryJsonSpecial(payload.text, name, overrides)
      : null;
    if (special) return special;
    const textOverrides = humanTextOverrides(overrides);
    if (TEXT_NAME.test(name) || kind === "text") {
      return ingestTextFile(name, payload.text, textOverrides);
    }
    return {
      kind: "entry",
      entries: [
        ingestPaste(payload.text, {
          ...textOverrides,
          source_file: name,
        }),
      ],
      errors: [],
    };
  }
  return ingestMediaStub(mediaMeta, overrides);
}

export function ingestNoticeForResults(results, { fileCount } = {}) {
  const list = Array.isArray(results) ? results : [results];
  const entries = list.flatMap((r) => r.entries || []);
  const errors = list.flatMap((r) => r.errors || []);
  const stubs = entries.filter(isBrowserMediaStub);
  const inbox = entries.filter((e) => e.media_path);
  const nFiles = fileCount != null ? fileCount : list.length;
  const fail = errors.length ? ` ${errors.length} skipped.` : "";
  if (!entries.length) return errors[0]?.message || "Nothing ingestible.";
  if (stubs.length) {
    return `Indexed ${entries.length} record(s) from ${nFiles} source(s).${fail} ${BROWSER_STUB_NOTICE}`;
  }
  if (inbox.length) {
    return `Indexed ${entries.length} record(s) from ${nFiles} source(s).${fail} Repo media copied beside the JSON sidecar.`;
  }
  return `Indexed ${entries.length} record(s) from ${nFiles} source(s).${fail}`;
}

function inboxFileUrl(name, indexUrl) {
  const raw = String(name || "");
  if (/^https?:\/\//i.test(raw) || raw.startsWith("/")) return raw;
  if (indexUrl.endsWith("/api/inbox")) return `/chatvault/inbox/${raw}`;
  const dir = indexUrl.replace(/index\.json$/, "");
  return `${dir}${raw}`;
}

export async function loadInboxFromRepo(fetchImpl = fetch) {
  let lastErr = new Error(
    "Repo inbox is not reachable. Start python3 -m domain_architect --site so /chatvault/inbox/ is served."
  );
  for (const url of INBOX_INDEX_PATHS) {
    try {
      const res = await fetchImpl(url);
      if (!res.ok) {
        lastErr = new Error(`Inbox ${url} returned ${res.status}.`);
        continue;
      }
      const payload = await res.json();
      if (payload && payload.format === "chatvault-export") {
        return { origin: url, entries: importVault(payload), files: [] };
      }
      const files = (payload.files || [])
        .map((item) => (typeof item === "string" ? item : item.url || item.name || ""))
        .filter(Boolean);
      const entries = [];
      const errors = [];
      for (const file of files) {
        const fileUrl = inboxFileUrl(file, url);
        try {
          const fileRes = await fetchImpl(fileUrl);
          if (!fileRes.ok) {
            errors.push({ file, message: `${fileUrl} returned ${fileRes.status}` });
            continue;
          }
          const body = await fileRes.json();
          if (body && body.format === "chatvault-export") {
            entries.push(...importVault(body));
          } else if (body && body.id && (body.raw_content || body.title)) {
            entries.push(...importVault({ format: "chatvault-export", entries: [body] }));
          }
        } catch (err) {
          errors.push({ file, message: err.message || String(err) });
        }
      }
      return { origin: url, entries, files, errors };
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr;
}

export async function postInboxExport(payload, fetchImpl = fetch) {
  const res = await fetchImpl("/api/inbox", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(body.error || `Inbox POST returned ${res.status}. Loopback --site writes JSON sidecars only.`);
  }
  return body;
}

export async function pullDaDrain(fetchImpl = fetch) {
  let lastErr = new Error("Domain Architect drain is not running on 127.0.0.1:7847.");
  for (const origin of drainOrigins()) {
    try {
      const res = await fetchImpl(`${origin}/queue`);
      if (!res.ok) {
        lastErr = new Error(`Drain ${origin} returned ${res.status}.`);
        continue;
      }
      const payload = await res.json();
      if (!payload || payload.format !== "chatvault-export") {
        lastErr = new Error("Drain did not return a ChatVault export.");
        continue;
      }
      return { origin, entries: importVault(payload), count: (payload.entries || []).length };
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr;
}
