/* Tab: CTF Flags */
window.Tab_ctf_flags = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-flag"></i> CTF Flags</h2><div class="card"><p class="loading">Loading...</p></div>';
        const res = await apiCall('/api/ctf/status').catch(() => ({}));
        el.innerHTML = `<h2><i class="fas fa-flag"></i> CTF Flags</h2>
            <div class="grid-2">
                <div class="card" style="text-align:center;">
                    <div style="font-size:3rem;font-weight:bold;color:var(--accent);">${res.flags_captured || 0}</div>
                    <div style="font-size:0.9rem;">Flags Captured</div>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:3rem;font-weight:bold;color:${res.risk_level > 50 ? 'var(--error)' : res.risk_level > 20 ? 'var(--warning)' : 'var(--success)'};">${res.risk_level || 0}%</div>
                    <div style="font-size:0.9rem;">Risk Level</div>
                </div>
                <div class="card" style="grid-column:1/-1;">
                    <h3>Submit Flag</h3>
                    <div style="display:flex;gap:8px;margin-top:8px;">
                        <input type="text" id="ctf-flag-input" class="input" placeholder="FLAG{...}" style="flex:1;">
                        <button id="ctf-flag-submit" class="btn btn-primary">Submit</button>
                    </div>
                    <div id="ctf-flag-result" style="margin-top:8px;font-size:0.85rem;"></div>
                </div>
            </div>`;

        const flagInput = el.querySelector('#ctf-flag-input');
        const flagBtn = el.querySelector('#ctf-flag-submit');
        const flagResult = el.querySelector('#ctf-flag-result');
        flagBtn.addEventListener('click', async () => {
            const val = flagInput.value.trim();
            if (!val) return;
            flagResult.innerHTML = '<p class="loading">Verifying...</p>';
            const res = await apiCall(`/api/ctf/flag?flag_value=${encodeURIComponent(val)}`, { method: 'POST' }).catch(() => null);
            if (res && res.success) {
                flagResult.innerHTML = '<p style="color:var(--success);">✓ Flag accepted!</p>';
            } else {
                flagResult.innerHTML = `<p style="color:var(--error);">${res?.message || 'Invalid flag'}</p>`;
            }
        });
    }
};