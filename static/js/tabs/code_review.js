/* Tab: Code Review */
window.Tab_code_review = {
    async render(el) {
        el.innerHTML = `<h2><i class="fas fa-code"></i> Code Review</h2>
            <div class="card">
                <div style="display:flex;gap:8px;margin-bottom:8px;align-items:center;">
                    <select id="cr-lang" class="input" style="width:120px;">
                        <option value="python">Python</option>
                        <option value="javascript">JavaScript</option>
                        <option value="cpp">C++</option>
                        <option value="go">Go</option>
                    </select>
                    <button id="cr-scan" class="btn btn-primary">Scan Code</button>
                </div>
                <textarea id="cr-code" class="input" style="width:100%;min-height:200px;font-family:monospace;font-size:0.85rem;" placeholder="Paste code for security review..."></textarea>
                <div id="cr-output" style="margin-top:12px;"></div>
            </div>`;

        const runBtn = el.querySelector('#cr-scan');
        const codeInput = el.querySelector('#cr-code');
        const langSelect = el.querySelector('#cr-lang');
        const output = el.querySelector('#cr-output');

        runBtn.addEventListener('click', async () => {
            const code = codeInput.value.trim();
            if (!code) return;
            output.innerHTML = '<p class="loading">Scanning code...</p>';
            const res = await apiCall('/api/scanv2', {
                method: 'POST',
                body: JSON.stringify({ code, language: langSelect.value }),
                headers: { 'Content-Type': 'application/json' }
            }).catch(() => null);
            if (!res) {
                output.innerHTML = '<p style="color:var(--error);">Error scanning code</p>';
                return;
            }
            const issues = res.issues || res.results || [];
            const summary = res.summary || {};
            let html = '';
            if (summary.critical || summary.high) {
                html += `<div style="margin-bottom:8px;">Critical: ${summary.critical || 0} | High: ${summary.high || 0} | Medium: ${summary.medium || 0} | Low: ${summary.low || 0}</div>`;
            }
            if (Array.isArray(issues) && issues.length) {
                html += issues.slice(0, 30).map((issue: any) => `
                    <div class="card" style="padding:8px;margin-bottom:4px;background:var(--bg);font-size:0.85rem;">
                        <div style="display:flex;justify-content:space-between;">
                            <strong>${issue.title || issue.rule || issue.type || 'Issue'}</strong>
                            <span class="badge" style="background:${issue.severity === 'critical' || issue.severity === 'high' ? 'var(--error)' : 'var(--warning)'};">${issue.severity || 'info'}</span>
                        </div>
                        ${issue.message || issue.description ? `<div style="margin-top:4px;">${issue.message || issue.description}</div>` : ''}
                        ${issue.line ? `<div style="font-size:0.75rem;color:var(--text-secondary);margin-top:4px;">Line ${issue.line}${issue.col ? ':' + issue.col : ''}</div>` : ''}
                    </div>
                `).join('');
            } else {
                html = '<p style="color:var(--text-secondary);">No issues found</p>';
            }
            if (res.output || res.stdout) {
                html += `<pre style="background:var(--bg);padding:12px;border-radius:6px;margin-top:8px;font-size:0.8rem;overflow-x:auto;">${(res.output || res.stdout || '').substring(0, 2000)}</pre>`;
            }
            output.innerHTML = html;
        });
    }
};