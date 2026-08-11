import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

export default function EvidenceChart({ chartData, height = 300 }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!chartData) return null;
  if (!mounted) return <div className="skeleton shimmer" style={{ width: '100%', height: `${height}px`, borderRadius: '8px' }} />;

  const figure = chartData.figure || chartData;
  const plotData = figure.data || [];
  const plotLayout = figure.layout || {};

  const baseLayout = {
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { family: 'Inter, sans-serif', color: '#94a3b8' },
    margin: { t: 40, r: 20, b: 40, l: 40 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)' },
    yaxis: { gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)' },
    autosize: true,
    showlegend: true,
    legend: { orientation: 'h', y: -0.2 }
  };

  const finalLayout = { ...baseLayout, ...plotLayout };

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1, minHeight: `${height}px` }}>
        <Plot
          data={plotData}
          layout={finalLayout}
          config={{ displayModeBar: true, displaylogo: false, responsive: true }}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%' }}
        />
      </div>
      {chartData.caption && (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', marginTop: '1rem', fontStyle: 'italic' }}>
          {chartData.caption}
        </p>
      )}
    </div>
  );
}
