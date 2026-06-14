/* Heatmap — SVG-based 28-day activity calendar */
window.Heatmap = {
    render(container, data) {
        if (!data || !data.length) {
            container.innerHTML = '<div style="text-align:center; color:var(--text-secondary)">\u041D\u0435\u0442 \u0434\u0430\u043D\u043D\u044B\u0445</div>';
            return;
        }

        const days = 28;
        const cellSize = 16;
        const gap = 3;
        const cols = 7;
        const rows = Math.ceil(days / cols);

        const maxCount = Math.max(...data.map(d => d.count), 1);

        const getColor = (count) => {
            if (count === 0) return 'var(--bg-primary)';
            const intensity = count / maxCount;
            if (intensity < 0.25) return 'rgba(0, 180, 216, 0.2)';
            if (intensity < 0.5) return 'rgba(0, 180, 216, 0.4)';
            if (intensity < 0.75) return 'rgba(0, 180, 216, 0.7)';
            return 'var(--accent)';
        };

        const totalDays = rows * cols;
        while (data.length < totalDays) {
            data.push({ date: '', count: 0 });
        }

        const svgWidth = cols * (cellSize + gap) + 40;
        const svgHeight = rows * (cellSize + gap) + 30;

        let svg = `<svg width="${svgWidth}" height="${svgHeight}" style="display:block;">`;
        const labels = ['\u041F\u043D', '\u0412\u0442', '\u0421\u0440', '\u0427\u0442', '\u041F\u0442', '\u0421\u0431', '\u0412\u0441'];

        labels.forEach((label, i) => {
            svg += `<text x="0" y="${i * (cellSize + gap) + cellSize}" fill="var(--text-secondary)" font-size="9" font-family="Inter">${label}</text>`;
        });

        data.forEach((day, i) => {
            const col = Math.floor(i / cols);
            const row = i % cols;
            const x = 30 + col * (cellSize + gap);
            const y = row * (cellSize + gap);
            const color = getColor(day.count);
            svg += `<rect x="${x}" y="${y}" width="${cellSize}" height="${cellSize}" rx="3" fill="${color}" title="${day.date}: ${day.count}">\n<title>${day.date || 'N/A'}: ${day.count} \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0439</title></rect>`;
        });

        // Legend
        const legendY = svgHeight - 12;
        const legendX = 30;
        svg += `<text x="${legendX}" y="${legendY}" fill="var(--text-secondary)" font-size="9" font-family="Inter">\u041C\u0435\u043D\u0435\u0435</text>`;
        [0.2, 0.4, 0.7, 1.0].forEach((intensity, i) => {
            const lx = legendX + 45 + i * (cellSize + gap);
            svg += `<rect x="${lx}" y="${legendY - 10}" width="${cellSize}" height="${cellSize}" rx="3" fill="${getColor(intensity * maxCount)}"/>`;
        });
        svg += `<text x="${legendX + 45 + 4 * (cellSize + gap) + 5}" y="${legendY}" fill="var(--text-secondary)" font-size="9" font-family="Inter">\u0411\u043E\u043B\u044C\u0448\u0435</text>`;
        svg += '</svg>';

        container.innerHTML = svg;
    }
};
