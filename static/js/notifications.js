/* Notifications — Browser Notifications for world events, achievements */
window.Notifications = {
    _permission: 'default',
    _lastCheck: 0,
    _checkInterval: 60000, // 1 minute

    async init() {
        if (!('Notification' in window)) return;
        this._permission = Notification.permission;
        if (this._permission === 'default') {
            // Don't auto-request, wait for user action
        }
    },

    async requestPermission() {
        if (!('Notification' in window)) return 'denied';
        if (this._permission === 'granted') return 'granted';
        const result = await Notification.requestPermission();
        this._permission = result;
        return result;
    },

    send(title, body, icon) {
        if (this._permission !== 'granted') return;
        try {
            const n = new Notification(title, {
                body: body,
                icon: icon || '/icon-192.png',
                badge: '/icon-192.png',
                tag: 'cyberteacher',
                renotify: true,
            });
            n.onclick = () => { window.focus(); n.close(); };
            setTimeout(() => n.close(), 8000);
        } catch (e) { /* ignore */ }
    },

    async pollEvents() {
        if (!navigator.onLine || this._permission !== 'granted') return;
        const now = Date.now();
        if (now - this._lastCheck < this._checkInterval) return;
        this._lastCheck = now;

        try {
            const world = await apiCall('/get_world');
            if ((world.active_incidents || 0) > 0) {
                const incident = (world.incidents || [])[0];
                if (incident) {
                    this.send(
                        `\u26A0\uFE0F ${incident.title}`,
                        `${incident.desc}`,
                    );
                }
            }

            const cp = await apiCall('/get_cyberpsychosis');
            if (cp.level === 'dangerous') {
                this.send(
                    '\uD83D\uDEA8 Cyberpsychosis Critical!',
                    '\u0423\u0447\u0435\u043D\u0438\u043A \u043D\u0430 \u0433\u0440\u0430\u043D\u0438 \u043F\u0435\u0440\u0435\u0433\u0440\u0443\u0437\u043A\u0438.',
                );
            }
        } catch (e) { /* ignore */ }
    }
};
