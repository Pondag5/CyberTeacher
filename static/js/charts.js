/* Charts — SVG-based charts for analytics */
window.Charts = {
    barChart(container, data, options) {
        options = options || {};
        const maxVal = Math.max(...data.map(d => d.value), 1);
        const barHeight = options.barHeight || 24;
        const barGap = options.barGap || 8;
        const labelWidth = options.labelWidth || 120;
        const barWidth = options.barWidth || 300;
        const height = data.length * (barHeight + barGap) + 40;

        let svg = `<svg width="${labelWidth + barWidth + 80}" height="${height}" style="display:block;">`;

        data.forEach((item, i) => {
            const y = i * (barHeight + barGap) + 10;
            const w = (item.value / maxVal) * barWidth;
            const color = item.color || 'var(--accent)';

            // Label
            svg += `<text x="0" y="${y + barHeight / 2 + 4}" fill="var(--text-primary)" font-size="12" font-family="Inter">${item.label}</text>`;

            // Bar background
            svg += `<rect x="${labelWidth}" y="${y}" width="${barWidth}" height="${barHeight}" rx="4" fill="var(--bg-primary)"/>`;

            // Bar fill
            svg += `<rect x="${labelWidth}" y="${y}" width="${w}" height="${barHeight}" rx="4" fill="${color}" opacity="0.8"/>`;

            // Value label
            svg += `<text x="${labelWidth + barWidth + 8}" y="${y + barHeight / 2 + 4}" fill="var(--text-secondary)" font-size="12" font-family="Inter" font-weight="600">${item.value}</text>`;
        });

        svg += '</svg>';
        container.innerHTML = svg;
    },

    lineChart(container, data, options) {
        options = options || {};
        const width = options.width || 500;
        const height = options.height || 150;
        const padding = 20;
        const maxVal = Math.max(...data.map(d => d.value), 1);

        const xStep = (width - 2 * padding) / Math.max(data.length - 1, 1);
        const yScale = (height - 2 * padding) / maxVal;

        let svg = `<svg width="${width}" height="${height}" style="display:block;">`;

        // Grid lines
        for (let i = 0; i <= 4; i++) {
            const y = padding + (height - 2 * padding) * (1 - i / 4);
            svg += `<line x1="${padding}" y1="${y}" x2="${width - padding}" y2="${y}" stroke="var(--border)" stroke-width="0.5"/>`;
            svg += `<text x="${padding - 4}" y="${y + 4}" fill="var(--text-secondary)" font-size="9" font-family="Inter" text-anchor="end">${Math.round(maxVal * i / 4)}</text>`;
        }

        // Line
        const points = data.map((d, i) => {
            const x = padding + i * xStep;
            const y = height - padding - d.value * yScale;
            return `${x},${y}`;
        });
        svg += `<polyline points="${points.join(' ')}" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`;

        // Dots
        data.forEach((d, i) => {
            const x = padding + i * xStep;
            const y = height - padding - d.value * yScale;
            svg += `<circle cx="${x}" cy="${y}" r="3" fill="var(--accent)"/>`;
        });

        // Labels
        data.forEach((d, i) => {
            const x = padding + i * xStep;
            svg += `<text x="${x}" y="${height - 4}" fill="var(--text-secondary)" font-size="9" font-family="Inter" text-anchor="middle">${d.label || ''}</text>`;
        });

        svg += '</svg>';
        container.innerHTML = svg;
    }
};
