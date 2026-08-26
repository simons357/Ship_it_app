export const SKIN_STORAGE_KEY = "chatvault.skin.v1";
export const DEFAULT_SKIN = "steel";

/** Glass is not a selectable skin. Invalid or archived names fall back to Steel. */
export const SKINS = {
  steel: {
    id: "steel",
    label: "Steel",
    blurb: "Charcoal + amber",
    themeColor: "#101112",
    accent: "#ffbf1a",
  },
  ink: {
    id: "ink",
    label: "Ink",
    blurb: "Near-black + ice",
    themeColor: "#050608",
    accent: "#3ee0ff",
  },
  signal: {
    id: "signal",
    label: "Signal",
    blurb: "Navy + magenta",
    themeColor: "#06040c",
    accent: "#ff2ec8",
  },
  day: {
    id: "day",
    label: "Day",
    blurb: "Paper + cobalt",
    themeColor: "#fff7e8",
    accent: "#0a3dff",
  },
};

export const SKIN_IDS = Object.freeze(Object.keys(SKINS));

const FORBIDDEN = new Set(["glass", "morph", "morph-glass", "morphglass", "frosted", "frost"]);

export function normalizeSkin(value) {
  const id = String(value || "")
    .trim()
    .toLowerCase();
  if (!id || FORBIDDEN.has(id) || !SKINS[id]) return DEFAULT_SKIN;
  return id;
}

export function loadSkin(storage) {
  const store = storage === undefined ? globalThis.localStorage : storage;
  try {
    return normalizeSkin(store?.getItem?.(SKIN_STORAGE_KEY));
  } catch {
    return DEFAULT_SKIN;
  }
}

export function saveSkin(id, storage) {
  const store = storage === undefined ? globalThis.localStorage : storage;
  const skin = normalizeSkin(id);
  try {
    store?.setItem?.(SKIN_STORAGE_KEY, skin);
  } catch {
    /* quota / private mode */
  }
  return skin;
}

export function applySkin(id, doc = globalThis.document) {
  const skin = normalizeSkin(id);
  if (!doc?.documentElement) return skin;
  doc.documentElement.dataset.skin = skin;
  const meta = doc.querySelector?.('meta[name="theme-color"]');
  if (meta) meta.setAttribute("content", SKINS[skin].themeColor);
  return skin;
}
