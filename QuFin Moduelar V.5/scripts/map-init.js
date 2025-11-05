async function fetchCountryScores() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/country-scores/');
        if (!response.ok) throw new Error('Failed to fetch scores');
        const data = await response.json();
        console.log('Fetched scores:', data);
        return data;
    } catch (error) {
        console.error('Error fetching scores:', error);
        return null;
    }
}

async function initializeMap() {
    const scores = await fetchCountryScores();
    if (scores) {
        window.countryScores = scores;
    }

    const mapContainer = document.getElementById('worldMap');
    if (!mapContainer) return;
    mapContainer.innerHTML = '';

    const width = mapContainer.clientWidth || 960;
    const height = mapContainer.clientHeight || 600;

    const svg = d3.select(mapContainer)
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', `0 0 ${width} ${height}`)
        .style('display', 'block');

    // Color scale for economic scores
    const colorScale = d3.scaleLinear()
        .domain([0, 25, 50, 75, 100])
        .range(['#ef4444', '#ff8a00', '#fef3c7', '#84cc16', '#22c55e'])
        .clamp(true);

    const projection = d3.geoNaturalEarth1()
        .scale(width / 6.5)
        .translate([width / 2, height / 2]);

    const path = d3.geoPath().projection(projection);

    // Load world map data
    const worldData = await d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json');
    const features = topojson.feature(worldData, worldData.objects.countries).features;

    // Create tooltip
    const tooltip = d3.select('body').append('div')
        .attr('class', 'country-tooltip')
        .style('opacity', 0)
        .style('position', 'absolute')
        .style('pointer-events', 'none')
        .style('z-index', 10000);

    // Draw countries
    svg.selectAll('path')
        .data(features)
        .enter()
        .append('path')
        .attr('d', path)
        .attr('fill', d => {
            const iso3 = d.properties.iso_a3;
            const score = window.countryScores[iso3];
            console.log('Country data:', {
                name: d.properties.name,
                iso3: iso3,
                score: score
            });
            return score !== undefined ? colorScale(score) : '#ccc';
        })
        .attr('stroke', '#fff')
        .attr('stroke-width', '0.5')
        .on('mouseover', function(event, d) {
            const iso3 = d.properties.iso_a3;
            const score = window.countryScores[iso3];
            const countryName = d.properties.name;

            d3.select(this)
                .style('opacity', 1)
                .style('stroke-width', '2')
                .raise();

            tooltip.transition()
                .duration(200)
                .style('opacity', .9);

            tooltip.html(`
                <div style="background: rgba(15, 23, 42, 0.95); padding: 12px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-weight: 700; margin-bottom: 6px; color: #fff;">
                        ${countryName}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-bottom: 8px;">
                        <div style="font-size: 12px; color: #94a3b8">Economic Score:</div>
                        <div style="font-size: 24px; font-weight: 800; color: ${score !== undefined ? colorScale(score) : '#94a3b8'}">
                            ${score !== undefined ? score.toFixed(1) : 'N/A'}
                        </div>
                    </div>
                    <div style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; margin: 8px 0;">
                        <div style="height: 100%; width: ${score !== undefined ? score : 0}%; 
                             background: ${score !== undefined ? colorScale(score) : '#94a3b8'}; 
                             transition: width 0.3s ease;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 8px;">
                        <span style="color: #94a3b8; font-size: 12px;">Status:</span>
                        <span style="color: ${score !== undefined ? colorScale(score) : '#94a3b8'}; font-weight: 500;">
                            ${score !== undefined ? 
                                (score >= 70 ? 'Excellent' :
                                score >= 50 ? 'Good' :
                                score >= 30 ? 'Fair' : 'Poor')
                            : 'Unknown'}
                        </span>
                    </div>
                    <div style="color: #64748b; font-size: 11px; margin-top: 8px;">
                        ISO Code: ${iso3 || 'Unknown'}
                    </div>
                </div>
            `)
                .style('left', (event.pageX + 12) + 'px')
                .style('top', (event.pageY - 28) + 'px');
        })
        .on('mouseout', function() {
            d3.select(this)
                .style('opacity', 0.8)
                .style('stroke-width', '0.5');

            tooltip.transition()
                .duration(500)
                .style('opacity', 0);
        });

    // Add legend
    const legend = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width - 220}, ${height - 80})`);

    const gradient = svg.append('defs')
        .append('linearGradient')
        .attr('id', 'score-gradient')
        .attr('x1', '0%')
        .attr('y1', '0%')
        .attr('x2', '100%')
        .attr('y2', '0%');

    gradient.selectAll('stop')
        .data([
            {offset: '0%', color: '#ef4444'},
            {offset: '25%', color: '#ff8a00'},
            {offset: '50%', color: '#fef3c7'},
            {offset: '75%', color: '#84cc16'},
            {offset: '100%', color: '#22c55e'}
        ])
        .enter()
        .append('stop')
        .attr('offset', d => d.offset)
        .attr('stop-color', d => d.color);

    legend.append('rect')
        .attr('width', 200)
        .attr('height', 20)
        .style('fill', 'url(#score-gradient)');

    legend.append('text')
        .attr('x', 0)
        .attr('y', 40)
        .text('0')
        .style('font-size', '12px');

    legend.append('text')
        .attr('x', 100)
        .attr('y', 40)
        .text('50')
        .style('font-size', '12px')
        .style('text-anchor', 'middle');

    legend.append('text')
        .attr('x', 200)
        .attr('y', 40)
        .text('100')
        .style('font-size', '12px')
        .style('text-anchor', 'end');
}

// Initialize map when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeMap();
    
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(initializeMap, 250);
    });
});
async function fetchCountryScores() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/country-scores/');
        if (!response.ok) throw new Error('Failed to fetch scores');
        const data = await response.json();
        window.countryScores = data;
        console.log('Fetched scores:', data); // Debug log
        return data;
    } catch (error) {
        console.error('Error fetching scores:', error);
        return null;
    }
}

async function initializeMap() {
    // Fetch latest scores from API
    await fetchCountryScores();
    
    // Debug check
    console.log('Country scores loaded:', window.countryScores);
    // Color scale for economic scores
    const colorScale = d3.scaleLinear()
        .domain([0, 25, 50, 75, 100])
        .range(['#ef4444', '#ff8a00', '#fef3c7', '#84cc16', '#22c55e'])
        .clamp(true);

    // ISO3 to country name mapping (explicit mapping to avoid external API calls)
    const countryMapping = {
        'RUS': 'Russia',
        'USA': 'United States',
        'CHN': 'China',
        'GBR': 'United Kingdom',
        // Add more mappings as needed
    };

    // Create tooltip div if it doesn't exist
    let tooltip = d3.select('#map-tooltip');
    if (tooltip.empty()) {
        tooltip = d3.select('body').append('div')
            .attr('id', 'map-tooltip')
            .attr('class', 'country-tooltip')
            .style('opacity', 0)
            .style('position', 'absolute')
            .style('pointer-events', 'none')
            .style('z-index', 10000);
    }

    const mapContainer = document.getElementById('worldMap');
    if (!mapContainer) return;

    const width = mapContainer.clientWidth || 960;
    const height = mapContainer.clientHeight || 600;

    // Clear existing content
    mapContainer.innerHTML = '';

    const svg = d3.select(mapContainer)
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', `0 0 ${width} ${height}`)
        .style('display', 'block');

    // Load world map data
    const worldData = await d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json');
    const features = topojson.feature(worldData, worldData.objects.countries).features;

    // Create map projection
    const projection = d3.geoNaturalEarth1()
        .scale(width / 6.5)
        .translate([width / 2, height / 2]);

    const path = d3.geoPath().projection(projection);

    // Draw countries
    svg.selectAll('path')
        .data(features)
        .enter()
        .append('path')
        .attr('d', path)
        .attr('fill', d => {
            const iso3 = d.properties.iso_a3;
            const score = window.countryScores?.[iso3];
            // Debug log
            console.log('Coloring country:', { 
                name: d.properties.name,
                iso3: iso3, 
                score: score,
                color: score !== undefined ? colorScale(score) : '#ccc'
            });
            return score !== undefined ? colorScale(score) : '#ccc';
        })
        .attr('stroke', '#fff')
        .attr('stroke-width', '0.5')
        .on('mouseover', function(event, d) {
            const iso3 = d.properties.iso_a3;
            const score = window.countryScores[iso3];
            const countryName = d.properties.name || countryMapping[iso3] || iso3;

            d3.select(this)
                .style('opacity', 1)
                .style('stroke-width', '2')
                .raise();

            tooltip.transition()
                .duration(200)
                .style('opacity', .9);

            tooltip.html(`
                <div style="background: rgba(15, 23, 42, 0.95); padding: 12px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-weight: 700; margin-bottom: 6px; color: #fff;">
                        ${countryName}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-bottom: 8px;">
                        <div style="font-size: 12px; color: #94a3b8">Economic Score:</div>
                        <div style="font-size: 20px; font-weight: 800; color: ${score !== undefined ? colorScale(score) : '#94a3b8'}">
                            ${score !== undefined ? score.toFixed(1) : 'N/A'}
                        </div>
                    </div>
                    <div style="height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden;">
                        <div style="height: 100%; width: ${score !== undefined ? score : 0}%; background: ${score !== undefined ? colorScale(score) : '#94a3b8'}; transition: width 0.3s ease;"></div>
                    </div>
                    <div style="color: #64748b; font-size: 11px; margin-top: 8px;">
                        ISO Code: ${iso3 || 'Unknown'}
                    </div>
                </div>
            `)
                .style('left', (event.pageX + 12) + 'px')
                .style('top', (event.pageY - 28) + 'px');
        })
        .on('mouseout', function() {
            d3.select(this)
                .style('opacity', 0.8)
                .style('stroke-width', '0.5');

            tooltip.transition()
                .duration(500)
                .style('opacity', 0);
        });

    // Add legend
    const legend = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width - 220}, ${height - 80})`);

    const gradient = svg.append('defs')
        .append('linearGradient')
        .attr('id', 'score-gradient')
        .attr('x1', '0%')
        .attr('y1', '0%')
        .attr('x2', '100%')
        .attr('y2', '0%');

    gradient.selectAll('stop')
        .data([
            {offset: '0%', color: '#ef4444'},
            {offset: '25%', color: '#ff8a00'},
            {offset: '50%', color: '#fef3c7'},
            {offset: '75%', color: '#84cc16'},
            {offset: '100%', color: '#22c55e'}
        ])
        .enter()
        .append('stop')
        .attr('offset', d => d.offset)
        .attr('stop-color', d => d.color);

    legend.append('rect')
        .attr('width', 200)
        .attr('height', 20)
        .style('fill', 'url(#score-gradient)');

    legend.append('text')
        .attr('x', 0)
        .attr('y', 40)
        .text('0')
        .style('font-size', '12px');

    legend.append('text')
        .attr('x', 100)
        .attr('y', 40)
        .text('50')
        .style('font-size', '12px')
        .style('text-anchor', 'middle');

    legend.append('text')
        .attr('x', 200)
        .attr('y', 40)
        .text('100')
        .style('font-size', '12px')
        .style('text-anchor', 'end');
}

// Initialize map when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeMap();
    
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(initializeMap, 250);
    });
});
