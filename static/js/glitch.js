/* CyberTeacher — Atmospheric Glitch Effects
   Time-based (3AM), debt-based visual disturbances */
window.GlitchAtmosphere = {
    _timer: null,
    _activeEffects: new Set(),

    init() {
        this._tick();
        this._timer = setInterval(() => this._tick(), 30000);
    },

    destroy() {
        if (this._timer) { clearInterval(this._timer); this._timer = null; }
        this._clearAll();
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
    },
};

// Auto-init after DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.GlitchAtmosphere.init());
} else {
    window.GlitchAtmosphere.init();
}
