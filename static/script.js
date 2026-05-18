// Конфигурация
const CONFIG = {
    API_BASE_URL: localStorage.getItem('ct_api_url') || 'http://localhost:8000'
};

// Состояние приложения
const state = {
    currentTab: 'tab-chat',
    chatHistory: [],
    quiz: {
        questions: [],
        currentIndex: 0,
        score: 0,
        topic: 'general'
    }
};

// DOM Элементы
const elements = {
    status: document.getElementById('status'),
    xpVal: document.getElementById('xp-val'),
    levelVal: document.getElementById('level-val'),
    streakVal: document.getElementById('streak-val'),
    xpBarFill: document.getElementById('xp-bar-fill'),
    xpBarText: document.getElementById('xp-bar-text'),
    skillsList: document.getElementById('skills-list'),
    chatMessages: document.getElementById('chat-messages'),
    chatInput: document.getElementById('chat-input'),
    chatSendBtn: document.getElementById('chat-send-btn'),
    startQuizBtn: document.getElementById('start-quiz-btn'),
    quizTopic: document.getElementById('quiz-topic'),
    quizArea: document.getElementById('quiz-area'),
    quizCounter: document.getElementById('quiz-counter'),
    quizScoreDisplay: document.getElementById('quiz-score-display'),
    questionText: document.getElementById('question-text'),
    optionsContainer: document.getElementById('options-container'),
    resultContainer: document.getElementById('result-container'),
    resultText: document.getElementById('result-text'),
    resultExplanation: document.getElementById('result-explanation'),
    nextQuestionBtn: document.getElementById('next-question-btn'),
    serverUrlInput: document.getElementById('server-url'),
    saveSettingsBtn: document.getElementById('save-settings'),
    coursesList: document.getElementById('courses-list'),
    labsList: document.getElementById('labs-list'),
    achievementsList: document.getElementById('achievements-list'),
    achievementsCount: document.getElementById('achievements-count'),
    statsContent: document.getElementById('stats-content'),
    themeSelect: document.getElementById('theme-select'),
    enableNotifBtn: document.getElementById('enable-notifications'),
    notifStatus: document.getElementById('notif-status'),
    versusScenarios: document.getElementById('versus-scenarios'),
    versusMenu: document.getElementById('versus-menu'),
    versusGame: document.getElementById('versus-game'),
    versusScenarioName: document.getElementById('versus-scenario-name'),
    versusAttempts: document.getElementById('versus-attempts'),
    versusMessages: document.getElementById('versus-messages'),
    versusInput: document.getElementById('versus-input'),
    versusSendBtn: document.getElementById('versus-send-btn'),
    versusExitBtn: document.getElementById('versus-exit-btn'),
    toggleOfflineBtn: document.getElementById('toggle-offline'),
    offlineStatus: document.getElementById('offline-status')
};

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initSettings();
    initTheme();
    initNotifications();
    initOfflineMode();
    initChat();
    initQuiz();
    checkConnection();
    loadProgress();
    loadCourses();
    loadLabs();
    loadAchievements();
    loadStats();
    loadVersusScenarios();
    checkVersusStatus();
    registerSW();
});

// Service Worker
function registerSW() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('SW registered'))
            .catch(err => console.log('SW registration failed', err));
    }
}

// Вкладки
function initTabs() {
    const navBtns = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;
            navBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            tabContents.forEach(tc => tc.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            if (tabId === 'tab-progress') loadProgress();
            if (tabId === 'tab-modes') loadModes();
            if (tabId === 'tab-courses') loadCourses();
            if (tabId === 'tab-labs') loadLabs();
            if (tabId === 'tab-achievements') loadAchievements();
            if (tabId === 'tab-stats') loadStats();
            if (tabId === 'tab-versus') checkVersusStatus();
            if (tabId === 'tab-daily') loadDailyChallenge();
            if (tabId === 'tab-profile') loadProfile();
            if (tabId === 'tab-story') loadStoryEpisodes();
            if (tabId === 'tab-tracks') loadTracks();
            if (tabId === 'tab-ctf') loadCTFStatus();
            if (tabId === 'tab-osint') loadThreats();
            if (tabId === 'tab-scanner') {}
            if (tabId === 'tab-shop') loadShop();
            if (tabId === 'tab-malware') {}
        });
    });
}

// Настройки
function initSettings() {
    elements.serverUrlInput.value = CONFIG.API_BASE_URL;
    elements.saveSettingsBtn.addEventListener('click', () => {
        const newUrl = elements.serverUrlInput.value.replace(/\/$/, '');
        localStorage.setItem('ct_api_url', newUrl);
        CONFIG.API_BASE_URL = newUrl;
        alert('Настройки сохранены!');
        checkConnection();
        loadProgress();
    });
}

// Тема
function initTheme() {
    const savedTheme = localStorage.getItem('ct_theme') || 'ocean';
    applyTheme(savedTheme);
    elements.themeSelect.value = savedTheme;
    
    elements.themeSelect.addEventListener('change', () => {
        applyTheme(elements.themeSelect.value);
    });
}

function applyTheme(theme) {
    document.body.className = document.body.className.replace(/theme-\w+/g, '').trim();
    if (theme && theme !== 'ocean') {
        document.body.classList.add(`theme-${theme}`);
    }
    localStorage.setItem('ct_theme', theme);
    
    const themeColors = {
        ocean: '#1e1e2e',
        sunset: '#1e1e2e',
        matrix: '#0a0a0a'
    };
    document.querySelector('meta[name="theme-color"]').content = themeColors[theme] || '#1e1e2e';
}

// Уведомления
function initNotifications() {
    elements.enableNotifBtn.addEventListener('click', requestNotifications);
    updateNotifStatus();
}

function updateNotifStatus() {
    if (!('Notification' in window)) {
        elements.notifStatus.textContent = 'Уведомления не поддерживаются';
        elements.enableNotifBtn.disabled = true;
        return;
    }
    
    if (Notification.permission === 'granted') {
        elements.notifStatus.textContent = '✅ Уведомления включены';
        elements.enableNotifBtn.textContent = 'Включены';
        elements.enableNotifBtn.disabled = true;
    } else if (Notification.permission === 'denied') {
        elements.notifStatus.textContent = '❌ Уведомления заблокированы';
        elements.enableNotifBtn.disabled = true;
    } else {
        elements.notifStatus.textContent = 'Уведомления отключены';
    }
}

async function requestNotifications() {
    if (!('Notification' in window)) return;
    
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
        new Notification('CyberTeacher', {
            body: 'Уведомления включены! Вы будете получать напоминания о челленджах.',
            icon: '/icon-192.png'
        });
    }
    updateNotifStatus();
}

// Офлайн-режим
function initOfflineMode() {
    if (!elements.toggleOfflineBtn || !elements.offlineStatus) return;

    elements.toggleOfflineBtn.addEventListener('click', async () => {
        try {
            const res = await fetch(`${CONFIG.API_BASE_URL}/api/offline`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'toggle' })
            });
            const data = await res.json();
            updateOfflineUI(data.offline_mode);
        } catch (err) {
            console.error('Offline toggle error:', err);
        }
    });

    loadOfflineStatus();
}

async function loadOfflineStatus() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/offline`);
        const data = await res.json();
        updateOfflineUI(data.offline_mode);
    } catch (err) {
        console.error('Offline status load error:', err);
    }
}

function updateOfflineUI(isOffline) {
    if (isOffline) {
        elements.offlineStatus.textContent = 'Офлайн-режим (без LLM)';
        elements.offlineStatus.style.color = '#f59e0b';
        elements.toggleOfflineBtn.textContent = 'Выключить';
    } else {
        elements.offlineStatus.textContent = 'Онлайн-режим';
        elements.offlineStatus.style.color = '#10b981';
        elements.toggleOfflineBtn.textContent = 'Включить';
    }
}

// Проверка соединения
async function checkConnection() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/health`);
        if (res.ok) {
            elements.status.innerHTML = '<span class="dot online"></span> Online';
        } else {
            throw new Error('Not OK');
        }
    } catch (e) {
        elements.status.innerHTML = '<span class="dot offline"></span> Offline';
    }
}

// Загрузка прогресса
async function loadProgress() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/progress`);
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        elements.xpVal.textContent = data.xp || 0;
        elements.levelVal.textContent = data.level || 1;
        elements.streakVal.textContent = data.streak || 0;
        
        // XP бар
        const xpNeeded = data.level * 100;
        const xpInLevel = (data.xp || 0) % xpNeeded;
        const progress = (xpInLevel / xpNeeded) * 100;
        elements.xpBarFill.style.width = `${progress}%`;
        elements.xpBarText.textContent = `${xpInLevel} / ${xpNeeded} XP`;
        
        elements.skillsList.innerHTML = '<p class="placeholder">Нет данных о навыках</p>';
    } catch (e) {
        elements.skillsList.innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

// Загрузка курсов
async function loadCourses() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/courses`);
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        renderCourses(data.courses || []);
    } catch (e) {
        elements.coursesList.innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

function renderCourses(courses) {
    if (courses.length === 0) {
        elements.coursesList.innerHTML = '<p class="placeholder">Нет доступных курсов</p>';
        return;
    }
    elements.coursesList.innerHTML = courses.map(c => `
        <div class="course-item ${c.active ? 'active' : ''}" onclick="selectCourse('${c.id}')">
            <div class="course-title">${c.icon || '📖'} ${c.name}</div>
            <div class="course-desc">${c.description || ''}</div>
            <div class="course-meta">
                <span>📄 ${c.topics_count || 0} тем</span>
                <span>⏱️ ${c.duration || '?'}</span>
            </div>
            <div class="course-progress-bar">
                <div class="course-progress-fill" style="width: ${c.progress || 0}%"></div>
            </div>
        </div>
    `).join('');
}

function selectCourse(courseId) {
    fetch(`${CONFIG.API_BASE_URL}/api/courses/${courseId}/select`, { method: 'POST' })
        .then(() => loadCourses());
}

// Загрузка лабораторий
async function loadLabs() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/labs`);
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        renderLabs(data.labs || []);
        // Проверяем статус Docker
        checkDockerStatus();
    } catch (e) {
        elements.labsList.innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

async function checkDockerStatus() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/docker/status`);
        if (!res.ok) return;
        const data = await res.json();
        const statusEl = document.getElementById('docker-status');
        if (statusEl) {
            statusEl.textContent = data.available ? '🟢 Docker доступен' : '🔴 Docker недоступен';
            statusEl.className = data.available ? 'docker-status available' : 'docker-status unavailable';
        }
    } catch (e) {
        // Docker status check failed silently
    }
}

function renderLabs(labs) {
    if (labs.length === 0) {
        elements.labsList.innerHTML = '<p class="placeholder">Нет доступных лабораторий</p>';
        return;
    }
    elements.labsList.innerHTML = `
        <div id="docker-status" class="docker-status">Проверка Docker...</div>
    ` + labs.map(lab => `
        <div class="lab-item ${lab.running ? 'running' : ''}" id="lab-${lab.id}">
            <div class="lab-header">
                <span class="lab-title">${lab.name}</span>
                <span class="lab-status ${lab.running ? 'running' : ''}">${lab.running ? '● Запущена' : '○ Остановлена'}</span>
            </div>
            <div class="lab-desc">${lab.description}</div>
            <div class="lab-tags">
                ${lab.tags.map(t => `<span class="lab-tag">${t}</span>`).join('')}
            </div>
            <div class="lab-actions">
                ${lab.running 
                    ? `<button class="lab-btn stop" onclick="stopLab('${lab.id}')">⏹ Остановить</button>`
                    : `<button class="lab-btn start" onclick="startLab('${lab.id}')">▶ Запустить</button>`
                }
            </div>
            ${lab.running && lab.ports ? `
                <div class="lab-ports">
                    Доступ: ${lab.ports.map(p => `<a href="${p}" target="_blank">${p}</a>`).join(', ')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

async function startLab(labId) {
    try {
        // Пробуем реальный Docker сначала
        let res = await fetch(`${CONFIG.API_BASE_URL}/api/docker/${labId}/start`, { method: 'POST' });
        if (!res.ok) {
            // Fallback на симуляцию
            res = await fetch(`${CONFIG.API_BASE_URL}/api/labs/${labId}/start`, { method: 'POST' });
        }
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        if (data.ports && data.ports.length > 0) {
            alert(`Лаборатория запущена!\n${data.ports.join('\n')}`);
        }
        loadLabs();
    } catch (e) {
        alert('Ошибка запуска лаборатории');
    }
}

async function stopLab(labId) {
    try {
        // Пробуем реальный Docker сначала
        let res = await fetch(`${CONFIG.API_BASE_URL}/api/docker/${labId}/stop`, { method: 'POST' });
        if (!res.ok) {
            // Fallback на симуляцию
            res = await fetch(`${CONFIG.API_BASE_URL}/api/labs/${labId}/stop`, { method: 'POST' });
        }
        if (!res.ok) throw new Error('Failed');
        loadLabs();
    } catch (e) {
        alert('Ошибка остановки лаборатории');
    }
}

// Загрузка достижений
async function loadAchievements() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/achievements`);
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        renderAchievements(data.achievements || [], data.total || 0);
    } catch (e) {
        elements.achievementsList.innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

function renderAchievements(achievements, total) {
    elements.achievementsCount.textContent = `${total} / ${achievements.length}`;
    
    if (achievements.length === 0) {
        elements.achievementsList.innerHTML = '<p class="placeholder">Нет достижений</p>';
        return;
    }
    elements.achievementsList.innerHTML = achievements.map(a => `
        <div class="achievement-item ${a.earned ? 'earned' : 'locked'}">
            <div class="achievement-icon">${a.icon}</div>
            <div class="achievement-name">${a.name}</div>
            <div class="achievement-desc">${a.desc}</div>
            ${a.xp ? `<div class="achievement-xp">+${a.xp} XP</div>` : ''}
        </div>
    `).join('');
}

// Загрузка статистики
async function loadStats() {
    try {
        elements.statsContent.innerHTML = '<p class="placeholder">Загрузка...</p>';
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/stats`);
        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`HTTP ${res.status}: ${errorText}`);
        }
        const data = await res.json();
        renderStats(data);
    } catch (e) {
        console.error('Stats load error:', e);
        elements.statsContent.innerHTML = `<p class="placeholder" style="color:var(--danger)">Ошибка: ${e.message}</p>`;
    }
}

function renderStats(data) {
    const activity = data.activity || [];
    const skills = data.skills || [];
    const weakTopics = data.weak_topics || [];
    const maxActivity = Math.max(...activity.map(a => a.value || 0), 1);
    
    elements.statsContent.innerHTML = `
        <div class="stats-summary">
            <div class="stat-card">
                <div class="stat-card-value">${data.total_quizzes || 0}</div>
                <div class="stat-card-label">Квизов пройдено</div>
            </div>
            <div class="stat-card">
                <div class="stat-card-value">${data.total_tasks || 0}</div>
                <div class="stat-card-label">Заданий выполнено</div>
            </div>
            <div class="stat-card">
                <div class="stat-card-value">${data.streak || 0}</div>
                <div class="stat-card-label">Дней стрик 🔥</div>
            </div>
            <div class="stat-card">
                <div class="stat-card-value">${data.level || 1}</div>
                <div class="stat-card-label">Уровень</div>
            </div>
        </div>
        
        ${activity.length > 0 ? `
            <h3>Активность за неделю</h3>
            <div class="stats-activity">
                ${activity.map(a => `
                    <div class="activity-bar">
                        <div class="activity-bar-fill" style="height: ${((a.value || 0) / maxActivity) * 100}px"></div>
                        <span class="activity-bar-label">${a.day || ''}</span>
                    </div>
                `).join('')}
            </div>
        ` : ''}
        
        ${skills.length > 0 ? `
            <h3>Навыки</h3>
            <div class="skills-list">
                ${skills.map(s => `
                    <div class="skill-bar">
                        <div class="skill-header">
                            <span>${s.name || 'Unknown'}</span>
                            <span>${s.level || 0}%</span>
                        </div>
                        <div class="skill-track">
                            <div class="skill-fill" style="width: ${s.level || 0}%"></div>
                        </div>
                    </div>
                `).join('')}
            </div>
        ` : ''}
        
        ${weakTopics.length > 0 ? `
            <div class="stats-weak-topics">
                <h3>Слабые темы</h3>
                ${weakTopics.map(t => `
                    <div class="weak-topic-item">
                        <span class="weak-topic-name">⚠️ ${t}</span>
                    </div>
                `).join('')}
            </div>
        ` : '<p class="placeholder">Нет слабых тем 🎉</p>'}
    `;
}

// ==================== ЧАТ ====================

function initChat() {
    elements.chatSendBtn.addEventListener('click', sendChatMessage);
    elements.chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });
}

function addMessage(role, content) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerHTML = `<div class="message-content">${escapeHtml(content)}</div>`;
    elements.chatMessages.appendChild(div);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function showTyping() {
    const div = document.createElement('div');
    div.className = 'message assistant';
    div.id = 'typing-indicator';
    div.innerHTML = `<div class="message-content"><div class="typing-indicator"><span></span><span></span><span></span></div></div>`;
    elements.chatMessages.appendChild(div);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function sendChatMessage() {
    const text = elements.chatInput.value.trim();
    if (!text) return;

    elements.chatInput.value = '';
    elements.chatSendBtn.disabled = true;
    addMessage('user', text);
    showTyping();

    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, history: state.chatHistory })
        });

        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        hideTyping();
        addMessage('assistant', data.response || 'Нет ответа');
        state.chatHistory = data.history || [];
    } catch (e) {
        hideTyping();
        addMessage('system', 'Ошибка соединения с сервером');
    }

    elements.chatSendBtn.disabled = false;
    elements.chatInput.focus();
}

// ==================== КВИЗ ====================

function initQuiz() {
    elements.startQuizBtn.addEventListener('click', startQuiz);
    elements.nextQuestionBtn.addEventListener('click', nextQuestion);
}

async function startQuiz() {
    state.quiz.topic = elements.quizTopic.value;
    state.quiz.currentIndex = 0;
    state.quiz.score = 0;

    elements.startQuizBtn.classList.add('hidden');
    elements.quizTopic.classList.add('hidden');
    elements.quizArea.classList.remove('hidden');

    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/quiz/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: state.quiz.topic, count: 5 })
        });

        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        state.quiz.questions = data.questions || [];
        if (state.quiz.questions.length === 0) throw new Error('No questions');
        showQuestion();
    } catch (e) {
        elements.quizArea.classList.add('hidden');
        elements.startQuizBtn.classList.remove('hidden');
        elements.startQuizBtn.textContent = 'Ошибка генерации. Попробовать снова?';
    }
}

function showQuestion() {
    const q = state.quiz.questions[state.quiz.currentIndex];
    elements.questionText.textContent = q.question;
    elements.optionsContainer.innerHTML = '';
    elements.resultContainer.classList.add('hidden');
    elements.quizCounter.textContent = `${state.quiz.currentIndex + 1}/${state.quiz.questions.length}`;
    elements.quizScoreDisplay.textContent = `Счёт: ${state.quiz.score}`;

    q.options.forEach((opt, idx) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = opt;
        btn.onclick = () => handleAnswer(idx, q.correct, btn, q.explanation);
        elements.optionsContainer.appendChild(btn);
    });
}

function handleAnswer(selected, correct, btn, explanation) {
    const allBtns = elements.optionsContainer.querySelectorAll('.option-btn');
    allBtns.forEach(b => b.disabled = true);

    if (selected === correct) {
        btn.classList.add('correct');
        state.quiz.score++;
        elements.resultText.textContent = "✅ Верно!";
        elements.resultText.style.color = "var(--accent)";
    } else {
        btn.classList.add('wrong');
        allBtns[correct].classList.add('correct');
        elements.resultText.textContent = "❌ Неверно!";
        elements.resultText.style.color = "var(--danger)";
    }

    elements.resultExplanation.textContent = explanation || '';
    elements.resultContainer.classList.remove('hidden');
    elements.quizScoreDisplay.textContent = `Счёт: ${state.quiz.score}`;
}

function nextQuestion() {
    state.quiz.currentIndex++;
    if (state.quiz.currentIndex < state.quiz.questions.length) {
        showQuestion();
    } else {
        finishQuiz();
    }
}

async function finishQuiz() {
    elements.quizArea.classList.add('hidden');
    elements.startQuizBtn.classList.remove('hidden');
    elements.quizTopic.classList.remove('hidden');
    elements.startQuizBtn.textContent = `Результат: ${state.quiz.score}/${state.quiz.questions.length}. Повторить?`;

    try {
        await fetch(`${CONFIG.API_BASE_URL}/api/quiz/result`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: state.quiz.topic,
                score: state.quiz.score,
                total: state.quiz.questions.length
            })
        });
    } catch (e) {
        console.error('Failed to submit quiz result:', e);
    }
}

// ==================== ДУЭЛЬ (VERSUS) ====================

function initVersus() {
    elements.versusSendBtn.addEventListener('click', sendVersusMove);
    elements.versusInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendVersusMove();
    });
    elements.versusExitBtn.addEventListener('click', stopVersus);
}

async function loadVersusScenarios() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/versus/scenarios`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        renderVersusScenarios(data.scenarios || []);
    } catch (e) {
        elements.versusScenarios.innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка</p>';
    }
}

function renderVersusScenarios(scenarios) {
    if (scenarios.length === 0) {
        elements.versusScenarios.innerHTML = '<p class="placeholder">Нет сценариев</p>';
        return;
    }
    elements.versusScenarios.innerHTML = scenarios.map(s => `
        <div class="versus-scenario-card" onclick="startVersus('${s.id}')">
            <div class="versus-scenario-name">${s.name}</div>
            <div class="versus-scenario-desc">${s.description}</div>
        </div>
    `).join('');
}

async function checkVersusStatus() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/versus/status`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        
        if (data.active) {
            showVersusGame(data);
        } else {
            showVersusMenu();
        }
    } catch (e) {
        showVersusMenu();
    }
}

function showVersusMenu() {
    elements.versusMenu.classList.remove('hidden');
    elements.versusGame.classList.add('hidden');
}

function showVersusGame(data) {
    elements.versusMenu.classList.add('hidden');
    elements.versusGame.classList.remove('hidden');
    elements.versusScenarioName.textContent = data.name || data.scenario;
    elements.versusAttempts.textContent = `Попыток: ${data.attempts || 0}`;
    elements.versusMessages.innerHTML = '';
}

async function startVersus(scenarioId) {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/versus/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scenario: scenarioId })
        });
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        
        showVersusGame(data);
        addVersusMessage('system', data.initial_message);
    } catch (e) {
        alert('Ошибка запуска дуэли');
    }
}

async function sendVersusMove() {
    const text = elements.versusInput.value.trim();
    if (!text) return;
    
    elements.versusInput.value = '';
    elements.versusSendBtn.disabled = true;
    
    addVersusMessage('user', text);
    
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/versus/move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        
        addVersusMessage('system', data.response);
        elements.versusAttempts.textContent = `Попыток: ${data.attempts}`;
    } catch (e) {
        addVersusMessage('system', '❌ Ошибка соединения');
    }
    
    elements.versusSendBtn.disabled = false;
    elements.versusInput.focus();
}

function addVersusMessage(role, content) {
    const div = document.createElement('div');
    div.className = `versus-message ${role}`;
    div.textContent = content;
    elements.versusMessages.appendChild(div);
    elements.versusMessages.scrollTop = elements.versusMessages.scrollHeight;
}

async function stopVersus() {
    try {
        await fetch(`${CONFIG.API_BASE_URL}/api/versus/stop`, { method: 'POST' });
        showVersusMenu();
    } catch (e) {
        alert('Ошибка завершения дуэли');
    }
}

// Инициализация дуэли при загрузке
document.addEventListener('DOMContentLoaded', () => {
    initVersus();
});

// ==================== РЕЖИМЫ ====================

async function loadModes() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/modes`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        renderModes(data.modes || []);
    } catch (e) {
        document.getElementById('modes-list').innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

function renderModes(modes) {
    const container = document.getElementById('modes-list');
    container.innerHTML = modes.map(m => `
        <div class="mode-item ${m.active ? 'active' : ''}" onclick="setMode('${m.id}')">
            <div class="mode-icon">${m.icon}</div>
            <div class="mode-info">
                <div class="mode-name">${m.name}</div>
                <div class="mode-desc">${m.desc}</div>
            </div>
            <div class="mode-status">${m.active ? '✅' : ''}</div>
        </div>
    `).join('');
}

async function setMode(modeId) {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/mode/set?mode_id=${modeId}`, { method: 'POST' });
        if (!res.ok) throw new Error('Failed');
        loadModes();
    } catch (e) {
        alert('Ошибка переключения режима');
    }
}

// ==================== ЕЖЕДНЕВНЫЙ ====================

async function loadDailyChallenge() {
    const container = document.getElementById('daily-content');
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/daily`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        renderDaily(data);
    } catch (e) {
        container.innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

function renderDaily(data) {
    const container = document.getElementById('daily-content');
    const diffColors = { easy: '#10b981', medium: '#f59e0b', hard: '#ef4444' };
    const diffLabels = { easy: 'Лёгкий', medium: 'Средний', hard: 'Сложный' };

    container.innerHTML = `
        <div class="daily-header">
            <span class="daily-streak">🔥 ${data.streak || 0} дней</span>
            <span class="daily-difficulty" style="background:${diffColors[data.difficulty] || '#888'}">${diffLabels[data.difficulty] || data.difficulty}</span>
        </div>
        ${data.completed ? `
            <div class="daily-completed">
                <div class="daily-checkmark">✅</div>
                <p>Челлендж выполнен!</p>
                <p class="daily-answer">Ответ: ${data.answer}</p>
            </div>
        ` : `
            <div class="daily-question">
                <h3>${data.question}</h3>
                <div class="daily-input-area">
                    <input type="text" id="daily-answer-input" placeholder="Твой ответ..." class="daily-input">
                    <button onclick="submitDailyAnswer()" class="btn primary">Ответить</button>
                </div>
            </div>
        `}
        <div class="daily-meta">
            <span>📂 ${data.category}</span>
            <span>📅 ${data.date}</span>
        </div>
    `;
}

async function submitDailyAnswer() {
    const input = document.getElementById('daily-answer-input');
    const answer = input.value.trim();
    if (!answer) return;

    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/daily/submit?answer=${encodeURIComponent(answer)}`, { method: 'POST' });
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();

        if (data.correct) {
            alert(`✅ Верно! +${data.xp_earned} XP\nОтвет: ${data.answer}`);
        } else {
            alert(`❌ Неверно.\nПравильный ответ: ${data.answer}\n${data.explanation}`);
        }
        loadDailyChallenge();
    } catch (e) {
        alert('Ошибка отправки ответа');
    }
}

// ==================== ПРОФИЛЬ ====================

async function loadProfile() {
    const container = document.getElementById('profile-content');
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/profile`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        renderProfile(data);
    } catch (e) {
        container.innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

function renderProfile(data) {
    const container = document.getElementById('profile-content');
    const avatar = data.avatar || '🛡️';
    const name = data.name || 'Аноним';

    container.innerHTML = `
        <div class="profile-header">
            <div class="profile-avatar">${avatar}</div>
            <div class="profile-name">${escapeHtml(name)}</div>
            <div class="profile-level">Уровень ${data.level || 1}</div>
        </div>
        <div class="profile-stats">
            <div class="profile-stat">
                <span class="profile-stat-value">${data.xp || 0}</span>
                <span class="profile-stat-label">XP</span>
            </div>
            <div class="profile-stat">
                <span class="profile-stat-value">${data.streak || 0}</span>
                <span class="profile-stat-label">Стрик 🔥</span>
            </div>
            <div class="profile-stat">
                <span class="profile-stat-value">${data.reputation || 0}</span>
                <span class="profile-stat-label">Репутация</span>
            </div>
            <div class="profile-stat">
                <span class="profile-stat-value">${data.points || 0}</span>
                <span class="profile-stat-label">Очки</span>
            </div>
        </div>
        <div class="profile-details">
            <div class="profile-detail-row">
                <span>🚩 Флагов</span>
                <span>${data.flags_captured || 0}</span>
            </div>
            <div class="profile-detail-row">
                <span>📝 Квизов</span>
                <span>${data.quizzes_taken || 0}</span>
            </div>
            <div class="profile-detail-row">
                <span>🐳 Лабораторий</span>
                <span>${data.labs_started || 0}</span>
            </div>
        </div>
        <div class="profile-edit">
            <input type="text" id="profile-name-input" placeholder="Имя" value="${escapeHtml(name)}" class="profile-input">
            <button onclick="updateProfile()" class="btn primary">Сохранить</button>
        </div>
    `;
}

async function updateProfile() {
    const nameInput = document.getElementById('profile-name-input');
    const name = nameInput.value.trim();
    if (!name) return;

    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/profile/update`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });
        if (!res.ok) throw new Error('Failed');
        alert('Профиль обновлён!');
        loadProfile();
    } catch (e) {
        alert('Ошибка обновления профиля');
    }
}

// ==================== STORY MODE ====================

async function loadStoryEpisodes() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/story`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        renderStoryEpisodes(data.episodes || []);
    } catch (e) {
        document.getElementById('story-list').innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

function renderStoryEpisodes(episodes) {
    const container = document.getElementById('story-list');
    const diffLabels = { 1: 'Лёгкий', 2: 'Средний', 3: 'Сложный' };
    const catIcons = { web: '🌐', network: '🔌', crypto: '🔐', malware: '🦠', forensics: '🔍', general: '📖' };

    container.innerHTML = episodes.map(ep => `
        <div class="story-item ${ep.completed ? 'completed' : ''}" onclick="startStoryEpisode(${ep.id})">
            <div class="story-icon">${catIcons[ep.category] || '📖'}</div>
            <div class="story-info">
                <div class="story-title">Эпизод ${ep.id}: ${ep.title}</div>
                <div class="story-desc">${ep.desc}</div>
                <div class="story-meta">
                    <span class="story-diff">${diffLabels[ep.difficulty] || ep.difficulty}</span>
                    <span class="story-xp">+${ep.xp} XP</span>
                </div>
            </div>
            <div class="story-status">${ep.completed ? '✅' : '🔒'}</div>
        </div>
    `).join('');
}

async function startStoryEpisode(episodeId) {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/story/start?episode_id=${episodeId}`, { method: 'POST' });
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        alert(`${data.prompt}\n\nВведи ответ или флаг для прохождения.`);
    } catch (e) {
        alert('Ошибка запуска эпизода');
    }
}

// ==================== TRACKS ====================

async function loadTracks() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/tracks`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        renderTracks(data.tracks || []);
    } catch (e) {
        document.getElementById('tracks-list').innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

function renderTracks(tracks) {
    const container = document.getElementById('tracks-list');
    const levelIcons = { beginner: '🟢', intermediate: '🟡', advanced: '🔴' };

    container.innerHTML = tracks.map(t => `
        <div class="track-item" onclick="startTrack('${t.id}')">
            <div class="track-header">
                <span class="track-name">${t.name}</span>
                <span class="track-level">${levelIcons[t.level] || ''} ${t.level}</span>
            </div>
            <div class="track-desc">${t.description}</div>
            <div class="track-meta">
                <span>📄 ${t.topics_count} тем</span>
                <span>⏱️ ${t.estimated_hours}ч</span>
            </div>
            <div class="track-progress-bar">
                <div class="track-progress-fill" style="width: ${t.progress || 0}%"></div>
            </div>
            <div class="track-progress-text">${t.progress || 0}%</div>
        </div>
    `).join('');
}

async function startTrack(trackId) {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/tracks/start?track_id=${trackId}`, { method: 'POST' });
        if (!res.ok) throw new Error('Failed');
        alert(`Трек "${trackId}" выбран. Начни изучение!`);
    } catch (e) {
        alert('Ошибка запуска трека');
    }
}

// ==================== CTF ====================

async function loadCTFStatus() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/ctf/status`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        const container = document.getElementById('ctf-status');
        container.innerHTML = `
            <div class="ctf-stats">
                <div class="ctf-stat">
                    <span class="ctf-stat-value">${data.flags_captured || 0}</span>
                    <span class="ctf-stat-label">Флагов 🚩</span>
                </div>
                <div class="ctf-stat">
                    <span class="ctf-stat-value">${data.risk_level || 0}</span>
                    <span class="ctf-stat-label">Риск ⚠️</span>
                </div>
                <div class="ctf-stat">
                    <span class="ctf-stat-value">${data.ctf_active ? '✅' : '❌'}</span>
                    <span class="ctf-stat-label">CTF активен</span>
                </div>
            </div>
        `;
    } catch (e) {
        document.getElementById('ctf-status').innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка соединения</p>';
    }
}

async function submitFlag() {
    const input = document.getElementById('ctf-flag-input');
    const flag = input.value.trim();
    if (!flag) return;

    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/flags/submit?flag_value=${encodeURIComponent(flag)}`, { method: 'POST' });
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        const resultDiv = document.getElementById('ctf-result');
        resultDiv.classList.remove('hidden');
        resultDiv.className = `ctf-result ${data.correct ? 'correct' : 'wrong'}`;
        resultDiv.textContent = data.message;
        input.value = '';
        loadCTFStatus();
    } catch (e) {
        const resultDiv = document.getElementById('ctf-result');
        resultDiv.classList.remove('hidden');
        resultDiv.className = 'ctf-result wrong';
        resultDiv.textContent = 'Ошибка соединения';
    }
}

// ==================== OSINT ====================

async function loadThreats() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/threats`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        renderThreats(data.threats || []);
    } catch (e) {
        document.getElementById('threats-list').innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка</p>';
    }
}

function renderThreats(threats) {
    const container = document.getElementById('threats-list');
    container.innerHTML = threats.map(t => `
        <div class="threat-item">
            <div class="threat-name">${t.name}</div>
            <div class="threat-country">🌍 ${t.country}</div>
            <div class="threat-desc">${t.description}</div>
            <div class="threat-targets">🎯 ${t.targets}</div>
        </div>
    `).join('');
}

function showOsintSection(section) {
    document.querySelectorAll('.osint-section').forEach(s => s.classList.add('hidden'));
    document.querySelectorAll('.osint-tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(`osint-${section}`).classList.remove('hidden');
    event.target.classList.add('active');

    if (section === 'news') loadNews();
    if (section === 'threats') loadThreats();
}

async function loadNews() {
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/news`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        const container = document.getElementById('news-list');
        const news = data.news || [];
        if (news.length === 0) {
            container.innerHTML = '<p class="placeholder">Нет новостей</p>';
            return;
        }
        container.innerHTML = news.slice(0, 10).map(n => `
            <div class="news-item">
                <div class="news-title">${n.title || 'Без заголовка'}</div>
                <div class="news-date">${n.date || ''}</div>
            </div>
        `).join('');
    } catch (e) {
        document.getElementById('news-list').innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка</p>';
    }
}

async function lookupCVE() {
    const input = document.getElementById('cve-input');
    const cveId = input.value.trim();
    if (!cveId) return;

    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/cve/${encodeURIComponent(cveId)}`);
        if (!res.ok) throw new Error('CVE not found');
        const data = await res.json();
        const resultDiv = document.getElementById('cve-result');
        resultDiv.classList.remove('hidden');
        const cve = data.cve;
        resultDiv.innerHTML = `
            <h3>${cve.id || cveId}</h3>
            <p>${cve.description || 'No description'}</p>
            <div class="cve-meta">
                <span>CVSS: ${cve.cvss || 'N/A'}</span>
                <span>Дата: ${cve.date || 'N/A'}</span>
            </div>
        `;
    } catch (e) {
        const resultDiv = document.getElementById('cve-result');
        resultDiv.classList.remove('hidden');
        resultDiv.innerHTML = `<p style="color:var(--danger)">CVE не найден: ${cveId}</p>`;
    }
}

// ==================== SCANNER ====================

async function scanCode() {
    const code = document.getElementById('scanner-code').value.trim();
    const lang = document.getElementById('scanner-lang').value;
    if (!code) return;

    const resultDiv = document.getElementById('scanner-result');
    resultDiv.classList.remove('hidden');
    resultDiv.innerHTML = '<p class="placeholder">Сканирование...</p>';

    try {
        const formData = new URLSearchParams();
        formData.append('code', code);
        formData.append('language', lang);

        const res = await fetch(`${CONFIG.API_BASE_URL}/api/scan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();

        const findings = data.findings || [];
        if (findings.length === 0) {
            resultDiv.innerHTML = '<p style="color:var(--accent)">✅ Уязвимостей не найдено!</p>';
            return;
        }

        resultDiv.innerHTML = `
            <h3>Найдено: ${findings.length}</h3>
            ${findings.map(f => `
                <div class="finding-item ${f.severity || 'info'}">
                    <span class="finding-severity">${f.severity || 'info'}</span>
                    <span class="finding-desc">${f.description || f.message || ''}</span>
                    <span class="finding-line">Строка: ${f.line || '?'}</span>
                </div>
            `).join('')}
        `;
    } catch (e) {
        resultDiv.innerHTML = `<p style="color:var(--danger)">Ошибка сканирования: ${e.message}</p>`;
    }
}

// ==================== SHOP ====================

async function loadShop() {
    try {
        const [shopRes, profileRes] = await Promise.all([
            fetch(`${CONFIG.API_BASE_URL}/api/shop`),
            fetch(`${CONFIG.API_BASE_URL}/api/profile`)
        ]);
        if (!shopRes.ok || !profileRes.ok) throw new Error('Failed');
        const shopData = await shopRes.json();
        const profileData = await profileRes.json();

        document.getElementById('shop-points').textContent = `Очки: ${profileData.points || 0}`;
        if (shopData.discount > 0) {
            const discountEl = document.getElementById('shop-discount');
            discountEl.classList.remove('hidden');
            discountEl.textContent = `Скидка: ${shopData.discount}%`;
        }

        renderShop(shopData.items || []);
    } catch (e) {
        document.getElementById('shop-list').innerHTML = '<p class="placeholder" style="color:var(--danger)">Ошибка</p>';
    }
}

function renderShop(items) {
    const container = document.getElementById('shop-list');
    const typeIcons = { theme: '🎨', consumable: '🧪', unlock_topic: '📂' };

    container.innerHTML = items.map(item => `
        <div class="shop-item" onclick="purchaseItem('${item.id}')">
            <div class="shop-icon">${typeIcons[item.type] || '📦'}</div>
            <div class="shop-info">
                <div class="shop-name">${item.name}</div>
                <div class="shop-desc">${item.description || ''}</div>
            </div>
            <div class="shop-price">
                ${item.original_price ? `<span class="shop-old-price">${item.original_price}</span>` : ''}
                <span class="shop-price-value">${item.price} XP</span>
            </div>
        </div>
    `).join('');
}

async function purchaseItem(itemId) {
    if (!confirm('Купить этот предмет?')) return;

    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/shop/purchase?item_id=${itemId}`, { method: 'POST' });
        if (!res.ok) {
            const err = await res.json();
            alert(err.detail || 'Ошибка покупки');
            return;
        }
        const data = await res.json();
        alert(`Куплено: ${data.item} за ${data.price} XP`);
        loadShop();
    } catch (e) {
        alert('Ошибка покупки');
    }
}

// ==================== MALWARE ====================

async function analyzeMalware() {
    const hash = document.getElementById('malware-hash').value.trim();
    if (!hash) return;

    const resultDiv = document.getElementById('malware-result');
    resultDiv.classList.remove('hidden');
    resultDiv.innerHTML = '<p class="placeholder">Анализ...</p>';

    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/api/malware?file_hash=${encodeURIComponent(hash)}`, { method: 'POST' });
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        const analysis = data.analysis || {};

        resultDiv.innerHTML = `
            <div class="malware-analysis">
                <h3>Результат анализа</h3>
                <div class="malware-hash-display">Hash: ${analysis.hash || hash}</div>
                ${analysis.name ? `<div class="malware-name">Имя: ${analysis.name}</div>` : ''}
                ${analysis.type ? `<div class="malware-type">Тип: ${analysis.type}</div>` : ''}
                ${analysis.severity ? `<div class="malware-severity">Severity: ${analysis.severity}</div>` : ''}
                ${analysis.description ? `<div class="malware-desc">${analysis.description}</div>` : ''}
                ${analysis.behavior ? `<div class="malware-behavior"><h4>Поведение:</h4><p>${analysis.behavior}</p></div>` : ''}
                ${analysis.unknown ? '<p style="color:var(--warning)">Образец не найден в базе</p>' : ''}
            </div>
        `;
    } catch (e) {
        resultDiv.innerHTML = `<p style="color:var(--danger)">Ошибка анализа: ${e.message}</p>`;
    }
}
