/* CyberTeacher — Cyberpsychosis Visual Effects Overmind */
window.CyberpsychosisOvermind = {
    _level: 'normal',
    _pollTimer: null,
    _overlay: null,
    _warningBanner: null,

    async init() {
        this._createOverlay();
        await this._poll();
        this._pollTimer = setInterval(() => this._poll(), 15000);
    },

    destroy() {
        if (this._pollTimer) { clearInterval(this._pollTimer); this._pollTimer = null; }
        this._removeOverlay();
        this._removeBanner();
        document.body.style.removeProperty('animation');
    },

    _createOverlay() {
        if (this._overlay) return;
        this._overlay = document.createElement('div');
        this._overlay.id = 'cp-overlay';
        this._overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9998;transition:all 1s ease;';
        document.body.appendChild(this._overlay);
    },

    _removeOverlay() {
        if (this._overlay) { this._overlay.remove(); this._overlay = null; }
    },

    _createBanner(text) {
        this._removeBanner();
        this._warningBanner = document.createElement('div');
        this._warningBanner.id = 'cp-warning';
        this._warningBanner.textContent = text;
        this._warningBanner.style.cssText = `
            position:fixed;top:0;left:0;width:100%;padding:8px 16px;
            background:rgba(255,0,0,0.85);color:#fff;font-weight:bold;
            text-align:center;z-index:9999;font-size:0.9rem;
            animation: cpPulse 2s infinite;
            font-family:monospace;letter-spacing:1px;
        `;
        document.body.appendChild(this._warningBanner);
    },

    _removeBanner() {
        if (this._warningBanner) { this._warningBanner.remove(); this._warningBanner = null; }
    },

    async _poll() {
        try {
            const res = await fetch('/api/cyberpsychosis');
            if (!res.ok) return;
            const data = await res.json();
            const level = data.level || 'normal';
            if (level !== this._level) {
                this._level = level;
                this._applyEffects(level, data.state || {});
            }
        } catch (e) {
            // silently fail
        }
    },

    _applyEffects(level, state) {
        const maxVal = Math.max(state.stress || 0, state.obsession || 0, state.recklessness || 0);
        const overlay = this._overlay;
        if (!overlay) return;

        // Remove existing animations from body
        document.body.style.removeProperty('animation');

        switch (level) {
            case 'normal':
                overlay.style.boxShadow = 'none';
                overlay.style.background = 'transparent';
                overlay.style.opacity = '0';
                this._removeBanner();
                break;

            case 'elevated':
                overlay.style.boxShadow = 'inset 0 0 60px rgba(255,50,50,0.15)';
                overlay.style.background = 'transparent';
                overlay.style.opacity = '0.6';
                this._removeBanner();
                break;

            case 'critical':
                overlay.style.boxShadow = 'inset 0 0 100px rgba(255,0,0,0.25), inset 0 0 200px rgba(255,0,0,0.1)';
                overlay.style.background = 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,0,0,0.03) 2px, rgba(255,0,0,0.03) 4px)';
                overlay.style.opacity = '1';
                this._applyGlitchToUI();
                this._removeBanner();
                break;

            case 'dangerous':
                overlay.style.boxShadow = 'inset 0 0 150px rgba(255,0,0,0.35), inset 0 0 300px rgba(255,0,0,0.15)';
                overlay.style.background = 'repeating-linear-gradient(0deg, transparent, transparent 1px, rgba(255,0,0,0.05) 1px, rgba(255,0,0,0.05) 3px)';
                overlay.style.opacity = '1';
                document.body.style.animation = 'cpShake 0.15s infinite';
                this._applyGlitchToUI();
                this._createBanner('⚠ КРИТИЧЕСКИЙ УРОВЕНЬ КИБЕРПСИХОЗА. ВОЗЬМИ ПАУЗУ.');
                break;
        }
    },

    _applyGlitchToUI() {
        const targets = document.querySelectorAll('h1, h2, h3, .card-title, .stat-value');
        if (targets.length === 0) return;
        const randomTarget = targets[Math.floor(Math.random() * targets.length)];
        if (window.GlitchText) {
            window.GlitchText.apply(randomTarget, 600);
        }
    },
};

// Inject CSS animations
(function() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes cpShake {
            0% { transform: translate(0, 0); }
            25% { transform: translate(-2px, 1px); }
            50% { transform: translate(2px, -1px); }
            75% { transform: translate(-1px, 2px); }
            100% { transform: translate(0, 0); }
        }
        @keyframes cpPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
    `;
    document.head.appendChild(style);
})();

// Auto-init on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.CyberpsychosisOvermind.init());
} else {
    window.CyberpsychosisOvermind.init();
}
