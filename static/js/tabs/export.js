/* Tab: Export — export/import user data (GDPR) */
window.Tab_export = {
    async render(el) {
        const token = localStorage.getItem('auth_token');
        el.innerHTML = `
            <h2>\uD83D\uDCC1 \u042D\u043A\u0441\u043F\u043E\u0440\u0442 / \u0418\u043C\u043F\u043E\u0440\u0442 \u0434\u0430\u043D\u043D\u044B\u0445</h2>

            <div class="grid-2">
                <div class="card">
                    <h3>\uD83D\uDCC4 \u042D\u043A\u0441\u043F\u043E\u0440\u0442 \u0434\u0430\u043D\u043D\u044B\u0445</h3>
                    <p>\u0421\u043A\u0430\u0447\u0430\u0439\u0442\u0435 JSON-\u0444\u0430\u0439\u043B \u0441 \u043F\u0440\u043E\u0444\u0438\u043B\u0435\u043C, \u043D\u0430\u0432\u044B\u043A\u0430\u043C\u0438 \u0438 \u043F\u0440\u043E\u0433\u0440\u0435\u0441\u0441\u043E\u043C.</p>
                    <button id="exportBtn">\uD83D\uDCE5 \u042D\u043A\u0441\u043F\u043E\u0440\u0442\u0438\u0440\u043E\u0432\u0430\u0442\u044C</button>
                    <div id="exportResult" style="margin-top:8px;"></div>
                </div>

                <div class="card">
                    <h3>\uD83D\uDCC3 \u0418\u043C\u043F\u043E\u0440\u0442 \u0434\u0430\u043D\u043D\u044B\u0445</h3>
                    <p>\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u0435 JSON-\u0444\u0430\u0439\u043B \u044D\u043A\u0441\u043F\u043E\u0440\u0442\u0430.</p>
                    <input type="file" id="importFile" accept=".json" style="margin-bottom:8px;">
                    <button id="importBtn" ${!token ? 'disabled' : ''}>\uD83D\uDCC2 \u0418\u043C\u043F\u043E\u0440\u0442\u0438\u0440\u043E\u0432\u0430\u0442\u044C</button>
                    <div id="importResult" style="margin-top:8px;"></div>
                </div>
            </div>

            <div class="card">
                <h3>\uD83D\uDCC4 \u041E\u0442\u0447\u0451\u0442 \u043E\u0431\u0443\u0447\u0435\u043D\u0438\u044F</h3>
                <p>\u0421\u043A\u0430\u0447\u0430\u0439\u0442\u0435 HTML-\u043E\u0442\u0447\u0451\u0442 \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043A\u0438, \u043D\u0430\u0432\u044B\u043A\u043E\u0432 \u0438 \u043F\u0440\u043E\u0433\u0440\u0435\u0441\u0441\u0430. \u041E\u0442\u043A\u0440\u043E\u0439\u0442\u0435 \u0432 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0435 \u0438 \u043F\u0435\u0447\u0430\u0442\u044C \u0432 PDF.</p>
                <button id="reportBtn">\uD83C\uDFC6 \u0421\u043A\u0430\u0447\u0430\u0442\u044C \u043E\u0442\u0447\u0451\u0442</button>
                <div id="reportResult" style="margin-top:8px;"></div>
            </div>

            <div class="card">
                <h3>\u2139\uFE0F \u0418\u043D\u0444\u043E\u0440\u043C\u0430\u0446\u0438\u044F</h3>
                <p>\u042D\u043A\u0441\u043F\u043E\u0440\u0442 \u0432\u043A\u043B\u044E\u0447\u0430\u0435\u0442: \u043F\u0440\u043E\u0444\u0438\u043B\u044C, \u043D\u0430\u0432\u044B\u043A\u0438 (XP, \u0443\u0440\u043E\u0432\u0435\u043D\u044C), \u0434\u043E\u0441\u0442\u0438\u0436\u0435\u043D\u0438\u044F, \u043F\u0440\u043E\u0433\u0440\u0435\u0441\u0441 \u043A\u0443\u0440\u0441\u043E\u0432.</p>
                <p>\u0418\u043C\u043F\u043E\u0440\u0442 \u0434\u043E\u0441\u0442\u0443\u043F\u0435\u043D \u0442\u043E\u043B\u044C\u043A\u043E \u0434\u043B\u044F \u0430\u0434\u043C\u0438\u043D\u0438\u0441\u0442\u0440\u0430\u0442\u043E\u0440\u043E\u0432 (\u0447\u0435\u0440\u0435\u0437 API \u0441 \u0442\u043E\u043A\u0435\u043D\u043E\u043C).</p>
            </div>
        `;

        document.getElementById('exportBtn').onclick = async () => {
            if (!token) {
                document.getElementById('exportResult').innerHTML = '<span style="color:var(--error);">\u0412\u043E\u0439\u0434\u0438\u0442\u0435 \u0432 \u043F\u0440\u043E\u0444\u0438\u043B\u044C</span>';
                return;
            }
            const res = await apiCall(`/export_user_data?token=${encodeURIComponent(token)}`);
            if (res.error) {
                document.getElementById('exportResult').innerHTML = `<span style="color:var(--error);">\u2717 ${res.error}</span>`;
                return;
            }
            // Download as JSON file
            const blob = new Blob([JSON.stringify(res, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `cyberteacher_export_${res.user?.username || 'user'}_${new Date().toISOString().slice(0,10)}.json`;
            a.click();
            URL.revokeObjectURL(url);
            document.getElementById('exportResult').innerHTML = '<span style="color:var(--success);">\u2705 \u0424\u0430\u0439\u043B \u0441\u043A\u0430\u0447\u0430\u043D</span>';
            if (window.Sounds) Sounds.success();
        };

        document.getElementById('importBtn').onclick = async () => {
            if (!token) {
                document.getElementById('importResult').innerHTML = '<span style="color:var(--error);">\u0422\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044F \u0430\u0434\u043C\u0438\u043D\u0438\u0441\u0442\u0440\u0430\u0442\u043E\u0440\u0441\u043A\u0438\u0439 \u0442\u043E\u043A\u0435\u043D</span>';
                return;
            }
            const file = document.getElementById('importFile').files[0];
            if (!file) {
                document.getElementById('importResult').innerHTML = '<span style="color:var(--error);">\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0430\u0439\u043B</span>';
                return;
            }
            try {
                const text = await file.text();
                const data = JSON.parse(text);
                const res = await apiCall('/import_user_data', {
                    method: 'POST',
                    body: JSON.stringify({ token, data }),
                });
                if (res.error) {
                    document.getElementById('importResult').innerHTML = `<span style="color:var(--error);">\u2717 ${res.error}</span>`;
                } else {
                    document.getElementById('importResult').innerHTML = `<span style="color:var(--success);">\u2705 \u0418\u043C\u043F\u043E\u0440\u0442\u0438\u0440\u043E\u0432\u0430\u043D\u043E: ${(res.imported_fields || []).join(', ')}</span>`;
                    if (window.Sounds) Sounds.success();
                }
            } catch (e) {
                document.getElementById('importResult').innerHTML = `<span style="color:var(--error);">\u2717 \u041E\u0448\u0438\u0431\u043A\u0430: ${e.message}</span>`;
            }
        };

        document.getElementById('reportBtn').onclick = async () => {
            if (!token) {
                document.getElementById('reportResult').innerHTML = '<span style="color:var(--error);">\u0412\u043E\u0439\u0434\u0438\u0442\u0435 \u0432 \u043F\u0440\u043E\u0444\u0438\u043B\u044C</span>';
                return;
            }
            const url = `${API_BASE}/api/report?token=${encodeURIComponent(token)}`;
            window.open(url, '_blank');
            document.getElementById('reportResult').innerHTML = '<span style="color:var(--success);">\u2705 \u041E\u0442\u0447\u0451\u0442 \u043E\u0442\u043A\u0440\u044B\u0442. \u041F\u0435\u0447\u0430\u0442\u044C \u0441 Ctrl+P.</span>';
            if (window.Sounds) Sounds.success();
        };
    }
};
