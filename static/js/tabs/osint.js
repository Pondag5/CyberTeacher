/* Tab: OSINT — APT groupings + News */
window.Tab_osint = {
    async render(el) {
        el.innerHTML = `<h2>\uD83D\uDD0D OSINT / Threat Intel</h2>
        <div style="display:flex; gap:12px; align-items:center; margin-bottom:16px;">
            <span class="badge" style="cursor:pointer;" onclick="window.Tab_osint._selectGrouping('country')">\uD83C\uDF0D \u041F\u043E \u0441\u0442\u0440\u0430\u043D\u0430\u043C</span>
            <span class="badge" style="cursor:pointer;" onclick="window.Tab_osint._selectGrouping('tactic')">\uD83C\uDFAF \u041F\u043E \u0442\u0430\u043A\u0442\u0438\u043A\u0430\u043C</span>
            <span class="badge" style="cursor:pointer;" onclick="window.Tab_osint._selectGrouping('tool')">\uD83D\uDD27 \u041F\u043E \u0438\u043D\u0441\u0442\u0440\u0443\u043C\u0435\u043D\u0442\u0430\u043C</span>
        </div>
        <div id="osintGroupings"></div>
        <div id="osintNews"></div>`;
        this._loadThreats();
        this._loadNews();
    },

    _selectGrouping(type) {
        const container = document.getElementById('osintGroupings');
        if (!container) return;
        container.innerHTML = '<p style="color:var(--text-secondary);">\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430...</p>';
        apiCall('/get_threats').then(res => {
            const threats = res.threats || [];
            if (!threats.length) {
                container.innerHTML = '<p style="color:var(--text-secondary);">\u041D\u0435\u0442 \u0434\u0430\u043D\u043D\u044B\u0445 \u043E\u0431 \u0443\u0433\u0440\u043E\u0437\u0430\u0445</p>';
                return;
            }
            let html = '';
            if (type === 'country') {
                const byCountry = {};
                threats.forEach(t => {
                    const country = t.country || 'Unknown';
                    if (!byCountry[country]) byCountry[country] = [];
                    byCountry[country].push(t);
                });
                html = Object.keys(byCountry).sort().map(c => `
                    <div class="card" style="margin:8px 0;">
                        <h4>\uD83C\uDF0D ${c} (${byCountry[c].length})</h4>
                        ${byCountry[c].map(t => `<div style="margin:4px 0;"><strong>${t.name}</strong> ${t.targets ? '\u2014 ' + t.targets : ''}</div>`).join('')}
                    </div>
                `).join('');
            } else if (type === 'tactic') {
                const byTactic = {};
                threats.forEach(t => {
                    (t.tactics || ['General']).forEach(tac => {
                        if (!byTactic[tac]) byTactic[tac] = [];
                        byTactic[tac].push(t.name);
                    });
                });
                html = Object.keys(byTactic).sort().map(tac => `
                    <div class="card" style="margin:8px 0;">
                        <h4>\uD83C\uDFAF ${tac} (${byTactic[tac].length})</h4>
                        <div style="font-size:0.85rem; color:var(--text-secondary);">${byTactic[tac].join(', ')}</div>
                    </div>
                `).join('');
            } else if (type === 'tool') {
                const byTool = {};
                threats.forEach(t => {
                    (t.tools || ['Unknown']).forEach(tool => {
                        if (!byTool[tool]) byTool[tool] = [];
                        byTool[tool].push(t.name);
                    });
                });
                const sorted = Object.keys(byTool).sort((a, b) => byTool[b].length - byTool[a].length);
                html = sorted.map(tool => `
                    <div class="card" style="margin:8px 0;">
                        <h4>\uD83D\uDD27 ${tool} (${byTool[tool].length})</h4>
                        <div style="font-size:0.85rem; color:var(--text-secondary);">${byTool[tool].join(', ')}</div>
                    </div>
                `).join('');
            }
            container.innerHTML = html;
        }).catch(() => {
            container.innerHTML = '<p style="color:var(--error);">\u041E\u0448\u0438\u0431\u043A\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043A\u0438 \u0434\u0430\u043D\u043D\u044B\u0445</p>';
        });
    },

    async _loadThreats() {
        const container = document.getElementById('osintGroupings');
        if (!container) return;
        this._selectGrouping('country');
    },

    async _loadNews() {
        const container = document.getElementById('osintNews');
        if (!container) return;
        container.innerHTML = '<p style="color:var(--text-secondary);">\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430 \u043D\u043E\u0432\u043E\u0441\u0442\u0435\u0439...</p>';
        const res = await apiCall('/get_news');
        const news = res.news || [];
        container.innerHTML = `<h3 style="margin-top:20px;">\uD83D\uDCF0 \u041D\u043E\u0432\u043E\u0441\u0442\u0438 \u043A\u0438\u0431\u0435\u0440\u0431\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u043E\u0441\u0442\u0438</h3>
        ${news.length ? news.slice(0, 8).map(n => `
            <div class="card" style="margin:6px 0; padding:10px 16px;">
                <div style="display:flex; align-items:flex-start; gap:8px;">
                    <span>\uD83D\uDCF0</span>
                    <div>
                        <strong>${typeof n === 'string' ? n : n.title || n}</strong>
                        ${n.desc ? `<div style="font-size:0.85rem; color:var(--text-secondary); margin-top:4px;">${n.desc}</div>` : ''}
                        ${n.link ? `<div style="margin-top:4px;"><a href="${n.link}" target="_blank" style="font-size:0.8rem;">\uD83D\uDD17 \u0427\u0438\u0442\u0430\u0442\u044C</a></div>` : ''}
                        ${n.source ? `<div style="font-size:0.75rem; color:var(--text-secondary); margin-top:2px;">${n.source}</div>` : ''}
                    </div>
                </div>
            </div>
        `).join('') : '<p style="color:var(--text-secondary);">\u041D\u043E\u0432\u043E\u0441\u0442\u0435\u0439 \u043F\u043E\u043A\u0430 \u043D\u0435\u0442. \u041F\u043E\u043F\u0440\u043E\u0431\u0443\u0439\u0442\u0435 \u043F\u043E\u0437\u0436\u0435.</p>'}`;
    }
};
