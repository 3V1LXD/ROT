self.addEventListener('install', (event) => {
    console.log('Service worker installed');
});

const cacheName = 'pwa-ini-editor-v1';
const filesToCache = [
    './',
    './index.html',
    './manifest.json',
    './app.js'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(cacheName).then((cache) => {
            return cache.addAll(filesToCache);
        })
    );
    console.log('Service worker installed');
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
