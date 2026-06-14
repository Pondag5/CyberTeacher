/* CyberTeacher — Utils v2 (apiCall, themes, renderUserInfo) */
const API_BASE = window.location.origin;

const API_PATH_MAP = {
    '/get_progress': '/api/progress',
    '/get_modes': '/api/modes',
    '/get_courses': '/api/courses',
    '/get_labs': '/api/labs',
    '/get_profile': '/api/profile',
    '/get_daily_challenge': '/api/daily',
    '/get_achievements_list': '/api/achievements/list',
    '/get_skills': '/api/skills',
    '/get_shop': '/api/shop',
    '/get_story_episodes': '/api/story',
    '/get_tracks': '/api/tracks',
    '/get_ctf_status': '/api/ctf/status',
    '/get_config': '/api/config',
    '/get_world': '/api/world',
    '/get_episodes': '/api/episodes',
    '/get_cyberpsychosis': '/api/cyberpsychosis',
    '/get_detailed_stats': '/api/stats',
    '/get_heatmap': '/api/heatmap',
    '/get_threats': '/api/threats',
    '/get_news': '/api/news',
    '/get_history': '/api/history',
    '/get_scan_rules': '/api/scan/rules',
    '/get_versus_scenarios': '/api/versus/scenarios',
    '/chat_with_llm': '/api/chat',
    '/docker_containers': '/api/docker/containers',
    '/docker_status': '/api/docker/status',
    '/docker_start_lab': '/api/docker/start',
    '/docker_stop_lab': '/api/docker/stop',
    '/start_lab': '/api/labs/start',
    '/stop_lab': '/api/labs/stop',
    '/generate_quiz': '/api/quiz/generate',
    '/submit_quiz_result': '/api/quiz/result',
    '/list_users': '/api/users',
    '/set_role': '/api/users/role',
    '/create_course': '/api/courses/create',
    '/verify_auth': '/api/auth/verify',
    '/login': '/api/auth/login',
    '/register': '/api/auth/register',
    '/set_mode': '/api/modes/set',
    '/select_course': '/api/courses/select',
    '/submit_daily_challenge': '/api/daily/submit',
    '/purchase_item': '/api/shop/purchase',
    '/scan_code': '/api/scan',
    '/start_versus': '/api/versus/start',
    '/versus_move': '/api/versus/move',
    '/start_story_episode': '/api/story/start',
    '/start_track': '/api/tracks/start',
    '/submit_flag': '/api/ctf/flag',
    '/analyze_malware': '/api/malware',
    '/export_user_data': '/api/gdpr/export',
    '/import_user_data': '/api/gdpr/import',
    '/export_report': '/api/report',
    '/create_user': '/api/auth/register',
    '/update_profile': '/api/profile/update',
    '/add_topic': '/api/courses/topic',
    '/update_course': '/api/courses/update',
    '/delete_course': '/api/courses/delete',
};

function _mapApiPath(endpoint) {
    if (endpoint.startsWith('http') || endpoint.startsWith('/api/')) return endpoint;
    for (const [old, new_] of Object.entries(API_PATH_MAP)) {
        if (endpoint === old || endpoint.startsWith(old + '?')) {
            const params = endpoint.includes('?') ? endpoint.split('?')[1] : '';
            return params ? `${new_}?${params}` : new_;
        }
    }
    return endpoint;
}

async function apiCall(endpoint, options = {}) {
    const mapped = _mapApiPath(endpoint);
    const url = mapped.startsWith('http') ? mapped : `${API_BASE}${mapped}`;
    const method = (options.method || 'GET').toUpperCase();
    try {
        const res = await fetch(url, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        if (!res.ok) {
            let detail = `HTTP ${res.status}`;
            try { const err = await res.json(); if (err.detail) detail = err.detail; } catch (e) {}
            throw new Error(detail);
        }
        const data = await res.json();

        if (method === 'GET' && window.OfflineDB && navigator.onLine) {
            try { await OfflineDB.cacheResponse(url, data, 3600000); } catch (e) { /* ignore */ }
        }
        return data;
    } catch(e) {
        console.error(`API error ${endpoint}:`, e);
        if (method === 'GET' && window.OfflineDB) {
            try {
                const cached = await OfflineDB.getCachedResponse(url);
                if (cached) {
                    console.log(`Serving from cache: ${endpoint}`);
                    return cached;
                }
            } catch (ce) { /* ignore */ }
        }
        return { error: true, message: e.message };
    }
}

function renderUserInfo() {
    const userInfoSpan = document.getElementById('userInfo');
    userInfoSpan.innerHTML = `
        <span class="avatar">${appState.avatar}</span>
        <span class="name">${appState.username}</span>
        <div class="xp-bar"><span class="level">${appState.level}</span> &#11088; ${Math.floor(appState.xp)} XP</div>
        <div class="xp-bar">&#128293; ${appState.streak} дн.</div>
    `;
}

function applyBeginnerMode() {
    const difficulty = localStorage.getItem('difficulty_level') || 'beginner';
    if (difficulty === 'beginner') {
        document.body.classList.add('beginner-mode');
    } else {
        document.body.classList.remove('beginner-mode');
    }
}

function initThemes() {
    const container = document.getElementById('themeToggle');
    if (!container) return;

    const themeDefs = window.ThemeManager ? window.ThemeManager.themes : [];
    container.innerHTML = themeDefs.map(t =>
        `<button class="theme-btn" data-theme="${t.id}" title="${t.desc}">${t.icon} ${t.label}</button>`
    ).join('');

    if (window.ThemeManager) {
        window.ThemeManager.init();
    }

    container.querySelectorAll('.theme-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (window.ThemeManager) {
                window.ThemeManager.apply(btn.dataset.theme);
            }
        });
    });
}

function initMobileMenu() {
    document.getElementById('menuToggle')?.addEventListener('click', () => {
        document.getElementById('sidebar').classList.toggle('open');
    });
    // Close sidebar on nav click (mobile)
    document.getElementById('navContainer')?.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            document.getElementById('sidebar').classList.remove('open');
        }
    });
}

function initSoundToggle() {
    const btn = document.getElementById('soundToggle');
    if (!btn) return;
    if (window.Sounds) window.Sounds.init();
    btn.addEventListener('click', () => {
        if (window.Sounds) {
            window.Sounds.toggle();
        }
    });
}

function updateStatusBar(data) {
    const el = (id) => document.getElementById(id);
    if (data) {
        if (data.llm_provider) el('statusLLM').textContent = `LLM: ${data.llm_provider}`;
        if (data.risk_level !== undefined) el('statusRisk').textContent = `Risk: ${data.risk_level}%`;
        if (data.cyberpsychosis !== undefined) el('statusCyber').textContent = `Cyberpsychosis: Stage ${data.cyberpsychosis}`;
        if (data.xp !== undefined) el('statusXP').textContent = `XP: ${Math.floor(data.xp)}`;
    }
    // Update clock
    const now = new Date();
    el('statusTime').textContent = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
}

// Init OfflineDB on load
if (window.OfflineDB) OfflineDB.init().catch(() => {});
