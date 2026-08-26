/* Domain Architect combined-origin service worker.
 * Network-first GET for the DA shell. Never cache POST.
 * Skip /chatvault/ so the nested ChatVault worker keeps the vault app.
 */
const CACHE = "da-shell-v2";
const SHELL = [
  "/",
  "/styles.css",
  "/da-home.js",
  "/da-search.mjs",
  "/manifest.webmanifest",
  "/favicon.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key.startsWith("da-shell-") && key !== CACHE).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  let url;
  try {
    url = new URL(req.url);
  } catch {
    return;
  }
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/chatvault/")) return;
  if (url.pathname.startsWith("/api/")) return;

  event.respondWith(
    fetch(req)
      .then((response) => {
        if (response && response.ok) {
          const copy = response.clone();
          caches.open(CACHE).then((cache) => cache.put(req, copy));
        }
        return response;
      })
      .catch(() => caches.match(req).then((cached) => cached || caches.match("/")))
  );
});
