/* Onboarding Wizard — first-time user setup */
window.Onboarding = {
    _completed: false,

    init() {
        this._completed = localStorage.getItem('onboarding_done') === 'true';
    },

    isCompleted() {
        return this._completed;
    },

    async show(el) {
        el.innerHTML = `
            <div style="max-width:600px; margin:0 auto; padding:20px;">
                <h1 style="text-align:center; font-size:2rem; margin-bottom:8px;">
                    <span style="background:linear-gradient(135deg, var(--accent), #9b59b6); -webkit-background-clip:text; background-clip:text; color:transparent;">
                        CyberTeacher
                    </span>
                </h1>
                <p style="text-align:center; color:var(--text-secondary); margin-bottom:24px;">AI-\u043D\u0430\u0441\u0442\u0430\u0432\u043D\u0438\u043A \u043F\u043E \u043A\u0438\u0431\u0435\u0440\u0431\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u043E\u0441\u0442\u0438</p>

                <div id="wizardStep1">
                    <div class="card" style="text-align:center; padding:30px;">
                        <div style="font-size:3rem; margin-bottom:16px;">\uD83E\uDDE0</div>
                        <h2>\u041A\u0430\u043A\u043E\u0439 \u0432\u0430\u0448 \u0443\u0440\u043E\u0432\u0435\u043D\u044C?</h2>
                        <p style="color:var(--text-secondary); margin:12px 0 20px;">\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435, \u0447\u0442\u043E\u0431\u044B \u0438\u043D\u0442\u0435\u0440\u0444\u0435\u0439\u0441 \u0431\u044B\u043B \u043A\u043E\u043C\u0444\u043E\u0440\u0442\u043D\u044B\u043C.</p>

                        <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
                            <div class="card difficulty-card" data-level="beginner" style="cursor:pointer; min-width:160px; padding:20px; border:2px solid transparent; transition:0.2s;">
                                <div style="font-size:2rem;">\uD83E\uDD13</div>
                                <h3>\u041D\u043E\u0432\u0438\u0447\u043E\u043A</h3>
                                <p style="font-size:0.8rem; color:var(--text-secondary);">\u0422\u043E\u043B\u044C\u043A\u043E \u0431\u0430\u0437\u043E\u0432\u044B\u0435 \u043A\u043E\u043C\u0430\u043D\u0434\u044B</p>
                            </div>
                            <div class="card difficulty-card" data-level="intermediate" style="cursor:pointer; min-width:160px; padding:20px; border:2px solid transparent; transition:0.2s;">
                                <div style="font-size:2rem;">\u2696\uFE0F</div>
                                <h3>\u0421\u0442\u0443\u0434\u0435\u043D\u0442</h3>
                                <p style="font-size:0.8rem; color:var(--text-secondary);">\u0421\u0442\u0430\u043D\u0434\u0430\u0440\u0442\u043D\u044B\u0439 \u0440\u0435\u0436\u0438\u043C</p>
                            </div>
                            <div class="card difficulty-card" data-level="advanced" style="cursor:pointer; min-width:160px; padding:20px; border:2px solid transparent; transition:0.2s;">
                                <div style="font-size:2rem;">\u26A1</div>
                                <h3>\u041F\u0440\u043E\u0444\u0438</h3>
                                <p style="font-size:0.8rem; color:var(--text-secondary);">\u041F\u043E\u043B\u043D\u044B\u0439 \u0434\u043E\u0441\u0442\u0443\u043F</p>
                            </div>
                            <div class="card difficulty-card" data-level="hardcore" style="cursor:pointer; min-width:160px; padding:20px; border:2px solid transparent; transition:0.2s;">
                                <div style="font-size:2rem;">\uD83D\uDD25</div>
                                <h3>\u0425\u0430\u0440\u0434\u043A\u043E\u0440</h3>
                                <p style="font-size:0.8rem; color:var(--text-secondary);">\u0411\u0435\u0437 \u043F\u043E\u0434\u0441\u043A\u0430\u0437\u043E\u043A</p>
                            </div>
                        </div>

                        <button id="wizardNext" style="margin-top:20px; display:none;">\u0414\u0430\u043B\u0435\u0435 \u2192</button>
                    </div>
                </div>

                <div id="wizardStep2" style="display:none;">
                    <div class="card" style="text-align:center; padding:30px;">
                        <div style="font-size:3rem; margin-bottom:16px;">\uD83C\uDFAF</div>
                        <h2>\u041A\u0430\u043A \u044D\u0442\u043E \u0440\u0430\u0431\u043E\u0442\u0430\u0435\u0442?</h2>
                        <div style="text-align:left; max-width:400px; margin:16px auto;">
                            <div style="padding:8px 0; border-bottom:1px solid var(--border);">\uD83D\uDCAC <strong>/quiz</strong> \u2014 \u043A\u0432\u0438\u0437\u044B</div>
                            <div style="padding:8px 0; border-bottom:1px solid var(--border);">\uD83D\uDC33 <strong>/lab</strong> \u2014 Docker-\u043B\u0430\u0431\u043E\u0440\u0430\u0442\u043E\u0440\u0438\u0438</div>
                            <div style="padding:8px 0; border-bottom:1px solid var(--border);">\uD83D\uDCDA <strong>/courses</strong> \u2014 \u043A\u0443\u0440\u0441\u044B</div>
                            <div style="padding:8px 0; border-bottom:1px solid var(--border);">\uD83C\uDFAF <strong>/daily</strong> \u2014 \u0435\u0436\u0435\u0434\u043D\u0435\u0432\u043D\u044B\u0439 \u0432\u044B\u0437\u043E\u0432</div>
                            <div style="padding:8px 0; border-bottom:1px solid var(--border);">\u2753 <strong>/help</strong> \u2014 \u0432\u0441\u0435 \u043A\u043E\u043C\u0430\u043D\u0434\u044B</div>
                            <div style="padding:8px 0;">\uD83E\uDE7A <strong>/doctor</strong> \u2014 \u043D\u0430\u0441\u0442\u0440\u043E\u0439\u043A\u0430 AI</div>
                        </div>
                        <button id="wizardStart" style="margin-top:20px;">\u041D\u0430\u0447\u0430\u0442\u044C! \uD83D\uDE80</button>
                    </div>
                </div>
            </div>
        `;

        let selectedLevel = null;

        el.querySelectorAll('.difficulty-card').forEach(card => {
            card.addEventListener('click', () => {
                el.querySelectorAll('.difficulty-card').forEach(c => c.style.borderColor = 'var(--border)');
                card.style.borderColor = 'var(--accent)';
                card.style.boxShadow = 'var(--glow)';
                selectedLevel = card.dataset.level;
                document.getElementById('wizardNext').style.display = 'inline-block';
                if (window.Sounds) Sounds.click();
            });
        });

        document.getElementById('wizardNext').onclick = () => {
            if (!selectedLevel) return;
            document.getElementById('wizardStep1').style.display = 'none';
            document.getElementById('wizardStep2').style.display = 'block';
            if (window.Sounds) Sounds.success();
        };

        document.getElementById('wizardStart').onclick = async () => {
            const token = localStorage.getItem('auth_token');
            if (token) {
                await apiCall('/get_config');
            }
            localStorage.setItem('difficulty_level', selectedLevel || 'beginner');
            localStorage.setItem('onboarding_done', 'true');
            this._completed = true;
            if (window.applyBeginnerMode) applyBeginnerMode();
            if (window.Sounds) Sounds.levelUp();
            loadInitialData();
        };
    }
};
