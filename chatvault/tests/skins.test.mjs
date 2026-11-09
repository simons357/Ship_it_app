import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  DEFAULT_SKIN,
  SKINS,
  SKIN_IDS,
  SKIN_STORAGE_KEY,
  normalizeSkin,
  loadSkin,
  saveSkin,
  applySkin,
} from "../js/skins.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

test("nocturne is default; glass is not a selectable skin", () => {
  assert.equal(DEFAULT_SKIN, "nocturne");
  assert.equal(SKIN_STORAGE_KEY, "chatvault.skin.v1");
  assert.ok(SKIN_IDS.includes("nocturne"));
  assert.ok(SKIN_IDS.includes("vellum"));
  assert.ok(SKIN_IDS.includes("observatory"));
  assert.equal("glass" in SKINS, false);
  assert.equal(normalizeSkin("glass"), "nocturne");
  assert.equal(normalizeSkin("morph-glass"), "nocturne");
  assert.equal(normalizeSkin("VELLUM"), "vellum");
});

test("skin persistence rejects glass", () => {
  const mem = new Map();
  const storage = {
    getItem: (k) => (mem.has(k) ? mem.get(k) : null),
    setItem: (k, v) => mem.set(k, String(v)),
  };
  assert.equal(saveSkin("observatory", storage), "observatory");
  assert.equal(loadSkin(storage), "observatory");
  assert.equal(saveSkin("glass", storage), "nocturne");
});

test("applySkin sets data-skin", () => {
  const meta = { setAttribute() {} };
  const doc = {
    documentElement: { dataset: {} },
    querySelector: () => meta,
  };
  assert.equal(applySkin("ink", doc), "ink");
  assert.equal(doc.documentElement.dataset.skin, "ink");
});

test("CSS defines every selectable skin and no glass", () => {
  const css = readFileSync(join(root, "css/app.css"), "utf8");
  for (const id of SKIN_IDS) {
    assert.match(css, new RegExp(`data-skin="${id}"`));
  }
  assert.doesNotMatch(css, /data-skin=["']glass["']/);
});
