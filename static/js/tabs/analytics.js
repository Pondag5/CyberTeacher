/* Tab: Analytics */
window.Tab_analytics = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-chart-line"></i> Analytics</h2><div class="card"><p class="loading">Computing metrics...</p></div>';
        const res = await apiCall('/api/analytics').catch(() => ({ metrics: {} }));
        const m = res.metrics || {};
        const items = [
            { label: 'Total XP', value: m.total_xp || 0, color: 'var(--accent)' },
            { label: 'Quizzes Taken', value: m.quizzes_taken || 0, color: 'var(--success)' },
            { label: 'Labs Started', value: m.labs_started || 0, color: 'var(--warning)' },
            { label: 'Missions Completed', value: m.missions_completed || 0, color: 'var(--info)' },
            { label: 'Flags Collected', value: m.flags_collected || 0, color: 'var(--error)' },
            { label: 'Assignments Done', value: m.assignments_completed || 0, color: 'var(--cyan)' },
            { label: 'Tracks Enrolled', value: m.tracks_enrolled || 0, color: 'var(--magenta)' },
        ];
        el.innerHTML = `<h2><i class="fas fa-chart-line"></i> Analytics</h2>
            <div class="grid-2">
                ${items.map(i => `
                    <div class="card" style="text-align:center;padding:16px;">
                        <div style="font-size:2rem;font-weight:bold;color:${i.color};">${i.value}</div>
                        <div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">${i.label}</div>
                    </div>
                `).join('')}
            </div>
            ${m.weak_topics?.length ? `
                <div class="card">
                    <h3>Weak Topics</h3>
                    <div style="margin-top:8px;">${m.weak_topics.map((t: any) => `
                        <div style="margin-bottom:6px;">
                            <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                                <span>${t.topic || t.name || '?'}</span>
                                <span style="color:var(--error);">${t.success_rate || 0}%</span>
                            </div>
                            <div style="width:100%;height:4px;background:var(--bg);border-radius:2px;overflow:hidden;">
                                <div style="height:100%;width:${t.success_rate || 0}%;background:var(--error);border-radius:2px;"></div>
                            </div>
                        </div>
                    `).join('')}</div>
                </div>
            ` : ''}
            ${m.avg_weak_success ? `<div class="card"><p style="font-size:0.85rem;">Avg weak topic success: ${m.avg_weak_success.toFixed(1)}%</p></div>` : ''}`;
    }
};