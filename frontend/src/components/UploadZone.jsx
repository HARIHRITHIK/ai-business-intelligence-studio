import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export default function UploadZone({ onUpload }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles?.length > 0) {
      onUpload(acceptedFiles[0]);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    maxSize: 52428800, // 50MB
    multiple: false
  });

  return (
    <div 
      {...getRootProps()} 
      style={{
        border: `2px dashed ${isDragActive ? 'var(--accent-blue)' : isDragReject ? 'var(--danger)' : 'var(--border)'}`,
        borderRadius: '16px',
        padding: '3rem 2rem',
        textAlign: 'center',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        background: isDragActive ? 'rgba(79, 142, 247, 0.05)' : 'var(--bg-card)',
        boxShadow: isDragActive ? '0 0 20px rgba(79, 142, 247, 0.2)' : 'none',
      }}
    >
      <input {...getInputProps()} />
      <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>
        {isDragActive ? '✨' : isDragReject ? '❌' : '☁️'}
      </div>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', fontWeight: 600 }}>
        {isDragActive ? 'Drop it!' : 'Drag & drop your data here'}
      </h3>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
        CSV or Excel · Max 50MB
      </p>
      <div style={{ marginTop: '1.5rem' }}>
        <button className="btn btn-primary" type="button">
          Browse Files
        </button>
      </div>
    </div>
  );
}
