import React from 'react';

export default function LoadingState() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '4rem' }}>
      <div>
        <div style={{ width: '200px', height: '32px', marginBottom: '1rem' }} className="skeleton shimmer" />
        <div style={{ width: '300px', height: '20px', marginBottom: '2rem' }} className="skeleton shimmer" />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
          {[1, 2, 3].map(i => (
            <div key={i} className="glass-card skeleton shimmer" style={{ height: '220px' }} />
          ))}
        </div>
      </div>

      <div>
        <div style={{ width: '250px', height: '32px', marginBottom: '2rem' }} className="skeleton shimmer" />
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {[1, 2].map(i => (
            <div key={i} className="glass-card skeleton shimmer" style={{ height: '140px' }} />
          ))}
        </div>
      </div>
      
      <div style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '2rem' }}>
        <div className="spinner" style={{ fontSize: '2rem', marginBottom: '1rem', display: 'inline-block' }}>⚙️</div>
        <p>Analyzing data patterns and extracting insights...</p>
      </div>
    </div>
  );
}
