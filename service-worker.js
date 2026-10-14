const CACHE = "lumera-v42";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.json",
  "./cover.png"
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Cache-first for static assets, network-first for API
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);

  // Skip API calls — always go to network
  if (url.pathname.startsWith("/api/")) {
    return;
  }

  // Everything else: serve from cache first, then update in background
  e.respondWith(
    caches.match(e.request).then((cached) => {
      const networkFetch = fetch(e.request).then((response) => {
        if (response.ok && e.request.method === "GET") {
          const clone = response.clone();
          caches.open(CACHE).then((cache) => cache.put(e.request, clone));
        }
        return response;
      }).catch(() => cached);

      return cached || networkFetch;
    })
  );
});
