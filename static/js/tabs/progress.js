/* Tab: Progress (with SVG heatmap) */
window.Tab_progress = {
    async render(el) {
        const stats = await apiCall('/get_detailed_stats');
        const heat = await apiCall('/get_heatmap');
        el.innerHTML = `
            <h2>\uD83D\uDCCA \u041F\u0440\u043E\u0433\u0440\u0435\u0441\u0441</h2>
            <div class="card"><strong>XP:</strong> ${appState.xp} | <strong>\u0423\u0440\u043E\u0432\u0435\u043D\u044C:</strong> ${appState.level} | <strong>\u0420\u0435\u043F\u0443\u0442\u0430\u0446\u0438\u044F:</strong> ${appState.reputation}</div>
            <div class="card"><strong>\u0421\u0442\u0440\u0438\u043A:</strong> ${appState.streak} \u0434\u043D\u0435\u0439</div>
            <div class="card"><h3>\u041D\u0430\u0432\u044B\u043A\u0438</h3><div class="grid-3">${(stats.skills || []).map(s => `<div><b>${s.name}</b> ${s.level}%</div>`).join('')}</div></div>
            <div class="card"><h3>\u0421\u043B\u0430\u0431\u044B\u0435 \u0442\u0435\u043C\u044B</h3>${(stats.weak_topics || []).map(t => `<span class="badge">${t}</span> `).join('') || '\u041D\u0435\u0442'}</div>
            <div class="card"><h3>\u0410\u043A\u0442\u0438\u0432\u043D\u043E\u0441\u0442\u044C (28 \u0434\u043D\u0435\u0439)</h3><div id="heatmapContainer"></div></div>
            <div id="progressRisk" style="margin-top:16px;"></div>
        `;
        if (window.Heatmap) {
            const container = document.getElementById('heatmapContainer');
            Heatmap.render(container, heat.heatmap || []);
        }
        this._riskInterval = setInterval(() => this._updateRisk(), 10000);
        this._updateRisk();
    },

    async _updateRisk() {
        const container = document.getElementById('progressRisk');
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
