import React from 'react';
import UploadZone from './UploadZone';

export default function LandingHero({ onUpload, onLoadSample }) {
  const samples = [
    { id: 'retail_sales',     icon: '🛍️', title: 'Retail Sales',    desc: 'Revenue, regional performance and product trends' },
    { id: 'hr_analytics',     icon: '👥', title: 'HR Analytics',     desc: 'Employee attrition, performance and compensation patterns' },
    { id: 'customer_churn',   icon: '📊', title: 'Customer Churn',   desc: 'Retention drivers, contract analysis and churn prediction' }
  ];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative', overflow: 'hidden', padding: '2rem' }}>
      <div className="orb" style={{ top: '10%', left: '20%', width: '400px', height: '400px', background: 'var(--accent-blue)' }}></div>
      <div className="orb" style={{ bottom: '10%', right: '20%', width: '350px', height: '350px', background: 'var(--accent-violet)', animationDelay: '-4s' }}></div>
      <div className="orb" style={{ top: '40%', left: '50%', width: '300px', height: '300px', background: 'var(--info)', transform: 'translate(-50%, -50%)', animationDelay: '-2s' }}></div>

      <div style={{ textAlign: 'center', maxWidth: '800px', zIndex: 1, marginBottom: '3rem' }}>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '2rem' }}>
          <span className="badge badge-success">Instant Insights</span>
          <span className="badge badge-info">No Setup Required</span>
          <span className="badge badge-warning">Export Ready</span>
        </div>
        <h1 style={{ fontSize: '4rem', fontWeight: 700, letterSpacing: '-0.02em', marginBottom: '1.5rem', lineHeight: 1.1 }}>
          <span style={{ background: 'var(--accent-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Your Data Has a Story.
          </span>
          <br />Let AI Tell It.
        </h1>
        <p style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', lineHeight: 1.6, maxWidth: '600px', margin: '0 auto' }}>
          Upload any business dataset and get executive-level insights in seconds — no data science degree required.
        </p>
      </div>

      <div style={{ width: '100%', maxWidth: '600px', zIndex: 1, marginBottom: '4rem' }}>
        <UploadZone onUpload={onUpload} />
      </div>

      <div style={{ width: '100%', maxWidth: '1000px', zIndex: 1 }}>
        <h3 style={{ textAlign: 'center', color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
          Or explore with a sample dataset
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
          {samples.map(sample => (
            <div key={sample.id} className="glass-card" style={{ display: 'flex', flexDirection: 'column' }}>
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>{sample.icon}</div>
              <h4 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.5rem' }}>{sample.title}</h4>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1.5rem', flex: 1 }}>{sample.desc}</p>
              <button className="btn btn-secondary" style={{ width: '100%' }} onClick={() => onLoadSample(sample.id)}>
                Load Sample →
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
