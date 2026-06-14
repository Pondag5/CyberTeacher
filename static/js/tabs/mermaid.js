/* Tab: Mermaid Diagram Generator */
window.Tab_mermaid = {
    async render(el) {
        el.innerHTML = `<h2><i class="fas fa-diagram-project"></i> Mermaid Generator</h2>
            <div class="card">
                <p style="color:var(--text-secondary);font-size:0.85rem;margin-bottom:8px;">Generate Mermaid diagrams for cybersecurity topics using LLM.</p>
                <div style="display:flex;gap:8px;">
                    <input type="text" id="mermaid-topic" class="input" placeholder="Topic (e.g. XSS attack flow)" style="flex:1;">
                    <button id="mermaid-gen" class="btn btn-primary">Generate</button>
                </div>
                <div id="mermaid-output" style="margin-top:12px;"></div>
            </div>`;

        const input = el.querySelector('#mermaid-topic');
        const btn = el.querySelector('#mermaid-gen');
        const output = el.querySelector('#mermaid-output');

        btn.addEventListener('click', async () => {
            const topic = input.value.trim();
            if (!topic) return;
            output.innerHTML = '<p class="loading">Generating diagram...</p>';
            const res = await apiCall(`/api/mermaid/generate?topic=${encodeURIComponent(topic)}`).catch(() => null);
            if (res && res.diagram) {
                output.innerHTML = `<pre style="background:var(--bg);padding:16px;border-radius:8px;font-size:0.8rem;overflow-x:auto;white-space:pre-wrap;max-height:400px;overflow-y:auto;">${res.diagram}</pre>
                    <button id="mermaid-copy" class="btn btn-sm" style="margin-top:8px;">Copy to clipboard</button>`;
                el.querySelector('#mermaid-copy').addEventListener('click', () => {
                    navigator.clipboard.writeText(res.diagram).catch(() => {});
                });
            } else {
                output.innerHTML = '<p style="color:var(--error);">Error generating diagram</p>';
            }
        });
    }
};