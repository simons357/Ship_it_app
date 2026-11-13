# searchVault hook — do not merge products

QStack is **not** the ChatVault app. It does not contain vault search. Do not copy the ChatVault PWA, CLAIM_LEDGER, or Domain Architect into QStack.

If a later integration wants ChatVault hybrid rank over **QStack’s own notes** (or any other corpus), copy the license unit only:

1. Copy [`chatvault/js/search.mjs`](../../chatvault/js/search.mjs) into the other product.
2. Call `searchVault(records, query)`.
3. Follow [`chatvault/js/ENGINE.md`](../../chatvault/js/ENGINE.md).
4. Runnable example: [`examples/search-engine-hook/hook.mjs`](../../examples/search-engine-hook/hook.mjs) (`node examples/search-engine-hook/hook.mjs`).

```js
import { searchVault, SEARCH_ENGINE_VERSION } from "./search.mjs";

const { engine, hits } = searchVault(records, "q6 damping");
```

Missing fields are empty. This is a local ranker over **your** records, not a web crawler and not the ChatVault UI.
