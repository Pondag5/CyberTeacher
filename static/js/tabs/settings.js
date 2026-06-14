/* CyberTeacher — Full Settings tab (all CLI config in web UI) */
window.Tab_settings = {
    _providerInfo: null,

    async render(el) {
        const difficulty = localStorage.getItem('difficulty_level') || 'beginner';
        const soundsMuted = localStorage.getItem('sounds_muted') === 'true';
        const currentTheme = localStorage.getItem('theme') || 'default';

        const themes = window.ThemeManager ? window.ThemeManager.themes : [];
        const themeOptions = themes.map(t =>
            `<button class="btn ${currentTheme === t.id ? 'btn-primary' : 'btn-secondary'} btn-sm settings-theme-btn" data-theme="${t.id}">${t.icon} ${t.label}</button>`
        ).join('');

        const config = await apiCall('/get_config');
        const provider = config.llm_provider || 'ollama';
        const lang = config.language || 'ru';
        const knownModels = window.PROVIDER_KNOWN_MODELS || {};

        const providers = ['ollama', 'groq', 'openrouter', 'huggingface', 'lmstudio', 'mock'];
        const providerBtns = providers.map(p => {
            const info = knownModels[p] || {};
            return `<button class="btn ${provider === p ? 'btn-primary' : 'btn-secondary'} btn-sm settings-provider-btn" data-provider="${p}">${p}${provider === p ? ' \u2714' : ''}</button>`;
        }).join('');

        el.innerHTML = `
            <div class="grid-2">
                <!-- 1. Theme -->
                <div class="card">
                    <h3>\uD83C\uDFA8 \u0422\u0435\u043C\u0430 \u043E\u0444\u043E\u0440\u043C\u043B\u0435\u043D\u0438\u044F</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u0446\u0432\u0435\u0442\u043E\u0432\u0443\u044E \u0442\u0435\u043C\u0443</p>
                    <div style="display:flex;flex-wrap:wrap;gap:6px;">${themeOptions}</div>
                </div>

                <!-- 2. Sound -->
                <div class="card">
                    <h3>\uD83D\uDD0A \u0417\u0432\u0443\u043A</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">\u0417\u0432\u0443\u043A\u043E\u0432\u044B\u0435 \u044D\u0444\u0444\u0435\u043A\u0442\u044B</p>
                    <div style="display:flex;align-items:center;gap:12px;">
                        <button class="btn ${soundsMuted ? 'btn-secondary' : 'btn-primary'} btn-sm" id="settingsSoundToggle">${soundsMuted ? '\uD83D\uDD07 \u0412\u043A\u043B\u044E\u0447\u0438\u0442\u044C' : '\uD83D\uDD0A \u041E\u0442\u043A\u043B\u044E\u0447\u0438\u0442\u044C'}</button>
                        <span style="font-size:0.8rem;color:var(--text-secondary);">${soundsMuted ? '\u0412\u044B\u043A\u043B\u044E\u0447\u0435\u043D' : '\u0412\u043A\u043B\u044E\u0447\u0451\u043D'}</span>
                    </div>
                </div>

                <!-- 3. Difficulty -->
                <div class="card">
                    <h3>\uD83D\uDCD8 \u0423\u0440\u043E\u0432\u0435\u043D\u044C \u0441\u043B\u043E\u0436\u043D\u043E\u0441\u0442\u0438</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">\u0412\u043B\u0438\u044F\u0435\u0442 \u043D\u0430 \u043A\u043E\u043B\u0438\u0447\u0435\u0441\u0442\u0432\u043E \u0432\u043A\u043B\u0430\u0434\u043E\u043A</p>
                    <div style="display:flex;flex-wrap:wrap;gap:6px;">
                        <button class="btn ${difficulty === 'beginner' ? 'btn-primary' : 'btn-secondary'} btn-sm settings-diff-btn" data-diff="beginner">\uD83E\uDD13 \u041D\u043E\u0432\u0438\u0447\u043E\u043A</button>
                        <button class="btn ${difficulty === 'intermediate' ? 'btn-primary' : 'btn-secondary'} btn-sm settings-diff-btn" data-diff="intermediate">\u2696\uFE0F \u0421\u0442\u0443\u0434\u0435\u043D\u0442</button>
                        <button class="btn ${difficulty === 'advanced' ? 'btn-primary' : 'btn-secondary'} btn-sm settings-diff-btn" data-diff="advanced">\u26A1 \u041F\u0440\u043E\u0444\u0438</button>
                        <button class="btn ${difficulty === 'hardcore' ? 'btn-primary' : 'btn-secondary'} btn-sm settings-diff-btn" data-diff="hardcore">\uD83D\uDD25 \u0425\u0430\u0440\u0434\u043A\u043E\u0440</button>
                    </div>
                </div>

                <!-- 4. Language -->
                <div class="card">
                    <h3>\uD83C\uDF10 \u042F\u0437\u044B\u043A</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">\u042F\u0437\u044B\u043A \u0438\u043D\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430</p>
                    <div style="display:flex;flex-wrap:wrap;gap:6px;">
                        <button class="btn ${lang === 'ru' ? 'btn-primary' : 'btn-secondary'} btn-sm settings-lang-btn" data-lang="ru">\uD83C\uDDF7\uD83C\uDDFA \u0420\u0443\u0441\u0441\u043A\u0438\u0439</button>
                        <button class="btn ${lang === 'en' ? 'btn-primary' : 'btn-secondary'} btn-sm settings-lang-btn" data-lang="en">\uD83C\uDDEC\uD83C\uDDE7 English</button>
                    </div>
                    <div class="settings-lang-result" style="margin-top:8px;font-size:0.85rem;"></div>
                </div>

                <!-- 5. LLM Provider -->
                <div class="card">
                    <h3>\uD83E\uDD16 LLM \u041F\u0440\u043E\u0432\u0430\u0439\u0434\u0435\u0440</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">\u0410\u043A\u0442\u0438\u0432\u043D\u044B\u0439: ${provider}</p>
                    <div style="display:flex;flex-wrap:wrap;gap:6px;">${providerBtns}</div>
                    <div class="settings-provider-result" style="margin-top:8px;font-size:0.85rem;"></div>
                    ${provider !== 'ollama' && provider !== 'mock' && provider !== 'lmstudio' ? `
                    <div style="margin-top:12px;display:flex;gap:8px;">
                        <input id="settingsApiKey" type="password" placeholder="API \u043A\u043B\u044E\u0447 \u0434\u043B\u044F ${provider}" style="flex:1;">
                        <button class="btn btn-sm btn-primary" id="settingsSetKeyBtn">\u0423\u0441\u0442\u0430\u043D\u043E\u0432\u0438\u0442\u044C</button>
                    </div>` : ''}
                </div>

                <!-- 6. LLM Model Info -->
                <div class="card">
                    <h3>\uD83D\uDCDA \u041C\u043E\u0434\u0435\u043B\u0438</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">\u0420\u0435\u043A\u043E\u043C\u0435\u043D\u0434\u0443\u0435\u043C\u044B\u0435 \u043C\u043E\u0434\u0435\u043B\u0438 \u0434\u043B\u044F ${provider}</p>
                    <div id="settingsModelList" style="font-size:0.85rem;"></div>
                </div>

                <!-- 7. Feature Flags -->
                <div class="card">
                    <h3>\u2699\uFE0F \u041C\u043E\u0434\u0443\u043B\u0438</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">\u0412\u043A\u043B\u044E\u0447\u0438\u0442\u044C/\u043E\u0442\u043A\u043B\u044E\u0447\u0438\u0442\u044C \u0444\u0443\u043D\u043A\u0446\u0438\u0438</p>
                    <div id="settingsFeatures" style="display:flex;flex-direction:column;gap:6px;">\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430...</div>
                </div>

                <!-- 8. Profile -->
                <div class="card">
                    <h3>\uD83D\uDC64 \u041F\u0440\u043E\u0444\u0438\u043B\u044C</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">\u0418\u0437\u043C\u0435\u043D\u0438\u0442\u044C \u0438\u043C\u044F \u0438 \u0430\u0432\u0430\u0442\u0430\u0440</p>
                    <div style="display:flex;gap:8px;margin-bottom:8px;">
                        <input id="settingsProfileName" placeholder="\u0418\u043C\u044F" style="flex:1;">
                        <button class="btn btn-sm btn-primary" id="settingsProfileSaveBtn">\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C</button>
                    </div>
                    <div style="display:flex;flex-wrap:wrap;gap:6px;">
                        ${['\uD83E\uDDD1\u200D\uD83D\uDCBB', '\uD83D\uDC68\u200D\uD83D\uDCBB', '\uD83D\uDC69\u200D\uD83D\uDCBB', '\uD83E\uDDD1\u200D\uD83C\uDFED', '\uD83D\uDD75\uFE0F\u200D\u2642\uFE0F', '\uD83D\uDC7E', '\uD83E\uDD16', '\uD83D\uDC7B', '\uD83E\uDDD8', '\uD83E\uDDD9'].map(emoji =>
                            `<span class="settings-avatar-option" data-avatar="${emoji}" style="cursor:pointer;font-size:1.5rem;padding:4px;">${emoji}</span>`
                        ).join('')}
                    </div>
                    <div class="settings-profile-result" style="margin-top:8px;font-size:0.85rem;"></div>
                </div>

                <!-- 9. Data -->
                <div class="card">
                    <h3>\uD83D\uDCBE \u0414\u0430\u043D\u043D\u044B\u0435</h3>
                    <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">\u042D\u043A\u0441\u043F\u043E\u0440\u0442/\u0438\u043C\u043F\u043E\u0440\u0442/\u0441\u0431\u0440\u043E\u0441</p>
                    <div style="display:flex;flex-wrap:wrap;gap:6px;">
                        <button class="btn btn-secondary btn-sm" id="settingsExportBtn">\u2B07 \u042D\u043A\u0441\u043F\u043E\u0440\u0442</button>
                        <button class="btn btn-secondary btn-sm" id="settingsImportBtn">\u2B06 \u0418\u043C\u043F\u043E\u0440\u0442</button>
                        <button class="btn btn-danger btn-sm" id="settingsResetBtn">\uD83D\uDDD1\uFE0F \u0421\u0431\u0440\u043E\u0441</button>
                    </div>
                    <input type="file" id="settingsImportFile" accept=".json" style="display:none;">
                </div>

                <!-- 10. About -->
                <div class="card">
                    <h3>\u2139\uFE0F \u041E \u043F\u0440\u0438\u043B\u043E\u0436\u0435\u043D\u0438\u0438</h3>
                    <div style="font-size:0.85rem;color:var(--text-secondary);line-height:1.6;">
                        <p><strong>CyberTeacher</strong> v5.21</p>
                        <p>AI-\u043D\u0430\u0441\u0442\u0430\u0432\u043D\u0438\u043A \u043F\u043E \u043A\u0438\u0431\u0435\u0440\u0431\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u043E\u0441\u0442\u0438</p>
                        <p style="margin-top:8px;">MIT License</p>
                    </div>
                </div>
            </div>
        `;

        this._attachThemeHandlers(el);
        this._attachSoundHandler(el);
        this._attachDifficultyHandlers(el);
        this._attachLangHandlers(el);
        this._attachProviderHandlers(el, provider, knownModels);
        this._loadModels(el, provider, knownModels);
        this._loadFeatures(el, config.feature_flags);
        this._attachProfileHandlers(el);
        this._attachDataHandlers(el);
    },

    _attachThemeHandlers(el) {
        el.querySelectorAll('.settings-theme-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                if (window.ThemeManager) window.ThemeManager.apply(btn.dataset.theme);
                el.querySelectorAll('.settings-theme-btn').forEach(b => { b.className = 'btn btn-secondary btn-sm'; });
                btn.className = 'btn btn-primary btn-sm';
                if (window.Sounds) window.Sounds.click();
            });
        });
    },

    _attachSoundHandler(el) {
        el.querySelector('#settingsSoundToggle')?.addEventListener('click', () => {
            if (window.Sounds) {
                const muted = window.Sounds.toggle();
                const btn = el.querySelector('#settingsSoundToggle');
                const label = btn.nextElementSibling;
                if (muted) {
                    btn.textContent = '\uD83D\uDD07 \u0412\u043A\u043B\u044E\u0447\u0438\u0442\u044C';
                    btn.className = 'btn btn-secondary btn-sm';
                    label.textContent = '\u0412\u044B\u043A\u043B\u044E\u0447\u0435\u043D';
                } else {
                    btn.textContent = '\uD83D\uDD0A \u041E\u0442\u043A\u043B\u044E\u0447\u0438\u0442\u044C';
                    btn.className = 'btn btn-primary btn-sm';
                    label.textContent = '\u0412\u043A\u043B\u044E\u0447\u0451\u043D';
                }
            }
        });
    },

    _attachDifficultyHandlers(el) {
        el.querySelectorAll('.settings-diff-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const diff = btn.dataset.diff;
                localStorage.setItem('difficulty_level', diff);
                el.querySelectorAll('.settings-diff-btn').forEach(b => { b.className = 'btn btn-secondary btn-sm'; });
                btn.className = 'btn btn-primary btn-sm';
                if (window.Sounds) window.Sounds.click();
                if (window.renderNav) window.renderNav();
                if (window.applyBeginnerMode) window.applyBeginnerMode();
            });
        });
    },

    _attachLangHandlers(el) {
        el.querySelectorAll('.settings-lang-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const lang = btn.dataset.lang;
                el.querySelectorAll('.settings-lang-btn').forEach(b => { b.className = 'btn btn-secondary btn-sm'; });
                btn.className = 'btn btn-primary btn-sm';
                const res = await apiCall(`/api/settings/lang?lang=${lang}`, { method: 'POST' });
                const resultDiv = el.querySelector('.settings-lang-result');
                if (res.status === 'ok') {
                    resultDiv.innerHTML = '<span style="color:var(--success);">\u2705 \u042F\u0437\u044B\u043A \u0438\u0437\u043C\u0435\u043D\u0451\u043D</span>';
                    if (window.Sounds) window.Sounds.success();
                } else {
                    resultDiv.innerHTML = `<span style="color:var(--error);">\u274C ${res.detail || '\u041E\u0448\u0438\u0431\u043A\u0430'}</span>`;
                }
            });
        });
    },

    _featureFlags: [
        { id: 'hints', label: '\uD83D\uDCA1 \u041F\u043E\u0434\u0441\u043A\u0430\u0437\u043A\u0438', desc: '\u041F\u043E\u0434\u0441\u043A\u0430\u0437\u043A\u0438 \u0432 \u0440\u0435\u0430\u043B\u044C\u043D\u043E\u043C \u0432\u0440\u0435\u043C\u0435\u043D\u0438' },
        { id: 'news', label: '\uD83D\uDCF0 \u041D\u043E\u0432\u043E\u0441\u0442\u0438', desc: '\u041D\u043E\u0432\u043E\u0441\u0442\u0438 \u043A\u0438\u0431\u0435\u0440\u0431\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u043E\u0441\u0442\u0438' },
        { id: 'social', label: '\uD83D\uDC65 Social Engineering', desc: '\u0422\u0440\u0435\u043D\u0430\u0436\u0451\u0440 \u0441\u043E\u0446\u0438\u0430\u043B\u044C\u043D\u043E\u0439 \u0438\u043D\u0436\u0435\u043D\u0435\u0440\u0438\u0438' },
        { id: 'sandbox', label: '\uD83D\uDEE1\uFE0F \u041F\u0435\u0441\u043E\u0447\u043D\u0438\u0446\u0430', desc: '\u0411\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u044B\u0439 \u0437\u0430\u043F\u0443\u0441\u043A \u043A\u043E\u0434\u0430' },
        { id: 'tracks', label: '\uD83D\uDEE4\uFE0F \u0422\u0440\u0435\u043A\u0438', desc: '\u041E\u0431\u0443\u0447\u0430\u044E\u0449\u0438\u0435 \u0442\u0440\u0435\u043A\u0438' },
        { id: 'missions', label: '\uD83C\uDFC1 \u041C\u0438\u0441\u0441\u0438\u0438', desc: '\u0421\u0438\u0441\u0442\u0435\u043C\u0430 \u043C\u0438\u0441\u0441\u0438\u0439' },
        { id: 'risk', label: '\u26A0\uFE0F \u0420\u0438\u0441\u043A', desc: '\u0423\u0440\u043E\u0432\u0435\u043D\u044C \u0440\u0438\u0441\u043A\u0430 \u0438\u0433\u0440\u043E\u043A\u0430' },
        { id: 'shop', label: '\uD83D\uDED2 \u041C\u0430\u0433\u0430\u0437\u0438\u043D', desc: '\u041C\u0430\u0433\u0430\u0437\u0438\u043D \u0437\u0430 XP' },
        { id: 'spaced_repetition', label: '\uD83D\uDD04 \u041F\u043E\u0432\u0442\u043E\u0440\u0435\u043D\u0438\u044F', desc: '\u0418\u043D\u0442\u0435\u0440\u0432\u0430\u043B\u044C\u043D\u044B\u0435 \u043F\u043E\u0432\u0442\u043E\u0440\u0435\u043D\u0438\u044F' },
    ],

    _attachProviderHandlers(el, currentProvider, knownModels) {
        el.querySelectorAll('.settings-provider-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const prov = btn.dataset.provider;
                if (prov === currentProvider) return;
                const resultDiv = el.querySelector('.settings-provider-result');
                resultDiv.innerHTML = '\u23F3 \u041F\u0435\u0440\u0435\u043A\u043B\u044E\u0447\u0435\u043D\u0438\u0435...';
                const res = await apiCall(`/api/provider/set?provider=${prov}`, { method: 'POST' });
                if (res.status === 'ok') {
                    resultDiv.innerHTML = `<span style="color:var(--success);">\u2705 \u041F\u0435\u0440\u0435\u043A\u043B\u044E\u0447\u0435\u043D\u043E \u043D\u0430 ${prov}</span>`;
                    el.querySelectorAll('.settings-provider-btn').forEach(b => {
                        b.className = 'btn btn-secondary btn-sm';
                        b.textContent = b.dataset.provider;
                    });
                    btn.className = 'btn btn-primary btn-sm';
                    btn.textContent = prov + ' \u2714';
                    if (window.Sounds) window.Sounds.success();
                    this.render(el);
                } else {
                    resultDiv.innerHTML = `<span style="color:var(--error);">\u274C ${res.detail || '\u041E\u0448\u0438\u0431\u043A\u0430'}</span>`;
                }
            });
        });

        const keyBtn = el.querySelector('#settingsSetKeyBtn');
        if (keyBtn) {
            keyBtn.addEventListener('click', async () => {
                const input = el.querySelector('#settingsApiKey');
                const key = input.value.trim();
                if (!key) return;
                const resultDiv = el.querySelector('.settings-provider-result');
                resultDiv.innerHTML = '\u23F3 \u0423\u0441\u0442\u0430\u043D\u043E\u0432\u043A\u0430...';
                const res = await apiCall(`/api/provider/key?provider=${currentProvider}&key=${encodeURIComponent(key)}`, { method: 'POST' });
                if (res.status === 'ok') {
                    resultDiv.innerHTML = '<span style="color:var(--success);">\u2705 \u041A\u043B\u044E\u0447 \u0443\u0441\u0442\u0430\u043D\u043E\u0432\u043B\u0435\u043D</span>';
                    input.value = '';
                    if (window.Sounds) window.Sounds.success();
                } else {
                    resultDiv.innerHTML = `<span style="color:var(--error);">\u274C ${res.detail || '\u041E\u0448\u0438\u0431\u043A\u0430'}</span>`;
                }
            });
        }
    },

    _loadModels(el, provider, knownModels) {
        const container = el.querySelector('#settingsModelList');
        const info = knownModels[provider] || knownModels['ollama'] || {};
        const models = info.suggested || [];
        if (!models.length) {
            container.innerHTML = '<span style="color:var(--text-secondary);">\u041D\u0435\u0442 \u0434\u0430\u043D\u043D\u044B\u0445</span>';
            return;
        }
        container.innerHTML = `<div style="display:flex;flex-direction:column;gap:4px;">${models.map(m =>
            `<div style="padding:4px 8px;background:var(--bg);border-radius:4px;font-family:var(--font-mono);font-size:0.8rem;">${m}</div>`
        ).join('')}</div>`;
        if (info.docs_url) {
            container.innerHTML += `<div style="margin-top:8px;"><a href="${info.docs_url}" target="_blank" style="font-size:0.8rem;">\uD83D\uDD17 \u0412\u0441\u0435 \u043C\u043E\u0434\u0435\u043B\u0438</a></div>`;
        }
    },

    async _loadFeatures(el, initialFlags) {
        const container = el.querySelector('#settingsFeatures');
        const flags = initialFlags || {};
        container.innerHTML = this._featureFlags.map(f => {
            const enabled = flags[f.id] !== false;
            return `<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 8px;background:var(--bg);border-radius:6px;">
                <div><strong>${f.label}</strong><div style="font-size:0.75rem;color:var(--text-secondary);">${f.desc}</div></div>
                <label class="toggle">
                    <input type="checkbox" ${enabled ? 'checked' : ''} data-feature="${f.id}">
                    <span class="toggle-slider"></span>
                    <span class="toggle-knob"></span>
                </label>
            </div>`;
        }).join('');
        container.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.addEventListener('change', async () => {
                const feature = cb.dataset.feature;
                await apiCall(`/api/features/toggle?feature=${feature}`, { method: 'POST' });
                if (window.Sounds) window.Sounds.click();
            });
        });
    },

    _attachProfileHandlers(el) {
        const saveBtn = el.querySelector('#settingsProfileSaveBtn');
        const nameInput = el.querySelector('#settingsProfileName');
        const resultDiv = el.querySelector('.settings-profile-result');

        el.querySelectorAll('.settings-avatar-option').forEach(span => {
            span.addEventListener('click', async () => {
                const avatar = span.dataset.avatar;
                const res = await apiCall('/update_profile', { method: 'POST', body: JSON.stringify({ avatar }) });
                if (res.status === 'ok') {
                    resultDiv.innerHTML = '<span style="color:var(--success);">\u2705 \u0410\u0432\u0430\u0442\u0430\u0440 \u043E\u0431\u043D\u043E\u0432\u043B\u0451\u043D</span>';
                    if (window.Sounds) window.Sounds.success();
                }
            });
        });

        if (saveBtn && nameInput) {
            saveBtn.addEventListener('click', async () => {
                const name = nameInput.value.trim();
                if (!name) { resultDiv.innerHTML = '<span style="color:var(--error);">\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0438\u043C\u044F</span>'; return; }
                const res = await apiCall('/update_profile', { method: 'POST', body: JSON.stringify({ name }) });
                if (res.status === 'ok') {
                    resultDiv.innerHTML = '<span style="color:var(--success);">\u2705 \u0418\u043C\u044F \u043E\u0431\u043D\u043E\u0432\u043B\u0451\u043D\u043E</span>';
                    nameInput.value = '';
                    if (window.Sounds) window.Sounds.success();
                } else {
                    resultDiv.innerHTML = `<span style="color:var(--error);">\u274C ${res.detail || '\u041E\u0448\u0438\u0431\u043A\u0430'}</span>`;
                }
            });
        }
    },

    _attachDataHandlers(el) {
        el.querySelector('#settingsExportBtn')?.addEventListener('click', async () => {
            try {
                const data = await apiCall('/export_user_data');
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `cyberteacher_backup_${new Date().toISOString().slice(0, 10)}.json`;
                a.click();
                URL.revokeObjectURL(url);
                if (window.Sounds) window.Sounds.success();
            } catch (e) {
                if (window.Sounds) window.Sounds.error();
            }
        });

        el.querySelector('#settingsImportBtn')?.addEventListener('click', () => {
            el.querySelector('#settingsImportFile')?.click();
        });
        el.querySelector('#settingsImportFile')?.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            try {
                const text = await file.text();
                const data = JSON.parse(text);
                await apiCall('/import_user_data', { method: 'POST', body: JSON.stringify(data) });
                if (window.Sounds) window.Sounds.success();
                alert('\u0414\u0430\u043D\u043D\u044B\u0435 \u0438\u043C\u043F\u043E\u0440\u0442\u0438\u0440\u043E\u0432\u0430\u043D\u044B');
            } catch (e) {
                if (window.Sounds) window.Sounds.error();
                alert('\u041E\u0448\u0438\u0431\u043A\u0430 \u0438\u043C\u043F\u043E\u0440\u0442\u0430');
            }
        });

        el.querySelector('#settingsResetBtn')?.addEventListener('click', () => {
            if (confirm('\u0421\u0431\u0440\u043E\u0441\u0438\u0442\u044C \u0432\u0441\u0435 \u043D\u0430\u0441\u0442\u0440\u043E\u0439\u043A\u0438 \u0438\u043D\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430?')) {
                localStorage.removeItem('theme');
                localStorage.removeItem('difficulty_level');
                localStorage.removeItem('sounds_muted');
                if (window.Sounds) window.Sounds.success();
                location.reload();
            }
        });
    }
};
