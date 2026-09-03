const CACHE = 'sk-v3-2026-polish';
const STATIC_ASSETS = [
  '/logo.jpg', '/og-image.jpg', '/favicon.ico', '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  if (req.mode === 'navigate' && url.origin === self.location.origin) {
    event.respondWith(
      fetch(req)
        .then(response => {
          const copy = response.clone();
          caches.open(CACHE).then(cache => cache.put('/index.html', copy));
          return response;
        })
        .catch(() => caches.match('/index.html'))
    );
    return;
  }

  if (url.origin === self.location.origin) {
    event.respondWith(
      caches.match(req).then(cached => cached || fetch(req).then(response => {
        const copy = response.clone();
        caches.open(CACHE).then(cache => cache.put(req, copy));
        return response;
      }))
    );
  }
});
