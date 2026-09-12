// Load the IIFE engines in Node without a browser.

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function memoryStorage() {
  const data = new Map();
  return {
    getItem(k) {
      return data.has(k) ? data.get(k) : null;
    },
    setItem(k, v) {
      data.set(String(k), String(v));
    },
    removeItem(k) {
      data.delete(k);
    },
  };
}

export function loadEngine(filename, extra = {}) {
  const code = fs.readFileSync(path.join(ROOT, filename), "utf8");
  const sandbox = {
    console,
    performance: { now: () => 0 },
    localStorage: memoryStorage(),
    document: {
      hidden: false,
      addEventListener() {},
      getElementById() {
        return null;
      },
    },
    navigator: {},
    window: null,
    globalThis: null,
    module: { exports: {} },
    exports: {},
    ...extra,
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  vm.runInNewContext(code, sandbox, { filename });
  return sandbox;
}

export { ROOT };
