import React, { useState } from 'react';

const getTypeIcon = (type) => {
  if (type === 'numerical') return '📊';
  if (type === 'datetime') return '📅';
  return '🏷️';
};

export default function DataOverview({ overview, loading }) {
  const [showTable, setShowTable] = useState(false);

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

  // Build column list stats
  const columnList = Object.keys(columnTypes).map(col => {
    const missingItem = missingSummary.find(m => m.column === col);
    const missingPct = missingItem ? missingItem.missing_pct : 0;
    return {
      name: col,
      type: columnTypes[col],
      completeness: Math.round(100 - missingPct)
    };
  });

  let qualityColor = 'var(--success)';
  if (qualityScore < 60) qualityColor = 'var(--danger)';
  else if (qualityScore < 80) qualityColor = 'var(--warning)';

  return (
    <div>
      <div className="section-header" style={{ marginBottom: '1.5rem' }}>
        <h2>Data Overview</h2>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
        <div className="stat-pill">
          <span className="label">Rows</span>
          <span className="value">{rows?.toLocaleString()}</span>
        </div>
        <div className="stat-pill">
          <span className="label">Columns</span>
          <span className="value">{columns}</span>
        </div>
        <div className="stat-pill">
          <span className="label">Quality Score</span>
          <span className="value" style={{ color: qualityColor }}>{qualityScore}/100</span>
        </div>
        <div className="stat-pill">
          <span className="label">Memory Size</span>
          <span className="value">{fileSize}</span>
        </div>
      </div>

      <div className="glass-card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: showTable ? '1.5rem' : '0' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Data Preview & Columns</h3>
          <button className="btn btn-ghost" style={{ padding: '0.25rem 0.5rem', fontSize: '0.875rem' }} onClick={() => setShowTable(!showTable)}>
            {showTable ? 'Hide Preview ↑' : 'Show Preview ↓'}
          </button>
        </div>

        {showTable && dataPreview.length > 0 && (
          <div style={{ overflowX: 'auto', marginBottom: '1.5rem' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border)' }}>
                  {columnList.slice(0, 8).map((col, i) => (
                    <th key={i} style={{ padding: '0.75rem', textAlign: 'left', color: 'var(--text-secondary)', fontWeight: 500, whiteSpace: 'nowrap' }}>
                      <span style={{ marginRight: '0.5rem' }}>{getTypeIcon(col.type)}</span>
                      {col.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {dataPreview.slice(0, 5).map((row, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.02)' }}>
                    {columnList.slice(0, 8).map((col, j) => (
                      <td key={j} style={{ padding: '0.75rem', color: 'var(--text-primary)', fontFamily: col.type === 'numerical' ? 'Fira Code' : 'Inter', whiteSpace: 'nowrap' }}>
                        {String(row[col.name] ?? '')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          {columnList.slice(0, 8).map((col, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.75rem', background: 'rgba(255,255,255,0.02)', borderRadius: '8px' }}>
              <span style={{ fontSize: '1.25rem' }}>{getTypeIcon(col.type)}</span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                  <span style={{ fontSize: '0.875rem', fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{col.name}</span>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{col.completeness}%</span>
                </div>
                <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${col.completeness}%`, background: col.completeness < 80 ? 'var(--warning)' : 'var(--accent-blue)' }} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
