import React, { useState, useEffect } from 'react';
import LandingHero from './components/LandingHero';
import TopFindings from './components/TopFindings';
import DataOverview from './components/DataOverview';
import InsightsList from './components/InsightsList';
import EvidenceSection from './components/EvidenceSection';
import Recommendations from './components/Recommendations';
import PredictionStudio from './components/PredictionStudio';
import ReportButtons from './components/ReportButtons';
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';
import LoadingState from './components/LoadingState';
import { useAnalysis } from './hooks/useAnalysis';

function App() {
  const [view, setView] = useState('landing'); // landing, analyzing, results
  const [activeSection, setActiveSection] = useState('top-findings');
  const [filename, setFilename] = useState('');

  const analysis = useAnalysis();

  useEffect(() => {
    if (view !== 'results') return;

    const sectionIds = [
      'top-findings',
      'data-overview',
      'key-insights',
      'supporting-evidence',
      'recommendations',
      'prediction-studio',
      'export-report'
    ];

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      { rootMargin: '-20% 0px -60% 0px', threshold: 0 }
    );

    sectionIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [view]);

  const handleUpload = async (file) => {
    analysis.resetAnalysis();
    setView('analyzing');
    setFilename(file.name);
    try {
      await analysis.uploadFile(file);
      setView('results');
    } catch (e) {
      console.error(e);
      setView('landing');
    }
  };

  const handleSampleLoad = async (sampleName) => {
    analysis.resetAnalysis();
    setView('analyzing');
    setFilename(`${sampleName}.csv`);
    try {
      await analysis.loadSample(sampleName);
      setView('results');
    } catch (e) {
      console.error(e);
      setView('landing');
    }
  };

  const handleNewAnalysis = () => {
    analysis.resetAnalysis();
    setView('landing');
    setFilename('');
  };

  if (view === 'landing') {
    return <LandingHero onUpload={handleUpload} onLoadSample={handleSampleLoad} />;
  }

  if (view === 'analyzing') {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <Topbar filename={filename} loading={true} />
        <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto', width: '100%' }}>
          <LoadingState />
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar 
        filename={filename} 
        activeSection={activeSection} 
        onNewAnalysis={handleNewAnalysis}
        dataOverview={analysis.overview}
      />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', marginLeft: '260px' }}>
        <Topbar 
          filename={filename} 
          qualityScore={analysis.overview?.quality_score} 
          onNewAnalysis={handleNewAnalysis}
        />
        <main style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
          <div id="top-findings" style={{ marginBottom: '4rem' }}>
            <TopFindings findings={analysis.topFindings} loading={analysis.loading.overview} />
          </div>
          
          <div id="data-overview" style={{ marginBottom: '4rem' }}>
            <DataOverview overview={analysis.overview} loading={analysis.loading.overview} />
          </div>

          <div id="key-insights" style={{ marginBottom: '4rem' }}>
            <InsightsList insights={analysis.insights} loading={analysis.loading.insights} />
          </div>

          <div id="supporting-evidence" style={{ marginBottom: '4rem' }}>
            <EvidenceSection charts={analysis.charts} loading={analysis.loading.charts} />
          </div>

          <div id="recommendations" style={{ marginBottom: '4rem' }}>
            <Recommendations recommendations={analysis.recommendations} loading={analysis.loading.recommendations} />
          </div>

          <div id="prediction-studio" style={{ marginBottom: '4rem' }}>
            <PredictionStudio 
              overview={analysis.overview} 
              prediction={analysis.prediction}
              loading={analysis.loading.prediction}
              error={analysis.errors.prediction}
              onPredict={analysis.runPrediction}
            />
          </div>

          <div id="export-report" style={{ paddingBottom: '4rem' }}>
            <ReportButtons sessionId={analysis.session} />
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
