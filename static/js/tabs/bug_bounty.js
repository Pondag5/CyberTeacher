/* Tab: Bug Bounty */
window.Tab_bug_bounty = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-bug"></i> Bug Bounty</h2><div class="card"><p class="loading">Loading scenarios...</p></div>';
        const res = await apiCall('/api/bounty/scenarios').catch(() => ({ scenarios: [] }));
        const scenarios = res.scenarios || [];
        el.innerHTML = `<h2><i class="fas fa-bug"></i> Bug Bounty Scenarios</h2>
            <p style="color:var(--text-secondary);font-size:0.85rem;margin-bottom:12px;">Practice writing bug bounty reports (CLI for interactive sessions).</p>
            <div class="grid-2">${scenarios.map(s => {
                const diffColor = s.difficulty === 'easy' ? 'var(--success)' : s.difficulty === 'medium' ? 'var(--warning)' : 'var(--error)';
                return `<div class="card">
                    <div style="display:flex;justify-content:space-between;">
                        <h3>${s.name}</h3>
                        <span class="badge" style="background:${diffColor};">${s.difficulty}</span>
                    </div>
                    <div style="margin-top:8px;font-size:0.85rem;">
                        <div>Reward: <strong style="color:var(--success);">$${s.reward?.toLocaleString() || 0}</strong></div>
                        <div style="color:var(--text-secondary);font-size:0.8rem;margin-top:4px;">Use /bounty start ${s.id} in CLI</div>
                    </div>
                </div>`;
            }).join('')}</div>`;
    }
};