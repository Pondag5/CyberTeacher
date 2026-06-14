/* Tab: Equipment / Tool Selection */
window.Tab_equipment = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-toolbox"></i> Equipment</h2><div class="card"><p class="loading">Loading...</p></div>';
        const res = await apiCall('/api/equipment').catch(() => ({ tools: [], used_ram: 0, max_ram: 100 }));
        const tools = res.tools || [];
        const used = res.used_ram || 0;
        const maxRam = res.max_ram || 100;
        const pct = maxRam > 0 ? (used / maxRam) * 100 : 0;

        el.innerHTML = `<h2><i class="fas fa-toolbox"></i> Equipment</h2>
            <div class="card">
                <div style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                        <span>RAM Used</span>
                        <span>${used} / ${maxRam}</span>
                    </div>
                    <div style="width:100%;height:8px;background:var(--bg);border-radius:4px;overflow:hidden;">
                        <div style="height:100%;width:${pct}%;background:${pct > 80 ? 'var(--error)' : pct > 50 ? 'var(--warning)' : 'var(--success)'};border-radius:4px;transition:width 0.3s;"></div>
                    </div>
                </div>
                <div class="grid-2">${tools.map(t => `
                    <div class="card tool-item ${t.selected ? 'selected' : ''}" data-tool="${t.name}" style="padding:10px;cursor:pointer;border:2px solid ${t.selected ? 'var(--accent)' : 'transparent'};transition:all 0.2s;">
                        <div style="display:flex;justify-content:space-between;">
                            <strong>${t.name}</strong>
                            <span style="font-size:0.8rem;color:var(--text-secondary);">${t.cost} RAM</span>
                        </div>
                        <div style="font-size:0.8rem;color:${t.selected ? 'var(--success)' : 'var(--text-secondary)'};margin-top:4px;">${t.selected ? '✓ Equipped' : 'Click to equip'}</div>
                    </div>
                `).join('')}</div>
            </div>`;

        el.querySelectorAll('.tool-item').forEach(card => {
            card.addEventListener('click', async () => {
                const tool = card.dataset.tool;
                const res = await apiCall(`/api/equipment/toggle?tool=${encodeURIComponent(tool)}`, { method: 'POST' }).catch(() => null);
                if (res) this.render(el);
            });
        });
    }
};