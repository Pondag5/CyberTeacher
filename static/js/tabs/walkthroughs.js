/* Tab: Walkthroughs & Exploit Search */
window.Tab_walkthroughs = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-book"></i> Walkthroughs</h2><div class="card"><p class="loading">Loading...</p></div>';
        const [wtRes, wuRes] = await Promise.all([
            apiCall('/api/walkthroughs').catch(() => ({ walkthroughs: [] })),
            apiCall('/api/writeups').catch(() => ({ writeups: [] })),
        ]);
        const walkthroughs = wtRes.walkthroughs || [];
        const writeups = wuRes.writeups || [];
        const all = [...walkthroughs, ...writeups.map((w: any) => ({ ...w, is_writeup: true }))];

        el.innerHTML = `<h2><i class="fas fa-book"></i> Walkthroughs & Writeups</h2>
            <div class="grid-2">
                <div class="card" style="max-height:500px;overflow-y:auto;">
                    <h3>Available Guides</h3>
                    ${all.length ? all.map(w => `
                        <div class="card wt-item" data-name="${w.name}" style="padding:8px;margin-bottom:4px;background:var(--bg);cursor:pointer;">
                            <strong>${w.name}</strong>
                            <div style="font-size:0.75rem;color:var(--text-secondary);">${w.is_writeup ? 'Writeup' : 'Walkthrough'} ${w.date ? '| ' + new Date(w.date * 1000).toLocaleDateString() : ''}</div>
                        </div>
                    `).join('') : '<p style="color:var(--text-secondary);">No guides available</p>'}
                </div>
                <div class="card">
                    <h3>Viewer</h3>
                    <div id="wt-content" style="font-size:0.85rem;white-space:pre-wrap;max-height:500px;overflow-y:auto;">
                        <p style="color:var(--text-secondary);">Click a guide to view</p>
                    </div>
                </div>
            </div>`;

        el.querySelectorAll('.wt-item').forEach(item => {
            item.addEventListener('click', async () => {
                const name = item.dataset.name;
                const content = el.querySelector('#wt-content');
                content.textContent = 'Loading...';
                const res = await apiCall(`/api/writeups/${encodeURIComponent(name)}`).catch(() => null);
                if (res && res.content) {
                    content.innerHTML = res.content.replace(/\n/g, '<br>');
                } else {
                    content.textContent = 'Content not available';
                }
            });
        });
    }
};