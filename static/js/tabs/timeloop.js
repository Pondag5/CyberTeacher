/* Tab: Time Loop / Branching Story */
window.Tab_timeloop = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-hourglass-half"></i> Time Loop</h2><div class="card"><p class="loading">Loading...</p></div>';
        const res = await apiCall('/api/timeloop').catch(() => ({ started: false }));
        if (!res.started) {
            el.innerHTML = `<h2><i class="fas fa-hourglass-half"></i> Time Loop</h2>
                <div class="card">
                    <p style="color:var(--text-secondary);">Branching incident response scenario. Make choices that affect the outcome.</p>
                    <button id="tl-start" class="btn btn-primary" style="margin-top:12px;">Start New Loop</button>
                </div>`;
            el.querySelector('#tl-start').addEventListener('click', async () => {
                await apiCall('/api/timeloop/start', { method: 'POST' });
                this.render(el);
            });
            return;
        }
        const node = res.node_data || {};
        const choices = node.choices || {};
        const history = res.history || [];

        el.innerHTML = `<h2><i class="fas fa-hourglass-half"></i> Time Loop</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>Story</h3>
                    <div style="margin-top:8px;font-size:0.9rem;line-height:1.6;min-height:100px;">${node.text || ''}</div>
                    ${Object.keys(choices).length ? `<div style="margin-top:12px;">
                        <h4>Choices:</h4>
                        ${Object.entries(choices).map(([key, ch]) => `
                            <button class="btn btn-sm tl-choice" data-choice="${key}" style="margin:4px;display:block;width:100%;text-align:left;">
                                ${ch.text || ch}
                            </button>
                        `).join('')}
                    </div>` : '<p style="color:var(--text-secondary);margin-top:12px;">The end of this path. Start a new loop?</p>'}
                    <button id="tl-reset" class="btn btn-sm" style="margin-top:12px;color:var(--error);">Reset</button>
                </div>
                <div class="card">
                    <h3>History</h3>
                    <div style="max-height:400px;overflow-y:auto;font-size:0.8rem;">${history.length ? history.map(h => `
                        <div style="padding:4px 0;border-bottom:1px solid var(--border);">
                            <div style="color:var(--accent);">→ ${h.label || h.choice}</div>
                        </div>
                    `).join('') : '<p style="color:var(--text-secondary);">No steps yet</p>'}</div>
                </div>
            </div>`;

        el.querySelectorAll('.tl-choice').forEach(btn => {
            btn.addEventListener('click', async () => {
                await apiCall(`/api/timeloop/choice?choice=${btn.dataset.choice}`, { method: 'POST' });
                this.render(el);
            });
        });
        el.querySelector('#tl-reset')?.addEventListener('click', async () => {
            await apiCall('/api/timeloop/start', { method: 'POST' });
            this.render(el);
        });
    }
};