/* Tab: Rewind — Машина времени */
window.Tab_rewind = {
    async render(el) {
        const res = await apiCall('/api/rewind').catch(() => ({ available_chapters: [], current_chapter: 1 }));
        const chapters = res.available_chapters || [];
        const current = res.current_chapter || 1;

        el.innerHTML = `
            <h2><i class="fas fa-hourglass-start"></i> Машина времени (Rewind)</h2>
            <div class="card" style="margin-bottom:16px;">
                <p style="color:var(--text-secondary);font-size:0.9rem;">
                    Вернись к любой пройденной главе и перепройди её. Цена — потеря воспоминаний учителя о событиях после выбранной главы.
                </p>
                <div style="margin-top:8px;color:var(--text-secondary);font-size:0.85rem;">
                    <strong>Текущая глава:</strong> ${current}<br>
                    <strong>Доступно для перемотки:</strong> ${chapters.length} глав
                </div>
            </div>
            <div class="card">
                <h3>Выбери главу для перемотки</h3>
                <div id="rewind-list" style="margin-top:12px;">
                    ${chapters.length
                        ? chapters.map(ch => `
                            <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);">
                                <span><strong>Глава ${ch.id}</strong> — ${ch.title}</span>
                                <button class="btn btn-sm btn-warning rewind-btn" data-ch="${ch.id}">
                                    \u21BA Перемотать к ${ch.id}
                                </button>
                            </div>
                        `).join('')
                        : '<p style="color:var(--text-secondary);">Нет пройденных глав для перемотки.</p>'
                    }
                </div>
                <div id="rewind-confirm" style="margin-top:16px;display:none;padding:12px;background:var(--bg-secondary);border-radius:6px;">
                    <p style="color:var(--warning);font-size:0.85rem;margin-bottom:12px;">
                        <strong>\u26A0 Внимание:</strong> перемотка сбросит прогресс в выбранной главе и всех последующих, а также удалит воспоминания учителя.
                    </p>
                    <button id="rewind-confirm-btn" class="btn btn-danger" style="margin-right:8px;">\u21BA Да, перемотать</button>
                    <button id="rewind-cancel-btn" class="btn btn-secondary">\u2715 Отмена</button>
                </div>
            </div>
        `;

        let selectedChapter = null;

        el.querySelectorAll('.rewind-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                selectedChapter = parseInt(btn.dataset.ch);
                const confirm = el.querySelector('#rewind-confirm');
                confirm.style.display = 'block';
                el.querySelector('#rewind-confirm-btn').onclick = async () => {
                    if (!selectedChapter) return;
                    const result = await apiCall('/api/rewind', {
                        method: 'POST',
                        body: JSON.stringify({ chapter: selectedChapter })
                    });
                    if (result.success) {
                        el.innerHTML = `
                            <h2><i class="fas fa-hourglass-start"></i> Машина времени (Rewind)</h2>
                            <div class="card" style="border-left:3px solid var(--success);">
                                <h3>\u2705 Перемотка завершена</h3>
                                <p style="color:var(--text-secondary);">${result.message}</p>
                                <button class="btn btn-primary" id="rewind-reload" style="margin-top:12px;">Обновить страницу</button>
                            </div>`;
                        el.querySelector('#rewind-reload')?.addEventListener('click', () => {
                            window.location.reload();
                        });
                    } else {
                        el.querySelector('#rewind-confirm').innerHTML = `
                            <p style="color:var(--error);">${result.message}</p>
                            <button id="rewind-retry" class="btn btn-secondary">\u21BB Повторить</button>`;
                        el.querySelector('#rewind-retry')?.addEventListener('click', () => this.render(el));
                    }
                };
                el.querySelector('#rewind-cancel-btn').onclick = () => {
                    selectedChapter = null;
                    el.querySelector('#rewind-confirm').style.display = 'none';
                };
            });
        });
    }
};
