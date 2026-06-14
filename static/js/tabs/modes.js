/* Tab: Modes */
window.Tab_modes = {
    async render(el) {
        const modes = appState.modes;
        el.innerHTML = `
            <h2>\uD83C\uDFAD \u0420\u0435\u0436\u0438\u043C\u044B \u043E\u0431\u0443\u0447\u0435\u043D\u0438\u044F</h2>
            <div class="grid-2">
                ${modes.map(m => `
                    <div class="card" data-mode="${m.id}">
                        <div style="font-size:2rem;">${m.icon || '\uD83E\uDD16'}</div>
                        <h3>${m.name}</h3>
                        <p>${m.desc || ''}</p>
                        <button class="set-mode-btn" data-mode="${m.id}">${m.active ? '\u2705 \u0410\u043A\u0442\u0438\u0432\u0435\u043D' : '\u0412\u044B\u0431\u0440\u0430\u0442\u044C'}</button>
                    </div>
                `).join('')}
            </div>
        `;
        el.querySelectorAll('.set-mode-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const res = await apiCall(`/set_mode?mode_id=${btn.dataset.mode}`, { method: 'POST' });
                if (!res.error) { appState.current_mode = btn.dataset.mode; this.render(el); }
            });
        });
    }
};
