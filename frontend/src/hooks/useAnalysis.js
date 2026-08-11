import { useState } from 'react';
import * as api from '../utils/api';

export function useAnalysis() {
  const [session, setSession] = useState(null);
  const [topFindings, setTopFindings] = useState([]);
  const [overview, setOverview] = useState(null);
  const [insights, setInsights] = useState([]);
  const [charts, setCharts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [prediction, setPrediction] = useState(null);

  const [loading, setLoading] = useState({
    upload: false,
    overview: false,
    insights: false,
    charts: false,
    recommendations: false,
    prediction: false
  });

  const [errors, setErrors] = useState({
    upload: null,
    overview: null,
    insights: null,
    charts: null,
    recommendations: null,
    prediction: null
  });

  const updateLoading = (key, val) => setLoading(p => ({ ...p, [key]: val }));
  const updateError = (key, val) => setErrors(p => ({ ...p, [key]: val }));

  const fetchParallelData = (sessionId) => {
    // Overview
    updateLoading('overview', true);
    api.getOverview(sessionId)
      .then(res => setOverview(res))
      .catch(e => updateError('overview', e.message))
      .finally(() => updateLoading('overview', false));

    // Insights
    updateLoading('insights', true);
    api.getInsights(sessionId)
      .then(res => setInsights(res?.all_insights || []))
      .catch(e => updateError('insights', e.message))
      .finally(() => updateLoading('insights', false));

    // Charts
    updateLoading('charts', true);
    api.getCharts(sessionId)
      .then(res => setCharts(res || []))
      .catch(e => updateError('charts', e.message))
      .finally(() => updateLoading('charts', false));

    // Recommendations
    updateLoading('recommendations', true);
    api.getRecommendations(sessionId)
      .then(res => setRecommendations(res?.recommendations || []))
      .catch(e => updateError('recommendations', e.message))
      .finally(() => updateLoading('recommendations', false));
  };

  const uploadFile = async (file) => {
    updateLoading('upload', true);
    updateError('upload', null);
    try {
      const data = await api.uploadFile(file);
      setSession(data.session_id);
      setTopFindings(data.top3 || []);
      fetchParallelData(data.session_id);
      return data;
    } catch (e) {
      updateError('upload', e.message);
      throw e;
    } finally {
      updateLoading('upload', false);
    }
  };

  const loadSample = async (name) => {
    updateLoading('upload', true);
    updateError('upload', null);
    try {
      const data = await api.loadSample(name);
      setSession(data.session_id);
      setTopFindings(data.top3 || []);
      fetchParallelData(data.session_id);
      return data;
    } catch (e) {
      updateError('upload', e.message);
      throw e;
    } finally {
      updateLoading('upload', false);
    }
  };

  const runPrediction = async (targetCol) => {
    if (!session) return;
    updateLoading('prediction', true);
    updateError('prediction', null);
    try {
      const data = await api.runPrediction(session, targetCol);
      setPrediction(data);
      return data;
    } catch (e) {
      updateError('prediction', e.message);
      throw e;
    } finally {
      updateLoading('prediction', false);
    }
  };

  const resetAnalysis = () => {
    setSession(null);
    setTopFindings([]);
    setOverview(null);
    setInsights([]);
    setCharts([]);
    setRecommendations([]);
    setPrediction(null);
    setErrors({
      upload: null,
      overview: null,
      insights: null,
      charts: null,
      recommendations: null,
      prediction: null
    });
  };

  return {
    session,
    topFindings,
    overview,
    insights,
    charts,
    recommendations,
    prediction,
    uploadFile,
    loadSample,
    runPrediction,
    resetAnalysis,
    loading,
    errors
  };
}
