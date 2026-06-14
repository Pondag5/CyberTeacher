/* Tab: External Labs — HackTheBox + TryHackMe */
window.Tab_labs_external = {
    async render(el) {
        el.innerHTML = `
            <h2><i class="fas fa-server"></i> External Labs</h2>
            <div class="grid-2" style="margin-top:12px;">
                <div class="card">
                    <h3><i class="fas fa-cube"></i> HackTheBox</h3>
                    <div style="display:flex;gap:8px;margin-bottom:12px;">
                        <button id="htb-machines-btn" class="btn btn-primary">Machines</button>
                        <button id="htb-status-btn" class="btn btn-sm">Status</button>
                    </div>
                    <div id="htb-result"></div>
                </div>
                <div class="card">
                    <h3><i class="fas fa-graduation-cap"></i> TryHackMe</h3>
                    <div style="display:flex;gap:8px;margin-bottom:12px;">
                        <button id="thm-rooms-btn" class="btn btn-primary">Rooms</button>
                        <button id="thm-status-btn" class="btn btn-sm">Status</button>
                    </div>
                    <div id="thm-result"></div>
                </div>
            </div>
        `;
        this.setupHTB(el);
        this.setupTHM(el);
    },

    setupHTB(el) {
        const result = el.querySelector('#htb-result');
        el.querySelector('#htb-machines-btn').addEventListener('click', async () => {
            result.innerHTML = '<p class="loading">Loading machines...</p>';
            const res = await apiCall('/api/htb/machines').catch(() => null);
            if (!res || !res.machines?.length) {
                result.innerHTML = '<p style="color:var(--text-secondary);">No machines or API error</p>';
                return;
            }
            result.innerHTML = `<p style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:8px;">Total: ${res.total} machines</p>
                <div style="max-height:400px;overflow-y:auto;">${res.machines.slice(0, 30).map(m => {
                    const diffColor = m.difficulty === 'Easy' ? 'var(--success)' : m.difficulty === 'Medium' ? 'var(--warning)' : 'var(--error)';
                    return `<div class="card htb-machine" data-id="${m.id}" style="padding:8px;margin-bottom:4px;background:var(--bg);cursor:pointer;">
                        <div style="display:flex;justify-content:space-between;">
                            <strong>${m.name || 'Unknown'}</strong>
                            <span class="badge" style="background:${diffColor};">${m.difficulty || '?'}</span>
                        </div>
                        <div style="font-size:0.75rem;color:var(--text-secondary);">${m.os || ''} | Points: ${m.points || 0}</div>
                    </div>`;
                }).join('')}</div>`;

            result.querySelectorAll('.htb-machine').forEach(card => {
                card.addEventListener('click', async () => {
                    const id = card.dataset.id;
                    const oldHtml = card.innerHTML;
                    card.innerHTML = '<p class="loading">Loading...</p>';
                    const detail = await apiCall(`/api/htb/machine/${id}`).catch(() => null);
                    card.innerHTML = oldHtml;
                    if (detail && detail.machine) {
                        const m = detail.machine;
                        const detailDiv = document.createElement('div');
                        detailDiv.className = 'card';
                        detailDiv.style.cssText = 'padding:12px;margin-top:8px;background:var(--bg);font-size:0.85rem;';
                        detailDiv.innerHTML = `
                            <strong>${m.name}</strong>
                            <div>OS: ${m.os || 'N/A'}</div>
                            <div>Difficulty: ${m.difficulty || 'N/A'}</div>
                            <div>Points: ${m.points || 'N/A'}</div>
                            <div>Rating: ${m.rating?.average || 'N/A'}</div>
                            <div>Status: ${m.status || 'N/A'}</div>
                            <div style="margin-top:6px;">${m.description || ''}</div>
                            ${m.hints?.length ? `<details style="margin-top:8px;"><summary>Hints (${m.hints.length})</summary>${m.hints.map(h => `<div style="margin:4px 0;">• ${h.text || ''}</div>`).join('')}</details>` : ''}
                            <button class="btn btn-sm" style="margin-top:8px;" onclick="this.closest('.card').remove()">Close</button>
                        `;
                        card.after(detailDiv);
                    }
                });
            });
        });

        el.querySelector('#htb-status-btn').addEventListener('click', async () => {
            result.innerHTML = '<p class="loading">Loading status...</p>';
            const res = await apiCall('/api/htb/status').catch(() => null);
            result.innerHTML = res ? '<p style="color:var(--success);">Status loaded (check console/CLI)</p>' : '<p style="color:var(--error);">Error</p>';
        });
    },

    setupTHM(el) {
        const result = el.querySelector('#thm-result');
        el.querySelector('#thm-rooms-btn').addEventListener('click', async () => {
            result.innerHTML = '<p class="loading">Loading rooms...</p>';
            const res = await apiCall('/api/thm/rooms').catch(() => null);
            if (!res || !res.rooms?.length) {
                result.innerHTML = '<p style="color:var(--text-secondary);">No rooms or API error</p>';
                return;
            }
            result.innerHTML = `<p style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:8px;">Total: ${res.total} rooms</p>
                <div style="max-height:400px;overflow-y:auto;">${res.rooms.slice(0, 30).map(r => {
                    const diffColor = r.difficulty === 'Easy' ? 'var(--success)' : r.difficulty === 'Medium' ? 'var(--warning)' : 'var(--error)';
                    return `<div class="thm-room" data-id="${r.id}" style="padding:8px;margin-bottom:4px;background:var(--bg);cursor:pointer;border-radius:6px;">
                        <div style="display:flex;justify-content:space-between;">
                            <strong>${r.title || 'Unknown'}</strong>
                            <span class="badge" style="background:${diffColor};">${r.difficulty || '?'}</span>
                        </div>
                        <div style="font-size:0.75rem;color:var(--text-secondary);">${r.type || ''} | Users: ${r.user_count || 0}</div>
                    </div>`;
                }).join('')}</div>`;

            result.querySelectorAll('.thm-room').forEach(card => {
                card.addEventListener('click', async () => {
                    const id = card.dataset.id;
                    card.innerHTML = '<p class="loading">Loading...</p>';
                    const detail = await apiCall(`/api/thm/room/${id}`).catch(() => null);
                    if (detail && detail.room) {
                        const r = detail.room;
                        card.innerHTML = `
                            <div class="card" style="padding:12px;background:var(--bg);">
                                <strong>${r.title || 'Unknown'}</strong>
                                <div style="font-size:0.85rem;margin-top:6px;">${r.description || ''}</div>
                                <div style="font-size:0.8rem;color:var(--text-secondary);margin-top:6px;">
                                    Type: ${r.type || 'N/A'} | Difficulty: ${r.difficulty || 'N/A'} | Rating: ${r.rating || 'N/A'}/5
                                </div>
                                ${r.tasks?.length ? `<details style="margin-top:8px;"><summary>Tasks (${r.tasks.length})</summary>${r.tasks.slice(0, 10).map(t => `<div style="margin:4px 0;font-size:0.8rem;">• ${t.title || 'Untitled'}</div>`).join('')}</details>` : ''}
                                <button class="btn btn-sm" style="margin-top:8px;" onclick="this.closest('.card').remove()">Close</button>
                            </div>
                        `;
                    } else {
                        card.innerHTML = '<p style="color:var(--error);">Room not found</p>';
                    }
                });
            });
        });

        el.querySelector('#thm-status-btn').addEventListener('click', async () => {
            result.innerHTML = '<p class="loading">Loading status...</p>';
            const res = await apiCall('/api/thm/status').catch(() => null);
            if (!res || res.error) {
                result.innerHTML = '<p style="color:var(--error);">Not authenticated</p>';
                return;
            }
            result.innerHTML = `
                <div class="card" style="padding:12px;background:var(--bg);">
                    <div>Username: <strong>${res.username || 'N/A'}</strong></div>
                    <div>Rank: ${res.rank || 'N/A'} | Level: ${res.level || 0}</div>
                    <div>Points: ${res.points || 0} | Streak: ${res.streak || 0} days</div>
                    <div>Rooms completed: ${res.rooms_completed || 0} | Badges: ${res.badges || 0}</div>
                </div>
            `;
        });
    }
};