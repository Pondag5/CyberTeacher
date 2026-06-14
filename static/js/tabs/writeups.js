/* Tab: Writeups + CVE search */
window.Tab_writeups = {
    async render(el) {
        el.innerHTML = `
            <h2><i class="fas fa-feather-alt"></i> Writeups & CVE</h2>
            <div class="grid-2" style="margin-top:12px;">
                <div class="card">
                    <h3><i class="fas fa-feather"></i> Мои writeups</h3>
                    <div id="writeup-list"><p class="loading">Загрузка...</p></div>
                </div>
                <div class="card">
                    <h3><i class="fas fa-shield-alt"></i> Поиск CVE</h3>
                    <div style="display:flex;gap:8px;margin-bottom:12px;">
                        <input type="text" id="cve-input" class="input" placeholder="CVE-2024-XXXX" style="flex:1;">
                        <button id="cve-search-btn" class="btn btn-primary">Найти</button>
                    </div>
                    <div id="cve-result"></div>
                </div>
            </div>
            <div class="card" id="writeup-viewer" style="display:none;margin-top:12px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <h3 id="writeup-viewer-title"></h3>
                    <button id="writeup-viewer-close" class="btn btn-sm">✕</button>
                </div>
                <div id="writeup-viewer-content" style="margin-top:8px;white-space:pre-wrap;font-size:0.85rem;line-height:1.6;background:var(--bg);padding:16px;border-radius:8px;max-height:500px;overflow-y:auto;"></div>
            </div>
        `;

        this.loadWriteupList(el);
        this.setupCveSearch(el);
    },

    async loadWriteupList(el) {
        const container = el.querySelector('#writeup-list');
        const res = await apiCall('/api/writeups').catch(() => ({ writeups: [] }));
        const list = res.writeups || [];
        if (!list.length) {
            container.innerHTML = '<p style="color:var(--text-secondary);font-size:0.85rem;">Нет сохранённых writeup\'ов</p>';
            return;
        }
        container.innerHTML = list.map(w => `
            <div class="writeup-item" data-name="${w.name}" style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid var(--border);cursor:pointer;">
                <span>${w.name}</span>
                <span style="font-size:0.75rem;color:var(--text-secondary);">${new Date(w.date * 1000).toLocaleDateString()}</span>
            </div>
        `).join('');

        container.querySelectorAll('.writeup-item').forEach(item => {
            item.addEventListener('click', async () => {
                const name = item.dataset.name;
                const viewer = el.querySelector('#writeup-viewer');
                const title = el.querySelector('#writeup-viewer-title');
                const content = el.querySelector('#writeup-viewer-content');
                title.textContent = name;
                content.textContent = 'Загрузка...';
                viewer.style.display = 'block';
                const res = await apiCall(`/api/writeups/${encodeURIComponent(name)}`).catch(() => null);
                if (res && res.content) {
                    content.textContent = res.content;
                } else {
                    content.textContent = 'Ошибка загрузки';
                }
            });
        });

        el.querySelector('#writeup-viewer-close').addEventListener('click', () => {
            el.querySelector('#writeup-viewer').style.display = 'none';
        });
    },

    setupCveSearch(el) {
        const input = el.querySelector('#cve-input');
        const btn = el.querySelector('#cve-search-btn');
        const result = el.querySelector('#cve-result');

        const doSearch = async () => {
            const cveId = input.value.trim();
            if (!cveId) return;
            result.innerHTML = '<p class="loading">Поиск...</p>';
            const res = await apiCall(`/api/cve/${encodeURIComponent(cveId)}`).catch(() => null);
            if (!res || !res.cve) {
                result.innerHTML = '<p style="color:var(--error);">CVE не найден</p>';
                return;
            }
            const c = res.cve;
            const severityColor = c.severity === 'CRITICAL' ? 'var(--error)' : c.severity === 'HIGH' ? 'var(--warning)' : 'var(--success)';
            result.innerHTML = `
                <div class="card" style="padding:12px;background:var(--bg);">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <strong>${c.id}</strong>
                        <span class="badge" style="background:${severityColor};">${c.severity} (${c.score})</span>
                    </div>
                    <p style="margin:8px 0;font-size:0.85rem;">${c.description || '—'}</p>
                    <div style="font-size:0.75rem;color:var(--text-secondary);">Published: ${c.published || '—'}</div>
                    ${c.references?.length ? `
                        <details style="margin-top:8px;">
                            <summary style="font-size:0.85rem;cursor:pointer;">References (${c.references.length})</summary>
                            <ul style="margin:4px 0 0 16px;font-size:0.8rem;">
                                ${c.references.slice(0, 10).map(r => `<li><a href="${r.url}" target="_blank" rel="noopener">${r.url}</a></li>`).join('')}
                            </ul>
                        </details>
                    ` : ''}
                </div>
            `;
        };

        btn.addEventListener('click', doSearch);
        input.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(); });
    }
};