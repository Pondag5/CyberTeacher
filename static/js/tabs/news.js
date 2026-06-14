/* Tab: Cyber News */
window.Tab_news = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-newspaper"></i> Cyber News</h2><div class="card"><p class="loading">Fetching news...</p></div>';
        const res = await apiCall('/api/news').catch(() => ({ news: [] }));
        const items = res.news || [];
        if (!items.length) {
            el.innerHTML = '<h2><i class="fas fa-newspaper"></i> Cyber News</h2><div class="card"><p style="color:var(--text-secondary);">No news available</p></div>';
            return;
        }
        el.innerHTML = `<h2><i class="fas fa-newspaper"></i> Cyber News</h2>
            <div class="card" style="max-height:600px;overflow-y:auto;">${items.map(item => {
                const title = item.title || item.name || '';
                const desc = item.description || item.summary || '';
                const url = item.url || item.link || '';
                const date = item.published || item.date || '';
                const source = item.source || '';
                return `<div class="card" style="padding:10px;margin-bottom:6px;background:var(--bg);">
                    <div style="display:flex;justify-content:space-between;">
                        <strong>${title}</strong>
                        ${source ? `<span style="font-size:0.75rem;color:var(--text-secondary);">${source}</span>` : ''}
                    </div>
                    ${desc ? `<p style="font-size:0.8rem;color:var(--text-secondary);margin:4px 0;">${desc}</p>` : ''}
                    <div style="display:flex;justify-content:space-between;font-size:0.75rem;">
                        ${date ? `<span>${date}</span>` : ''}
                        ${url ? `<a href="${url}" target="_blank" rel="noopener" style="color:var(--accent);">Read →</a>` : ''}
                    </div>
                </div>`;
            }).join('')}</div>`;
    }
};