/* NotificationsWS — real-time notifications via WebSocket */
window.NotificationsWS = {
    _ws: null,
    _reconnectTimer: null,
    _connected: false,

    connect() {
        if (this._ws && this._ws.readyState === WebSocket.OPEN) return;
        const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
        const token = localStorage.getItem('auth_token') || '';
        const url = `${protocol}//${location.host}/notifications${token ? '?token=' + token : ''}`;

        try {
            this._ws = new WebSocket(url);

            this._ws.onopen = () => {
                this._connected = true;
                console.log('[NotificationsWS] Connected');
                // Keep-alive ping
                this._ping();
            };

            this._ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this._handleEvent(data);
                } catch (e) { /* ignore */ }
            };

            this._ws.onclose = () => {
                this._connected = false;
                console.log('[NotificationsWS] Disconnected, reconnecting in 10s...');
                this._reconnectTimer = setTimeout(() => this.connect(), 10000);
            };

            this._ws.onerror = () => {
                this._connected = false;
            };
        } catch (e) {
            this._reconnectTimer = setTimeout(() => this.connect(), 10000);
        }
    },

    _ping() {
        if (!this._ws || this._ws.readyState !== WebSocket.OPEN) return;
        this._ws.send(JSON.stringify({ type: 'ping' }));
        setTimeout(() => this._ping(), 25000);
    },

    _handleEvent(data) {
        if (data.type === 'pong') return;

        // Narrative events from event engine
        if (data.events && Array.isArray(data.events)) {
            for (const evt of data.events) {
                this._showNarrativeBanner(evt);
            }
            return;
        }

        // Browser notification
        if (window.Notifications && Notifications._permission === 'granted') {
            if (data.type === 'incident') {
                Notifications.send(
                    `\u26A0\uFE0F ${data.data?.title || 'Incident'}`,
                    data.data?.severity || 'New incident in the world'
                );
            }
            if (data.type === 'cyberpsychosis') {
                Notifications.send(
                    '\uD83D\uDEA8 Cyberpsychosis Alert',
                    `Level: ${data.data?.level || 'unknown'}`
                );
            }
        }

        // In-app notification banner
        this._showBanner(data);
    },

    _showNarrativeBanner(evt) {
        const banner = document.createElement('div');
        banner.style.cssText = `
            position: fixed; top: 60px; right: 20px; z-index: 100;
            background: var(--bg-card); border: 1px solid var(--accent);
            border-left: 4px solid #ff00ff;
            border-radius: 12px; padding: 14px 18px; max-width: 360px;
            box-shadow: 0 4px 24px rgba(255,0,255,0.3);
            animation: slideIn 0.4s ease;
            font-family: monospace;
        `;

        const effectsHtml = evt.effects && evt.effects.length
            ? `<div style="margin-top:8px; font-size:0.8rem; color:var(--text-secondary);">[${evt.effects.join(', ')}]</div>`
            : '';

        banner.innerHTML = `
            <div style="color:#ff00ff; font-weight:700; margin-bottom:6px; font-size:0.85rem;">
                \u26A1 ${evt.title || 'Narrative Event'}
            </div>
            <div style="color:var(--text-primary); font-size:0.9rem; line-height:1.4;">
                ${evt.message || ''}
            </div>
            ${effectsHtml}
        `;
        document.body.appendChild(banner);

        setTimeout(() => { banner.style.opacity = '0'; banner.style.transition = 'opacity 0.5s'; }, 6000);
        setTimeout(() => banner.remove(), 6500);

        if (window.Sounds && Sounds.glitch) Sounds.glitch();
    },

    _showBanner(data) {
        const container = document.getElementById('content');
        if (!container) return;

        const banner = document.createElement('div');
        banner.style.cssText = `
            position: fixed; top: 60px; right: 20px; z-index: 100;
            background: var(--bg-card); border: 1px solid var(--accent);
            border-radius: 12px; padding: 12px 16px; max-width: 300px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4); animation: slideIn 0.3s ease;
        `;

        const titles = {
            incident: '\u26A0\uFE0F World Event',
            cyberpsychosis: '\uD83D\uDEA8 Cyberpsychosis',
            achievement: '\uD83C\uDFC6 Achievement',
        };

        const colors = {
            incident: 'var(--warning)',
            cyberpsychosis: 'var(--error)',
            achievement: 'var(--accent)',
        };

        const title = titles[data.type] || '\uD83D\uDD14 Notification';
        const color = colors[data.type] || 'var(--accent)';
        const body = data.data?.title || data.data?.level || JSON.stringify(data.data || '');

        banner.innerHTML = `
            <div style="color:${color}; font-weight:600; margin-bottom:4px;">${title}</div>
            <div style="color:var(--text-primary); font-size:0.9rem;">${body}</div>
        `;
        document.body.appendChild(banner);
        setTimeout(() => { banner.style.opacity = '0'; banner.style.transition = '0.5s'; }, 5000);
        setTimeout(() => banner.remove(), 5500);

        if (window.Sounds) Sounds.notification();
    },

    disconnect() {
        if (this._ws) this._ws.close();
        clearTimeout(this._reconnectTimer);
    }
};
