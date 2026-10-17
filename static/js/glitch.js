/* CyberTeacher — Atmospheric Glitch Effects
   Time-based (3AM), debt-based visual disturbances, WS-triggered glitches */
window.GlitchAtmosphere = {
    _timer: null,
    _activeEffects: new Set(),
    _wsConnected: false,

    init() {
        this._tick();
        this._timer = setInterval(() => this._tick(), 30000);
        this._setupWebSocket();
    },

    destroy() {
        if (this._timer) { clearInterval(this._timer); this._timer = null; }
        this._clearAll();
    },

    _setupWebSocket() {
        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/glitch`;
            this._ws = new WebSocket(wsUrl);
            
            this._ws.onopen = () => {
                this._wsConnected = true;
                console.log('[Glitch] WebSocket connected');
            };
            
            this._ws.onmessage = (event) => {
                try {
                    const msg = JSON.parse(event.data);
                    this._handleWSMessage(msg);
                } catch (e) { /* silent */ }
            };
            
            this._ws.onclose = () => {
                this._wsConnected = false;
                // Reconnect after 5s
                setTimeout(() => this._setupWebSocket(), 5000);
            };
            
            this._ws.onerror = () => { /* silent */ };
        } catch (e) { /* silent */ }
    },

    _handleWSMessage(msg) {
        switch (msg.type) {
            case 'glitch_text':
                this.glitchText(msg.selector || '.chat-messages .bubble', msg.duration || 500);
                break;
            case 'glitch_color':
                this.glitchColor(msg.duration || 3000);
                break;
            case 'fake_console_log':
                this.fakeConsoleLog(msg.text || 'SYSTEM: Unauthorized access detected', msg.style || 'error');
                break;
            case 'fake_camera_request':
                this.fakeCameraRequest();
                break;
            case 'phantom_message':
                this.showPhantomBanner(msg.text);
                break;
            case 'cp_spike':
                this._triggerCPSpike(msg.level || 2);
                break;
        }
    },

    _tick() {
        const hour = new Date().getHours();
        const isWitchingHour = hour === 3;

        if (isWitchingHour && !this._activeEffects.has('witching')) {
            this._enableWitchingHour();
        } else if (!isWitchingHour && this._activeEffects.has('witching')) {
            this._disableWitchingHour();
        }

        this._checkDebts();
        this._checkCPGlitch();
    },

    /* ─── Glitch Text Effect ─── */
    glitchText(selector, duration = 500) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
            const original = el.textContent;
            const chars = '!@#$%^&*()_+-=[]{}|;:,.<>?';
            let iterations = 0;
            const maxIterations = Math.floor(duration / 50);
            
            const interval = setInterval(() => {
                el.textContent = original.split('').map(c => 
                    Math.random() < 0.3 ? chars[Math.floor(Math.random() * chars.length)] : c
                ).join('');
                iterations++;
                if (iterations >= maxIterations) {
                    clearInterval(interval);
                    el.textContent = original;
                }
            }, 50);
        });
    },

    /* ─── Glitch Color (B&W) ─── */
    glitchColor(duration = 3000) {
        if (this._activeEffects.has('glitch_color')) return;
        this._activeEffects.add('glitch_color');
        
        const style = document.createElement('style');
        style.id = 'glitch-color-css';
        style.textContent = `
            @keyframes colorGlitch {
                0%, 100% { filter: grayscale(0) hue-rotate(0deg); }
                25% { filter: grayscale(1) hue-rotate(90deg); }
                50% { filter: grayscale(1) hue-rotate(180deg); }
                75% { filter: grayscale(1) hue-rotate(270deg); }
            }
            body.glitch-color { animation: colorGlitch ${duration}ms ease-in-out; }
        `;
        document.head.appendChild(style);
        document.body.classList.add('glitch-color');
        
        setTimeout(() => {
            this._activeEffects.delete('glitch_color');
            document.body.classList.remove('glitch-color');
            const s = document.getElementById('glitch-color-css');
            if (s) s.remove();
        }, duration);
    },

    /* ─── Fake Console Log ─── */
    fakeConsoleLog(text, style = 'error') {
        const consoleEl = document.querySelector('.terminal-console, .console-output, #console-log');
        if (!consoleEl) return;
        
        const line = document.createElement('div');
        line.className = `console-line console-${style}`;
        line.style.cssText = `
            font-family: monospace; 
            color: ${style === 'error' ? '#ff4444' : style === 'warn' ? '#ffaa00' : '#44ff44'};
            margin: 2px 0;
            opacity: 0;
            animation: fadeIn 0.3s forwards;
        `;
        
        const timestamp = new Date().toLocaleTimeString();
        line.textContent = `[${timestamp}] ${text}`;
        consoleEl.appendChild(line);
        consoleEl.scrollTop = consoleEl.scrollHeight;
        
        // Remove after 10s
        setTimeout(() => {
            line.style.animation = 'fadeOut 0.5s forwards';
            setTimeout(() => line.remove(), 500);
        }, 10000);
    },

    /* ─── Fake Camera Request ─── */
    fakeCameraRequest() {
        if (this._activeEffects.has('fake_camera')) return;
        this._activeEffects.add('fake_camera');
        
        // Create fake permission dialog
        const overlay = document.createElement('div');
        overlay.id = 'fake-camera-overlay';
        overlay.style.cssText = `
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9); z-index: 99999;
            display: flex; align-items: center; justify-content: center;
            font-family: monospace;
        `;
        overlay.innerHTML = `
            <div style="background: #111; border: 2px solid #ff4444; padding: 30px; border-radius: 8px; text-align: center; max-width: 400px;">
                <div style="font-size: 3rem; margin-bottom: 16px;">📷</div>
                <h2 style="color: #ff4444; margin-bottom: 12px;">Camera Access Requested</h2>
                <p style="color: #aaa; margin-bottom: 24px;">CyberTeacher wants to access your camera</p>
                <div style="display: flex; gap: 12px; justify-content: center;">
                    <button id="fake-camera-allow" style="background: #ff4444; color: white; border: none; padding: 10px 24px; border-radius: 4px; cursor: pointer;">Allow</button>
                    <button id="fake-camera-deny" style="background: #333; color: #aaa; border: none; padding: 10px 24px; border-radius: 4px; cursor: pointer;">Block</button>
                </div>
                <p style="color: #666; font-size: 0.8rem; margin-top: 16px;">This is a simulation. No camera access is actually requested.</p>
            </div>
        `;
        document.body.appendChild(overlay);
        
        document.getElementById('fake-camera-allow').onclick = () => {
            overlay.remove();
            this._activeEffects.delete('fake_camera');
            this.fakeConsoleLog('CAMERA: Access GRANTED (simulated)', 'warn');
        };
        document.getElementById('fake-camera-deny').onclick = () => {
            overlay.remove();
            this._activeEffects.delete('fake_camera');
            this.fakeConsoleLog('CAMERA: Access DENIED', 'error');
        };
        
        // Auto-close after 10s
        setTimeout(() => {
            if (document.getElementById('fake-camera-overlay')) {
                document.getElementById('fake-camera-overlay').remove();
                this._activeEffects.delete('fake_camera');
            }
        }, 10000);
    },

    /* ─── Phantom Banner ─── */
    showPhantomBanner(text) {
        const banner = document.createElement('div');
        banner.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 9999;
            background: linear-gradient(135deg, #1a0033, #000);
            border: 1px solid #ff00ff; border-radius: 8px;
            padding: 16px 24px; max-width: 350px;
            font-family: monospace; font-size: 0.85rem;
            color: #ff00ff; box-shadow: 0 0 30px rgba(255,0,255,0.3);
            animation: phantomSlideIn 0.5s ease-out, phantomFlicker 3s infinite;
            cursor: pointer;
        `;
        banner.textContent = text;
        document.body.appendChild(banner);
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes phantomSlideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
            @keyframes phantomFlicker { 0%, 95% { opacity: 1; } 96% { opacity: 0.6; } 97% { opacity: 0.9; } 98% { opacity: 0.4; } 99% { opacity: 0.8; } 100% { opacity: 1; } }
        `;
        document.head.appendChild(style);
        
        banner.onclick = () => banner.remove();
        setTimeout(() => { if (banner.parentNode) banner.remove(); }, 15000);
    },

    _triggerCPSpike(level) {
        // Temporarily increase CP glitch intensity
        if (this._activeEffects.has('cp_glitch')) {
            this._updateCPGlitch(Math.min(4, level + 1));
            setTimeout(() => this._updateCPGlitch(level), 5000);
        }
    },

    /* ─── 3AM Witching Hour ─── */
    _enableWitchingHour() {
        this._activeEffects.add('witching');
        const style = document.createElement('style');
        style.id = 'glitch-witching-css';
        style.textContent = `
            @keyframes witchingFlicker {
                0%, 95% { opacity: 1; }
                96% { opacity: 0.7; }
                97% { opacity: 0.9; }
                98% { opacity: 0.5; }
                99% { opacity: 0.8; }
            }
            @keyframes witchingGlitch {
                0%, 90% { transform: none; opacity: 1; }
                91% { transform: translate(-1px, 1px); opacity: 0.8; }
                92% { transform: translate(1px, -1px); opacity: 0.9; }
                93% { transform: translate(0, 0); opacity: 1; }
            }
            body.witching-hour .sidebar {
                animation: witchingFlicker 3s infinite;
            }
            body.witching-hour .status-bar {
                animation: witchingGlitch 8s infinite;
            }
            body.witching-hour #cp-overlay {
                box-shadow: inset 0 0 80px rgba(100,0,150,0.12) !important;
            }
        `;
        document.head.appendChild(style);
        document.body.classList.add('witching-hour');

        const logo = document.querySelector('.sidebar .logo, .sidebar h1, .sidebar h2');
        if (logo && window.GlitchText) {
            setInterval(() => {
                if (new Date().getHours() === 3) {
                    window.GlitchText.apply(logo, 400);
                }
            }, 20000);
        }
    },

    _disableWitchingHour() {
        this._activeEffects.delete('witching');
        document.body.classList.remove('witching-hour');
        const style = document.getElementById('glitch-witching-css');
        if (style) style.remove();
    },

    /* ─── Debt Warning ─── */
    async _checkDebts() {
        try {
            const res = await fetch('/api/debts');
            if (!res.ok) return;
            const data = await res.json();
            const total = data.total || 0;

            if (total >= 5 && !this._activeEffects.has('debt_critical')) {
                this._enableDebtWarning(total);
            } else if (total < 5 && this._activeEffects.has('debt_critical')) {
                this._disableDebtWarning();
            } else if (this._activeEffects.has('debt_critical')) {
                this._updateDebtBadge(total);
            }

            if (total >= 3 && total < 5 && !this._activeEffects.has('debt_warning')) {
                this._activeEffects.add('debt_warning');
            } else if (total < 3 && this._activeEffects.has('debt_warning')) {
                this._activeEffects.delete('debt_warning');
            }
        } catch (e) { /* silent */ }
    },

    _enableDebtWarning(total) {
        this._activeEffects.add('debt_critical');
        const badge = document.createElement('div');
        badge.id = 'debt-critical-badge';
        badge.style.cssText = `
            position: fixed; bottom: 16px; left: 16px; z-index: 9999;
            background: rgba(255,0,0,0.9); color: #fff;
            padding: 8px 14px; border-radius: 8px;
            font-family: monospace; font-weight: bold;
            font-size: 0.8rem; box-shadow: 0 0 20px rgba(255,0,0,0.4);
            animation: debtPulse 1.5s infinite;
            cursor: pointer;
        `;
        badge.textContent = `\uD83D\uDCA5 ДОЛГОВ: ${total}. Подсказки отключены.`;
        badge.onclick = () => {
            const tab = document.querySelector('[data-tab="debt"], [data-tab="profile"]');
            if (tab) tab.click();
        };
        document.body.appendChild(badge);

        const style = document.createElement('style');
        style.id = 'glitch-debt-css';
        style.textContent = `
            @keyframes debtPulse {
                0%, 100% { box-shadow: 0 0 20px rgba(255,0,0,0.4); }
                50% { box-shadow: 0 0 40px rgba(255,0,0,0.7); }
            }
        `;
        document.head.appendChild(style);

        if (window.Sounds && Sounds.glitch) Sounds.glitch();
    },

    _updateDebtBadge(total) {
        const badge = document.getElementById('debt-critical-badge');
        if (badge) {
            badge.textContent = `\uD83D\uDCA5 ДОЛГОВ: ${total}. Подсказки отключены.`;
        }
    },

    _disableDebtWarning() {
        this._activeEffects.delete('debt_critical');
        this._activeEffects.delete('debt_warning');
        const badge = document.getElementById('debt-critical-badge');
        if (badge) badge.remove();
        const style = document.getElementById('glitch-debt-css');
        if (style) style.remove();
    },

    /* ─── CP-based Glitches (Chapter 7) ─── */
    async _checkCPGlitch() {
        try {
            const res = await fetch('/api/cyberpsychosis');
            if (!res.ok) return;
            const data = await res.json();
            const level = data.level || 0; // 0-4

            if (level >= 2 && !this._activeEffects.has('cp_glitch')) {
                this._enableCPGlitch(level);
            } else if (level < 2 && this._activeEffects.has('cp_glitch')) {
                this._disableCPGlitch();
            } else if (this._activeEffects.has('cp_glitch')) {
                this._updateCPGlitch(level);
            }
        } catch (e) { /* silent */ }
    },

    _enableCPGlitch(level) {
        this._activeEffects.add('cp_glitch');
        const style = document.createElement('style');
        style.id = 'glitch-cp-css';
        const intensity = Math.min(level * 0.3, 1.0);
        style.textContent = `
            @keyframes cpFlicker {
                0%, 90% { opacity: 1; }
                91% { opacity: ${0.7 - intensity * 0.3}; }
                92% { opacity: ${0.9 - intensity * 0.2}; }
                93% { opacity: ${0.5 - intensity * 0.2}; }
                94% { opacity: ${0.8 - intensity * 0.3}; }
                95% { opacity: 1; }
            }
            @keyframes cpTextGlitch {
                0%, 85% { transform: none; opacity: 1; }
                86% { transform: translate(-${2 * level}px, ${1 * level}px); opacity: ${0.9 - level * 0.1}; }
                87% { transform: translate(${1 * level}px, -${2 * level}px); opacity: ${0.8 - level * 0.1}; }
                88% { transform: translate(-${1 * level}px, ${1 * level}px); opacity: 1; }
            }
            body.cp-glitch .sidebar {
                animation: cpFlicker ${5 - level}s infinite;
            }
            body.cp-glitch .chat-messages .bubble {
                animation: cpTextGlitch ${8 - level * 2}s infinite;
            }
            body.cp-glitch #cp-overlay {
                box-shadow: inset 0 0 ${80 + level * 40}px rgba(255, 0, 100, ${0.12 + level * 0.05}) !important;
            }
        `;
        document.head.appendChild(style);
        document.body.classList.add('cp-glitch');

        const logo = document.querySelector('.sidebar .logo, .sidebar h1, .sidebar h2');
        if (logo && window.GlitchText) {
            this._cpGlitchInterval = setInterval(() => {
                if (window.GlitchText) {
                    window.GlitchText.apply(logo, 300 * (5 - level));
                }
            }, 15000);
        }
    },

    _updateCPGlitch(level) {
        const style = document.getElementById('glitch-cp-css');
        if (style) {
            const intensity = Math.min(level * 0.3, 1.0);
            style.textContent = `
                @keyframes cpFlicker {
                    0%, 90% { opacity: 1; }
                    91% { opacity: ${0.7 - intensity * 0.3}; }
                    92% { opacity: ${0.9 - intensity * 0.2}; }
                    93% { opacity: ${0.5 - intensity * 0.2}; }
                    94% { opacity: ${0.8 - intensity * 0.3}; }
                    95% { opacity: 1; }
                }
                @keyframes cpTextGlitch {
                    0%, 85% { transform: none; opacity: 1; }
                    86% { transform: translate(-${2 * level}px, ${1 * level}px); opacity: ${0.9 - level * 0.1}; }
                    87% { transform: translate(${1 * level}px, -${2 * level}px); opacity: ${0.8 - level * 0.1}; }
                    88% { transform: translate(-${1 * level}px, ${1 * level}px); opacity: 1; }
                }
                body.cp-glitch .sidebar {
                    animation: cpFlicker ${5 - level}s infinite;
                }
                body.cp-glitch .chat-messages .bubble {
                    animation: cpTextGlitch ${8 - level * 2}s infinite;
                }
                body.cp-glitch #cp-overlay {
                    box-shadow: inset 0 0 ${80 + level * 40}px rgba(255, 0, 100, ${0.12 + level * 0.05}) !important;
                }
            `;
        }
    },

    _disableCPGlitch() {
        this._activeEffects.delete('cp_glitch');
        document.body.classList.remove('cp-glitch');
        const style = document.getElementById('glitch-cp-css');
        if (style) style.remove();
        if (this._cpGlitchInterval) {
            clearInterval(this._cpGlitchInterval);
            this._cpGlitchInterval = null;
        }
    },

    _clearAll() {
        this._disableWitchingHour();
        this._disableDebtWarning();
        this._disableCPGlitch();
        this._activeEffects.delete('glitch_color');
        this._activeEffects.delete('fake_camera');
        const s = document.getElementById('glitch-color-css');
        if (s) s.remove();
        const cam = document.getElementById('fake-camera-overlay');
        if (cam) cam.remove();
    },
};

// Auto-init after DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.GlitchAtmosphere.init());
} else {
    window.GlitchAtmosphere.init();
}
