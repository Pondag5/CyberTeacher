/* Tab: Chat (with WebSocket streaming) */
window.Tab_chat = {
    render(el) {
        el.innerHTML = `
            <h2>💬 Чат с CyberTeacher</h2>
            <div class="chat-messages" id="chatMessages"></div>
            <div id="chat-kb-sources" style="font-size:0.75rem;color:var(--text-secondary);margin-bottom:6px;display:none;"></div>
            <div style="display:flex; gap:12px; align-items:center;">
                <div id="personaIndicator" style="display:none; font-size:0.85rem; padding:4px 10px; background:var(--bg-card); border-radius:12px; border:1px solid var(--accent); color:var(--accent);"></div>
                <textarea id="chatInput" rows="2" style="flex:1;" placeholder="Задайте вопрос по кибербезопасности..."></textarea>
                <button id="sendChatBtn">Отправить</button>
            </div>
        `;
        const messagesDiv = document.getElementById('chatMessages');
        const input = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendChatBtn');
        const personaIndicator = document.getElementById('personaIndicator');
        const kbSourcesDiv = document.getElementById('chat-kb-sources');

        function showPersona(persona) {
            if (!persona) return;
            personaIndicator.style.display = 'inline-flex';
            personaIndicator.innerHTML = `<span>${persona.emoji}</span> <strong>${persona.name}</strong> (${persona.id})`;
        }

        function addMessage(role, text, isStreaming) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${role}`;
            const bubble = document.createElement('div');
            bubble.className = 'bubble';
            if (role === 'assistant') {
                if (window.marked) bubble.innerHTML = marked.parse(text);
                else bubble.innerText = text;
                if (isStreaming) bubble.id = 'streamingBubble';
            } else {
                bubble.innerText = text;
            }
            msgDiv.appendChild(bubble);
            messagesDiv.appendChild(msgDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            return bubble;
        }

        async function loadHistory() {
            const hist = await apiCall('/get_history?limit=30');
            if (hist.history) {
                messagesDiv.innerHTML = '';
                hist.history.forEach(msg => addMessage(msg.role, msg.content, false));
            }
        }
        loadHistory();

        function useStreaming() {
            return typeof WebSocket !== 'undefined';
        }

        sendBtn.onclick = async () => {
            const msg = input.value.trim();
            if (!msg) return;
            addMessage('user', msg, false);
            input.value = '';

            if (useStreaming()) {
                const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
                const token = localStorage.getItem('auth_token') || '';
                const wsUrl = `${protocol}//${location.host}/chat_stream?message=${encodeURIComponent(msg)}&mode=${appState.current_mode}&token=${encodeURIComponent(token)}`;
                const ws = new WebSocket(wsUrl);

                let fullText = '';
                const bubble = addMessage('assistant', '', true);

                ws.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        if (data.persona) {
                            showPersona(data.persona);
                        }
                        if (data.chunk) {
                            fullText += data.chunk;
                            if (window.marked) bubble.innerHTML = marked.parse(fullText);
                            else bubble.innerText = fullText;
                            messagesDiv.scrollTop = messagesDiv.scrollHeight;
                        }
                        if (data.done || data.error) {
                            bubble.removeAttribute('id');
                            if (window.marked) bubble.innerHTML = marked.parse(fullText || data.error || 'Empty response');
                        }
                    } catch (e) { /* ignore parse errors */ }
                };
                ws.onerror = () => {
                    bubble.removeAttribute('id');
                    if (!fullText) bubble.innerText = '\u041E\u0448\u0438\u0431\u043A\u0430 \u0441\u043E\u0435\u0434\u0438\u043D\u0438\u0438.';
                };
                ws.onclose = () => { bubble.removeAttribute('id'); };
            } else {
                // Fallback to REST API
                const res = await apiCall(`/chat?message=${encodeURIComponent(msg)}&mode=${appState.current_mode}`, {
                    method: 'POST'
                });
                if (res.persona) showPersona(res.persona);
                if (kbSourcesDiv) {
                    if (res.kb_sources && res.kb_sources.length) {
                        kbSourcesDiv.style.display = 'block';
                        kbSourcesDiv.innerHTML = '📚 Из БЗ: ' + res.kb_sources.map(s => '<span style="color:var(--accent);">' + s + '</span>').join(', ');
                    } else {
                        kbSourcesDiv.style.display = 'none';
                    }
                }
                if (res.response) addMessage('assistant', res.response, false);
                else addMessage('assistant', 'Ошибка связи с ИИ.', false);
            }
        };

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendBtn.click();
            }
        });
    }
};
