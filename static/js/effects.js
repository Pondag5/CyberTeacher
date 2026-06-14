/* CyberTeacher — Enhanced Visual Effects v2 */
/* ─── GlitchText — scrambles text on hover ─── */
window.GlitchText = {
    _chars: '!@#$%^&*()_+-=[]{}|;:,.<>?/~`\u0394\u03A0\u03A3\u03A9\u00A5\u00A3',

    apply(element, duration) {
        if (!element) return;
        duration = duration || 1500;
        const original = element.textContent;
        const maxIterations = 12;
        let iteration = 0;

        const interval = setInterval(() => {
            element.textContent = original
                .split('')
                .map((char, i) => {
                    if (i < Math.floor(iteration)) return original[i];
                    if (char === ' ') return ' ';
                    return this._chars[Math.floor(Math.random() * this._chars.length)];
                })
                .join('');

            iteration += 1 / (duration / maxIterations / 100);
            if (iteration >= original.length) {
                clearInterval(interval);
                element.textContent = original;
            }
        }, 40);
    },

    applyAll() {
        document.querySelectorAll('.glitch-trigger').forEach(el => {
            el.addEventListener('mouseenter', () => this.apply(el, 800));
        });
    }
};

/* ─── CyberBorder — animated neon border glow on hover ─── */
window.CyberBorder = {
    init() {
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transition = 'box-shadow 0.3s, border-color 0.3s';
                card.style.boxShadow = 'var(--glow), var(--shadow-md)';
                card.style.borderColor = 'var(--accent)';
            });
            card.addEventListener('mouseleave', () => {
                card.style.boxShadow = '';
                card.style.borderColor = '';
            });
        });
    }
};

/* ─── TypeWriter — typing animation for text elements ─── */
window.TypeWriter = {
    async type(element, text, speed = 30) {
        if (!element) return;
        element.textContent = '';
        for (let i = 0; i < text.length; i++) {
            element.textContent += text[i];
            if (window.Sounds && window.Sounds.keypress) {
                window.Sounds.keypress();
            }
            await new Promise(r => setTimeout(r, speed));
        }
    },

    async typeToElement(element, speed = 30) {
        const text = element.textContent;
        await this.type(element, text, speed);
    }
};

/* ─── Confetti — celebratory particles ─── */
window.Confetti = {
    fire(count = 30) {
        const container = document.createElement('div');
        container.className = 'confetti-container';
        document.body.appendChild(container);

        const colors = ['var(--accent)', 'var(--success)', 'var(--warning)', 'var(--error)', '#a78bfa', '#f472b6'];

        for (let i = 0; i < count; i++) {
            const piece = document.createElement('div');
            piece.className = 'confetti-piece';
            const color = colors[Math.floor(Math.random() * colors.length)];
            const size = Math.random() * 8 + 4;
            const x = Math.random() * 100;
            const delay = Math.random() * 0.5;
            const rot = Math.random() * 360;

            piece.style.cssText = `
                left: ${x}%;
                bottom: -10px;
                width: ${size}px;
                height: ${size * 0.6}px;
                background: ${color};
                border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
                animation-delay: ${delay}s;
                animation-duration: ${1 + Math.random()}s;
                transform: rotate(${rot}deg);
                box-shadow: 0 0 4px ${color};
            `;
            container.appendChild(piece);
        }

        setTimeout(() => container.remove(), 3000);
    }
};

/* ─── Counter — animated number tick-up ─── */
window.Counter = {
    animate(element, target, duration = 800, prefix = '', suffix = '') {
        if (!element) return;
        const start = parseInt(element.dataset.counterStart) || 0;
        const startTime = performance.now();
        element.classList.add('counter-value');

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (target - start) * eased);
            element.textContent = prefix + current.toLocaleString() + suffix;
            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = prefix + target.toLocaleString() + suffix;
            }
        }
        requestAnimationFrame(update);
    }
};

/* ─── CyberTerminal — adds terminal-like cursor blink to elements ─── */
window.CyberTerminal = {
    init() {
        document.querySelectorAll('.terminal-cursor').forEach(el => {
            const cursor = document.createElement('span');
            cursor.className = 'terminal-cursor-blink';
            cursor.textContent = '\u2588';
            cursor.style.cssText = 'animation: blink 1s step-end infinite; color: var(--accent); margin-left: 2px;';
            el.appendChild(cursor);
        });
    }
};

/* ─── MatrixRain — falling green characters for Dark Matrix theme ─── */
window.MatrixRain = {
    _canvas: null,
    _ctx: null,
    _drops: [],
    _fontSize: 14,
    _columns: 0,
    _animFrame: null,
    _isRunning: false,

    init() {
        if (this._isRunning) return;
        this._canvas = document.createElement('canvas');
        this._canvas.id = 'matrixRainCanvas';
        this._canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.06';
        document.body.prepend(this._canvas);
        this._ctx = this._canvas.getContext('2d');
        this._resize();
        window.addEventListener('resize', () => this._resize());
        this._isRunning = true;
        this._animate();
    },

    destroy() {
        this._isRunning = false;
        if (this._animFrame) { cancelAnimationFrame(this._animFrame); this._animFrame = null; }
        if (this._canvas) { this._canvas.remove(); this._canvas = null; }
        this._drops = [];
    },

    _resize() {
        if (!this._canvas) return;
        this._canvas.width = window.innerWidth;
        this._canvas.height = window.innerHeight;
        this._columns = Math.floor(this._canvas.width / this._fontSize);
        this._drops = [];
        for (let i = 0; i < this._columns; i++) {
            this._drops[i] = Math.floor(Math.random() * -100);
        }
    },

    _animate() {
        if (!this._isRunning || !this._ctx || !this._canvas) return;
        const ctx = this._ctx;
        const w = this._canvas.width;
        const h = this._canvas.height;

        ctx.fillStyle = 'rgba(10, 10, 15, 0.05)';
        ctx.fillRect(0, 0, w, h);

        const accent = 'var(--accent)';
        const style = getComputedStyle(document.documentElement);
        let color = style.getPropertyValue('--accent').trim() || '#00FF41';
        // Fallback for theme-matrix
        if (!color || color === '#00FFC3') color = '#00FF41';

        ctx.fillStyle = color;
        ctx.font = this._fontSize + 'px monospace';

        for (let i = 0; i < this._drops.length; i++) {
            const char = String.fromCharCode(0x30A0 + Math.random() * 96);
            ctx.fillStyle = color;
            ctx.globalAlpha = 0.3 + Math.random() * 0.7;
            ctx.fillText(char, i * this._fontSize, this._drops[i] * this._fontSize);

            if (this._drops[i] * this._fontSize > h && Math.random() > 0.975) {
                this._drops[i] = 0;
            }
            this._drops[i]++;
        }
        ctx.globalAlpha = 1;

        this._animFrame = requestAnimationFrame(() => this._animate());
    }
};
