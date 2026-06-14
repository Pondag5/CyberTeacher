/* Tab: Skills */
window.Tab_skills = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-code-branch"></i> Skills</h2><div class="card"><p class="loading">Loading skills...</p></div>';
        const res = await apiCall('/api/skills').catch(() => ({ skills: [] }));
        const items = res.skills || [];
        if (!items.length) {
            el.innerHTML = '<h2><i class="fas fa-code-branch"></i> Skills</h2><div class="card"><p style="color:var(--text-secondary);">No skills yet</p></div>';
            return;
        }
        el.innerHTML = `<h2><i class="fas fa-code-branch"></i> Skills</h2>
            <div class="grid-2">${items.map(s => {
                const pct = s.level > 0 ? Math.min(100, (s.xp / (s.level * 100)) * 100) : s.xp > 0 ? 10 : 0;
                return `<div class="card">
                    <h3>${s.name || s.id}</h3>
                    <div style="margin-top:8px;">
                        <div style="display:flex;justify-content:space-between;font-size:0.8rem;">
                            <span>Level ${s.level || 0}</span>
                            <span>${s.xp || 0} XP</span>
                        </div>
                        <div style="width:100%;height:6px;background:var(--bg);border-radius:3px;margin-top:4px;overflow:hidden;">
                            <div style="height:100%;width:${pct}%;background:var(--accent);border-radius:3px;transition:width 0.5s;"></div>
                        </div>
                    </div>
                </div>`;
            }).join('')}</div>`;
    }
};