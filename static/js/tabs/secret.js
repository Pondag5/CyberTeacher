/* Tab: Secret Room — Тайная комната */
window.Tab_secret = {
    async render(el) {
        const status = await apiCall('/api/secret').catch(() => ({ unlocked: false, visited: false, remaining: 0, has_artifact: false, can_unlock: false }));

        const remaining = status.remaining || 0;
        const hours = Math.floor(remaining / 3600);
        const mins = Math.floor((remaining % 3600) / 60);

        if (status.unlocked) {
            el.innerHTML = `
                <h2><i class="fas fa-door-open"></i> Тайная комната</h2>
                <div class="card" style="border-left:3px solid var(--accent);">
                    <h3>\u2705 Комната открыта</h3>
                    <p style="color:var(--text-secondary);font-size:0.9rem;">
                        Ты нашёл тайную комнату учителя. Здесь хранятся его воспоминания и фрагменты правды.
                    </p>
                    <div style="margin-top:12px;">
                        <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:4px;">
                            <span>Осталось времени:</span>
                            <span><strong>${hours}ч ${mins}мин</strong></span>
                        </div>
                        <div style="height:8px;background:var(--bg-secondary);border-radius:4px;overflow:hidden;">
                            <div id="secret-timer-bar" style="width:100%;height:100%;background:var(--accent);border-radius:4px;transition:width 0.5s;"></div>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-top:8px;">
                            <span>Посещена:</span>
                            <span style="color:${status.visited ? 'var(--success)' : 'var(--warning)'};">${status.visited ? 'Да' : 'Нет'}</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                            <span>Артефакт получен:</span>
                            <span style="color:${status.has_artifact ? 'var(--success)' : 'var(--warning)'};">${status.has_artifact ? 'Да' : 'Нет'}</span>
                        </div>
                    </div>
                    ${!status.visited
                        ? `<button id="secret-enter-btn" class="btn btn-primary" style="margin-top:12px;">\uD83D\uDCAB Войти в комнату</button>`
                        : `<p style="color:var(--text-secondary);font-size:0.85rem;margin-top:12px;">Ты уже был здесь. Комната исчезнет через ${hours}ч ${mins}мин.</p>`}
                </div>
            `;

            el.querySelector('#secret-enter-btn')?.addEventListener('click', async () => {
                const result = await apiCall('/api/secret/enter', { method: 'POST' });
                if (result.visited) {
                    this.render(el);
                } else {
                    el.querySelector('#secret-enter-btn')?.insertAdjacentHTML('afterend',
                        `<p style="color:var(--error);margin-top:8px;">${result.message}</p>`);
                }
            });
        } else if (status.can_unlock) {
            el.innerHTML = `
                <h2><i class="fas fa-door-open"></i> Тайная комната</h2>
                <div class="card">
                    <h3>\u2753 Комната скоро появится</h3>
                    <p style="color:var(--text-secondary);font-size:0.9rem;">
                        Все условия выполнены. Тайная комната откроется в ближайшее время.
                    </p>
                    <p style="color:var(--text-secondary);font-size:0.85rem;margin-top:8px;">
                        Проверь эту вкладку позже — комната доступна только на 24 часа после появления.
                    </p>
                </div>
            `;
        } else {
            el.innerHTML = `
                <h2><i class="fas fa-door-open"></i> Тайная комната</h2>
                <div class="card">
                    <h3>\u274C Комната заперта</h3>
                    <p style="color:var(--text-secondary);font-size:0.9rem;">
                        Чтобы открыть тайную комнату, нужно:
                    </p>
                    <ul style="margin-top:8px;font-size:0.85rem;color:var(--text-secondary);">
                        <li>\u2713 Пройти все 8 глав сюжета</li>
                        <li>\u2713 Выбрать фракцию</li>
                        <li>\u2713 Встретиться с Watchers</li>
                    </ul>
                    <p style="color:var(--text-secondary);font-size:0.85rem;margin-top:12px;">
                        После выполнения условий комната появится на 24 часа.
                    </p>
                </div>
            `;
        }
    }
};
