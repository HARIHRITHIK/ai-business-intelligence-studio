from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse, Response
from pydantic import BaseModel
import pandas as pd
import uuid
import os
import io
import time

from core.profiler import DataProfiler
from core.insight_engine import InsightEngine
from core.nlg import NLGEngine
from core.chart_builder import ChartBuilder
from core.predictor import AutoMLPredictor
from core.reporter import ReportGenerator

# We will import the session dictionary from main
# Alternatively, use a local reference and let main import it
# For simplicity and avoiding circular imports, we'll assume a global dict is passed or we define it here and import in main.
sessions = {}

router = APIRouter()

profiler = DataProfiler()
insight_engine = InsightEngine()
nlg = NLGEngine()
chart_builder = ChartBuilder()
predictor = AutoMLPredictor()
reporter = ReportGenerator()

class PredictRequest(BaseModel):
    target_column: str

def process_dataframe(df: pd.DataFrame, filename: str) -> dict:
    session_id = str(uuid.uuid4())
    
    # 1. Profile
    profile = profiler.profile(df)
    
    # 2. Insights
    all_insights = insight_engine.generate(df, profile)
    top3_insights = insight_engine.top3(all_insights)
    
    # 3. Recommendations
    recommendations = nlg.recommendation_from_insights(all_insights, profile)
    
    # 4. Charts
    charts = chart_builder.build_charts(df, profile, top3_insights)
    
    # Store session
    sessions[session_id] = {
        "filename": filename,
        "df": df,
        "profile": profile,
        "insights": all_insights,
        "top3": top3_insights,
        "recommendations": recommendations,
        "charts": charts,
        "prediction": None,
        "created_at": time.time(),
    }
    
    return {
        "session_id": session_id,
        "filename": filename,
        "rows": profile['rows'],
        "columns": profile['columns'],
        "top3": top3_insights,
        "quality_score": profile['quality_score']
    }

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported")
        
    try:
        max_size = 50 * 1024 * 1024  # 50MB
        chunks = []
        bytes_read = 0
        while True:
            chunk = await file.read(1024 * 1024)  # 1MB chunk
            if not chunk:
                break
            bytes_read += len(chunk)
            if bytes_read > max_size:
                raise HTTPException(status_code=400, detail="File too large (max 50MB)")
            chunks.append(chunk)
            
        content = b"".join(chunks)
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
            
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded dataset contains no data rows")
            
        return process_dataframe(df, file.filename)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.post("/samples/{name}")
async def load_sample(name: str):
    file_path = f"data/samples/{name}.csv"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sample not found")
        
    try:
        df = pd.read_csv(file_path)
        return process_dataframe(df, f"{name}.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading sample: {str(e)}")

@router.get("/overview/{session_id}")
async def get_overview(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]["profile"]

@router.get("/insights/{session_id}")
async def get_insights(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "top3": sessions[session_id]["top3"],
        "all_insights": sessions[session_id]["insights"]
    }

@router.get("/charts/{session_id}")
async def get_charts(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]["charts"]

@router.get("/recommendations/{session_id}")
async def get_recommendations(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"recommendations": sessions[session_id]["recommendations"]}

@router.post("/predict/{session_id}")
async def run_predict(session_id: str, request: PredictRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session = sessions[session_id]
    try:
        prediction_results = predictor.predict(session["df"], request.target_column)
        session["prediction"] = prediction_results
        return prediction_results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

@router.get("/report/html/{session_id}")
async def download_html_report(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    try:
        html_content = reporter.generate_html(sessions[session_id])
        return HTMLResponse(
            content=html_content,
            headers={
                "Content-Disposition": f"inline; filename=report_{session_id[:8]}.html"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@router.get("/report/pdf/{session_id}")
async def download_pdf_report(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    try:
        pdf_bytes = reporter.generate_pdf(sessions[session_id])
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=report_{session_id[:8]}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
