/* Tab: Tracks — with topic list, progress, navigation */
window.Tab_tracks = {
    async render(el) {
        const tracks = appState.tracks || [];
        el.innerHTML = `<h2>\uD83D\uDEE4\uFE0F \u0422\u0440\u0435\u043A\u0438 \u043E\u0431\u0443\u0447\u0435\u043D\u0438\u044F</h2>
        <p style="color:var(--text-secondary); margin-bottom:16px;">\u041F\u043E\u0441\u043B\u0435\u0434\u043E\u0432\u0430\u0442\u0435\u043B\u044C\u043D\u043E\u0441\u0442\u0438 \u0442\u0435\u043C \u0434\u043B\u044F \u043E\u0441\u0432\u043E\u0435\u043D\u0438\u044F \u043A\u0438\u0431\u0435\u0440\u0431\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u043E\u0441\u0442\u0438</p>
        <div class="grid-2">${tracks.map(t => `
            <div class="card" data-track="${t.id}">
                <h3>${t.name}</h3>
                <p>${t.description || ''}</p>
                <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
                    <span style="font-size:0.8rem;"><strong>\u0423\u0440\u043E\u0432\u0435\u043D\u044C:</strong> ${t.level || 'beginner'}</span>
                    <span style="font-size:0.8rem; color:var(--text-secondary);">${t.topics_count || 0} \u0442\u0435\u043C</span>
                    ${t.estimated_hours ? `<span style="font-size:0.8rem; color:var(--text-secondary);">~${t.estimated_hours}\u0447</span>` : ''}
                </div>
                <div style="margin:8px 0;">
                    <div style="display:flex; justify-content:space-between; font-size:0.8rem;">
                        <span>\u041F\u0440\u043E\u0433\u0440\u0435\u0441\u0441</span>
                        <span>${t.progress || 0}%</span>
                    </div>
                    <div style="height:6px; background:var(--bg-secondary); border-radius:3px; overflow:hidden; margin-top:2px;">
                        <div style="height:100%; width:${t.progress || 0}%; background:var(--accent); border-radius:3px; transition:width 0.3s;"></div>
                    </div>
                </div>
                <button data-track="${t.id}" class="start-track">${t.progress > 0 ? '\u25B6 \u041F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u0442\u044C' : '\u041D\u0430\u0447\u0430\u0442\u044C \u0442\u0440\u0435\u043A'}</button>
                <div class="track-detail" style="display:none; margin-top:12px;"></div>
            </div>
        `).join('')}</div>`;
        el.querySelectorAll('.start-track').forEach(btn => {
            btn.onclick = async () => {
                const card = btn.closest('.card');
                const detail = card.querySelector('.track-detail');
                const trackId = btn.dataset.track;
                if (detail.style.display === 'block') {
                    detail.style.display = 'none';
                    return;
                }
                btn.disabled = true;
                btn.textContent = '\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430...';
                await apiCall(`/start_track?track_id=${trackId}`, { method: 'POST' });
                btn.disabled = false;
                const track = (appState.tracks || []).find(t => t.id === trackId);
                if (track && track.topics && track.topics.length) {
                    const topics = track.topics;
                    const progress = track.progress || 0;
                    const total = topics.length;
                    const doneCount = Math.round(progress / 100 * total);
                    detail.style.display = 'block';
                    detail.innerHTML = `
                        <div class="card" style="padding:16px; background:var(--bg-secondary);">
                            <h4 style="margin-bottom:12px;">\uD83D\uDCCB \u0422\u0435\u043C\u044B \u0442\u0440\u0435\u043A\u0430: ${track.name}</h4>
                            ${topics.map((topic, i) => {
                                const completed = i < doneCount;
                                return `<div class="card" style="padding:10px 16px; margin:6px 0; display:flex; align-items:center; gap:12px; ${completed ? 'opacity:0.6;' : ''}">
                                    <span style="font-size:1.2rem;">${completed ? '\u2705' : (i === doneCount ? '\u25B6' : '\uD83D\uDCD6')}</span>
                                    <div style="flex:1;">
                                        <strong>${i+1}. ${topic.title || topic.name || topic.topic_id || ''}</strong>
                                        ${topic.description ? `<div style="font-size:0.85rem;color:var(--text-secondary);">${topic.description}</div>` : ''}
                                    </div>
                                    ${topic.lab_id ? `<span style="font-size:0.8rem;padding:2px 8px;background:var(--accent);border-radius:4px;">\uD83D\uDC33 \u043B\u0430\u0431\u0430</span>` : ''}
                                    ${topic.quiz_topic ? `<span style="font-size:0.8rem;padding:2px 8px;background:var(--bg-secondary);border-radius:4px;">\uD83D\uDCDD \u043A\u0432\u0438\u0437</span>` : ''}
                                </div>`;
                            }).join('')}
                            ${track.prerequisites && track.prerequisites.length ? `<div style="margin-top:12px; padding:8px; background:var(--bg); border-radius:8px;"><strong>\uD83D\uDD12 \u0422\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044F:</strong> ${track.prerequisites.join(', ')}</div>` : ''}
                            <div style="margin-top:12px; text-align:center; color:var(--text-secondary); font-size:0.85rem;">
                                \u041F\u0440\u043E\u0433\u0440\u0435\u0441\u0441: ${doneCount}/${total} \u0442\u0435\u043C (${progress}%)
                            </div>
                        </div>
                    `;
                    btn.textContent = '\u25BC \u0421\u0432\u0435\u0440\u043D\u0443\u0442\u044C';
                    if (window.Sounds) Sounds.success();
                } else {
                    btn.textContent = '\u25B6 \u041F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u0442\u044C';
                }
            };
        });
    }
};
