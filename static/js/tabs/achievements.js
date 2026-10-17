/* Tab: Achievements */
window.Tab_achievements = {
    async render(el) {
        const ach = await apiCall('/get_achievements_list');
        const earnedCount = (ach.achievements || []).filter(a => a.earned).length;
        el.innerHTML = `<h2>\uD83C\uDFC6 \u0414\u043E\u0441\u0442\u0438\u0436\u0435\u043D\u0438\u044F</h2>
        <div id="achievementsRisk" style="margin-bottom:12px;"></div>
        <div class="card">\u041F\u043E\u043B\u0443\u0447\u0435\u043D\u043E: ${earnedCount} / ${(ach.achievements || []).length}</div>
        <div class="grid-2">${(ach.achievements || []).map(a => `
            <div class="card" style="${a.earned ? 'border-color: var(--accent)' : ''}">${a.earned ? '\u2705 ' : '\uD83D\uDD12 '} ${a.name}<br><small>${a.desc}</small>${a.earned ? ` <span class="badge">+${a.xp || 0} XP</span>` : ''}</div>
        `).join('')}</div>`;
        this._updateRisk(el);
    },

    async _updateRisk() {
        const container = document.getElementById('achievementsRisk');
        if (!container) return;
        try {
            const [noise, trace, debts] = await Promise.all([
                apiCall('/api/noise'),
                apiCall('/api/trace'),
                apiCall('/api/debts'),
            ]);
            const noisePct = Math.min(noise.level || 0, 100);
            const noiseColor = noisePct > 70 ? 'var(--error)' : noisePct > 40 ? 'var(--warning, orange)' : 'var(--success)';
            const traceActive = trace.active && !trace.expired;
            const tracePct = traceActive ? Math.min((trace.remaining_seconds || 0) / 180 * 100, 100) : 0;
            container.innerHTML = `
                <div class="card">
                    <h3>\uD83D\uDCCA Risk Status</h3>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between;"><span>\uD83D\uDCF4 Noise</span><span>${noisePct}%</span></div>
                        <div style="height:8px; background:var(--bg-secondary); border-radius:4px; overflow:hidden;"><div style="width:${noisePct}%; height:100%; background:${noiseColor}; border-radius:4px; transition: width 0.5s;"></div></div>
                    </div>
                    <div style="margin-bottom:8px; display:${traceActive ? 'block' : 'none'};">
                        <div style="display:flex; justify-content:space-between;"><span>\uD83D\uDD0D Trace</span><span>${Math.ceil((trace.remaining_seconds || 0) / 60)}m ${(trace.remaining_seconds || 0) % 60}s</span></div>
                        <div style="height:8px; background:var(--bg-secondary); border-radius:4px; overflow:hidden;"><div style="width:${tracePct}%; height:100%; background:var(--error); border-radius:4px; transition: width 1s;"></div></div>
                        <div style="font-size:0.75rem; color:var(--text-secondary);">Target: ${trace.target || '?'}</div>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between;"><span>\uD83D\uDCB3 Debts</span><span style="color:${(debts.total || 0) >= 5 ? 'var(--error)' : (debts.total || 0) >= 3 ? 'orange' : 'inherit'};">${debts.total || 0}</span></div>
                    </div>
                </div>
            `;
        } catch (e) { /* silent */ }
    }
};
