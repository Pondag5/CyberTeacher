/* Tab: Missions — with prerequisites, locked state, and flag submission */
window.Tab_missions = {
    async render(el) {
        el.innerHTML = '<div class="card"><p class="loading">\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430 \u043C\u0438\u0441\u0441\u0438\u0439...</p></div>';
        const res = await apiCall('/api/missions').catch(() => ({ missions: [] }));
        const missions = res.missions || [];
        if (!missions.length) {
            el.innerHTML = '<h2>\uD83C\uDFC1 \u041C\u0438\u0441\u0441\u0438\u0438</h2><div class="card"><p style="color:var(--text-secondary);">\u041D\u0435\u0442 \u0434\u043E\u0441\u0442\u0443\u043F\u043D\u044B\u0445 \u043C\u0438\u0441\u0441\u0438\u0439</p></div>';
            return;
        }
        el.innerHTML = `<h2>\uD83C\uDFC1 \u041C\u0438\u0441\u0441\u0438\u0438</h2>
            <div class="grid-2">${missions.map(m => {
                const diffColor = m.difficulty === 'easy' ? 'var(--success)' : m.difficulty === 'medium' ? 'var(--warning)' : 'var(--error)';
                const isLocked = m.locked && !m.completed;
                return `<div class="card" data-mission="${m.id}" style="${m.completed ? 'opacity:0.6;' : ''} ${isLocked ? 'opacity:0.4;' : ''}">
                    <h3>${m.completed ? '\u2705 ' : isLocked ? '\uD83D\uDD12 ' : ''}${m.name}</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);">${m.desc || ''}</p>
                    <div style="display:flex;gap:8px;margin-top:8px;align-items:center;">
                        <span class="badge" style="background:${diffColor};">${m.difficulty || 'medium'}</span>
                        <span style="font-size:0.8rem;">+${m.xp_reward || 0} XP</span>
                        ${!m.completed && !isLocked ? `<button class="btn btn-sm btn-primary start-mission" data-id="${m.id}">\u041D\u0430\u0447\u0430\u0442\u044C</button>` : ''}
                    </div>
                    ${isLocked && m.prerequisites && m.prerequisites.length ? `<p style="font-size:0.75rem;color:var(--error);margin-top:4px;">\uD83D\uDD12 \u0422\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044F: ${m.prerequisites.join(', ')}</p>` : ''}
                    <div class="mission-detail" style="display:none;margin-top:12px;"></div>
                </div>`;
            }).join('')}</div>
            <div id="missionsRisk" style="margin-top:16px;"></div>
        `;

        el.querySelectorAll('.start-mission').forEach(btn => {
            btn.addEventListener('click', async () => {
                btn.disabled = true;
                btn.textContent = '\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430...';
                const res = await apiCall(`/api/missions/start?mission_id=${btn.dataset.id}`, { method: 'POST' });
                btn.disabled = false;
                const card = btn.closest('.card');
                const detail = card.querySelector('.mission-detail');
                if (res.mission || res.status === 'ok') {
                    const data = res.mission || res;
                    const steps = data.steps || [];
                    detail.style.display = 'block';
                    detail.innerHTML = `<div class="card" style="padding:12px;background:var(--bg);">
                        <h4>\uD83D\uDCD6 ${data.name || data.title || btn.dataset.id}</h4>
                        <p style="white-space:pre-wrap;margin:8px 0;font-size:0.85rem;">${data.description || data.desc || '\u0417\u0430\u043F\u0443\u0449\u0435\u043D\u043E'}</p>
                        ${steps.length ? `<div style="margin-bottom:8px;"><strong>\uD83C\uDFAF \u0428\u0430\u0433\u0438:</strong><ol style="margin:4px 0 0 16px;">${steps.map(s => `<li>${s.objective || s.flag || ''}</li>`).join('')}</ol></div>` : ''}
                        ${data.hint ? `<div style="margin-top:8px;font-size:0.85rem;color:var(--accent);">\uD83D\uDCA1 ${data.hint}</div>` : ''}
                        <div style="margin-top:12px;display:flex;gap:8px;">
                            <input class="mission-flag-input" placeholder="\u0412\u0432\u0435\u0434\u0438\u0442\u0435 FLAG{...}" style="flex:1;">
                            <button class="mission-flag-submit" data-id="${btn.dataset.id}">\uD83D\uDE80 \u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C</button>
                        </div>
                        <div class="mission-flag-result" style="margin-top:8px;"></div>
                    </div>`;
                    btn.textContent = '\u25BC \u0421\u0432\u0435\u0440\u043D\u0443\u0442\u044C';
                    this._attachSubmitHandler(detail, btn.dataset.id);
                } else {
                    btn.textContent = '\u041D\u0430\u0447\u0430\u0442\u044C';
                    if (res.detail) alert(res.detail);
                }
            });
        });

        this._riskInterval = setInterval(() => this._updateRisk(), 10000);
        this._updateRisk();
    },

    _attachSubmitHandler(detail, missionId) {
        const submitBtn = detail.querySelector('.mission-flag-submit');
        const input = detail.querySelector('.mission-flag-input');
        const resultDiv = detail.querySelector('.mission-flag-result');
        if (!submitBtn || !input) return;
        submitBtn.onclick = async () => {
            const flag = input.value.trim();
            if (!flag) return;
            submitBtn.disabled = true;
            submitBtn.textContent = '\u23F3 ...';
            const res = await apiCall(`/api/missions/submit?mission_id=${missionId}&flag=${encodeURIComponent(flag)}`, { method: 'POST' });
            submitBtn.disabled = false;
            submitBtn.textContent = '\uD83D\uDE80 \u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C';
            if (res.correct) {
                resultDiv.innerHTML = `\u2705 \u0428\u0430\u0433 ${res.step || ''} \u0432\u044B\u043F\u043E\u043B\u043D\u0435\u043D! +${res.xp_earned || 0} XP`;
                resultDiv.style.color = 'var(--success)';
                input.disabled = true;
                if (window.Sounds) Sounds.achievement();
                await loadInitialData();
                this.render(document.querySelector('#content .tab-content'));
            } else {
                resultDiv.innerHTML = `\u274C ${res.message || '\u041D\u0435\u0432\u0435\u0440\u043D\u044B\u0439 \u0444\u043B\u0430\u0433'}`;
                resultDiv.style.color = 'var(--error)';
            }
        };
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') submitBtn.click();
        });
    },

    async _updateRisk() {
        const container = document.getElementById('missionsRisk');
        if (!container) return;
        try {
            const [noise, trace, debts] = await Promise.all([
                apiCall('/api/noise'),
                apiCall('/api/trace'),
                apiCall('/api/debts'),
            ]);
            const noisePct = Math.min(noise.level || 0, 100);
            const noiseColor = noisePct > 70 ? 'var(--error)' : noisePct > 40 ? 'var(--warning, orange)' : 'var(--success)';
            const traceActive = trace.active && !trace.expired;
            const tracePct = traceActive ? Math.min((trace.remaining_seconds || 0) / 180 * 100, 100) : 0;
            container.innerHTML = `
                <div class="card">
                    <h3>\uD83D\uDCCA Risk Status</h3>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between;"><span>\uD83D\uDCF4 Noise</span><span>${noisePct}%</span></div>
                        <div style="height:8px; background:var(--bg-secondary); border-radius:4px; overflow:hidden;"><div style="width:${noisePct}%; height:100%; background:${noiseColor}; border-radius:4px; transition: width 0.5s;"></div></div>
                    </div>
                    <div style="margin-bottom:8px; display:${traceActive ? 'block' : 'none'};">
                        <div style="display:flex; justify-content:space-between;"><span>\uD83D\uDD0D Trace</span><span>${Math.ceil((trace.remaining_seconds || 0) / 60)}m ${(trace.remaining_seconds || 0) % 60}s</span></div>
                        <div style="height:8px; background:var(--bg-secondary); border-radius:4px; overflow:hidden;"><div style="width:${tracePct}%; height:100%; background:var(--error); border-radius:4px; transition: width 1s;"></div></div>
                        <div style="font-size:0.75rem; color:var(--text-secondary);">Target: ${trace.target || '?'}</div>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between;"><span>\uD83D\uDCB3 Debts</span><span style="color:${(debts.total || 0) >= 5 ? 'var(--error)' : (debts.total || 0) >= 3 ? 'orange' : 'inherit'};">${debts.total || 0}</span></div>
                    </div>
                </div>
            `;
        } catch (e) { /* silent */ }
    }
};
