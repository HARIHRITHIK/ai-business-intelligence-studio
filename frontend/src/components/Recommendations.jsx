import React from 'react';

const getImpactColor = (impact) => {
  switch (impact?.toLowerCase()) {
    case 'high': return 'var(--success)';
    case 'medium': return 'var(--warning)';
    case 'low': return 'var(--info)';
    default: return 'var(--accent-blue)';
  }
};

export default function Recommendations({ recommendations = [], loading }) {
  if (loading || !recommendations.length) {
    return (
      <div className="section-header">
        <h2>Business Recommendations</h2>
        <p>Actions based on your data patterns</p>
        <div style={{ display: 'grid', gap: '1rem', marginTop: '1.5rem' }}>
          {[1,2,3].map(i => <div key={i} className="glass-card skeleton shimmer" style={{ height: '100px' }} />)}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="section-header">
        <h2>Business Recommendations</h2>
        <p>Actions based on your data patterns</p>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {recommendations.map((rec, idx) => (
          <div 
            key={idx} 
            className="glass-card animate-in"
            style={{ 
              animationDelay: `${idx * 150}ms`,
              display: 'flex',
              gap: '1.5rem',
              alignItems: 'flex-start',
              borderLeft: `4px solid ${getImpactColor(rec.impact)}`
            }}
          >
            <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--text-muted)', lineHeight: 1, minWidth: '40px', textAlign: 'center' }}>
              {idx + 1}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                <span className="badge" style={{ backgroundColor: `${getImpactColor(rec.impact)}20`, color: getImpactColor(rec.impact) }}>
                  {rec.impact || 'Medium'} Impact
                </span>
                {rec.category && (
                  <span className="badge" style={{ backgroundColor: 'rgba(255,255,255,0.05)', color: 'var(--text-secondary)' }}>
                    {rec.category}
                  </span>
                )}
              </div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.5rem' }}>{rec.action}</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.5 }}>
                {rec.rationale}
              </p>
            </div>
            <div style={{ fontSize: '1.5rem', opacity: 0.5 }}>💡</div>
          </div>
        ))}
      </div>
    </div>
  );
}
