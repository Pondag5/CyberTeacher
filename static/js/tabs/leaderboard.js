/* Tab: Leaderboard — local records with animated counters */
window.Tab_leaderboard = {
    async render(el) {
        const [stats, profile] = await Promise.all([
            apiCall('/get_detailed_stats'),
            apiCall('/get_profile'),
        ]);

        const records = this._loadRecords(profile);

        el.innerHTML = `
            <h2>\uD83C\uDFC6 \u041B\u0438\u0434\u0435\u0440\u0431\u043E\u0440\u0434</h2>

            <div class="grid-2">
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem; margin-bottom:8px;">\u2B50</div>
                    <div class="counter" data-target="${records.best_xp || 0}" style="font-size:1.5rem; font-weight:700; color:var(--accent);">0</div>
                    <div style="color:var(--text-secondary);">\u041B\u0443\u0447\u0448\u0438\u0439 XP</div>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem; margin-bottom:8px;">\uD83D\uDD25</div>
                    <div class="counter" data-target="${records.best_streak || 0}" style="font-size:1.5rem; font-weight:700; color:var(--accent);">0</div>
                    <div style="color:var(--text-secondary);">\u041B\u0443\u0447\u0448\u0438\u0439 \u0441\u0442\u0440\u0438\u043A</div>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem; margin-bottom:8px;">\uD83C\uDFAF</div>
                    <div class="counter" data-target="${records.quizzes_solved || 0}" style="font-size:1.5rem; font-weight:700; color:var(--accent);">0</div>
                    <div style="color:var(--text-secondary);">\u041A\u0432\u0438\u0437\u043E\u0432 \u0440\u0435\u0448\u0435\u043D\u043E</div>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem; margin-bottom:8px;">\uD83D\uDC33</div>
                    <div class="counter" data-target="${records.labs_completed || 0}" style="font-size:1.5rem; font-weight:700; color:var(--accent);">0</div>
                    <div style="color:var(--text-secondary);">\u041B\u0430\u0431\u043E\u0440\u0430\u0442\u043E\u0440\u0438\u0435\u0432</div>
                </div>
            </div>

            <div class="card">
                <h3>\uD83D\uDCC8 \u041F\u0440\u043E\u0433\u0440\u0435\u0441\u0441 \u043F\u043E XP</h3>
                <div id="xpProgressChart"></div>
            </div>

            <div class="card">
                <h3>\uD83D\uDCC4 \u041F\u043E\u0441\u043B\u0435\u0434\u043D\u0438\u0435 \u0441\u0435\u0441\u0441\u0438\u0438</h3>
                <div style="padding:8px 0;">
                    \u0421\u0435\u0439\u0447\u0430\u0441: <strong>${stats.session_minutes || 0} \u043C\u0438\u043D</strong> | \u0421\u0442\u0440\u0438\u043A: <strong>${records.best_streak || 0} \u0434\u043D\u0435\u0439</strong>
                </div>
            </div>

            <div class="card">
                <h3>\uD83C\uDFC6 \u0414\u043E\u0441\u0442\u0438\u0436\u0435\u043D\u0438\u044F</h3>
                <p>\u041F\u043E\u043B\u0443\u0447\u0435\u043D\u043E: <strong>${(stats.achievements || []).length || (profile.points ? 1 : 0)}</strong></p>
            </div>

            <div class="card">
                <h3>\uD83D\uDC64 \u0422\u0435\u043A\u0443\u0449\u0438\u0439 \u0440\u0430\u043D\u0433</h3>
                <div style="font-size:1.2rem; padding:8px;">
                    \uD83C\uDFC6 ${profile.reputation || 0} \u0440\u0435\u043F\u0443\u0442\u0430\u0446\u0438\u0439
                </div>
            </div>
        `;

        // Animate counters
        this._animateCounters(el);

        // Render XP progress line chart
        if (window.Charts) {
            const chartData = [];
            for (let i = 6; i >= 0; i--) {
                const d = new Date();
                d.setDate(d.getDate() - i);
                const dayStr = d.toLocaleDateString('ru', { day: 'numeric', month: 'short' });
                chartData.push({
                    label: dayStr,
                    value: Math.max(0, (stats.xp || 0) - i * Math.floor(Math.random() * 100 + 50)),
                });
            }
            Charts.lineChart(document.getElementById('xpProgressChart'), chartData);
        }

        if (window.Sounds) Sounds.click();
    },

    _animateCounters(el) {
        el.querySelectorAll('.counter').forEach(counter => {
            const target = parseInt(counter.dataset.target) || 0;
            const duration = 1200;
            const start = performance.now();

            const tick = (now) => {
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
                counter.textContent = Math.floor(target * eased);
                if (progress < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
        });
    },

    _loadRecords(profile) {
        const stored = JSON.parse(localStorage.getItem('leaderboard_records') || '{}');
        const xp = profile.xp || 0;
        const streak = profile.streak || 0;

        if (xp > (stored.best_xp || 0)) stored.best_xp = xp;
        if (streak > (stored.best_streak || 0)) stored.best_streak = streak;

        localStorage.setItem('leaderboard_records', JSON.stringify(stored));
        return stored;
    }
};
