/* Tab: Courses — with topic list after selection */
window.Tab_courses = {
    async render(el) {
        const courses = appState.courses || [];
        el.innerHTML = `<h2>\uD83D\uDCDA \u041A\u0443\u0440\u0441\u044B</h2><div class="grid-2">${courses.map(c => `
            <div class="card" ${c.active ? 'style="border:2px solid var(--accent);"' : ''}>
                <h3>${c.icon || '\uD83D\uDCD6'} ${c.name}</h3>
                <p>${c.description || ''}</p>
                <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
                    <span>\u041F\u0440\u043E\u0433\u0440\u0435\u0441\u0441: ${c.progress || 0}%</span>
                    ${c.topics_count ? `<span style="font-size:0.8rem;color:var(--text-secondary);">${c.topics_count} \u0442\u0435\u043C</span>` : ''}
                    ${c.duration ? `<span style="font-size:0.8rem;color:var(--text-secondary);">${c.duration}</span>` : ''}
                </div>
                <button data-course="${c.id}" class="select-course">${c.active ? '\u2705 \u0410\u043A\u0442\u0438\u0432\u0435\u043D' : '\u0412\u044B\u0431\u0440\u0430\u0442\u044C'}</button>
            </div>
        `).join('')}</div>`;
        el.querySelectorAll('.select-course').forEach(btn => {
            btn.onclick = async () => {
                btn.disabled = true;
                btn.textContent = '\u0417\u0430\u0433\u0440\u0443\u0437\u043A\u0430...';
                await apiCall(`/select_course?course_id=${encodeURIComponent(btn.dataset.course)}`, { method: 'POST' });
                await loadInitialData();
                const selected = appState.courses.find(c => c.active);
                if (selected) {
                    await this._showCourseTopics(el, selected);
                } else {
                    this.render(el);
                }
                if (window.Sounds) Sounds.success();
            };
        });
        const active = courses.find(c => c.active);
        if (active) this._showCourseTopics(el, active);
    },

    async _showCourseTopics(el, course) {
        const oldCard = el.querySelector(`[data-course="${course.id}"]`);
        let topics = course.topics || [];
        if (!topics.length && course.id) {
            const res = await apiCall(`/get_courses`);
            const found = (res.courses || []).find(c => c.id === course.id);
            if (found) topics = found.topics || [];
        }
        if (!topics.length) return;
        const done = Array.isArray(course.progress) ? course.progress : [];
        let topicsHtml = topics.map((t, i) => {
            const completed = done.includes(t.id || t) || done.includes(i);
            return `<div class="card" style="padding:10px 16px; margin:6px 0; ${completed ? 'opacity:0.6;' : ''}">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:1.2rem;">${completed ? '\u2705' : '\uD83D\uDCD6'}</span>
                    <div><strong>${t.title || t.name || t}</strong>
                    ${t.description ? `<div style="font-size:0.85rem;color:var(--text-secondary);">${t.description}</div>` : ''}</div>
                </div>
            </div>`;
        }).join('');
        const container = document.createElement('div');
        container.id = 'courseTopics';
        container.style.cssText = 'margin-top:20px;';
        container.innerHTML = `<h3 style="margin-bottom:12px;">\uD83D\uDCCB \u0422\u0435\u043C\u044B \u043A\u0443\u0440\u0441\u0430: ${course.name}</h3>${topicsHtml}`;
        const existing = el.querySelector('#courseTopics');
        if (existing) existing.replaceWith(container);
        else el.appendChild(container);
    }
};
