import React from 'react';
import EvidenceChart from './EvidenceChart';

export default function EvidenceSection({ charts = [], loading }) {
  if (loading || !charts.length) {
    return (
      <div className="section-header">
        <h2>Supporting Evidence</h2>
        <p>Data supporting the insights above</p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
          {[1,2].map(i => <div key={i} className="glass-card skeleton shimmer" style={{ height: '350px' }} />)}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="section-header">
        <h2>Supporting Evidence</h2>
        <p>Data supporting the insights above</p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>
        {charts.map((chart, idx) => (
          <div key={idx} className="glass-card animate-in" style={{ animationDelay: `${idx * 150}ms`, padding: '1.5rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 500, marginBottom: '1rem' }}>{chart.title}</h3>
            <EvidenceChart chartData={chart} height={300} />
          </div>
        ))}
      </div>
    </div>
  );
}
