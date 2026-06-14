/* Tab: Quiz — now with multiplayer mode + hardcore timer */
window.Tab_quiz = {
    _mpWs: null,
    _mpRoom: null,
    _timer: null,

    render(el) {
        const difficulty = localStorage.getItem('difficulty_level') || 'beginner';
        const isHardcore = difficulty === 'hardcore';

        el.innerHTML = `
            <h2>\uD83D\uDCDD \u041A\u0432\u0438\u0437\u044B</h2>

            <div class="grid-2">
                <div class="card">
                    <h3>\u2705 \u041E\u0434\u0438\u043D\u043E\u0447\u043D\u044B\u0439 \u0440\u0435\u0436\u0438\u043C</h3>
                    <label>\u0422\u0435\u043C\u0430: <input id="quizTopic" value="general" placeholder="web, crypto, networking"></label>
                    <label>\u0412\u043E\u043F\u0440\u043E\u0441\u043E\u0432: <input id="quizCount" type="number" value="5" min="1" max="20"></label>
                    ${isHardcore ? '<div style="color:var(--error); font-size:0.8rem; margin:4px 0;">\u26A0\uFE0F Hardcore: \u0442\u0430\u0439\u043C\u0435\u0440 30 \u0441\u0435\u043A\u0443\u043D\u0434 \u043D\u0430 \u0432\u043E\u043F\u0440\u043E\u0441</div>' : ''}
                    <button id="genQuizBtn">\u0421\u0433\u0435\u043D\u0435\u0440\u0438\u0440\u043E\u0432\u0430\u0442\u044C \u043A\u0432\u0438\u0437</button>
                </div>

                <div class="card">
                    <h3>\uD83E\uDD1D \u041C\u0443\u043B\u044C\u0442\u0438\u043F\u043B\u0435\u0435\u0440</h3>
                    <div id="mpSection">
                        <p style="color:var(--text-secondary); font-size:0.9rem;">\u0418\u0433\u0440\u0430\u0439\u0442\u0435 \u0432\u043C\u0435\u0441\u0442\u0435 \u0441 \u0434\u0440\u0443\u0437\u044C\u044F\u043C\u0438!</p>
                        <input id="mpRoomId" placeholder="\u041A\u043E\u0434 \u043A\u043E\u043C\u043D\u0430\u0442\u044B (4 \u0431\u0443\u043A\u0432\u044B)" maxlength="4" style="text-transform:uppercase; text-align:center; font-size:1.2rem; letter-spacing:4px; width:160px; margin:0 auto; display:block;">
                        <div style="display:flex; gap:8px; justify-content:center; margin-top:12px;">
                            <button id="mpCreateBtn" style="font-size:0.85rem;">\u2795 \u0421\u043E\u0437\u0434\u0430\u0442\u044C</button>
                            <button id="mpJoinBtn" style="font-size:0.85rem;">\u2794 \u0412\u043E\u0439\u0442\u0438</button>
                        </div>
                    </div>
                    <div id="mpGame" style="display:none; margin-top:12px;">
                        <div id="mpStatus" style="color:var(--accent); text-align:center; padding:8px;"></div>
                        <div id="mpPlayers" style="display:flex; gap:6px; justify-content:center; flex-wrap:wrap;"></div>
                        <div id="mpLeaderboard" style="margin-top:12px;"></div>
                        <div id="mpQuestionArea" style="display:none; margin-top:12px;"></div>
                        <div style="display:flex; gap:8px; justify-content:center; margin-top:12px;">
                            <button id="mpStartBtn" style="display:none; font-size:0.85rem;">\u25B6 \u041D\u0430\u0447\u0430\u0442\u044C</button>
                            <button id="mpNextBtn" style="display:none; font-size:0.85rem;">\u25B6\u25B6 \u0421\u043B\u0435\u0434\u0443\u044E\u0449\u0438\u0439</button>
                        </div>
                    </div>
                </div>
            </div>

            <div id="quizContainer"></div>
        `;

        // Single player quiz
        document.getElementById('genQuizBtn').onclick = () => this._generateQuiz(isHardcore);
        // Multiplayer
        document.getElementById('mpCreateBtn').onclick = () => this._mpCreate();
        document.getElementById('mpJoinBtn').onclick = () => this._mpJoin();
        document.getElementById('mpStartBtn').onclick = () => this._mpAction('start', {});
        document.getElementById('mpNextBtn').onclick = () => this._mpAction('next', {});
    },

    async _generateQuiz(isHardcore) {
        const topic = document.getElementById('quizTopic').value;
        const count = parseInt(document.getElementById('quizCount').value);
        const res = await apiCall('/generate_quiz', { method: 'POST', body: JSON.stringify({ topic, count }) });
        if (res.questions) {
            let quizHtml = `<div class="card"><h3>\u041A\u0432\u0438\u0437: ${topic}</h3>`;
            const timerId = isHardcore ? 'quizTimer' : null;

            if (isHardcore) {
                quizHtml += `<div id="quizTimer" style="text-align:center; font-size:1.5rem; font-weight:700; color:var(--error); margin:8px 0;">0:${count * 30}</div>`;
            }

            res.questions.forEach((q, i) => {
                quizHtml += `<div class="quiz-question" data-qidx="${i}"><p><strong>${i+1}. ${q.question}</strong></p>`;
                q.options.forEach((opt, oi) => { quizHtml += `<label><input type="radio" name="q${i}" value="${oi}"> ${opt}</label><br>`; });
                quizHtml += `<div class="quiz-feedback" id="fb${i}"></div></div><hr>`;
            });
            quizHtml += `<button id="submitQuizBtn">\u041F\u0440\u043E\u0432\u0435\u0440\u0438\u0442\u044C \u043E\u0442\u0432\u0435\u0442\u044B</button></div>`;
            document.getElementById('quizContainer').innerHTML = quizHtml;

            // Hardcore timer
            if (isHardcore) {
                let remaining = count * 30;
                this._timer = setInterval(() => {
                    remaining--;
                    const m = Math.floor(remaining / 60);
                    const s = remaining % 60;
                    const el = document.getElementById('quizTimer');
                    if (el) el.textContent = `${m}:${s.toString().padStart(2, '0')}`;
                    if (remaining <= 0) {
                        clearInterval(this._timer);
                        document.getElementById('submitQuizBtn')?.click();
                    }
                }, 1000);
            }

            document.getElementById('submitQuizBtn').onclick = () => {
                if (this._timer) clearInterval(this._timer);
                let score = 0;
                res.questions.forEach((q, i) => {
                    const sel = document.querySelector(`input[name="q${i}"]:checked`);
                    if (sel && parseInt(sel.value) === q.correct) {
                        score++;
                        document.getElementById(`fb${i}`).innerHTML = '<span style="color:var(--success);">\u2713 \u0412\u0435\u0440\u043D\u043E!</span>';
                        if (window.Sounds) Sounds.success();
                    } else {
                        document.getElementById(`fb${i}`).innerHTML = `<span style="color:var(--error);">\u2717 ${q.options[q.correct]}</span>`;
                        if (window.Sounds) Sounds.error();
                    }
                });
                const pct = Math.round(score / res.questions.length * 100);
                alert(`\u0420\u0435\u0437\u0443\u043B\u044C\u0442\u0430\u0442: ${score}/${res.questions.length} (${pct}%)`);
                apiCall('/submit_quiz_result', { method: 'POST', body: JSON.stringify({ topic, score, total: res.questions.length }) });
            };
        }
    },

    _mpCreate() {
        const roomId = document.getElementById('mpRoomId').value.toUpperCase() || Math.random().toString(36).substr(2, 4).toUpperCase();
        const name = prompt('\u0412\u0430\u0448\u0435 \u0438\u043C\u044F \u0434\u043B\u044F \u043A\u043E\u043C\u043D\u0430\u0442\u044B:', 'Host') || 'Host';
        this._mpConnect(roomId, name);
        this._mpRoom = roomId;
        this._mpAction('create', { room: roomId, name });
    },

    _mpJoin() {
        const roomId = document.getElementById('mpRoomId').value.toUpperCase();
        if (!roomId) { alert('\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043A\u043E\u0434'); return; }
        const name = prompt('\u0412\u0430\u0448\u0435 \u0438\u043C\u044F:', 'Player') || 'Player';
        this._mpConnect(roomId, name);
        this._mpRoom = roomId;
        this._mpAction('join', { room: roomId, name });
    },

    _mpConnect(roomId, name) {
        if (this._mpWs) this._mpWs.close();
        const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
        const token = localStorage.getItem('auth_token') || '';
        this._mpWs = new WebSocket(`${protocol}//${location.host}/quiz_multiplayer${token ? '?token=' + token : ''}`);

        this._mpWs.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if (data.type === 'state') this._mpRenderState(data.data);
            if (data.type === 'question') this._mpRenderQuestion(data.data);
            if (data.type === 'leaderboard') this._mpRenderLeaderboard(data.data);
            if (data.type === 'player_joined') {
                document.getElementById('mpStatus').textContent = `${data.name} \u043F\u043E\u0434\u043A\u043B\u044E\u0447\u0438\u043B\u0441\u044F! (\u0412\u0441\u0435\u0433\u043E: ${data.players})`;
                if (window.Sounds) Sounds.notification();
            }
            if (data.type === 'finished') {
                document.getElementById('mpStatus').innerHTML = '<strong style="color:var(--success);">\u041A\u0432\u0438\u0437 \u0437\u0430\u0432\u0435\u0440\u0448\u0451\u043D!</strong>';
                this._mpRenderLeaderboard(data.leaderboard);
            }
            if (data.type === 'answer_result') {
                const r = data.data;
                const fb = document.getElementById('mpAnswerFeedback');
                if (fb) {
                    fb.innerHTML = r.correct
                        ? '<span style="color:var(--success);">\u2713 \u0412\u0435\u0440\u043D\u043E!</span>'
                        : `<span style="color:var(--error);">\u2717 \u041D\u0435\u0432\u0435\u0440\u043D\u043E. \u041F\u0440\u0430\u0432\u0438\u043B\u044C\u043D\u043E: ${r.options[r.correct_answer]}</span>`;
                    if (window.Sounds) r.correct ? Sounds.success() : Sounds.error();
                }
            }
            if (data.type === 'error') {
                document.getElementById('mpStatus').innerHTML = `<span style="color:var(--error);">\u2717 ${data.message}</span>`;
            }
        };

        this._mpWs.onopen = () => {
            document.getElementById('mpGame').style.display = 'block';
            document.getElementById('mpStatus').textContent = `\u041F\u043E\u0434\u043A\u043B\u044E\u0447\u0435\u043D\u043E \u043A \u043A\u043E\u043C\u043D\u0430\u0442\u0435 ${roomId}...`;
            if (window.Sounds) Sounds.click();
        };
    },

    _mpAction(action, extra) {
        if (this._mpWs && this._mpWs.readyState === WebSocket.OPEN) {
            this._mpWs.send(JSON.stringify({ action, ...extra }));
        }
    },

    _mpRenderState(state) {
        if (!state) return;
        document.getElementById('mpStatus').textContent = `\u041A\u043E\u043C\u043D\u0430\u0442\u0430: ${state.room_id} | \u0418\u0433\u0440\u043E\u043A\u043E\u0432: ${state.players} | \u0412\u043E\u043F\u0440\u043E\u0441\u043E\u0432: ${state.current_question + 1}/${state.total_questions}`;
        document.getElementById('mpStartBtn').style.display = state.host === localStorage.getItem('username') && !state.started ? 'inline-block' : 'none';
        document.getElementById('mpNextBtn').style.display = state.started && state.host === localStorage.getItem('username') ? 'inline-block' : 'none';
    },

    _mpRenderQuestion(q) {
        if (!q) return;
        const area = document.getElementById('mpQuestionArea');
        area.style.display = 'block';
        let html = `<p style="font-size:1.1rem; font-weight:600;">${q.question}</p>`;
        q.options.forEach((opt, i) => {
            html += `<button class="mp-answer-btn" data-idx="${i}" style="display:block; width:100%; text-align:left; margin:4px 0;">${opt}</button>`;
        });
        html += '<div id="mpAnswerFeedback" style="text-align:center; margin-top:8px;"></div>';
        area.innerHTML = html;
        area.querySelectorAll('.mp-answer-btn').forEach(btn => {
            btn.onclick = () => {
                this._mpAction('answer', { answer: parseInt(btn.dataset.idx) });
                area.querySelectorAll('.mp-answer-btn').forEach(b => b.disabled = true);
            };
        });
        if (window.Sounds) Sounds.click();
    },

    _mpRenderLeaderboard(board) {
        if (!board) return;
        const el = document.getElementById('mpLeaderboard');
        el.innerHTML = '<h4>\uD83D\uDCCA \u0422\u0430\u0431\u043B\u0438\u0446\u0430 \u043B\u0438\u0434\u0435\u0440\u043E\u0432:</h4>' +
            board.map((p, i) => `<div style="padding:4px 0; border-bottom:1px solid var(--border);">${i === 0 ? '\uD83E\uDD47' : i === 1 ? '\uD83E\uDD48' : i === 2 ? '\uD83E\uDD49' : '  '} ${p.name}: <strong>${p.score}</strong> \u2022 streak: ${p.streak}</div>`).join('');
    }
};
