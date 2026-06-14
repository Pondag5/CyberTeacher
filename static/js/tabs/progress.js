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
        `;
        if (window.Heatmap) {
            const container = document.getElementById('heatmapContainer');
            Heatmap.render(container, heat.heatmap || []);
        }
    }
};
