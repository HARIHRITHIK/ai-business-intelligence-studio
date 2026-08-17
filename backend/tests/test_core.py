import pytest
import pandas as pd
import numpy as np
from core.profiler import DataProfiler
from core.insight_engine import InsightEngine
from core.predictor import AutoMLPredictor
from core.nlg import NLGEngine
from core.reporter import ReportGenerator
from core.chart_builder import ChartBuilder

@pytest.fixture
def sample_df():
    """Create a realistic test DataFrame with predictable statistical patterns."""
    np.random.seed(42)
    n = 100
    dates = pd.date_range(start='2024-01-01', periods=n, freq='D')
    revenue = np.linspace(1000, 5000, n) + np.random.normal(0, 100, n)
    # Inject 2 extreme outliers for anomaly detection
    revenue[10] = 15000
    revenue[20] = 16000
    
    ad_spend = revenue * 0.2 + np.random.normal(0, 50, n)
    category = np.random.choice(['Electronics', 'Clothing', 'Home'], size=n, p=[0.6, 0.2, 0.2])
    churn = np.random.choice(['Yes', 'No'], size=n, p=[0.25, 0.75])

    return pd.DataFrame({
        'Date': dates,
        'Revenue': revenue,
        'Ad_Spend': ad_spend,
        'Category': category,
        'Churn': churn,
        'Customer_ID': [f'CUST_{i:04d}' for i in range(n)]
    })

def test_data_profiler_roles_and_quality(sample_df):
    profiler = DataProfiler()
    profile = profiler.profile(sample_df)

    assert profile['rows'] == 100
    assert profile['columns'] == 6
    assert 0 <= profile['quality_score'] <= 100

    roles = profile['column_types']
    assert roles['Date'] == 'datetime'
    assert roles['Revenue'] == 'numerical'
    assert roles['Category'] == 'categorical'
    assert roles['Customer_ID'] == 'id'

    assert len(profile['preview']) == 10
    assert 'Revenue' in profile['column_profiles']
    assert 'mean' in profile['column_profiles']['Revenue']

def test_insight_engine_discovery(sample_df):
    profiler = DataProfiler()
    profile = profiler.profile(sample_df)
    
    engine = InsightEngine()
    insights = engine.generate(sample_df, profile)

    assert len(insights) > 0
    top3 = engine.top3(insights)
    assert len(top3) <= 3

    # Verify every insight has NLG strings
    for ins in insights:
        assert 'headline' in ins and len(ins['headline']) > 0
        assert 'explanation' in ins and len(ins['explanation']) > 0
        assert 'business_implication' in ins and len(ins['business_implication']) > 0
        assert 'severity' in ins

    # Check for anomaly detection on the injected outliers
    anomaly_insights = [i for i in insights if i.get('type') == 'anomaly']
    assert len(anomaly_insights) > 0

    # Check for correlation detection (Revenue & Ad_Spend)
    corr_insights = [i for i in insights if i.get('type') == 'correlation']
    assert len(corr_insights) > 0

def test_automl_predictor_regression(sample_df):
    predictor = AutoMLPredictor()
    result = predictor.predict(sample_df, target_col='Revenue')

    assert result['task_type'] == 'regression'
    assert result['metric_name'] == 'R² Score'
    assert result['metric_value'] is not None
    assert len(result['feature_importances']) > 0
    assert 'plain_english' in result
    assert result['best_model'] in ['Linear Regression', 'Random Forest']

def test_automl_predictor_classification(sample_df):
    predictor = AutoMLPredictor()
    result = predictor.predict(sample_df, target_col='Churn')

    assert result['task_type'] == 'classification'
    assert result['metric_name'] == 'Accuracy'
    assert result['metric_value'] is not None
    assert len(result['feature_importances']) > 0
    assert result['best_model'] in ['Logistic Regression', 'Random Forest']

def test_chart_builder_and_pdf_generation(sample_df):
    profiler = DataProfiler()
    profile = profiler.profile(sample_df)
    
    engine = InsightEngine()
    insights = engine.generate(sample_df, profile)
    top3 = engine.top3(insights)
    
    nlg = NLGEngine()
    recs = nlg.recommendation_from_insights(insights, profile)

    cb = ChartBuilder()
    charts = cb.build_charts(sample_df, profile, top3)
    assert len(charts) > 0

    session_data = {
        'filename': 'test_data.csv',
        'profile': profile,
        'top3': top3,
        'insights': insights,
        'recommendations': recs,
        'charts': charts
    }

    reporter = ReportGenerator()
    html = reporter.generate_html(session_data)
    assert '<html' in html.lower()
    assert 'Top Findings' in html

    pdf_bytes = reporter.generate_pdf(session_data)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 10000  # Non-trivial PDF file with embedded charts
    assert pdf_bytes.startswith(b'%PDF')
