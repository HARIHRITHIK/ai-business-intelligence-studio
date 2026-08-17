import React, { useState } from 'react';
import EvidenceChart from './EvidenceChart';

export default function PredictionStudio({ overview, prediction, loading, error, onPredict }) {
  const [targetCol, setTargetCol] = useState('');

  const colTypes = overview?.column_types || {};
  const numCols = Object.keys(colTypes).filter(c => colTypes[c] === 'numerical' || colTypes[c] === 'categorical');

  const confidenceVal = prediction?.metric_value != null ? Math.max(0, Math.round(prediction.metric_value * 100)) : 0;

  return (
    <div>
      <div className="section-header" style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
        <h2 style={{ margin: 0 }}>Prediction Studio</h2>
        <span className="badge badge-info">AutoML Lite</span>
      </div>
      
      <div className="glass-card" style={{ padding: '1.75rem' }}>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.5 }}>
          Select a business target metric to train an automated predictive pattern model and identify the primary key drivers.
        </p>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap', marginBottom: (prediction || error) ? '2rem' : '0' }}>
          <select 
            value={targetCol} 
            onChange={(e) => setTargetCol(e.target.value)}
            style={{ 
              padding: '0.75rem 1rem', 
              borderRadius: '8px', 
              background: 'rgba(255,255,255,0.05)', 
              border: '1px solid var(--border)', 
              color: 'var(--text-primary)',
              fontFamily: 'Inter',
              flex: '1 1 240px',
              maxWidth: '320px'
            }}
          >
            <option value="" style={{ background: '#0d1526', color: '#94a3b8' }}>Select target column...</option>
            {numCols.map(c => (
              <option key={c} value={c} style={{ background: '#0d1526', color: '#f1f5f9' }}>
                {colTypes[c] === 'numerical' ? '📊' : '🏷️'} {c}
              </option>
            ))}
          </select>
          <button 
            className="btn btn-primary" 
            onClick={() => onPredict(targetCol)}
            disabled={!targetCol || loading}
          >
            {loading ? <span className="spinner" style={{ display: 'inline-block', marginRight: '0.5rem' }}>↻</span> : null}
            {loading ? 'Analyzing Patterns...' : 'Analyze Drivers'}
          </button>
        </div>

        {error && !loading && (
          <div className="animate-in" style={{ padding: '0.75rem 1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger)', borderRadius: '8px', color: 'var(--danger)', fontSize: '0.9rem', marginBottom: '1rem' }}>
            ⚠️ Analysis Notice: {error}
          </div>
        )}

        {prediction && !loading && (
          <div className="animate-in" style={{ borderTop: '1px solid var(--border)', paddingTop: '2rem' }}>
            <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap', marginBottom: '2rem' }}>
              <div className="stat-pill" style={{ flex: '0 0 160px' }}>
                <span className="label">{prediction.metric_name || 'Model Confidence'}</span>
                <span className="value" style={{ color: 'var(--accent-violet)' }}>{confidenceVal}%</span>
              </div>
              <div style={{ flex: 1, minWidth: '260px' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.5rem' }}>Executive Driver Analysis</h3>
                <p style={{ color: 'var(--text-secondary)', lineHeight: 1.5, fontSize: '0.95rem' }}>{prediction.plain_english}</p>
                
                {prediction.feature_importances?.length > 0 && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '1rem' }}>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', alignSelf: 'center' }}>Top Drivers:</span>
                    {prediction.feature_importances.slice(0, 4).map((f, idx) => (
                      <span key={idx} className="badge" style={{ background: 'rgba(155, 89, 229, 0.15)', color: '#c084fc', border: '1px solid rgba(155, 89, 229, 0.3)' }}>
                        #{idx + 1} {f.feature} ({Math.round(f.importance * 100)}%)
                      </span>
                    ))}
                  </div>
                )}

                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.75rem' }}>
                  Model Pipeline: <span style={{ fontFamily: 'Fira Code', color: 'var(--text-secondary)' }}>{prediction.best_model}</span> (StandardScaler + Cross-Validated)
                </p>
              </div>
            </div>
            
            {prediction.feature_chart && (
              <div style={{ height: '350px', background: 'rgba(0,0,0,0.2)', borderRadius: '12px', padding: '1rem', border: '1px solid var(--border)' }}>
                <EvidenceChart chartData={prediction.feature_chart} height={320} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
