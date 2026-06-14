/* Tab: Session Summary Generator */
window.Tab_summary = {
    async render(el) {
        el.innerHTML = `<h2><i class="fas fa-feather-alt"></i> Summary Generator</h2>
            <div class="card">
                <p style="color:var(--text-secondary);margin-bottom:12px;">Generate a structured summary on any topic using your knowledge base.</p>
                <div style="display:flex;gap:8px;">
                    <input type="text" id="summary-topic" class="input" placeholder="Topic (e.g. SQL injection, XSS, nmap)" style="flex:1;">
                    <button id="gen-summary" class="btn btn-primary">Generate</button>
                </div>
                <div id="summary-output" style="margin-top:12px;font-size:0.85rem;white-space:pre-wrap;max-height:500px;overflow-y:auto;"></div>
            </div>`;

        const input = el.querySelector('#summary-topic');
        const btn = el.querySelector('#gen-summary');
        const output = el.querySelector('#summary-output');

        const generate = async () => {
            const topic = input.value.trim();
            if (!topic) return;
            output.innerHTML = '<p class="loading">Generating summary...</p>';
            const res = await apiCall(`/api/summary?topic=${encodeURIComponent(topic)}`, { method: 'POST' }).catch(() => null);
            if (res && res.content) {
                output.innerHTML = `<div class="badge" style="margin-bottom:8px;">${res.topic}</div>${res.content.replace(/\n/g, '<br>')}`;
            } else {
                output.innerHTML = '<p style="color:var(--error);">Error generating summary</p>';
            }
        };

        btn.addEventListener('click', generate);
        input.addEventListener('keydown', e => { if (e.key === 'Enter') generate(); });
    }
};