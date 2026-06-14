/* Tab: Code Sandbox */
window.Tab_sandbox = {
    async render(el) {
        el.innerHTML = `
            <h2><i class="fas fa-shield-halved"></i> Code Sandbox</h2>
            <div class="card">
                <div style="display:flex;gap:8px;margin-bottom:8px;align-items:center;">
                    <select id="sandbox-lang" class="input" style="width:120px;">
                        <option value="python">Python</option>
                        <option value="bash">Bash</option>
                    </select>
                    <input type="number" id="sandbox-timeout" class="input" value="10" min="1" max="60" style="width:80px;" title="Timeout (s)">
                    <button id="sandbox-run" class="btn btn-primary">Run</button>
                </div>
                <textarea id="sandbox-code" class="input" style="width:100%;min-height:200px;font-family:monospace;font-size:0.85rem;" placeholder="print('Hello, CyberTeacher!')"></textarea>
                <div id="sandbox-output" style="margin-top:12px;font-size:0.85rem;"></div>
            </div>
        `;
        const runBtn = el.querySelector('#sandbox-run');
        const codeInput = el.querySelector('#sandbox-code');
        const langSelect = el.querySelector('#sandbox-lang');
        const timeoutInput = el.querySelector('#sandbox-timeout');
        const output = el.querySelector('#sandbox-output');

        runBtn.addEventListener('click', async () => {
            const code = codeInput.value.trim();
            if (!code) return;
            output.innerHTML = '<p class="loading">Running in sandbox...</p>';
            const res = await apiCall('/api/sandbox/run', {
                method: 'POST',
                body: JSON.stringify({
                    code,
                    language: langSelect.value,
                    timeout: parseInt(timeoutInput.value) || 10
                }),
                headers: { 'Content-Type': 'application/json' }
            }).catch(() => null);
            if (!res) {
                output.innerHTML = '<p style="color:var(--error);">Error: no response</p>';
                return;
            }
            if (!res.success) {
                output.innerHTML = `<p style="color:var(--error);">Error: ${res.error || 'Unknown'}</p>`;
                return;
            }
            const outParts = [];
            if (res.stdout) outParts.push(`<pre style="background:var(--bg);padding:12px;border-radius:6px;overflow-x:auto;margin:0;">${res.stdout}</pre>`);
            if (res.stderr) outParts.push(`<pre style="background:var(--bg);padding:12px;border-radius:6px;overflow-x:auto;margin:8px 0 0;color:var(--error);">${res.stderr}</pre>`);
            outParts.push(`<div style="font-size:0.75rem;color:var(--text-secondary);margin-top:6px;">Exit code: ${res.returncode}</div>`);
            output.innerHTML = outParts.join('');
        });
    }
};