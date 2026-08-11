import React from 'react';

export default function Sidebar({ filename, activeSection, onNewAnalysis, dataOverview }) {
  const navItems = [
    { id: 'top-findings', icon: '🔍', label: 'Top Findings' },
    { id: 'data-overview', icon: '📋', label: 'Data Overview' },
    { id: 'key-insights', icon: '💡', label: 'Key Insights' },
    { id: 'supporting-evidence', icon: '📊', label: 'Supporting Evidence' },
    { id: 'recommendations', icon: '🎯', label: 'Recommendations' },
    { id: 'prediction-studio', icon: '🔮', label: 'Prediction Studio', optional: true },
    { id: 'export-report', icon: '📄', label: 'Export Report' }
  ];

  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <aside style={{
      width: '260px',
      height: '100vh',
      position: 'fixed',
      left: 0,
      top: 0,
      background: 'var(--bg-secondary)',
      borderRight: '1px solid var(--border)',
      display: 'flex',
      flexDirection: 'column',
      padding: '1.5rem',
      zIndex: 10
    }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '1.25rem', fontWeight: 700, margin: 0 }}>
          <span style={{ background: 'var(--accent-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            BI Studio
          </span>
        </h1>
        <div style={{ marginTop: '1rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          <div style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', marginBottom: '0.25rem' }}>
            📄 {filename || 'No file loaded'}
          </div>
          {dataOverview && (
            <div style={{ fontFamily: 'Fira Code', fontSize: '0.75rem', opacity: 0.7 }}>
              {dataOverview.rows} × {dataOverview.columns}
            </div>
          )}
        </div>
      </div>

      <nav style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {navItems.map(item => (
          <button
            key={item.id}
            onClick={() => scrollTo(item.id)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              padding: '0.75rem 1rem',
              borderRadius: '8px',
              border: 'none',
              background: activeSection === item.id ? 'rgba(255,255,255,0.05)' : 'transparent',
              color: activeSection === item.id ? 'var(--text-primary)' : 'var(--text-secondary)',
              cursor: 'pointer',
              textAlign: 'left',
              fontFamily: 'Inter',
              fontWeight: activeSection === item.id ? 500 : 400,
              transition: 'all 0.2s',
              position: 'relative'
            }}
          >
            <span style={{ fontSize: '1.1rem' }}>{item.icon}</span>
            <span style={{ flex: 1 }}>{item.label}</span>
            {item.optional && <span className="badge badge-info" style={{ fontSize: '0.6rem', padding: '0.1rem 0.4rem' }}>OPT</span>}
            {activeSection === item.id && (
              <div style={{ position: 'absolute', left: 0, top: '20%', bottom: '20%', width: '3px', background: 'var(--accent-blue)', borderRadius: '0 4px 4px 0' }} />
            )}
          </button>
        ))}
      </nav>

      <div style={{ marginTop: 'auto', paddingTop: '1.5rem' }}>
        <button className="btn btn-secondary" style={{ width: '100%' }} onClick={onNewAnalysis}>
          + New Analysis
        </button>
      </div>
    </aside>
  );
}
