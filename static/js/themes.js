/* CyberTeacher — Theme Manager (5 cyberpunk themes) */
window.ThemeManager = {
    themes: [
        { id: 'default',       label: 'Неон',    icon: '\u26A1',  desc: 'Основная киберпанк-тема' },
        { id: 'matrix',        label: 'Matrix',   icon: '\uD83D\uDDA5', desc: 'Матричный зелёный' },
        { id: 'hacker',        label: 'Hacker',   icon: '\uD83D\uDD11', desc: 'Терминал хакера' },
        { id: 'ocean',         label: 'Ocean',    icon: '\uD83C\uDF0A', desc: 'Глубокий океан' },
        { id: 'sunset',        label: 'Sunset',   icon: '\uD83C\uDF05', desc: 'Неоновый закат' },
    ],

    _current: 'default',

    get current() { return this._current; },

    apply(themeId) {
        const validThemes = this.themes.map(t => t.id);
        if (!validThemes.includes(themeId)) themeId = 'default';

        document.body.classList.remove(...validThemes.map(t => `theme-${t}`));
        if (themeId !== 'default') {
            document.body.classList.add(`theme-${themeId}`);
        }

        this._current = themeId;
        localStorage.setItem('theme', themeId);

        // Update active button state
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.theme === themeId);
        });

        // Apply Hacker Terminal monospace globally
        if (themeId === 'hacker') {
            document.body.style.setProperty('--font-body', "'Fira Code', 'Cascadia Code', monospace");
        } else {
            document.body.style.removeProperty('--font-body');
        }

        // Trigger particles color update
        if (window.CyberParticles && window.CyberParticles.updateColor) {
            window.CyberParticles.updateColor();
        }

        // Matrix Rain: start for Dark Matrix, stop for others
        if (themeId === 'matrix') {
            if (window.MatrixRain) setTimeout(() => window.MatrixRain.init(), 100);
        } else {
            if (window.MatrixRain) window.MatrixRain.destroy();
        }

        // Sound feedback
        if (window.Sounds && window.Sounds.click) {
            window.Sounds.click();
        }
    },

    init() {
        const saved = localStorage.getItem('theme') || 'default';
        this.apply(saved);
    },

    getRandom() {
        const idx = Math.floor(Math.random() * this.themes.length);
        return this.themes[idx];
    },

    cycle() {
        const ids = this.themes.map(t => t.id);
        const curIdx = ids.indexOf(this._current);
        const nextIdx = (curIdx + 1) % ids.length;
        this.apply(ids[nextIdx]);
        return this._current;
    }
};
