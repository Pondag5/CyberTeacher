/* CyberTeacher — Sound Effects v2 (Web Audio API, no files) */
window.Sounds = {
    _ctx: null,
    _muted: false,
    _volume: 0.15,

    init() {
        this._muted = localStorage.getItem('sounds_muted') === 'true';
        this._updateToggleUI();
    },

    get muted() { return this._muted; },
    set muted(val) {
        this._muted = !!val;
        localStorage.setItem('sounds_muted', this._muted);
        this._updateToggleUI();
    },

    toggle() {
        this.muted = !this._muted;
        return this._muted;
    },

    _updateToggleUI() {
        document.querySelectorAll('.sound-toggle').forEach(el => {
            el.classList.toggle('muted', this._muted);
            el.textContent = this._muted ? '\uD83D\uDD07' : '\uD83D\uDD0A';
        });
        document.querySelectorAll('.sound-indicator').forEach(el => {
            el.style.opacity = this._muted ? '0.3' : '1';
        });
    },

    _getCtx() {
        if (!this._ctx) {
            try {
                this._ctx = new (window.AudioContext || window.webkitAudioContext)();
            } catch (e) { return null; }
        }
        if (this._ctx.state === 'suspended') {
            this._ctx.resume().catch(() => {});
        }
        return this._ctx;
    },

    _play(freq, duration, type = 'sine', volume) {
        if (this._muted) return;
        const ctx = this._getCtx();
        if (!ctx) return;
        const vol = volume !== undefined ? volume : this._volume;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        gain.gain.setValueAtTime(vol, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + duration);
    },

    _noise(duration, volume) {
        if (this._muted) return;
        const ctx = this._getCtx();
        if (!ctx) return;
        const vol = volume !== undefined ? volume : 0.05;
        const bufferSize = ctx.sampleRate * duration;
        const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        const source = ctx.createBufferSource();
        source.buffer = buffer;
        const gain = ctx.createGain();
        gain.gain.setValueAtTime(vol, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
        source.connect(gain);
        gain.connect(ctx.destination);
        source.start(ctx.currentTime);
    },

    // Ascending C-E-G arpeggio
    success() {
        if (this._muted) return;
        this._play(523, 0.1);
        setTimeout(() => this._play(659, 0.1), 100);
        setTimeout(() => this._play(784, 0.15), 200);
    },

    // Descending sawtooth
    error() {
        if (this._muted) return;
        this._play(200, 0.15, 'sawtooth', 0.08);
        setTimeout(() => this._play(150, 0.2, 'sawtooth', 0.08), 150);
    },

    // C-E-G-C asc
    achievement() {
        if (this._muted) return;
        this._play(523, 0.08);
        setTimeout(() => this._play(659, 0.08), 80);
        setTimeout(() => this._play(784, 0.08), 160);
        setTimeout(() => this._play(1047, 0.2), 240);
    },

    // Short square wave click
    click() {
        if (this._muted) return;
        this._play(800, 0.04, 'square', 0.06);
    },

    // Two-tone chime
    notification() {
        if (this._muted) return;
        this._play(880, 0.1);
        setTimeout(() => this._play(1100, 0.15), 120);
    },

    // Ascending scale
    levelUp() {
        if (this._muted) return;
        const notes = [523, 587, 659, 784, 880, 1047, 1175, 1319];
        notes.forEach((n, i) => setTimeout(() => this._play(n, 0.12), i * 70));
    },

    // Page/tab switch swoosh
    pageTransition() {
        if (this._muted) return;
        this._play(300, 0.08, 'sine', 0.04);
        setTimeout(() => this._play(500, 0.1, 'sine', 0.03), 80);
    },

    // Keypress tick for terminal
    keypress() {
        if (this._muted) return;
        this._play(600, 0.02, 'square', 0.02);
    },

    // Hover ding
    hover() {
        if (this._muted) return;
        this._play(1200, 0.03, 'sine', 0.02);
    },

    // Glitch / error burst
    glitch() {
        if (this._muted) return;
        this._noise(0.05, 0.06);
        this._play(50, 0.05, 'sawtooth', 0.04);
    }
};
