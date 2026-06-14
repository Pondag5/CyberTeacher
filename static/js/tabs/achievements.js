/* Tab: Achievements */
window.Tab_achievements = {
    async render(el) {
        const ach = await apiCall('/get_achievements_list');
        const earnedCount = (ach.achievements || []).filter(a => a.earned).length;
        el.innerHTML = `<h2>\uD83C\uDFC6 \u0414\u043E\u0441\u0442\u0438\u0436\u0435\u043D\u0438\u044F</h2>
        <div class="card">\u041F\u043E\u043B\u0443\u0447\u0435\u043D\u043E: ${earnedCount} / ${(ach.achievements || []).length}</div>
        <div class="grid-2">${(ach.achievements || []).map(a => `
            <div class="card" style="${a.earned ? 'border-color: var(--accent)' : ''}">${a.earned ? '\u2705 ' : '\uD83D\uDD12 '} ${a.name}<br><small>${a.desc}</small>${a.earned ? ` <span class="badge">+${a.xp || 0} XP</span>` : ''}</div>
        `).join('')}</div>`;
    }
};
