import io
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "active_sessions" in data

def test_sample_datasets_full_flow():
    samples = ["retail_sales", "hr_analytics", "customer_churn"]
    
    for sample in samples:
        # 1. Load sample
        res = client.post(f"/api/samples/{sample}")
        assert res.status_code == 200
        data = res.json()
        assert "session_id" in data
        assert data["rows"] > 0
        assert data["columns"] > 0
        assert len(data["top3"]) > 0
        assert 0 <= data["quality_score"] <= 100
        
        session_id = data["session_id"]
        
        # 2. Get Overview
        res_ov = client.get(f"/api/overview/{session_id}")
        assert res_ov.status_code == 200
        overview = res_ov.json()
        assert "column_types" in overview
        assert len(overview["preview"]) > 0
        
        # 3. Get Insights
        res_ins = client.get(f"/api/insights/{session_id}")
        assert res_ins.status_code == 200
        insights_data = res_ins.json()
        assert len(insights_data["all_insights"]) > 0
        
        # 4. Get Charts
        res_ch = client.get(f"/api/charts/{session_id}")
        assert res_ch.status_code == 200
        charts = res_ch.json()
        assert isinstance(charts, list)
        
        # 5. Get Recommendations
        res_rec = client.get(f"/api/recommendations/{session_id}")
        assert res_rec.status_code == 200
        assert len(res_rec.json()["recommendations"]) > 0
        
        # 6. Run Prediction on first numerical/categorical column
        target_col = list(overview["column_types"].keys())[1]
        res_pred = client.post(f"/api/predict/{session_id}", json={"target_column": target_col})
        assert res_pred.status_code == 200
        pred_data = res_pred.json()
        assert "best_model" in pred_data
        assert "plain_english" in pred_data
        
        # 7. HTML Report
        res_html = client.get(f"/api/report/html/{session_id}")
        assert res_html.status_code == 200
        assert "text/html" in res_html.headers["content-type"]
        
        # 8. PDF Report
        res_pdf = client.get(f"/api/report/pdf/{session_id}")
        assert res_pdf.status_code == 200
        assert res_pdf.headers["content-type"] == "application/pdf"
        assert res_pdf.content.startswith(b"%PDF")

def test_file_upload_csv():
    csv_content = b"Date,Sales,Region\n2024-01-01,100,North\n2024-01-02,150,South\n2024-01-03,200,East"
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}
    
    response = client.post("/api/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == 3
    assert data["columns"] == 3
    assert "session_id" in data

def test_file_upload_invalid_extension():
    fake_file = {"file": ("script.py", io.BytesIO(b"print('hello')"), "text/plain")}
    response = client.post("/api/upload", files=fake_file)
    assert response.status_code == 400
    assert "supported" in response.json()["detail"].lower()

def test_missing_session_404():
    fake_session_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/overview/{fake_session_id}")
    assert response.status_code == 404
