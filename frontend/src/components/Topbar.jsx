import React from 'react';

export default function Topbar({ filename, qualityScore, onNewAnalysis, loading }) {
  let qualityColor = 'var(--success)';
  if (qualityScore < 60) qualityColor = 'var(--danger)';
  else if (qualityScore < 80) qualityColor = 'var(--warning)';

  return (
    <header style={{
      height: '64px',
      background: 'rgba(13, 21, 38, 0.8)',
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid var(--border)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 2rem',
      position: 'sticky',
      top: 0,
      zIndex: 9
    }}>
      <div style={{ width: '200px' }}>
        {/* Logo space if no sidebar, but we rely on sidebar mostly */}
      </div>

      <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '1rem' }}>
        {filename && (
          <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>📄</span> {filename}
          </span>
        )}
        {!loading && qualityScore !== undefined && (
          <span className="badge" style={{ backgroundColor: `${qualityColor}20`, color: qualityColor }}>
            Quality: {qualityScore}/100
          </span>
        )}
      </div>

      <div style={{ width: '200px', display: 'flex', justifyContent: 'flex-end' }}>
        {onNewAnalysis && (
          <button className="btn btn-ghost" style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }} onClick={onNewAnalysis}>
            New Analysis
          </button>
        )}
      </div>
    </header>
  );
}
