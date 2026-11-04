/* Tab: History — Timeline of cybersecurity eras with progression + chat search */
window.Tab_history = {
    async render(el) {
        el.innerHTML = `<h2><i class="fas fa-history"></i> История кибербезопасности</h2>
            <div class="card" style="margin-bottom:16px;">
                <h3><i class="fas fa-search"></i> Поиск по истории чата</h3>
                <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;">
                    <input id="chat-search-q" class="input" style="flex:1;min-width:200px;" placeholder="Поиск в диалогах...">
                    <button id="chat-search-btn" class="btn btn-primary"><i class="fas fa-search"></i> Найти</button>
                </div>
                <div id="chat-search-results" style="margin-top:10px;font-size:0.9rem;"></div>
            </div>
            <div class="card"><p class="loading">Загрузка истории...</p></div>`;
        const [res, progressRes] = await Promise.all([
            apiCall('/api/history/eras').catch(() => ({ eras: [] })),
            apiCall('/api/history/progress').catch(() => ({ completed_eras: [], xp: 0 })),
        ]);
        const eras = res.eras || [];
        const completed = progressRes.completed_eras || [];
        const totalXp = progressRes.xp || 0;

        // Chat search
        const searchBtn = el.querySelector('#chat-search-btn');
        const searchQ = el.querySelector('#chat-search-q');
        const searchRes = el.querySelector('#chat-search-results');
        async function doSearch() {
            if (!searchRes) return;
            const q = searchQ?.value || '';
            searchRes.innerHTML = '<p style="color:var(--text-secondary);">Поиск...</p>';
            try {
                const r = await apiCall('/api/chat/history/search?q=' + encodeURIComponent(q) + '&limit=20').catch(() => ({ results: [] }));
                const items = r.results || [];
                if (!items.length) {
                    searchRes.innerHTML = '<p style="color:var(--text-secondary);">Ничего не найдено</p>';
                    return;
                }
                searchRes.innerHTML = items.map(it => `
                    <div style="padding:6px 0;border-bottom:1px solid var(--border);">
                        <div style="font-size:0.75rem;color:var(--text-secondary);">${it.role} ${it.timestamp ? '• ' + new Date(it.timestamp).toLocaleString() : ''}</div>
                        <div>${(it.content||'').replace(/</g,'&lt;').replace(/>/g,'&gt;').substring(0,200)}${(it.content||'').length>200?'...':''}</div>
                    </div>
                `).join('');
            } catch(e) {
                searchRes.innerHTML = '<p style="color:var(--error);">Ошибка поиска</p>';
            }
        }
        if (searchBtn) searchBtn.onclick = doSearch;
        if (searchQ) searchQ.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(); });

        if (!eras.length) {
            // keep search card, replace second card
            const cards = el.querySelectorAll('.card');
            if (cards[1]) cards[1].innerHTML = '<p style="color:var(--text-secondary);">Исторические эпохи не загружены</p>';
            return;
        }

        const cards = el.querySelectorAll('.card');
        if (cards[1]) {
            cards[1].innerHTML = `<div style="margin-bottom:16px;display:flex;gap:16px;flex-wrap:wrap;">
                <span>📊 Пройдено эпох: ${completed.length}/${eras.length}</span>
                <span>⚡ Всего XP: ${totalXp}</span>
            </div>
            <div style="position:relative;padding-left:20px;">${eras.map((era, i) => {
                const done = completed.includes(era.name);
                const locked = i > 0 && !completed.includes(eras[i-1].name) && !done;
                return `<div class="card" style="margin-bottom:12px;position:relative;${done ? 'opacity:0.6;' : ''}${locked ? 'opacity:0.3;' : ''}">
                    <div style="position:absolute;left:-20px;top:16px;width:12px;height:12px;border-radius:50%;background:${done ? 'var(--success)' : locked ? 'var(--error)' : 'var(--accent)'};"></div>
                    <h3>${done ? '✅ ' : locked ? '🔒 ' : ''}${era.name}</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);">${era.period}</p>
                    <p>${era.description || ''}</p>
                    ${!done && !locked ? `<button class="btn btn-sm btn-primary study-era" data-era="${era.name}">📖 Изучить +${era.xp || 20} XP</button>` : ''}
                    ${done ? `<span style="font-size:0.8rem;color:var(--success);">✅ Изучено</span>` : ''}
                    ${locked ? `<span style="font-size:0.8rem;color:var(--error);">🔒 Сначала изучите предыдущую эпоху</span>` : ''}
                    <div class="era-detail" style="display:none;margin-top:12px;"></div>
                </div>`;
            }).join('')}</div>`;
        }

        el.querySelectorAll('.study-era').forEach(btn => {
            btn.onclick = async () => {
                const card = btn.closest('.card');
                const detail = card.querySelector('.era-detail');
                btn.disabled = true;
                btn.textContent = 'Загрузка...';
                const res = await apiCall(`/api/history/study?era=${encodeURIComponent(btn.dataset.era)}`, { method: 'POST' });
                btn.disabled = false;
                detail.style.display = 'block';
                if (res.events && res.events.length) {
                    detail.innerHTML = `<div class="card" style="padding:12px;background:var(--bg-secondary);">
                        <h4>📅 Ключевые события</h4>
                        <ul style="margin:8px 0;">${res.events.map(e => `<li><strong>${e.year}:</strong> ${e.event}</li>`).join('')}</ul>
                        ${res.tools ? `<p><strong>🛠️ Инструменты:</strong> ${res.tools}</p>` : ''}
                        ${res.vulnerabilities ? `<p><strong>⚠️ Уязвимости:</strong> ${res.vulnerabilities}</p>` : ''}
                        <p style="margin-top:8px;color:var(--success);">✅ Изучено! +${res.xp_earned || 0} XP</p>
                    </div>`;
                }
                btn.textContent = '✅ Изучено';
                btn.disabled = true;
                if (window.Sounds) Sounds.success();
                await loadInitialData();
            };
        });
    }
};
