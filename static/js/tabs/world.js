/* Tab: World — with live WS notifications */
window.Tab_world = {
    _ws: null,

    async render(el) {
        await this._loadData(el);
        this._connectWS(el);
    },

    async _loadData(el) {
        const [world, episodes, cp] = await Promise.all([
            apiCall('/get_world'),
            apiCall('/get_episodes'),
            apiCall('/get_cyberpsychosis'),
        ]);

        el.innerHTML = `
            <h2>\uD83C\uDF0D Persistent World</h2>
            <div id="worldNotifications" style="max-height:100px; overflow-y:auto; margin-bottom:16px;"></div>

            <div class="grid-3">
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem;">\u26A0\uFE0F</div>
                    <div id="incidentsCount" style="font-size:1.8rem; font-weight:700;">${world.active_incidents || 0}</div>
                    <p>\u0410\u043A\u0442\u0438\u0432\u043D\u044B\u0445 \u0438\u043D\u0446\u0438\u0434\u0435\u043D\u0442\u043E\u0432</p>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem;">\u2694\uFE0F</div>
                    <div id="factionsCount" style="font-size:1.8rem; font-weight:700;">${(world.discovered_factions || []).length}</div>
                    <p>\u0418\u0437\u0432\u0435\u0441\u0442\u043D\u044B\u0445 \u0444\u0440\u0430\u043A\u0446\u0438\u0439</p>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem;">\uD83D\uDCA1</div>
                    <div id="knowledgeCount" style="font-size:1.8rem; font-weight:700;">${(world.unlocked_knowledge || []).length}</div>
                    <p>\u0420\u0430\u0437\u0431\u043B\u043E\u043A\u0438\u0440\u043E\u0432\u0430\u043D\u043D\u044B\u0445 \u0442\u0435\u043C</p>
                </div>
            </div>

            ${(world.incidents || []).length > 0 ? `
            <div class="card" id="incidentsList">
                <h3>\u26A0\uFE0F \u0410\u043A\u0442\u0438\u0432\u043D\u044B\u0435 \u0438\u043D\u0446\u0438\u0434\u0435\u043D\u0442\u044B</h3>
                ${world.incidents.map(inc => `
                    <div style="padding:8px 0; border-bottom:1px solid var(--border);">
                        <span class="badge">${inc.severity}</span> <strong>${inc.title}</strong>
                        <p style="color:var(--text-secondary); margin-top:4px;">${inc.desc}</p>
                    </div>
                `).join('')}
            </div>
            ` : '<div class="card" style="color:var(--text-secondary)">\u0418\u043D\u0446\u0438\u0434\u0435\u043D\u0442\u043E\u0432 \u043D\u0435\u0442. \u041C\u0438\u0440 \u0441\u043F\u043E\u043A\u043E\u0439\u0435\u043D.</div>'}

            ${(world.discovered_factions || []).length > 0 ? `
            <div class="card">
                <h3>\u2694\uFE0F \u0424\u0440\u0430\u043A\u0446\u0438\u0438</h3>
                ${world.discovered_factions.map(f => `<span class="badge" style="margin:4px;">${f}</span>`).join('')}
            </div>
            ` : ''}

            <div class="card">
                <h3>\uD83D\uDCCB \u0412\u0430\u0436\u043D\u044B\u0435 \u043C\u043E\u043C\u0435\u043D\u0442\u044B (${(episodes.episodes || []).length})</h3>
                ${(episodes.episodes || []).slice(0, 5).map(ep => {
                    const icons = { breakthrough: '\uD83C\uDFAF', failure: '\uD83D\uDCA5', discovery: '\uD83D\uDD0D', milestone: '\uD83C\uDFC6' };
                    return `<div style="padding:4px 0;">${icons[ep.category] || '\uD83D\uDCCC'} ${ep.title}</div>`;
                }).join('') || '<div style="color:var(--text-secondary)">\u041F\u0443\u0441\u0442\u043E</div>'}
            </div>

            <div class="card">
                <h3>\uD83E\uDDE0 Cyberpsychosis</h3>
                <div class="grid-3">
                    ${this._bar('\u0421\u0442\u0440\u0435\u0441\u0441', cp.state?.stress || 0, 60)}
                    ${this._bar('\u041E\u0431\u044A\u044F\u0434\u0435\u043D\u0438\u0435', cp.state?.obsession || 0, 60)}
                    ${this._bar('\u0411\u0435\u0441\u0440\u0430\u0441\u0441\u0438\u0435', cp.state?.recklessness || 0, 60)}
                </div>
                <p style="margin-top:8px; color:var(--text-secondary);">\u0423\u0440\u043E\u0432\u0435\u043D\u044C: <span class="badge">${cp.level || 'normal'}</span></p>
            </div>
        `;
    },

    _connectWS(el) {
        if (this._ws) this._ws.close();
        try {
            const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
            const token = localStorage.getItem('auth_token') || '';
            this._ws = new WebSocket(`${protocol}//${location.host}/notifications${token ? '?token=' + token : ''}`);
            this._ws.onmessage = (e) => {
                try {
                    const data = JSON.parse(e.data);
                    if (data.type === 'incident' || data.type === 'cyberpsychosis') {
                        this._addNotification(data);
                        this._refreshCounters();
                    }
                } catch (err) { /* ignore */ }
            };
            this._ws.onclose = () => setTimeout(() => this._connectWS(el), 15000);
        } catch (e) { /* ws not available */ }
    },

    _addNotification(data) {
        const container = document.getElementById('worldNotifications');
        if (!container) return;
        const item = document.createElement('div');
        item.className = 'card';
        item.style.cssText = 'padding:8px 12px; margin-bottom:6px; border-left:3px solid var(--accent); animation: slideIn 0.3s ease;';
        const icon = data.type === 'incident' ? '\u26A0\uFE0F' : '\uD83D\uDEA8';
        item.innerHTML = `${icon} <strong>${data.data?.title || data.data?.level || data.type}</strong> <span style="color:var(--text-secondary); font-size:0.8rem;">\u2014 \u0442\u043E\u043B\u044C\u043A\u043E \u0447\u0442\u043E</span>`;
        container.prepend(item);
        if (window.Sounds) Sounds.notification();
        setTimeout(() => { item.style.opacity = '0'; item.style.transition = '0.5s'; }, 10000);
        setTimeout(() => item.remove(), 10500);
    },

    async _refreshCounters() {
        const world = await apiCall('/get_world');
        const incEl = document.getElementById('incidentsCount');
        if (incEl) incEl.textContent = world.active_incidents || 0;
    },

    _bar(label, value, threshold) {
        const color = value > threshold ? 'var(--error)' : 'var(--accent)';
        return `
            <div>${label}: <strong>${Math.round(value)}%</strong></div>
            <div style="background:var(--bg-primary); height:6px; border-radius:3px;">
                <div style="width:${Math.min(100, value)}%; height:100%; background:${color}; border-radius:3px;"></div>
            </div>
        `;
    }
};
