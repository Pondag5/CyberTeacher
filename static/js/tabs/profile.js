/* Tab: Profile (with auth, radar chart) */
window.Tab_profile = {
    async render(el) {
        const token = localStorage.getItem('auth_token');
        if (!token) {
            this._renderAuth(el);
            return;
        }
        const profile = await apiCall(`/verify_auth?token=${encodeURIComponent(token)}`);
        if (profile.error || !profile.valid) {
            localStorage.removeItem('auth_token');
            this._renderAuth(el);
            return;
        }
        this._renderProfile(el, profile.user);
    },

    _renderAuth(el) {
        el.innerHTML = `
            <h2>\uD83D\uDD10 \u0412\u0445\u043E\u0434 / \u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044F</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>\u0412\u043E\u0439\u0442\u0438</h3>
                    <p><input id="loginUser" placeholder="\u0418\u043C\u044F \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044F"></p>
                    <p><input id="loginPass" type="password" placeholder="\u041F\u0430\u0440\u043E\u043B\u044C"></p>
                    <button id="loginBtn">\u0412\u043E\u0439\u0442\u0438</button>
                    <div id="loginError" style="color:var(--error); margin-top:8px;"></div>
                </div>
                <div class="card">
                    <h3>\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044F</h3>
                    <p><input id="regUser" placeholder="\u0418\u043C\u044F \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044F"></p>
                    <p><input id="regName" placeholder="\u041E\u0442\u043E\u0431\u0440\u0430\u0437\u0438\u0442\u0435\u043B\u044C\u043D\u043E\u0435 \u0438\u043C\u044F"></p>
                    <p><input id="regPass" type="password" placeholder="\u041F\u0430\u0440\u043E\u043B\u044C"></p>
                    <button id="regBtn">\u0421\u043E\u0437\u0434\u0430\u0442\u044C \u0430\u043A\u043A\u0430\u0443\u043D\u0442</button>
                    <div id="regError" style="color:var(--error); margin-top:8px;"></div>
                    <div id="regSuccess" style="color:var(--success); margin-top:8px;"></div>
                </div>
            </div>
        `;
        document.getElementById('loginBtn').onclick = async () => {
            const u = document.getElementById('loginUser').value;
            const p = document.getElementById('loginPass').value;
            const res = await apiCall(`/login?username=${encodeURIComponent(u)}&password=${encodeURIComponent(p)}`, { method: 'POST' });
            if (res.error) { document.getElementById('loginError').innerText = res.message || 'Ошибка входа'; return; }
            if (res.token) {
                localStorage.setItem('auth_token', res.token);
                if (res.display_name) { appState.username = res.display_name; appState.avatar = res.avatar || '\uD83E\uDDD1\u200D\uD83D\uDCBB'; renderUserInfo(); }
                this.render(el);
                if (window.Sounds) Sounds.success();
            }
        };
        document.getElementById('regBtn').onclick = async () => {
            const u = document.getElementById('regUser').value;
            const n = document.getElementById('regName').value;
            const p = document.getElementById('regPass').value;
            const res = await apiCall(`/register?username=${encodeURIComponent(u)}&password=${encodeURIComponent(p)}&display_name=${encodeURIComponent(n)}`, { method: 'POST' });
            if (res.error) { document.getElementById('regError').innerText = res.message || 'Ошибка регистрации'; return; }
            document.getElementById('regSuccess').innerText = '\u0410\u043A\u043A\u0430\u0443\u043D\u0442 \u0441\u043E\u0437\u0434\u0430\u043D! \u0412\u043E\u0439\u0434\u0438\u0442\u0435.';
            if (window.Sounds) Sounds.notification();
        };
    },

    _renderProfile(el, user) {
        el.innerHTML = `
            <h2>\uD83D\uDC64 \u041F\u0440\u043E\u0444\u0438\u043B\u044C</h2>
            <div class="card">
                <p>\uD83E\uDDD1\u200D\uD83D\uDCBB <strong>${user.display_name || user.username}</strong> (${user.user_id})</p>
                <p>\u0414\u043E\u043B\u0436\u043D\u043E\u0441\u0442\u044C: <span class="badge">${user.role || 'user'}</span></p>
                <p>\u0421\u043E\u0437\u0434\u0430\u043D: ${new Date((user.created_at || 0) * 1000).toLocaleDateString()}</p>
                <div style="margin-top:12px; display:flex; gap:8px;">
                    <button id="logoutBtn" style="background:var(--error);">\u0412\u044B\u0439\u0442\u0438</button>
                </div>
            </div>
            <div class="card"><h3>\uD83C\uDFC6 \u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043A\u0430</h3>XP: ${appState.xp} | \u0423\u0440\u043E\u0432\u0435\u043D\u044C: ${appState.level} | \u0420\u0435\u043F\u0443\u0442\u0430\u0446\u0438\u044F: ${appState.reputation}</div>
            <div class="card"><h3>\uD83D\uDCCA \u041D\u0430\u0432\u044B\u043A\u0438</h3><div id="radarChart"></div></div>
        `;
        document.getElementById('logoutBtn').onclick = () => {
            localStorage.removeItem('auth_token');
            appState.username = '\u0410\u043D\u043E\u043D\u0438\u043C';
            appState.avatar = '\uD83E\uDDD1\u200D\uD83D\uDCBB';
            renderUserInfo();
            this.render(el);
        };
        // Render radar chart
        const radarEl = document.getElementById('radarChart');
        if (radarEl && appState.skills && appState.skills.length) {
            this._renderRadar(radarEl, appState.skills);
        } else if (radarEl) {
            radarEl.innerHTML = '<div style="color:var(--text-secondary)">\u041D\u0435\u0442 \u0434\u0430\u043D\u043D\u044B\u0445</div>';
        }
    },

    _renderRadar(el, skills) {
        const cx = 120, cy = 120, r = 90;
        const n = Math.min(skills.length, 6);
        if (n < 3) { el.innerHTML = '<div style="color:var(--text-secondary)">\u041C\u0438\u043D\u0438\u043C\u0443\u043C 3 \u043D\u0430\u0432\u044B\u043A\u0430 \u0434\u043B\u044F \u0433\u0440\u0430\u0444\u0438\u043A\u0430</div>'; return; }

        const angleStep = (2 * Math.PI) / n;
        let svg = `<svg width="240" height="240" viewBox="0 0 240 240">`;

        // Grid circles
        for (let level = 1; level <= 5; level++) {
            const gr = (level / 5) * r;
            svg += `<circle cx="${cx}" cy="${cy}" r="${gr}" fill="none" stroke="var(--border)" stroke-width="0.5"/>`;
        }

        // Axes + labels
        const points = [];
        skills.slice(0, n).forEach((s, i) => {
            const angle = i * angleStep - Math.PI / 2;
            const x = cx + r * Math.cos(angle);
            const y = cy + r * Math.sin(angle);
            svg += `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="var(--border)" stroke-width="0.5"/>`;
            const lx = cx + (r + 15) * Math.cos(angle);
            const ly = cy + (r + 15) * Math.sin(angle);
            const label = (s.name || s.id || '').slice(0, 8);
            svg += `<text x="${lx}" y="${ly}" text-anchor="middle" fill="var(--text-secondary)" font-size="9" font-family="Inter">${label}</text>`;
            const level = s.level || 0;
            const px = cx + (level / 5) * r * Math.cos(angle);
            const py = cy + (level / 5) * r * Math.sin(angle);
            points.push(`${px},${py}`);
        });

        // Data polygon
        svg += `<polygon points="${points.join(' ')}" fill="var(--accent)" fill-opacity="0.2" stroke="var(--accent)" stroke-width="2"/>`;

        // Data points
        points.forEach(p => {
            const [px, py] = p.split(',');
            svg += `<circle cx="${px}" cy="${py}" r="3" fill="var(--accent)"/>`;
        });

        svg += '</svg>';
        el.innerHTML = svg;
    }
};
