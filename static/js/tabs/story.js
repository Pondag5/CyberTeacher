/* Tab: Story — chapters + episodes with narrative */
window.Tab_story = {
    _currentChapterId: null,
    _currentEpisodeId: null,

    async render(el) {
        const [chData, epData] = await Promise.all([
            apiCall('/api/chapters'),
            apiCall('/api/story')
        ]);
        const chapters = chData.chapters || [];
        const episodes = epData.episodes || [];
        appState.storyEpisodes = episodes;

        el.innerHTML = `<h2>\uD83D\uDCDC Story Mode</h2>
        <div style="margin-bottom:16px; display:flex; gap:8px; flex-wrap:wrap;">
            <button class="tab-btn active" data-view="chapters">\uD83D\uDCD6 Главы</button>
            <button class="tab-btn" data-view="episodes">\uD83C\uDFB2 Эпизоды</button>
        </div>
        <div id="story-view"></div>`;

        const showView = (view) => {
            const container = el.querySelector('#story-view');
            el.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.view === view));
            if (view === 'chapters') this._renderChapters(container, chapters, episodes);
            else this._renderEpisodes(container, episodes);
        };

        el.querySelectorAll('.tab-btn').forEach(btn => {
            btn.onclick = () => showView(btn.dataset.view);
        });
        showView('chapters');
    },

    _renderChapters(container, chapters, episodes) {
        container.innerHTML = `<div class="grid-2">${chapters.map(ch => `
            <div class="card" data-ch="${ch.id}"
                 style="${ch.locked ? 'opacity:0.3;' : ''} ${ch.completed ? 'border-left:3px solid var(--success);' : ''}">
                <h3>${ch.locked ? '\uD83D\uDD12 ' : ch.completed ? '\u2705 ' : ''}Глава ${ch.id}: ${ch.title}</h3>
                <p style="color:var(--text-secondary); font-size:0.85rem;">${ch.subtitle || ''}</p>
                <div style="margin:8px 0;">
                    <div style="height:6px; background:var(--bg-secondary); border-radius:3px; overflow:hidden;">
                        <div style="width:${ch.progress}%; height:100%; background:var(--accent); border-radius:3px;"></div>
                    </div>
                    <span style="font-size:0.75rem; color:var(--text-secondary);">${ch.episodes_completed || 0}/${ch.episode_count} эпизодов</span>
                </div>
                ${ch.locked ? '<p style="font-size:0.8rem;color:var(--error);">\uD83D\uDD12 Завершите предыдущую главу</p>' : ''}
                ${!ch.locked && !ch.completed ? `<button class="start-chapter" data-ch="${ch.id}">\uD83D\uDCD6 Начать главу</button>` : ''}
                ${ch.completed ? `<span style="font-size:0.8rem;color:var(--success);">\u2728 Артефакт получен</span>` : ''}
                <div class="chapter-detail" style="display:none; margin-top:12px;"></div>
            </div>
        `).join('')}</div>`;

        container.querySelectorAll('.start-chapter').forEach(btn => {
            btn.onclick = async () => {
                const chId = parseInt(btn.dataset.ch);
                const res = await apiCall('/api/chapter/start', { method: 'POST', body: { chapter_id: chId } });
                if (res.intro) {
                    const card = btn.closest('.card');
                    const detail = card.querySelector('.chapter-detail');
                    detail.style.display = 'block';
                    detail.innerHTML = `<div class="card" style="padding:16px; background:var(--bg-secondary);">
                        <p style="white-space:pre-wrap;">${res.intro}</p>
                        <button class="start-episode" data-ch="${chId}" style="margin-top:12px;">\uD83C\uDFB2 К эпизодам</button>
                    </div>`;
                    btn.textContent = '\u25BC Свернуть';
                    detail.querySelector('.start-episode').onclick = () => {
                        container.closest('#story-view').parentElement?.querySelector('[data-view="episodes"]')?.click();
                    };
                }
            };
        });
    },

    _renderEpisodes(container, episodes) {
        container.innerHTML = `<div class="grid-2">${episodes.map(ep => `
            <div class="card" data-ep="${ep.id}"
                 ${ep.completed ? 'style="opacity:0.6;"' : ''} ${ep.locked ? 'style="opacity:0.3;"' : ''}>
                <h3>${ep.locked ? '\uD83D\uDD12 ' : ep.completed ? '\u2705 ' : ''}${ep.title || '\u042D\u043F\u0438\u0437\u043E\u0434 ' + ep.id}</h3>
                <p>${ep.desc || ''}</p>
                <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                    <span class="badge">\u0421\u043B\u043E\u0436\u043D\u043E\u0441\u0442\u044C: ${ep.difficulty || 1}/4</span>
                    <span style="font-size:0.8rem; color:var(--text-secondary);">+${ep.xp || 0} XP</span>
                    ${ep.category ? `<span style="font-size:0.8rem; color:var(--accent);">${ep.category}</span>` : ''}
                </div>
                ${ep.locked ? '<p style="font-size:0.8rem;color:var(--error);margin-top:4px;">\uD83D\uDD12 Завершите предыдущий</p>' : ''}
                ${!ep.locked ? `<button data-ep="${ep.id}" class="start-story" ${ep.completed ? 'disabled' : ''}>${ep.completed ? '\u2705 Пройдено' : '\u041D\u0430\u0447\u0430\u0442\u044C'}</button>` : ''}
                <div class="story-detail" style="display:none; margin-top:12px;"></div>
            </div>
        `).join('')}</div>`;

        container.querySelectorAll('.start-story').forEach(btn => {
            btn.onclick = async () => {
                const card = btn.closest('.card');
                const detail = card.querySelector('.story-detail');
                const epId = parseInt(btn.dataset.ep);
                if (detail.style.display === 'block') {
                    detail.style.display = 'none';
                    btn.textContent = card.style.opacity === '0.6' ? '\u2705 Пройдено' : '\u041D\u0430\u0447\u0430\u0442\u044C';
                    return;
                }
                btn.disabled = true;
                btn.textContent = '\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430...';
                const res = await apiCall(`/start_story_episode?episode_id=${epId}`, { method: 'POST' });
                btn.disabled = false;
                if (res.prompt) {
                    const ep = (appState.storyEpisodes || []).find(e => e.id === epId) || {};
                    const objs = Array.isArray(ep.obj) ? ep.obj : (ep.objectives || []);
                    const hints = Array.isArray(ep.hint) ? ep.hint : (ep.hints || []);
                    detail.style.display = 'block';
                    detail.innerHTML = `
                        <div class="card" style="padding:16px; background:var(--bg-secondary);">
                            <h3 style="margin-bottom:8px;">\uD83D\uDCD6 ${ep.title || '\u042D\u043F\u0438\u0437\u043E\u0434 ' + ep.id}</h3>
                            <p style="white-space:pre-wrap; margin-bottom:12px;">${res.prompt}</p>
                            ${objs.length ? `<div style="margin-bottom:12px;"><strong>\uD83C\uDFAF Цели:</strong><ul style="margin:4px 0 0 16px;">${objs.map(o => `<li>${o}</li>`).join('')}</ul></div>` : ''}
                            ${hints.length ? `<div style="margin-bottom:12px;"><strong>\uD83D\uDCA1 Подсказка:</strong><div style="margin:4px 0 0 16px; color:var(--text-secondary);">${hints[0]}</div></div>` : ''}
                            ${ep.lab ? `<div style="margin-bottom:12px;"><strong>\uD83D\uDC33 Лаборатория:</strong> ${ep.lab}</div>` : ''}
                            <div style="margin-top:12px; display:flex; gap:8px;">
                                <input class="flag-input" placeholder="Введите FLAG{...}" style="flex:1;">
                                <button class="flag-submit" data-ep="${epId}">\uD83D\uDE80 Отправить</button>
                            </div>
                            <div class="flag-result" style="margin-top:8px;"></div>
                        </div>
                    `;
                    btn.textContent = '\u25BC Свернуть';
                    if (window.Sounds) Sounds.success();
                    this._attachFlagHandler(detail, epId);
                } else {
                    btn.textContent = '\u041D\u0430\u0447\u0430\u0442\u044C';
                }
                this._currentEpisodeId = epId;
            };
        });
    },

    _attachFlagHandler(detail, epId) {
        const submitBtn = detail.querySelector('.flag-submit');
        const input = detail.querySelector('.flag-input');
        const resultDiv = detail.querySelector('.flag-result');
        if (!submitBtn || !input) return;
        submitBtn.onclick = async () => {
            const answer = input.value.trim();
            if (!answer) return;
            submitBtn.disabled = true;
            submitBtn.textContent = '\u23F3 Проверка...';
            const res = await apiCall(`/api/story/submit?answer=${encodeURIComponent(answer)}`, { method: 'POST' });
            submitBtn.disabled = false;
            submitBtn.textContent = '\uD83D\uDE80 Отправить';
            if (res.correct) {
                resultDiv.innerHTML = `\u2705 Правильно! +${res.xp_earned || 100} XP`;
                resultDiv.style.color = 'var(--success)';
                input.disabled = true;
                if (window.Sounds) Sounds.achievement();
                await loadInitialData();
                const ep = (appState.storyEpisodes || []).find(e => e.id === epId);
                const card = detail.closest('.card');
                if (ep && ep.completed) card.style.opacity = '0.6';
            } else {
                const hint = res.hint ? `\uD83D\uDCA1 ${res.hint}` : '';
                resultDiv.innerHTML = `\u274C Неверно. ${hint}`;
                resultDiv.style.color = 'var(--error)';
                if (window.Sounds) Sounds.error();
            }
        };
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') submitBtn.click();
        });
    }
};