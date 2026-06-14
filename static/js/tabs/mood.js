/* Tab: Mood & Emotions */
window.Tab_mood = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-smile"></i> Mood & Emotions</h2><div class="card"><p class="loading">Loading...</p></div>';
        const [moodRes, emotRes] = await Promise.all([
            apiCall('/api/mood').catch(() => ({ moods: {}, current: 'normal' })),
            apiCall('/api/emotions').catch(() => ({ states: {}, current: {} }))
        ]);
        const moods = moodRes.moods || {};
        const currentMood = moodRes.current || 'normal';
        const states = emotRes.states || {};
        const currentEmotion = emotRes.current || {};

        el.innerHTML = `<h2><i class="fas fa-smile"></i> Mood & Emotions</h2>
            <div class="grid-2">
                <div class="card">
                    <h3><i class="fas fa-theater-masks"></i> Teacher Mood</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:8px;">Current: <strong>${moods[currentMood]?.name || currentMood}</strong> ${moods[currentMood]?.emoji || ''}</p>
                    <div style="display:flex;flex-wrap:wrap;gap:6px;">${Object.entries(moods).map(([key, m]) => `
                        <button class="btn btn-sm set-mood ${key === currentMood ? 'btn-primary' : ''}" data-mood="${key}">${m.emoji} ${m.name}</button>
                    `).join('')}</div>
                </div>
                <div class="card">
                    <h3><i class="fas fa-heart"></i> Student Emotion</h3>
                    <div style="margin-top:8px;font-size:0.85rem;">
                        ${currentEmotion.emotion ? `
                            <div>Detected: <strong>${states[currentEmotion.emotion]?.name || currentEmotion.emotion}</strong> ${states[currentEmotion.emotion]?.emoji || ''}</div>
                            <div style="color:var(--text-secondary);margin-top:4px;">${states[currentEmotion.emotion]?.tone || ''}</div>
                        ` : '<div style="color:var(--text-secondary);">No emotion data yet</div>'}
                    </div>
                    <hr style="border-color:var(--border);margin:12px 0;">
                    <div style="font-size:0.8rem;"><strong>Available states:</strong></div>
                    ${Object.entries(states).map(([key, s]) => `
                        <div style="margin-top:6px;font-size:0.8rem;">${s.emoji} ${s.name} — ${s.tone}</div>
                    `).join('')}
                </div>
            </div>`;

        el.querySelectorAll('.set-mood').forEach(btn => {
            btn.addEventListener('click', async () => {
                const mood = btn.dataset.mood;
                await apiCall(`/api/mood/set?mood=${mood}`, { method: 'POST' });
                this.render(el);
            });
        });
    }
};