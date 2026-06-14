/* Tab: Daily — with fallback questions */
window.Tab_daily = {
    _fallbackQuestions: [
        { question: '\u041A\u0430\u043A\u043E\u0439 \u043F\u043E\u0440\u0442 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0435\u0442 SSH?', answer: '22' },
        { question: '\u0427\u0442\u043E \u043E\u0437\u043D\u0430\u0447\u0430\u0435\u0442 XSS?', answer: 'cross-site scripting' },
        { question: '\u041A\u0430\u043A\u043E\u0439 \u043F\u043E\u0440\u0442 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0435\u0442 HTTPS?', answer: '443' },
        { question: '\u0427\u0442\u043E \u0442\u0430\u043A\u043E\u0435 SQLi?', answer: 'sql injection' },
        { question: '\u041A\u0430\u043A\u0430\u044F \u043A\u043E\u043C\u0430\u043D\u0434\u0430 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0435\u0442\u0441\u044F \u0434\u043B\u044F \u0441\u043A\u0430\u043D\u0438\u0440\u043E\u0432\u0430\u043D\u0438\u044F \u043F\u043E\u0440\u0442\u043E\u0432?', answer: 'nmap' },
    ],

    async render(el) {
        const daily = appState.daily || {};
        const alreadyDone = daily.completed || daily.status === 'completed';
        const q = daily.question || this._fallbackQuestions[new Date().getDay() % this._fallbackQuestions.length].question;
        el.innerHTML = `
            <h2>\uD83C\uDFAF \u0415\u0436\u0435\u0434\u043D\u0435\u0432\u043D\u044B\u0439 \u0432\u044B\u0437\u043E\u0432</h2>
            <div class="card">
                ${daily.streak > 1 ? `<div style="margin-bottom:8px; color:var(--accent);">\uD83D\uDD25 \u0421\u0442\u0440\u0438\u043A: ${daily.streak} \u0434\u043D\u0435\u0439</div>` : ''}
                <p><strong>${q}</strong></p>
                ${daily.category ? `<div style="font-size:0.8rem; color:var(--text-secondary);">\u041A\u0430\u0442\u0435\u0433\u043E\u0440\u0438\u044F: ${daily.category} | \u0421\u043B\u043E\u0436\u043D\u043E\u0441\u0442\u044C: ${daily.difficulty || 1}</div>` : ''}
                ${alreadyDone ? '<p style="color:var(--success); margin-top:8px;">\u2705 \u0423\u0436\u0435 \u0432\u044B\u043F\u043E\u043B\u043D\u0435\u043D\u043E</p>' : `
                <div style="display:flex; gap:8px; margin-top:12px;">
                    <input id="dailyAnswer" placeholder="\u0412\u0430\u0448 \u043E\u0442\u0432\u0435\u0442" style="flex:1;">
                    <button id="submitDaily">\u041E\u0442\u0432\u0435\u0442\u0438\u0442\u044C</button>
                </div>
                `}
                <div id="dailyResult" style="margin-top:8px;"></div>
            </div>
        `;
        if (!alreadyDone) {
            document.getElementById('submitDaily').onclick = async () => {
                const ans = document.getElementById('dailyAnswer').value;
                if (!ans) return;
                const btn = document.getElementById('submitDaily');
                btn.disabled = true;
                btn.textContent = '\u041F\u0440\u043E\u0432\u0435\u0440\u044F\u044E...';
                const res = await apiCall(`/submit_daily_challenge?answer=${encodeURIComponent(ans)}`, { method: 'POST' });
                const resultDiv = document.getElementById('dailyResult');
                if (res.correct) {
                    resultDiv.innerHTML = `<span style="color:var(--success);">\u2705 \u041F\u0440\u0430\u0432\u0438\u043B\u044C\u043D\u043E! +${res.xp_earned || 50} XP</span>`;
                    appState.xp += res.xp_earned || 50;
                    renderUserInfo();
                    btn.textContent = '\u2705 \u0412\u044B\u043F\u043E\u043B\u043D\u0435\u043D\u043E';
                    if (window.Sounds) Sounds.achievement();
                } else {
                    const correctAns = res.correct_answer || this._fallbackQuestions.find(fq => fq.question === q)?.answer || '';
                    resultDiv.innerHTML = `<span style="color:var(--error);">\u274C \u041D\u0435\u0432\u0435\u0440\u043D\u043E. \u041F\u0440\u0430\u0432\u0438\u043B\u044C\u043D\u044B\u0439 \u043E\u0442\u0432\u0435\u0442: ${correctAns}</span>`;
                    btn.disabled = false;
                    btn.textContent = '\u041E\u0442\u0432\u0435\u0442\u0438\u0442\u044C';
                    if (window.Sounds) Sounds.error();
                }
            };
        }
    }
};
