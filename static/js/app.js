/* CyberTeacher — App v2 (state, routing, tab transitions, init) */
let currentTab = 'modes';
const _loadedTabs = new Set();

const TAB_SOURCES = {
    modes: 'js/tabs/modes.js', chat: 'js/tabs/chat.js', progress: 'js/tabs/progress.js',
    quiz: 'js/tabs/quiz.js', daily: 'js/tabs/daily.js', profile: 'js/tabs/profile.js',
    courses: 'js/tabs/courses.js', story: 'js/tabs/story.js', tracks: 'js/tabs/tracks.js',
    ctf: 'js/tabs/ctf.js', labs: 'js/tabs/labs.js', osint: 'js/tabs/osint.js',
    scanner: 'js/tabs/scanner.js', shop: 'js/tabs/shop.js', malware: 'js/tabs/malware.js',
    achievements: 'js/tabs/achievements.js', versus: 'js/tabs/versus.js', world: 'js/tabs/world.js',
    stats: 'js/tabs/stats.js', admin: 'js/tabs/admin.js', export: 'js/tabs/export.js',
    leaderboard: 'js/tabs/leaderboard.js',
    missions: 'js/tabs/missions.js',
    writeups: 'js/tabs/writeups.js',
    recon: 'js/tabs/recon.js',
    labs_external: 'js/tabs/labs_external.js',
    social: 'js/tabs/social.js',
    phishing: 'js/tabs/phishing.js',
    sandbox: 'js/tabs/sandbox.js',
    network: 'js/tabs/network.js',

    mood: 'js/tabs/mood.js',
    summary: 'js/tabs/summary.js',
    dockergen: 'js/tabs/dockergen.js',
    news: 'js/tabs/news.js',
    history: 'js/tabs/history.js',
    threats: 'js/tabs/threats.js',
    offline: 'js/tabs/offline.js',
    skills: 'js/tabs/skills.js',
    equipment: 'js/tabs/equipment.js',
    timeloop: 'js/tabs/timeloop.js',
    sync: 'js/tabs/sync.js',
    exploit: 'js/tabs/exploit.js',
    dashboard: 'js/tabs/dashboard.js',
    analytics: 'js/tabs/analytics.js',
    code_review: 'js/tabs/code_review.js',
    walkthroughs: 'js/tabs/walkthroughs.js',
    ctf_flags: 'js/tabs/ctf_flags.js',
    mermaid: 'js/tabs/mermaid.js',

    bug_bounty: 'js/tabs/bug_bounty.js',
    media: 'js/tabs/media.js',
    context: 'js/tabs/context.js',
    doctor: 'js/tabs/doctor.js',
    mistakes: 'js/tabs/mistakes.js', feedback: 'js/tabs/feedback.js',
    settings: 'js/tabs/settings.js'
};

let appState = {
    xp: 0, level: 1, reputation: 0, streak: 0, points: 0,
    username: '\u0410\u043D\u043E\u043D\u0438\u043C', avatar: '\uD83E\uDDD1\u200D\uD83D\uDCBB',
    modes: [], current_mode: 'teacher',
    courses: [], labs: [], achievements: [],
    weak_topics: [], skills: [], shop: [],
    daily: null, storyEpisodes: [], tracks: [], missions: [],
    ctf: { flags_captured: 0, risk_level: 0 },
    chatHistory: []
};

const tabs = [
    { id: 'modes', icon: 'fa-robot', label: '\u0420\u0435\u0436\u0438\u043C\u044B' },
    { id: 'chat', icon: 'fa-comment', label: '\u0427\u0430\u0442' },
    { id: 'progress', icon: 'fa-chart-line', label: '\u041F\u0440\u043E\u0433\u0440\u0435\u0441\u0441' },
    { id: 'quiz', icon: 'fa-pen-alt', label: '\u041A\u0432\u0438\u0437\u044B' },
    { id: 'daily', icon: 'fa-calendar-day', label: '\u0414\u0435\u0439\u043B\u0438' },
    { id: 'profile', icon: 'fa-user', label: '\u041F\u0440\u043E\u0444\u0438\u043B\u044C' },
    { id: 'courses', icon: 'fa-book', label: '\u041A\u0443\u0440\u0441\u044B' },
    { id: 'story', icon: 'fa-scroll', label: '\u0418\u0441\u0442\u043E\u0440\u0438\u044F' },
    { id: 'tracks', icon: 'fa-road', label: '\u0422\u0440\u0435\u043A\u0438' },
    { id: 'ctf', icon: 'fa-flag-checkered', label: 'CTF' },
    { id: 'labs', icon: 'fa-flask', label: '\u041B\u0430\u0431\u044B' },
    { id: 'osint', icon: 'fa-globe', label: 'OSINT' },
    { id: 'scanner', icon: 'fa-code', label: '\u0421\u043A\u0430\u043D\u0435\u0440' },
    { id: 'shop', icon: 'fa-store', label: '\u041C\u0430\u0433\u0430\u0437\u0438\u043D' },
    { id: 'malware', icon: 'fa-skull', label: 'Malware' },
    { id: 'achievements', icon: 'fa-trophy', label: '\u0414\u043E\u0441\u0442\u0438\u0436\u0435\u043D\u0438\u044F' },
    { id: 'versus', icon: 'fa-fist-raised', label: '\u0414\u0443\u044D\u043B\u044C' },
    { id: 'world', icon: 'fa-globe-americas', label: '\u041C\u0438\u0440' },
    { id: 'stats', icon: 'fa-chart-simple', label: '\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043A\u0430' },
    { id: 'export', icon: 'fa-download', label: '\u0414\u0430\u043D\u043D\u044B\u0435' },
    { id: 'missions', icon: 'fa-flag-checkered', label: '\u041C\u0438\u0441\u0441\u0438\u0438' },
    { id: 'writeups', icon: 'fa-feather-alt', label: 'Writeups' },
    { id: 'recon', icon: 'fa-satellite-dish', label: 'Recon' },
    { id: 'labs_external', icon: 'fa-server', label: 'External Labs' },
    { id: 'social', icon: 'fa-user-secret', label: 'Social' },
    { id: 'phishing', icon: 'fa-fish', label: 'Phishing' },
    { id: 'sandbox', icon: 'fa-shield-halved', label: 'Sandbox' },
    { id: 'network', icon: 'fa-network-wired', label: 'Network' },
    { id: 'mood', icon: 'fa-smile', label: 'Mood' },
    { id: 'summary', icon: 'fa-feather-alt', label: 'Summary' },
    { id: 'dockergen', icon: 'fa-cubes', label: 'Docker Gen' },
    { id: 'news', icon: 'fa-newspaper', label: 'News' },
    { id: 'history', icon: 'fa-history', label: 'History' },
    { id: 'threats', icon: 'fa-skull-crossbones', label: 'Threats' },
    { id: 'offline', icon: 'fa-wifi-slash', label: 'Offline' },
    { id: 'skills', icon: 'fa-code-branch', label: 'Skills' },
    { id: 'equipment', icon: 'fa-toolbox', label: 'Equipment' },
    { id: 'timeloop', icon: 'fa-hourglass-half', label: 'Time Loop' },
    { id: 'sync', icon: 'fa-sync', label: 'Sync' },
    { id: 'exploit', icon: 'fa-bug', label: 'Exploit' },
    { id: 'dashboard', icon: 'fa-chart-pie', label: 'Dashboard' },
    { id: 'analytics', icon: 'fa-chart-line', label: 'Analytics' },
    { id: 'code_review', icon: 'fa-code', label: 'Code Review' },
    { id: 'walkthroughs', icon: 'fa-book', label: 'Walkthroughs' },
    { id: 'ctf_flags', icon: 'fa-flag', label: 'CTF Flags' },
    { id: 'mermaid', icon: 'fa-diagram-project', label: 'Mermaid' },
    { id: 'bug_bounty', icon: 'fa-bug', label: 'Bug Bounty' },
    { id: 'media', icon: 'fa-play-circle', label: 'Media' },
    { id: 'leaderboard', icon: 'fa-medal', label: '\u0420\u0435\u043A\u043E\u0440\u0434\u044B' },
    { id: 'admin', icon: 'fa-cog', label: '\u0410\u0434\u043C\u0438\u043D' },
    { id: 'doctor', icon: 'fa-stethoscope', label: '\u0414\u0438\u0430\u0433\u043D\u043E\u0441\u0442\u0438\u043A\u0430' },
    { id: 'context', icon: 'fa-database', label: '\u041A\u043E\u043D\u0442\u0435\u043A\u0441\u0442' },
    { id: 'mistakes', icon: 'fa-exclamation-triangle', label: '\u041E\u0448\u0438\u0431\u043A\u0438' },
    { id: 'feedback', icon: 'fa-comment-dots', label: '\u041E\u0442\u0437\u044B\u0432' },
    { id: 'settings', icon: 'fa-sliders-h', label: '\u041D\u0430\u0441\u0442\u0440\u043E\u0439\u043A\u0438' }
];

function renderNav() {
    const navContainer = document.getElementById('navContainer');
    const difficulty = localStorage.getItem('difficulty_level') || 'beginner';

    const hiddenTabs = {
        beginner: ['ctf', 'osint', 'scanner', 'malware', 'versus', 'admin', 'leaderboard', 'export'],
        intermediate: ['admin'],
        advanced: [],
        hardcore: [],
    };
    const hidden = hiddenTabs[difficulty] || [];
    const visibleTabs = tabs.filter(t => !hidden.includes(t.id));

    navContainer.innerHTML = visibleTabs.map(tab => `
        <div class="nav-item ${currentTab === tab.id ? 'active' : ''}" data-tab="${tab.id}">
            <i class="fas ${tab.icon}"></i>
            <span>${tab.label}</span>
        </div>
    `).join('');

    const badge = document.getElementById('difficultyBadge');
    if (badge) {
        const levelLabels = {
            beginner: '\uD83E\uDD13 \u041D\u043E\u0432\u0438\u0447\u043E\u043A',
            intermediate: '\u2696\uFE0F \u0421\u0442\u0443\u0434\u0435\u043D\u0442',
            advanced: '\u26A1 \u041F\u0440\u043E\u0444\u0438',
            hardcore: '\uD83D\uDD25 \u0425\u0430\u0440\u0434\u043A\u043E\u0440'
        };
        badge.innerHTML = `<span class="badge">${levelLabels[difficulty] || difficulty}</span>`;
    }

    document.querySelectorAll('.nav-item').forEach(el => {
        el.addEventListener('click', () => {
            if (currentTab === el.dataset.tab) return;
            if (window.Sounds) window.Sounds.click();
            currentTab = el.dataset.tab;
            renderNav();
            renderCurrentTab();
        });
    });
}

function loadTabScript(tabId) {
    if (_loadedTabs.has(tabId) || !TAB_SOURCES[tabId]) return Promise.resolve();
    return new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = TAB_SOURCES[tabId];
        s.onload = () => { _loadedTabs.add(tabId); resolve(); };
        s.onerror = () => resolve();
        document.body.appendChild(s);
    });
}

async function renderCurrentTab() {
    const contentDiv = document.getElementById('content');

    // Play tab transition sound
    if (window.Sounds) window.Sounds.pageTransition();

    // Fade out current content
    contentDiv.style.opacity = '0';
    contentDiv.style.transform = 'translateY(8px)';
    contentDiv.style.transition = 'opacity 0.2s, transform 0.2s';

    // Show skeleton loading
    setTimeout(async () => {
        contentDiv.innerHTML = `
            <div class="tab-content">
                <div class="skeleton skeleton-card"></div>
                <div class="skeleton skeleton-line"></div>
                <div class="skeleton skeleton-line"></div>
                <div class="skeleton skeleton-line" style="width:60%"></div>
            </div>
        `;

        await loadTabScript(currentTab);
        const tab = window['Tab_' + currentTab];
        if (tab && tab.render) {
            contentDiv.innerHTML = '<div class="tab-content"></div>';
            const innerDiv = contentDiv.querySelector('.tab-content');
            await tab.render(innerDiv);
        } else {
            contentDiv.innerHTML = '<div class="tab-content"><div class="card"><p>\u0421\u0442\u0440\u0430\u043D\u0438\u0446\u0430 \u0432 \u0440\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u043A\u0435</p></div></div>';
        }

        // Fade in new content
        contentDiv.style.opacity = '1';
        contentDiv.style.transform = 'translateY(0)';

        // Re-init border effects for new cards
        if (window.CyberBorder) setTimeout(() => window.CyberBorder.init(), 100);
        if (window.GlitchText) setTimeout(() => window.GlitchText.applyAll(), 100);
    }, 200);
}

async function loadInitialData() {
    const [progress, modesRes, coursesRes, labsRes, profileRes, dailyRes, achievementsRes, skillsRes, shopRes, storyRes, tracksRes, ctfRes] = await Promise.all([
        apiCall('/get_progress').catch(() => ({})),
        apiCall('/get_modes').catch(() => ({ modes: [] })),
        apiCall('/get_courses').catch(() => ({ courses: [] })),
        apiCall('/get_labs').catch(() => ({ labs: [] })),
        apiCall('/get_profile').catch(() => ({})),
        apiCall('/get_daily_challenge').catch(() => ({})),
        apiCall('/get_achievements_list').catch(() => ({ achievements: [] })),
        apiCall('/get_skills').catch(() => ({ skills: [] })),
        apiCall('/get_shop').catch(() => ({ items: [] })),
        apiCall('/get_story_episodes').catch(() => ({ episodes: [] })),
        apiCall('/get_tracks').catch(() => ({ tracks: [] })),
        apiCall('/get_ctf_status').catch(() => ({}))
    ]);
    appState.xp = progress.xp || 0;
    appState.level = progress.level || 1;
    appState.reputation = progress.reputation || 0;
    appState.streak = progress.streak || 0;
    appState.points = progress.points || 0;
    appState.username = profileRes.name || '\u0410\u043D\u043E\u043D\u0438\u043C';
    appState.avatar = profileRes.avatar || '\uD83E\uDDD1\u200D\uD83D\uDCBB';
    appState.modes = modesRes.modes || [];
    appState.current_mode = modesRes.current || 'teacher';
    appState.courses = coursesRes.courses || [];
    appState.labs = labsRes.labs || [];
    appState.achievements = achievementsRes.achievements || [];
    appState.skills = skillsRes.skills || [];
    appState.shop = shopRes.items || [];
    appState.daily = dailyRes;
    appState.storyEpisodes = storyRes.episodes || [];
    appState.tracks = tracksRes.tracks || [];
    appState.ctf = ctfRes;
    renderUserInfo();
    renderNav();
    renderCurrentTab();

    // Update status bar with API data
    updateStatusBar({ xp: progress.xp, risk_level: ctfRes.risk_level });
}

document.addEventListener('DOMContentLoaded', () => {
    initThemes();
    initMobileMenu();
    initSoundToggle();

    // Clock tick
    setInterval(() => updateStatusBar(), 10000);
    updateStatusBar();

    // Check onboarding
    if (window.Onboarding) {
        Onboarding.init();
        if (!Onboarding.isCompleted()) {
            const contentDiv = document.getElementById('content');
            Onboarding.show(contentDiv);
            renderNav();
            return;
        }
    }
    loadInitialData();

    // Cyberpunk effects
    if (window.CyberParticles) CyberParticles.init('content');
    if (window.CyberBorder) setTimeout(() => window.CyberBorder.init(), 500);
    if (window.GlitchText) setTimeout(() => window.GlitchText.applyAll(), 500);

    // Notifications
    if (window.Notifications) {
        Notifications.init();
        setInterval(() => Notifications.pollEvents(), 60000);
        document.getElementById('notifBtn')?.addEventListener('click', async () => {
            const perm = await Notifications.requestPermission();
            if (perm === 'granted') {
                Notifications.send('\u2705 \u0423\u0432\u0435\u0434\u043E\u043C\u043B\u0435\u043D\u0438\u044F \u0432\u043A\u043B\u044E\u0447\u0435\u043D\u044B', '\u0412\u044B \u0431\u0443\u0434\u0435\u0442\u0435 \u043F\u043E\u043B\u0443\u0447\u0430\u0442\u044C \u0443\u0432\u0435\u0434\u043E\u043C\u043B\u0435\u043D\u0438\u044F \u043E \u0441\u043E\u0431\u044B\u0442\u0438\u044F\u0445 \u0432 \u043C\u0438\u0440\u0435.');
            } else {
                alert('\u0423\u0432\u0435\u0434\u043E\u043C\u043B\u0435\u043D\u0438\u044F \u043D\u0435 \u0440\u0430\u0437\u0440\u0435\u0448\u0435\u043D\u044B.');
            }
        });
    }
    if (window.NotificationsWS) NotificationsWS.connect();

    // ── State auto-save ──
    async function pwaSaveState() {
        try {
            const resp = await fetch('/api/save', { method: 'POST' });
            const data = await resp.json();
            if (data.status === 'ok') {
                console.log('[AutoSave] state saved', new Date().toLocaleTimeString());
            }
        } catch (e) {
            console.warn('[AutoSave] failed:', e);
        }
    }

    window.addEventListener('beforeunload', () => {
        pwaSaveState();
    });
    setInterval(pwaSaveState, 30000); // every 30 seconds
});
