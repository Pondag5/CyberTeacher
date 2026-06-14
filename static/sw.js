const CACHE_STATIC = 'cyberteacher-static-v6';
const CACHE_API = 'cyberteacher-api-v4';
const CACHE_OFFLINE = 'cyberteacher-offline-v1';
const API_CACHE_MAX = 50;

const OFFLINE_HTML = `<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CyberTeacher — Offline</title>
<style>
body{background:#1e1e2e;color:#e0e0e0;font-family:Inter,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.box{text-align:center;padding:40px;max-width:400px}
h1{font-size:2rem;background:linear-gradient(135deg,#00B4D8,#9b59b6);-webkit-background-clip:text;background-clip:text;color:transparent}
p{color:#a0a0b0;margin-top:16px}
.retry{background:#00B4D8;border:none;padding:10px 24px;border-radius:30px;font-weight:600;color:#121212;cursor:pointer;margin-top:20px;font-family:inherit}
.retry:hover{background:#0096b8}
</style></head>
<body>
<div class="box">
<h1>CyberTeacher</h1>
<p>\u0412\u044B \u043E\u0444\u0444\u043B\u0430\u0439\u043D. \u041F\u043E\u0434\u043A\u043B\u044E\u0447\u0438\u0442\u0435\u0441\u044C \u043A \u0438\u043D\u0442\u0435\u0440\u043D\u0435\u0442\u0443 \u0434\u043B\u044F \u043F\u043E\u043B\u043D\u043E\u0433\u043E \u0434\u043E\u0441\u0442\u0443\u043F\u0430.</p>
<button class="retry" onclick="location.reload()">\u041F\u043E\u043F\u0440\u043E\u0431\u043E\u0432\u0430\u0442\u044C \u0441\u043D\u043E\u0432\u0430</button>
</div></body></html>`;

async function trimCache(cacheName, maxEntries) {
    const cache = await caches.open(cacheName);
    const keys = await cache.keys();
    if (keys.length > maxEntries) {
        await Promise.all(keys.slice(0, keys.length - maxEntries).map(k => cache.delete(k)));
    }
}

// --- Install ---
self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        (async () => {
            const offlineCache = await caches.open(CACHE_OFFLINE);
            await offlineCache.put(
                new Request('/offline.html'),
                new Response(OFFLINE_HTML, { headers: { 'Content-Type': 'text/html; charset=utf-8' } })
            );
        })()
    );
});

// --- Activate ---
self.addEventListener('activate', (event) => {
    event.waitUntil(
        (async () => {
            const keys = await caches.keys();
            const validCaches = new Set([CACHE_STATIC, CACHE_API, CACHE_OFFLINE]);
            const toDelete = keys.filter(k => !validCaches.has(k));
            await Promise.all(toDelete.map(k => caches.delete(k)));
            await trimCache(CACHE_STATIC, 50);
            await trimCache(CACHE_API, API_CACHE_MAX);
            await clients.claim();
        })()
    );
});

// --- Fetch ---
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Navigation requests: network first, fallback to offline page
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request).catch(async () => {
                return caches.match('/offline.html');
            })
        );
        return;
    }

    // API requests: network first, cache fallback
    if (url.pathname.startsWith('/api/') ||
        url.pathname.startsWith('/get_') || url.pathname.startsWith('/chat_') ||
        url.pathname === '/health_check' || url.pathname === '/register' ||
        url.pathname === '/login' || url.pathname === '/verify_auth') {
        event.respondWith(
            (async () => {
                try {
                    const response = await fetch(event.request);
                    if (response.ok) {
                        const cache = await caches.open(CACHE_API);
                        cache.put(event.request, response.clone());
                        trimCache(CACHE_API, API_CACHE_MAX);
                    }
                    return response;
                } catch (e) {
                    const cached = await caches.match(event.request);
                    return cached || new Response(JSON.stringify({ error: 'offline' }), {
                        headers: { 'Content-Type': 'application/json' }
                    });
                }
            })()
        );
        return;
    }

    // Static assets: network first, cache fallback (always fresh)
    event.respondWith(
        (async () => {
            try {
                const response = await fetch(event.request);
                if (response.ok && event.request.method === 'GET') {
                    const cache = await caches.open(CACHE_STATIC);
                    cache.put(event.request, response.clone());
                }
                return response;
            } catch (e) {
                const cached = await caches.match(event.request);
                return cached || new Response('', { status: 408 });
            }
        })()
    );
});

// --- Messages ---
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
