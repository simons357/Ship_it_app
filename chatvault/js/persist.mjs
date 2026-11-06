/**
 * Vault persistence: IndexedDB when present, localStorage otherwise.
 * This is device memory, not multi-device sync.
 */

export const VAULT_IDB = "chatvault";
export const VAULT_STORE = "kv";
export const VAULT_KEY = "export";
export const LS_KEY = "chatvault.engine.v1";

function idbAvailable() {
  return typeof indexedDB !== "undefined";
}

function openDb() {
  return new Promise((resolve) => {
    if (!idbAvailable()) return resolve(null);
    const req = indexedDB.open(VAULT_IDB, 1);
    req.onupgradeneeded = () => {
      if (!req.result.objectStoreNames.contains(VAULT_STORE)) {
        req.result.createObjectStore(VAULT_STORE);
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => resolve(null);
  });
}

export async function savePersistent(payload, localStorageLike) {
  const ls = localStorageLike === undefined ? globalThis.localStorage : localStorageLike;
  const json = JSON.stringify(payload);
  try {
    ls?.setItem?.(LS_KEY, json);
  } catch {
    /* quota — try IDB only */
  }
  const db = await openDb();
  if (!db) return { localStorage: true, idb: false };
  return new Promise((resolve) => {
    const tx = db.transaction(VAULT_STORE, "readwrite");
    tx.objectStore(VAULT_STORE).put(payload, VAULT_KEY);
    tx.oncomplete = () => resolve({ localStorage: true, idb: true });
    tx.onerror = () => resolve({ localStorage: true, idb: false });
  });
}

export async function clearPersistent(localStorageLike) {
  const ls = localStorageLike === undefined ? globalThis.localStorage : localStorageLike;
  try {
    ls?.removeItem?.(LS_KEY);
  } catch {
    /* ignore */
  }
  const db = await openDb();
  if (!db) return { localStorage: true, idb: false };
  return new Promise((resolve) => {
    const tx = db.transaction(VAULT_STORE, "readwrite");
    tx.objectStore(VAULT_STORE).delete(VAULT_KEY);
    tx.oncomplete = () => resolve({ localStorage: true, idb: true });
    tx.onerror = () => resolve({ localStorage: true, idb: false });
  });
}

export async function loadPersistent(importVault, localStorageLike) {
  const ls = localStorageLike === undefined ? globalThis.localStorage : localStorageLike;
  const db = await openDb();
  if (db) {
    const fromIdb = await new Promise((resolve) => {
      const tx = db.transaction(VAULT_STORE, "readonly");
      const req = tx.objectStore(VAULT_STORE).get(VAULT_KEY);
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => resolve(null);
    });
    if (fromIdb?.format === "chatvault-export") {
      try {
        return importVault(fromIdb);
      } catch {
        /* fall through */
      }
    }
  }
  try {
    const raw = ls?.getItem?.(LS_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (parsed.format === "chatvault-export") return importVault(parsed);
    if (Array.isArray(parsed)) return parsed;
  } catch {
    /* demo fallback at caller */
  }
  return null;
}

export const BENCH_HISTORY_KEY = "chatvault.bench.history.v1";

export function loadBenchHistory(storage) {
  const store = storage === undefined ? globalThis.localStorage : storage;
  try {
    const raw = store?.getItem?.(BENCH_HISTORY_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function appendBenchHistory(summary, storage) {
  const store = storage === undefined ? globalThis.localStorage : storage;
  const prev = loadBenchHistory(store);
  const next = [
    {
      at: summary.at,
      pass: summary.pass,
      mean_ndcg5: summary.mean_ndcg5,
      mean_mrr: summary.mean_mrr,
      mean_took_ms: summary.mean_took_ms,
      engine: summary.engine,
    },
    ...prev,
  ].slice(0, 52);
  try {
    store?.setItem?.(BENCH_HISTORY_KEY, JSON.stringify(next));
  } catch {
    /* quota */
  }
  return next;
}
