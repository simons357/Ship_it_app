export const SKIN_STORAGE_KEY = "chatvault.skin.v1";
export const DEFAULT_SKIN = "nocturne";

/**
 * Glass / morph-glass is the Base44 look. It is not a selectable skin here.
 * Invalid names fall back to Nocturne.
 */
export const SKINS = {
  nocturne: {
    id: "nocturne",
    label: "Nocturne",
    blurb: "Mysterious — ink hall, quiet gold",
    themeColor: "#0b0a08",
  },
  vellum: {
    id: "vellum",
    label: "Vellum",
    blurb: "Classy — paper, oxblood, serif",
    themeColor: "#f3ead8",
  },
  observatory: {
    id: "observatory",
    label: "Observatory",
    blurb: "Artsy — midnight indigo, star copper",
    themeColor: "#070b18",
  },
  steel: {
    id: "steel",
    label: "Steel",
    blurb: "Charcoal + amber",
    themeColor: "#101112",
  },
  ink: {
    id: "ink",
    label: "Ink",
    blurb: "Near-black + ice",
    themeColor: "#050608",
  },
  signal: {
    id: "signal",
    label: "Signal",
    blurb: "Navy + magenta",
    themeColor: "#06040c",
  },
  day: {
    id: "day",
    label: "Day",
    blurb: "Paper + cobalt",
    themeColor: "#fff7e8",
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
    const raw = store?.getItem?.(SKIN_STORAGE_KEY);
    const skin = normalizeSkin(raw);
    if (raw !== skin) {
      try {
        store?.setItem?.(SKIN_STORAGE_KEY, skin);
      } catch {
        /* quota */
      }
    }
    return skin;
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
    /* private mode */
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
