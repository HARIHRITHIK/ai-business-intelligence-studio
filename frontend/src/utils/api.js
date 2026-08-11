import axios from 'axios';

const client = axios.create({
  baseURL: '/api'
});

const extractError = (error, fallback) =>
  error.response?.data?.detail || error.response?.data?.message || fallback;

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const res = await client.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  } catch (error) {
    throw new Error(extractError(error, 'Failed to upload file. Please check the file format.'));
  }
};

export const loadSample = async (name) => {
  try {
    const res = await client.post(`/samples/${name}`);
    return res.data;
  } catch (error) {
    throw new Error(extractError(error, 'Failed to load sample dataset.'));
  }
};

export const getOverview = async (sessionId) => {
  try {
    const res = await client.get(`/overview/${sessionId}`);
    return res.data;
  } catch (error) {
    throw new Error(extractError(error, 'Failed to load data overview.'));
  }
};

export const getInsights = async (sessionId) => {
  try {
    const res = await client.get(`/insights/${sessionId}`);
    return res.data;
  } catch (error) {
    throw new Error(extractError(error, 'Failed to generate insights.'));
  }
};

export const getCharts = async (sessionId) => {
  try {
    const res = await client.get(`/charts/${sessionId}`);
    return res.data;
  } catch (error) {
    throw new Error(extractError(error, 'Failed to load charts.'));
  }
};

export const getRecommendations = async (sessionId) => {
  try {
    const res = await client.get(`/recommendations/${sessionId}`);
    return res.data;
  } catch (error) {
    throw new Error(extractError(error, 'Failed to generate recommendations.'));
  }
};

export const runPrediction = async (sessionId, targetCol) => {
  try {
    const res = await client.post(`/predict/${sessionId}`, { target_column: targetCol });
    return res.data;
  } catch (error) {
    throw new Error(extractError(error, 'Pattern analysis failed. Try a different target column.'));
  }
};

export const getReportUrl = (sessionId, format = 'html') => {
  return `/api/report/${format}/${sessionId}`;
};
