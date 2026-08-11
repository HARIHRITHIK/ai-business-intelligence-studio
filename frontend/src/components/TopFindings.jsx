import React from 'react';

const getSeverityColor = (severity) => {
  switch (severity?.toLowerCase()) {
    case 'positive': return 'var(--success)';
    case 'critical': return 'var(--danger)';
    case 'warning': return 'var(--warning)';
    case 'info': return 'var(--info)';
    default: return 'var(--accent-blue)';
  }
};

const getSeverityLabel = (severity) => {
  switch (severity?.toLowerCase()) {
    case 'positive': return '✓ Positive';
    case 'critical': return '⚠ Critical';
    case 'warning': return '↘ Watch';
    case 'info': return 'ℹ Info';
    default: return 'Insight';
  }
};

export default function TopFindings({ findings = [], loading }) {
  if (loading || !findings.length) {
    return (
      <div className="section-header">
        <h2>Top Findings</h2>
        <p>The most important patterns in your data</p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
          {[1, 2, 3].map(i => (
            <div key={i} className="glass-card skeleton shimmer" style={{ height: '200px' }} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="section-header">
        <h2>Top Findings</h2>
        <p>The most important patterns in your data</p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
        {findings.map((finding, idx) => (
          <div 
            key={idx} 
            className="glass-card animate-in" 
            style={{ 
              animationDelay: `${idx * 200}ms`,
              borderTop: `3px solid ${getSeverityColor(finding.severity)}`
            }}
          >
            <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>{finding.icon || '💡'}</div>
            <div style={{ marginBottom: '0.75rem' }}>
              <span 
                className="badge" 
                style={{ 
                  backgroundColor: `${getSeverityColor(finding.severity)}20`,
                  color: getSeverityColor(finding.severity)
                }}
              >
                {getSeverityLabel(finding.severity)}
              </span>
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.75rem', lineHeight: 1.4 }}>
              {finding.headline}
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.5 }}>
              {finding.explanation}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
