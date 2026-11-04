/**
 * Try to ID. Never a claim. UNKNOWN stays first-class.
 * House catalog is always here. Nearby public lists (iNaturalist, GBIF)
 * pipe in when the phone is online. No invented pins. No fake confidence.
 */

import { HOUSE_CATALOG } from "./catalog.js";
import { coarseLocation } from "./contracts.js";

export function guildFromFeatures(features) {
  if (!features) return null;
  const peak = Number(features.peakHz);
  const rms = Number(features.rms) || 0;
  if (!Number.isFinite(peak) || rms < 0.008) return null;
  if (peak >= 4000 && peak <= 18000) return "dolphin";
  if (peak >= 3000 && peak <= 9000) return "insect";
  if (peak >= 800 && peak <= 7000) return "bird";
  if (peak >= 300 && peak <= 2500) return "frog";
  return null;
}

function hourWrap(hour, range) {
  if (!range || !Number.isFinite(hour)) return true;
  const [a, b] = range;
  if (a <= b) return hour >= a && hour < b;
  return hour >= a || hour < b;
}

function tokens(s) {
  return String(s || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .split(/\s+/)
    .filter((w) => w.length > 1);
}

function scoreSpecies(sp, { q, guild, hour, habitat }) {
  let score = 0;
  const blob = [sp.common, sp.scientific, sp.group, ...(sp.cues || [])].join(" ").toLowerCase();
  if (q) {
    if (blob.includes(q)) score += 8;
    for (const t of tokens(q)) {
      if (t.length < 3) continue;
      if (blob.includes(t)) score += 3;
    }
    if (score === 0) return 0;
  }
  if (guild) {
    if (guild === "bird" && sp.group === "bird") score += 2;
    if (guild === "dolphin" && sp.group === "dolphin") score += 3;
    if ((guild === "insect" || guild === "frog") && sp.group === "critter") score += 2;
  }
  if (habitat && (sp.habitats || []).includes(habitat)) score += 1;
  if (sp.hour) {
    if (hourWrap(hour, sp.hour)) score += 2;
    else score -= 3;
  } else if (sp.group === "bird" && Number.isFinite(hour) && (hour >= 20 || hour < 5)) {
    score -= 1.5;
  }
  return score;
}

/** Where you are, not a species. House / porch / yard / woods from the walk. */
export function habitatFromWalk({ role, meters, hour } = {}) {
  const d = Number(meters) || 0;
  const h = Number.isFinite(hour) ? hour : new Date().getHours();
  if (d > 200) return "woods";
  if (d > 50) return "yard";
  if (role === "scout" && d > 20) return "yard";
  if (h >= 18 || h < 6) return "porch";
  return "house";
}

function asCandidate(sp, extra = {}) {
  return {
    id: sp.id,
    common: sp.common,
    scientific: sp.scientific || "",
    group: sp.group,
    source: extra.source || sp.source || "house-catalog",
    score: extra.score ?? 0,
    maybe: true,
  };
}

/**
 * Suggest, do not name. claimed is always false.
 */
export function tryIdentify({ words = "", features = null, hour = null, habitat = "house" } = {}) {
  const q = String(words || "").trim().toLowerCase();
  const guild = guildFromFeatures(features);
  const hr = Number.isFinite(hour) ? hour : new Date().getHours();
  let scored = HOUSE_CATALOG.map((sp) => ({
    sp,
    score: scoreSpecies(sp, { q, guild, hour: hr, habitat }),
  }))
    .filter((row) => row.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 6)
    .map((row) => asCandidate(row.sp, { score: row.score, source: "house-catalog" }));

  return {
    claimed: false,
    label: q ? String(words).trim() : "UNKNOWN",
    candidates: scored,
  };
}

export function mergeCandidates(local = [], remote = []) {
  const out = [];
  const seen = new Set();
  for (const c of [...local, ...remote]) {
    if (!c?.common) continue;
    const key = String(c.scientific || c.common).toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({ ...c, maybe: true });
  }
  return out.slice(0, 8);
}

export function taxaFromInat(json) {
  const results = json?.results;
  if (!Array.isArray(results)) return [];
  const out = [];
  for (const row of results) {
    const taxon = row.taxon || row;
    const common = String(taxon.preferred_common_name || taxon.name || "").trim();
    const scientific = String(taxon.name || "").trim();
    if (!common && !scientific) continue;
    const iconic = String(taxon.iconic_taxon_name || "").toLowerCase();
    let group = "critter";
    if (iconic === "aves") group = "bird";
    if (iconic === "mammalia" && /dolphin|tursiops|stenella|delphinus/i.test(`${common} ${scientific}`)) {
      group = "dolphin";
    }
    out.push({
      id: `inat-${taxon.id || scientific || common}`,
      common: common || scientific,
      scientific,
      group,
      source: "inaturalist",
      score: 2,
      maybe: true,
    });
  }
  return out;
}

export function taxaFromGbif(json) {
  const results = json?.results;
  if (!Array.isArray(results)) return [];
  const out = [];
  for (const row of results) {
    const scientific = String(row.species || row.scientificName || "").trim();
    const common = String(row.vernacularName || "").trim();
    if (!scientific && !common) continue;
    const name = `${common} ${scientific}`;
    let group = "critter";
    if (row.class === "Aves" || /bird/i.test(name)) group = "bird";
    if (/dolphin|tursiops|stenella|delphinus/i.test(name)) group = "dolphin";
    out.push({
      id: `gbif-${row.speciesKey || row.key || scientific || common}`,
      common: common || scientific,
      scientific,
      group,
      source: "gbif",
      score: 2,
      maybe: true,
    });
  }
  return out;
}

async function fetchJson(url, ms = 4000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    const res = await fetch(url, { signal: ctrl.signal, headers: { accept: "application/json" } });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  } finally {
    clearTimeout(t);
  }
}

/** Coarse location only. Optional. Failure is silence, not a fake list. */
export async function pipeNearbyWildlife(lat, lon) {
  const coarse = coarseLocation(lat, lon);
  if (!coarse) return { ok: false, taxa: [], sources: [] };
  const inatUrl =
    `https://api.inaturalist.org/v1/observations?lat=${coarse.lat}&lng=${coarse.lon}` +
    `&radius=40&iconic_taxa=Aves,Amphibia,Mammalia,Insecta,Reptilia` +
    `&quality_grade=research&per_page=30&order=desc&order_by=created_at`;
  const gbifUrl =
    `https://api.gbif.org/v1/occurrence/search?decimalLatitude=${coarse.lat}` +
    `&decimalLongitude=${coarse.lon}&radius=50000&kingdomKey=1&limit=30`;
  const [inat, gbif] = await Promise.all([fetchJson(inatUrl), fetchJson(gbifUrl)]);
  const taxa = mergeCandidates(taxaFromInat(inat || {}), taxaFromGbif(gbif || {}));
  const sources = [];
  if (inat) sources.push("inaturalist");
  if (gbif) sources.push("gbif");
  return { ok: sources.length > 0, taxa, sources, coarse };
}
