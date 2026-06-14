/* Tab: Scanner */
window.Tab_scanner = {
    render(el) {
        el.innerHTML = `<h2>\uD83D\uDCBB Code Scanner</h2><div class="card"><textarea id="codeInput" rows="8" placeholder="\u0412\u0441\u0442\u0430\u0432\u044C\u0442\u0435 \u043A\u043E\u0434 \u0434\u043B\u044F \u0430\u043D\u0430\u043B\u0438\u0437\u0430..."></textarea><select id="scanLang"><option>python</option><option>javascript</option></select><button id="scanBtn">\u0421\u043A\u0430\u043D\u0438\u0440\u043E\u0432\u0430\u0442\u044C</button><pre id="scanResult"></pre></div>`;
        document.getElementById('scanBtn').onclick = async () => {
            const code = document.getElementById('codeInput').value;
            const lang = document.getElementById('scanLang').value;
            const res = await apiCall('/scan_code', { method: 'POST', body: JSON.stringify({ code, language: lang }) });
            document.getElementById('scanResult').innerText = JSON.stringify(res.results || res, null, 2);
        };
    }
};
