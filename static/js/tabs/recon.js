/* Tab: External Recon — Shodan + Censys */
window.Tab_recon = {
    async render(el) {
        el.innerHTML = `
            <h2><i class="fas fa-satellite-dish"></i> External Recon</h2>
            <div class="grid-2" style="margin-top:12px;">
                <div class="card">
                    <h3><i class="fas fa-search"></i> Shodan Search</h3>
                    <div style="display:flex;gap:8px;margin-bottom:12px;">
                        <input type="text" id="shodan-query" class="input" placeholder="nginx port:443" style="flex:1;">
                        <button id="shodan-search-btn" class="btn btn-primary">Search</button>
                    </div>
                    <div style="display:flex;gap:8px;margin-bottom:12px;">
                        <input type="text" id="shodan-host" class="input" placeholder="IP-address" style="flex:1;">
                        <button id="shodan-host-btn" class="btn btn-sm">Host</button>
                    </div>
                    <div id="shodan-result"></div>
                </div>
                <div class="card">
                    <h3><i class="fas fa-shield-halved"></i> Censys Search</h3>
                    <div style="display:flex;gap:8px;margin-bottom:12px;">
                        <input type="text" id="censys-query" class="input" placeholder="service:SSH" style="flex:1;">
                        <button id="censys-search-btn" class="btn btn-primary">Search</button>
                    </div>
                    <div id="censys-result"></div>
                </div>
            </div>
        `;
        this.setupShodan(el);
        this.setupCensys(el);
    },

    setupShodan(el) {
        const queryInput = el.querySelector('#shodan-query');
        const searchBtn = el.querySelector('#shodan-search-btn');
        const hostInput = el.querySelector('#shodan-host');
        const hostBtn = el.querySelector('#shodan-host-btn');
        const result = el.querySelector('#shodan-result');

        searchBtn.addEventListener('click', async () => {
            const q = queryInput.value.trim();
            if (!q) return;
            result.innerHTML = '<p class="loading">Searching Shodan...</p>';
            const res = await apiCall(`/api/shodan?query=${encodeURIComponent(q)}`).catch(() => null);
            if (!res || !res.results?.length) {
                result.innerHTML = '<p style="color:var(--text-secondary);">No results</p>';
                return;
            }
            result.innerHTML = `<p style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:8px;">Found ${res.total} results</p>
                ${res.results.slice(0, 20).map(r => `
                    <div class="card" style="padding:8px;margin-bottom:6px;background:var(--bg);">
                        <div style="display:flex;justify-content:space-between;">
                            <strong>${r.ip}:${r.port}</strong>
                            <span style="font-size:0.75rem;color:var(--text-secondary);">${r.country}</span>
                        </div>
                        <div style="font-size:0.8rem;margin-top:4px;">${r.product}</div>
                        <div style="font-size:0.75rem;color:var(--text-secondary);">${r.os} ${r.vulns?.length ? '| ' + r.vulns.join(', ') : ''}</div>
                    </div>
                `).join('')}`;
        });

        hostBtn.addEventListener('click', async () => {
            const ip = hostInput.value.trim();
            if (!ip) return;
            result.innerHTML = '<p class="loading">Looking up host...</p>';
            const res = await apiCall(`/api/shodan/host?ip=${encodeURIComponent(ip)}`).catch(() => null);
            if (!res || !res.host) {
                result.innerHTML = '<p style="color:var(--error);">Host not found</p>';
                return;
            }
            const h = res.host;
            result.innerHTML = `
                <div class="card" style="padding:12px;background:var(--bg);">
                    <div><strong>${h.ip}</strong> <span style="font-size:0.8rem;color:var(--text-secondary);">${h.hostname}</span></div>
                    <div style="font-size:0.85rem;margin-top:6px;">OS: ${h.os}</div>
                    <div style="font-size:0.85rem;">Org: ${h.org}</div>
                    <div style="font-size:0.85rem;">Ports: ${(h.ports || []).join(', ')}</div>
                    ${h.vulns?.length ? `<div style="font-size:0.85rem;color:var(--error);">Vulns: ${h.vulns.join(', ')}</div>` : ''}
                </div>
            `;
        });
    },

    setupCensys(el) {
        const input = el.querySelector('#censys-query');
        const btn = el.querySelector('#censys-search-btn');
        const result = el.querySelector('#censys-result');

        btn.addEventListener('click', async () => {
            const q = input.value.trim();
            if (!q) return;
            result.innerHTML = '<p class="loading">Searching Censys...</p>';
            const res = await apiCall(`/api/censys?query=${encodeURIComponent(q)}`).catch(() => null);
            if (!res || !res.results?.length) {
                result.innerHTML = '<p style="color:var(--text-secondary);">No results</p>';
                return;
            }
            result.innerHTML = `<p style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:8px;">Found ${res.total} results</p>
                ${res.results.slice(0, 20).map(r => `
                    <div class="card" style="padding:8px;margin-bottom:6px;background:var(--bg);">
                        <div style="display:flex;justify-content:space-between;">
                            <strong>${r.ip}:${r.port}</strong>
                            <span style="font-size:0.75rem;color:var(--text-secondary);">${r.service}</span>
                        </div>
                        <div style="font-size:0.8rem;color:var(--text-secondary);">Cert: ${r.certificate}</div>
                    </div>
                `).join('')}`;
        });
    }
};