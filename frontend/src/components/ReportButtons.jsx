import React, { useState } from 'react';
import { getReportUrl } from '../utils/api';

export default function ReportButtons({ sessionId }) {
  const [loadingPdf, setLoadingPdf] = useState(false);

  const handleDownloadPdf = () => {
    setLoadingPdf(true);
    // Simulate slight delay before redirect for effect
    setTimeout(() => {
      window.open(getReportUrl(sessionId, 'pdf'), '_blank');
      setLoadingPdf(false);
    }, 800);
  };

  const handleViewHtml = () => {
    window.open(getReportUrl(sessionId, 'html'), '_blank');
  };

  if (!sessionId) return null;

  return (
    <div className="glass-card" style={{ display: 'flex', gap: '1.5rem', justifyContent: 'center', padding: '2rem' }}>
      <button 
        className="btn btn-secondary" 
        onClick={handleViewHtml}
        style={{ padding: '1rem 2rem', fontSize: '1.1rem', minWidth: '200px' }}
      >
        <span style={{ marginRight: '0.5rem' }}>🌐</span> View Full Report
      </button>
      
      <button 
        className="btn btn-primary" 
        onClick={handleDownloadPdf}
        disabled={loadingPdf}
        style={{ padding: '1rem 2rem', fontSize: '1.1rem', minWidth: '200px' }}
      >
        {loadingPdf ? (
          <><span className="spinner" style={{ display: 'inline-block', marginRight: '0.5rem' }}>↻</span> Generating...</>
        ) : (
          <><span style={{ marginRight: '0.5rem' }}>📄</span> Download PDF</>
        )}
      </button>
    </div>
  );
}
