/* Tab: Offline Mode + Local LLM (LM Studio) */
window.Tab_offline = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-wifi-slash"></i> Offline & Local LLM</h2><div class="card"><p class="loading">Loading...</p></div>';
        const [offRes, provRes, lmRes] = await Promise.all([
            apiCall('/api/offline').catch(() => ({ offline_mode: false })),
            apiCall('/api/providers').catch(() => ({ providers: [], current: 'ollama', lmstudio_running: false })),
            apiCall('/api/provider/lmstudio/check').catch(() => ({ running: false })),
        ]);
        const isOffline = offRes.offline_mode;
        const providers = provRes.providers || [];
        const current = provRes.current || 'ollama';
        const lmRunning = lmRes.running || provRes.lmstudio_running;
        const lmModels = lmRes.models || [];

        el.innerHTML = `<h2><i class="fas fa-wifi-slash"></i> Offline & Local LLM</h2>
            <div class="grid-2">
                <div class="card">
                    <h3><i class="fas fa-network-wired"></i> Connection</h3>
                    <div style="display:flex;align-items:center;gap:12px;margin:12px 0;">
                        <span style="font-size:2rem;">${isOffline ? '📡' : '🌐'}</span>
                        <div>
                            <div>Status: <strong style="color:${isOffline ? 'var(--warning)' : 'var(--success)'};">${isOffline ? 'OFFLINE' : 'ONLINE'}</strong></div>
                            <div style="font-size:0.85rem;color:var(--text-secondary);">Use cached data + local LLM when offline</div>
                        </div>
                    </div>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        <button id="offline-on" class="btn btn-sm ${isOffline ? 'btn-secondary' : ''}">Go Offline</button>
                        <button id="offline-off" class="btn btn-sm ${!isOffline ? 'btn-secondary' : ''}">Go Online</button>
                        <button id="offline-toggle" class="btn btn-sm">Toggle</button>
                    </div>
                </div>
                <div class="card">
                    <h3><i class="fas fa-microchip"></i> LM Studio</h3>
                    <div style="display:flex;align-items:center;gap:8px;margin:12px 0;">
                        <span style="font-size:1.5rem;color:${lmRunning ? 'var(--success)' : 'var(--error)'};">${lmRunning ? '●' : '○'}</span>
                        <div>
                            <div>Status: <strong style="color:${lmRunning ? 'var(--success)' : 'var(--error)'};">${lmRunning ? 'RUNNING' : 'NOT DETECTED'}</strong></div>
                            <div style="font-size:0.85rem;color:var(--text-secondary);">http://localhost:1234/v1</div>
                            ${lmModels.length ? `<div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">Model: ${lmModels[0]}</div>` : ''}
                        </div>
                    </div>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        <button id="use-lmstudio" class="btn btn-sm btn-primary" ${!lmRunning ? 'disabled' : ''}>Use LM Studio</button>
                        <button id="check-lmstudio" class="btn btn-sm">Re-check</button>
                    </div>
                </div>
                <div class="card" style="grid-column:1/-1;">
                    <h3><i class="fas fa-random"></i> Active Provider</h3>
                    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;">${providers.map(p => {
                        const isActive = p.current;
                        const color = p.status === 'running' ? 'var(--success)' : p.status === 'active' ? 'var(--accent)' : 'var(--text-secondary)';
                        return `<button class="btn btn-sm set-provider" data-provider="${p.name}" style="${isActive ? 'border:2px solid ' + color + ';' : ''}${p.name === 'lmstudio' && p.status === 'not_found' ? 'opacity:0.4;' : ''}">
                            ${isActive ? '● ' : ''}${p.name}
                        </button>`;
                    }).join('')}</div>
                    <div style="margin-top:8px;font-size:0.8rem;color:var(--text-secondary);">
                        Current: <strong style="color:var(--accent);">${current}</strong>
                        ${current === 'lmstudio' && lmRunning ? '| using local model' : ''}
                        ${current === 'ollama' ? '| using Ollama (default)' : ''}
                    </div>
                </div>
            </div>`;

        el.querySelector('#offline-on')?.addEventListener('click', async () => {
            await apiCall('/api/offline?action=on', { method: 'POST' });
            this.render(el);
        });
        el.querySelector('#offline-off')?.addEventListener('click', async () => {
            await apiCall('/api/offline?action=off', { method: 'POST' });
            this.render(el);
        });
        el.querySelector('#offline-toggle')?.addEventListener('click', async () => {
            await apiCall('/api/offline?action=toggle', { method: 'POST' });
            this.render(el);
        });
        el.querySelector('#use-lmstudio')?.addEventListener('click', async () => {
            await apiCall('/api/provider/set?provider=lmstudio', { method: 'POST' });
            this.render(el);
        });
        el.querySelector('#check-lmstudio')?.addEventListener('click', () => this.render(el));

        el.querySelectorAll('.set-provider').forEach(btn => {
            btn.addEventListener('click', async () => {
                const provider = btn.dataset.provider;
                await apiCall(`/api/provider/set?provider=${provider}`, { method: 'POST' });
                this.render(el);
            });
        });
    }
};