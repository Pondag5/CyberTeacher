/* Tab: Phishing Kit */
window.Tab_phishing = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-fish"></i> Phishing Kit</h2><div class="card"><p class="loading">Loading templates...</p></div>';
        const res = await apiCall('/api/phishing/templates').catch(() => ({ templates: {} }));
        const templates = res.templates || {};
        const entries = Object.entries(templates);

        el.innerHTML = `<h2><i class="fas fa-fish"></i> Phishing Kit</h2>
            <div class="grid-2">
                <div class="card">
                    <h3><i class="fas fa-list"></i> Templates</h3>
                    <div style="margin-top:8px;">${entries.length ? entries.map(([key, t]) => `
                        <div class="card" style="padding:8px;margin-bottom:6px;background:var(--bg);cursor:pointer;" data-template="${key}">
                            <strong>${t.name}</strong>
                            <div style="font-size:0.8rem;color:var(--text-secondary);">${t.scenario}</div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);">${(t.elements || []).join(', ')}</div>
                        </div>
                    `).join('') : '<p style="color:var(--text-secondary);">No templates</p>'}
                    </div>
                    ${entries.length ? '<button id="phishing-generate" class="btn btn-primary" style="margin-top:8px;">Generate random</button>' : ''}
                </div>
                <div class="card">
                    <h3><i class="fas fa-envelope"></i> Generated Email</h3>
                    <div id="phishing-output" style="margin-top:8px;font-size:0.85rem;white-space:pre-wrap;max-height:500px;overflow-y:auto;">
                        <p style="color:var(--text-secondary);">Select a template and click generate</p>
                    </div>
                </div>
            </div>`;

        el.querySelectorAll('[data-template]').forEach(card => {
            card.addEventListener('click', async () => {
                const key = card.dataset.template;
                const output = el.querySelector('#phishing-output');
                output.innerHTML = '<p class="loading">Generating...</p>';
                const res = await apiCall('/api/phishing/generate', {
                    method: 'POST',
                    body: JSON.stringify({ template_type: key }),
                    headers: { 'Content-Type': 'application/json' }
                }).catch(() => null);
                if (res && res.content) {
                    output.innerHTML = `<div class="badge" style="margin-bottom:8px;">${res.template_name || key}</div>${res.content.replace(/\n/g, '<br>')}`;
                } else {
                    output.innerHTML = '<p style="color:var(--error);">Error generating</p>';
                }
            });
        });

        el.querySelector('#phishing-generate')?.addEventListener('click', async () => {
            const output = el.querySelector('#phishing-output');
            output.innerHTML = '<p class="loading">Generating random...</p>';
            const res = await apiCall('/api/phishing/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            }).catch(() => null);
            if (res && res.content) {
                output.innerHTML = `<div class="badge" style="margin-bottom:8px;">${res.template_name || 'Random'}</div>${res.content.replace(/\n/g, '<br>')}`;
            } else {
                output.innerHTML = '<p style="color:var(--error);">Error generating</p>';
            }
        });
    }
};