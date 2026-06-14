/* Tab: Labs — with port URLs, task info, auto-polling */
window.Tab_labs = {
    _pollTimer: null,

    async render(el) {
        const labs = appState.labs || [];
        const containers = await apiCall('/docker_containers');
        const dockerStatus = await apiCall('/docker_status');

        el.innerHTML = `
            <h2>\uD83D\uDC33 \u041B\u0430\u0431\u043E\u0440\u0430\u0442\u043E\u0440\u0438\u0438</h2>
            <div class="card">
                <p>\uD83D\uDCE6 Docker: ${dockerStatus.available ? '<span style="color:var(--success)">\u0414\u043E\u0441\u0442\u0443\u043F\u0435\u043D</span>' : '<span style="color:var(--error)">\u041D\u0435\u0434\u043E\u0441\u0442\u0443\u043F\u0435\u043D</span>'}</p>
                <div id="runningContainers" style="display:flex; gap:8px; flex-wrap:wrap; margin-top:8px;">
                    ${(containers.containers || []).map(c => `
                        <div class="card" style="padding:8px 12px; min-width:120px; cursor:grab;"
                             draggable="true" data-container="${c.name}">
                            <strong>${c.name}</strong>
                            <div style="color:${c.status === 'running' ? 'var(--success)' : 'var(--error)'}; font-size:0.8rem;">${c.status}</div>
                            ${c.ports ? `<div style="font-size:0.75rem; color:var(--accent);">${Array.isArray(c.ports) ? c.ports.map(p => `<a href="${p}" target="_blank">\uD83D\uDD17 ${p}</a>`).join(' | ') : c.ports}</div>` : ''}
                        </div>
                    `).join('')}
                    ${!(containers.containers || []).length ? '<p style="color:var(--text-secondary);">\u041D\u0435\u0442 \u0437\u0430\u043F\u0443\u0449\u0435\u043D\u043D\u044B\u0445 \u043A\u043E\u043D\u0442\u0435\u0439\u043D\u0435\u0440\u043E\u0432</p>' : ''}
                </div>
            </div>

            <div id="labsDropZone" style="min-height:60px; border:2px dashed var(--border); border-radius:12px; padding:16px; margin:16px 0; text-align:center; color:var(--text-secondary); display:none;">
                \uD83D\uDCE4 \u041F\u0435\u0440\u0435\u0442\u0430\u0449\u0438\u0442\u0435 \u043A\u043E\u043D\u0442\u0435\u0439\u043D\u0435\u0440 \u0441\u044E\u0434\u0430 \u0434\u043B\u044F \u043E\u0441\u0442\u0430\u043D\u043E\u0432\u043A\u0438
            </div>

            <div class="grid-2" id="labsGrid">
                ${labs.map(l => `
                    <div class="card" data-lab="${l.id}" id="lab-${l.id}">
                        <h3>${l.name}</h3>
                        <p>${l.description || ''}</p>
                        <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                            <span class="badge">${l.difficulty || 'N/A'}</span>
                            <span style="font-size:0.8rem; color:var(--text-secondary);">${(l.tags || []).join(', ')}</span>
                        </div>
                        ${l.task ? `<div style="margin-top:8px; padding:8px; background:var(--bg); border-radius:8px; font-size:0.85rem;"><strong>\uD83D\uDCCC \u0417\u0430\u0434\u0430\u0447\u0430:</strong> ${l.task}</div>` : ''}
                        <div style="margin-top:12px; display:flex; gap:8px; flex-wrap:wrap;">
                            <button class="start-lab" data-lab="${l.id}">\u25B6 \u0417\u0430\u043F\u0443\u0441\u0442\u0438\u0442\u044C</button>
                            <button class="stop-lab" data-lab="${l.id}" style="background:var(--error);">\u25A0 \u041E\u0441\u0442\u0430\u043D\u043E\u0432\u0438\u0442\u044C</button>
                        </div>
                        <div class="lab-result" style="margin-top:8px;"></div>
                    </div>
                `).join('')}
            </div>
        `;

        el.querySelectorAll('.start-lab').forEach(btn => {
            btn.onclick = async () => {
                if (window.Sounds) Sounds.click();
                const labId = btn.dataset.lab;
                btn.disabled = true; btn.textContent = '\u23F3 \u0417\u0430\u043F\u0443\u0441\u043A...';
                const res = await apiCall(`/start_lab?lab_id=${labId}`, { method: 'POST' });
                btn.disabled = false;
                const resultDiv = btn.closest('.card').querySelector('.lab-result');
                if (res.status === 'ok') {
                    if (window.Sounds) Sounds.success();
                    resultDiv.innerHTML = `<div style="color:var(--success);">\u2705 \u0417\u0430\u043F\u0443\u0449\u0435\u043D\u043E</div>`;
                    if (res.ports) {
                        const ports = Array.isArray(res.ports) ? res.ports : [res.ports];
                        resultDiv.innerHTML += `<div style="margin-top:8px;"><strong>\uD83D\uDD17 \u0421\u0441\u044B\u043B\u043A\u0438:</strong><br>${ports.map(p => `<a href="${p}" target="_blank" style="display:inline-block;margin:4px;">${p}</a>`).join('')}</div>`;
                    }
                    if (res.container_id) {
                        resultDiv.innerHTML += `<div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">\uD83D\uDC33 ID: ${res.container_id.substring(0, 12)}</div>`;
                    }
                    if (res.message) {
                        resultDiv.innerHTML += `<div style="font-size:0.85rem;color:var(--text-secondary);margin-top:4px;">${res.message}</div>`;
                    }
                } else if (res.error) {
                    resultDiv.innerHTML = `<div style="color:var(--error);">\u274C ${res.error}</div>`;
                    if (window.Sounds) Sounds.error();
                }
                btn.textContent = '\u25B6 \u0417\u0430\u043F\u0443\u0441\u0442\u0438\u0442\u044C';
            };
        });

        el.querySelectorAll('.stop-lab').forEach(btn => {
            btn.onclick = async () => {
                if (window.Sounds) Sounds.click();
                const labId = btn.dataset.lab;
                await apiCall(`/stop_lab?lab_id=${labId}`, { method: 'POST' });
                const resultDiv = btn.closest('.card').querySelector('.lab-result');
                resultDiv.innerHTML = `<div style="color:var(--text-secondary);">\u25A0 \u041E\u0441\u0442\u0430\u043D\u043E\u0432\u043B\u0435\u043D\u043E</div>`;
                if (window.Sounds) Sounds.notification();
                this._pollContainers(el);
            };
        });

        this._initDragDrop(el);
        this._startPolling(el);
    },

    _startPolling(el) {
        if (this._pollTimer) clearInterval(this._pollTimer);
        this._pollTimer = setInterval(() => this._pollContainers(el), 10000);
    },

    async _pollContainers(el) {
        const containers = await apiCall('/docker_containers');
        const zone = el.querySelector('#runningContainers');
        if (!zone) return;
        const items = containers.containers || [];
        if (!items.length) {
            zone.innerHTML = '<p style="color:var(--text-secondary);">\u041D\u0435\u0442 \u0437\u0430\u043F\u0443\u0449\u0435\u043D\u043D\u044B\u0445 \u043A\u043E\u043D\u0442\u0435\u0439\u043D\u0435\u0440\u043E\u0432</p>';
            return;
        }
        zone.innerHTML = items.map(c => `
            <div class="card" style="padding:8px 12px; min-width:120px; cursor:grab;"
                 draggable="true" data-container="${c.name}">
                <strong>${c.name}</strong>
                <div style="color:${c.status === 'running' ? 'var(--success)' : 'var(--error)'}; font-size:0.8rem;">${c.status}</div>
                ${c.ports ? `<div style="font-size:0.75rem; color:var(--accent);">${Array.isArray(c.ports) ? c.ports.map(p => `<a href="${p}" target="_blank">\uD83D\uDD17</a>`).join(' | ') : c.ports}</div>` : ''}
            </div>
        `).join('');
    },

    _initDragDrop(el) {
        const draggables = el.querySelectorAll('[draggable="true"]');
        const dropZone = el.querySelector('#labsDropZone');
        if (!dropZone || !draggables.length) return;
        draggables.forEach(item => {
            item.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', item.dataset.container);
                item.style.opacity = '0.5';
                dropZone.style.display = 'block';
            });
            item.addEventListener('dragend', () => {
                item.style.opacity = '1';
                dropZone.style.display = 'none';
            });
        });
        dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.style.borderColor = 'var(--accent)'; dropZone.style.background = 'rgba(0,180,216,0.05)'; });
        dropZone.addEventListener('dragleave', () => { dropZone.style.borderColor = 'var(--border)'; dropZone.style.background = ''; });
        dropZone.addEventListener('drop', async (e) => {
            e.preventDefault();
            dropZone.style.borderColor = 'var(--border)';
            dropZone.style.background = '';
            const containerName = e.dataTransfer.getData('text/plain');
            if (containerName) {
                if (window.Sounds) Sounds.notification();
                await apiCall(`/stop_lab?lab_id=${containerName.replace('-web', '')}`, { method: 'POST' });
                this._pollContainers(el);
            }
        });
    }
};
