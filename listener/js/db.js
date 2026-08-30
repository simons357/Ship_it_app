const KEY = "listener.v1";
const DB_NAME = "listener-v1";
const DB_VER = 1;

function blank() {
  return {
    deviceId: null,
    deviceName: "This phone",
    sessions: [],
    activeSessionId: null,
    breadcrumbs: [],
    nodes: [],
    notes: [],
    encounters: [],
    exclusions: [],
    cards: [],
    library: [],
    broadcasts: [],
    syncQueue: [],
    originals: {},
    pairedDevices: [],
    _sawHello: false,
  };
}

const originals = new Map();
let idb = null;

function openIDB() {
  if (idb) return Promise.resolve(idb);
  if (typeof indexedDB === "undefined") return Promise.resolve(null);
  return new Promise((resolve) => {
    try {
      const req = indexedDB.open(DB_NAME, DB_VER);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains("kv")) db.createObjectStore("kv");
        if (!db.objectStoreNames.contains("originals")) db.createObjectStore("originals");
      };
      req.onsuccess = () => {
        idb = req.result;
        resolve(idb);
      };
      req.onerror = () => resolve(null);
    } catch {
      resolve(null);
    }
  });
}

function idbReq(req) {
  return new Promise((resolve, reject) => {
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export function loadState() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return blank();
    return { ...blank(), ...JSON.parse(raw) };
  } catch {
    return blank();
  }
}

export function saveState(state) {
  const copy = { ...state, originals: {} };
  try {
    localStorage.setItem(KEY, JSON.stringify(copy));
  } catch {
    /* quota — IndexedDB still tries */
  }
  openIDB().then((db) => {
    if (!db) return;
    const tx = db.transaction("kv", "readwrite");
    tx.objectStore("kv").put(copy, "app");
  }).catch(() => {});
}

export async function hydrate() {
  const db = await openIDB();
  if (db) {
    try {
      const tx = db.transaction("kv", "readonly");
      const row = await idbReq(tx.objectStore("kv").get("app"));
      if (row && typeof row === "object") {
        try {
          localStorage.setItem(KEY, JSON.stringify({ ...row, originals: {} }));
        } catch {
          /* ignore */
        }
        return rememberDevice({ ...blank(), ...row });
      }
    } catch {
      /* fall through */
    }
  }
  return rememberDevice(loadState());
}

export function putOriginal(id, blob, meta) {
  originals.set(id, { blob, meta });
  openIDB().then((db) => {
    if (!db) return;
    const tx = db.transaction("originals", "readwrite");
    tx.objectStore("originals").put({ blob, meta }, id);
  }).catch(() => {});
  return id;
}

export function getOriginal(id) {
  return originals.get(id) || null;
}

export async function loadOriginal(id) {
  if (originals.has(id)) return originals.get(id);
  const db = await openIDB();
  if (!db) return null;
  try {
    const tx = db.transaction("originals", "readonly");
    const row = await idbReq(tx.objectStore("originals").get(id));
    if (row) originals.set(id, row);
    return row || null;
  } catch {
    return null;
  }
}

export function rememberDevice(state) {
  if (!state.deviceId) {
    state.deviceId = crypto.randomUUID();
    state.deviceName = "This phone";
  }
  return state;
}
