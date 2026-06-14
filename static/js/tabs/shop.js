/* Tab: Shop */
window.Tab_shop = {
    async render(el) {
        const items = appState.shop;
        el.innerHTML = `<h2>\uD83D\uDED2 \u041C\u0430\u0433\u0430\u0437\u0438\u043D</h2>
        ${items.length ? `<p style="color:var(--text-secondary); margin-bottom:12px;">\u041A\u0443\u043F\u0438\u0442\u0435 \u0442\u0435\u043C\u044B, \u043F\u043E\u0434\u0441\u043A\u0430\u0437\u043A\u0438 \u0438 \u0431\u043E\u043D\u0443\u0441\u044B \u0437\u0430 XP</p>
        <div class="grid-2">${items.map(i => `
            <div class="card">
                <h3>${i.name}</h3>
                <p>${i.description}</p>
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:1.2rem;">\uD83D\uDCB0 ${i.price} \u043E\u0447\u043A\u043E\u0432</span>
                    ${i.original_price ? `<span style="font-size:0.8rem; color:var(--text-secondary); text-decoration:line-through;">${i.original_price} \u043E\u0447\u043A\u043E\u0432</span>` : ''}
                </div>
                ${i.type ? `<div style="font-size:0.75rem; color:var(--text-secondary); margin-top:4px;">${i.type}</div>` : ''}
                <button data-item="${i.id}" class="buy-item">\u041A\u0443\u043F\u0438\u0442\u044C</button>
                <div class="purchase-result" style="font-size:0.85rem; margin-top:4px;"></div>
            </div>
        `).join('')}</div>` : '<div class="card"><p style="color:var(--text-secondary);">\u041C\u0430\u0433\u0430\u0437\u0438\u043D \u0432\u0440\u0435\u043C\u0435\u043D\u043D\u043E \u043D\u0435\u0434\u043E\u0441\u0442\u0443\u043F\u0435\u043D. \u041F\u043E\u043F\u0440\u043E\u0431\u0443\u0439\u0442\u0435 \u043F\u043E\u0437\u0436\u0435.</p>'}`;
        el.querySelectorAll('.buy-item').forEach(btn => {
            btn.onclick = async () => {
                btn.disabled = true;
                const res = await apiCall(`/purchase_item?item_id=${btn.dataset.item}`, { method: 'POST' });
                const resultDiv = btn.closest('.card').querySelector('.purchase-result');
                if (res.status === 'ok') {
                    resultDiv.innerHTML = '<span style="color:var(--success);">\u2705 \u041A\u0443\u043F\u043B\u0435\u043D\u043E!</span>';
                    if (window.Sounds) Sounds.success();
                    await loadInitialData();
                } else if (res.detail) {
                    resultDiv.innerHTML = `<span style="color:var(--error);">\u274C ${res.detail}</span>`;
                    if (window.Sounds) Sounds.error();
                }
                btn.disabled = false;
            };
        });
    }
};
