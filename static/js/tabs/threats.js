/* Tab: APT Threats */
window.Tab_threats = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-skull-crossbones"></i> APT Threats</h2><div class="card"><p class="loading">Loading threats...</p></div>';
        const res = await apiCall('/api/threats').catch(() => ({ threats: [] }));
        const items = res.threats || [];
        if (!items.length) {
            el.innerHTML = '<h2><i class="fas fa-skull-crossbones"></i> APT Threats</h2><div class="card"><p style="color:var(--text-secondary);">No threat data</p></div>';
            return;
        }
        el.innerHTML = `<h2><i class="fas fa-skull-crossbones"></i> APT Threats</h2>
            <div class="card" style="max-height:600px;overflow-y:auto;">${items.map(g => `
                <div class="card threat-item" data-id="${g.id}" style="padding:10px;margin-bottom:6px;background:var(--bg);cursor:pointer;">
                    <div style="display:flex;justify-content:space-between;">
                        <strong style="color:var(--error);">${g.name || g.id}</strong>
                        <span style="font-size:0.75rem;color:var(--text-secondary);">${g.country || ''}</span>
                    </div>
                    <div style="font-size:0.8rem;color:var(--text-secondary);margin:4px 0;">
                        ${g.targets || ''} ${g.aliases?.length ? '(' + g.aliases.join(', ') + ')' : ''}
                    </div>
                    <div class="threat-detail" style="display:none;margin-top:8px;font-size:0.85rem;">
                        <p>${g.description || ''}</p>
                        ${g.tactics?.length ? `<div style="margin-top:4px;"><strong>Tactics:</strong> ${g.tactics.join(', ')}</div>` : ''}
                        ${g.tools?.length ? `<div><strong>Tools:</strong> ${g.tools.join(', ')}</div>` : ''}
                    </div>
                </div>
            `).join('')}</div>`;

        el.querySelectorAll('.threat-item').forEach(card => {
            card.addEventListener('click', () => {
                const detail = card.querySelector('.threat-detail');
                detail.style.display = detail.style.display === 'none' ? 'block' : 'none';
            });
        });
    }
};