import React, { useState } from 'react';
import EvidenceChart from './EvidenceChart';

const getCategoryColor = (category) => {
  switch (category?.toLowerCase()) {
    case 'trend': return 'var(--accent-blue)';
    case 'anomaly': return 'var(--warning)';
    case 'segment': return 'var(--accent-violet)';
    case 'correlation': return 'var(--info)';
    case 'warning': return 'var(--danger)';
    default: return 'var(--text-secondary)';
  }
};

export default function InsightsList({ insights = [], loading }) {
  const [expandedId, setExpandedId] = useState(null);

  if (loading || !insights.length) {
    return (
      <div className="section-header">
        <h2>Key Business Insights</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1.5rem' }}>
          {[1,2,3].map(i => <div key={i} className="glass-card skeleton shimmer" style={{ height: '120px' }} />)}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="section-header">
        <h2>Key Business Insights</h2>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {insights.map((insight, idx) => (
          <div 
            key={idx} 
            className="glass-card animate-in"
            style={{ 
              animationDelay: `${idx * 100}ms`,
              borderLeft: `4px solid ${getCategoryColor(insight.category)}`,
              padding: '1.5rem'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '2rem' }}>
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                  <span style={{ fontSize: '1.25rem' }}>{insight.icon || '📌'}</span>
                  <span 
                    className="badge" 
                    style={{ 
                      backgroundColor: `${getCategoryColor(insight.category)}20`,
                      color: getCategoryColor(insight.category)
                    }}
                  >
                    {insight.category || 'Insight'}
                  </span>
                </div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.5rem' }}>{insight.headline}</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.5, marginBottom: '0.75rem' }}>
                  {insight.explanation}
                </p>
                {(insight.business_implication || insight.implication) && (
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', fontStyle: 'italic', borderLeft: '2px solid rgba(255,255,255,0.1)', paddingLeft: '0.75rem', marginTop: '0.5rem' }}>
                    💡 <strong style={{ color: 'var(--text-secondary)', fontStyle: 'normal' }}>Strategic Takeaway:</strong> {insight.business_implication || insight.implication}
                  </p>
                )}
              </div>
              
              <button 
                className="btn btn-ghost" 
                style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem', color: 'var(--accent-blue)', whiteSpace: 'nowrap' }}
                onClick={() => document.getElementById('supporting-evidence')?.scrollIntoView({ behavior: 'smooth' })}
              >
                View Evidence ↓
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
