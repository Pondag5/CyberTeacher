/* Tab: Context — context budget manager + chat history */
window.Tab_context = {
    async render(el) {
        el.innerHTML = '<div class="card"><p class="loading">\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430 \u043A\u043E\u043D\u0442\u0435\u043A\u0441\u0442\u0430...</p></div>';
        const [budget, history] = await Promise.all([
            apiCall('/api/context/budget').catch(() => null),
            apiCall('/api/context/history').catch(() => []),
        ]);

        const stats = budget || {};
        const hist = Array.isArray(history) ? history : (history.history || history.messages || []);

        const pct = stats.budget_max ? Math.round((stats.budget_used || 0) / stats.budget_max * 100) : 0;
        const barColor = pct > 80 ? 'var(--error)' : pct > 50 ? 'var(--warning)' : 'var(--success)';
        const bar = `<div style="height:20px;background:var(--bg);border-radius:10px;overflow:hidden;">
            <div style="height:100%;width:${Math.min(pct, 100)}%;background:${barColor};border-radius:10px;transition:width 0.3s;"></div>
        </div>`;

        el.innerHTML = `<h2>\uD83D\uDCCA \u041A\u043E\u043D\u0442\u0435\u043A\u0441\u0442</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>\uD83D\uDCC8 \u0411\u044E\u0434\u0436\u0435\u0442 \u043A\u043E\u043D\u0442\u0435\u043A\u0441\u0442\u0430</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">
                        \u0418\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u043D\u043E: ${stats.budget_used || 0} / ${stats.budget_max || '...'} \u0442\u043E\u043A\u0435\u043D\u043E\u0432
                    </p>
                    ${bar}
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px;font-size:0.85rem;">
                        <div>\u0421\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0439: ${stats.message_count || 0}</div>
                        <div>\u0421\u0436\u0430\u0442\u0438\u0439: ${stats.summary_count || 0}</div>
                        <div>\u041C\u0430\u043A\u0441 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0439: ${stats.max_messages || 30}</div>
                        <div>\u0422\u043E\u043A\u0435\u043D\u043E\u0432 \u043D\u0430 \u0441\u0436\u0430\u0442\u0438\u0435: ${stats.summary_tokens || 500}</div>
                    </div>
                    <div style="margin-top:12px;display:flex;gap:8px;">
                        <button class="btn btn-sm btn-primary" id="contextClearBtn">\uD83D\uDDD1\uFE0F \u041E\u0447\u0438\u0441\u0442\u0438\u0442\u044C</button>
                    </div>
                </div>
                <div class="card">
                    <h3>\u26A0\uFE0F \u041A\u043E\u043D\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044F</h3>
                    <div style="display:flex;flex-direction:column;gap:12px;">
                        <div>
                            <label style="font-size:0.85rem;display:block;margin-bottom:4px;">\u041C\u0430\u043A\u0441\u0438\u043C\u0443\u043C \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0439</label>
                            <input type="number" id="contextMaxMsg" value="${stats.max_messages || 30}" min="5" max="200" style="width:100px;">
                        </div>
                        <div>
                            <label style="font-size:0.85rem;display:block;margin-bottom:4px;">\u0422\u043E\u043A\u0435\u043D\u043E\u0432 \u043D\u0430 \u0441\u0436\u0430\u0442\u0438\u0435</label>
                            <input type="number" id="contextSummaryTokens" value="${stats.summary_tokens || 500}" min="100" max="2000" step="100" style="width:100px;">
                        </div>
                        <div>
                            <label style="font-size:0.85rem;display:block;margin-bottom:4px;">\u0411\u044E\u0434\u0436\u0435\u0442 (\u0442\u043E\u043A\u0435\u043D\u044B)</label>
                            <input type="number" id="contextBudgetMax" value="${stats.budget_max || 4000}" min="1000" max="32000" step="500" style="width:120px;">
                        </div>
                        <button class="btn btn-sm btn-primary" id="contextSaveBtn" style="align-self:flex-start;">\uD83D\uDCBE \u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C</button>
                        <div id="contextConfigResult" style="font-size:0.85rem;"></div>
                    </div>
                </div>
            </div>
            <div class="card" style="margin-top:16px;">
                <h3>\uD83D\uDCDC \u0418\u0441\u0442\u043E\u0440\u0438\u044F \u0447\u0430\u0442\u0430</h3>
                <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:8px;">
                    \u041F\u043E\u0441\u043B\u0435\u0434\u043D\u0438\u0435 ${hist.length} \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0439
                </p>
                <div style="max-height:300px;overflow-y:auto;font-size:0.85rem;">
                ${hist.slice(-20).reverse().map((m: any) => {
                    const role = (m.role || m.role_name || 'unknown') === 'user' ? '\uD83D\uDC64' : '\uD83E\uDD16';
                    const content = (m.content || m.message || '')?.slice(0, 200);
                    const ts = m.timestamp ? new Date(m.timestamp).toLocaleString() : '';
                    return `<div style="padding:6px 8px;margin-bottom:4px;background:var(--bg);border-radius:4px;">
                        <div style="display:flex;justify-content:space-between;">
                            <strong>${role} ${role === '\uD83D\uDC64' ? '\u0423\u0447\u0435\u043D\u0438\u043A' : '\u0423\u0447\u0438\u0442\u0435\u043B\u044C'}</strong>
                            <small style="color:var(--text-secondary);">${ts}</small>
                        </div>
                        <div style="color:var(--text-secondary);">${content}</div>
                    </div>`;
                }).join('')}
                </div>
            </div>`;

        el.querySelector('#contextClearBtn')?.addEventListener('click', async () => {
            if (!confirm('\u041E\u0447\u0438\u0441\u0442\u0438\u0442\u044C \u0432\u0441\u044E \u0438\u0441\u0442\u043E\u0440\u0438\u044E \u0447\u0430\u0442\u0430?')) return;
            const res = await apiCall('/api/context/budget?action=clear', { method: 'POST' });
            if (res.status === 'ok' || res.budget_used !== undefined) {
                if (window.Sounds) window.Sounds.success();
                this.render(el);
            }
        });

        el.querySelector('#contextSaveBtn')?.addEventListener('click', async () => {
            const maxMsg = parseInt(el.querySelector('#contextMaxMsg')?.value || '30');
            const summaryTokens = parseInt(el.querySelector('#contextSummaryTokens')?.value || '500');
            const budgetMax = parseInt(el.querySelector('#contextBudgetMax')?.value || '4000');
            const resultDiv = el.querySelector('#contextConfigResult');
            if (!resultDiv) return;
            resultDiv.innerHTML = '\u23F3 \u0421\u043E\u0445\u0440\u0430\u043D\u0435\u043D\u0438\u0435...';
            const res = await apiCall('/api/context/budget', {
                method: 'POST',
                body: JSON.stringify({ max_messages: maxMsg, summary_tokens: summaryTokens, budget_max: budgetMax }),
            });
            if (res.status === 'ok') {
                resultDiv.innerHTML = '<span style="color:var(--success);">\u2705 \u0421\u043E\u0445\u0440\u0430\u043D\u0435\u043D\u043E</span>';
                if (window.Sounds) window.Sounds.success();
            } else {
                resultDiv.innerHTML = `<span style="color:var(--error);">\u274C ${res.detail || '\u041E\u0448\u0438\u0431\u043A\u0430'}</span>`;
                if (window.Sounds) window.Sounds.error();
            }
        });
    }
};