/* Tab: Admin — user management, role assignment, course management */
window.Tab_admin = {
    _token: null,

    async render(el) {
        const token = localStorage.getItem('auth_token');
        if (!token) {
            el.innerHTML = '<div class="card">\u0414\u043B\u044F \u0434\u043E\u0441\u0442\u0443\u043F\u0430 \u043D\u0443\u0436\u0435\u043D \u0432\u0445\u043E\u043D \u043F\u043E\u0434 \u0430\u0434\u043C\u0438\u043D\u0438\u0441\u0442\u0440\u0430\u0442\u043E\u0440\u0441\u043A\u043E\u0439 \u0443\u0447\u0451\u0442\u043A\u043E\u0439. \u041F\u0435\u0440\u0435\u0439\u0434\u0438\u0442\u0435 \u0432 \u041F\u0440\u043E\u0444\u0438\u043B\u044C.</div>';
            return;
        }

        this._token = token;
        const [usersData, coursesData] = await Promise.all([
            apiCall(`/list_users?token=${encodeURIComponent(token)}`),
            apiCall('/get_courses'),
        ]);

        if (usersData.error) {
            el.innerHTML = `<div class="card" style="color:var(--error);">\u26A0\uFE0F ${usersData.error || '\u041D\u0435\u0442 \u0434\u043E\u0441\u0442\u0443\u043F\u0430 (admin only)'}</div>`;
            return;
        }

        const users = usersData.users || [];
        const courses = coursesData.courses || [];

        el.innerHTML = `
            <h2>\u2699\uFE0F \u041F\u0430\u043D\u0435\u043B\u044C \u0443\u043F\u0440\u0430\u0432\u043B\u0435\u043D\u0438\u044F</h2>

            <div class="grid-2">
                <div class="card">
                    <h3>\uD83D\uDC65 \u041F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0438 (${users.length})</h3>
                    <div style="max-height:300px; overflow-y:auto;">
                        <table style="width:100%; border-collapse:collapse;">
                            <tr style="border-bottom:1px solid var(--border); text-align:left;">
                                <th style="padding:6px;">\u0418\u043C\u044F</th>
                                <th style="padding:6px;">\u0420\u043E\u043B\u044C</th>
                                <th style="padding:6px;">\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u044F</th>
                            </tr>
                            ${users.map(u => `
                                <tr style="border-bottom:1px solid var(--border);">
                                    <td style="padding:6px;">${u.avatar || '\uD83E\uDDD1\u200D\uD83D\uDCBB'} ${u.display_name || u.username}</td>
                                    <td style="padding:6px;"><span class="badge">${u.role || 'student'}</span></td>
                                    <td style="padding:6px;">
                                        <select class="role-select" data-user="${u.username}" style="background:var(--bg-primary); border:1px solid var(--border); color:var(--text-primary); padding:4px 8px; border-radius:8px;">
                                            <option value="student" ${u.role === 'student' ? 'selected' : ''}>student</option>
                                            <option value="teacher" ${u.role === 'teacher' ? 'selected' : ''}>teacher</option>
                                            <option value="admin" ${u.role === 'admin' ? 'selected' : ''}>admin</option>
                                        </select>
                                    </td>
                                </tr>
                            `).join('')}
                        </table>
                    </div>
                </div>

                <div class="card">
                    <h3>\uD83D\uDCDA \u041A\u0443\u0440\u0441\u044B (${courses.length})</h3>
                    <div style="max-height:300px; overflow-y:auto;">
                        ${courses.map(c => `
                            <div style="padding:8px 0; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
                                <div>${c.icon || '\uD83D\uDCDA'} <strong>${c.name}</strong> <span class="badge">${c.difficulty}</span></div>
                                <div style="font-size:0.8rem; color:var(--text-secondary);">${(c.topics || []).length} \u0442\u0435\u043C</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>

            <div class="card">
                <h3>\u2795 \u0421\u043E\u0437\u0434\u0430\u0442\u044C \u043A\u0443\u0440\u0441</h3>
                <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:end;">
                    <input id="newCourseName" placeholder="\u041D\u0430\u0437\u0432\u0430\u043D\u0438\u0435">
                    <input id="newCourseDesc" placeholder="\u041E\u043F\u0438\u0441\u0430\u043D\u0438\u0435" style="flex:1;">
                    <select id="newCourseDiff" style="width:120px;">
                        <option value="beginner">beginner</option>
                        <option value="intermediate">intermediate</option>
                        <option value="advanced">advanced</option>
                        <option value="expert">expert</option>
                    </select>
                    <button id="createCourseBtn">\u0421\u043E\u0437\u0434\u0430\u0442\u044C</button>
                </div>
                <div id="courseResult" style="margin-top:8px;"></div>
            </div>
        `;

        // Role change handlers
        el.querySelectorAll('.role-select').forEach(sel => {
            sel.addEventListener('change', async () => {
                const username = sel.dataset.user;
                const role = sel.value;
                const res = await apiCall('/set_role', {
                    method: 'POST',
                    body: JSON.stringify({ token, target_user: username, role })
                });
                if (res.error) {
                    document.getElementById('courseResult').innerHTML = `<span style="color:var(--error);">\u2717 ${res.error}</span>`;
                } else {
                    document.getElementById('courseResult').innerHTML = `<span style="color:var(--success);">\u2705 ${username} \u2014 \u0440\u043E\u043B\u044C: ${role}</span>`;
                    if (window.Sounds) Sounds.notification();
                }
            });
        });

        // Course creation
        document.getElementById('createCourseBtn').onclick = async () => {
            const name = document.getElementById('newCourseName').value;
            const desc = document.getElementById('newCourseDesc').value;
            const diff = document.getElementById('newCourseDiff').value;
            if (!name) return;
            const res = await apiCall('/create_course', {
                method: 'POST',
                body: JSON.stringify({ token, name, description: desc, difficulty: diff })
            });
            if (res.error) {
                document.getElementById('courseResult').innerHTML = `<span style="color:var(--error);">\u2717 ${res.error}</span>`;
            } else {
                document.getElementById('courseResult').innerHTML = `<span style="color:var(--success);">\u2705 \u041A\u0443\u0440\u0441 \u0441\u043E\u0437\u0434\u0430\u043D: ${res.name}</span>`;
                if (window.Sounds) Sounds.success();
                document.getElementById('newCourseName').value = '';
                document.getElementById('newCourseDesc').value = '';
                this.render(el);
            }
        };
    }
};
