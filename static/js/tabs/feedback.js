/* Tab: Feedback — send feedback / bug reports */
window.Tab_feedback = {
    async render(el) {
        el.innerHTML = `
            <h2>\uD83D\uDCE3 \u041E\u0431\u0440\u0430\u0442\u043D\u0430\u044F \u0441\u0432\u044F\u0437\u044C</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>\uD83D\uDCDD \u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">
                        \u0421\u043E\u043E\u0431\u0449\u0438\u0442\u0435 \u043E\u0431 \u043E\u0448\u0438\u0431\u043A\u0435, \u043F\u0440\u0435\u0434\u043B\u043E\u0436\u0438\u0442\u0435 \u0444\u0438\u0447\u0443 \u0438\u043B\u0438 \u043F\u043E\u0434\u0435\u043B\u0438\u0442\u0435\u0441\u044C \u0438\u0434\u0435\u0435\u0439
                    </p>
                    <div style="display:flex;flex-direction:column;gap:12px;">
                        <input id="feedbackName" placeholder="\u0412\u0430\u0448\u0435 \u0438\u043C\u044F (\u043D\u0435\u043E\u0431\u044F\u0437\u0430\u0442\u0435\u043B\u044C\u043D\u043E)" style="padding:8px;border-radius:6px;border:1px solid var(--border);">
                        <textarea id="feedbackMessage" placeholder="\u041E\u043F\u0438\u0448\u0438\u0442\u0435 \u043F\u0440\u043E\u0431\u043B\u0435\u043C\u0443 \u0438\u043B\u0438 \u0438\u0434\u0435\u044E..." rows="5" style="padding:8px;border-radius:6px;border:1px solid var(--border);resize:vertical;font-family:inherit;"></textarea>
                        <button id="feedbackSubmitBtn" class="btn btn-primary">\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C</button>
                        <div id="feedbackResult" style="font-size:0.9rem;"></div>
                    </div>
                </div>
                <div class="card">
                    <h3>\uD83D\uDD17 \u0414\u0440\u0443\u0433\u0438\u0435 \u0441\u043F\u043E\u0441\u043E\u0431\u044B</h3>
                    <div style="line-height:2;font-size:0.9rem;">
                        <p>\uD83D\uDEE0\uFE0F GitHub Issues:
                            <a href="https://github.com/anomalyco/cyberteacher/issues" target="_blank" style="color:var(--accent);">
                                anomalyco/cyberteacher
                            </a>
                        </p>
                        <p style="margin-top:12px;color:var(--text-secondary);font-size:0.85rem;">
                            \u0417\u0430\u043F\u043E\u043B\u043D\u0438\u0442\u0435 \u0444\u043E\u0440\u043C\u0443 \u0441\u043B\u0435\u0432\u0430 \u0438\u043B\u0438 \u0441\u043E\u0437\u0434\u0430\u0439\u0442\u0435 Issue \u043D\u0430 GitHub.\u00A0
                            \u0412\u0441\u0435 \u043E\u0442\u0437\u044B\u0432\u044B \u0441\u043E\u0445\u0440\u0430\u043D\u044F\u044E\u0442\u0441\u044F \u043B\u043E\u043A\u0430\u043B\u044C\u043D\u043E.
                        </p>
                    </div>
                </div>
            </div>`;

        document.getElementById('feedbackSubmitBtn').onclick = async () => {
            const name = document.getElementById('feedbackName').value.trim();
            const message = document.getElementById('feedbackMessage').value.trim();
            const resultDiv = document.getElementById('feedbackResult');
            if (!message) {
                resultDiv.innerHTML = '<span style="color:var(--error);">\u274C \u041D\u0430\u043F\u0438\u0448\u0438\u0442\u0435 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435</span>';
                return;
            }
            const btn = document.getElementById('feedbackSubmitBtn');
            btn.disabled = true;
            btn.textContent = '\u041E\u0442\u043F\u0440\u0430\u0432\u043A\u0430...';
            const res = await apiCall(`/api/feedback?name=${encodeURIComponent(name || 'Anonymous')}&message=${encodeURIComponent(message)}`, { method: 'POST' });
            if (res.status === 'ok') {
                resultDiv.innerHTML = '<span style="color:var(--success);">\u2705 ' + (res.detail || '\u0421\u043F\u0430\u0441\u0438\u0431\u043E!') + '</span>';
                document.getElementById('feedbackMessage').value = '';
                document.getElementById('feedbackName').value = '';
                if (window.Sounds) window.Sounds.success();
            } else {
                resultDiv.innerHTML = '<span style="color:var(--error);">\u274C ' + (res.detail || '\u041E\u0448\u0438\u0431\u043A\u0430') + '</span>';
                if (window.Sounds) window.Sounds.error();
            }
            btn.disabled = false;
            btn.textContent = '\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C';
        };
    }
};