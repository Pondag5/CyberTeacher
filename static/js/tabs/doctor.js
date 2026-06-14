/* Tab: Doctor — LLM provider status + system health */
window.Tab_doctor = {
    async render(el) {
        el.innerHTML = '<div class="card"><p class="loading">\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430 \u0434\u0438\u0430\u0433\u043D\u043E\u0441\u0442\u0438\u043A\u0438...</p></div>';
        const data = await apiCall('/api/doctor').catch(() => null);
        if (!data) {
            el.innerHTML = '<h2>\uD83D\uDC69\u200D\uD83D\uDD2C \u0414\u0438\u0430\u0433\u043D\u043E\u0441\u0442\u0438\u043A\u0430</h2><div class="card"><p style="color:var(--error);">\u274C \u041D\u0435 \u0443\u0434\u0430\u043B\u043E\u0441\u044C \u043F\u043E\u043B\u0443\u0447\u0438\u0442\u044C \u0434\u0430\u043D\u043D\u044B\u0435</p></div>';
            return;
        }

        const providers = data.providers || [];
        const circuit = data.circuit_breakers || [];
        const current = data.current_provider || 'unknown';

        const providerCards = providers.map(p => {
            const ok = p.available && p.key_set && p.running !== false;
            const icon = ok ? '\u2705' : (p.key_set ? '\u26A0\uFE0F' : '\u274C');
            const color = ok ? 'var(--success)' : (p.key_set ? 'var(--warning)' : 'var(--error)');
            const detail = !p.key_set ? '\u041A\u043B\u044E\u0447 \u043D\u0435 \u0437\u0430\u0434\u0430\u043D' :
                p.running === false ? '\u041D\u0435 \u0437\u0430\u043F\u0443\u0449\u0435\u043D' :
                p.model_loaded === false ? `\u041C\u043E\u0434\u0435\u043B\u044C ${p.model} \u043D\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043D\u0430` :
                p.name === 'MockLLM' ? '\u0412\u0441\u0435\u0433\u0434\u0430 \u0434\u043E\u0441\u0442\u0443\u043F\u0435\u043D' :
                '\u0413\u043E\u0442\u043E\u0432';
            return `<div class="card" style="padding:12px;border-left:3px solid ${color};${current === p.name.toLowerCase() ? 'border-color:var(--accent);' : ''}">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div><strong>${icon} ${p.name}</strong>${current === p.name.toLowerCase() ? ' <span class="badge">\u0410\u043A\u0442\u0438\u0432\u0435\u043D</span>' : ''}</div>
                    <span style="color:${color};font-size:0.85rem;">${detail}</span>
                </div>
                ${p.model ? `<div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">\u041C\u043E\u0434\u0435\u043B\u044C: ${p.model}</div>` : ''}
            </div>`;
        }).join('');

        const circuitRows = circuit.map(c => {
            const state = c.circuit_state === 'closed' ? '\u2705 \u041E\u0442\u043A\u0440\u044B\u0442' : '\uD83D\uDD12 \u0417\u0430\u043A\u0440\u044B\u0442';
            const stateColor = c.circuit_state === 'closed' ? 'var(--success)' : 'var(--error)';
            return `<div style="display:flex;justify-content:space-between;padding:6px 8px;background:var(--bg);border-radius:4px;margin-bottom:4px;">
                <span>${c.model || c.name || '\u041D\u0435\u0438\u0437\u0432\u0435\u0441\u0442\u043D\u043E'}</span>
                <span style="color:${stateColor};">${state} (\u043E\u0448\u0438\u0431\u043E\u043A: ${c.failures || 0})</span>
            </div>`;
        }).join('');

        el.innerHTML = `<h2>\uD83D\uDC69\u200D\uD83D\uDD2C \u0414\u0438\u0430\u0433\u043D\u043E\u0441\u0442\u0438\u043A\u0430</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>\uD83D\uDEE0\uFE0F \u041F\u0440\u043E\u0432\u0430\u0439\u0434\u0435\u0440\u044B</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">
                        \u0422\u0435\u043A\u0443\u0449\u0438\u0439: <strong>${current}</strong> | Fallback: ${(data.fallback_order || []).join(' → ')}
                    </p>
                    <div style="display:flex;flex-direction:column;gap:8px;">${providerCards}</div>
                </div>
                <div class="card">
                    <h3>\u26A1 Circuit Breakers</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">
                        \u0421\u043E\u0441\u0442\u043E\u044F\u043D\u0438\u0435 \u043A\u0430\u043D\u0430\u043B\u043E\u0432 LLM
                    </p>
                    ${circuitRows || '<p style="color:var(--text-secondary);">\u041D\u0435\u0442 \u0434\u0430\u043D\u043D\u044B\u0445</p>'}
                </div>
            </div>
            <div class="card" style="margin-top:16px;">
                <h3>\u2139\uFE0F \u041A\u043E\u043C\u0430\u043D\u0434\u044B</h3>
                <div style="font-size:0.85rem;line-height:1.8;">
                    <code>/doctor test</code> — \u043F\u0440\u043E\u0442\u0435\u0441\u0442\u0438\u0440\u043E\u0432\u0430\u0442\u044C \u0432\u0441\u0435 \u043F\u0440\u043E\u0432\u0430\u0439\u0434\u0435\u0440\u044B<br>
                    <code>/doctor setup ollama</code> — \u0443\u0441\u0442\u0430\u043D\u043E\u0432\u0438\u0442\u044C Ollama<br>
                    <code>/doctor setup groq</code> — \u043D\u0430\u0441\u0442\u0440\u043E\u0438\u0442\u044C Groq API<br>
                    <code>/provider &lt;name&gt;</code> — \u0441\u043C\u0435\u043D\u0438\u0442\u044C \u043F\u0440\u043E\u0432\u0430\u0439\u0434\u0435\u0440 \u0432 \u041D\u0430\u0441\u0442\u0440\u043E\u0439\u043A\u0430\u0445
                </div>
            </div>`;
    }
};