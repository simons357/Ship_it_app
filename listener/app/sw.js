self.addEventListener("install", (e) => {
  e.waitUntil(caches.open("listener-v1").then((c) => c.addAll(["./", "./index.html", "./css/app.css"])));
  self.skipWaiting();
});
self.addEventListener("activate", (e) => {
  e.waitUntil(self.clients.claim());
});
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
