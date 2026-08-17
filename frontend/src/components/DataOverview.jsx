import React, { useState } from 'react';

const getTypeIcon = (type) => {
  if (type === 'numerical') return '📊';
  if (type === 'datetime') return '📅';
  if (type === 'id') return '🔑';
  return '🏷️';
};

export default function DataOverview({ overview, loading }) {
  const [showTable, setShowTable] = useState(true);
  const [selectedCol, setSelectedCol] = useState(null);

  if (loading || !overview) {
    return (
      <div className="section-header">
        <h2>Data Overview</h2>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
          {[1,2,3,4].map(i => <div key={i} className="stat-pill skeleton shimmer" style={{ flex: 1, height: '80px' }} />)}
        </div>
      </div>
    );
  }

  const rows = overview?.rows;
  const columns = overview?.columns;
  const qualityScore = overview?.quality_score ?? 0;
  const fileSize = overview?.memory_mb != null ? `${overview.memory_mb} MB` : 'N/A';
  const dataPreview = overview?.preview || [];
  const columnTypes = overview?.column_types || {};
  const missingSummary = overview?.missing_summary || [];
  const columnProfiles = overview?.column_profiles || {};

  // Build full column list
  const columnList = Object.keys(columnTypes).map(col => {
    const missingItem = missingSummary.find(m => m.column === col);
    const missingPct = missingItem ? missingItem.missing_pct : 0;
    return {
      name: col,
      type: columnTypes[col],
      completeness: Math.round(100 - missingPct),
      profile: columnProfiles[col] || {}
    };
  });

  let qualityColor = 'var(--success)';
  if (qualityScore < 60) qualityColor = 'var(--danger)';
  else if (qualityScore < 80) qualityColor = 'var(--warning)';

  const activeProfile = selectedCol ? columnProfiles[selectedCol] : null;
  const activeType = selectedCol ? columnTypes[selectedCol] : null;

  return (
    <div>
      <div className="section-header" style={{ marginBottom: '1.5rem' }}>
        <h2>Data Overview</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
          Structural dataset profile, completeness metrics, and exploratory preview.
        </p>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="stat-pill">
          <span className="label">Total Records</span>
          <span className="value">{rows?.toLocaleString()}</span>
        </div>
        <div className="stat-pill">
          <span className="label">Total Columns</span>
          <span className="value">{columns}</span>
        </div>
        <div className="stat-pill">
          <span className="label">Quality Score</span>
          <span className="value" style={{ color: qualityColor }}>{qualityScore}/100</span>
        </div>
        <div className="stat-pill">
          <span className="label">Memory Footprint</span>
          <span className="value">{fileSize}</span>
        </div>
      </div>

      <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600, margin: 0 }}>Column Profiles & Data Health</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              Click any column below to inspect detailed statistics.
            </p>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.75rem', marginBottom: selectedCol ? '1.5rem' : '0' }}>
          {columnList.map((col, i) => {
            const isSelected = selectedCol === col.name;
            return (
              <div 
                key={i} 
                onClick={() => setSelectedCol(isSelected ? null : col.name)}
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.75rem', 
                  padding: '0.75rem', 
                  background: isSelected ? 'rgba(79, 142, 247, 0.15)' : 'rgba(255,255,255,0.02)', 
                  border: isSelected ? '1px solid var(--accent-blue)' : '1px solid rgba(255,255,255,0.05)',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                <span style={{ fontSize: '1.25rem' }}>{getTypeIcon(col.type)}</span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <span style={{ fontSize: '0.85rem', fontWeight: isSelected ? 600 : 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {col.name}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{col.completeness}%</span>
                  </div>
                  <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: `${col.completeness}%`, background: col.completeness < 80 ? 'var(--warning)' : 'var(--accent-blue)' }} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {selectedCol && activeProfile && (
          <div className="animate-in" style={{ padding: '1rem 1.25rem', background: 'rgba(0,0,0,0.25)', borderRadius: '8px', border: '1px solid var(--border)', marginTop: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <span style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--accent-blue)' }}>
                {getTypeIcon(activeType)} {selectedCol} ({activeType})
              </span>
              <button 
                className="btn btn-ghost" 
                style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem' }}
                onClick={() => setSelectedCol(null)}
              >
                ✕ Close
              </button>
            </div>
            
            {activeType === 'numerical' && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1.5rem', fontSize: '0.85rem' }}>
                <div><span style={{ color: 'var(--text-muted)' }}>Mean:</span> <strong style={{ fontFamily: 'Fira Code' }}>{activeProfile.mean?.toFixed(2) ?? 'N/A'}</strong></div>
                <div><span style={{ color: 'var(--text-muted)' }}>Median:</span> <strong style={{ fontFamily: 'Fira Code' }}>{activeProfile.median?.toFixed(2) ?? 'N/A'}</strong></div>
                <div><span style={{ color: 'var(--text-muted)' }}>Min:</span> <strong style={{ fontFamily: 'Fira Code' }}>{activeProfile.min?.toFixed(2) ?? 'N/A'}</strong></div>
                <div><span style={{ color: 'var(--text-muted)' }}>Max:</span> <strong style={{ fontFamily: 'Fira Code' }}>{activeProfile.max?.toFixed(2) ?? 'N/A'}</strong></div>
                <div><span style={{ color: 'var(--text-muted)' }}>Std Dev:</span> <strong style={{ fontFamily: 'Fira Code' }}>{activeProfile.std?.toFixed(2) ?? 'N/A'}</strong></div>
                <div><span style={{ color: 'var(--text-muted)' }}>Skewness:</span> <strong style={{ fontFamily: 'Fira Code' }}>{activeProfile.skew?.toFixed(2) ?? 'N/A'}</strong></div>
              </div>
            )}

            {activeType === 'categorical' && activeProfile.top_values && (
              <div style={{ fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--text-muted)', marginRight: '0.5rem' }}>Top Categories:</span>
                {Object.entries(activeProfile.top_values).map(([val, cnt], idx) => (
                  <span key={idx} className="badge" style={{ marginRight: '0.5rem', background: 'rgba(255,255,255,0.05)', color: 'var(--text-primary)' }}>
                    {val}: <strong style={{ color: 'var(--accent-blue)' }}>{cnt}</strong>
                  </span>
                ))}
              </div>
            )}

            {activeType === 'datetime' && (
              <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.85rem' }}>
                <div><span style={{ color: 'var(--text-muted)' }}>Start Date:</span> <strong>{activeProfile.min_date ? activeProfile.min_date.split('T')[0] : 'N/A'}</strong></div>
                <div><span style={{ color: 'var(--text-muted)' }}>End Date:</span> <strong>{activeProfile.max_date ? activeProfile.max_date.split('T')[0] : 'N/A'}</strong></div>
                <div><span style={{ color: 'var(--text-muted)' }}>Timespan:</span> <strong>{activeProfile.date_range_days ?? 0} days</strong></div>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="glass-card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: showTable ? '1.25rem' : '0' }}>
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600, margin: 0 }}>Data Sample Preview</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              Showing first {dataPreview.length} rows of raw structured data.
            </p>
          </div>
          <button 
            className="btn btn-secondary" 
            style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }} 
            onClick={() => setShowTable(!showTable)}
          >
            {showTable ? 'Hide Table ↑' : 'Show Table ↓'}
          </button>
        </div>

        {showTable && dataPreview.length > 0 && (
          <div style={{ overflowX: 'auto', borderRadius: '8px', border: '1px solid var(--border)' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.825rem' }}>
              <thead>
                <tr style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border)' }}>
                  {columnList.map((col, i) => (
                    <th key={i} style={{ padding: '0.75rem 1rem', textAlign: 'left', color: 'var(--text-secondary)', fontWeight: 600, whiteSpace: 'nowrap' }}>
                      <span style={{ marginRight: '0.4rem' }}>{getTypeIcon(col.type)}</span>
                      {col.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {dataPreview.map((row, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)', background: i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.01)' }}>
                    {columnList.map((col, j) => (
                      <td key={j} style={{ padding: '0.65rem 1rem', color: 'var(--text-primary)', fontFamily: col.type === 'numerical' ? 'Fira Code' : 'Inter', whiteSpace: 'nowrap' }}>
                        {String(row[col.name] ?? '—')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
