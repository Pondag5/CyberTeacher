/* Risk indicators: noise, trace, debt */
function renderRiskIndicators(container) {
    container.innerHTML = `
        <div class="card" style="padding:12px;">
            <h3 style="margin-bottom:8px;">\uD83D\uDCCA Risk Status</h3>
            <div id="noise-indicator" style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between;">
                    <span>\uD83D\uDCF4 Noise</span>
                    <span id="noise-value">0%</span>
                </div>
                <div style="height:8px; background:var(--bg-secondary); border-radius:4px; overflow:hidden;">
                    <div id="noise-bar" style="width:0%; height:100%; background:var(--success); border-radius:4px; transition: width 0.5s;"></div>
                </div>
            </div>
            <div id="trace-indicator" style="margin-bottom:8px; display:none;">
                <div style="display:flex; justify-content:space-between;">
                    <span>\uD83D\uDD0D Trace</span>
                    <span id="trace-value">--</span>
                </div>
                <div style="height:8px; background:var(--bg-secondary); border-radius:4px; overflow:hidden;">
                    <div id="trace-bar" style="width:0%; height:100%; background:var(--error); border-radius:4px; transition: width 1s;"></div>
                </div>
                <div id="trace-target" style="font-size:0.75rem; color:var(--text-secondary);"></div>
            </div>
            <div id="debt-indicator">
                <div style="display:flex; justify-content:space-between;">
                    <span>\uD83D\uDCB3 Debts</span>
                    <span id="debt-value">0</span>
                </div>
            </div>
            <button id="stealth-toggle" style="margin-top:8px; width:100%;" class="btn-secondary">\uD83E\uDD77 Toggle Stealth</button>
        </div>
    `;

    document.getElementById('stealth-toggle').onclick = async () => {
        const res = await apiCall('/api/stealth/toggle', { method: 'POST' });
        updateRiskIndicators();
    };
}

async function updateRiskIndicators() {
    try {
        const noiseEl = document.getElementById('noise-bar');
        const noiseVal = document.getElementById('noise-value');
        const traceEl = document.getElementById('trace-indicator');
        const traceBar = document.getElementById('trace-bar');
        const traceVal = document.getElementById('trace-value');
        const traceTarget = document.getElementById('trace-target');
        const debtVal = document.getElementById('debt-value');

        if (noiseEl) {
            const noiseRes = await apiCall('/api/noise');
            const level = noiseRes.level || 0;
            const pct = Math.min(level, 100);
            noiseEl.style.width = pct + '%';
            noiseEl.style.background = pct > 70 ? 'var(--error)' : pct > 40 ? 'var(--warning, orange)' : 'var(--success)';
            noiseVal.textContent = pct + '%';
        }

        if (traceEl) {
            const traceRes = await apiCall('/api/trace');
            if (traceRes.active) {
                traceEl.style.display = 'block';
                const remaining = traceRes.remaining_seconds || 0;
                const pct = Math.min(remaining / 180 * 100, 100);
                traceBar.style.width = pct + '%';
                traceVal.textContent = Math.ceil(remaining / 60) + 'm ' + (remaining % 60) + 's';
                traceTarget.textContent = 'Target: ' + (traceRes.target || '?');
            } else {
                traceEl.style.display = 'none';
            }
        }

        if (debtVal) {
            const debtRes = await apiCall('/api/debts');
            debtVal.textContent = debtRes.total || 0;
            debtVal.style.color = debtRes.total >= 5 ? 'var(--error)' : debtRes.total >= 3 ? 'orange' : 'inherit';
        }
    } catch(e) { /* silent */ }
}

// Auto-update every 10 seconds
if (typeof window !== 'undefined') {
    setInterval(updateRiskIndicators, 10000);
}
