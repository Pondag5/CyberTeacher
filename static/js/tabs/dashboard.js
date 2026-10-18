/* Tab: Dashboard */
window.Tab_dashboard = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-chart-pie"></i> Dashboard</h2><div class="card"><p class="loading">Loading dashboard...</p></div>';
        const [progress, stats, profile, noise, trace, debts] = await Promise.all([
            apiCall('/api/stats').catch(() => ({})),
            apiCall('/api/progress').catch(() => ({})),
            apiCall('/api/profile').catch(() => ({})),
            apiCall('/api/noise').catch(() => ({})),
            apiCall('/api/trace').catch(() => ({})),
            apiCall('/api/debts').catch(() => ({})),
        ]);
        el.innerHTML = `<h2><i class="fas fa-chart-pie"></i> Dashboard</h2>
            <div class="grid-2">
                <div class="card">
                    <h3><i class="fas fa-user"></i> Profile</h3>
                    <div style="margin-top:8px;font-size:0.9rem;">
                        <div>${profile.name || profile.username || 'User'} ${profile.avatar || ''}</div>
                        <div style="margin-top:4px;color:var(--text-secondary);font-size:0.85rem;">Level ${progress.level || 0} | ${progress.xp || 0} XP</div>
                    </div>
                </div>
                <div class="card">
                    <h3><i class="fas fa-chart-simple"></i> Stats</h3>
                    <div style="margin-top:8px;font-size:0.85rem;">
                        <div>Quizzes: ${stats.quizzes_taken || 0} | Labs: ${stats.labs_started || 0}</div>
                        <div>Reputation: ${stats.reputation || 0} | Streak: ${stats.streak || 0}</div>
                        <div>Flags: ${stats.flags_captured || 0} | Skills: ${stats.skills_learned || 0}</div>
                    </div>
                </div>
                <div class="card" id="risk-indicators-container">
                    <h3><i class="fas fa-shield"></i> Risk Status</h3>
                    <div id="risk-indicators-inner"></div>
                </div>
                <div class="card" style="grid-column:1/-1;">
                    <h3><i class="fas fa-activity"></i> Activity</h3>
                    <div id="dashboard-history" style="margin-top:8px;font-size:0.85rem;max-height:200px;overflow-y:auto;">
                        <p style="color:var(--text-secondary);">Loading activity...</p>
                    </div>
                </div>
            </div>`;

        // Risk indicators (shared component)
        const riskInner = el.querySelector('#risk-indicators-inner');
        if (riskInner && typeof renderRiskIndicators === 'function') {
            renderRiskIndicators(riskInner);
            updateRiskIndicators();
        } else if (riskInner) {
            riskInner.innerHTML = '<p style="color:var(--text-secondary);">Risk indicators unavailable</p>';
        }

        const historyRes = await apiCall('/api/history?limit=10').catch(() => ({ history: [] }));
        const history = historyRes.history || [];
        const historyEl = el.querySelector('#dashboard-history');
        if (history.length) {
            historyEl.innerHTML = history.map(h => `
                <div style="padding:4px 0;border-bottom:1px solid var(--border);">
                    <span style="color:var(--text-secondary);font-size:0.75rem;">[${h.role || h.sender || '?'}]</span>
                    ${(h.message || h.content || '').substring(0, 100)}
                </div>
            `).join('');
        } else {
            historyEl.innerHTML = '<p style="color:var(--text-secondary);">No recent activity</p>';
        }
    }
};