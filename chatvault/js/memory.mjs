/**
 * Persistent search memory on this device.
 * Records queries and opens. Session context can nudge same-project hits.
 * It is not a second ranker and not a cloud brain.
 */

export const MEMORY_KEY = "chatvault.memory.v1";
export const MEMORY_VERSION = "chatvault-memory-0.1.0";

export function emptyMemory() {
  return {
    version: MEMORY_VERSION,
    queries: [],
    opens: [],
    lastProject: "",
    lastQuery: "",
    lastOpenedId: "",
  };
}

export function loadMemory(storage) {
  const store = storage === undefined ? globalThis.localStorage : storage;
  try {
    const raw = store?.getItem?.(MEMORY_KEY);
    if (!raw) return emptyMemory();
    const parsed = JSON.parse(raw);
    return { ...emptyMemory(), ...parsed, version: MEMORY_VERSION };
  } catch {
    return emptyMemory();
  }
}

export function saveMemory(memory, storage) {
  const store = storage === undefined ? globalThis.localStorage : storage;
  const next = { ...emptyMemory(), ...memory, version: MEMORY_VERSION };
  try {
    store?.setItem?.(MEMORY_KEY, JSON.stringify(next));
  } catch {
    /* quota */
  }
  return next;
}

export function rememberQuery(memory, query, storage) {
  const q = String(query || "").trim();
  if (!q) return memory;
  const queries = [{ q, at: new Date().toISOString() }, ...(memory.queries || [])].slice(0, 200);
  return saveMemory({ ...memory, queries, lastQuery: q }, storage);
}

export function rememberOpen(memory, entry, storage) {
  if (!entry?.id) return memory;
  const opens = [{ id: entry.id, project: entry.project_category || "", at: new Date().toISOString() }, ...(memory.opens || [])].slice(
    0,
    200
  );
  return saveMemory({
    ...memory,
    opens,
    lastOpenedId: entry.id,
    lastProject: entry.project_category || memory.lastProject || "",
  }, storage);
}

/**
 * Tiny same-project nudge after the ranker. Factor 1.05.
 * Bench the ranker WITHOUT this. Observe it separately.
 */
export function applySessionContext(result, memory) {
  const project = memory?.lastProject;
  const lastId = memory?.lastOpenedId;
  if ((!project && !lastId) || !result?.hits?.length) {
    return { ...result, context: "none" };
  }
  const hits = result.hits
    .map((h) => {
      const projectBoost = project && h.entry.project_category === project ? 1.05 : 1;
      const recencyBoost = lastId && h.entry.id === lastId ? 1.02 : 1;
      const boost = projectBoost * recencyBoost;
      return {
        ...h,
        score: h.score * boost,
        signals: {
          ...(h.signals || {}),
          memory_project: projectBoost > 1 ? 1 : 0,
          memory_recency: recencyBoost > 1 ? 1 : 0,
        },
      };
    })
    .sort((a, b) => b.score - a.score || String(a.entry.title).localeCompare(String(b.entry.title)));
  const bits = [];
  if (project) bits.push(`project:${project}`);
  if (lastId) bits.push("recency");
  return { ...result, hits, context: bits.join("+") || "none" };
}
