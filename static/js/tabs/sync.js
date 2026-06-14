/* Tab: Cross-Platform Sync */
window.Tab_sync = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-sync"></i> Sync</h2><div class="card"><p class="loading">Loading...</p></div>';
        const idRes = await apiCall('/api/sync/id').catch(() => ({ sync_id: 'unknown' }));
        el.innerHTML = `<h2><i class="fas fa-sync"></i> Cross-Platform Sync</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>Device ID</h3>
                    <div style="font-size:1.2rem;font-family:monospace;margin:12px 0;">${idRes.sync_id}</div>
                    <p style="font-size:0.8rem;color:var(--text-secondary);">Use this ID to identify your progress across devices</p>
                    <button id="sync-export" class="btn btn-primary" style="margin-top:12px;">Export Progress</button>
                    <div id="sync-result" style="margin-top:8px;font-size:0.85rem;"></div>
                </div>
                <div class="card">
                    <h3>About Sync</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-top:8px;">
                        Sync allows you to export your progress and import it on another device.
                    </p>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-top:8px;">
                        CLI commands: /sync export [file], /sync import &lt;file&gt;, /sync id
                    </p>
                </div>
            </div>`;

        el.querySelector('#sync-export').addEventListener('click', async () => {
            const result = el.querySelector('#sync-result');
            result.innerHTML = '<p class="loading">Exporting...</p>';
            const res = await apiCall('/api/sync/export', { method: 'POST' }).catch(() => null);
            if (res && res.status === 'ok') {
                result.innerHTML = '<p style="color:var(--success);">Progress exported successfully</p>';
            } else {
                result.innerHTML = '<p style="color:var(--error);">Export failed</p>';
            }
        });
    }
};