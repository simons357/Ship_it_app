/**
 * Spatial layout for the vault. Not a notebook list.
 * Clusters = project_category (or first tag). Edges = shared tags.
 */

export const ATLAS_VERSION = "chatvault-atlas-0.1.0";

export function clusterKey(entry) {
  const project = String(entry?.project_category || "").trim();
  if (project) return project;
  const tag = (entry?.search_tags || []).find((t) => String(t).trim());
  return tag ? String(tag) : "unfiled";
}

function hash32(s) {
  let h = 2166136261;
  for (const ch of String(s)) {
    h ^= ch.charCodeAt(0);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

export function massOf(entry) {
  return (
    (entry.key_claims || []).length +
    (entry.theorems || []).length +
    (entry.open_gaps || []).length
  );
}

export function layoutConstellation(entries, { width = 920, height = 560 } = {}) {
  const list = entries || [];
  const groups = new Map();
  for (const entry of list) {
    const key = clusterKey(entry);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(entry);
  }
  const clusters = [...groups.keys()].sort();
  const cx = width / 2;
  const cy = height / 2;
  const orbit = Math.min(width, height) * 0.31;
  const nodes = [];
  const hubs = [];

  clusters.forEach((key, i) => {
    const ang = clusters.length === 1 ? -Math.PI / 2 : (i / clusters.length) * Math.PI * 2 - Math.PI / 2;
    const gx = cx + Math.cos(ang) * orbit;
    const gy = cy + Math.sin(ang) * orbit;
    const members = groups.get(key);
    hubs.push({ id: `hub:${key}`, x: gx, y: gy, cluster: key, count: members.length });
    members.forEach((entry, j) => {
      const n = members.length;
      const a2 = n === 1 ? 0 : (j / n) * Math.PI * 2 + (hash32(entry.id) % 40) / 80;
      const spread = n === 1 ? 0 : 36 + (hash32(entry.id) % 24);
      const mass = massOf(entry);
      nodes.push({
        id: entry.id,
        x: gx + Math.cos(a2) * spread,
        y: gy + Math.sin(a2) * spread,
        r: 6 + Math.min(12, mass * 2),
        cluster: key,
        title: entry.title,
        source_ai: entry.source_ai,
        visibility: entry.visibility,
        mass,
      });
    });
  });

  const byTag = new Map();
  for (const entry of list) {
    const tags = [...(entry.search_tags || []), ...(entry.project_tags || [])];
    for (const tag of tags) {
      const t = String(tag).trim();
      if (!t) continue;
      if (!byTag.has(t)) byTag.set(t, []);
      byTag.get(t).push(entry.id);
    }
  }

  const edges = [];
  const seen = new Set();
  for (const [tag, ids] of byTag) {
    const unique = [...new Set(ids)];
    if (unique.length < 2) continue;
    for (let i = 0; i < unique.length; i += 1) {
      for (let j = i + 1; j < unique.length; j += 1) {
        const a = unique[i];
        const b = unique[j];
        const key = a < b ? `${a}|${b}` : `${b}|${a}`;
        if (seen.has(key)) continue;
        seen.add(key);
        edges.push({ from: a, to: b, tag });
      }
    }
  }

  return { version: ATLAS_VERSION, width, height, clusters, hubs, nodes, edges };
}
