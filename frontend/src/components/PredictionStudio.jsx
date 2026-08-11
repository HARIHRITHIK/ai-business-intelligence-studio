import React, { useState } from 'react';
import EvidenceChart from './EvidenceChart';

export default function PredictionStudio({ overview, prediction, loading, onPredict }) {
  const [targetCol, setTargetCol] = useState('');

  const colTypes = overview?.column_types || {};
  const numCols = Object.keys(colTypes).filter(c => colTypes[c] === 'numerical' || colTypes[c] === 'categorical');

  const confidenceVal = prediction?.metric_value != null ? Math.max(0, Math.round(prediction.metric_value * 100)) : 0;

  return (
    <div>
      <div className="section-header" style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
        <h2 style={{ margin: 0 }}>Prediction Studio</h2>
        <span className="badge badge-info">Optional</span>
      </div>
      
      <div className="glass-card">
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Select a target column to analyze which factors most strongly drive it.
        </p>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: prediction ? '2rem' : '0' }}>
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
              flex: 1,
              maxWidth: '300px'
            }}
          >
            <option value="" style={{ background: '#0d1526', color: '#94a3b8' }}>Select target column...</option>
            {numCols.map(c => (
              <option key={c} value={c} style={{ background: '#0d1526', color: '#f1f5f9' }}>{c}</option>
            ))}
          </select>
          <button 
            className="btn btn-primary" 
            onClick={() => onPredict(targetCol)}
            disabled={!targetCol || loading}
          >
            {loading ? <span className="spinner" style={{ display: 'inline-block', marginRight: '0.5rem' }}>↻</span> : null}
            {loading ? 'Analyzing...' : 'Analyze Drivers'}
          </button>
        </div>

        {prediction && !loading && (
          <div className="animate-in" style={{ borderTop: '1px solid var(--border)', paddingTop: '2rem' }}>
            <div style={{ display: 'flex', gap: '2rem', marginBottom: '2rem' }}>
              <div className="stat-pill" style={{ flex: '0 0 150px' }}>
                <span className="label">{prediction.metric_name || 'Confidence'}</span>
                <span className="value" style={{ color: 'var(--accent-violet)' }}>{confidenceVal}%</span>
              </div>
              <div style={{ flex: 1 }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.5rem' }}>Analysis Results</h3>
                <p style={{ color: 'var(--text-secondary)', lineHeight: 1.5 }}>{prediction.plain_english}</p>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                  Analysis method: <span style={{ fontFamily: 'Fira Code' }}>{prediction.best_model}</span>
                </p>
              </div>
            </div>
            
            {prediction.feature_chart && (
              <div style={{ height: '350px', background: 'rgba(0,0,0,0.2)', borderRadius: '12px', padding: '1rem' }}>
                <EvidenceChart chartData={prediction.feature_chart} height={320} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
