import { test } from "node:test";
import assert from "node:assert/strict";
import { DEMO_ENTRIES } from "../js/engine.mjs";
import { clusterKey, layoutConstellation, massOf } from "../js/atlas.mjs";

test("constellation clusters by project and draws tag edges", () => {
  const layout = layoutConstellation(DEMO_ENTRIES, { width: 800, height: 500 });
  assert.equal(layout.nodes.length, DEMO_ENTRIES.length);
  assert.ok(layout.clusters.includes("mathematics"));
  assert.ok(layout.clusters.includes("product"));
  assert.ok(layout.edges.some((e) => e.tag === "chatvault"));
  const euler = layout.nodes.find((n) => n.title.includes("Euler"));
  assert.equal(euler.cluster, "mathematics");
  assert.ok(euler.r > 6);
});

test("layout is deterministic for the same ids", () => {
  const a = layoutConstellation(DEMO_ENTRIES);
  const b = layoutConstellation(DEMO_ENTRIES);
  assert.deepEqual(
    a.nodes.map((n) => [n.id, n.x, n.y]),
    b.nodes.map((n) => [n.id, n.x, n.y])
  );
});

test("private clinical fragment is its own cluster and has mass 0", () => {
  const clinical = DEMO_ENTRIES.find((e) => e.project_category === "clinical");
  assert.equal(clusterKey(clinical), "clinical");
  assert.equal(massOf(clinical), 0);
});
