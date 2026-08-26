import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  SKIN_STORAGE_KEY,
  DEFAULT_SKIN,
  SKINS,
  SKIN_IDS,
  normalizeSkin,
  loadSkin,
  saveSkin,
  applySkin,
} from "../js/skins.mjs";
import { SEARCH_ENGINE_VERSION } from "../js/search.mjs";
import { SCHEMA_VERSION } from "../js/engine.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

function read(rel) {
  return readFileSync(join(root, rel), "utf8");
}

test("steel is default; glass is not a selectable skin", () => {
  assert.equal(DEFAULT_SKIN, "steel");
  assert.equal(SKIN_STORAGE_KEY, "chatvault.skin.v1");
  assert.deepEqual([...SKIN_IDS].sort(), ["day", "ink", "signal", "steel"]);
  assert.equal("glass" in SKINS, false);
  for (const forbidden of ["glass", "morph-glass", "frosted", "morph"]) {
    assert.equal(normalizeSkin(forbidden), "steel");
  }
  assert.equal(normalizeSkin("INK"), "ink");
  assert.equal(normalizeSkin(""), "steel");
});

test("skin persistence writes only allowed ids", () => {
  const mem = new Map();
  const storage = {
    getItem: (k) => (mem.has(k) ? mem.get(k) : null),
    setItem: (k, v) => mem.set(k, String(v)),
  };
  assert.equal(loadSkin(storage), "steel");
  assert.equal(saveSkin("signal", storage), "signal");
  assert.equal(storage.getItem(SKIN_STORAGE_KEY), "signal");
  assert.equal(loadSkin(storage), "signal");
  assert.equal(saveSkin("glass", storage), "steel");
  assert.equal(storage.getItem(SKIN_STORAGE_KEY), "steel");
  storage.setItem(SKIN_STORAGE_KEY, "glass");
  assert.equal(loadSkin(storage), "steel");
  assert.equal(storage.getItem(SKIN_STORAGE_KEY), "steel");
});

test("applySkin sets data-skin and theme-color", () => {
  const attrs = new Map();
  const meta = {
    setAttribute(name, value) {
      attrs.set(`meta:${name}`, value);
    },
  };
  const doc = {
    documentElement: { dataset: {} },
    querySelector(sel) {
      return sel === 'meta[name="theme-color"]' ? meta : null;
    },
  };
  assert.equal(applySkin("ink", doc), "ink");
  assert.equal(doc.documentElement.dataset.skin, "ink");
  assert.equal(attrs.get("meta:content"), SKINS.ink.themeColor);
  assert.equal(applySkin("glass", doc), "steel");
  assert.equal(doc.documentElement.dataset.skin, "steel");
  assert.equal(attrs.get("meta:content"), "#101112");
});

test("CSS skins are variable overrides with no glass and no backdrop-filter", () => {
  const css = read("css/app.css");
  assert.match(css, /:root\[data-skin="steel"\]/);
  assert.match(css, /:root\[data-skin="ink"\]/);
  assert.match(css, /:root\[data-skin="signal"\]/);
  assert.match(css, /:root\[data-skin="day"\]/);
  assert.doesNotMatch(css, /data-skin=["']glass["']/);
  assert.doesNotMatch(css, /backdrop-filter\s*:/i);
  assert.doesNotMatch(css, /chatvault-glass-bg/);
  assert.match(css, /--bg:\s*#101112/);
  assert.match(css, /--accent:\s*#ffbf1a/);
  assert.match(css, /--accent:\s*#3ee0ff/);
  assert.match(css, /--accent:\s*#ff2ec8/);
  assert.match(css, /--accent:\s*#0a3dff/);
  assert.match(css, /--bg:\s*#fff7e8/);
});

test("PWA cache and asset query are 0.6.0; drain module is cached; old glass cache name is gone", () => {
  const sw = read("sw.js");
  const html = read("index.html");
  const app = read("js/app.js");
  const boot = read("js/skin-boot.js");
  const css = read("css/app.css");
  assert.match(sw, /chatvault-engine-v0\.6\.0/);
  assert.match(sw, /drain\.mjs/);
  assert.doesNotMatch(sw, /0\.5\.0/);
  assert.doesNotMatch(sw, /chatvault-glass-bg/);
  assert.match(sw, /skins\.mjs/);
  assert.match(sw, /skin-boot\.js/);
  assert.match(html, /app\.css\?v=0\.6\.0/);
  assert.match(html, /app\.js\?v=0\.6\.0/);
  assert.match(html, /skin-boot\.js\?v=0\.6\.0/);
  assert.match(html, /connect-src 'self' http:\/\/127\.0\.0\.1:7847 http:\/\/localhost:7847/);
  assert.match(app, /sw\.js\?v=0\.6\.0/);
  assert.match(app, /ingestDroppedFiles/);
  assert.match(app, /pullDaDrain/);
  assert.doesNotMatch(app, /ingestTextFile/);
  assert.match(css, /\.dropzone/);
  assert.match(css, /\.badge\.origin-ai/);
  assert.match(css, /\.badge\.origin-human/);
  assert.match(css, /\.vault-media/);
  assert.match(css, /\.banner\.warn/);
  assert.match(boot, /chatvault\.skin\.v1/);
  assert.doesNotMatch(boot, /glass/);
});

test("skin switcher is in the live shell; glass is not offered", () => {
  const app = read("js/app.js");
  assert.match(app, /data-set-skin/);
  assert.match(app, /skinSwitcher/);
  assert.match(app, /from "\.\/skins\.mjs"/);
  assert.doesNotMatch(app, /data-set-skin="glass"/);
  assert.doesNotMatch(app, /label:\s*"Glass"/);
});

test("search ranking and ledger schema versions stay locked", () => {
  assert.equal(SEARCH_ENGINE_VERSION, "chatvault-hybrid-0.2.0");
  assert.equal(SCHEMA_VERSION, "chatvault-engine-0.3.0");
});
