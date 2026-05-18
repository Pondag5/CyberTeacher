const CACHE_NAME = 'cyberteacher-v12';
const ASSETS = [
    '/',
    '/index.html',
    '/style.css',
    '/script.js',
    '/manifest.json',
    '/icon-192.png',
    '/icon-512.png'
];

// Установка Service Worker и кэширование ассетов
self.addEventListener('install', (event) => {
    // Немедленная активация нового SW
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS);
        })
    );
});

// Активация и очистка старого кэша
self.addEventListener('activate', (event) => {
    // Захват контроля над всеми вкладками
    event.waitUntil(clients.claim());
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME)
                    .map((name) => caches.delete(name))
            );
        })
    );
});

// Обработка запросов (Network First, затем Cache)
self.addEventListener('fetch', (event) => {
    // API запросы всегда идут в сеть
    if (event.request.url.includes('/api/')) {
        event.respondWith(fetch(event.request));
        return;
    }

    // Статика: сначала сеть, потом кэш (для обновлений)
    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // Кэшируем успешные ответы
                if (response && response.status === 200) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            })
            .catch(() => {
                // Если сеть недоступна — берем из кэша
                return caches.match(event.request);
            })
    );
});
