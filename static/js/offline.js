/* OfflineDB — IndexedDB wrapper for offline-first state management */
window.OfflineDB = {
    _db: null,
    _dbName: 'CyberTeacher',
    _version: 1,

    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this._dbName, this._version);
            request.onupgradeneeded = (e) => {
                const db = e.target.result;
                if (!db.objectStoreNames.contains('state')) db.createObjectStore('state');
                if (!db.objectStoreNames.contains('chat')) db.createObjectStore('chat', { keyPath: 'id', autoIncrement: true });
                if (!db.objectStoreNames.contains('cache')) db.createObjectStore('cache', { keyPath: 'key' });
            };
            request.onsuccess = (e) => {
                this._db = e.target.result;
                resolve(this._db);
            };
            request.onerror = () => reject(request.error);
        });
    },

    async saveState(key, value) {
        if (!this._db) await this.init();
        return new Promise((resolve, reject) => {
            const tx = this._db.transaction('state', 'readwrite');
            tx.objectStore('state').put(value, key);
            tx.oncomplete = () => resolve();
            tx.onerror = () => reject(tx.error);
        });
    },

    async loadState(key) {
        if (!this._db) await this.init();
        return new Promise((resolve, reject) => {
            const tx = this._db.transaction('state', 'readonly');
            const req = tx.objectStore('state').get(key);
            req.onsuccess = () => resolve(req.result);
            req.onerror = () => reject(req.error);
        });
    },

    async saveChatMessage(msg) {
        if (!this._db) await this.init();
        return new Promise((resolve, reject) => {
            const tx = this._db.transaction('chat', 'readwrite');
            tx.objectStore('chat').add(msg);
            tx.oncomplete = () => resolve();
            tx.onerror = () => reject(tx.error);
        });
    },

    async getChatMessages(limit) {
        if (!this._db) await this.init();
        limit = limit || 50;
        return new Promise((resolve, reject) => {
            const tx = this._db.transaction('chat', 'readonly');
            const store = tx.objectStore('chat');
            const req = store.openCursor(null, 'prev');
            const results = [];
            req.onsuccess = (e) => {
                const cursor = e.target.result;
                if (cursor && results.length < limit) {
                    results.unshift(cursor.value);
                    cursor.continue();
                } else {
                    resolve(results);
                }
            };
            req.onerror = () => reject(req.error);
        });
    },

    async cacheResponse(key, value, ttlMs) {
        if (!this._db) await this.init();
        ttlMs = ttlMs || 3600000; // 1 hour default
        return new Promise((resolve, reject) => {
            const tx = this._db.transaction('cache', 'readwrite');
            tx.objectStore('cache').put({ key, value, expires: Date.now() + ttlMs });
            tx.oncomplete = () => resolve();
            tx.onerror = () => reject(tx.error);
        });
    },

    async getCachedResponse(key) {
        if (!this._db) await this.init();
        return new Promise((resolve, reject) => {
            const tx = this._db.transaction('cache', 'readonly');
            const req = tx.objectStore('cache').get(key);
            req.onsuccess = () => {
                const item = req.result;
                if (item && item.expires > Date.now()) resolve(item.value);
                else resolve(null);
            };
            req.onerror = () => reject(req.error);
        });
    },

    async clearExpired() {
        if (!this._db) await this.init();
        return new Promise((resolve, reject) => {
            const tx = this._db.transaction('cache', 'readwrite');
            const store = tx.objectStore('cache');
            const req = store.openCursor();
            let count = 0;
            req.onsuccess = (e) => {
                const cursor = e.target.result;
                if (cursor) {
                    if (cursor.value.expires <= Date.now()) {
                        cursor.delete();
                        count++;
                    }
                    cursor.continue();
                } else {
                    resolve(count);
                }
            };
            req.onerror = () => reject(req.error);
        });
    }
};
