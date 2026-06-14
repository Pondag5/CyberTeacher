/* Tab: Docker Compose Generator */
window.Tab_dockergen = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-cubes"></i> Docker Generator</h2><div class="card"><p class="loading">Loading images...</p></div>';
        const res = await apiCall('/api/dockergen/images').catch(() => ({ images: [] }));
        const images = res.images || [];
        const selected = new Set();

        el.innerHTML = `<h2><i class="fas fa-cubes"></i> Docker Generator</h2>
            <p style="color:var(--text-secondary);font-size:0.85rem;margin-bottom:12px;">Select labs to include in your docker-compose.yml</p>
            <div class="grid-2" style="margin-bottom:12px;">${images.map(img => `
                <div class="card docker-img" data-id="${img.id}" style="cursor:pointer;padding:12px;border:2px solid transparent;transition:border-color 0.2s;">
                    <h4>${img.name}</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);">${img.desc}</p>
                    <div style="font-size:0.75rem;color:var(--text-secondary);">Ports: ${(img.ports || []).join(', ') || 'none'}</div>
                </div>
            `).join('')}</div>
            <button id="docker-gen-btn" class="btn btn-primary">Generate docker-compose.yml</button>
            <div id="docker-output" style="margin-top:12px;display:none;">
                <h3>docker-compose.yml</h3>
                <pre id="docker-compose-text" style="background:var(--bg);padding:16px;border-radius:8px;font-size:0.8rem;overflow-x:auto;margin-top:8px;"></pre>
                <button id="docker-copy-btn" class="btn btn-sm" style="margin-top:8px;">Copy to clipboard</button>
            </div>`;

        el.querySelectorAll('.docker-img').forEach(card => {
            card.addEventListener('click', () => {
                const id = card.dataset.id;
                if (selected.has(id)) {
                    selected.delete(id);
                    card.style.borderColor = 'transparent';
                } else {
                    selected.add(id);
                    card.style.borderColor = 'var(--accent)';
                }
            });
        });

        el.querySelector('#docker-gen-btn').addEventListener('click', async () => {
            const output = el.querySelector('#docker-output');
            const text = el.querySelector('#docker-compose-text');
            output.style.display = 'none';
            const res = await apiCall('/api/dockergen/generate', {
                method: 'POST',
                body: JSON.stringify({ labs: Array.from(selected) }),
                headers: { 'Content-Type': 'application/json' }
            }).catch(() => null);
            if (res && res.compose) {
                text.textContent = res.compose;
                output.style.display = 'block';
            } else {
                text.textContent = 'Error generating compose file';
                output.style.display = 'block';
            }
        });

        el.querySelector('#docker-copy-btn').addEventListener('click', () => {
            const text = el.querySelector('#docker-compose-text');
            navigator.clipboard.writeText(text.textContent).catch(() => {});
        });
    }
};