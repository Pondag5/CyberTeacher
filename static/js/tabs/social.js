/* Tab: Social Engineering Trainer */
window.Tab_social = {
    async render(el) {
        el.innerHTML = '<h2><i class="fas fa-user-secret"></i> Social Engineering</h2><div class="card"><p class="loading">Loading scenarios...</p></div>';
        const res = await apiCall('/api/social/scenarios').catch(() => ({ scenarios: {} }));
        const scenarios = res.scenarios || {};
        const entries = Object.entries(scenarios);
        if (!entries.length) {
            el.innerHTML = '<h2><i class="fas fa-user-secret"></i> Social Engineering</h2><div class="card"><p style="color:var(--text-secondary);">No scenarios available (LLM required for interaction)</p></div>';
            return;
        }
        el.innerHTML = `<h2><i class="fas fa-user-secret"></i> Social Engineering</h2>
            <p style="color:var(--text-secondary);font-size:0.85rem;margin-bottom:12px;">Choose a scenario to simulate. Uses LLM for victim responses.</p>
            <div class="grid-2">${entries.map(([key, sc]) => `
                <div class="card">
                    <h3 style="color:var(--accent);">${sc.name}</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin:8px 0;">${sc.goal}</p>
                    <button class="btn btn-primary start-social" data-key="${key}">Start scenario</button>
                </div>
            `).join('')}</div>
            <div id="social-session" style="display:none;margin-top:16px;">
                <div class="card">
                    <div style="display:flex;justify-content:space-between;">
                        <h3 id="social-title"></h3>
                        <button id="social-end" class="btn btn-sm" style="color:var(--error);">End session</button>
                    </div>
                    <div id="social-conversation" style="margin-top:12px;max-height:400px;overflow-y:auto;font-size:0.85rem;"></div>
                    <div style="display:flex;gap:8px;margin-top:8px;">
                        <input type="text" id="social-msg" class="input" placeholder="Your message to the victim..." style="flex:1;">
                        <button id="social-send" class="btn btn-primary">Send</button>
                    </div>
                </div>
            </div>`;

        el.querySelectorAll('.start-social').forEach(btn => {
            btn.addEventListener('click', () => {
                const key = btn.dataset.key;
                const sc = scenarios[key];
                const session = el.querySelector('#social-session');
                session.style.display = 'block';
                el.querySelector('#social-title').textContent = `Scenario: ${sc.name} — ${sc.goal}`;
                el.querySelector('#social-conversation').innerHTML = '<p style="color:var(--text-secondary);">Session started. Send your first message.</p>';
                session.dataset.key = key;
                session.dataset.messages = '';
            });
        });

        const sendBtn = el.querySelector('#social-send');
        const msgInput = el.querySelector('#social-msg');
        sendBtn.addEventListener('click', async () => {
            const msg = msgInput.value.trim();
            if (!msg) return;
            const conversation = el.querySelector('#social-conversation');
            conversation.innerHTML += `<div style="color:var(--accent);margin:4px 0;">You: ${msg}</div>`;
            msgInput.value = '';
            conversation.innerHTML += '<p class="loading" style="font-size:0.8rem;">Victim thinking...</p>';
            conversation.scrollTop = conversation.scrollHeight;
        });

        el.querySelector('#social-end').addEventListener('click', () => {
            el.querySelector('#social-session').style.display = 'none';
        });
    }
};