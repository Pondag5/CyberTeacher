/* Tab: CTF */
window.Tab_ctf = {
    async render(el) {
        const ctf = appState.ctf;
        el.innerHTML = `<h2>\uD83C\uDFF3\uFE0F CTF</h2><div class="card">\u0424\u043B\u0430\u0433\u043E\u0432 \u043D\u0430\u0439\u0434\u0435\u043D\u043E: ${ctf.flags_captured || 0} | \u0423\u0440\u043E\u0432\u0435\u043D\u044C \u0440\u0438\u0441\u043A\u0430: ${ctf.risk_level || 0}<br><input id="flagInput" placeholder="\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0444\u043B\u0430\u0433"><button id="submitFlag">\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C</button></div>`;
        document.getElementById('submitFlag').onclick = async () => {
            const flag = document.getElementById('flagInput').value;
            const res = await apiCall(`/submit_flag?flag_value=${encodeURIComponent(flag)}`, { method: 'POST' });
            alert(res.message);
            if (res.correct) loadInitialData();
        };
    }
};
