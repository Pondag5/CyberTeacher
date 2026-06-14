/* CyberParticles — animated background canvas with floating particles + connections */
window.CyberParticles = {
    _canvas: null,
    _ctx: null,
    _particles: [],
    _animFrame: null,
    _maxParticles: 50,
    _connectionDistance: 120,

    init(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        this._canvas = document.createElement('canvas');
        this._canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;pointer-events:none;opacity:0.4';
        container.appendChild(this._canvas);
        this._ctx = this._canvas.getContext('2d');
        this._resize();
        window.addEventListener('resize', () => this._resize());
        this._createParticles();
        this._animate();
    },

    _resize() {
        if (!this._canvas) return;
        this._canvas.width = window.innerWidth;
        this._canvas.height = window.innerHeight;
    },

    _createParticles() {
        this._particles = [];
        for (let i = 0; i < this._maxParticles; i++) {
            this._particles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                r: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.2,
            });
        }
    },

    _animate() {
        if (!this._ctx || !this._canvas) return;
        const ctx = this._ctx;
        const w = this._canvas.width;
        const h = this._canvas.height;

        ctx.clearRect(0, 0, w, h);

        // Get accent color from CSS
        const style = getComputedStyle(document.documentElement);
        const accent = style.getPropertyValue('--accent').trim() || '#00B4D8';

        // Update + draw particles
        this._particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > w) p.vx *= -1;
            if (p.y < 0 || p.y > h) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = accent;
            ctx.globalAlpha = p.opacity;
            ctx.fill();
        });

        // Draw connections
        for (let i = 0; i < this._particles.length; i++) {
            for (let j = i + 1; j < this._particles.length; j++) {
                const dx = this._particles[i].x - this._particles[j].x;
                const dy = this._particles[i].y - this._particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < this._connectionDistance) {
                    ctx.beginPath();
                    ctx.moveTo(this._particles[i].x, this._particles[i].y);
                    ctx.lineTo(this._particles[j].x, this._particles[j].y);
                    ctx.strokeStyle = accent;
                    ctx.globalAlpha = 0.15 * (1 - dist / this._connectionDistance);
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        ctx.globalAlpha = 1;

        this._animFrame = requestAnimationFrame(() => this._animate());
    },

    destroy() {
        if (this._animFrame) cancelAnimationFrame(this._animFrame);
        if (this._canvas) this._canvas.remove();
    }
};
