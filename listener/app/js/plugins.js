/**
 * Owner apps plug in here. Listener does not borrow a stranger's weather
 * or a stranger's search. Set the URLs on this phone:
 *
 *   localStorage.setItem("listener.weather", "https://your-weather/current")
 *   localStorage.setItem("listener.search", "https://your-chatvault/listener")
 *
 * Weather GET  ?lat=&lon=  → { label, tempC, wet, source }
 * Search POST /index       → store a kept hearing (you chose this)
 * Search GET  ?q=          → { results: [{ label, t, id }] }
 */

export function ownerEndpoints() {
  try {
    return {
      weather: String(localStorage.getItem("listener.weather") || "").trim(),
      search: String(localStorage.getItem("listener.search") || "").trim(),
    };
  } catch {
    return { weather: "", search: "" };
  }
}

export async function fetchOwnerWeather(lat, lon) {
  const base = ownerEndpoints().weather;
  if (!base) return null;
  const url = new URL(base, location.href);
  if (Number.isFinite(lat)) url.searchParams.set("lat", String(lat));
  if (Number.isFinite(lon)) url.searchParams.set("lon", String(lon));
  const res = await fetch(url.toString());
  if (!res.ok) return null;
  const data = await res.json();
  if (!data || typeof data !== "object") return null;
  return {
    source: data.source || "owner-weather",
    t: Date.now(),
    lat: Number.isFinite(lat) ? lat : null,
    lon: Number.isFinite(lon) ? lon : null,
    label: String(data.label || data.weather || "").trim() || "unknown weather",
    wet: data.wet === true || /rain|drizzle|thunder|storm/i.test(String(data.label || "")),
    snow: data.snow === true || /snow|sleet|blizzard|ice/i.test(String(data.label || "")),
    tempC: Number.isFinite(data.tempC) ? data.tempC : null,
    code: data.code ?? null,
  };
}

export async function indexOwnerSearch(payload) {
  const base = ownerEndpoints().search;
  if (!base) return { ok: false, connected: false };
  try {
    const res = await fetch(new URL("index", base.endsWith("/") ? base : `${base}/`).toString(), {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });
    return { ok: res.ok, connected: true, status: res.status };
  } catch {
    return { ok: false, connected: true };
  }
}

export async function queryOwnerSearch(q) {
  const base = ownerEndpoints().search;
  if (!base) return { ok: false, connected: false, results: [] };
  try {
    const url = new URL(base, location.href);
    url.searchParams.set("q", q);
    const res = await fetch(url.toString());
    if (!res.ok) return { ok: false, connected: true, results: [] };
    const data = await res.json();
    return { ok: true, connected: true, results: Array.isArray(data.results) ? data.results : [] };
  } catch {
    return { ok: false, connected: true, results: [] };
  }
}
