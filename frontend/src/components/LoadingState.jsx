import React, { useState, useEffect } from 'react';

export default function LoadingState() {
  const [showColdStartNotice, setShowColdStartNotice] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowColdStartNotice(true);
    }, 4000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
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
      
      <div style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '1rem' }}>
        <div className="spinner" style={{ fontSize: '2rem', marginBottom: '0.75rem', display: 'inline-block' }}>⚙️</div>
        <p style={{ fontSize: '1rem', fontWeight: 500, color: 'var(--text-primary)' }}>
          Profiling dataset and calculating statistical patterns...
        </p>
        {showColdStartNotice && (
          <p className="animate-in" style={{ fontSize: '0.85rem', color: 'var(--accent-blue)', marginTop: '0.5rem' }}>
            ☁️ Initializing service (free cloud instances may take ~15–20s to wake up on first launch).
          </p>
        )}
      </div>
    </div>
  );
}
