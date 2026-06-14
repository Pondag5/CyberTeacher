/* Tab: Network Topology */
window.Tab_network = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-network-wired"></i> Network Topology</h2><div class="card"><p class="loading">Loading network status...</p></div>';
        const res = await apiCall('/api/network/status').catch(() => null);
        if (!res || !res.labs) {
            el.innerHTML = '<h2><i class="fas fa-network-wired"></i> Network Topology</h2><div class="card"><p style="color:var(--text-secondary);">Docker not available</p></div>';
            return;
        }
        const entries = Object.entries(res.labs);
        el.innerHTML = `<h2><i class="fas fa-network-wired"></i> Network Topology</h2>
            <div class="card">
                <div style="display:flex;gap:16px;margin-bottom:12px;font-size:0.85rem;">
                    <span>Active: <strong style="color:var(--success);">${res.running}</strong> / ${res.total}</span>
                </div>
                <div style="position:relative;padding:20px;background:var(--bg);border-radius:8px;min-height:100px;">
                    <div style="font-weight:bold;margin-bottom:12px;">Host (CyberTeacher)</div>
                    ${entries.map(([key, lab]) => `
                        <div style="margin-left:20px;padding:8px;border-left:2px solid ${lab.running ? 'var(--success)' : 'var(--error)'};margin-bottom:8px;">
                            <div style="display:flex;align-items:center;gap:8px;">
                                <span style="color:${lab.running ? 'var(--success)' : 'var(--error)'};">${lab.running ? '●' : '○'}</span>
                                <strong>${key}</strong>
                                <span style="font-size:0.8rem;color:var(--text-secondary);">${lab.name || ''}</span>
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-left:16px;">Ports: ${(lab.ports || []).join(', ') || 'none'}</div>
                        </div>
                    `).join('')}
                </div>
            </div>`;
    }
};