/* Tab: Stats (advanced analytics dashboard) */
window.Tab_stats = {
    async render(el) {
        const [stats, heat, skills, world, cp, episodes] = await Promise.all([
            apiCall('/get_detailed_stats'),
            apiCall('/get_heatmap'),
            apiCall('/get_skills'),
            apiCall('/get_world'),
            apiCall('/get_cyberpsychosis'),
            apiCall('/get_episodes'),
        ]);

        el.innerHTML = `
            <h2>\uD83D\uDCC8 \u0410\u043D\u0430\u043B\u0438\u0442\u0438\u043A\u0430</h2>

            <div class="grid-3">
                <div class="card" style="text-align:center;">
                    <div style="font-size:2.5rem; color:var(--accent);">${stats.xp || 0}</div>
                    <div style="color:var(--text-secondary);">XP</div>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2.5rem; color:var(--accent);">Lvl ${stats.level || 1}</div>
                    <div style="color:var(--text-secondary);">\u0423\u0440\u043E\u0432\u0435\u043D\u044C</div>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2.5rem; color:var(--accent);">${stats.streak || 0}</div>
                    <div style="color:var(--text-secondary);">\u0421\u0442\u0440\u0438\u043A \u0434\u043D\u0435\u0439</div>
                </div>
            </div>

            <div class="card">
                <h3>\uD83C\uDFAF \u041A\u0432\u0438\u0437\u044B \u0438 \u0437\u0430\u0434\u0430\u043D\u0438\u044F</h3>
                <div class="grid-2">
                    <div>\u041F\u0440\u043E\u0439\u0434\u0435\u043D\u043E \u043A\u0432\u0438\u0437\u043E\u0432: <strong>${stats.total_quizzes || 0}</strong></div>
                    <div>\u0420\u0435\u0448\u0435\u043D\u043E \u0437\u0430\u0434\u0430\u043D\u0438\u0439: <strong>${stats.total_tasks || 0}</strong></div>
                </div>
            </div>

            <div class="card">
                <h3>\uD83D\uDCCA \u041D\u0430\u0432\u044B\u043A\u0438</h3>
                <div id="skillsRadar"></div>
                <div class="grid-3" style="margin-top:12px;">
                    ${(skills.skills || []).map(s => `
                        <div style="padding:6px; border-left:3px solid var(--accent);">
                            <strong>${s.name || s.id}</strong>
                            <div style="color:var(--text-secondary); font-size:0.8rem;">XP: ${s.xp || 0} | \u0423\u0440: ${s.level || 0}</div>
                            <div style="background:var(--bg-primary); height:4px; border-radius:2px; margin-top:4px;">
                                <div style="width:${Math.min(100, ((s.level || 0) / 5) * 100)}%; height:100%; background:var(--accent); border-radius:2px;"></div>
                            </div>
                        </div>
                    `).join('') || '<div style="color:var(--text-secondary)">\u041D\u0435\u0442 \u0434\u0430\u043D\u043D\u044B\u0445</div>'}
                </div>
            </div>

            <div class="card">
                <h3>\uD83D\uDD25 \u0410\u043A\u0442\u0438\u0432\u043D\u043E\u0441\u0442\u044C</h3>
                <div id="statsHeatmap"></div>
            </div>

            <div class="card">
                <h3>\uD83C\uDF0D \u041C\u0438\u0440</h3>
                <div class="grid-3">
                    <div>\u0418\u043D\u0446\u0438\u0434\u0435\u043D\u0442\u043E\u0432: <strong>${world.active_incidents || 0}</strong></div>
                    <div>\u0420\u0435\u0448\u0435\u043D\u043E: <strong>${world.resolved_incidents || 0}</strong></div>
                    <div>\u0424\u0440\u0430\u043A\u0446\u0438\u0439: <strong>${(world.discovered_factions || []).length}</strong></div>
                </div>
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

            <div class="card">
                <h3>\uD83D\uDCCB \u041F\u0430\u043C\u044F\u0442\u044C (${(episodes.stats?.total_episodes || 0})</h3>
                <div class="grid-2">
                    ${Object.entries(episodes.stats?.by_category || {}).map(([cat, count]) => `
                        <div>${cat}: <strong>${count}</strong></div>
                    `).join('')}
                </div>
            </div>

            <div class="card">
                <h3>\u2699\uFE0F \u0421\u0438\u0441\u0442\u0435\u043C\u0430</h3>
                <div class="grid-3">
                    <div>\u0421\u043B\u0430\u0431\u044B\u0435 \u0442\u0435\u043C\u044B: <strong>${(stats.weak_topics || []).length}</strong></div>
                    <div>\u041F\u043E\u0441\u0435\u0449\u0435\u043D\u0438\u0435: <strong>${stats.session_minutes || 0} \u043C\u0438\u043D</strong></div>
                    <div>\u0421\u0442\u0440\u0430\u0442\u0435\u0433\u0438\u044F: <strong>${stats.total_quizzes || 0} \u043A\u0432\u0438\u0437\u043E\u0432</strong></div>
                </div>
            </div>
        `;

        // Render heatmap
        if (window.Heatmap) {
            const hmContainer = document.getElementById('statsHeatmap');
            Heatmap.render(hmContainer, heat.heatmap || []);
        }
        // Render skills radar
        if (skills.skills && skills.skills.length >= 3) {
            Tab_profile._renderRadar(document.getElementById('skillsRadar'), skills.skills);
        }
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
