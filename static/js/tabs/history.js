/* Tab: History — Timeline of cybersecurity eras with progression */
window.Tab_history = {
    async render(el) {
        el.innerHTML = '<div class="card"><p class="loading">\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430 \u0438\u0441\u0442\u043E\u0440\u0438\u0438...</p></div>';
        const [res, progressRes] = await Promise.all([
            apiCall('/api/history/eras').catch(() => ({ eras: [] })),
            apiCall('/api/history/progress').catch(() => ({ completed_eras: [], xp: 0 })),
        ]);
        const eras = res.eras || [];
        const completed = progressRes.completed_eras || [];
        const totalXp = progressRes.xp || 0;

        if (!eras.length) {
            el.innerHTML = '<h2><i class="fas fa-history"></i> \u0418\u0441\u0442\u043E\u0440\u0438\u044F \u043A\u0438\u0431\u0435\u0440\u0431\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u043E\u0441\u0442\u0438</h2><div class="card"><p style="color:var(--text-secondary);">\u0418\u0441\u0442\u043E\u0440\u0438\u0447\u0435\u0441\u043A\u0438\u0435 \u044D\u043F\u043E\u0445\u0438 \u043D\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043D\u044B</p></div>';
            return;
        }

        el.innerHTML = `<h2><i class="fas fa-history"></i> \u0418\u0441\u0442\u043E\u0440\u0438\u044F \u043A\u0438\u0431\u0435\u0440\u0431\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u043E\u0441\u0442\u0438</h2>
            <div style="margin-bottom:16px;display:flex;gap:16px;flex-wrap:wrap;">
                <span>\uD83D\uDCCA \u041F\u0440\u043E\u0439\u0434\u0435\u043D\u043E \u044D\u043F\u043E\u0445: ${completed.length}/${eras.length}</span>
                <span>\u26A1 \u0412\u0441\u0435\u0433\u043E XP: ${totalXp}</span>
            </div>
            <div style="position:relative;padding-left:20px;">${eras.map((era, i) => {
                const done = completed.includes(era.name);
                const locked = i > 0 && !completed.includes(eras[i-1].name) && !done;
                return `<div class="card" style="margin-bottom:12px;position:relative;${done ? 'opacity:0.6;' : ''}${locked ? 'opacity:0.3;' : ''}">
                    <div style="position:absolute;left:-20px;top:16px;width:12px;height:12px;border-radius:50%;background:${done ? 'var(--success)' : locked ? 'var(--error)' : 'var(--accent)'};"></div>
                    <h3>${done ? '\u2705 ' : locked ? '\uD83D\uDD12 ' : ''}${era.name}</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);">${era.period}</p>
                    <p>${era.description || ''}</p>
                    ${!done && !locked ? `<button class="btn btn-sm btn-primary study-era" data-era="${era.name}">\uD83D\uDCD6 \u0418\u0437\u0443\u0447\u0438\u0442\u044C +${era.xp || 20} XP</button>` : ''}
                    ${done ? `<span style="font-size:0.8rem;color:var(--success);">\u2705 \u0418\u0437\u0443\u0447\u0435\u043D\u043E</span>` : ''}
                    ${locked ? `<span style="font-size:0.8rem;color:var(--error);">\uD83D\uDD12 \u0421\u043D\u0430\u0447\u0430\u043B\u0430 \u0438\u0437\u0443\u0447\u0438\u0442\u0435 \u043F\u0440\u0435\u0434\u044B\u0434\u0443\u0449\u0443\u044E \u044D\u043F\u043E\u0445\u0443</span>` : ''}
                    <div class="era-detail" style="display:none;margin-top:12px;"></div>
                </div>`;
            }).join('')}</div>`;

        el.querySelectorAll('.study-era').forEach(btn => {
            btn.onclick = async () => {
                const card = btn.closest('.card');
                const detail = card.querySelector('.era-detail');
                btn.disabled = true;
                btn.textContent = '\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430...';
                const res = await apiCall(`/api/history/study?era=${encodeURIComponent(btn.dataset.era)}`, { method: 'POST' });
                btn.disabled = false;
                detail.style.display = 'block';
                if (res.events && res.events.length) {
                    detail.innerHTML = `<div class="card" style="padding:12px;background:var(--bg-secondary);">
                        <h4>\uD83D\uDCC5 \u041A\u043B\u044E\u0447\u0435\u0432\u044B\u0435 \u0441\u043E\u0431\u044B\u0442\u0438\u044F</h4>
                        <ul style="margin:8px 0;">${res.events.map(e => `<li><strong>${e.year}:</strong> ${e.event}</li>`).join('')}</ul>
                        ${res.tools ? `<p><strong>\uD83D\uDEE0\uFE0F \u0418\u043D\u0441\u0442\u0440\u0443\u043C\u0435\u043D\u0442\u044B:</strong> ${res.tools}</p>` : ''}
                        ${res.vulnerabilities ? `<p><strong>\u26A0\uFE0F \u0423\u044F\u0437\u0432\u0438\u043C\u043E\u0441\u0442\u0438:</strong> ${res.vulnerabilities}</p>` : ''}
                        <p style="margin-top:8px;color:var(--success);">\u2705 \u0418\u0437\u0443\u0447\u0435\u043D\u043E! +${res.xp_earned || 0} XP</p>
                    </div>`;
                }
                btn.textContent = '\u2705 \u0418\u0437\u0443\u0447\u0435\u043D\u043E';
                btn.disabled = true;
                if (window.Sounds) Sounds.success();
                await loadInitialData();
            };
        });
    }
};
