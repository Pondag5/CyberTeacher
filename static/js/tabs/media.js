/* Tab: Media Resources */
window.Tab_media = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-play-circle"></i> Media</h2><div class="card"><p class="loading">Loading media...</p></div>';
        const res = await apiCall('/api/media').catch(() => ({ resources: [] }));
        const items = res.resources || [];
        el.innerHTML = `<h2><i class="fas fa-play-circle"></i> Media Resources</h2>
            <div class="grid-2">${items.map(m => `
                <div class="card">
                    <div style="display:flex;align-items:center;gap:12px;">
                        <span style="font-size:2rem;">${m.type === 'video' ? '🎬' : '📄'}</span>
                        <div>
                            <h3>${m.title}</h3>
                            <div style="font-size:0.85rem;color:var(--text-secondary);">
                                ${m.type === 'video' ? `${m.duration}` : `${m.pages} pages`}
                            </div>
                            <span class="badge" style="margin-top:4px;">${m.type}</span>
                        </div>
                    </div>
                </div>
            `).join('')}</div>`;
    }
};