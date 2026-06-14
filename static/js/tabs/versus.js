/* Tab: Versus */
window.Tab_versus = {
    render(el) {
        el.innerHTML = `<h2>\uD83E\uDD4A \u0414\u0443\u044D\u043B\u044C (Versus Mode)</h2><div class="card"><select id="versusScenario"><option value="redteam">Red Team vs Blue Team</option></select><button id="startVersus">\u041D\u0430\u0447\u0430\u0442\u044C \u0434\u0443\u044D\u043B\u044C</button><div id="versusChat"></div><input id="versusMsg" placeholder="\u0412\u0430\u0448 \u0445\u043E\u0434..."><button id="versusSend">\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C</button></div>`;
        let active = false;
        document.getElementById('startVersus').onclick = async () => {
            const scenario = document.getElementById('versusScenario').value;
            const res = await apiCall('/start_versus', { method: 'POST', body: JSON.stringify({ scenario }) });
            if (res.status === 'ok') { active = true; document.getElementById('versusChat').innerHTML = `<p>${res.initial_message}</p>`; }
        };
        document.getElementById('versusSend').onclick = async () => {
            if (!active) return;
            const msg = document.getElementById('versusMsg').value;
            const res = await apiCall('/versus_move', { method: 'POST', body: JSON.stringify({ message: msg }) });
            document.getElementById('versusChat').innerHTML += `<p><b>\u0412\u044B:</b> ${msg}</p><p><b>\u0421\u0438\u0441\u0442\u0435\u043C\u0430:</b> ${res.response}</p>`;
            document.getElementById('versusMsg').value = '';
        };
    }
};
