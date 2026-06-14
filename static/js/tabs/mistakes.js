/* Tab: Common Mistakes — weak topics and quiz history */
window.Tab_mistakes = {
    async render(el) {
        el.innerHTML = '<div class="card"><p class="loading">\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430 \u043E\u0448\u0438\u0431\u043E\u043A...</p></div>';

        const [weakRes, statsRes] = await Promise.all([
            apiCall('/api/weak-topics'),
            apiCall('/api/stats'),
        ]);

        const weak = weakRes.weak_topics || [];
        const stats = statsRes.quiz_history || [];
        const mistakes = stats.filter(s => (s.score || 0) < (s.total || 1) * 0.6);

        if (!weak.length && !mistakes.length) {
            el.innerHTML = `
                <h2>\u274C \u0427\u0430\u0441\u0442\u044B\u0435 \u043E\u0448\u0438\u0431\u043A\u0438</h2>
                <div class="card">
                    <p style="color:var(--success);">\u2705 \u041E\u0448\u0438\u0431\u043E\u043A \u043D\u0435\u0442! \u0412\u044B \u043E\u0442\u043B\u0438\u0447\u043D\u043E \u0441\u043F\u0440\u0430\u0432\u043B\u044F\u0435\u0442\u0435\u0441\u044C.</p>
                </div>`;
            return;
        }

        el.innerHTML = `<h2>\u274C \u0427\u0430\u0441\u0442\u044B\u0435 \u043E\u0448\u0438\u0431\u043A\u0438</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>\uD83D\uDCA1 \u0421\u043B\u0430\u0431\u044B\u0435 \u0442\u0435\u043C\u044B</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">
                        \u0422\u0435\u043C\u044B, \u0433\u0434\u0435 \u0432\u044B \u043D\u0430\u0431\u0440\u0430\u043B\u0438 &lt;60% \u043F\u0440\u0430\u0432\u0438\u043B\u044C\u043D\u044B\u0445 \u043E\u0442\u0432\u0435\u0442\u043E\u0432
                    </p>
                    ${weak.map(t => `
                        <div style="display:flex;align-items:center;gap:8px;padding:8px;background:var(--bg);border-radius:6px;margin-bottom:6px;">
                            <span style="color:var(--error);">\u26A0\uFE0F</span>
                            <span>${t}</span>
                            <a href="#" class="btn btn-sm btn-secondary" style="margin-left:auto;" data-quiz-topic="${t}">
                                \uD83D\uDCDD \u041F\u0440\u043E\u0439\u0442\u0438 \u043A\u0432\u0438\u0437
                            </a>
                        </div>
                    `).join('')}
                </div>
                <div class="card">
                    <h3>\uD83D\uDCCA \u041F\u0440\u043E\u0432\u0430\u043B\u0435\u043D\u043D\u044B\u0435 \u043A\u0432\u0438\u0437\u044B</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">
                        \u041F\u043E\u0441\u043B\u0435\u0434\u043D\u0438\u0435 \u043A\u0432\u0438\u0437\u044B \u0441 \u0440\u0435\u0437\u0443\u043B\u044C\u0442\u0430\u0442\u043E\u043C &lt;60%
                    </p>
                    ${mistakes.length ? mistakes.slice(-10).reverse().map(m => {
                        const pct = Math.round((m.score || 0) / (m.total || 1) * 100);
                        return `<div style="padding:8px;background:var(--bg);border-radius:6px;margin-bottom:6px;">
                            <div style="display:flex;justify-content:space-between;">
                                <strong>${m.topic || '\u041D\u0435\u0438\u0437\u0432\u0435\u0441\u0442\u043D\u043E'}</strong>
                                <span style="color:${pct < 30 ? 'var(--error)' : 'var(--warning)'};">${m.score}/${m.total} (${pct}%)</span>
                            </div>
                            ${m.date ? `<small style="color:var(--text-secondary);">${m.date}</small>` : ''}
                        </div>`;
                    }).join('') : '<p style="color:var(--text-secondary);">\u041D\u0435\u0442 \u0434\u0430\u043D\u043D\u044B\u0445</p>'}
                </div>
            </div>
            <div class="card" style="margin-top:16px;">
                <h3>\uD83D\uDCD6 \u0420\u0435\u043A\u043E\u043C\u0435\u043D\u0434\u0430\u0446\u0438\u0438</h3>
                <ul style="line-height:1.8;font-size:0.9rem;">
                    ${weak.length ? `<li>\u041F\u043E\u0432\u0442\u043E\u0440\u0438\u0442\u0435 \u0442\u0435\u043C\u044B: <strong>${weak.join(', ')}</strong></li>` : ''}
                    <li>\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0439\u0442\u0435 \u0440\u0435\u0436\u0438\u043C \u043F\u043E\u0432\u0442\u043E\u0440\u0435\u043D\u0438\u044F \u0432 \u043A\u0432\u0438\u0437\u0430\u0445</li>
                    <li>\u041F\u0440\u043E\u0445\u043E\u0434\u0438\u0442\u0435 \u043B\u0430\u0431\u044B \u043F\u043E \u0441\u043B\u0430\u0431\u044B\u043C \u0442\u0435\u043C\u0430\u043C</li>
                </ul>
            </div>`;

        el.querySelectorAll('[data-quiz-topic]').forEach(a => {
            a.addEventListener('click', e => {
                e.preventDefault();
                const topic = a.dataset.quizTopic;
                if (window.appState && window.Sounds) window.Sounds.click();
                if (window.renderTab) window.renderTab('quiz');
            });
        });
    }
};